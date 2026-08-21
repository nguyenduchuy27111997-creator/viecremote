const TONE = {
  ok: "text-open bg-open-bg border-open/35",
  no: "text-closed bg-closed-bg border-closed/35",
  unk: "text-unk bg-unk-bg border-unk/35",
} as const

const DOT = { ok: "bg-open", no: "bg-closed", unk: "bg-unk" } as const

/**
 * `whitespace-nowrap` bắt buộc: một nhãn compact gãy xuống dòng thứ hai trông
 * như hai nhãn. Chấm màu phía trước cho phép quét trạng thái mà không cần đọc.
 */
export function Badge({ tone, children }: { tone: keyof typeof TONE; children: React.ReactNode }) {
  return (
    <span
      className={`inline-flex w-fit shrink-0 items-center gap-1.5 justify-self-start whitespace-nowrap rounded-sm border px-2.5 py-[6px] text-[10.5px] font-semibold uppercase leading-none tracking-[0.06em] ${TONE[tone]}`}
    >
      <span aria-hidden className={`size-[5px] rounded-full ${DOT[tone]}`} />
      {children}
    </span>
  )
}
