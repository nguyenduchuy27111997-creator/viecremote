import type { MetadataRoute } from "next"
import { SITE_URL } from "@/lib/site"

/**
 * Cho phép lập chỉ mục toàn bộ. Chặn /api — đó là mặt hàng của giai đoạn 2,
 * không phải nội dung để Google đọc.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: "*", allow: "/", disallow: ["/api/"] }],
    sitemap: `${SITE_URL}/sitemap.xml`,
  }
}
