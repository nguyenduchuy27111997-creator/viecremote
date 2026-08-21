import { cname } from "./countries"
import type { Job } from "./db"

/**
 * Chuỗi máy sinh -> câu người đọc được.
 *
 * Người dùng không bao giờ cần biết mã DQ hay tiền tố A-0x. Nhưng câu sinh ra
 * phải nói ĐÚNG thứ bằng chứng nói — không diễn giải rộng hơn dữ liệu.
 */
export function evidenceText(j: Job): string {
  const ev = (j.evidence ?? "").trim()
  if (!ev) return ""

  if (ev.startsWith("DQ-02(location)")) {
    const raw = ev.slice("DQ-02(location):".length).split("|")[0]
    const codes = (ev.split("|").pop() ?? "").split("/").filter(Boolean)
    const names = codes.map(cname).join(", ")
    return names
      ? `Tin ghi địa điểm: ${raw}. Chỉ tuyển ở ${names} — không có Việt Nam.`
      : `Tin ghi địa điểm: ${raw}.`
  }
  if (ev.startsWith("A-02(location)"))
    return `Tin ghi địa điểm: ${after(ev)} — không giới hạn quốc gia.`
  if (ev.startsWith("A-03(location)")) {
    const raw = after(ev)
    return /vi[eệ]t ?nam/i.test(raw)
      ? `Tin ghi địa điểm: ${raw} — nơi này ở Việt Nam.`
      : `Tin ghi địa điểm: ${raw} — vùng này bao gồm Việt Nam.`
  }
  if (ev.startsWith("A-01(schema)"))
    return `Công ty tự khai danh sách quốc gia nhận ứng viên, và có Việt Nam: ${after(ev)}`
  if (ev.startsWith("DQ-09(schema)"))
    return `Công ty tự khai danh sách quốc gia nhận ứng viên, và không có Việt Nam: ${after(ev)}`
  if (ev.startsWith("DQ-02(title)"))
    return `Nơi chốn nằm trong tiêu đề: ${after(ev)}`
  if (ev.startsWith("XUNG-DOT:")) {
    const [a, b = ""] = ev.slice("XUNG-DOT:".length).split("|")
    return `Hai nguồn mâu thuẫn — văn bản nói “${a}”, dữ liệu có cấu trúc nói “${b}”. Không đoán bên nào đúng.`
  }
  return `Trích từ tin: ${ev}`
}

const after = (ev: string) => ev.split(/:\s?/).slice(1).join(": ")
