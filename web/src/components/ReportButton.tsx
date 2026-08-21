"use client"

import { useEffect, useRef, useState } from "react"

const REASONS = [
  { v: "nhan-sai", t: "Nhãn sai — tin này thật ra ngược lại" },
  { v: "tin-da-dong", t: "Tin đã đóng hoặc bị gỡ" },
  { v: "trich-dan-sai", t: "Trích dẫn không khớp tin gốc" },
  { v: "khac", t: "Khác" },
]

/**
 * Sứ mệnh gọi tỷ lệ báo sai là chỉ số sống còn. Nút này là cách duy nhất đo nó.
 *
 * Không hỏi email, không tài khoản — rào cản càng thấp thì càng nhiều người
 * báo, và ta không muốn giữ dữ liệu cá nhân của ai cả.
 */
export function ReportButton({ kind, refId }: { kind: "job" | "company"; refId: string }) {
  const [open, setOpen] = useState(false)
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle")
  const [msg, setMsg] = useState("")
  const opened = useRef(0)

  useEffect(() => {
    if (open) opened.current = Date.now()
  }, [open])

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const f = new FormData(e.currentTarget)
    setState("sending")
    try {
      const r = await fetch("/api/bao-sai", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          kind,
          ref: refId,
          reason: f.get("reason"),
          note: f.get("note"),
          website: f.get("website"), // honeypot
          elapsed: Date.now() - opened.current,
        }),
      })
      const j = (await r.json()) as { ok?: boolean; error?: string }
      if (!r.ok || !j.ok) throw new Error(j.error || "Gửi thất bại")
      setState("done")
    } catch (err) {
      setState("error")
      setMsg(err instanceof Error ? err.message : "Gửi thất bại")
    }
  }

  if (state === "done")
    return (
      <p
        role="status"
        className="mt-8 rounded-md border border-open/35 bg-open-bg px-4 py-3 text-[13.5px] text-open"
      >
        Đã nhận. Tôi đọc báo cáo hằng tuần và sẽ đọc lại tin gốc trước khi sửa.
      </p>
    )

  if (!open)
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="mt-8 rounded-sm border border-line bg-card px-3.5 py-2.5 text-[13px] text-text-2 transition-colors hover:border-field hover:text-text"
      >
        Báo nhãn sai
      </button>
    )

  return (
    <form onSubmit={submit} className="mt-8 rounded-lg border border-line bg-card p-4">
      <p className="text-[14px] font-medium">Nhãn này sai ở đâu?</p>
      <p className="mt-1 text-[12.5px] text-text-3">
        Không cần email, không cần tài khoản. Tôi không lưu bất kỳ thông tin cá nhân nào.
      </p>

      <fieldset className="mt-4">
        <legend className="sr-only">Lý do</legend>
        {REASONS.map((r, i) => (
          <label key={r.v} className="flex items-start gap-2.5 py-1.5 text-[13.5px] text-text-2">
            <input type="radio" name="reason" value={r.v} defaultChecked={i === 0} className="mt-1" />
            {r.t}
          </label>
        ))}
      </fieldset>

      <label className="mt-3 block">
        <span className="font-mono text-[11px] uppercase tracking-wider text-text-3">
          Ghi chú <span className="normal-case">(tuỳ chọn)</span>
        </span>
        <textarea
          name="note"
          rows={3}
          maxLength={600}
          placeholder="Câu nào trong tin gốc cho thấy nhãn sai?"
          className="mt-1.5 w-full rounded-sm border border-line bg-bg px-2.5 py-2 text-[13px] transition-colors placeholder:text-text-3 hover:border-field"
        />
      </label>

      {/* Honeypot: ẩn với người, hấp dẫn với bot. aria-hidden + tabIndex để
          trình đọc màn hình và bàn phím không bao giờ chạm tới. */}
      <input
        type="text"
        name="website"
        tabIndex={-1}
        autoComplete="off"
        aria-hidden
        className="absolute left-[-9999px] size-px opacity-0"
      />

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <button
          type="submit"
          disabled={state === "sending"}
          className="rounded-sm border border-open/35 bg-open-bg px-4 py-2.5 text-[13px] text-open transition-colors hover:border-open/60 disabled:opacity-50"
        >
          {state === "sending" ? "Đang gửi…" : "Gửi báo cáo"}
        </button>
        <button
          type="button"
          onClick={() => setOpen(false)}
          className="rounded-sm border border-line px-4 py-2.5 text-[13px] text-text-2 transition-colors hover:border-field"
        >
          Huỷ
        </button>
        {state === "error" && <span role="alert" className="text-[12.5px] text-closed">{msg}</span>}
      </div>
    </form>
  )
}
