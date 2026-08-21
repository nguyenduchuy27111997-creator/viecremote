import "server-only"
import { getCloudflareContext } from "@opennextjs/cloudflare"

/**
 * Xác thực khoá API.
 *
 * Lưu SHA-256 chứ không lưu khoá thô: nếu cơ sở dữ liệu rò, kẻ lấy được vẫn
 * không gọi API được. Đây là mặt hàng của giai đoạn 2 — mất nó là mất sản phẩm.
 *
 * Chưa có khoá nào trong bảng ⇒ API mở, nhưng bị giới hạn nhịp chặt hơn (xem
 * route). Như vậy giai đoạn 0/1 vẫn công khai được mà không phải sửa code khi
 * bắt đầu bán.
 */
export async function sha256(s: string) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("")
}

export type Caller = { tier: "key"; label: string } | { tier: "anon" }

export async function authenticate(req: Request): Promise<Caller | null> {
  const raw = req.headers.get("x-api-key")?.trim()
  const { env } = await getCloudflareContext({ async: true })

  if (!raw) {
    const any = await env.DB.prepare("SELECT 1 FROM api_key WHERE revoked = 0").first()
    // Có khoá đang hoạt động ⇒ API đã ở chế độ bán, không cho gọi ẩn danh nữa.
    return any ? null : { tier: "anon" }
  }

  const row = await env.DB
    .prepare("SELECT label FROM api_key WHERE hash = ? AND revoked = 0")
    .bind(await sha256(raw))
    .first<{ label: string }>()
  return row ? { tier: "key", label: row.label } : null
}
