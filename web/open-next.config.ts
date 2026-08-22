import { defineCloudflareConfig } from "@opennextjs/cloudflare"

/**
 * `enableCacheInterception: false` — bắt buộc với Next 16 + cacheComponents.
 *
 * Bug đã biết: opennextjs-cloudflare#1223. Với cache interception bật, yêu cầu
 * RSC tới route đã cache PPR làm worker treo và trả 500 ("code had hung and
 * would never generate a response"). Tắt nó thì route đi thẳng vào runtime.
 *
 * Đổi lại: mất một tầng cache ở biên. Chấp nhận được — kho dựng lại mỗi ngày
 * nên vốn không cần revalidate lúc chạy.
 */
export default defineCloudflareConfig({
  enableCacheInterception: false,
})
