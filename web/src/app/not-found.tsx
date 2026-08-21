import Link from "next/link"
import { Eyebrow } from "@/components/Page"

export const metadata = { title: "Không tìm thấy" }

/**
 * 3.666 URL công ty. Link cũ, gõ sai, công ty bị gỡ khỏi kho — tất cả đổ về
 * đây. Một trang 404 trống là ngõ cụt; phải có lối ra.
 */
export default function NotFound() {
  return (
    <div className="glow rise">
      <Eyebrow>404</Eyebrow>
      <h1 className="mt-4 max-w-[18ch] text-[clamp(28px,4.6vw,42px)]">
        Không có <span className="grad">trang này</span>
      </h1>
      <p className="mt-5 max-w-[56ch] text-[15.5px] leading-relaxed text-text-2">
        Công ty hoặc tin bạn tìm không có trong kho — có thể tin đã bị gỡ khỏi trang tuyển dụng
        gốc, hoặc công ty chưa bao giờ được thu thập.
      </p>
      <p className="mt-4 max-w-[56ch] text-[13px] leading-relaxed text-text-3">
        Kho chỉ có công ty tuyển qua <b className="text-text-2">Greenhouse, Lever, Ashby</b>.
        Tin biến mất khỏi nguồn sẽ bị gỡ trong vòng 48 giờ — đó là chủ ý, tin zombie phá đúng
        giá trị của trang này.
      </p>
      <p className="mt-7 flex flex-wrap gap-2">
        <Link
          href="/"
          className="rounded-sm border border-open/35 bg-open-bg px-4 py-2.5 text-[13.5px] text-open transition-colors hover:border-open/60"
        >
          Tra cứu công ty
        </Link>
        <Link
          href="/tin-mo"
          className="rounded-sm border border-line bg-card px-4 py-2.5 text-[13.5px] transition-colors hover:border-field"
        >
          Tin đang mở
        </Link>
        <Link
          href="/phuong-phap"
          className="rounded-sm border border-line bg-card px-4 py-2.5 text-[13.5px] transition-colors hover:border-field"
        >
          Giới hạn của kho
        </Link>
      </p>
    </div>
  )
}
