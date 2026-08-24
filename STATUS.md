# Trạng thái — 23/08/2026

> **ĐỔI HƯỚNG 22/08** sang **mạng lưới nối công ty nước ngoài với kỹ sư Việt** ([PIVOT.md](PIVOT.md)).
> **SỬA THỨ TỰ 23/08** sau khi đối chiếu toàn văn Công báo: **Đ3 trước, L2 sau**
> ([legal-research.md](legal-research.md) · [legal-options.md](legal-options.md)).

## Ba tầng, theo đúng thứ tự làm

| | Là gì | Trạng thái | Cần giấy phép? |
|---|---|---|---|
| **L1** | Tra cứu minh bạch — công ty nào tuyển được ở VN | ✅ **Chạy**, precision 97,5% | Không |
| **Đ3** | Bán nghiên cứu cho công ty nước ngoài | ✅ **Chạy** — `/hiring-in-vietnam`, báo cáo, 13 thư chào hàng soạn sẵn | Miễn phí: không · **Thu tiền: vùng xám** — [legal-options.md](legal-options.md) Đ3 |
| **L2** | Mạng lưới — hồ sơ kỹ sư, giới thiệu có thu phí | 🔒 Đã đặc tả, **hai câu pháp lý còn chặn** | Có — [prd.md](prd.md) Mục 2 |

**Vì sao Đ3 trước:** L2 cần Giấy phép + ký quỹ 300 triệu, mà hai câu pháp lý chưa có lời giải.
Bỏ 300 triệu trước khi trả lời được là đặt cược sai thứ tự. Đ3 có doanh thu, không cần giấy
phép nào, và trả lời câu quan trọng hơn — *có ai trả tiền không*.

**Việc kế tiếp là của bạn, không tự động được:** tìm địa chỉ liên hệ cho 13 thư trong
`content/outreach-*.txt` rồi gửi. Đó là bài kiểm tra thật của Đ3.
Trục chuyển từ *tin* sang *công ty* (21/08). Giao diện chuyển sang **Next.js 16 + Cloudflare D1**
(21/08) — xem [ARCHITECTURE-WEB.md](ARCHITECTURE-WEB.md), triển khai [DEPLOY-WEB.md](DEPLOY-WEB.md). Spec: [prd.md](prd.md). Launch mục tiêu ~2–3 tuần.

---

## Sứ mệnh

> **Làm thị trường việc remote quốc tế minh bạch với kỹ sư Việt Nam.**

Không phải giúp họ được tuyển. Làm cho họ **nhìn thấy sự thật**. Chi tiết: [MISSION.md](MISSION.md).

Hai hệ quả chi phối mọi quyết định build:
1. **Độ chính xác chính là sản phẩm** — nhãn sai là thất bại sứ mệnh, không phải bug
2. **Câu "không" giá trị ngang câu "có"** — và dữ liệu loại trừ là thứ dồi dào nhất

---

## Dữ liệu — đo được, không ước lượng

150 tin remote ngẫu nhiên, chấm tay từ toàn văn:

| | | |
|---|---|---|
| Loại trừ (bị giới hạn địa lý) | 126 | **84,0%** |
| Chưa xác định | 18 | 12,0% |
| Mở toàn cầu | 6 | 4,0% |
| **Ghi rõ tuyển được ở VN** | **0** | **0,0%** |

Cận trên 95%: **1,98%**.

**Số khác:** tin nêu cơ chế trả lương **7,2%** · tin khai `applicantLocationRequirements` **25%** · đòn bẩy công ty **64:1** · nhãn `worldwide` của danh bạ cộng đồng sai **79%** ở mức tin · chi phí chấm tay ~2 phút/tin · chi phí LLM 5–35 USD/tháng.

**Chất lượng phép đo:**

| Phép đo | Kết quả |
|---|---|
| Đối chứng cố định 180 tin | precision 100% · DQ recall 100% · accuracy 100% |
| **Chấm mù phân tầng, mẫu mới** | **precision 97,5%** (39/40) · KTC 95%: 87–100% |

**Lấy mẫu phân tầng là bắt buộc.** Mẫu ngẫu nhiên gần như không chạm nhóm "mở toàn cầu"
(hơn 1% kho), nên hai đợt đo đầu — 85% rồi 90% — **đo nhầm thứ**. Lần rút thẳng từ nhóm
"mở" đầu tiên cho **70%**. Mười loại lỗi cơ học được tìm ra và sửa; đo lại trên mẫu không
giao: 90%, rồi 97,5%.

> **Càng xa tin tuyển dụng thật, tuyên bố càng "toàn cầu".** Mẫu hình lặp ở ba nguồn độc lập.

---

## Điều dữ liệu quyết định về sản phẩm

Trang này **không phải bộ lọc tìm việc tốt** — 0/150 nghĩa là không có gì để lọc ra.
Nó là **bộ kiểm tra loại trừ** — 84% có lý do trích dẫn được.

Marketing hứa sai chuyện này thì thất bại ngày đầu tiên.

---

## Tài sản

**Pipeline chạy được** (`tools/`, Python stdlib, không framework/DB/server):
`pull_sample` · `discover_slugs` · `export_jobs` · `rescore` · `country` · `score_rules` ·
`tiering` · `eval` — và **`build.py`** sinh toàn bộ site tĩnh.

**Kho hiện tại: 34.313 tin remote · 3.666 công ty** (21/08: +11.390 tin, +1.256 công ty).

**Trục công ty** — 110 tuyển được ở VN · 1.071 chưa rõ · 2.485 khoá.

| Nhãn tin | Số tin | |
|---|---|---|
| Mở toàn cầu + mở cho VN | 409 | 1,2% |
| Bị giới hạn địa lý | 29.607 | 86,3% |
| Chưa xác định | 4.297 | 12,5% |

110 công ty có tin mở. **`scoring-sheet.csv`** — 180 tin chấm tay, có trích dẫn.
**`a9-targets.csv`** — 403 công ty worldwide, đã xếp hạng.

**Năm cổng chặn build** (build FAIL nếu vi phạm): C1 mọi nhãn phải có trích dẫn nguyên văn
chứa từ khoá đã khớp · C2 không phát sinh JobPosting schema · C3 chỉ tin đang mở ·
C4 trích đoạn ≤300 ký tự · C5 không được gán "mở toàn cầu" khi công ty tự khai danh sách
nước không có VN. Cộng thêm kiểm link nội bộ.

**Hai bản giao diện cùng chạy được:**

| | `build.py` (tĩnh) | `web/` (Next.js 16) |
|---|---|---|
| Build | 2,0 giây · 0 phụ thuộc | ~25 giây · 288 gói |
| Tra cứu | không | FTS5 phía máy chủ |
| API B2B | không | `/api/companies` |
| Cổng C1–C5 | ✅ cả 5 | ✅ cả 5 |

Cổng nằm ở **`tools/gates.py`**, hai luồng cùng gọi — một bộ luật, không nhân đôi.
Đã kiểm đối kháng: 6 ca cố ý làm hỏng đều bị chặn, cả hai luồng thoát mã 1.

Bản tĩnh là đường lui, giữ tới khi Next.js chạy production ổn định một tháng.

**Hệ thiết kế:** [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) — hướng **Linear/Vercel**: nền tối mặc
định, màu OKLCH (ba màu ngữ nghĩa cùng độ sáng cảm nhận), sans toàn bộ (bỏ serif), có chuyển
động và phím tắt ⌘K. Tương phản đo trên DOM thật 1.338 phần tử đạt, cả hai chế độ.

**ĐÃ LAUNCH.** L1 chạy tại https://viec-remote.nguyenduchuy27111997.workers.dev
Repo: https://github.com/nguyenduchuy27111997-creator/viecremote (public)
Cập nhật hằng ngày: GitHub Actions 22:17 UTC — [OPERATIONS.md](OPERATIONS.md) Mục 8.

**Chặn còn lại:** token Cloudflare Web Analytics (không có thì cổng GĐ 0 không đo được) ·
A8 và A3. Rà soát pháp lý hoãn tới trước ca nối đầu tiên.

---

## Lộ trình

| Mốc | Việc | Ước tính |
|---|---|---|
| M0 | `build.py`: danh sách + chi tiết tin | ✅ xong |
| M1 | Bộ lọc · trang "vì sao bị loại" · trang công ty | ✅ xong |
| M2 | Trang phương pháp · kiểm C1–C5 tự động | ✅ xong |
| M2b | Audit phân tầng đến precision ≥90% | ✅ xong — 97,5% |
| **M3** | **Tên miền · deploy · cron hằng ngày** | **← bạn làm, 3h** |
| **M4** | **Launch** | |

Kiến trúc: **sinh trang tĩnh**, không máy chủ, không database. Hosting 0 đồng.

### Năm ràng buộc không được bỏ

| | |
|---|---|
| **C1** | Mọi nhãn phải có **trích dẫn nguyên văn** chứa từ khoá đã khớp. Không trích được → "Chưa xác định" |
| **C2** | **Không phát sinh JobPosting schema** — Q1 chưa có câu trả lời pháp lý |
| **C3** | Tin biến mất khỏi feed → **gỡ trong 48h** |
| **C4** | Trích đoạn ≤ 300 ký tự, luôn link về tin gốc |
| **C5** | Không gán "mở toàn cầu" khi công ty tự khai danh sách nước **không có VN** |

**Build FAIL nếu vi phạm bất kỳ cổng nào** — cả năm đều đã chạy và đã từng chặn build thật.

---

## Chưa bao giờ kiểm

- **A3** — có công ty nào trả tiền không
- **A8** — nhãn cơ chế có đổi hành vi kỹ sư không
- **Rà soát pháp lý** — hoãn tới trước ca nối đầu tiên ([legal-research.md](legal-research.md) Mục 4)

**Chưa có bằng chứng nào cho thấy ai sẽ trả tiền.** Sứ mệnh làm rõ hướng, không làm rõ khả thi.
**Ba tài liệu kinh doanh:**
- [business-model.md](business-model.md) — *mô hình nào*: chuyển trục từ tin sang công ty, bảy phương án đã chấm
- [BUSINESS-PLAN.md](BUSINESS-PLAN.md) — *kế hoạch 18 tháng*: ba giai đoạn có cổng thoát, ba kịch bản
- [OPERATIONS.md](OPERATIONS.md) — *vận hành*: nhịp ngày/tuần/tháng, 12 giờ người/tháng, ~12 USD/năm
- [ARCHITECTURE-BACKEND.md](ARCHITECTURE-BACKEND.md) — *back-end + devops*: pipeline Python
  0 phụ thuộc, 7 lỗ hổng devops. **#1: dự án chưa phải git repo**
- [BUILD-NEXT.md](BUILD-NEXT.md) — *còn phải build gì*: **8 giờ chặn launch đã xong** (analytics,
  sitemap, 404, ảnh OG, nút báo sai). Còn 12 giờ nhóm sau, làm khi có số liệu cổng GĐ 0

A3 (phía cầu) chặn toàn bộ đường doanh thu có trần cao và **chưa bao giờ chạy**.

---

## File

| File | Vai trò |
|---|---|
| [prd.md](prd.md) | **Spec build** — đọc cái này để code |
| [MISSION.md](MISSION.md) | Sứ mệnh + 5 hệ quả |
| [rubric-spec.md](rubric-spec.md) | Quy tắc chấm nhãn, v0.4 |
| `tools/inbox.py` | **Hộp thư vận hành** — yêu cầu Đ3, báo sai, ghi danh trên production. Chạy mỗi sáng |
| [legal-research.md](legal-research.md) | **Pháp lý L2 — đối chiếu toàn văn Công báo** |
| [legal-options.md](legal-options.md) | **Cấu trúc hợp pháp — cửa nào đóng, cửa nào mở** |
| [legal-brief.md](legal-brief.md) | 15 câu cho luật sư/kế toán (nền) |
| `scoring-sheet.csv` · `a9-targets.csv` | Dữ liệu |
| `tools/` | Pipeline |
| `archive/` | v1, brd-v2, pivot-v3, chiến lược khán giả, bản đồ cộng đồng, bài viết — **giữ lại, không xoá** |

---

## Cổng sau launch

30 ngày, < 100 người dùng duy nhất → xem lại. Chỉ số sống còn: **tỷ lệ báo nhãn sai**.
