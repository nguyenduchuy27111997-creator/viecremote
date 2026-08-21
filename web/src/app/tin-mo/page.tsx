import Link from "next/link"
import { cacheLife } from "next/cache"
import { all, meta, type Job } from "@/lib/db"
import { SCOPE_LABEL, SCOPE_TONE } from "@/lib/labels"
import { Badge } from "@/components/Badge"
import { DensityBar, StatRow } from "@/components/Stat"
import { Eyebrow, Lead, Note } from "@/components/Page"
import { evidenceText } from "@/lib/evidence"

export const metadata = { title: "Tin đang mở cho người ở Việt Nam" }

const SHORT: Record<string, string> = {
  "Mở toàn cầu": "Toàn cầu",
  "Mở cho Việt Nam": "Mở cho VN",
}

/** Trục phụ. Trục chính là công ty — xem business-model.md Mục 1. */
export default async function OpenJobs() {
  "use cache"
  cacheLife("days")
  const m = await meta()
  const jobs = await all<Job & { company_name: string }>(
    `SELECT j.*, c.name AS company_name FROM job j
     JOIN company c ON c.slug = j.company_slug
     WHERE j.scope IN ('worldwide','vn')
     ORDER BY CASE j.scope WHEN 'worldwide' THEN 0 ELSE 1 END, c.name, j.title`,
  )
  const items = [
    { tone: "open" as const, n: +m.n_job_global, label: "mở toàn cầu", href: "/tin-mo" },
    { tone: "unk" as const, n: +m.n_job_vn, label: "mở cho vùng hoặc nước có VN", href: "/tin-mo" },
    { tone: "closed" as const, n: +m.n_job_excluded, label: "bị giới hạn địa lý", href: "/vi-sao-bi-loai" },
  ]

  return (
    <>
      <div className="glow rise">
      <Eyebrow>Trục tin · {jobs.length.toLocaleString("vi-VN")} vị trí</Eyebrow>
      <h1 className="mt-4 max-w-[19ch] text-[clamp(30px,5vw,48px)]">
        Tin nào <span className="grad">thực sự mở</span> cho người ở Việt Nam
      </h1>
      <Lead>
        Trong <b className="tabular-nums text-text">{(+m.n_jobs).toLocaleString("vi-VN")}</b> tin
        remote đã chấm, chỉ <b className="tabular-nums text-text">{jobs.length}</b> tin không vướng
        giới hạn địa lý nào chặn người ở Việt Nam.
      </Lead>

      <div className="mt-9">
        <DensityBar items={items} />
        <StatRow items={items} unit="tin" />
      </div>
      </div>

      <Note>
        Muốn xem theo công ty — trục ổn định hơn, vì tin đổi hằng ngày còn công ty đổi hằng quý —
        thì về{" "}
        <Link className="underline underline-offset-2 hover:text-text" href="/">
          sổ đăng ký công ty
        </Link>
        .
      </Note>

      <ul className="mt-8 divide-y divide-line-2/60">
        {jobs.map((j, i) => (
          <li
            key={j.id}
            className="rise -mx-3 grid grid-cols-1 items-start gap-y-2.5 rounded-md px-3 py-4 transition-colors duration-150 hover:bg-card sm:grid-cols-[max-content_1fr] sm:gap-x-5 sm:gap-y-0"
            style={{ animationDelay: `${Math.min(i, 12) * 22}ms` }}
          >
            <Badge tone={SCOPE_TONE[j.scope]}>
              {SHORT[SCOPE_LABEL[j.scope]] ?? SCOPE_LABEL[j.scope]}
            </Badge>
            <div className="min-w-0">
              <Link href={`/viec/${j.id}`} className="text-[16px] font-medium hover:underline">
                {j.title}
              </Link>
              <div className="mt-1 font-mono text-[11.5px] text-text-3">
                <Link
                  href={`/cong-ty/${j.company_slug}`}
                  className="underline underline-offset-2 hover:text-text"
                >
                  {j.company_name}
                </Link>{" "}
                · {j.location_raw}
              </div>
              <p className="mt-2 rounded-xs border-l-2 border-line bg-card py-2 pl-3 pr-2.5 font-mono text-[12px] leading-relaxed text-text-2">
                {evidenceText(j)}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </>
  )
}
