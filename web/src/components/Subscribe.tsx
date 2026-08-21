"use client"

import Link from "next/link"
import { useEffect, useRef, useState } from "react"

/**
 * Kênh sở hữu duy nhất. Không có nó thì mọi lưu lượng từ bài công bố bay hết
 * sau một tuần.
 *
 * Đổi lại: email LÀ dữ liệu cá nhân, nên form phải nói THẲNG sẽ dùng để làm gì
 * ngay tại chỗ nhập — không giấu trong trang điều khoản.
 */
export function Subscribe() {
  const [state, setState] = useState<"idle" | "sending" | "done" | "pending" | "error">("idle")
  const [msg, setMsg] = useState("")
  const mounted = useRef(0)

  useEffect(() => { mounted.current = Date.now() }, [])

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const f = new FormData(e.currentTarget)
    setState("sending")
    try {
      const r = await fetch("/api/dang-ky", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          email: f.get("email"),
          website: f.get("website"),
          elapsed: Date.now() - mounted.current,
        }),
      })
      const j = (await r.json()) as { ok?: boolean; error?: string; pending?: boolean }
      if (!j.ok) throw new Error(j.error || "Gửi thất bại")
      setState(j.pending ? "pending" : "done")
    } catch (err) {
      setState("error")
      setMsg(err instanceof Error ? err.message : "Gửi thất bại")
    }
  }

  if (state === "done" || state === "pending")
    return (
      <p role="status" className="rounded-md border border-open/35 bg-open-bg px-4 py-3 text-[13px] text-open">
        {state === "done"
          ? "Đã gửi thư xác nhận. Bấm đường dẫn trong thư để hoàn tất — chưa bấm thì chưa tính là đăng ký."
          : "Đã ghi nhận. Hệ thống gửi thư chưa được cấu hình nên chưa có thư xác nhận."}
      </p>
    )

  return (
    <form onSubmit={submit} className="max-w-[52ch]">
      <label htmlFor="sub" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
        Nhận tin khi kho đổi đáng kể
      </label>
      <div className="mt-2 flex flex-wrap gap-2">
        <input
          id="sub"
          name="email"
          type="email"
          required
          placeholder="ban@vidu.com"
          className="min-w-52 flex-1 rounded-sm border border-line bg-bg px-3 py-[11px] text-[13px] leading-5 transition-colors placeholder:text-text-3 hover:border-field"
        />
        <input type="text" name="website" tabIndex={-1} autoComplete="off" aria-hidden
          className="absolute left-[-9999px] size-px opacity-0" />
        <button
          type="submit"
          disabled={state === "sending"}
          className="rounded-sm border border-line bg-raised px-4 py-[11px] text-[13px] leading-5 transition-colors hover:border-field disabled:opacity-50"
        >
          {state === "sending" ? "Đang gửi…" : "Đăng ký"}
        </button>
      </div>
      <p className="mt-2.5 text-[12px] leading-relaxed text-text-3">
        Cần xác nhận qua thư. Không quảng cáo, không bán địa chỉ cho ai, huỷ một cú bấm.{" "}
        <Link className="underline underline-offset-2 hover:text-text-2" href="/rieng-tu">
          Cách dữ liệu được xử lý
        </Link>
        .
      </p>
      {state === "error" && <p role="alert" className="mt-2 text-[12.5px] text-closed">{msg}</p>}
    </form>
  )
}
