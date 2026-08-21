import { ImageResponse } from "next/og"
import { one, parseLocked, type Company } from "@/lib/db"
import { cname } from "@/lib/countries"

export const alt = "Hồ sơ địa lý tuyển dụng"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

const TONE = {
  ok: { fg: "#6fd5ab", bg: "#002b1c" },
  unk: { fg: "#e4b563", bg: "#301f00" },
  no: { fg: "#ff9f9f", bg: "#391718" },
} as const

/** Chia sẻ một công ty thì thứ đáng hiện là KẾT LUẬN, không phải tên trang. */
export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const c = await one<Company>("SELECT * FROM company WHERE slug = ?", slug)
  if (!c) return new ImageResponse(<div style={{ background: "#0a0c11", width: "100%", height: "100%" }} />, size)

  const t = TONE[c.verdict as keyof typeof TONE] ?? TONE.unk
  const locked = parseLocked(c.locked).slice(0, 5)

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
              display: "flex", fontSize: 78, fontWeight: 700, letterSpacing: -3,
              lineHeight: 1.05, maxWidth: 1040,
            }}
          >
            {c.name}
          </div>
          <div
            style={{
              display: "flex", alignSelf: "flex-start", marginTop: 30, fontSize: 34, fontWeight: 600,
              color: t.fg, background: t.bg, border: `2px solid ${t.fg}55`,
              borderRadius: 12, padding: "12px 22px",
            }}
          >
            {c.verdict_label}
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 12, fontSize: 22, color: "#adb1b9" }}>
          <div style={{ display: "flex" }}>
            {c.n_jobs.toLocaleString("vi-VN") + " tin remote"
              + (c.n_global > 0 ? ` · ${c.n_global} vị trí mở toàn cầu` : "")
              + (c.n_vn > 0 ? ` · ${c.n_vn} mở cho VN` : "")}
          </div>
          {locked.length > 0 && (
            <div style={{ display: "flex", color: "#ff9f9f" }}>
              {"khoá vào " + locked.map(([k]) => cname(k)).join(", ")}
            </div>
          )}
        </div>
      </div>
    ),
    size,
  )
}
