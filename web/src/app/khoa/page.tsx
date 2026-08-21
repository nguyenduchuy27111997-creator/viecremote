import Link from "next/link"
import { cacheLife } from "next/cache"
import { all, meta } from "@/lib/db"
import { cname } from "@/lib/countries"
import { BarRow, Eyebrow, Lead, Note } from "@/components/Page"

export const metadata = {
  title: "Công ty khoá tuyển vào nước nào",
  description:
    "104 nước, xếp theo số công ty khoá tuyển vào đó. Dữ liệu suy từ mệnh đề giới hạn địa lý trong tin gốc.",
}

/**
 * Dữ liệu giàu nhất trong kho — 2.324/3.666 công ty có mệnh đề khoá địa lý —
 * mà trước đó không có đường nào vào. Vừa là nội dung SEO, vừa trả lời đúng
 * câu người ta thật sự hỏi: "công ty này khoá vào đâu?"
 */
export default async function LockedIndex() {
  "use cache"
  cacheLife("days")
  const m = await meta()
  const rows = await all<{ code: string; n_comp: number; n_jobs: number }>(
    `SELECT code, count(*) n_comp, sum(n_jobs) n_jobs
     FROM locked GROUP BY code ORDER BY n_comp DESC`,
  )
  const top = rows[0]?.n_comp ?? 1

  return (
    <>
      <div className="glow rise">
        <Eyebrow>{rows.length} nước · {(+m.n_companies).toLocaleString("vi-VN")} công ty</Eyebrow>
        <h1 className="mt-4 max-w-[17ch] text-[clamp(30px,5vw,48px)]">
          Công ty <span className="grad">khoá tuyển</span> vào nước nào
        </h1>
        <Lead>
          Khi một tin ghi <i>&ldquo;Remote (US only)&rdquo;</i> hay <i>&ldquo;EMEA&rdquo;</i>,
          đó là một mệnh đề khoá. Bảng dưới đếm theo <b className="text-text">số công ty</b> có
          ít nhất một tin khoá vào nước đó.
        </Lead>
      </div>

      <div className="scroll-x mt-9 rounded-lg border border-line bg-card">
        <table className="w-full border-collapse">
          <caption className="sr-only">Số công ty khoá tuyển, theo nước</caption>
          <tbody>
            {rows.map((r) => (
              <BarRow
                key={r.code}
                label={<Link className="hover:underline" href={`/khoa/${r.code.toLowerCase()}`}>{cname(r.code)}</Link>}
                n={r.n_comp}
                pct={(100 * r.n_comp) / top}
              />
            ))}
          </tbody>
        </table>
      </div>

      <Note>
        Một công ty có thể khoá vào nhiều nước, nên tổng lớn hơn số công ty. Chỉ đếm mệnh đề
        <b className="text-text-2"> trích dẫn được</b> — công ty khoá ngầm mà không viết ra sẽ
        không xuất hiện ở đây.
      </Note>
    </>
  )
}
