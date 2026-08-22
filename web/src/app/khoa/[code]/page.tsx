import Link from "next/link"
import { notFound } from "next/navigation"
import type { Metadata } from "next"
import { all, one, type Company } from "@/lib/db"
import { cname, CNAME } from "@/lib/countries"
import { Badge } from "@/components/Badge"
import { Crumb, Eyebrow, Lead, Note, ToneChip } from "@/components/Page"

// Kho dựng lại mỗi ngày; ISR thường thay cho "use cache".
export const revalidate = 86400

const SHORT: Record<string, string> = {
  "Tuyển toàn cầu": "Toàn cầu",
  "Tuyển được ở Việt Nam": "Mở cho VN",
  "Chưa xác định": "Chưa rõ",
  "Phần lớn khoá, còn tin chưa rõ": "Phần lớn khoá",
  "Không tuyển ở Việt Nam": "Khoá",
}

/**
 * Dựng sẵn TẤT CẢ 104 mã nước, và khoá không cho mã ngoài danh sách.
 *
 * Vì sao không dùng App Shell như trang công ty: với PPR, vỏ tĩnh được gửi kèm
 * status 200 TRƯỚC khi biết param có hợp lệ không — nên `notFound()` stream sau
 * không đổi được status. `/khoa/zzz` trả 200, và Google sẽ lập chỉ mục rác.
 *
 * Ở đây tập param là ĐÓNG và nhỏ (104) nên dựng hết, và dùng `instant = false`
 * để route CHẶN cho tới khi biết param — đổi lại điều hướng không còn tức thì,
 * nhưng status code đúng. Với 104 trang dựng sẵn thì gần như không ai chạm vào
 * đường chặn đó. Trang công ty KHÔNG làm vậy được: 3.666 slug và còn tăng.
 *
 * (`dynamicParams` không dùng chung với cacheComponents được — cùng họ với
 * `revalidate`. `instant = false` là lối thoát mà chính thông báo lỗi chỉ ra.)
 */

export async function generateStaticParams() {
  const rows = await all<{ code: string }>("SELECT DISTINCT code FROM locked")
  return rows.map((r) => ({ code: r.code.toLowerCase() }))
}

async function load(code: string) {
  const up = code.toUpperCase()
  if (!CNAME[up] && up.length > 6) return null
  const rows = await all<Company & { locked_jobs: number }>(
    `SELECT c.*, l.n_jobs AS locked_jobs FROM locked l
     JOIN company c ON c.slug = l.slug
     WHERE l.code = ? ORDER BY l.n_jobs DESC, c.name LIMIT 300`,
    up,
  )
  if (!rows.length) return null
  const tot = await one<{ n: number; j: number }>(
    "SELECT count(*) n, sum(n_jobs) j FROM locked WHERE code = ?",
    up,
  )
  return { up, rows, n: tot?.n ?? rows.length, j: tot?.j ?? 0 }
}

export async function generateMetadata({
  params,
}: { params: Promise<{ code: string }> }): Promise<Metadata> {
  const d = await load((await params).code)
  if (!d) return {}
  return {
    title: `${d.n} công ty khoá tuyển vào ${cname(d.up)}`,
    description: `Danh sách công ty remote có mệnh đề giới hạn tuyển dụng vào ${cname(d.up)}, kèm trích dẫn từ tin gốc.`,
  }
}

export default async function LockedCountry({
  params,
}: { params: Promise<{ code: string }> }) {
  const d = await load((await params).code)
  if (!d) notFound()

  return (
    <>
      <div className="glow rise">
        <Crumb to="/khoa" label="Khoá tuyển" current={cname(d.up)} />
        <Eyebrow>{d.n.toLocaleString("vi-VN")} công ty · {d.j.toLocaleString("vi-VN")} tin</Eyebrow>
        <h1 className="mt-4 max-w-[19ch] text-[clamp(28px,4.6vw,42px)]">
          Công ty khoá tuyển vào <span className="grad">{cname(d.up)}</span>
        </h1>
        <Lead>
          Mỗi công ty dưới đây có ít nhất một tin ghi mệnh đề giới hạn tuyển dụng vào{" "}
          {cname(d.up)}. <b className="text-text">Không có nghĩa là công ty đó khoá hoàn toàn</b> —
          nhiều công ty khoá một số vị trí và mở toàn cầu ở vị trí khác.
        </Lead>
      </div>

      <ul className="mt-9 divide-y divide-line-2/60">
        {d.rows.map((c, i) => (
          <li
            key={c.slug}
            className="rise -mx-3 rounded-md transition-colors duration-150 hover:bg-card"
            style={{ animationDelay: `${Math.min(i, 12) * 22}ms` }}
          >
            <Link
              href={`/cong-ty/${c.slug}`}
              className="grid grid-cols-1 items-center gap-y-2.5 px-3 py-3.5 sm:grid-cols-[max-content_1fr_max-content] sm:gap-x-4 sm:gap-y-0"
            >
              <Badge tone={c.verdict}>{SHORT[c.verdict_label] ?? c.verdict_label}</Badge>
              <span className="min-w-0">
                <span className="block truncate text-[15px] font-medium">{c.name}</span>
                <span className="mt-1.5 flex flex-wrap items-center gap-1.5">
                  <ToneChip tone="closed">{c.locked_jobs} tin khoá vào {cname(d.up)}</ToneChip>
                  {c.n_global > 0 && <ToneChip tone="open">{c.n_global} mở toàn cầu</ToneChip>}
                  {c.n_vn > 0 && <ToneChip tone="open">{c.n_vn} mở cho VN</ToneChip>}
                </span>
              </span>
              <span className="whitespace-nowrap font-mono text-[11px] tabular-nums text-text-3">
                {c.n_jobs} tin
              </span>
            </Link>
          </li>
        ))}
      </ul>

      {d.n > d.rows.length && (
        <Note>
          Hiển thị {d.rows.length} công ty khoá nhiều tin nhất trong tổng số{" "}
          {d.n.toLocaleString("vi-VN")}.
        </Note>
      )}
    </>
  )
}
