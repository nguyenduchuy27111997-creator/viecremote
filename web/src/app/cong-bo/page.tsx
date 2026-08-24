import Link from "next/link"
import { all, one } from "@/lib/db"
import { REASON } from "@/lib/labels"
import { cname } from "@/lib/countries"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"

export const revalidate = 86400

export const metadata = {
  title: "Tôi chấm 34 nghìn tin remote. 0 tin ghi rõ tuyển được ở Việt Nam",
  description:
    "Bài công bố: cách kho được dựng, ba con số chính, rào cản là gì, và vì sao "
    + "kênh tin đăng công khai về mặt cấu trúc không dành cho kỹ sư Việt.",
}

/**
 * BÀI CÔNG BỐ — bản chính tắc, sống trên chính site.
 *
 * Vì sao là trang chứ không phải bản dán từ content/bai-cong-bo.md: kho đổi
 * mỗi ngày, và bài học đắt nhất của dự án là số tĩnh lỗi thời chỉ sau MỘT chu
 * kỳ (110 → 103 → 91). Trang này kéo số từ D1 như mọi trang khác nên KHÔNG
 * THỂ lỗi thời — mọi bản đăng mạng xã hội trỏ về đây, và người đọc mở ra luôn
 * thấy số khớp với trang tra cứu.
 *
 * Các dữ kiện TĨNH (0/150 chấm tay, chuỗi đo 70% → 97,5%, 530k lập trình
 * viên) là sự kiện lịch sử, không trôi theo kho — để nguyên chữ.
 */
export default async function CongBo() {
  const c = await one<{ total: number; jobs: number; open: number; closed: number }>(
    `SELECT (SELECT count(*) FROM company) total, (SELECT count(*) FROM job) jobs,
            (SELECT count(*) FROM company WHERE verdict='ok') open,
            (SELECT count(*) FROM company WHERE verdict='no') closed`,
  )
  const el = await all<{ eligibility: string; n: number }>(
    "SELECT eligibility, count(*) n FROM job GROUP BY eligibility",
  )
  const reasons = await all<{ reason: string; n: number }>(
    `SELECT reason, count(*) n FROM job
     WHERE eligibility='excluded' AND reason IS NOT NULL
     GROUP BY reason ORDER BY n DESC`,
  )
  const locks = await all<{ code: string; n: number }>(
    "SELECT code, sum(n_jobs) n FROM locked GROUP BY code ORDER BY n DESC LIMIT 5",
  )
  // "glob" là TOÁN TỬ của SQLite — dùng làm alias là lỗi cú pháp ngay chữ đầu.
  const ww = await one<{ n_glob: number; n_vn: number }>(
    `SELECT sum(scope='worldwide') n_glob, sum(scope='vn') n_vn
     FROM job WHERE eligibility='worldwide'`,
  )

  const jobs = c?.jobs ?? 0
  const of = (k: string) => el.find((e) => e.eligibility === k)?.n ?? 0
  const num = (n: number) => n.toLocaleString("vi-VN")
  const pct = (n: number) => `${((100 * n) / jobs).toFixed(1).replace(".", ",")}%`
  const openJobs = of("worldwide")

  return (
    <article>
      <p className="font-mono text-[11.5px] text-text-3">
        <Link className="underline underline-offset-2 hover:text-text-2" href="/research" lang="en">
          English version →
        </Link>
      </p>

      <div className="glow rise mt-4">
        <Eyebrow>Bài công bố · số liệu cập nhật mỗi ngày</Eyebrow>
        <h1 className="mt-4 max-w-[22ch] text-[clamp(28px,4.8vw,44px)]">
          Tôi chấm {num(jobs)} tin remote. Có <span className="grad">0 tin</span> ghi rõ tuyển
          được người ở Việt Nam
        </h1>
        <Lead>
          Tôi hay thấy câu này trong các nhóm dev: <i>&ldquo;remote thì làm ở đâu chẳng
          được.&rdquo;</i> Tôi muốn biết nó đúng bao nhiêu phần — nên kéo toàn bộ tin remote từ
          ba nền tảng công khai (Greenhouse, Lever, Ashby) rồi đọc từng tin bằng máy, tìm một
          thứ duy nhất: <b className="text-text">có câu nào chặn người đang sống ở Việt Nam
          không.</b>
        </Lead>
      </div>

      <Section title="Ba con số">
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <tbody>
              {([
                ["Bị giới hạn địa lý", of("excluded"), "text-closed"],
                ["Chưa đủ căn cứ kết luận", of("unknown"), "text-unk"],
                ["Không vướng giới hạn nào", openJobs, "text-open"],
              ] as const).map(([label, n, tone]) => (
                <tr key={label} className="border-b border-line last:border-0">
                  <td className="px-4 py-3">{label}</td>
                  <td className={`px-4 py-3 text-right font-mono tabular-nums ${tone}`}>{num(n)}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-3">{pct(n)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          Trong {num(openJobs)} tin mở: {num(ww?.n_glob ?? 0)} tin mở toàn cầu, {num(ww?.n_vn ?? 0)}{" "}
          tin mở cho một vùng hoặc nước có Việt Nam. Tính theo <b className="text-text-2">công
          ty</b> thì rõ hơn: trong {num(c?.total ?? 0)} công ty,{" "}
          <b className="text-open">{num(c?.open ?? 0)} công ty tuyển được người ở Việt Nam</b> —
          còn <b className="text-closed">{num(c?.closed ?? 0)} công ty khoá hoàn toàn</b>, không
          một vị trí nào.
          <br />
          <br />
          Và con số làm tôi dừng lại lâu nhất: tôi chấm tay 150 tin ngẫu nhiên, đọc từ đầu đến
          cuối. <b className="text-text-2">Không một tin nào ghi rõ tuyển được người ở Việt
          Nam.</b> Không phải &ldquo;ít&rdquo;. Là 0.
        </Note>
      </Section>

      <Section
        title="Rào cản là gì"
        hint="Không phải cảm tính. Là những mệnh đề rất cụ thể, viết sẵn trong tin."
      >
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <tbody>
              {reasons.filter((r) => r.n > 100).map((r) => (
                <tr key={r.reason} className="border-b border-line last:border-0">
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-2">{num(r.n)}</td>
                  <td className="px-4 py-3">{REASON[r.reason] ?? r.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          Nước bị khoá vào nhiều nhất:{" "}
          {locks.map((l, i) => (
            <span key={l.code}>
              {i > 0 && " · "}
              <b className="text-text-2">{cname(l.code)} {num(l.n)}</b>
            </span>
          ))}
          . Riêng nhóm tin gắn nhãn remote nhưng bên trong bắt lên văn phòng là loại lãng phí
          thời gian trắng trợn nhất — nhãn nói một đằng, mệnh đề trong tin nói một nẻo.
        </Note>
      </Section>

      <Section title="Điều nghịch lý — và là phần quan trọng nhất">
        <div className="mt-4 max-w-[64ch] space-y-4 text-[14.5px] leading-relaxed text-text-2">
          <p>
            Việt Nam có khoảng <b className="text-text">530.000 lập trình viên</b>, mỗi năm thêm
            50.000–60.000 cử nhân IT, và đứng <b className="text-text">top 6 thế giới</b> về gia
            công phần mềm. Vậy mà 0/150 tin ghi rõ tuyển được ở đây.
          </p>
          <p>
            Hai điều này <b className="text-text">không mâu thuẫn</b>. Chúng nói một điều khác
            hẳn: <b className="text-text">việc tuyển kỹ sư Việt có thật — nhưng nó không đi qua
            tin đăng công khai.</b> Nó đi qua công ty gia công, qua EOR, qua hợp đồng nhà thầu,
            qua giới thiệu nội bộ.
          </p>
          <p>
            Nghĩa là: nếu chiến lược tìm việc của bạn là <i>rải đơn vào các tin remote trên
            LinkedIn</i>, bạn đang câu ở khúc sông gần như không có cá. Không phải vì bạn kém.
            Vì kênh đó <b className="text-text">về mặt cấu trúc</b> không dành cho bạn.
          </p>
        </div>
      </Section>

      <Section title="Nên tôi làm trang này" hint="Không phải job board. Không nhận hồ sơ. Không đăng tin.">
        <ul className="mt-4 max-w-[64ch] space-y-2.5 text-[14px] leading-relaxed text-text-2">
          <li>
            <Link className="underline underline-offset-2 hover:text-text" href="/?v=ok">
              {num(c?.open ?? 0)} công ty tuyển được người ở Việt Nam
            </Link>{" "}
            — kèm số vị trí đang mở
          </li>
          <li>
            <Link className="underline underline-offset-2 hover:text-text" href="/khoa">
              Hồ sơ từng công ty
            </Link>{" "}
            — họ khoá tuyển vào những nước nào, đếm theo số tin
          </li>
          <li>
            <Link className="underline underline-offset-2 hover:text-text" href="/vi-sao-bi-loai">
              {num(of("excluded"))} tin bị loại, kèm lý do trích dẫn được
            </Link>{" "}
            — để bạn biết <i>đừng</i> mất thời gian vào đâu
          </li>
          <li>
            <Link className="underline underline-offset-2 hover:text-text" href="/thay-doi">
              Nhật ký đổi nhãn
            </Link>{" "}
            — công ty vừa mở hay vừa đóng với Việt Nam. Kho dựng lại mỗi ngày và ghi đè chính
            nó; trang đó là thứ duy nhất nhớ hôm qua
          </li>
        </ul>
        <Note>
          Mỗi kết luận đều kèm <b className="text-text-2">trích dẫn nguyên văn</b> từ tin gốc.
          Không có &ldquo;theo thuật toán của chúng tôi&rdquo;. Bạn đọc được đúng câu mà máy đã
          đọc.
        </Note>
      </Section>

      <Section title="Giới hạn — nói thẳng" hint="Tôi không muốn bạn tin trang này hơn mức nó xứng đáng.">
        <ul className="mt-4 max-w-[64ch] space-y-2.5 text-[13.5px] leading-relaxed text-text-2">
          <li>
            <b className="text-text">Chỉ ba nền tảng.</b> Greenhouse, Lever, Ashby. Công ty dùng
            Workday, Taleo, hay trang tự xây thì không có ở đây.
          </li>
          <li>
            <b className="text-text">Thiên về công ty Mỹ và châu Âu.</b> Slug thu từ chỉ mục web
            công khai, nên mẫu lệch.
          </li>
          <li>
            <b className="text-text">Độ chính xác đo được: 97,5%</b> — rút 40 tin từ nhóm đã gán
            &ldquo;mở&rdquo;, người chấm mù đọc lại tin gốc rồi so. Nghĩa là cứ 40 tin gắn nhãn
            &ldquo;mở&rdquo; thì khoảng 1 tin sai.
          </li>
          <li>
            Điều đáng nói nhất về con số đó: <b className="text-text">lần đo trung thực đầu tiên
            cho 70%</b>. Hai lần đo trước cho 85% và 90%, nhưng lấy mẫu ngẫu nhiên — mà nhóm
            &ldquo;mở&rdquo; chỉ chiếm hơn 1% kho nên mẫu ngẫu nhiên gần như không chạm tới nó.
            Hai con số đẹp kia không sai; chúng <b className="text-text">đo nhầm thứ</b>. Toàn bộ
            năm đợt đo và mười lỗi đã sửa nằm ở{" "}
            <Link className="underline underline-offset-2 hover:text-text" href="/phuong-phap">
              trang Phương pháp
            </Link>
            .
          </li>
        </ul>
        <Note>
          Thấy nhãn sai? Báo cho tôi ngay trên trang công ty. Trang này chỉ có giá trị đúng bằng
          độ chính xác của nó — một danh sách &ldquo;đủ điều kiện&rdquo; mà sai thì tệ hơn là
          không có gì. Miễn phí, không cần tài khoản, không quảng cáo, không bán dữ liệu của ai.
        </Note>
      </Section>
    </article>
  )
}
