import { getCloudflareContext } from "@opennextjs/cloudflare"

/**
 * Yêu cầu báo cáo thị trường từ công ty nước ngoài — sản phẩm Đ3.
 *
 * Khác /api/dang-ky ở chỗ KHÔNG cần double opt-in: đây không phải đăng ký nhận
 * tin định kỳ mà là một yêu cầu đơn lẻ, trả lời một lần rồi thôi. Gửi thư xác
 * nhận cho một yêu cầu B2B là thêm ma sát không mua được gì.
 *
 * Vẫn là dữ liệu cá nhân (email công việc gắn với một người), nên vẫn: chỉ lưu
 * đúng thứ cần để trả lời, không IP, không dấu vết, xoá khi được yêu cầu.
 */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/

export async function POST(req: Request) {
  let body: Record<string, unknown>
  try {
    body = await req.json()
  } catch {
    return Response.json({ error: "Malformed request body" }, { status: 400 })
  }

  const company = String(body.company ?? "").trim().slice(0, 120)
  const email = String(body.email ?? "").trim().toLowerCase().slice(0, 254)
  const role = String(body.role ?? "").trim().slice(0, 200) || null
  const note = String(body.note ?? "").trim().slice(0, 1000) || null

  if (!company) return Response.json({ error: "Company is required" }, { status: 400 })
  if (!EMAIL_RE.test(email)) return Response.json({ error: "Invalid email address" }, { status: 400 })

  // Cùng hai lớp chống bot như các form khác — không lớp nào cần cookie.
  if (String(body.website ?? "")) return Response.json({ ok: true })
  if (Number(body.elapsed ?? 0) < 2000) return Response.json({ ok: true })

  const { env } = await getCloudflareContext({ async: true })
  await env.DB.prepare(
    "INSERT INTO inquiry (company, email, role, note, created_at) VALUES (?,?,?,?,?)",
  )
    .bind(company, email, role, note, new Date().toISOString())
    .run()

  return Response.json({ ok: true })
}
