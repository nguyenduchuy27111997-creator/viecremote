import { getCloudflareContext } from "@opennextjs/cloudflare"
import { SITE_URL } from "@/lib/site"

/**
 * Đăng ký nhận tin — DOUBLE OPT-IN.
 *
 * Email LÀ dữ liệu cá nhân theo Luật 91/2025, khác mọi dữ liệu khác trong kho
 * (vốn chỉ nói về công ty). Nên ở đây:
 *   - chỉ lưu email + token, không lưu IP, không lưu tên
 *   - chưa xác nhận thì KHÔNG được coi là đã đăng ký
 *   - mọi thư đều có đường huỷ một cú bấm
 *
 * Cloudflare Email Service chỉ dùng cho thư GIAO DỊCH — thư xác nhận thì đúng
 * mục đích. BẢN TIN thật sự sau này phải dùng nền tảng khác.
 */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/

export async function POST(req: Request) {
  let body: Record<string, unknown>
  try {
    body = await req.json()
  } catch {
    return Response.json({ error: "Thân yêu cầu không hợp lệ" }, { status: 400 })
  }

  const email = String(body.email ?? "").trim().toLowerCase().slice(0, 254)
  if (!EMAIL_RE.test(email))
    return Response.json({ error: "Địa chỉ email không hợp lệ" }, { status: 400 })

  // Cùng ba lớp chống bot như form báo sai, không lớp nào cần cookie.
  if (String(body.website ?? "")) return Response.json({ ok: true })
  if (Number(body.elapsed ?? 0) < 2000) return Response.json({ ok: true })

  const { env } = await getCloudflareContext({ async: true })
  const db = env.DB

  const existing = await db
    .prepare("SELECT token, confirmed FROM subscriber WHERE email = ?")
    .bind(email)
    .first<{ token: string; confirmed: number }>()

  // Đã xác nhận rồi thì im lặng thành công — không tiết lộ ai đã đăng ký.
  if (existing?.confirmed) return Response.json({ ok: true })

  const token = existing?.token ?? crypto.randomUUID().replace(/-/g, "")
  if (!existing) {
    await db
      .prepare("INSERT INTO subscriber (email, token, created_at) VALUES (?,?,?)")
      .bind(email, token, new Date().toISOString())
      .run()
  }

  const link = `${SITE_URL}/xac-nhan?t=${token}`
  const mailer = (env as { EMAIL?: { send: (m: unknown) => Promise<unknown> } }).EMAIL
  if (!mailer) {
    // Chưa gắn binding: vẫn lưu, nhưng nói THẲNG là chưa gửi được thư.
    // Im lặng ở đây sẽ tạo một danh sách chờ mà không ai xác nhận được.
    return Response.json(
      { ok: true, pending: true, note: "Chưa cấu hình gửi thư — bản ghi đã lưu, chưa gửi xác nhận." },
      { status: 202 },
    )
  }

  await mailer.send({
    to: email,
    from: { email: "xacnhan@viecremote.com", name: "viecremote" },
    subject: "Xác nhận đăng ký nhận tin",
    text: `Bấm vào đường dẫn này để xác nhận đăng ký:\n\n${link}\n\n`
      + `Nếu bạn không đăng ký, bỏ qua thư này — không có gì xảy ra và địa chỉ của bạn `
      + `sẽ bị xoá sau 7 ngày.`,
    html: `<p>Bấm để xác nhận đăng ký nhận tin từ viecremote:</p>`
      + `<p><a href="${link}">${link}</a></p>`
      + `<p style="color:#666;font-size:13px">Nếu bạn không đăng ký, bỏ qua thư này — `
      + `không có gì xảy ra và địa chỉ của bạn sẽ bị xoá sau 7 ngày.</p>`,
  })

  return Response.json({ ok: true })
}
