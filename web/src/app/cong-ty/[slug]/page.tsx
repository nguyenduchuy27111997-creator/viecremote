import Link from "next/link"
import { Suspense } from "react"
import { notFound } from "next/navigation"
import type { Metadata } from "next"
import { all, one, parseDeclared, parseLocked, parseReasons, type Company, type Job } from "@/lib/db"
import { MECH, REASON, SCOPE_LABEL, SCOPE_TONE } from "@/lib/labels"
import { cname } from "@/lib/countries"
import { Badge } from "@/components/Badge"
import { BarRow, Chip, Crumb, KV, KVTable, Section, ToneChip } from "@/components/Page"
import { Loading, RowSkeleton } from "@/components/Skeleton"
import { ReportButton } from "@/components/ReportButton"
import { evidenceText } from "@/lib/evidence"

// Kho dựng lại mỗi ngày; ISR thường thay cho "use cache".
export const revalidate = 86400

const SHORT: Record<string, string> = {
  "Mở toàn cầu": "Toàn cầu",
  "Mở cho Việt Nam": "Mở cho VN",
  "Không mở cho VN": "Khoá",
  "Chưa xác định": "Chưa rõ",
}

/**
 * Chỉ dựng sẵn công ty CÓ tin mở — nhóm đáng đọc nhất và chỉ vài trăm trang.
 * Số còn lại dựng theo yêu cầu lần đầu rồi nằm trong cache, nên build không
 * phình theo kích thước kho.
 */
export async function generateStaticParams() {
  const rows = await all<{ slug: string }>(
    "SELECT slug FROM company WHERE verdict = 'ok' ORDER BY n_global DESC LIMIT 200",
  )
  return rows.map((r) => ({ slug: r.slug }))
}

async function load(slug: string) {
  const c = await one<Company>("SELECT * FROM company WHERE slug = ?", slug)
  if (!c) return null
  const jobs = await all<Job>(
    `SELECT * FROM job WHERE company_slug = ?
     ORDER BY CASE scope WHEN 'worldwide' THEN 0 WHEN 'vn' THEN 1 WHEN 'unknown' THEN 2 ELSE 3 END,
     title LIMIT 300`,
    slug,
  )
  return { c, jobs }
}

export async function generateMetadata({
  params,
}: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const d = await load((await params).slug)
  if (!d) return {}
  return {
    title: `${d.c.name} — địa lý tuyển dụng`,
    description: `${d.c.name}: ${d.c.verdict_label.toLowerCase()}. ${d.c.n_jobs} tin remote, kèm trích dẫn.`,
  }
}

// `await params` phải nằm TRONG ranh giới Suspense, kể cả với slug đã dựng sẵn:
// await ở ngoài sẽ trói App Shell vào một URL, và slug lạ mất trang tức thời.
export default function CompanyPage(props: { params: Promise<{ slug: string }> }) {
  return (
    <Suspense
      fallback={
        <>
          <Loading label="Đang tải hồ sơ công ty" />
          <div aria-hidden className="h-[46px] w-1/2 animate-pulse bg-line-2" />
          <RowSkeleton n={6} />
        </>
      }
    >
      <Profile params={props.params} />
    </Suspense>
  )
}

async function Profile({ params }: { params: Promise<{ slug: string }> }) {
  const d = await load((await params).slug)
  if (!d) notFound()
  const { c, jobs } = d
  const locked = parseLocked(c.locked)
  const declared = parseDeclared(c.declared)
  const reasons = parseReasons(c.reasons)
  const open = jobs.filter((j) => j.scope === "worldwide" || j.scope === "vn")
  const rest = jobs.filter((j) => j.scope !== "worldwide" && j.scope !== "vn")
  const lockMax = locked[0]?.[1] || 1
  const rMax = reasons[0]?.[1] || 1

  return (
    <>
      <div className="glow rise">
      <Crumb to="/" label="Công ty" current={c.name} />
      <h1 className="mt-4 text-[clamp(30px,4.6vw,42px)]">{c.name}</h1>

      {/* Kết luận đặt ngay dưới tên: đó là thứ duy nhất người đọc tới đây để biết. */}
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Badge tone={c.verdict}>{c.verdict_label}</Badge>
        {c.n_global > 0 && <ToneChip tone="open">{c.n_global} vị trí toàn cầu</ToneChip>}
        {c.n_vn > 0 && <ToneChip tone="open">{c.n_vn} vị trí mở cho VN</ToneChip>}
      </div>

      {/* Cùng công ty này có bản tiếng Anh cho phía cầu. Kỹ sư là người mang
          link đi: gửi bản tiếng Việt cho hiring manager nước ngoài là vô ích,
          nên đường sang bản tiếng Anh phải nằm ngay đây, không phải trong nav. */}
      <p className="mt-3 font-mono text-[11.5px] text-text-3">
        <Link className="underline underline-offset-2 hover:text-text-2" href={`/company/${c.slug}`} lang="en">
          English version for employers →
        </Link>
      </p>
      </div>

      <KVTable>
        <KV k="Tin remote đang mở">
          <span className="tabular-nums">{c.n_jobs.toLocaleString("vi-VN")}</span>
        </KV>
        <KV k="Cơ chế hợp đồng">{MECH[c.mechanism] ?? c.mechanism}</KV>
        <KV k="Nguồn">{c.source}</KV>
        {declared.length > 0 && (
          <KV k="Công ty tự khai nhận ứng viên tại">
            <span className="flex flex-wrap gap-1.5">
              {declared.slice(0, 14).map((x) => (
                <Chip key={x}>{cname(x)}</Chip>
              ))}
            </span>
          </KV>
        )}
        {c.n_pay > 0 && (
          <KV k="Tin có công bố lương">
            <span className="tabular-nums">{`${c.n_pay}/${c.n_jobs}`}</span>
          </KV>
        )}
      </KVTable>

      <p className="mt-3 max-w-[64ch] text-[12.5px] leading-relaxed text-text-3">
        Cơ chế hợp đồng và địa lý tuyển là thuộc tính của công ty, không phải của từng tin —
        biết một lần dùng cho mọi tin.
      </p>

      {locked.length > 0 && (
        <Section
          title="Công ty này khoá tuyển vào đâu"
          hint="Đếm theo số tin có mệnh đề giới hạn địa lý. Một tin có thể nêu nhiều nước."
        >
          <div className="scroll-x mt-3 rounded-lg border border-line">
            <table className="w-full border-collapse">
              <caption className="sr-only">Số tin có mệnh đề giới hạn địa lý, theo nước</caption>
              <tbody>
                {locked.slice(0, 12).map(([code, n]) => (
                  <BarRow key={code} label={cname(code)} n={n} pct={(100 * n) / lockMax} />
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {reasons.length > 0 && (
        <Section title="Vì sao các tin còn lại bị loại">
          <div className="scroll-x mt-3 rounded-lg border border-line">
            <table className="w-full border-collapse">
              <caption className="sr-only">Số tin bị loại theo lý do</caption>
              <tbody>
                {reasons.map(([code, n]) => (
                  <BarRow key={code} label={REASON[code] ?? code} n={n} pct={(100 * n) / rMax} />
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {open.length > 0 && <JobList title="Vị trí mở cho người ở Việt Nam" jobs={open} />}
      {rest.length > 0 && <JobList title="Vị trí khác" jobs={rest} />}

      <ReportButton kind="company" refId={c.slug} />
    </>
  )
}

function JobList({ title, jobs }: { title: string; jobs: Job[] }) {
  return (
    <Section title={title}>
      <p className="mt-1 font-mono text-[11.5px] tabular-nums text-text-3">{jobs.length} vị trí</p>
      <ul className="mt-3 divide-y divide-line-2/60">
        {jobs.map((j) => {
          const openJob = j.scope === "worldwide" || j.scope === "vn"
          return (
            <li
              key={j.id}
              className="-mx-3 grid grid-cols-1 items-start gap-y-2.5 rounded-md px-3 py-4 transition-colors duration-150 hover:bg-card sm:grid-cols-[max-content_1fr] sm:gap-x-5 sm:gap-y-0"
            >
              <Badge tone={SCOPE_TONE[j.scope]}>
                {SHORT[SCOPE_LABEL[j.scope]] ?? SCOPE_LABEL[j.scope]}
              </Badge>
              <div className="min-w-0">
                {openJob ? (
                  <Link href={`/viec/${j.id}`} className="text-[15.5px] font-medium hover:underline">
                    {j.title}
                  </Link>
                ) : (
                  <a
                    href={j.url}
                    rel="nofollow noopener"
                    className="text-[15.5px] font-medium text-text-2 hover:underline"
                  >
                    {j.title} <span aria-hidden>↗</span>
                    <span className="sr-only">(mở tin gốc ở trang khác)</span>
                  </a>
                )}
                <div className="mt-1 font-mono text-[11.5px] text-text-3">{j.location_raw}</div>
                <p className="mt-2 rounded-xs border-l-2 border-line bg-card py-2 pl-3 pr-2.5 font-mono text-[12px] leading-relaxed text-text-2">
                  {evidenceText(j)}
                </p>
              </div>
            </li>
          )
        })}
      </ul>
    </Section>
  )
}
