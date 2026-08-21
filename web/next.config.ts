import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  // Bật Cache Components: PPR thành mặc định, và caching chuyển sang opt-in
  // qua directive "use cache" thay vì ngầm định.
  // Cache Components: PPR thành mặc định, caching chuyển sang opt-in qua "use cache".
  cacheComponents: true,
  // Cần cả hai để có hành vi kiểu ISR: Cache Components dựng App Shell,
  // Partial Prefetching nâng nó thành trang đầy đủ khi đã biết params.
  // Nhờ đó build chỉ dựng sẵn ~200 công ty, 2.200 công ty còn lại dựng khi có
  // lượt xem đầu tiên rồi nằm trong cache — build không phình theo kho.
  partialPrefetching: true,
  // D1 cục bộ (miniflare) là một tiến trình duy nhất; 11 worker build đập cùng
  // lúc làm nó trả "internal error". Build chạy vài giây nên nối tiếp là đủ.
  experimental: { cpus: 1 },
}

export default nextConfig

// Dev: nạp binding Cloudflare (D1) vào `next dev`, nếu không getCloudflareContext rỗng.
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare"
initOpenNextCloudflareForDev()
