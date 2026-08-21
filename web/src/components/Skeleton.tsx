/**
 * Khung chờ phải CÙNG KÍCH THƯỚC với nội dung thật. Một dòng "đang tải…" cao
 * 20px rồi bị thay bằng danh sách cao 900px là cú nhảy bố cục — đúng thứ CLS đo.
 */
export function RowSkeleton({ n = 8 }: { n?: number }) {
  return (
    <ul aria-hidden className="mt-8 animate-pulse">
      {Array.from({ length: n }, (_, i) => (
        <li
          key={i}
          className="grid grid-cols-1 gap-y-2.5 rounded-md px-3 py-4 sm:grid-cols-[max-content_1fr] sm:gap-x-5 sm:gap-y-0"
        >
          <span className="h-[24px] w-[104px] rounded-sm bg-line-2" />
          <div className="space-y-2">
            <span className="block h-[18px] w-1/3 rounded-xs bg-line-2" />
            <span className="block h-[14px] w-2/3 rounded-xs bg-line-2" />
          </div>
        </li>
      ))}
    </ul>
  )
}

export function BlockSkeleton({ h }: { h: number }) {
  return <div aria-hidden style={{ height: h }} className="animate-pulse rounded-lg bg-line-2/60" />
}

/** Thông báo cho trình đọc màn hình trong lúc lỗ động chưa về. */
export function Loading({ label }: { label: string }) {
  return (
    <p role="status" aria-live="polite" className="sr-only">
      {label}
    </p>
  )
}
