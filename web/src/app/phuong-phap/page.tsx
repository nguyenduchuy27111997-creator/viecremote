import { cacheLife } from "next/cache"
import { meta } from "@/lib/db"
import { Eyebrow, KV, KVTable, Lead, PageTitle, Section } from "@/components/Page"

export const metadata = { title: "Phương pháp" }

const AUDIT = [
  ["Đợt 1 — 40 tin ngẫu nhiên", "bắt đúng tin bị loại 88,6% · tổng thể 85,0%"],
  ["Đợt 2 — 30 tin mới", "bắt đúng tin bị loại 100% · tổng thể 90,0%"],
  ["Đợt 3 — 40 tin phân tầng từ nhóm “mở”", "độ chính xác 70,0%"],
  ["Đợt 4 — 40 tin phân tầng, sau khi sửa", "độ chính xác 90,0%"],
  ["Đợt 5 — 40 tin phân tầng hoàn toàn khác", "độ chính xác 97,5%"],
  ["Đối chứng cố định 180 tin", "bắt đúng tin bị loại 100% · tổng thể 100%"],
]

const FIXES = [
  "“SEA” trong danh sách thành phố Mỹ là Seattle, bị đọc thành Southeast Asia.",
  "“Anywhere USA”, “Remote (anywhere in the U.S.)” — mệnh đề thu hẹp ngay sau “anywhere” bị bỏ qua.",
  "“Anywhere; Europe” là thẻ địa điểm, không phải hai lựa chọn ngang hàng.",
  "“Remote, Australia, APAC” — Greenhouse ghi phân cấp kiểu làm việc, nước, vùng cha.",
  "Nhãn địa điểm “Global” nhưng thân tin liệt kê đóng 15 nước, không có Việt Nam.",
  "Chip “Home based - Worldwide” dùng lại cho mọi tin, trong khi thân tin ghi Location: EMEA.",
  "Câu trong mục phúc lợi nói “work from anywhere” là đãi ngộ, không phải phạm vi tuyển.",
  "Múi giờ ngoài Mỹ (CET, EET, BST) và dạng viết đủ chữ chưa nằm trong bộ luật.",
  "Tin ghi rõ (On-site) vẫn lọt bộ lọc remote vì mô tả có nhắc “remote”.",
  "Cửa sổ trích dẫn cắt cứng 180 ký tự làm mất chính từ khoá đã khớp.",
]

export default async function Method() {
  "use cache"
  cacheLife("days")
  const m = await meta()
  const tot = +m.n_jobs
  const pct = (n: number) => `${((100 * n) / tot).toFixed(1)}%`

  return (
    <>
      <div className="glow rise">
      <Eyebrow>Độ chính xác là sản phẩm</Eyebrow>
      <h1 className="mt-4 text-[clamp(30px,5vw,48px)]">
        <span className="grad">Phương pháp</span>
      </h1>
      <Lead>Thứ duy nhất trang này bán là sự thật. Nên phương pháp phải kiểm tra được.</Lead>
      </div>

      <h2 className="mt-10 text-[21px]">Cách chấm</h2>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        Mỗi tin đi qua ba tầng: <b>trường địa điểm</b> có cấu trúc, rồi <b>quy tắc loại trừ</b> trên
        tiêu đề và mô tả, rồi <b>quy tắc bằng chứng dương</b> — chỉ tính khi nằm trong câu nói về
        điều kiện tuyển dụng, không tính khi nằm trong mục phúc lợi.
      </p>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        <b>Mọi nhãn phải kèm trích dẫn nguyên văn.</b> Không trích được thì ghi “Chưa xác định” —
        không đoán.
      </p>

      <h2 className="mt-10 text-[21px]">Số liệu hiện tại</h2>
      <KVTable>
          <KV k="Công ty có hồ sơ">{(+m.n_companies).toLocaleString("vi-VN")}</KV>
          <KV k="Công ty tuyển được ở Việt Nam">
            {m.n_comp_ok} ({((100 * +m.n_comp_ok) / +m.n_companies).toFixed(1)}%)
          </KV>
          <KV k="Tin đã chấm">{tot.toLocaleString("vi-VN")}</KV>
          <KV k="Mở toàn cầu">{`${m.n_job_global} (${pct(+m.n_job_global)})`}</KV>
          <KV k="Mở cho Việt Nam (vùng hoặc nước có VN)">{`${m.n_job_vn} (${pct(+m.n_job_vn)})`}</KV>
          <KV k="Bị giới hạn địa lý">
            {`${(+m.n_job_excluded).toLocaleString("vi-VN")} (${pct(+m.n_job_excluded)})`}
          </KV>
          <KV k="Chưa xác định">
            {`${(+m.n_job_unknown).toLocaleString("vi-VN")} (${pct(+m.n_job_unknown)})`}
          </KV>
      </KVTable>

      <h2 className="mt-10 text-[21px]">Đối chứng tay</h2>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        Bộ quy tắc được đối chứng bằng <b>chấm mù</b>: người chấm đọc tin gốc và kết luận độc lập,
        không nhìn nhãn máy. Bất đồng thì người thứ hai đọc lại từ đầu và phân xử.
      </p>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        <b>Đo riêng chiều “mở”.</b> Mẫu ngẫu nhiên gần như không chạm nhóm mở toàn cầu — nhóm đó
        chỉ chiếm hơn 1% kho. Nên phép đo quan trọng nhất phải <b>lấy mẫu phân tầng</b>: rút thẳng
        từ nhóm đã gán “mở”, đúng nơi sai lầm gây thiệt hại lớn nhất.
      </p>
      <KVTable>{AUDIT.map(([k, v]) => <KV key={k} k={k}>{v}</KV>)}</KVTable>
      <p className="mt-4 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        Mỗi đợt dùng mẫu <b>không giao</b> với đợt trước. <b>Đợt 3 là lần đo trung thực đầu tiên</b> —
        hai đợt đầu lấy ngẫu nhiên nên hầu như chỉ chạm nhóm bị loại, tức chiều dễ. Con số 90% của
        đợt 2 không sai, nó chỉ <b>đo nhầm thứ</b>.
      </p>

      <h2 className="mt-10 text-[21px]">Mười loại lỗi đã tìm ra và sửa</h2>
      <ul className="mt-4 grid gap-2 sm:grid-cols-2">
        {FIXES.map((f) => (
          <li
            key={f}
            className="rounded-md border border-line bg-card px-4 py-3 text-[13px] leading-relaxed text-text-2 transition-colors hover:border-field"
          >
            {f}
          </li>
        ))}
      </ul>
      <p className="mt-4 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        <b>Điều một yêu cầu múi giờ KHÔNG chứng minh.</b> “Làm giờ EST” là yêu cầu ca làm, không
        phải yêu cầu nơi ở — người tại Việt Nam làm 20:30–05:30 giờ Việt vẫn đáp ứng được. Suy
        “phải làm giờ Mỹ” thành “phải ở Mỹ” là lỗi mà chính người chấm mắc hai lần, máy thì không.
      </p>

      <h2 className="mt-10 text-[21px]">Còn sai ở đâu</h2>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        97,5% nghĩa là <b>cứ 40 tin gắn nhãn “mở” thì khoảng 1 tin sai</b>. Khoảng tin cậy 95% cho
        con số này là 87–100% — mẫu 40 tin không đủ để phân biệt 97,5% với 92%.
      </p>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        Điểm yếu đã biết: nhóm dựa vào bằng chứng <b>văn xuôi</b> thay vì trường địa điểm có cấu
        trúc mỏng manh nhất, vì một câu trong mô tả dễ bị đọc lệch ngữ cảnh hơn một trường dữ liệu.
      </p>
      <p className="mt-3 max-w-[68ch] text-[14.5px] leading-relaxed text-text-2">
        <b>Giới hạn mẫu, nói thẳng:</b> ba nguồn ATS công khai; slug thu từ chỉ mục web nên thiên
        về công ty Mỹ và châu Âu; đây là ảnh chụp tại một thời điểm, không phải toàn bộ thị trường.
      </p>
      <p className="mt-6 font-mono text-[12px] text-text-3">Kho dựng ngày {m.built_at}.</p>
    </>
  )
}
