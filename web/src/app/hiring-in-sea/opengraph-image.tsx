import { ImageResponse } from "next/og"
import { all, one } from "@/lib/db"
import { SEA_CODES } from "@/lib/sea"

export const alt = "Most companies reach Southeast Asia and stop at one country"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

/**
 * Ảnh chia sẻ cho trang khu vực. Con số lấy từ kho, không viết cứng — ảnh này
 * là thứ người ta thấy trước cả trang, nên nó sai là hỏng trước khi vào.
 */
export default async function Image() {
  const codes = SEA_CODES.map((c) => `'${c}'`).join(",")
  const reach = await one<{ n: number }>(
    `SELECT count(DISTINCT slug) n FROM locked WHERE code IN (${codes})`)
  const trap = await all<{ n: number }>(
    `SELECT count(*) n FROM (
       SELECT slug FROM locked WHERE code IN (${codes})
       GROUP BY slug HAVING count(DISTINCT code) = 1)`)
  const trapped = trap[0]?.n ?? 0

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
            display: "flex", fontSize: 66, fontWeight: 700, letterSpacing: -2.5,
            lineHeight: 1.1, maxWidth: 1040,
          }}
        >
          Most companies reach Southeast Asia and stop at one country
        </div>

        <div style={{ display: "flex", gap: 56, fontSize: 22, color: "#adb1b9" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: "#eff4fc" }}>
              {reach?.n ?? 0}
            </div>
            <div style={{ display: "flex" }}>companies hire in the region</div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: "#6fd5ab" }}>
              {trapped}
            </div>
            <div style={{ display: "flex" }}>name exactly one country in it</div>
          </div>
        </div>
      </div>
    ),
    size,
  )
}
