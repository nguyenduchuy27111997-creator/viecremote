import Link from "next/link"

/**
 * Mẫu dùng chung. Đặt ở đây thay vì lặp lại: năm trang tự viết tiêu đề riêng
 * là năm thang chữ khác nhau sau ba lần sửa.
 */

export function Eyebrow({ children }: { children: React.ReactNode }) {
  return (
    <p className="flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.16em] text-text-3">
      <span aria-hidden className="h-px w-6 bg-gradient-to-r from-open to-transparent" />
      {children}
    </p>
  )
}

export function PageTitle({ children }: { children: React.ReactNode }) {
  return <h1 className="mt-4 max-w-[19ch] text-[clamp(30px,5vw,46px)]">{children}</h1>
}

export function Lead({ children }: { children: React.ReactNode }) {
  return <p className="mt-5 max-w-[60ch] text-[15.5px] leading-relaxed text-text-2">{children}</p>
}

export function Note({ children }: { children: React.ReactNode }) {
  return <p className="mt-5 max-w-[64ch] text-[13px] leading-relaxed text-text-3">{children}</p>
}

export function Section({ title, hint, children }: {
  title: string
  hint?: React.ReactNode
  children: React.ReactNode
}) {
  return (
    <section className="mt-12">
      <h2 className="text-[20px]">{title}</h2>
      {hint && <p className="mt-2 max-w-[64ch] text-[12.5px] leading-relaxed text-text-3">{hint}</p>}
      {children}
    </section>
  )
}

export function Crumb({ to, label, current }: { to: string; label: string; current: string }) {
  return (
    <p className="font-mono text-[11.5px] text-text-3">
      <Link className="hover:text-text" href={to}>{label}</Link>{" "}
      <span aria-hidden className="text-text-3">/</span> {current}
    </p>
  )
}

export function Chip({ children }: { children: React.ReactNode }) {
  return (
    <span className="whitespace-nowrap rounded-xs border border-line bg-card px-2 py-[3px] font-mono text-[11px] text-text-2">
      {children}
    </span>
  )
}

export function ToneChip({ tone, children }: {
  tone: "open" | "closed" | "unk"
  children: React.ReactNode
}) {
  const c = {
    open: "border-open/35 bg-open-bg text-open",
    closed: "border-closed/35 bg-closed-bg text-closed",
    unk: "border-unk/35 bg-unk-bg text-unk",
  }[tone]
  return (
    <span className={`whitespace-nowrap rounded-xs border px-2 py-[3px] font-mono text-[11px] tabular-nums ${c}`}>
      {children}
    </span>
  )
}

export function KV({ k, children }: { k: string; children: React.ReactNode }) {
  return (
    <tr className="border-b border-line-2 last:border-0">
      <th className="block px-4 pr-4 pt-3 text-left align-top font-mono text-[11px] font-normal uppercase leading-relaxed tracking-wider text-text-3 sm:table-cell sm:w-72 sm:py-3">
        {k}
      </th>
      <td className="block px-4 pb-3 text-[14px] sm:table-cell sm:py-3">{children}</td>
    </tr>
  )
}

export function KVTable({ children }: { children: React.ReactNode }) {
  return (
    <div className="scroll-x mt-6 rounded-lg border border-line bg-card">
      <table className="w-full border-collapse">
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}

/** Hàng có thanh tỉ lệ. Thanh và số ở HAI ô riêng — gộp một ô thì thanh 100%
 *  đẩy con số lớn nhất, tức quan trọng nhất, ra ngoài khung. */
export function BarRow({ label, n, pct, tone = "closed", locale = "vi-VN" }: {
  label: React.ReactNode
  n: number
  pct: number
  tone?: "open" | "closed" | "unk"
  /** Trang phía cầu viết tiếng Anh: "1.793" kiểu Việt đọc thành một phẩy bảy chín ba. */
  locale?: "vi-VN" | "en-US"
}) {
  const bar = { open: "bg-open", closed: "bg-closed", unk: "bg-unk" }[tone]
  return (
    <tr className="border-b border-line-2 transition-colors duration-150 last:border-0 hover:bg-card">
      <th className="py-3 pl-4 pr-4 text-left align-top text-[13.5px] font-normal">{label}</th>
      <td className="w-[38%] py-3">
        <span className="block h-[7px] w-full overflow-hidden rounded-full bg-line-2">
          <span
            className={`block h-full min-w-[3px] rounded-full opacity-90 ${bar}`}
            style={{ width: `${Math.max(1, Math.min(100, pct))}%` }}
          />
        </span>
      </td>
      <td className="w-[1%] whitespace-nowrap py-3 pl-3 pr-4 text-right font-mono text-[12.5px] tabular-nums text-text-2">
        {n.toLocaleString(locale)}
      </td>
    </tr>
  )
}
