import { ImageResponse } from "next/og"
import { one, parseLocked, type Company } from "@/lib/db"
import { ename } from "@/lib/countries"

export const alt = "Where this company's remote postings allow hiring"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

import { NEIGHBOURS } from "@/lib/sea"

const SEA = new Set(NEIGHBOURS)

const TONE = {
  ok: { fg: "#6fd5ab", bg: "#002b1c", label: "Can hire in Vietnam" },
  unk: { fg: "#e4b563", bg: "#301f00", label: "No clause either way" },
  no: { fg: "#ff9f9f", bg: "#391718", label: "Cannot hire in Vietnam" },
} as const

/**
 * Ảnh chia sẻ cho trang gương soi — bản tiếng Anh của ảnh ở /cong-ty/[slug].
 *
 * Hai khác biệt có chủ ý, không phải chép rồi dịch:
 *   - nhãn tiếng Anh, vì người dán link này là công ty nước ngoài
 *   - nếu công ty ĐÃ tuyển ở Đông Nam Á thì dòng cuối nói ĐIỀU ĐÓ, không nói
 *     danh sách nước. "You already hire in Malaysia" là câu khiến người ta bấm;
 *     "khoá vào US, DE, GB" thì không.
 */
export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const c = await one<Company>("SELECT * FROM company WHERE slug = ?", slug)
  if (!c) {
    return new ImageResponse(
      <div style={{ background: "#0a0c11", width: "100%", height: "100%" }} />, size)
  }

  const t = TONE[c.verdict as keyof typeof TONE] ?? TONE.unk
  const locked = parseLocked(c.locked)
  const sea = locked.filter(([k]) => SEA.has(k)).map(([k]) => ename(k))
  const name = c.name.replace(/[-_]+/g, " ").replace(/\b\w/g, (m) => m.toUpperCase())

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

        <div style={{ display: "flex", flexDirection: "column" }}>
          <div
            style={{
              display: "flex", fontSize: 74, fontWeight: 700, letterSpacing: -3,
              lineHeight: 1.05, maxWidth: 1040,
            }}
          >
            {name}
          </div>
          <div
            style={{
              display: "flex", alignSelf: "flex-start", marginTop: 30, fontSize: 34, fontWeight: 600,
              color: t.fg, background: t.bg, border: `2px solid ${t.fg}55`,
              borderRadius: 12, padding: "12px 22px",
            }}
          >
            {t.label}
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 12, fontSize: 23, color: "#adb1b9" }}>
          <div style={{ display: "flex" }}>
            {c.n_jobs.toLocaleString("en-US") + " live postings"
              + (c.n_global > 0 ? ` · ${c.n_global} open worldwide` : "")
              + (c.n_excluded > 0 ? ` · ${c.n_excluded} exclude Vietnam` : "")}
          </div>
          {sea.length > 0 && (
            <div style={{ display: "flex", color: "#6fd5ab" }}>
              {`You already hire in ${sea.join(", ")} — Vietnam is the same problem`}
            </div>
          )}
        </div>
      </div>
    ),
    size,
  )
}
