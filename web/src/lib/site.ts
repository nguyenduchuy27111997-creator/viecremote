/** Một nguồn sự thật cho URL gốc. Sitemap, ảnh OG và metadata đều cần nó. */
export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL?.replace(/\/$/, "") || "https://viecremote.com"

export const SITE_NAME = "viecremote"
