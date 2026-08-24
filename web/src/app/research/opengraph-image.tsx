import { ImageResponse } from "next/og"
import { one } from "@/lib/db"

export const alt = "I scored tens of thousands of remote job posts. 0 of 150 hand-scored said they hire in Vietnam"
export const size = { width: 1200, height: 630 }
export const contentType = "image/png"

/**
 * Ảnh chia sẻ cho bài nghiên cứu tiếng Anh — thứ hiện ra khi link được dán
 * lên HN/Twitter/LinkedIn. Con số kéo từ kho như chính trang.
 *
 * "0 of 150 hand-scored" chứ KHÔNG phải "zero" trần: kho có 60 tin nhắc Việt
 * Nam trong dữ liệu cấu trúc, nên "zero said" trên toàn kho là SAI — chỉ đúng
 * trên mẫu chấm tay. Site bán độ chính xác; câu thiếu định danh mẫu là chỗ
 * HN xé đầu tiên, và họ xé đúng.
 */
export default async function Image() {
  const c = await one<{ jobs: number; open: number; total: number }>(
    `SELECT (SELECT count(*) FROM job) jobs,
            (SELECT count(*) FROM company WHERE verdict='ok') open,
            (SELECT count(*) FROM company) total`,
  )
  const num = (n: number) => n.toLocaleString("en-US")

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
            lineHeight: 1.12, maxWidth: 1050,
          }}
        >
          I scored {num(c?.jobs ?? 0)} remote job posts. 0 of 150 hand-scored said they hire in Vietnam.
        </div>

        <div style={{ display: "flex", gap: 56, fontSize: 22, color: "#adb1b9" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", fontSize: 44, fontWeight: 700, color: "#6fd5ab" }}>
              {num(c?.open ?? 0)} / {num(c?.total ?? 0)}
            </div>
            <div style={{ display: "flex" }}>companies can actually hire there</div>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", fontSize: 44, fontWeight: 700, color: "#eff4fc" }}>
              97.5%
            </div>
            <div style={{ display: "flex" }}>measured precision, method public</div>
          </div>
        </div>
      </div>
    ),
    size,
  )
}
