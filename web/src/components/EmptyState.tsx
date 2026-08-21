import Link from "next/link"

/** "0 kết quả" là ngõ cụt. Luôn kèm lối ra: bỏ bộ lọc, hoặc gợi ý cụ thể. */
export function EmptyState({ q, hasFilter }: { q?: string; hasFilter: boolean }) {
  return (
    <div className="rise mt-8 rounded-lg border border-line bg-card px-6 py-8">
      <p className="text-[15.5px] font-medium">
        {q ? <>Không có công ty nào tên gần với “{q}”.</> : <>Không có công ty nào khớp bộ lọc.</>}
      </p>
      <ul className="mt-3 space-y-1.5 text-[13.5px] leading-relaxed text-text-2">
        <li>
          Kho chỉ có công ty tuyển qua <b className="text-text">Greenhouse, Lever, Ashby</b> —
          công ty dùng nền tảng khác sẽ không xuất hiện.
        </li>
        <li>Tên trong kho là slug bảng tuyển dụng, thường viết liền và không dấu.</li>
        {hasFilter && <li>Thử bỏ bớt bộ lọc.</li>}
      </ul>
      <p className="mt-5 flex flex-wrap gap-2">
        <Link
          href="/"
          className="rounded-sm border border-line bg-raised px-3 py-2 text-[13px] transition-colors hover:border-field"
        >
          Xoá hết bộ lọc
        </Link>
        <Link
          href="/?v=ok"
          className="rounded-sm border border-open/35 bg-open-bg px-3 py-2 text-[13px] text-open transition-colors hover:border-open/60"
        >
          Xem công ty tuyển được ở VN
        </Link>
        <Link
          href="/phuong-phap"
          className="rounded-sm border border-line bg-raised px-3 py-2 text-[13px] transition-colors hover:border-field"
        >
          Giới hạn của kho
        </Link>
      </p>
    </div>
  )
}
