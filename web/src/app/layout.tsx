import type { Metadata } from "next"
import Link from "next/link"
import { Be_Vietnam_Pro, IBM_Plex_Mono } from "next/font/google"
import { Subscribe } from "@/components/Subscribe"
import { SITE_URL } from "@/lib/site"
import "./globals.css"

/**
 * Chỉ hai font: một sans, một mono. Không serif.
 *
 * Be Vietnam Pro được thiết kế RIÊNG cho tiếng Việt — dấu xếp chồng (ế, ộ, ữ)
 * đặt đúng chỗ. Tự host qua next/font: tải lúc build, không request chặn render
 * sang bên thứ ba, không CLS.
 */
const sans = Be_Vietnam_Pro({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
  variable: "--font-be-vietnam",
})
const mono = IBM_Plex_Mono({
  subsets: ["latin", "vietnamese"],
  weight: ["400", "500"],
  display: "swap",
  variable: "--font-plex-mono",
})

export const metadata: Metadata = {
  // Không có metadataBase thì ảnh OG được giải về http://localhost:3000 —
  // mọi lượt chia sẻ trên production sẽ hiện thẻ hỏng.
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Công ty nào thật sự tuyển được người ở Việt Nam",
    template: "%s — viecremote",
  },
  description:
    "Hồ sơ địa lý tuyển dụng của hàng nghìn công ty remote, mỗi kết luận kèm trích dẫn nguyên văn từ tin gốc.",
}

const NAV = [
  { href: "/", label: "Công ty" },
  { href: "/tin-mo", label: "Tin mở" },
  { href: "/khoa", label: "Khoá tuyển" },
  { href: "/lam-gi", label: "Làm gì" },
  { href: "/vi-sao-bi-loai", label: "Vì sao bị loại" },
  { href: "/phuong-phap", label: "Phương pháp" },
]

/**
 * Cổng GĐ 0 ghi: "ngày 30, dưới 100 người dùng duy nhất -> dừng lại". Không có
 * analytics thì cổng quan trọng nhất của cả kế hoạch KHÔNG BẤM ĐƯỢC.
 *
 * Cloudflare Web Analytics: miễn phí, không cookie, không cần banner đồng ý.
 * Lưu ý trung thực — nó vẫn ghi IP và user-agent, theo GDPR đó vẫn là dữ liệu
 * cá nhân dù không có cookie; phải nêu trong trang riêng tư.
 *
 * Nó KHÔNG theo được phễu. Đủ cho "bao nhiêu người duy nhất", không đủ cho
 * "bao nhiêu người bấm sang tin gốc" — chỉ số đó phải chờ GĐ 1.
 *
 * Chưa có token thì không chèn gì cả: đặt NEXT_PUBLIC_CF_ANALYTICS_TOKEN.
 */
const CF_TOKEN = process.env.NEXT_PUBLIC_CF_ANALYTICS_TOKEN

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={`${sans.variable} ${mono.variable}`}>
      <body className="bg-bg font-sans text-text antialiased">
        <a
          href="#noi-dung"
          className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-30 focus:rounded-sm focus:border focus:border-field focus:bg-card focus:px-4 focus:py-2.5 focus:text-[14px]"
        >
          Bỏ qua điều hướng
        </a>

        <header className="sticky top-0 z-20 border-b border-line/70 bg-bg/80 backdrop-blur-xl">
          {/* Dưới sm: logo một hàng, nav thành dải cuộn ngang. Bốn mục cho
              gãy dòng tự do sẽ tạo bố cục lệch lạc ở màn hẹp. */}
          <nav
            aria-label="Chính"
            className="mx-auto flex max-w-5xl flex-col px-5 py-1.5 sm:flex-row sm:items-center sm:gap-x-1"
          >
            <Link
              href="/"
              className="flex shrink-0 items-center gap-2 py-3 text-[14px] font-semibold tracking-tight sm:mr-4"
            >
              <span
                aria-hidden
                className="size-[15px] rotate-45 rounded-[3px] bg-gradient-to-br from-open to-focus"
              />
              viecremote
            </Link>
            <span className="scroll-x -mx-1 flex pb-1 sm:mx-0 sm:pb-0">
              {NAV.map((n) => (
                <Link
                  key={n.href}
                  href={n.href}
                  /* px-2.5 py-3 + leading-5 = 44px chiều cao, đạt WCAG 2.5.8 */
                  className="shrink-0 whitespace-nowrap rounded-sm px-2.5 py-3 text-[13.5px] leading-5 text-text-2 transition-colors duration-150 hover:bg-card hover:text-text"
                >
                  {n.label}
                </Link>
              ))}
            </span>
          </nav>
        </header>

        <main id="noi-dung" className="mx-auto max-w-5xl px-5 py-10">
          {children}
        </main>

        <footer className="mx-auto max-w-5xl border-t border-line/70 px-5 py-9">
          <Subscribe />
          <p className="mt-8 text-[12.5px] leading-relaxed text-text-3">
            Không nhận hồ sơ. Mọi thông tin lấy từ tin gốc do công ty tự công bố.
            Nhãn có thể sai — xem{" "}
            <Link className="text-text-2 underline underline-offset-2 hover:text-text" href="/phuong-phap">
              phương pháp và giới hạn
            </Link>
            {" · "}
            <Link className="text-text-2 underline underline-offset-2 hover:text-text" href="/rieng-tu">
              dữ liệu và riêng tư
            </Link>
            .
          </p>
        </footer>

        {CF_TOKEN && (
          // `defer` chứ không `type="module"`: hai cách chạy như nhau cho beacon,
          // nhưng luật no-sync-scripts của Next không nhận ra module script vốn
          // đã hoãn, nên nó báo lỗi. Dùng defer thì khỏi phải tắt luật.
          <script
            defer
            src="https://static.cloudflareinsights.com/beacon.min.js"
            data-cf-beacon={JSON.stringify({ token: CF_TOKEN })}
          />
        )}
      </body>
    </html>
  )
}
