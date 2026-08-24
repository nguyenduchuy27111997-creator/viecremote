import { ImageResponse } from "next/og"
import { all, one } from "@/lib/db"
import { SEA, SEA_CODES, bySlug } from "@/lib/sea"

export const alt = "Hiring remotely in this market — what postings actually allow"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

export async function generateStaticParams() {
  return SEA.map((c) => ({ country: c.slug }))
}

/**
 * Ảnh chia sẻ cho trang thị trường. Giữ đúng bất đối xứng của trang: Việt Nam
 * hiện con số CHẤM ĐƯỢC (91 công ty tuyển được), năm nước kia hiện dấu chân —
 * ảnh mà hứa hơn trang là mồi câu sai, người bấm vào sẽ thấy ngay.
 */
export default async function Image({ params }: { params: Promise<{ country: string }> }) {
  const c = bySlug((await params).country)
  if (!c) {
    return new ImageResponse(
      <div style={{ background: "#0a0c11", width: "100%", height: "100%" }} />, size)
  }

  const foot = await one<{ n: number }>(
    "SELECT count(DISTINCT slug) n FROM locked WHERE code = ?", c.code)
  const codes = SEA_CODES.map((x) => `'${x}'`).join(",")
  const alone = await all<{ n: number }>(
    `SELECT count(*) n FROM (
       SELECT slug FROM locked WHERE code IN (${codes})
       GROUP BY slug HAVING count(DISTINCT code) = 1 AND max(code) = '${c.code}')`)
  const open = c.scored
    ? await one<{ n: number }>("SELECT count(*) n FROM company WHERE verdict='ok'")
    : null

  const stats: [string, string, string][] = open
    ? [[String(open.n), "companies can hire here", "#6fd5ab"],
       [String(foot?.n ?? 0), "restrict postings to it", "#adb1b9"]]
    : [[String(foot?.n ?? 0), "companies restrict postings to it", "#eff4fc"],
       [String(alone[0]?.n ?? 0), "hire nowhere else in SEA", "#6fd5ab"]]

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

        <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
          <div style={{ display: "flex", fontSize: 28, color: "#adb1b9" }}>
            Hiring remotely in
          </div>
          <div
            style={{
              display: "flex", fontSize: 82, fontWeight: 700, letterSpacing: -3,
              lineHeight: 1.02, maxWidth: 1040, textTransform: "capitalize",
            }}
          >
            {c.name.replace(/^the /, "")}
          </div>
          {!c.scored && (
            <div style={{ display: "flex", fontSize: 22, color: "#e4b563" }}>
              reported by hiring footprint — not scored the way Vietnam is
            </div>
          )}
        </div>

        <div style={{ display: "flex", gap: 56, fontSize: 22, color: "#adb1b9" }}>
          {stats.map(([n, label, tone]) => (
            <div key={label} style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <div style={{ display: "flex", fontSize: 46, fontWeight: 700, color: tone }}>{n}</div>
              <div style={{ display: "flex" }}>{label}</div>
            </div>
          ))}
        </div>
      </div>
    ),
    size,
  )
}
