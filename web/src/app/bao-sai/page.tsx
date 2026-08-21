import Link from "next/link"
import { Suspense } from "react"
import { all } from "@/lib/db"
import { Eyebrow, Lead, Note, PageTitle } from "@/components/Page"

export const metadata = { title: "Báo sai đã nhận", robots: { index: false } }

const LABEL: Record<string, string> = {
  "nhan-sai": "Nhãn sai",
  "tin-da-dong": "Tin đã đóng",
  "trich-dan-sai": "Trích dẫn sai",
  khac: "Khác",
}

type Row = {
  id: number
  kind: string
  ref: string
  reason: string
  note: string | null
  created_at: string
  resolved: number
}

/**
 * Trang nội bộ — [OPERATIONS.md](../../OPERATIONS.md) xếp 30 phút/tuần để đọc.
 *
 * Không cache: đây là hàng đợi công việc, dữ liệu cũ ở đây vô dụng.
 * `robots: noindex` — không có gì bí mật, nhưng cũng không cần Google lập chỉ mục.
 */
export default function Reports() {
  return (
    <>
      <Eyebrow>Nội bộ</Eyebrow>
      <PageTitle>Báo sai đã nhận</PageTitle>
      {/* Hàng đợi công việc — dữ liệu cũ ở đây vô dụng, nên KHÔNG cache.
          Bọc Suspense để Next dựng vỏ tĩnh rồi stream danh sách lúc chạy. */}
      <Suspense fallback={<Note>Đang tải báo cáo…</Note>}>
        <Queue />
      </Suspense>
    </>
  )
}

async function Queue() {
  const rows = await all<Row>(
    "SELECT * FROM report ORDER BY resolved, created_at DESC LIMIT 200",
  )
  const open = rows.filter((r) => !r.resolved)

  return (
    <>
      <Lead>
        <b className="tabular-nums text-text">{open.length}</b> báo cáo chưa xử lý.
        Tỷ lệ báo sai là chỉ số sống còn — đọc hằng tuần, và{" "}
        <b className="text-text">đọc lại tin gốc trước khi sửa nhãn</b>.
      </Lead>

      {rows.length === 0 ? (
        <Note>Chưa có báo cáo nào.</Note>
      ) : (
        <ul className="mt-8 divide-y divide-line-2/60">
          {rows.map((r) => (
            <li key={r.id} className="py-4">
              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`rounded-xs border px-2 py-[3px] font-mono text-[11px] ${
                    r.resolved
                      ? "border-line bg-card text-text-3"
                      : "border-unk/35 bg-unk-bg text-unk"
                  }`}
                >
                  {LABEL[r.reason] ?? r.reason}
                </span>
                <Link
                  href={r.kind === "job" ? `/viec/${r.ref}` : `/cong-ty/${r.ref}`}
                  className="text-[14px] font-medium hover:underline"
                >
                  {r.ref}
                </Link>
                <span className="font-mono text-[11px] text-text-3">
                  {r.kind} · {r.created_at.slice(0, 16).replace("T", " ")}
                </span>
              </div>
              {r.note && (
                <p className="mt-2 rounded-xs border-l-2 border-line bg-card py-2 pl-3 pr-2.5 font-mono text-[12px] leading-relaxed text-text-2">
                  {r.note}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}

      <Note>
        Đánh dấu đã xử lý bằng SQL:{" "}
        <code className="rounded-xs border border-line bg-card px-1.5 py-0.5 font-mono text-[12px]">
          UPDATE report SET resolved=1 WHERE id=…
        </code>
      </Note>
    </>
  )
}
