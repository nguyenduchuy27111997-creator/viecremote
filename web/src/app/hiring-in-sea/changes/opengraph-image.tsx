import { ImageResponse } from "next/og"
import { one } from "@/lib/db"

export const alt = "Companies that opened or closed to Vietnam — daily change log"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

/**
 * Ảnh chia sẻ cho nhật ký đổi nhãn. Số sống: khi kho còn rỗng, ảnh nói thật
 * "tracking since 24 Aug 2026, 0 flips yet" — cùng nguyên tắc trạng-thái-rỗng-
 * trung-thực của chính trang. Ảnh hứa hơn trang là mồi câu sai.
 */
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
            display: "flex", fontSize: 64, fontWeight: 700, letterSpacing: -2.5,
            lineHeight: 1.12, maxWidth: 1040,
          }}
        >
          Companies that opened or closed to Vietnam
        </div>

        <div style={{ display: "flex", gap: 56, fontSize: 22, color: "#adb1b9" }}>
          {total === 0 ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <div style={{ display: "flex", fontSize: 40, fontWeight: 700, color: "#eff4fc" }}>
                Tracking since 24 Aug 2026
              </div>
              <div style={{ display: "flex" }}>
                the corpus rebuilds daily — this page is the only thing that remembers yesterday
              </div>
            </div>
          ) : (
            <>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: "#6fd5ab" }}>
                  {c?.opened ?? 0}
                </div>
                <div style={{ display: "flex" }}>opened to Vietnam</div>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: "#ff9f9f" }}>
                  {c?.closed ?? 0}
                </div>
                <div style={{ display: "flex" }}>closed</div>
              </div>
            </>
          )}
        </div>
      </div>
    ),
    size,
  )
}
