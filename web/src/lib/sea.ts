/**
 * Đông Nam Á — trục sản phẩm phía cầu sau khi pivot (24/08).
 *
 * Vì sao đổi trục từ Việt Nam sang khu vực:
 *   - Ngách rộng gấp đôi: 133 công ty chỉ mở ĐÚNG MỘT nước ĐNA, so với 71
 *     công ty ở ĐNA mà đóng với riêng Việt Nam.
 *   - Câu hỏi sắc hơn. "Sao không tuyển ở Việt Nam" là lời cầu xin; "bạn ở
 *     Singapore rồi, sao chỉ Singapore" là một khoảng trống họ tự thấy.
 *   - Ra xa Điều 27.1(c) Luật Việc làm hơn: nghiên cứu chính sách tuyển dụng
 *     KHU VỰC của công ty nước ngoài, không phải thông tin thị trường lao động
 *     Việt Nam. Rủi ro pháp lý giảm khi pivot, không tăng.
 *
 * BẤT ĐỐI XỨNG PHẢI GIỮ THẲNG: tools/score_rules.py chỉ chấm cho VIỆT NAM.
 * Cột `verdict`, `n_vn` là về Việt Nam. Với bốn nước còn lại ta chỉ có DẤU CHÂN
 * (mệnh đề khoá nhắc tới nước đó), không có kết luận "tuyển được hay không".
 * Trang từng nước phải hiện đúng thứ đó — bịa verdict cho Thái Lan là làm hỏng
 * đúng thứ khiến kho này đáng tin.
 */
export type Country = {
  slug: string
  code: string
  name: string
  /** Có bộ chấm đầy đủ hay chỉ có dấu chân? Chỉ Việt Nam có. */
  scored: boolean
}

export const SEA: Country[] = [
  { slug: "vietnam", code: "VN", name: "Vietnam", scored: true },
  { slug: "philippines", code: "PH", name: "the Philippines", scored: false },
  { slug: "indonesia", code: "ID", name: "Indonesia", scored: false },
  { slug: "thailand", code: "TH", name: "Thailand", scored: false },
  { slug: "malaysia", code: "MY", name: "Malaysia", scored: false },
  { slug: "singapore", code: "SG", name: "Singapore", scored: false },
]

export const SEA_CODES = SEA.map((c) => c.code)

/** Mã dùng cho tín hiệu "đã tuyển ở láng giềng" — KHÔNG gồm VN (đang xét) và
 *  KHÔNG gồm SG (bậc chi phí khác hẳn, không cùng bài toán). */
export const NEIGHBOURS = ["PH", "ID", "TH", "MY"]

export const bySlug = (s: string) => SEA.find((c) => c.slug === s)
export const byCode = (c: string) => SEA.find((x) => x.code === c)
