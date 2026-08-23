import type { MetadataRoute } from "next"
import { all } from "@/lib/db"
import { SITE_URL } from "@/lib/site"

// Kho dựng lại mỗi ngày; ISR thường thay cho "use cache".
export const revalidate = 86400

/**
 * Sứ mệnh là để người ta TÌM THẤY sự thật. Không có sitemap thì 3.666 trang
 * công ty phải chờ Google tự bò tới — mất hàng tháng, và trang sâu có thể
 * không bao giờ được lập chỉ mục.
 *
 * Giới hạn của giao thức là 50.000 URL/tệp. Nay ~4.100 nên một tệp đủ; khi kho
 * lên 10.000 công ty vẫn còn dư. Vượt ngưỡng thì phải chuyển sang generateSitemaps.
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const now = new Date()

  const fixed: MetadataRoute.Sitemap = [
    { url: `${SITE_URL}/`, lastModified: now, changeFrequency: "daily", priority: 1 },
    { url: `${SITE_URL}/tin-mo`, lastModified: now, changeFrequency: "daily", priority: 0.9 },
    { url: `${SITE_URL}/vi-sao-bi-loai`, lastModified: now, changeFrequency: "daily", priority: 0.8 },
    { url: `${SITE_URL}/khoa`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${SITE_URL}/lam-gi`, lastModified: now, changeFrequency: "monthly", priority: 0.9 },
    { url: `${SITE_URL}/hiring-in-vietnam`, lastModified: now, changeFrequency: "weekly", priority: 0.9 },
    { url: `${SITE_URL}/api`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${SITE_URL}/rieng-tu`, lastModified: now, changeFrequency: "monthly", priority: 0.3 },
    { url: `${SITE_URL}/phuong-phap`, lastModified: now, changeFrequency: "weekly", priority: 0.7 },
  ]

  // Công ty tuyển được đứng trước và ưu tiên cao hơn: đó là trang đáng lập chỉ
  // mục nhất, và nếu Google chỉ bò một phần thì nên bò phần đó trước.
  const companies = await all<{ slug: string; verdict: string }>(
    `SELECT slug, verdict FROM company
     ORDER BY CASE verdict WHEN 'ok' THEN 0 WHEN 'unk' THEN 1 ELSE 2 END, n_global DESC`,
  )
  const codes = await all<{ code: string }>("SELECT DISTINCT code FROM locked")
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
    ...codes.map((c) => ({
      url: `${SITE_URL}/khoa/${c.code.toLowerCase()}`,
      lastModified: now,
      changeFrequency: "weekly" as const,
      priority: 0.6,
    })),
    ...jobs.map((j) => ({
      url: `${SITE_URL}/viec/${j.id}`,
      lastModified: now,
      changeFrequency: "daily" as const,
      priority: 0.6,
    })),
  ]
}
