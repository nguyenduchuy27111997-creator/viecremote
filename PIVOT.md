# Đổi hướng: từ tra cứu sang mạng lưới

**Ngày:** 22/08/2026 · **Quyết định:** công ty nước ngoài ↔ kỹ sư Việt
**Thay thế** hướng "web tra cứu đọc-only" đã chốt 17/08

---

## 0. Điều cần biết trước tiên

`legal-brief.md` đã đánh dấu **đúng mô hình này** là câu hỏi chưa có lời giải — **B-Q5** — và
mặc định an toàn ghi trong đó là:

> *"Không triển khai mô hình giới thiệu dưới bất kỳ hình thức nào."*

Bây giờ bạn chọn đi vào đúng ô đó. Điều này **làm được**, nhiều công ty làm thật. Nhưng nó
biến dự án từ *"12 USD/năm, một người, không pháp nhân"* thành **một doanh nghiệp có điều kiện**.

Tài liệu này nói cái giá đó bằng con số, và nói cái gì trong 3 tháng vừa build vẫn còn dùng được.

---

## 1. Ba rào phải qua

### 1.1 Điều kiện kinh doanh dịch vụ việc làm

**Nghị định 352/2025/NĐ-CP**, hiệu lực 01/01/2026. Hoạt động *"tư vấn, giới thiệu việc làm"*
là ngành nghề có điều kiện.

| Điều kiện | Con số |
|---|---|
| Ký quỹ tại ngân hàng VN | **300.000.000 đồng** |
| Trụ sở, hợp đồng thuê tối thiểu | **24 tháng** |
| Người đại diện pháp luật | đủ năng lực và kinh nghiệm theo quy định |
| Pháp nhân | bắt buộc — không làm với tư cách cá nhân |

**Tin tốt:** thủ tục *cấp giấy phép* đã bị **bãi bỏ từ 01/07/2026** theo Luật Đầu tư sửa đổi 2025
— tức đã qua rồi. Không phải đi xin phép nữa.

**Tin cần hiểu đúng:** bãi bỏ thủ tục **không** đồng nghĩa nới điều kiện. Trọng tâm chuyển sang
**hậu kiểm** — phải duy trì đủ điều kiện suốt quá trình hoạt động, và bị kiểm tra bất kỳ lúc nào.
Thiếu ký quỹ khi bị kiểm là vi phạm, không phải "chưa kịp làm".

Luật cũng nói rõ dịch vụ việc làm **được** thực hiện bằng phương thức điện tử và thương mại
điện tử — nên nền tảng online không nằm ngoài phạm vi, mà nằm **trong** phạm vi.

### 1.2 Chuyển dữ liệu cá nhân ra nước ngoài

Đây là rào ít ai nghĩ tới, và nó chạm vào **đúng hành vi cốt lõi** của mô hình: gửi hồ sơ kỹ sư
Việt cho công ty nước ngoài.

**Điều 18, Nghị định 356/2025** yêu cầu, cho mỗi luồng chuyển:

- **Hồ sơ đánh giá tác động chuyển dữ liệu xuyên biên giới** (Mẫu số 09)
- **Thông báo Bộ Công an**, nộp trong **60 ngày** kể từ ngày chuyển
- **Văn bản thoả thuận ràng buộc trách nhiệm pháp lý** với bên nhận ở nước ngoài
- Cam kết bảo vệ quyền của chủ thể dữ liệu Việt Nam

Có miễn trừ cho *quản lý nhân sự, vận chuyển hậu cần, thanh toán quốc tế, tình huống khẩn cấp*.
**Nhưng miễn trừ "quản lý nhân sự" nhiều khả năng dành cho doanh nghiệp quản lý nhân viên CỦA
MÌNH**, không phải cho bên trung gian gửi hồ sơ người thứ ba. Đây là điểm phải hỏi luật sư,
không được tự suy.

Hệ quả thực tế: **mỗi công ty nước ngoài nhận hồ sơ là một thoả thuận ràng buộc phải ký.**
Không thể "đăng hồ sơ lên cho ai xem cũng được".

### 1.3 Ranh giới "kết nối có đồng ý" và "mua bán dữ liệu"

Luật 91/2025 **cấm mua bán dữ liệu cá nhân**, chế tài tới **10 lần doanh thu** từ hành vi vi phạm.

Câu hỏi B-Q5 nguyên văn: ứng viên bấm *"cho phép giới thiệu tôi tới công ty X"*, có nhật ký
đồng ý, ta thu **phí dịch vụ kết nối** từ công ty. Đó là dịch vụ hợp pháp hay là bán dữ liệu?

**Vẫn chưa có câu trả lời.** Đây là câu hỏi đắt nhất trong toàn bộ dự án, và giờ nó không còn
tránh được nữa — nó nằm ngay giữa mô hình doanh thu.

### 1.4 Mất miễn trừ hiện có

Hiện dự án **được miễn** bổ nhiệm DPO và lập hồ sơ DPIA vì không xử lý dữ liệu nhạy cảm và dưới
100.000 chủ thể. Xử lý hồ sơ ứng viên ở quy mô mạng lưới sẽ **vượt cả hai điều kiện** — CV chứa
dữ liệu có thể bị xếp là nhạy cảm, và mục tiêu vốn là nhiều hơn 100.000 người.

---

## 2. Cái gì còn dùng được — nhiều hơn bạn nghĩ

Đây là phần đáng mừng. **Phía cầu của mạng lưới đã build xong rồi.**

| Tài sản | Vai trò mới |
|---|---|
| **3.666 hồ sơ địa lý tuyển dụng** | Chính là danh sách khách hàng tiềm năng, đã lọc sẵn |
| **110 công ty tuyển được ở VN** | **Khách hàng ấm nhất.** Họ đã chứng minh làm được — có sẵn cơ chế trả lương |
| **2.485 công ty khoá hoàn toàn** | Danh sách loại trừ. Đừng mất thời gian gọi |
| **Bảng `locked` 104 nước** | Biết công ty nào khoá vào đâu = biết ai *sắp* cần mở rộng |
| Pipeline chấm nhãn, cổng C1–C5 | Chạy nguyên, không sửa gì |
| Trang tra cứu công khai | **Phễu thu hút kỹ sư** — lý do để họ vào và quay lại |
| CI/CD, cron, seed nguyên tử | Dùng lại toàn bộ |

Nói cách khác: 3 tháng vừa rồi không phải xây nhầm. Nó xây **đúng một nửa** — nửa khó hơn, vì
dữ liệu công ty phải cào và chấm, còn hồ sơ kỹ sư thì họ tự nhập.

**Và nó xây được một thứ hiếm:** biết công ty nào *thật sự* tuyển được người ở Việt Nam, kèm
trích dẫn. Khi gọi bán, đó là câu mở đầu tốt hơn mọi lời chào.

---

## 3. Cái gì phải bỏ

| Điều đã chốt | Vì sao phải bỏ |
|---|---|
| *"Người dùng nên rời đi sau khi có câu trả lời"* | Mạng lưới cần họ **ở lại** |
| *"Không tài khoản, không đăng nhập"* | Hồ sơ kỹ sư bắt buộc phải có tài khoản |
| *"Không thu dữ liệu cá nhân"* | Đó chính là hàng hoá của mô hình mới |
| Chi phí ~12 USD/năm | Ký quỹ 300 triệu + pháp nhân + kế toán + luật sư |
| Miễn trừ DPO/DPIA | Mất khi vượt ngưỡng |

`MISSION.md` phải viết lại. Sứ mệnh A (*minh bạch thị trường*) vẫn đứng được — nhưng nó thành
**phương tiện** thu hút kỹ sư, không còn là mục đích cuối.

---

## 4. Đường đi đề xuất — không đảo lộn thứ tự

Đừng dựng pháp nhân và ký quỹ 300 triệu trước khi biết có ai dùng. Ba bước, mỗi bước có cổng.

### Bước 1 — Launch bản tra cứu, thu email · tháng 0–2 · chi phí ~12 USD

**Không đổi gì về mặt pháp lý.** Bản tra cứu hiện tại không phải dịch vụ việc làm: nó không
giới thiệu ai cho ai, không thu hồ sơ, không thu phí.

Mục tiêu: **đo xem có kỹ sư Việt nào quan tâm không.** Danh sách email chính là hạt giống của
mạng lưới sau này.

**Cổng:** 30 ngày sau launch, dưới 100 người dùng duy nhất ⇒ dừng. Mạng lưới không có người
thì không thành mạng lưới.

### Bước 2 — A3 với chính 110 công ty đó · tháng 2–4 · chi phí 0

Bạn đã có tên, có bằng chứng họ tuyển được ở Việt Nam, và có URL tin gốc.

Hỏi thẳng: *"Anh đang tuyển remote toàn cầu. Nếu tôi đưa 20 kỹ sư Việt đã sàng lọc, anh có
trả phí không, và bao nhiêu?"*

**Cổng:** dưới 3/10 nói có ⇒ **không dựng pháp nhân**. Giữ bản tra cứu làm dự án phụ.

### Bước 3 — Dựng pháp nhân, ký quỹ, xây mạng lưới · tháng 4+ · chi phí thật

Chỉ vào khi bước 1 và 2 đều qua cổng. Lúc đó mới tiêu tiền:

| Việc | Ước tính |
|---|---|
| Thành lập công ty | 3–10 triệu |
| **Ký quỹ** | **300 triệu** (giữ trong ngân hàng, không mất) |
| Thuê trụ sở 24 tháng | tuỳ |
| Luật sư: B-Q5 + Điều 18 + DPO | **cần thật, không tự làm được** |

---

## 5. Việc phải làm ngay, không chờ

Một việc, và nó rẻ:

> **Buổi tư vấn luật sư về ba câu hỏi B-Q5, Điều 18 NĐ 356, và điều kiện NĐ 352.**

Trước đây `legal-brief.md` nói buổi này *không chặn launch* vì đã chọn mặc định an toàn là
tránh hẳn mô hình giới thiệu. **Bây giờ mặc định đó không còn.** Ba câu hỏi này quyết định mô
hình có tồn tại được không, và trả lời sai thì chế tài là **10 lần doanh thu**.

Chi phí một buổi tư vấn nhỏ hơn nhiều so với việc build sáu tháng rồi phát hiện không được phép.

---

## 6. Rủi ro lớn nhất, nói thẳng

Không phải pháp lý. Pháp lý chỉ là tiền và giấy tờ, giải được.

**Rủi ro thật là cold start hai phía.** Kỹ sư không vào nếu chưa có công ty; công ty không trả
tiền nếu chưa có kỹ sư. Và bạn đang cạnh tranh với thứ vốn đã hoạt động: công ty gia công đã
có sẵn quan hệ, và mạng lưới giới thiệu cá nhân vốn miễn phí.

Lợi thế duy nhất bạn có mà họ không có: **biết chính xác công ty nào tuyển được ở Việt Nam, có
bằng chứng trích dẫn được.** Đó là thứ để mở cửa. Không phải thứ để giữ cửa.

Giữ cửa thì phải bằng chất lượng sàng lọc — và đó là việc của người, không phải của máy.
