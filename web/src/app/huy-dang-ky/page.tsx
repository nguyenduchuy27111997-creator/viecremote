import Link from "next/link"
import { getCloudflareContext } from "@opennextjs/cloudflare"
import { Eyebrow, Lead } from "@/components/Page"

export const metadata = { title: "Huỷ đăng ký", robots: { index: false } }

/**
 * Huỷ đăng ký = XOÁ HẲN bản ghi, không phải đánh dấu.
 * Giữ lại một danh sách "đã huỷ" vẫn là giữ dữ liệu cá nhân của người đã yêu
 * cầu ngừng xử lý.
 */
export default async function Unsubscribe({
  searchParams,
}: { searchParams: Promise<{ t?: string }> }) {
  const t = (await searchParams).t ?? ""
  let done = false
  if (t) {
    const { env } = await getCloudflareContext({ async: true })
    const r = await env.DB.prepare("DELETE FROM subscriber WHERE token = ?").bind(t).run()
    done = (r.meta?.changes ?? 0) > 0
  }

  return (
    <div className="glow rise">
      <Eyebrow>Đăng ký nhận tin</Eyebrow>
      <h1 className="mt-4 text-[clamp(28px,4.6vw,42px)]">
        {done ? <>Đã <span className="grad">xoá</span> địa chỉ của bạn</> : <>Không tìm thấy</>}
      </h1>
      <Lead>
        {done
          ? "Địa chỉ đã bị xoá hẳn khỏi cơ sở dữ liệu, không phải chỉ đánh dấu. Không còn gì để xoá thêm."
          : "Đường dẫn không đúng, hoặc địa chỉ đã được xoá trước đó."}
      </Lead>
      <p className="mt-7">
        <Link
          href="/"
          className="rounded-sm border border-line bg-card px-4 py-2.5 text-[13.5px] transition-colors hover:border-field"
        >
          Về trang chủ
        </Link>
      </p>
    </div>
  )
}
