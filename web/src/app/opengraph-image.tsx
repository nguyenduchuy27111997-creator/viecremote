import { ImageResponse } from "next/og"
import { meta } from "@/lib/db"

export const alt = "Công ty nào thật sự tuyển được người ở Việt Nam"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

/**
 * Thẻ chia sẻ là CON SỐ, không phải logo.
 *
 * Bài công bố sống bằng lượt chia sẻ trên Facebook, LinkedIn, HN. Không có ảnh
 * OG thì mọi lượt chia sẻ hiện thẻ trắng — trông như link hỏng, tỉ lệ bấm rơi
 * thẳng. Và thứ khiến người ta bấm là 110/3.666, không phải tên trang.
 */
export default async function Image() {
  const m = await meta()
  const ok = +m.n_comp_ok
  const tot = +m.n_companies

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%", height: "100%", display: "flex", flexDirection: "column",
          justifyContent: "space-between", background: "#0a0c11", color: "#eff4fc",
          padding: 72, fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 20, height: 20, borderRadius: 5, transform: "rotate(45deg)",
              background: "linear-gradient(135deg,#6fd5ab,#8ab4ff)",
            }}
          />
          <div style={{ display: "flex", fontSize: 26, fontWeight: 600, letterSpacing: -0.5 }}>
            viecremote
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <div
            style={{
              display: "flex", fontSize: 130, fontWeight: 700, letterSpacing: -6,
              lineHeight: 1, color: "#6fd5ab",
            }}
          >
            <span>{ok}</span>
            <span style={{ color: "#4a4f58" }}>/{tot.toLocaleString("vi-VN")}</span>
          </div>
          <div
            style={{
              display: "flex", fontSize: 42, fontWeight: 600, letterSpacing: -1.4,
              marginTop: 22, maxWidth: 980,
            }}
          >
            công ty remote thật sự tuyển được người ở Việt Nam
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 22, color: "#adb1b9" }}>
          <div style={{ display: "flex" }}>
            {(+m.n_jobs).toLocaleString("vi-VN")} tin đã chấm · mỗi kết luận kèm trích dẫn
          </div>
          <div style={{ display: "flex", color: "#ff9f9f" }}>86,3% khoá theo địa lý</div>
        </div>
      </div>
    ),
    size,
  )
}
