import type { MetadataRoute } from "next"
import { cacheLife } from "next/cache"
import { all } from "@/lib/db"
import { SITE_URL } from "@/lib/site"

/**
 * Sứ mệnh là để người ta TÌM THẤY sự thật. Không có sitemap thì 3.666 trang
 * công ty phải chờ Google tự bò tới — mất hàng tháng, và trang sâu có thể
 * không bao giờ được lập chỉ mục.
 *
 * Giới hạn của giao thức là 50.000 URL/tệp. Nay ~4.100 nên một tệp đủ; khi kho
 * lên 10.000 công ty vẫn còn dư. Vượt ngưỡng thì phải chuyển sang generateSitemaps.
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // `revalidate` không dùng chung với cacheComponents — dùng "use cache".
  "use cache"
  cacheLife("days")
  const now = new Date()

  const fixed: MetadataRoute.Sitemap = [
    { url: `${SITE_URL}/`, lastModified: now, changeFrequency: "daily", priority: 1 },
    { url: `${SITE_URL}/tin-mo`, lastModified: now, changeFrequency: "daily", priority: 0.9 },
    { url: `${SITE_URL}/vi-sao-bi-loai`, lastModified: now, changeFrequency: "daily", priority: 0.8 },
    { url: `${SITE_URL}/phuong-phap`, lastModified: now, changeFrequency: "weekly", priority: 0.7 },
  ]

  // Công ty tuyển được đứng trước và ưu tiên cao hơn: đó là trang đáng lập chỉ
  // mục nhất, và nếu Google chỉ bò một phần thì nên bò phần đó trước.
  const companies = await all<{ slug: string; verdict: string }>(
    `SELECT slug, verdict FROM company
     ORDER BY CASE verdict WHEN 'ok' THEN 0 WHEN 'unk' THEN 1 ELSE 2 END, n_global DESC`,
  )
  const jobs = await all<{ id: string }>(
    "SELECT id FROM job WHERE scope IN ('worldwide','vn') ORDER BY id",
  )

  return [
    ...fixed,
    ...companies.map((c) => ({
      url: `${SITE_URL}/cong-ty/${c.slug}`,
      lastModified: now,
      changeFrequency: "weekly" as const,
      priority: c.verdict === "ok" ? 0.8 : 0.4,
    })),
    ...jobs.map((j) => ({
      url: `${SITE_URL}/viec/${j.id}`,
      lastModified: now,
      changeFrequency: "daily" as const,
      priority: 0.6,
    })),
  ]
}
