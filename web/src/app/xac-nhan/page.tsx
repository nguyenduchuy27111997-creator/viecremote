import Link from "next/link"
import { getCloudflareContext } from "@opennextjs/cloudflare"
import { Eyebrow, Lead, Note } from "@/components/Page"

export const metadata = { title: "Xác nhận đăng ký", robots: { index: false } }

/** Bước thứ hai của double opt-in. Chỉ sau bước này mới tính là đã đăng ký. */
export default async function Confirm({
  searchParams,
}: { searchParams: Promise<{ t?: string }> }) {
  const t = (await searchParams).t ?? ""
  let ok = false
  if (t) {
    const { env } = await getCloudflareContext({ async: true })
    const r = await env.DB
      .prepare("UPDATE subscriber SET confirmed = 1, confirmed_at = ? WHERE token = ? AND confirmed = 0")
      .bind(new Date().toISOString(), t)
      .run()
    ok = (r.meta?.changes ?? 0) > 0
    if (!ok) {
      const already = await env.DB
        .prepare("SELECT 1 FROM subscriber WHERE token = ? AND confirmed = 1")
        .bind(t)
        .first()
      ok = Boolean(already)
    }
  }

  return (
    <div className="glow rise">
      <Eyebrow>Đăng ký nhận tin</Eyebrow>
      <h1 className="mt-4 text-[clamp(28px,4.6vw,42px)]">
        {ok ? <>Đã <span className="grad">xác nhận</span></> : <>Đường dẫn không hợp lệ</>}
      </h1>
      <Lead>
        {ok
          ? "Bạn đã ở trong danh sách. Tôi sẽ báo khi mạng lưới mở, và gửi thư khi kho có thay đổi đáng kể. Không quảng cáo, không bán địa chỉ cho ai. Mỗi thư đều có đường huỷ một cú bấm."
          : "Đường dẫn xác nhận đã hết hạn hoặc không đúng. Thử đăng ký lại ở cuối trang chủ."}
      </Lead>
      <p className="mt-7">
        <Link
          href="/"
          className="rounded-sm border border-line bg-card px-4 py-2.5 text-[13.5px] transition-colors hover:border-field"
        >
          Về sổ đăng ký công ty
        </Link>
      </p>
      <Note>
        Xử lý dữ liệu cá nhân:{" "}
        <Link className="underline underline-offset-2 hover:text-text" href="/rieng-tu">
          trang riêng tư
        </Link>
        .
      </Note>
    </div>
  )
}
