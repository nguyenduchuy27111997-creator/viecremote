# Chiến lược khán giả — tiếp cận dev Việt

**Ngày:** 17/08/2026
**Bối cảnh:** [STATUS.md](STATUS.md). Cổng 0.1 đã loại mô hình bản tin việc làm; đây là hướng thay thế.

---

## 0. Kết luận trước

**Audience-first là hướng đúng — nhưng thứ tự đề xuất bị ngược, và một mắt xích là bất hợp pháp.**

Ba sửa:

| Đề xuất | Vấn đề | Sửa |
|---|---|---|
| Login để có nhiều người dùng | Login là **thuế chuyển đổi**, không phải tài sản, khi chưa có gì sau cổng | Email trước. Login ở tháng 6, khi có dữ liệu đáng gác |
| Gửi email thường xuyên | Tần suất đi trước giá trị = chết tên miền | Tuần, và chỉ khi mỗi số có thứ chưa ai có |
| "Sau này tính chuyện kiếm tiền" | Con đường hiển nhiên nhất (bán quyền truy cập ứng viên) **bị PDPL cấm**, phạt tới 10× doanh thu | Chốt giả thuyết doanh thu **ngay bây giờ** — nó quyết định thu hút ai |

Và một điều quan trọng hơn cả ba:

> **Audience-first hoãn việc KIẾM TIỀN, không hoãn việc TẠO GIÁ TRỊ.** Vẫn cần lý do để 100 người đầu tiên xuất hiện. Cổng 0.1 vừa chứng minh lý do hiển nhiên (danh sách việc tốt hơn) là **yếu**.

Nhưng có một lý do khác, mạnh hơn, và nó nằm ngay trong dữ liệu vừa đo.

---

## 1. Mồi câu không phải danh sách việc — là NGHIÊN CỨU

Sáu vòng đo đạc sinh ra những con số **không tồn tại ở đâu khác, bằng tiếng Việt hay tiếng Anh**:

| Phát hiện | Vì sao dev Việt quan tâm |
|---|---|
| **84% tin "remote" giới hạn địa lý** — đọc tay 150 tin | Giải thích vì sao họ nộp 30 lần được hồi đáp 1 |
| **0/150 tin khai tuyển được ở VN** | Xác nhận cảm giác của họ là đúng, không phải do họ kém |
| **79% công ty ghi `worldwide` nhưng tin thật bị giới hạn** — GitLab, Linear, Replit, Twilio, Ramp nêu tên | Cụ thể, kiểm chứng được, gây tranh luận |
| **Chỉ 7% tin nêu cơ chế trả lương** | Đặt tên cho nỗi đau chưa ai đặt tên |
| **Chỉ 25% tin khai `applicantLocationRequirements`** — và cách đọc nó trong 10 giây | Mẹo dùng được ngay |
| **Nghị định 253/2026 hiệu lực 01/07/2026**, giảm trừ 15,5tr/tháng | Mọi bài tiếng Việt đang lưu hành đã sai số liệu |

Đây là **nghiên cứu gốc**, và nghiên cứu gốc là thứ vừa lan truyền được trong cộng đồng vừa được AI trích dẫn ([brd-v2.md](brd-v2.md) Mục 16.1.1).

**Tiêu đề đầu tiên tự nó là một bài:**

> *"Tôi đọc tay 150 tin remote quốc tế. Không tin nào tuyển được ở Việt Nam."*

Bài đó không cần sản phẩm. Không cần login. Không cần pipeline. Nó đã viết được từ hôm nay.

---

## 2. Khán giả tìm việc là DÒNG CHẢY, không phải TỒN KHO

Đây là điểm quyết định cách đo thành công, và hầu hết chiến lược audience bỏ qua.

Người đăng ký vì **đang tìm việc**. Khi có việc, họ ngừng đọc. Danh sách **tự phân rã** — khác hẳn khán giả dev-tools hay tin tức, nơi người ta ở lại nhiều năm.

Hệ quả:

| Đo sai | Đo đúng |
|---|---|
| Tổng người đăng ký | **Số người/tháng đi qua giai đoạn "sắp nhận offer"** |
| Tỷ lệ giữ chân dài hạn | **Tỷ lệ chuyển đổi tại thời điểm rời đi** |

Và đây là chỗ đẹp: **thời điểm họ rời đi chính là thời điểm họ cần EOR, cần Wise/Payoneer, cần tư vấn thuế.** Deel trả **1.500 USD/khách mới** (đã kiểm chứng, [brd-v2.md](brd-v2.md) 11.3.1).

> Rời bỏ không phải thất bại của mô hình. **Rời bỏ chính là sự kiện kiếm tiền.**

Nghĩa là đừng tối ưu cho người ở lại lâu. Tối ưu cho **số người đi qua**, và cho việc có mặt đúng lúc họ đi.

---

## 3. Giả thuyết doanh thu — chốt bây giờ, thực thi sau

Không chốt bây giờ thì sẽ thu hút sai khán giả. "Mọi dev Việt" cho CPM thấp. **"Dev Việt đang thật sự theo đuổi remote quốc tế"** là đúng phân khúc mà bên trả tiền muốn.

| # | Dòng | Hợp pháp | Điều kiện |
|---|---|---|---|
| 1 | **Affiliate EOR / thanh toán** (Deel 1.500 USD/khách, Wise, Payoneer) | Có | Có ngay từ người đầu tiên nhận offer. Bắt buộc công bố quan hệ affiliate |
| 2 | **Tài trợ bản tin** | Có | CPM dev 25–150 USD. Ở 3.000 người đăng ký, một slot/tuần ≈ 450–600 USD/tháng |
| 3 | **Hồ sơ công ty "đã xác minh cơ chế"** | Có | Cần dataset trước |
| 4 | ~~Bán quyền truy cập ứng viên~~ | **KHÔNG — PDPL cấm**, phạt tới 10× doanh thu | — |

Dòng 2 đáng chú ý: **450–600 USD/tháng ở 3.000 người đăng ký** vượt xa kịch bản cơ sở của mô hình cũ (150–300 USD/tháng). Bản tin dev có tỷ lệ mở 40–50% — cao bất thường, và đó là lý do CPM cao.

---

## 4. Kênh — cụ thể, có tên

| Kênh | Ghi chú | Rủi ro |
|---|---|---|
| **Viblo** (`viblo.asia`) | Cộng đồng IT hàng đầu VN, tiếng Việt, từ 2014. **Đã có Viblo CV** → vừa là kênh vừa là đối thủ tiềm năng | Đăng bài nghiên cứu ở đây là cách nhanh nhất chạm đúng người. Nhưng đừng xây thứ cạnh tranh trực diện với Viblo CV |
| **Spiderum** | Mạng chia sẻ quan điểm, không riêng IT | Khán giả rộng hơn, ít đúng phân khúc hơn |
| **VOZ** | Diễn đàn lớn, mục IT | Văn hoá khắt khe với self-promotion — đọc luật trước |
| **Nhóm Facebook dev VN** | Nơi hard side thật sự ở | **Chưa lập bản đồ (R10).** Bị ban ở nhóm lớn nhất = mất kênh chính vĩnh viễn |
| **Bản tin riêng** | Kênh duy nhất sở hữu được | Chỉ có giá trị sau khi ba kênh trên đưa người tới |

**Nguyên tắc:** ba kênh đầu là **đất thuê**. Bản tin là **đất sở hữu**. Mọi bài đăng phải có đường dẫn về bản tin, nếu không thì đang xây tài sản cho người khác.

---

## 5. Login — trả lời câu "khi nào", không phải "có hay không"

Login mua được: cá nhân hoá, dữ liệu người dùng chất lượng hơn, cơ chế giữ chân.
Login tốn: **tỷ lệ chuyển đổi**. Ở 0–1.000 người, email-only chuyển đổi cao hơn nhiều lần. Và nó mở rộng bề mặt PDPL đúng lúc chưa có gì để bảo vệ.

[prd.md](prd.md) P4 đã chọn **không tài khoản** ở v1 vì lý do đó. Lý do vẫn đứng.

**Điều kiện để mở login:**

1. Có **tài sản đáng gác** — dataset công ty × cơ chế trả lương. Hiện có **0 bản ghi**; A8 sinh ra 10–20
2. ≥ 1.000 người đăng ký email — đủ để đo được chênh lệch chuyển đổi
3. Đã qua rà soát pháp lý ([legal-brief.md](legal-brief.md))

Trước đó: **email + xác nhận hai bước, không mật khẩu, không hồ sơ.**

---

## 6. Tần suất email — ràng buộc cứng

Đã nghiên cứu ([prd.md](prd.md) FR-6.7): tỷ lệ báo spam mục tiêu **< 0,10%**; người gửi tuân thủ đạt ~89% vào inbox, không tuân thủ **22–34% rơi vào spam**.

| Nhịp | Điều kiện |
|---|---|
| **Tuần** | Mặc định. Mỗi số phải có ≥1 thứ chưa ai có |
| 2 lần/tuần | Chỉ khi tỷ lệ mở > 45% qua 8 số liên tiếp |
| Hằng ngày | Không. Nguồn cung 4% không đủ, và sẽ thành nhiễu |

**Quy tắc:** ít hơn 8 tin worldwide trong tuần → **vẫn gửi**, nói thẳng số lượng thấp. Độn tin yếu là cách nhanh nhất mất niềm tin ([prd.md](prd.md) FR-6.6).

---

## 7. Kế hoạch 8 tuần

| Tuần | Việc | Sinh ra |
|---|---|---|
| **1** | **A8** — 10 cuộc trò chuyện ([a8-interview.md](a8-interview.md)) | Quyết định đi/dừng + 10–20 bản ghi cơ chế |
| **1** | Bản đồ cộng đồng (R10) — nhóm nào, luật gì, admin ai | Danh sách kênh, tránh bị ban |
| **2** | **Bài 1**: *"Tôi đọc tay 150 tin remote. Không tin nào tuyển được ở VN."* Đăng Viblo + 2 nhóm FB | Kiểm giả thuyết mồi câu |
| **2** | Trang đăng ký email. Không login | Kênh sở hữu |
| **3–4** | **Bài 2**: *"84% tin remote không tuyển ngoài nước họ — cách nhận ra trong 10 giây"* (dạy đọc `applicantLocationRequirements`) | Nội dung dùng được ngay |
| **4** | Bản tin số 1: 10–20 tin worldwide **+ cột cơ chế** từ bản ghi A8 | Sản phẩm tối thiểu |
| **5–6** | **Bài 3**: thuế & cách nhận tiền theo Nghị định 253/2026 — **sau khi kế toán rà** | Nội dung không ai cập nhật |
| **7–8** | Đo: người đăng ký, tỷ lệ mở, nguồn đến. Quyết định có tiếp không | Dữ liệu quyết định |

**Cổng tuần 8:** ≥ 300 người đăng ký **và** tỷ lệ mở ≥ 40% → tiếp tục, bắt đầu affiliate. < 100 người đăng ký → mồi câu sai, dừng.

---

## 8. Ba cách hỏng, đã lường

**1. Xây khán giả sai.** Thu hút "mọi dev Việt" bằng nội dung chung chung → CPM thấp, affiliate không chuyển đổi. **Phòng:** mọi bài phải nói về *làm remote cho nước ngoài*, không về lập trình nói chung.

**2. Đất thuê bị thu hồi.** Bị ban khỏi nhóm FB lớn nhất, hoặc Viblo đổi chính sách. **Phòng:** R10 trước khi đăng; mọi bài dẫn về bản tin.

**3. Nội dung cạn sau 3 bài.** Sáu vòng nghiên cứu cho khoảng 6–8 bài. Sau đó phải **tạo dữ liệu mới** — tức là quay lại đo. **Phòng:** coi việc đo là hoạt động định kỳ, không phải giai đoạn. Mỗi quý chấm lại 100 tin → bài mới + dữ liệu tươi cho GEO.

---

## 9. Điều chiến lược này KHÔNG sửa

**Phía cầu vẫn chưa được kiểm.** A3 chưa bao giờ chạy. Khán giả dev không tự sinh ra người trả tiền — affiliate và tài trợ thì có, nhưng hồ sơ công ty trả phí thì vẫn cần công ty đồng ý trả.

**Mật độ việc vẫn là 4%.** Bản tin sẽ có 10–25 tin/tuần, không phải 100. Đó là trần.

**Vẫn treo vào A8.** Nếu nhãn cơ chế không đổi hành vi kỹ sư, bản tin mất điểm khác biệt và trở lại là bản sao của Real Work From Anywhere — miễn phí, đã tồn tại, tiếng Anh.
