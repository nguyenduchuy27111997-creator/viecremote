import { ImageResponse } from "next/og"
import { one } from "@/lib/db"

export const alt = "Công ty vừa mở hay vừa đóng với Việt Nam — nhật ký đổi nhãn"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

/** Bản Việt của ảnh /hiring-in-sea/changes — đích chia sẻ là nhóm dev Việt. */
export default async function Image() {
  const c = await one<{ n: number; opened: number; closed: number }>(
    `SELECT count(*) n,
            sum(to_v = 'ok') opened,
            sum(from_v = 'ok') closed
     FROM verdict_change`,
  )
  const total = c?.n ?? 0

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%", height: "100%", display: "flex", flexDirection: "column",
          justifyContent: "space-between", background: "#0a0c11", color: "#eff4fc",
          padding: 72, fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14, fontSize: 24, color: "#adb1b9" }}>
          <div
            style={{
              width: 18, height: 18, borderRadius: 5, transform: "rotate(45deg)",
              background: "linear-gradient(135deg,#6fd5ab,#8ab4ff)",
            }}
          />
          viecremote
        </div>

        <div
          style={{
            display: "flex", fontSize: 62, fontWeight: 700, letterSpacing: -2.5,
            lineHeight: 1.14, maxWidth: 1040,
          }}
        >
          Công ty vừa mở hay vừa đóng với Việt Nam
        </div>

        <div style={{ display: "flex", gap: 56, fontSize: 22, color: "#adb1b9" }}>
          {total === 0 ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <div style={{ display: "flex", fontSize: 40, fontWeight: 700, color: "#eff4fc" }}>
                Theo dõi từ 24/08/2026
              </div>
              <div style={{ display: "flex" }}>
                kho dựng lại mỗi ngày — trang này là thứ duy nhất nhớ hôm qua
              </div>
            </div>
          ) : (
            <>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: "#6fd5ab" }}>
                  {c?.opened ?? 0}
                </div>
                <div style={{ display: "flex" }}>vừa mở cho Việt Nam</div>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: "#ff9f9f" }}>
                  {c?.closed ?? 0}
                </div>
                <div style={{ display: "flex" }}>vừa đóng</div>
              </div>
            </>
          )}
        </div>
      </div>
    ),
    size,
  )
}
