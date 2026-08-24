import Link from "next/link"
import { all } from "@/lib/db"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"

export const revalidate = 86400

export const metadata = {
  title: "Công ty vừa mở hay vừa đóng với Việt Nam",
  description:
    "Nhật ký đổi nhãn: mỗi dòng là một công ty đổi vị trí công bố về việc tuyển ở Việt Nam, "
    + "ghi đúng ngày bản dựng bắt được. Không kho dữ liệu nào khác theo dõi điều này.",
}

type Change = {
  slug: string
  name: string | null
  from_v: string
  to_v: string
  changed_at: string
}

const LABEL: Record<string, string> = {
  ok: "tuyển được ở VN",
  no: "không tuyển ở VN",
  unk: "chưa xác định",
}

/**
 * Bản tiếng Việt của /hiring-in-sea/changes — CÙNG dữ liệu, người đọc khác.
 *
 * Với kỹ sư, "công ty vừa mở cho VN" là tín hiệu hành động mạnh nhất cả kho
 * có: một cửa vừa mở và chưa ai chen. Ngược lại "vừa đóng" tiết kiệm cho họ
 * một lá đơn vô ích. Sứ mệnh là kỹ sư Việt — dữ liệu độc quyền nhất phải phục
 * vụ họ trước, không phải chỉ nằm bên trang bán hàng tiếng Anh.
 *
 * Link công ty trỏ về /cong-ty (bản tiếng Việt, có trích dẫn mệnh đề) chứ
 * không phải /company (bản cho nhà tuyển dụng).
 */
export default async function ThayDoi() {
  const rows = await all<Change>(
    `SELECT v.slug, c.name, v.from_v, v.to_v, v.changed_at
     FROM verdict_change v LEFT JOIN company c ON c.slug = v.slug
     ORDER BY v.changed_at DESC, v.slug LIMIT 300`,
  )

  const opened = rows.filter((r) => r.to_v === "ok")
  const closed = rows.filter((r) => r.from_v === "ok")
  const shifted = rows.filter((r) => r.to_v !== "ok" && r.from_v !== "ok")

  const day = (iso: string) => iso.slice(0, 10)
  const Row = ({ r }: { r: Change }) => (
    <tr className="border-b border-line last:border-0">
      <td className="whitespace-nowrap px-4 py-2.5 font-mono text-[11.5px] text-text-3">
        {day(r.changed_at)}
      </td>
      <td className="px-4 py-2.5">
        <Link className="hover:underline" href={`/cong-ty/${r.slug}`}>
          {r.name ?? r.slug}
        </Link>
      </td>
      <td className="px-4 py-2.5 text-[12.5px] text-text-3">
        {LABEL[r.from_v] ?? r.from_v} → <b className="text-text-2">{LABEL[r.to_v] ?? r.to_v}</b>
      </td>
    </tr>
  )
  const Table = ({ items }: { items: Change[] }) => (
    <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
      <table className="w-full border-collapse text-[13.5px]">
        <tbody>{items.map((r) => <Row key={r.slug + r.changed_at} r={r} />)}</tbody>
      </table>
    </div>
  )

  return (
    <>
      <div className="glow rise">
        <Eyebrow>Nhật ký đổi nhãn · cập nhật mỗi ngày</Eyebrow>
        <h1 className="mt-4 max-w-[18ch] text-[clamp(28px,4.8vw,44px)]">
          Công ty vừa <span className="grad">mở hay đóng</span> với Việt Nam
        </h1>
        <Lead>
          Kho dựng lại mỗi ngày và ghi đè chính nó — trang này là thứ duy nhất nhớ hôm qua.
          Mỗi dòng là một công ty đổi vị trí <b className="text-text">công bố</b> về việc tuyển
          ở Việt Nam, ghi đúng ngày bản dựng bắt được.
        </Lead>
      </div>

      {rows.length === 0 ? (
        <Section title="Chưa có gì — và đó là trạng thái trung thực">
          <p className="mt-4 max-w-[64ch] text-[14px] leading-relaxed text-text-2">
            Theo dõi bắt đầu ngày <b className="text-text">24/08/2026</b>. Nhãn đổi khi công ty
            sửa tin của họ, nên dòng xuất hiện đúng ngày điều đó xảy ra — thường vài dòng mỗi
            tuần trên 3.630 công ty. Trong lúc chờ,{" "}
            <Link className="underline underline-offset-2 hover:text-text" href="/tin-mo">
              danh sách tin đang mở
            </Link>{" "}
            là chỗ đáng xem hơn.
          </p>
          <Note>
            Một nhật ký rỗng vài ngày sau khi ra mắt là hình dạng của nhật ký trung thực. Feed
            đã đầy sẵn nghĩa là ngày tháng được bịa ra.
          </Note>
        </Section>
      ) : (
        <>
          {opened.length > 0 && (
            <Section
              title={`Vừa mở cho Việt Nam (${opened.length})`}
              hint="Tín hiệu hành động mạnh nhất cả kho có: một cửa vừa mở và chưa ai chen."
            >
              <Table items={opened} />
            </Section>
          )}
          {closed.length > 0 && (
            <Section
              title={`Vừa đóng với Việt Nam (${closed.length})`}
              hint="Tiết kiệm cho bạn một lá đơn: vị trí từng mở giờ không còn."
            >
              <Table items={closed} />
            </Section>
          )}
          {shifted.length > 0 && (
            <Section
              title={`Dịch giữa khoá và chưa rõ (${shifted.length})`}
              hint="Chuyển giữa mệnh đề loại trừ tường minh và không có mệnh đề nào — tín hiệu
                    yếu hơn, giữ cho đủ."
            >
              <Table items={shifted} />
            </Section>
          )}
          <Note>
            Nhãn đọc từ tin công bố. Một dòng ở đây nghĩa là vị trí <i>công bố</i> đổi — chính
            sách thật có thể đã đổi sớm hơn mà không tin nào nói ra.
          </Note>
        </>
      )}
    </>
  )
}
