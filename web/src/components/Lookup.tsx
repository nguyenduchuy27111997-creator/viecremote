import Link from "next/link"
import { all } from "@/lib/db"
import { ename } from "@/lib/countries"

/** PH/ID/TH/MY — tín hiệu mạnh nhất trong kho. Xem tools/prospects.py. */
const SEA = new Set(["PH", "ID", "TH", "MY"])

type Hit = { slug: string; name: string; verdict: string; n_jobs: number; locked: string }

/**
 * Ô tra cứu cho PHÍA CẦU — để công ty tự tìm chính mình.
 *
 * Form GET thuần, không JavaScript phía client: kết quả có URL riêng, chia sẻ
 * được, quay lui được, và chạy cả khi script bị chặn. Ô tra ở trang chủ dùng
 * client component vì nó lọc một danh sách dài có phân trang; ở đây chỉ cần
 * tìm một cái tên rồi đi tiếp, nên thêm JavaScript là thêm thứ hỏng được mà
 * không đổi gì.
 */
export async function Lookup({ q }: { q?: string }) {
  const query = (q ?? "").trim().slice(0, 60)
  let hits: Hit[] = []

  if (query) {
    // FTS5 cần chuỗi truy vấn hợp lệ. Bọc token bằng dấu nháy kép và thêm *
    // để tra được tiền tố — người ta gõ "snow" chứ ít khi gõ đủ "snowflake".
    const term = query.replace(/["']/g, " ").split(/\s+/).filter(Boolean)
      .map((t) => `"${t}"*`).join(" ")
    if (term) {
      hits = await all<Hit>(
        `SELECT c.slug, c.name, c.verdict, c.n_jobs, c.locked
         FROM company_fts f JOIN company c ON c.slug = f.slug
         WHERE company_fts MATCH ? ORDER BY c.n_jobs DESC LIMIT 8`,
        term,
      )
    }
  }

  return (
    <div lang="en">
      <form action="/hiring-in-vietnam" method="get" className="max-w-[52ch]">
        <label htmlFor="lk" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
          Look up your own company
        </label>
        <div className="mt-2 flex flex-wrap gap-2">
          <input
            id="lk"
            name="q"
            defaultValue={query}
            placeholder="Snowflake, GitLab, your company…"
            className="min-w-52 flex-1 rounded-sm border border-line bg-bg px-3 py-[11px] text-[13px] leading-5 transition-colors placeholder:text-text-3 hover:border-field"
          />
          <button
            type="submit"
            className="rounded-sm border border-line bg-raised px-4 py-[11px] text-[13px] leading-5 transition-colors hover:border-field"
          >
            Look up
          </button>
        </div>
        <p className="mt-2.5 max-w-[52ch] text-[12px] leading-relaxed text-text-3">
          See what your own job postings say about where you can hire — read from your public
          board, quoted clause by clause.
        </p>
      </form>

      {query && (
        <div className="mt-5">
          {hits.length === 0 ? (
            <p className="text-[13.5px] text-text-3">
              No company matching <b className="text-text-2">{query}</b> in this corpus. It tracks
              boards on Greenhouse, Ashby and Lever — a company hiring elsewhere will not appear.
            </p>
          ) : (
            <ul className="divide-y divide-line rounded-lg border border-line bg-card">
              {hits.map((h) => {
                const sea = JSON.parse(h.locked || "[]")
                  .map(([c]: [string, number]) => c)
                  .filter((c: string) => SEA.has(c))
                return (
                  <li key={h.slug}>
                    <Link
                      href={`/hiring-in-vietnam/${h.slug}`}
                      className="flex flex-wrap items-baseline gap-x-3 gap-y-1 px-4 py-3 text-[13.5px] transition-colors hover:bg-raised"
                    >
                      <span className="font-medium">{h.name}</span>
                      <span className="font-mono text-[11.5px] text-text-3">
                        {h.n_jobs.toLocaleString("en-US")} postings
                      </span>
                      {sea.length > 0 && (
                        <span className="font-mono text-[11px] text-open">
                          hires in {sea.map(ename).join(", ")}
                        </span>
                      )}
                    </Link>
                  </li>
                )
              })}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}
