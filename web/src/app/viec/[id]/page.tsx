import Link from "next/link"
import { Suspense } from "react"
import { notFound } from "next/navigation"
import { cacheLife } from "next/cache"
import type { Metadata } from "next"
import { all, one, type Job } from "@/lib/db"
import { MECH, SCOPE_LABEL, SCOPE_TONE } from "@/lib/labels"
import { Badge } from "@/components/Badge"
import { evidenceText } from "@/lib/evidence"
import { Loading } from "@/components/Skeleton"
import { ReportButton } from "@/components/ReportButton"

/** Chỉ tin MỞ mới có trang riêng: tin bị loại đã có kết luận ngay trên trang công ty,
 *  dựng thêm 19.000 trang chỉ để nói "không" là lãng phí và làm loãng chỉ mục. */
export async function generateStaticParams() {
  const rows = await all<{ id: string }>(
    "SELECT id FROM job WHERE scope IN ('worldwide','vn') ORDER BY id LIMIT 500",
  )
  return rows.map((r) => ({ id: r.id }))
}

async function load(id: string) {
  "use cache"
  cacheLife("days")
  const j = await one<Job & { company_name: string }>(
    `SELECT j.*, c.name AS company_name FROM job j
     JOIN company c ON c.slug = j.company_slug
     WHERE j.id = ? AND j.scope IN ('worldwide','vn')`,
    id,
  )
  return j
}

export async function generateMetadata({
  params,
}: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const j = await load((await params).id)
  return j ? { title: `${j.title} — ${j.company_name}` } : {}
}

export default function JobPage(props: { params: Promise<{ id: string }> }) {
  return (
    <Suspense
      fallback={
        <>
          <Loading label="Đang tải tin tuyển dụng" />
          <div aria-hidden className="animate-pulse space-y-4">
            <div className="h-[40px] w-3/4 bg-line-2" />
            <div className="h-[190px] bg-line-2/60" />
            <div className="h-[110px] bg-line-2/60" />
          </div>
        </>
      }
    >
      <Detail params={props.params} />
    </Suspense>
  )
}

async function Detail({ params }: { params: Promise<{ id: string }> }) {
  const j = await load((await params).id)
  if (!j) notFound()
  return (
    <>
      <div className="glow rise">
      <p className="font-mono text-[12px] text-text-3">
        <Link className="underline" href="/tin-mo">Tin mở</Link> ›{" "}
        <Link className="underline" href={`/cong-ty/${j.company_slug}`}>{j.company_name}</Link>
      </p>
      <h1 className="mt-4 max-w-[26ch] text-[clamp(26px,4vw,38px)]">{j.title}</h1>
      <p className="mt-3 text-[15px] text-text-2">{j.company_name}</p>

      </div>
      <div className="scroll-x mt-6 rounded-lg border border-line bg-card">
      <table className="w-full border-collapse">
        <tbody>
          <KV k="Trạng thái"><Badge tone={SCOPE_TONE[j.scope]}>{SCOPE_LABEL[j.scope]}</Badge></KV>
          <KV k="Cơ chế hợp đồng">{MECH[j.mechanism ?? "unknown"]}</KV>
          <KV k="Địa điểm ghi trên tin">{j.location_raw || "—"}</KV>
          <KV k="Trùng múi giờ với GMT+7">
            {j.tz_overlap == null ? "không nêu" : `${j.tz_overlap} giờ`}
          </KV>
          <KV k="Công bố lương">{j.pay ? "có" : "không"}</KV>
        </tbody>
      </table>
      </div>

      <section className="mt-9">
        <h2 className="text-[21px]">Bằng chứng</h2>
        <blockquote className="mt-3 rounded-md border border-open/35 border-l-[3px] border-l-open bg-open-bg px-4 py-3.5 font-mono text-[13px] leading-relaxed">
          {evidenceText(j)}
        </blockquote>
        <p className="mt-2 font-mono text-[12px] text-text-3">Trích từ: {j.evidence_src}</p>
      </section>

      {j.excerpt && (
        <section className="mt-9">
          <h2 className="text-[21px]">Trích đoạn mô tả</h2>
          <p className="mt-3 max-w-[70ch] text-[14.5px] leading-relaxed text-text-2">{j.excerpt}…</p>
        </section>
      )}

      <p className="mt-9">
        <a
          href={j.url}
          rel="nofollow noopener"
          className="inline-block rounded-sm border border-text px-5 py-3 text-[14px] font-medium transition-colors duration-150 hover:bg-text hover:text-bg"
        >
          Xem tin gốc và nộp tại đó →
        </a>
      </p>

      <ReportButton kind="job" refId={j.id} />
    </>
  )
}

function KV({ k, children }: { k: string; children: React.ReactNode }) {
  return (
    <tr className="border-b border-line-2">
      <th className="block py-2.5 pr-4 text-left align-top font-mono text-[11.5px] font-normal uppercase tracking-wide text-text-3 sm:table-cell sm:w-64">
        {k}
      </th>
      <td className="block pb-2.5 text-[14px] sm:table-cell sm:py-2.5">{children}</td>
    </tr>
  )
}
