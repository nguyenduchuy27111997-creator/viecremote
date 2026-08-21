import Link from "next/link"
import { cacheLife } from "next/cache"
import { all, meta } from "@/lib/db"
import { Eyebrow, Lead, Note } from "@/components/Page"

export const metadata = {
  title: "Vậy tôi nên làm gì",
  description:
    "86% tin remote khoá theo địa lý. Đây là điều dữ liệu nói bạn nên làm khác đi — và điều nó không nói được.",
}

/**
 * Lỗ hổng sản phẩm lớn nhất trước trang này: kho nói 97% công ty đóng, rồi
 * KHÔNG có bước tiếp theo nào.
 *
 * Đây không phải mồi giữ chân — sứ mệnh nói người dùng NÊN rời đi sau khi có
 * câu trả lời. Đây là phần hoàn tất câu trả lời. Mọi khẳng định trên trang này
 * phải truy được về một con số trong kho; chỗ nào không có số thì nói thẳng là
 * không có số.
 */
export default async function WhatToDo() {
  "use cache"
  cacheLife("days")
  const m = await meta()
  const mech = await all<{ mechanism: string; n: number }>(
    "SELECT mechanism, count(*) n FROM company WHERE verdict='ok' GROUP BY mechanism",
  )
  const known = mech.filter((r) => r.mechanism !== "unknown").reduce((a, r) => a + r.n, 0)
  const ok = +m.n_comp_ok

  return (
    <>
      <div className="glow rise">
        <Eyebrow>Đọc sau khi đã tra</Eyebrow>
        <h1 className="mt-4 max-w-[17ch] text-[clamp(30px,5vw,48px)]">
          Vậy tôi nên <span className="grad">làm gì</span>
        </h1>
        <Lead>
          Trang này không hứa giúp bạn được tuyển. Nó nói điều dữ liệu{" "}
          <b className="text-text">thật sự</b> cho phép kết luận — và chỗ nào nó im lặng.
        </Lead>
      </div>

      <Block n="01" title="Đừng rải đơn vào tin remote công khai">
        <p>
          Trong <Num>{(+m.n_jobs).toLocaleString("vi-VN")}</Num> tin đã chấm, chỉ{" "}
          <Num>{m.n_job_global}</Num> tin mở toàn cầu và <Num>{m.n_job_vn}</Num> tin mở cho vùng
          hoặc nước có Việt Nam. Cộng lại chưa tới <b className="text-text">1,2%</b>.
        </p>
        <p>
          Đây không phải chuyện bạn giỏi hay kém. Kênh tin đăng công khai{" "}
          <b className="text-text">về mặt cấu trúc</b> không dành cho người ở Việt Nam. Rải 100
          đơn vào đó, kỳ vọng thống kê là hơn 98 đơn rơi vào tin có mệnh đề chặn bạn từ trước
          khi ai đó đọc CV.
        </p>
        <p>
          Việt Nam có khoảng 530.000 lập trình viên và đứng top 6 thế giới về gia công phần mềm.
          Việc tuyển kỹ sư Việt <b className="text-text">có thật</b> — nó đi qua công ty gia
          công, EOR, hợp đồng nhà thầu, giới thiệu nội bộ. Không đi qua tin đăng.
        </p>
      </Block>

      <Block n="02" title="Nhắm công ty, đừng nhắm tin">
        <p>
          Địa lý tuyển dụng là thuộc tính của <b className="text-text">công ty</b>, không phải
          của từng tin. Một công ty đã dựng được cách trả lương cho người ở Việt Nam thì làm
          được cho mọi vị trí; công ty chưa dựng thì không vị trí nào cứu được.
        </p>
        <p>
          Nên danh sách đáng theo dõi là <Num>{ok}</Num> công ty, không phải{" "}
          <Num>{m.n_job_global}</Num> tin. Tin đổi hằng ngày; công ty đổi hằng quý.
        </p>
        <p>
          <Link className="underline underline-offset-2 hover:text-text" href="/?v=ok">
            Xem {ok} công ty đó →
          </Link>
        </p>
      </Block>

      <Block n="03" title="Hỏi cơ chế trả lương TRƯỚC khi bỏ công">
        <p>
          Một công ty ở Mỹ không thể trả lương cho bạn như trả cho nhân viên Mỹ. Phải qua một
          trong ba cách: <b className="text-text">EOR</b> (thuê qua bên thứ ba như Deel, Remote,
          Oyster), <b className="text-text">hợp đồng nhà thầu</b> (bạn tự xuất hoá đơn, tự lo
          thuế), hoặc <b className="text-text">pháp nhân tại Việt Nam</b> (công ty có văn phòng ở
          đây).
        </p>
        <p>
          Ba cách đó khác nhau rất xa về thuế, bảo hiểm, và mức bạn nên đòi. Nhưng trong{" "}
          <Num>{ok}</Num> công ty tuyển được ở Việt Nam, chỉ <Num>{known}</Num> công ty nói ra
          mình dùng cách nào.
        </p>
        <p className="rounded-md border border-unk/35 bg-unk-bg px-4 py-3 text-unk">
          Hơn <b>90%</b> công ty mở <b>không cho bạn biết bạn sẽ được trả lương bằng cách nào.</b>{" "}
          Đó là câu hỏi đầu tiên nên hỏi trong buổi phỏng vấn đầu tiên — trước khi bàn lương.
        </p>
      </Block>

      <Block n="04" title="Đọc kỹ ba loại mệnh đề dễ bỏ sót">
        <ul className="space-y-2.5">
          <li>
            <b className="text-text">&ldquo;Remote&rdquo; mà thật ra là hybrid.</b>{" "}
            <Num>5.466</Num> tin gắn nhãn remote nhưng bên trong yêu cầu có mặt tại văn phòng.
            Đây là loại lãng phí thời gian trắng trợn nhất trong kho.
          </li>
          <li>
            <b className="text-text">Hình thức lao động chỉ tồn tại ở một nước.</b> Tin đòi
            W-2 (Mỹ) hay PAYE (Anh) là đã loại bạn, dù không câu nào nhắc tới quốc gia.{" "}
            <Num>793</Num> tin thuộc loại này.
          </li>
          <li>
            <b className="text-text">Yêu cầu múi giờ.</b> <Num>375</Num> tin. Nhưng cẩn thận
            chiều ngược lại: <i>&ldquo;làm giờ EST&rdquo;</i> là yêu cầu <b>ca làm</b>, không
            phải yêu cầu <b>nơi ở</b>. Người ở Việt Nam làm 20:30–05:30 giờ Việt vẫn đáp ứng
            được. Đừng tự loại mình.
          </li>
        </ul>
      </Block>

      <Block n="05" title="Điều trang này KHÔNG nói được">
        <ul className="space-y-2.5">
          <li>
            <b className="text-text">Công ty có thật sự nhận bạn không.</b> Kho chỉ đọc được
            điều công ty <i>viết ra</i>. Không có mệnh đề chặn không đồng nghĩa với sẽ nhận.
          </li>
          <li>
            <b className="text-text">Mức lương bạn nên đòi.</b> Chỉ 51/{ok} công ty mở có tin
            công bố lương.
          </li>
          <li>
            <b className="text-text">Các kênh không đăng tin.</b> Công ty gia công, agency,
            giới thiệu — chỗ việc tuyển kỹ sư Việt thật sự diễn ra — đều nằm ngoài kho này.
          </li>
          <li>
            <b className="text-text">Công ty dùng nền tảng khác.</b> Kho chỉ có Greenhouse,
            Lever, Ashby. Workday, Taleo, trang tự xây đều không có.
          </li>
        </ul>
        <p>
          Độ chính xác nhãn &ldquo;mở&rdquo; là <b className="text-text">97,5%</b> — cứ 40 tin
          thì khoảng 1 tin sai. Cách đo và toàn bộ giới hạn:{" "}
          <Link className="underline underline-offset-2 hover:text-text" href="/phuong-phap">
            trang phương pháp
          </Link>
          .
        </p>
      </Block>

      <Note>
        Thấy nhãn sai ở đâu thì báo — có nút trên mọi trang công ty và trang tin. Trang này chỉ
        có giá trị đúng bằng độ chính xác của nó.
      </Note>
    </>
  )
}

function Num({ children }: { children: React.ReactNode }) {
  return <b className="font-mono tabular-nums text-text">{children}</b>
}

function Block({ n, title, children }: {
  n: string
  title: string
  children: React.ReactNode
}) {
  return (
    <section className="mt-11 border-t border-line pt-7">
      <p className="font-mono text-[11px] tracking-[0.16em] text-text-3">{n}</p>
      <h2 className="mt-2.5 max-w-[24ch] text-[22px]">{title}</h2>
      <div className="mt-4 max-w-[66ch] space-y-3.5 text-[14.5px] leading-relaxed text-text-2">
        {children}
      </div>
    </section>
  )
}
