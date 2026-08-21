"use client"

import { useRouter, useSearchParams } from "next/navigation"
import { useEffect, useRef, useState, useTransition } from "react"

/**
 * Tra cứu đẩy vào URL, không giữ trong state cục bộ — kết quả chia sẻ được,
 * quay lui được, và việc lọc thật sự chạy trên máy chủ bằng FTS.
 *
 * Nhãn hiện rõ chứ không dùng placeholder làm nhãn: placeholder biến mất ngay
 * khi người dùng gõ chữ đầu tiên, đúng lúc họ cần nó nhất.
 */
export function SearchBox() {
  const sp = useSearchParams()
  const router = useRouter()
  const [q, setQ] = useState(sp.get("q") ?? "")
  const [pending, start] = useTransition()
  const box = useRef<HTMLInputElement>(null)

  // ⌘K / Ctrl+K nhảy thẳng vào ô tra cứu — phím tắt mà người dùng công cụ
  // kỹ thuật mặc định là có.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault()
        box.current?.focus()
        box.current?.select()
      }
    }
    addEventListener("keydown", onKey)
    return () => removeEventListener("keydown", onKey)
  }, [])

  useEffect(() => {
    const t = setTimeout(() => {
      const u = new URLSearchParams(sp.toString())
      q ? u.set("q", q) : u.delete("q")
      u.delete("p")
      const next = u.toString() ? `/?${u}` : "/"
      if (next !== `${location.pathname}${location.search}`) {
        start(() => router.replace(next, { scroll: false }))
      }
    }, 250)
    return () => clearTimeout(t)
  }, [q, sp, router])

  const setParam = (k: string, v: string) => {
    const u = new URLSearchParams(sp.toString())
    v ? u.set(k, v) : u.delete(k)
    u.delete("p")
    start(() => router.replace(u.toString() ? `/?${u}` : "/", { scroll: false }))
  }

  const field =
    "rounded-sm border border-line bg-bg px-2.5 py-2 text-[13px] text-text transition-colors duration-150 hover:border-field"

  return (
    <search className="rise mt-9 rounded-lg border border-line bg-card p-4" style={{ animationDelay: "280ms" }}>
      <div className="flex flex-wrap items-end gap-x-5 gap-y-3">
        <p className="flex min-w-56 flex-1 flex-col gap-1.5">
          <label htmlFor="q" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
            Tên công ty
          </label>
          <span className="relative flex items-center">
            <input
              id="q"
              ref={box}
              type="search"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="canonical, supabase…"
              className={`${field} w-full pr-14 placeholder:text-text-3`}
            />
            <kbd
              aria-hidden
              className="pointer-events-none absolute right-2 rounded-xs border border-line bg-raised px-1.5 py-0.5 font-mono text-[10px] text-text-3"
            >
              ⌘K
            </kbd>
          </span>
        </p>

        <p className="flex flex-col gap-1.5">
          <label htmlFor="v" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
            Kết luận
          </label>
          <select id="v" value={sp.get("v") ?? ""} onChange={(e) => setParam("v", e.target.value)} className={field}>
            <option value="">Tất cả</option>
            <option value="ok">Tuyển được ở VN</option>
            <option value="unk">Chưa xác định</option>
            <option value="no">Không tuyển ở VN</option>
          </select>
        </p>

        {/* Chỉ 3% tin nêu cơ chế hợp đồng. Không ghi rõ độ phủ thì bộ lọc này
            cho người dùng cảm giác lọc được một thứ mà 91% dữ liệu là "không rõ"
            — đúng kiểu hứa quá khả năng mà sứ mệnh cấm. */}
        <p className="flex flex-col gap-1.5">
          <label htmlFor="mech" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
            Cơ chế <span className="normal-case tracking-normal">(chỉ 3% tin nêu)</span>
          </label>
          <select id="mech" value={sp.get("mech") ?? ""} onChange={(e) => setParam("mech", e.target.value)} className={field}>
            <option value="">Tất cả</option>
            <option value="eor">EOR</option>
            <option value="contractor">Nhà thầu</option>
            <option value="unknown">Không rõ</option>
          </select>
        </p>
      </div>

      {/* aria-live để người dùng trình đọc màn hình biết kết quả đang đổi —
          nếu không, việc lọc diễn ra hoàn toàn im lặng với họ. */}
      <p role="status" aria-live="polite" className="mt-2.5 h-4 font-mono text-[11px] text-text-3">
        {pending ? "Đang tra cứu…" : ""}
      </p>
    </search>
  )
}
