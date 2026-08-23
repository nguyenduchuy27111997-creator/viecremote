import Link from "next/link"
import { Suspense } from "react"
import { all, meta, one, parseLocked, type Company } from "@/lib/db"
import { MECH } from "@/lib/labels"
import { cname } from "@/lib/countries"
import { Badge } from "@/components/Badge"
import { Chip, Eyebrow, ToneChip } from "@/components/Page"
import { DensityBar, StatRow } from "@/components/Stat"
import { SearchBox } from "@/components/SearchBox"
import { BlockSkeleton, Loading, RowSkeleton } from "@/components/Skeleton"
import { EmptyState } from "@/components/EmptyState"

// Kho dựng lại mỗi ngày; ISR thường thay cho "use cache".
export const revalidate = 86400

const PAGE = 60

/** Nhãn ngắn cho hàng danh sách. Bản đầy đủ giữ trên trang hồ sơ, nơi có chỗ. */
const SHORT: Record<string, string> = {
  "Tuyển toàn cầu": "Toàn cầu",
  "Tuyển được ở Việt Nam": "Mở cho VN",
  "Chưa xác định": "Chưa rõ",
  "Phần lớn khoá, còn tin chưa rõ": "Phần lớn khoá",
  "Không tuyển ở Việt Nam": "Khoá",
}

/**
 * Vỏ trang là tĩnh, danh sách là lỗ động được stream vào (PPR).
 * Người dùng thấy tiêu đề và số liệu ngay ở tốc độ CDN; kết quả tra cứu đến
 * sau — thay vì chờ cả trang chỉ vì một tham số truy vấn.
 */
export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; mech?: string; p?: string; v?: string }>
}) {
  return (
    <>
      <Suspense fallback={<BlockSkeleton h={360} />}>
        <Header />
      </Suspense>
      {/* useSearchParams đọc dữ liệu chỉ có lúc chạy — phải nằm sau ranh giới
          Suspense, nếu không cả vỏ trang mất khả năng dựng sẵn. */}
      <Suspense fallback={<div className="mt-9 h-[104px] rounded-lg border border-line bg-card" />}>
        <SearchBox />
      </Suspense>
      <Suspense
        fallback={
          <>
            <Loading label="Đang tra cứu công ty" />
            <RowSkeleton />
          </>
        }
      >
        <Registry searchParams={searchParams} />
      </Suspense>
    </>
  )
}

async function Header() {
  const m = await meta()
  const items = [
    { tone: "open" as const, n: +m.n_comp_ok, label: "tuyển được người ở Việt Nam", href: "/?v=ok" },
    { tone: "unk" as const, n: +m.n_comp_unk, label: "chưa đủ căn cứ kết luận", href: "/?v=unk" },
    { tone: "closed" as const, n: +m.n_comp_no, label: "khoá, không tuyển ở VN", href: "/?v=no" },
  ]
  return (
    <div className="glow">
      <div className="rise">
        <Eyebrow>Sổ đăng ký địa lý tuyển dụng</Eyebrow>
        <h1 className="mt-4 max-w-[17ch] text-[clamp(34px,6vw,58px)]">
          Công ty nào <span className="grad">thật sự tuyển được</span> người ở Việt Nam
        </h1>
        <p className="mt-6 max-w-[58ch] text-[16px] leading-relaxed text-text-2">
          Hồ sơ của{" "}
          <b className="font-medium tabular-nums text-text">
            {(+m.n_companies).toLocaleString("vi-VN")}
          </b>{" "}
          công ty, dựng từ{" "}
          <b className="font-medium tabular-nums text-text">
            {(+m.n_jobs).toLocaleString("vi-VN")}
          </b>{" "}
          tin remote. Mỗi kết luận kèm trích dẫn nguyên văn từ tin gốc.
        </p>
      </div>

      <div className="mt-9">
        <DensityBar items={items} />
        <StatRow items={items} unit="công ty" />
      </div>

      <p className="rise mt-6 max-w-[62ch] text-[13px] leading-relaxed text-text-3" style={{ animationDelay: "240ms" }}>
        Địa lý tuyển và cơ chế hợp đồng là thuộc tính của{" "}
        <b className="font-medium text-text-2">công ty</b>, không phải của từng tin. Tin đổi hằng
        ngày; công ty đổi hằng quý. Cần trục tin thì xem{" "}
        <Link className="text-text-2 underline underline-offset-2 hover:text-text" href="/tin-mo">
          danh sách tin đang mở
        </Link>
        .
      </p>

      <ForCompanies />
    </div>
  )
}

/**
 * Khối duy nhất trên trang này nói với PHÍA CẦU.
 *
 * Đ3 (legal-options.md Mục 3) là đường có doanh thu mà không cần Giấy phép
 * dịch vụ việc làm — nhưng nó đang nằm sau mục nav thứ 7 và không ai tìm ra.
 * Đặt ở đây vì người đọc trang này gồm cả người ở công ty nước ngoài đi tra
 * đối thủ, không chỉ kỹ sư Việt.
 *
 * Tiếng Anh có chủ ý: người trả tiền không đọc tiếng Việt. Khối tiếng Anh
 * giữa trang tiếng Việt là cố ý gây chú ý, không phải sót bản dịch — nên có
 * lang="en" để trình đọc màn hình đổi giọng đúng.
 */
async function ForCompanies() {
  // Số phải sống như mọi số khác trên site. Cứng ở đây thì tới ngày kho đổi,
  // khối bán hàng thành khối nói dối — và nó là khối duy nhất người trả tiền đọc.
  const m = await one<{ mech: number; mech_ok: number }>(
    `SELECT count(*) mech, sum(verdict='ok') mech_ok
     FROM company WHERE mechanism <> 'unknown'`,
  )
  return (
    <aside
      className="rise mt-9 rounded-lg border border-line bg-card p-5 sm:p-6"
      style={{ animationDelay: "300ms" }}
      lang="en"
    >
      <p className="font-mono text-[11px] uppercase tracking-wider text-text-3">
        For companies hiring remotely
      </p>
      <p className="mt-3 max-w-[62ch] text-[14px] leading-relaxed text-text-2">
        {m?.mech ?? 0} companies in this corpus already hire through an employer-of-record or
        contractor arrangement — the machinery needed to hire anywhere.{" "}
        <b className="text-text">{m?.mech_ok ?? 0}</b> of them include Vietnam. If you already run
        an EOR, adding it is a policy edit, not a project.
      </p>
      <Link
        href="/hiring-in-sea"
        className="mt-4 inline-block rounded-sm border border-line bg-raised px-4 py-[11px] text-[13px] leading-5 transition-colors hover:border-field"
      >
        Read the market brief →
      </Link>
    </aside>
  )
}

async function Registry({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; mech?: string; p?: string; v?: string }>
}) {
  const sp = await searchParams
  const q = (sp.q ?? "").trim()
  const page = Math.max(1, +(sp.p ?? 1) || 1)
  const off = (page - 1) * PAGE

  // Xếp công ty tuyển được lên trước, rồi theo số vị trí mở. FTS chỉ dùng khi
  // có từ khoá — LIKE '%x%' quét toàn bảng, không dùng được ở quy mô này.
  const where: string[] = []
  const args: unknown[] = []
  if (sp.v) { where.push("c.verdict = ?"); args.push(sp.v) }
  if (sp.mech) { where.push("c.mechanism = ?"); args.push(sp.mech) }
  const join = q ? "JOIN company_fts f ON f.slug = c.slug AND company_fts MATCH ?" : ""
  const pre: unknown[] = q ? [`${q.replace(/["*]/g, "")}*`] : []
  const cond = where.length ? `WHERE ${where.join(" AND ")}` : ""
  const order = `ORDER BY CASE c.verdict WHEN 'ok' THEN 0 WHEN 'unk' THEN 1 ELSE 2 END,
                 c.n_global DESC, c.n_jobs DESC, c.name`

  const rows = await all<Company>(
    `SELECT c.* FROM company c ${join} ${cond} ${order} LIMIT ? OFFSET ?`,
    ...pre, ...args, PAGE + 1, off,
  )
  const more = rows.length > PAGE
  const list = rows.slice(0, PAGE)

  if (!list.length) return <EmptyState q={q} hasFilter={Boolean(sp.v || sp.mech)} />

  const qs = (p: number) => {
    const u = new URLSearchParams()
    if (q) u.set("q", q)
    if (sp.mech) u.set("mech", sp.mech)
    if (sp.v) u.set("v", sp.v)
    if (p > 1) u.set("p", String(p))
    return u.toString() ? `/?${u}` : "/"
  }

  return (
    <>
      <ul className="mt-8 divide-y divide-line-2/60">
        {list.map((c, i) => <Row key={c.slug} c={c} i={i} />)}
      </ul>
      <nav aria-label="Phân trang" className="mt-8 flex items-center gap-1.5 font-mono text-[12.5px]">
        {page > 1 && (
          <Link
            className="rounded-sm border border-line px-3 py-2.5 transition-colors hover:border-field"
            href={qs(page - 1)}
          >
            ← trước
          </Link>
        )}
        <span aria-current="page" className="px-3 py-2.5 tabular-nums text-text-3">
          trang {page}
        </span>
        {more && (
          <Link
            className="rounded-sm border border-line px-3 py-2.5 transition-colors hover:border-field"
            href={qs(page + 1)}
          >
            sau →
          </Link>
        )}
      </nav>
    </>
  )
}

function Row({ c, i }: { c: Company; i: number }) {
  const locked = parseLocked(c.locked)
  return (
    <li
      className="rise -mx-3 rounded-md transition-colors duration-150 hover:bg-card/70"
      style={{ animationDelay: `${Math.min(i, 12) * 22}ms` }}
    >
      <Link
        href={`/cong-ty/${c.slug}`}
        className="grid grid-cols-1 items-center gap-y-2.5 px-3 py-3.5 sm:grid-cols-[max-content_1fr_max-content] sm:gap-x-4 sm:gap-y-0"
      >
        <Badge tone={c.verdict}>{SHORT[c.verdict_label] ?? c.verdict_label}</Badge>

        <span className="min-w-0">
          <span className="block truncate text-[15px] font-medium">{c.name}</span>
          {/* Địa lý là dữ liệu, không phải câu văn. Chip cho quét bằng mắt thay
              vì bắt đọc hết một mệnh đề. */}
          <span className="mt-1.5 flex flex-wrap items-center gap-1.5">
            {c.n_global > 0 && <ToneChip tone="open">{c.n_global} toàn cầu</ToneChip>}
            {c.n_vn > 0 && <ToneChip tone="open">{c.n_vn} mở cho VN</ToneChip>}
            {locked.slice(0, 4).map(([code, n]) => (
              <Chip key={code}>
                {cname(code)} <span className="tabular-nums text-text-3">{n}</span>
              </Chip>
            ))}
            {locked.length > 4 && (
              <span className="font-mono text-[11px] tabular-nums text-text-3">
                +{locked.length - 4}
              </span>
            )}
            {!c.n_global && !c.n_vn && !locked.length && (
              <span className="font-mono text-[11px] text-text-3">
                không đủ căn cứ về địa lý tuyển
              </span>
            )}
          </span>
        </span>

        <span className="whitespace-nowrap font-mono text-[11px] tabular-nums text-text-3">
          {c.n_jobs} tin · {MECH[c.mechanism] ?? c.mechanism}
        </span>
      </Link>
    </li>
  )
}
