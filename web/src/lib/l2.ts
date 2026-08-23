import "server-only"

/**
 * CÔNG TẮC L2 — mặc định TẮT, và tắt là trạng thái đúng.
 *
 * L2 (mạng lưới: hồ sơ kỹ sư, đồng ý theo từng công ty, giới thiệu có thu phí)
 * KHÔNG được vận hành cho tới khi đủ ba thứ:
 *
 *   1. Giấy phép hoạt động dịch vụ việc làm — NĐ 352/2025 Điều 14–15.
 *      Luật Việc làm Điều 27.4 nêu đích danh phương thức thương mại điện tử.
 *   2. Hồ sơ đánh giá tác động chuyển dữ liệu xuyên biên giới đã gửi Bộ Công an
 *      — Luật 91/2025 Điều 20.2, trong 60 ngày kể từ lần chuyển ĐẦU TIÊN.
 *   3. Hai câu pháp lý còn mở có lời giải — legal-research.md Mục 7.
 *
 * Vì sao là biến môi trường chứ không phải cờ trong cơ sở dữ liệu: cờ trong DB
 * bật được bằng một câu UPDATE lúc 2 giờ sáng. Biến môi trường buộc phải deploy
 * lại, tức là có người xem diff.
 *
 * Bật KHÔNG phải là quyết định kỹ thuật. Chế tài nếu sai: 10 lần khoản thu,
 * sàn 3 tỷ, có thể truy cứu hình sự (Luật 91/2025 Điều 8).
 */
export const L2_ON = process.env.L2_ENABLED === "yes-licensed-and-filed"

/** Ném 503 ở tầng API. Dùng cho mọi route ghi dữ liệu L2. */
export function assertL2() {
  if (!L2_ON) {
    throw new Response(
      JSON.stringify({
        error: "L2 chưa mở",
        detail:
          "Mạng lưới chưa vận hành. Cần Giấy phép dịch vụ việc làm và hồ sơ "
          + "chuyển dữ liệu xuyên biên giới trước. Xem legal-research.md.",
      }),
      { status: 503, headers: { "content-type": "application/json" } },
    )
  }
}
