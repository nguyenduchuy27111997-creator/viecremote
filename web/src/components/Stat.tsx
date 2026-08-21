import Link from "next/link"

type Item = { tone: "open" | "closed" | "unk"; n: number; label: string; href: string }

const BAR = { open: "bg-open", closed: "bg-closed", unk: "bg-unk" } as const
const TXT = { open: "text-open", closed: "text-closed", unk: "text-unk" } as const
const RING = {
  open: "hover:border-open/45",
  closed: "hover:border-closed/45",
  unk: "hover:border-unk/45",
} as const

/**
 * Ba con số CHÍNH LÀ câu chuyện: 3% mở, 68% khoá. Chôn chúng trong một đoạn
 * văn là làm hỏng điều duy nhất trang này có để nói.
 *
 * `tabular-nums` bắt buộc: chữ số tỉ lệ làm 1.071 và 2.485 lệch cột, mắt mất
 * khả năng so sánh hai con số chỉ bằng cách nhìn.
 */
export function StatRow({ items, unit }: { items: Item[]; unit: string }) {
  const tot = items.reduce((a, s) => a + s.n, 0) || 1
  return (
    <section aria-label="Tổng quan">
      <ul className="grid grid-cols-1 gap-2.5 sm:grid-cols-3">
        {items.map((s, i) => (
          <li key={s.tone} className="rise" style={{ animationDelay: `${60 + i * 70}ms` }}>
            <Link
              href={s.href}
              className={`group relative block overflow-hidden rounded-lg border border-line bg-card p-5 transition-colors duration-200 ${RING[s.tone]}`}
            >
              {/* quầng sáng chỉ hiện khi rê chuột — phản hồi, không trang trí */}
              <span
                aria-hidden
                className={`pointer-events-none absolute -left-8 -top-14 size-36 rounded-full opacity-0 blur-2xl transition-opacity duration-300 group-hover:opacity-20 ${BAR[s.tone]}`}
              />
              <span className={`block h-[3px] w-8 rounded-full ${BAR[s.tone]}`} />
              <span
                className={`mt-4 block font-mono text-[38px] font-medium leading-none tracking-[-0.03em] tabular-nums ${TXT[s.tone]}`}
              >
                {s.n.toLocaleString("vi-VN")}
              </span>
              <span className="mt-2.5 block text-[13.5px] text-text-2 transition-colors group-hover:text-text">
                {s.label}
              </span>
              <span className="mt-1 block font-mono text-[11px] tabular-nums text-text-3">
                {((100 * s.n) / tot).toFixed(1)}% · {tot.toLocaleString("vi-VN")} {unit}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  )
}

/** Thanh mật độ: 3% trông ra 3%. Con số một mình không truyền được tỉ lệ. */
export function DensityBar({ items }: { items: Item[] }) {
  const tot = items.reduce((a, s) => a + s.n, 0) || 1
  return (
    <div aria-hidden className="mb-2.5 flex h-1.5 w-full gap-1">
      {items.map((s) => (
        <span
          key={s.tone}
          className={`rounded-full ${BAR[s.tone]}`}
          style={{ width: `${(100 * s.n) / tot}%` }}
        />
      ))}
    </div>
  )
}
