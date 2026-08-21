import type { MetadataRoute } from "next"
import { SITE_URL } from "@/lib/site"

/**
 * Cho phép lập chỉ mục toàn bộ, kể cả /api (trang tài liệu — nó chính là trang
 * bán hàng). Chặn các ĐIỂM CUỐI trả JSON và các trang nội bộ.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{
      userAgent: "*",
      allow: "/",
      disallow: ["/api/companies", "/api/bao-sai", "/api/dang-ky",
                 "/bao-sai", "/xac-nhan", "/huy-dang-ky"],
    }],
    sitemap: `${SITE_URL}/sitemap.xml`,
  }
}
