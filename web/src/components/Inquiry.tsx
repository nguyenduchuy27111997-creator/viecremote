"use client"

import Link from "next/link"
import { useEffect, useRef, useState } from "react"

/**
 * Phía CẦU — sản phẩm Đ3 (legal-options.md Mục 3).
 *
 * KHÔNG phải cổng đổi email lấy báo cáo (sửa 24/08). Toàn bộ báo cáo nằm công
 * khai trên trang, không cần đăng ký gì — bắt đổi email mới được đọc là tự tạo
 * ra một việc phải làm tay cho người vận hành, đúng thứ mô hình này tránh.
 * Form giờ chỉ để báo khi kho ĐỔI, tức là thứ không đọc sẵn trên trang được.
 *
 * Đây là con đường duy nhất có doanh thu mà không cần giấy phép nào, và lý do
 * là NHỮNG GÌ NÓ KHÔNG LÀM: không thu dữ liệu kỹ sư, không giới thiệu ai, không
 * tư vấn cho người lao động. Bán nghiên cứu về chính sách tuyển dụng của công
 * ty — dữ liệu tổ chức, không phải dữ liệu người.
 *
 * KHÔNG thêm trường nào về ứng viên vào form này. Một ô "gửi CV của bạn" biến
 * nó từ nghiên cứu thị trường thành dịch vụ việc làm có điều kiện, và đổi hẳn
 * chế độ pháp lý áp dụng cho cả sản phẩm.
 *
 * Tiếng Anh vì khách là công ty nước ngoài — cùng lý do trang này không dịch.
 */
export function Inquiry() {
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle")
  const [msg, setMsg] = useState("")
  const mounted = useRef(0)

  useEffect(() => { mounted.current = Date.now() }, [])

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const f = new FormData(e.currentTarget)
    setState("sending")
    try {
      const r = await fetch("/api/inquiry", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          company: f.get("company"),
          email: f.get("email"),
          role: f.get("role"),
          note: f.get("note"),
          website: f.get("website"),
          elapsed: Date.now() - mounted.current,
        }),
      })
      const j = (await r.json()) as { ok?: boolean; error?: string }
      if (!j.ok) throw new Error(j.error || "Could not send")
      setState("done")
    } catch (err) {
      setState("error")
      setMsg(err instanceof Error ? err.message : "Could not send")
    }
  }

  if (state === "done")
    return (
      <p role="status" className="rounded-md border border-open/35 bg-open-bg px-4 py-3 text-[13px] text-open">
        Noted. You will hear from us when a company opens or closes to Vietnam — not on a
        schedule, only when the corpus actually changes. Nothing else.
      </p>
    )

  const field =
    "w-full rounded-sm border border-line bg-bg px-3 py-[11px] text-[13px] leading-5 " +
    "transition-colors placeholder:text-text-3 hover:border-field"

  return (
    <form onSubmit={submit} className="max-w-[54ch]">
      <div className="grid gap-3 sm:grid-cols-2">
        <div>
          <label htmlFor="iq-co" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
            Company
          </label>
          <input id="iq-co" name="company" required placeholder="Acme Inc." className={`mt-2 ${field}`} />
        </div>
        <div>
          <label htmlFor="iq-em" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
            Work email
          </label>
          <input id="iq-em" name="email" type="email" required placeholder="you@acme.com" className={`mt-2 ${field}`} />
        </div>
      </div>

      <div className="mt-3">
        <label htmlFor="iq-role" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
          Roles you are hiring for <span className="normal-case tracking-normal">(optional)</span>
        </label>
        <input id="iq-role" name="role" placeholder="Senior backend, platform, data" className={`mt-2 ${field}`} />
      </div>

      <div className="mt-3">
        <label htmlFor="iq-note" className="font-mono text-[11px] uppercase tracking-wider text-text-3">
          Anything specific <span className="normal-case tracking-normal">(optional)</span>
        </label>
        <textarea id="iq-note" name="note" rows={3}
          placeholder="We run an EOR in 6 countries and want to know what adding Vietnam costs us."
          className={`mt-2 resize-y ${field}`} />
      </div>

      <input type="text" name="website" tabIndex={-1} autoComplete="off" aria-hidden
        className="absolute left-[-9999px] size-px opacity-0" />

      <button
        type="submit"
        disabled={state === "sending"}
        className="mt-4 rounded-sm border border-line bg-raised px-4 py-[11px] text-[13px] leading-5 transition-colors hover:border-field disabled:opacity-50"
      >
        {state === "sending" ? "Sending…" : "Notify me on changes"}
      </button>

      <p className="mt-3 max-w-[54ch] text-[12px] leading-relaxed text-text-3">
        We store your company name and work email to send those alerts and nothing else — no
        newsletter, no resale, no tracking pixel. Ask and it is deleted.{" "}
        <Link className="underline underline-offset-2 hover:text-text-2" href="/rieng-tu">
          How data is handled
        </Link>
        .
      </p>

      {state === "error" && <p role="alert" className="mt-2 text-[12.5px] text-closed">{msg}</p>}
    </form>
  )
}
