import { getCloudflareContext } from "@opennextjs/cloudflare"

/**
 * Nhận báo sai nhãn.
 *
 * KHÔNG thu dữ liệu cá nhân nào: không email, không tài khoản, không lưu IP.
 * Đó là lựa chọn có chủ ý — giữ nguyên miễn trừ DPO/DPIA của Nghị định
 * 356/2025, và không có gì để rò rỉ.
 *
 * Chống spam ba lớp, không lớp nào cần cookie:
 *   1. Turnstile (nếu đã cấu hình khoá) — Cloudflare, không cookie
 *   2. Honeypot: ô ẩn mà người thật không bao giờ điền
 *   3. Thời gian: gửi dưới 2 giây sau khi mở form thì gần như chắc là bot
 */
const REASONS = new Set(["nhan-sai", "tin-da-dong", "trich-dan-sai", "khac"])
const MAX_NOTE = 600

export async function POST(req: Request) {
  let body: Record<string, unknown>
  try {
    body = await req.json()
  } catch {
    return Response.json({ error: "Thân yêu cầu không hợp lệ" }, { status: 400 })
  }

  const kind = String(body.kind ?? "")
  const ref = String(body.ref ?? "").slice(0, 200)
  const reason = String(body.reason ?? "")
  const note = String(body.note ?? "").slice(0, MAX_NOTE).trim()

  if (!["job", "company"].includes(kind) || !ref)
    return Response.json({ error: "Thiếu thông tin tin hoặc công ty" }, { status: 400 })
  if (!REASONS.has(reason))
    return Response.json({ error: "Lý do không hợp lệ" }, { status: 400 })

  // Honeypot: người thật không thấy ô này nên không bao giờ điền.
  if (String(body.website ?? "")) return Response.json({ ok: true })
  // Quá nhanh để là người đọc rồi gõ.
  if (Number(body.elapsed ?? 0) < 2000) return Response.json({ ok: true })

  const { env } = await getCloudflareContext({ async: true })
  const secret = (env as { TURNSTILE_SECRET?: string }).TURNSTILE_SECRET
  if (secret) {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ secret, response: String(body.token ?? "") }),
    })
    const v = (await r.json()) as { success?: boolean }
    if (!v.success) return Response.json({ error: "Không xác minh được" }, { status: 400 })
  }

  const db = env.DB
  // Tham chiếu phải tồn tại — nếu không thì đây là rác, hoặc là dò tìm.
  const exists = await db
    .prepare(kind === "job" ? "SELECT 1 FROM job WHERE id=?" : "SELECT 1 FROM company WHERE slug=?")
    .bind(ref)
    .first()
  if (!exists) return Response.json({ error: "Không có tin hoặc công ty này" }, { status: 404 })

  await db
    .prepare("INSERT INTO report (kind, ref, reason, note, created_at) VALUES (?,?,?,?,?)")
    .bind(kind, ref, reason, note || null, new Date().toISOString())
    .run()

  return Response.json({ ok: true })
}
