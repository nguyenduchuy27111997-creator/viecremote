import { ImageResponse } from "next/og"
import { one } from "@/lib/db"

export const alt = "Tôi chấm hàng chục nghìn tin remote. 0/150 tin chấm tay ghi rõ tuyển được ở Việt Nam"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

/** Bản Việt của ảnh /research — đích chia sẻ là nhóm dev Việt. */
export default async function Image() {
  const c = await one<{ jobs: number; open: number; total: number }>(
    `SELECT (SELECT count(*) FROM job) jobs,
            (SELECT count(*) FROM company WHERE verdict='ok') open,
            (SELECT count(*) FROM company) total`,
  )
  const num = (n: number) => n.toLocaleString("vi-VN")

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
            display: "flex", fontSize: 60, fontWeight: 700, letterSpacing: -2.5,
            lineHeight: 1.14, maxWidth: 1050,
          }}
        >
          Tôi chấm {num(c?.jobs ?? 0)} tin remote. 0/150 tin chấm tay ghi rõ tuyển được ở Việt Nam.
        </div>

        <div style={{ display: "flex", gap: 56, fontSize: 22, color: "#adb1b9" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", fontSize: 44, fontWeight: 700, color: "#6fd5ab" }}>
              {num(c?.open ?? 0)} / {num(c?.total ?? 0)}
            </div>
            <div style={{ display: "flex" }}>công ty thật sự tuyển được ở VN</div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", fontSize: 44, fontWeight: 700, color: "#eff4fc" }}>
              97,5%
            </div>
            <div style={{ display: "flex" }}>độ chính xác đo được, phương pháp công khai</div>
          </div>
        </div>
      </div>
    ),
    size,
  )
}
