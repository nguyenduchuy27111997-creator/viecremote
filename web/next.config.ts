import type { NextConfig } from "next"

/**
 * KHÔNG bật `cacheComponents`.
 *
 * Next 16 Cache Components (PPR + "use cache") KHÔNG chạy được trên runtime
 * Cloudflare Workers. Next tự cảnh báo lúc chạy — "cannot guarantee that Cache
 * Components will run as expected due to the current runtime's implementation
 * of setTimeout()" — và worker treo, trả 500 ở MỌI route.
 *
 * Đã thử workaround `enableCacheInterception: false` (opennextjs-cloudflare
 * #1223): không đủ, vẫn treo. Gốc rễ là setTimeout, không phải cache interception.
 *
 * Nên dùng ISR thường: `export const revalidate = N` ở từng route. Mất khả năng
 * stream vỏ tĩnh trước, nhưng kho vốn dựng lại mỗi ngày nên gần như không mất gì.
 */
const nextConfig: NextConfig = {
  // Pivot 24/08: trục sản phẩm phía cầu đổi từ Việt Nam sang Đông Nam Á.
  // URL cũ đã nằm trong sitemap đã nộp và có thể đã được chia sẻ — chuyển
  // hướng vĩnh viễn thay vì để 404 và mất hết giá trị đã tích.
  async redirects() {
    return [
      { source: "/hiring-in-vietnam", destination: "/hiring-in-sea/vietnam", permanent: true },
      { source: "/hiring-in-vietnam/:slug", destination: "/company/:slug", permanent: true },
    ]
  },

  // Bật Cache Components: PPR thành mặc định, và caching chuyển sang opt-in
  // qua directive "use cache" thay vì ngầm định.
  // D1 cục bộ (miniflare) là một tiến trình duy nhất; 11 worker build đập cùng
  // lúc làm nó trả "internal error". Build chạy vài giây nên nối tiếp là đủ.
  experimental: { cpus: 1 },
}

export default nextConfig

// Dev: nạp binding Cloudflare (D1) vào `next dev`, nếu không getCloudflareContext rỗng.
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare"
initOpenNextCloudflareForDev()
