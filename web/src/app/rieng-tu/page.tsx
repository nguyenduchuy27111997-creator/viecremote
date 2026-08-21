import Link from "next/link"
import { Eyebrow, Lead, Note } from "@/components/Page"

export const metadata = {
  title: "Dữ liệu và riêng tư",
  description: "Trang này thu gì, không thu gì, và vì sao.",
}

/**
 * Bắt buộc từ lúc bật analytics và thu email — cả hai đều chạm dữ liệu cá nhân
 * theo Luật 91/2025. Viết bằng tiếng người, không phải điều khoản mẫu.
 */
export default function Privacy() {
  return (
    <>
      <div className="glow rise">
        <Eyebrow>Luật 91/2025 · Nghị định 356/2025</Eyebrow>
        <h1 className="mt-4 max-w-[16ch] text-[clamp(30px,5vw,46px)]">
          Dữ liệu và <span className="grad">riêng tư</span>
        </h1>
        <Lead>
          Trang này gần như không thu gì. Dưới đây là toàn bộ danh sách, không có phần &ldquo;và
          các mục đích khác&rdquo;.
        </Lead>
      </div>

      <Sec title="Không thu">
        <ul className="space-y-2">
          <li>Không tài khoản, không đăng nhập, không mật khẩu.</li>
          <li>Không CV, không hồ sơ ứng viên. Trang này <b className="text-text">không nhận hồ sơ</b>.</li>
          <li>Không cookie theo dõi, không quảng cáo, không mã của bên thứ ba nào ngoài mục dưới.</li>
          <li>
            <b className="text-text">Không bán dữ liệu cá nhân cho ai.</b> Luật 91/2025 cấm mua
            bán dữ liệu cá nhân, và mô hình kinh doanh của trang này cũng không cần tới nó.
          </li>
        </ul>
      </Sec>

      <Sec title="Có thu — ba thứ">
        <dl className="space-y-5">
          <Item k="Thống kê truy cập">
            Cloudflare Web Analytics: <b className="text-text">không cookie</b>, không định danh
            cá nhân, không theo bạn qua các trang khác. Nó vẫn thấy địa chỉ IP và chuỗi trình
            duyệt trong lúc xử lý — theo chuẩn chặt thì đó vẫn là dữ liệu cá nhân, nên nói rõ ở
            đây. Dùng đúng một việc: đếm bao nhiêu người dùng trang.
          </Item>
          <Item k="Báo nhãn sai">
            Lưu: loại lỗi, ghi chú bạn gõ, thời điểm, và mã tin/công ty.{" "}
            <b className="text-text">Không lưu email, không lưu IP.</b> Không có cách nào để nối
            báo cáo đó về bạn — kể cả tôi.
          </Item>
          <Item k="Đăng ký nhận tin">
            Chỉ khi bạn tự nhập. Lưu: địa chỉ email và một mã ngẫu nhiên. Cần{" "}
            <b className="text-text">xác nhận qua thư</b> mới tính là đăng ký. Huỷ đăng ký là{" "}
            <b className="text-text">xoá hẳn bản ghi</b>, không phải đánh dấu.
          </Item>
        </dl>
      </Sec>

      <Sec title="Dữ liệu về công ty thì khác">
        <p>
          Phần lớn nội dung trang này — địa lý tuyển dụng, mệnh đề giới hạn, trích dẫn — là dữ
          liệu <b className="text-text">về công ty</b>, suy từ tin tuyển dụng công ty tự công bố.
          Đó không phải dữ liệu cá nhân và không thuộc phạm vi mục trên.
        </p>
        <p>
          Trang không tự nhận là nguồn gốc của tin. Mọi tin đều dẫn về trang tuyển dụng gốc, và
          trích đoạn mô tả bị chặn cứng ở 300 ký tự.
        </p>
      </Sec>

      <Sec title="Muốn xoá dữ liệu của mình">
        <p>
          Email: bấm đường huỷ trong bất kỳ thư nào — xoá ngay, không hỏi lại. Mất đường dẫn thì
          đăng ký lại rồi bấm huỷ trong thư xác nhận.
        </p>
        <p>
          Báo nhãn sai: không có gì để xoá vì không có gì nối về bạn.
        </p>
      </Sec>

      <Note>
        Cập nhật 22/08/2026. Đây là mô tả thực tế hệ thống đang làm, không phải điều khoản mẫu —
        nếu hành vi đổi thì trang này đổi trước.{" "}
        <Link className="underline underline-offset-2 hover:text-text" href="/phuong-phap">
          Phương pháp và giới hạn
        </Link>
        .
      </Note>
    </>
  )
}

function Sec({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mt-11 border-t border-line pt-7">
      <h2 className="text-[21px]">{title}</h2>
      <div className="mt-4 max-w-[66ch] space-y-3.5 text-[14.5px] leading-relaxed text-text-2">
        {children}
      </div>
    </section>
  )
}

function Item({ k, children }: { k: string; children: React.ReactNode }) {
  return (
    <div>
      <dt className="font-mono text-[11px] uppercase tracking-wider text-text-3">{k}</dt>
      <dd className="mt-1.5">{children}</dd>
    </div>
  )
}
