import Link from "next/link"
import { cacheLife } from "next/cache"
import { all, meta } from "@/lib/db"
import { REASON } from "@/lib/labels"
import { cname } from "@/lib/countries"
import { BarRow, Eyebrow, Lead, Note, PageTitle, Section } from "@/components/Page"

export const metadata = { title: "Vì sao tin bị loại" }

/** Lõi sản phẩm: 86% kho là câu "không", và mỗi câu "không" đều trích dẫn được. */
export default async function Why() {
  "use cache"
  cacheLife("days")
  const m = await meta()

  const reasons = await all<{ reason: string; n: number }>(
    `SELECT reason, count(*) n FROM job
     WHERE scope = 'excluded' AND reason IS NOT NULL
     GROUP BY reason ORDER BY n DESC`,
  )
  const rows = await all<{ evidence: string }>(
    "SELECT evidence FROM job WHERE scope='excluded' AND evidence LIKE 'DQ-02(location)%'",
  )
  const cs = new Map<string, number>()
  for (const r of rows)
    for (const c of (r.evidence.split("|").pop() ?? "").split("/"))
      if (c.length === 2) cs.set(c, (cs.get(c) ?? 0) + 1)
  const top = [...cs].sort((a, b) => b[1] - a[1]).slice(0, 14)

  const rMax = reasons[0]?.n || 1
  const cMax = top[0]?.[1] || 1
  const tot = +m.n_job_excluded

  return (
    <>
      <div className="glow rise">
      <Eyebrow>Bộ kiểm tra loại trừ</Eyebrow>
      <h1 className="mt-4 max-w-[16ch] text-[clamp(30px,5vw,48px)]">
        Vì sao tin <span className="grad">bị loại</span>
      </h1>
      <Lead>
        <b className="tabular-nums text-text">{tot.toLocaleString("vi-VN")}</b> tin bị giới hạn địa
        lý — <b className="tabular-nums text-text">{((100 * tot) / +m.n_jobs).toFixed(1)}%</b> toàn
        kho. Câu trả lời “không” có giá trị ngang câu “có”: nó tiết kiệm 40 phút viết đơn. Mỗi lý
        do dưới đây dựa trên một câu trích được từ tin gốc.
      </Lead>
      </div>

      <Section
        title="Theo loại rào cản"
        hint="Mỗi tin tính đúng một lý do — lý do mạnh nhất khi có nhiều mệnh đề cùng loại trừ."
      >
        <div className="scroll-x mt-4 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse">
            <caption className="sr-only">Số tin bị loại theo loại rào cản</caption>
            <tbody>
              {reasons.map((r) => (
                <BarRow
                  key={r.reason}
                  label={REASON[r.reason] ?? r.reason}
                  n={r.n}
                  pct={(100 * r.n) / rMax}
                />
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section
        title="Nước khoá tuyển nhiều nhất"
        hint="Đếm theo số tin nêu đích danh nước đó. Một tin có thể nêu nhiều nước, nên tổng ở đây lớn hơn số tin."
      >
        <div className="scroll-x mt-4 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse">
            <caption className="sr-only">Số tin khoá tuyển theo nước</caption>
            <tbody>
              {top.map(([c, n]) => (
                <BarRow key={c} label={cname(c)} n={n} pct={(100 * n) / cMax} />
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Note>
        Đây là <b className="text-text-2">thứ dồi dào nhất trong kho</b> — và cũng là thứ chưa ai
        công bố. Cách chấm và độ chính xác đo được:{" "}
        <Link className="underline underline-offset-2 hover:text-text" href="/phuong-phap">
          phương pháp
        </Link>
        .
      </Note>
    </>
  )
}
