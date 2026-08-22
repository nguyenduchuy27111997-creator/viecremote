import Link from "next/link"
import { meta } from "@/lib/db"
import { Eyebrow, Lead, Note } from "@/components/Page"

// Kho dựng lại mỗi ngày; ISR thường thay cho "use cache".
export const revalidate = 86400

export const metadata = {
  title: "API — dữ liệu địa lý tuyển dụng",
  description:
    "Truy vấn công ty nào tuyển được ở đâu, kèm trích dẫn từ tin gốc. JSON, con trỏ phân trang.",
}

/**
 * Trang này vừa là tài liệu vừa là trang bán hàng — nó chính là thứ mang đi khi
 * chạy A3 (hỏi nhà cung cấp EOR có trả tiền cho dữ liệu này không).
 *
 * Nên nó phải nói rõ CẢ giới hạn. Bán một tập dữ liệu 3.666 công ty như thể nó
 * là 123 triệu là cách nhanh nhất để mất khách ngay buổi thứ hai.
 */
export default async function ApiDocs() {
  const m = await meta()

  return (
    <>
      <div className="glow rise">
        <Eyebrow>Giao diện lập trình</Eyebrow>
        <h1 className="mt-4 max-w-[18ch] text-[clamp(30px,5vw,46px)]">
          Dữ liệu <span className="grad">địa lý tuyển dụng</span> theo công ty
        </h1>
        <Lead>
          Không phải &ldquo;công ty X đang tuyển&rdquo; — chuyện đó ai cũng bán. Đây là{" "}
          <b className="text-text">công ty X tuyển được ở đâu, và câu nào trong tin chứng minh</b>.
          Thuộc tính này không có trong bất kỳ nguồn dữ liệu tuyển dụng nào khác.
        </Lead>
      </div>

      <Sec title="Điểm cuối">
        <Code>{`GET /api/companies?verdict=ok&limit=100&cursor=<slug>`}</Code>
        <table className="mt-4 w-full border-collapse text-[13.5px]">
          <tbody>
            <P k="verdict" v="ok · unk · no — tuyển được ở VN / chưa đủ căn cứ / khoá" />
            <P k="mech" v="eor · contractor · entity · unknown" />
            <P k="limit" v="tối đa 50 khi ẩn danh, 500 khi có khoá" />
            <P k="cursor" v="slug cuối của trang trước; lấy từ next_cursor" />
          </tbody>
        </table>
      </Sec>

      <Sec title="Phản hồi">
        <Code>{`{
  "data": [{
    "slug": "canonical",
    "name": "canonical",
    "verdict": "ok",
    "verdict_label": "Tuyển toàn cầu",
    "jobs": { "total": 242, "global": 80, "vn": 19, "excluded": 133, "unknown": 10 },
    "mechanism": "unknown",
    "source": "greenhouse",
    "locked_countries": [{ "code": "EMEA", "jobs": 106 }, { "code": "US", "jobs": 53 }],
    "declared_countries": [],
    "exclusion_reasons": [{ "code": "DQ-02", "jobs": 121 }]
  }],
  "next_cursor": "canva",
  "tier": "anon",
  "limit_max": 50
}`}</Code>
        <p>
          Phân trang bằng <b className="text-text">con trỏ</b>, không phải offset: kho dựng lại
          mỗi ngày nên offset sẽ bỏ sót hoặc lặp bản ghi giữa hai lần gọi.
        </p>
      </Sec>

      <Sec title="Xác thực">
        <Code>{`curl -H "x-api-key: <khoá>" https://viecremote.com/api/companies`}</Code>
        <p>
          Hiện API <b className="text-text">mở, không cần khoá</b>, trần 50 bản ghi mỗi lượt.
          Khi có khách trả tiền đầu tiên, chế độ ẩn danh sẽ đóng lại và trần lên 500.
        </p>
        <p>
          Khoá lưu dưới dạng băm SHA-256 — cơ sở dữ liệu rò thì khoá vẫn không dùng được.
        </p>
      </Sec>

      <Sec title="Quy mô và giới hạn — đọc trước khi quyết">
        <table className="mt-1 w-full border-collapse text-[13.5px]">
          <tbody>
            <P k="Công ty" v={(+m.n_companies).toLocaleString("vi-VN")} />
            <P k="Tin đã chấm" v={(+m.n_jobs).toLocaleString("vi-VN")} />
            <P k="Công ty có dữ liệu nước bị khoá" v="2.324 (63%)" />
            <P k="Độ chính xác nhãn “mở”" v="97,5% · KTC 95%: 87–100%" />
            <P k="Cập nhật" v="hằng ngày" />
          </tbody>
        </table>
        <ul className="mt-4 space-y-2">
          <li>
            <b className="text-text">Chỉ ba nền tảng:</b> Greenhouse, Lever, Ashby. Không có
            Workday, Taleo, trang tự xây.
          </li>
          <li>
            <b className="text-text">Mẫu lệch về Mỹ và châu Âu</b> — slug thu từ chỉ mục web công khai.
          </li>
          <li>
            <b className="text-text">Cơ chế hợp đồng phủ rất mỏng:</b> chỉ 3% tin nêu ra. Đừng
            xây phễu dựa vào trường này.
          </li>
          <li>
            <b className="text-text">Không có lịch sử.</b> Đây là ảnh chụp hiện tại, chưa có
            chuỗi thời gian.
          </li>
        </ul>
      </Sec>

      <Sec title="Được phép làm gì">
        <p>
          Dữ liệu suy ra từ tin tuyển dụng công ty tự công bố — là dữ liệu{" "}
          <b className="text-text">về công ty</b>, không phải dữ liệu cá nhân. Không có tên,
          email hay hồ sơ của bất kỳ ai trong đó.
        </p>
        <p>
          Mỗi kết luận đều có trích dẫn nguyên văn tại <Code inline>/cong-ty/&#123;slug&#125;</Code>.
          Nếu bạn công bố lại số liệu, hãy dẫn về trang đó để người đọc kiểm được.
        </p>
      </Sec>

      <Note>
        Cần trần cao hơn, xuất theo lô, hay trường mà API chưa có? Đó đúng là câu tôi muốn nghe —
        gửi qua nút báo trên bất kỳ{" "}
        <Link className="underline underline-offset-2 hover:text-text" href="/?v=ok">
          trang công ty
        </Link>{" "}
        nào.
      </Note>
    </>
  )
}

function Sec({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-11 border-t border-line pt-7">
      <h2 className="text-[21px]">{title}</h2>
      <div className="mt-4 max-w-[72ch] space-y-3.5 text-[14.5px] leading-relaxed text-text-2">
        {children}
      </div>
    </section>
  )
}

function Code({ children, inline }: { children: React.ReactNode; inline?: boolean }) {
  if (inline)
    return (
      <code className="rounded-xs border border-line bg-card px-1.5 py-0.5 font-mono text-[12.5px] text-text">
        {children}
      </code>
    )
  return (
    <pre className="scroll-x rounded-md border border-line bg-card p-4 font-mono text-[12.5px] leading-relaxed text-text">
      {children}
    </pre>
  )
}

function P({ k, v }: { k: string; v: string }) {
  return (
    <tr className="border-b border-line-2 last:border-0">
      <th className="w-64 py-2.5 pr-4 text-left align-top font-mono text-[12px] font-normal text-text">
        {k}
      </th>
      <td className="py-2.5 text-text-2">{v}</td>
    </tr>
  )
}
