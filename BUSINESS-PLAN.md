# Kế hoạch kinh doanh — 18 tháng

**Ngày:** 21/08/2026 · **Mô hình:** [business-model.md](business-model.md) · **Vận hành:** [OPERATIONS.md](OPERATIONS.md)
**Trạng thái:** chưa launch. Doanh thu **0**. A3 (phía cầu) **chưa bao giờ chạy**.

---

## 0. Đọc cái này trước

Tài liệu này có **hai** thứ mà kế hoạch kinh doanh thường trộn lẫn:

1. **Điều đã biết** — số đo được, ghi rõ nguồn.
2. **Điều đang cược** — giả định chưa kiểm, ghi rõ là giả định.

Trộn hai thứ đó là cách tự lừa mình hiệu quả nhất. Ở đây chúng tách bảng riêng.

---

## 1. Điều đã biết

| Số | Giá trị | Nguồn |
|---|---|---|
| Công ty có hồ sơ | **3.666** | đo |
| Công ty tuyển được ở VN | **110** (3,0%) | đo |
| Công ty khoá hoàn toàn | **2.485** (67,8%) | đo |
| Tin remote đã chấm | **34.313** | đo |
| Tin mở | **409** (1,2%) | đo |
| Tin nêu cơ chế trả lương | **3,0%** máy · **7,2%** chấm tay (n=150) | đo — dù lấy số nào thì >92% không nói |
| Tin ghi rõ tuyển được ở VN | **0/150** | chấm tay |
| Precision nhãn "mở" | **97,5%** | audit phân tầng, mẫu 40, KTC 87–100% |
| Lập trình viên VN | **530.000** | báo cáo ngành |
| Chi phí vận hành | **~12 USD/năm** | tính |
| Thời gian vận hành | **12 giờ/tháng** | ước từ quy trình thật |

---

## 2. Điều đang cược

| Giả định | Nếu sai thì sao | Kiểm bằng |
|---|---|---|
| Kỹ sư Việt quan tâm đủ để quay lại | Không có khán giả → không có gì để bán | **A8** · cổng 30 ngày |
| Nhà cung cấp EOR muốn mua dữ liệu địa lý tuyển | **Toàn bộ giai đoạn 2 sụp** | **A3** |
| Phát hiện "0/150" đủ hấp dẫn để lan | Không có phân phối → không có khán giả | GĐ 0 |
| Kho lên được 10.000 công ty | Dưới ngưỡng đó dữ liệu không bán được | Đã đi 3.666, nguồn slug đang cạn |
| Precision giữ ≥95% khi kho gấp ba | Sản phẩm mất thứ duy nhất nó bán | Audit hằng tháng |

**Rủi ro lớn nhất không phải kỹ thuật.** Là ô số 2: chưa một mẩu bằng chứng nào cho thấy có
người trả tiền.

---

## 3. Ba giai đoạn, có cổng thoát

### GĐ 0 — Launch và đo khán giả · tháng 0–3 · doanh thu 0

**Mục tiêu duy nhất: biết có ai quan tâm không.** Không kiếm tiền.

| Tuần | Việc | Ai |
|---|---|---|
| 1 | Cloudflare: tạo D1, nạp seed, deploy, tên miền | **Bạn** |
| 1 | Cài cron `refresh.sh --deploy` | **Bạn** |
| 2–3 | **A8 — 10 cuộc với kỹ sư Việt thật.** Hỏi: *trước khi nộp đơn remote, bạn kiểm gì?* | **Bạn** |
| 3 | Bài công bố — **đã viết**: [content/bai-cong-bo.md](content/bai-cong-bo.md) + [bản ngắn](content/bai-cong-bo-ngan.md) | Bạn đọc lại, thay `[LINK]` |
| 4 | Đăng: nhóm dev Việt trên Facebook, /r/vietnam, Hacker News, LinkedIn | **Bạn** |
| 5–12 | Vận hành theo [OPERATIONS.md](OPERATIONS.md) · audit hằng tháng | Tự động + 12h/tháng |

**Bài công bố** — mũi nhọn phân phối, không phải danh sách tin:

> *"Tôi chấm 34.313 tin remote của 3.666 công ty. 86,3% khoá theo địa lý. 0/150 ghi rõ tuyển
> được ở Việt Nam. Hơn 92% không nói cơ chế trả lương. Đây là 110 công ty tuyển được người ở
> VN, mỗi kết luận kèm trích dẫn."*

Bản đầy đủ: [content/bai-cong-bo.md](content/bai-cong-bo.md) · ba bản ngắn cho Facebook,
LinkedIn, Hacker News: [content/bai-cong-bo-ngan.md](content/bai-cong-bo-ngan.md)

**Cổng ra GĐ 0** — đo ở ngày thứ 30 sau launch:

| Kết quả | Hành động |
|---|---|
| ≥ 500 người dùng duy nhất | Đi tiếp GĐ 1 |
| 100–500 | Đi tiếp nhưng **hoãn GĐ 2**, dồn sức vào phân phối |
| < 100 | **Dừng lại.** Xem lại giả định gốc, đừng xây thêm |

---

### GĐ 1 — Tiền nhỏ, an toàn sứ mệnh · tháng 3–9 · mục tiêu 350–1.150 USD/tháng

Hai dòng, cả hai **không đổi được nội dung xuất bản**:

| Dòng | Cơ chế | Ước tính |
|---|---|---|
| **Tài trợ** | Một dòng tách bạch rõ, nhà cung cấp EOR là người mua tự nhiên | 200–1.000 USD/th |
| **Affiliate cổng thanh toán** | Wise/Payoneer — **kỹ sư chính là người mua**, nên attribution chạy | ~150 USD/th |

**Không đủ sống.** Mục đích không phải sống — là kiểm xem *có ai quan tâm đủ để trả tiền* trước
khi đầu tư vào GĐ 2.

Song song, việc quan trọng nhất của cả kế hoạch:

> **A3 — 10 cuộc với nhà cung cấp EOR và công ty gia công VN.**
> Hỏi thẳng: *dữ liệu địa lý tuyển dụng theo công ty giải quyết vấn đề gì của anh, và trả
> bao nhiêu?*

**Cổng ra GĐ 1:**

| Kết quả A3 | Hành động |
|---|---|
| ≥ 3/10 nói sẽ trả ≥ 200 USD/tháng | Vào GĐ 2 |
| 1–2/10 | Làm thử một khách trả tiền trước khi xây API đầy đủ |
| 0/10 | **Không vào GĐ 2.** Giữ GĐ 1 làm dự án phụ, hoặc dừng |

---

### GĐ 2 — Dữ liệu B2B · tháng 9–18 · mục tiêu 4.900 USD/tháng

**Chỉ vào khi A3 xác nhận.** Ba điều kiện, thiếu một là chưa vào:

1. A3 đạt cổng trên
2. Kho ≥ **10.000 công ty** (nay 3.666)
3. Precision ≥ **95%** trên ba đợt audit liên tiếp

Sản phẩm: **sổ đăng ký địa lý tuyển dụng** — API + file, cập nhật hằng tháng.
Đã có nguyên mẫu chạy: `/api/companies`.

Người mua: nhà cung cấp EOR (Deel, Remote, Oyster, Multiplier) làm outbound · công ty gia công
VN tìm khách · hãng nghiên cứu thị trường.

**Ta không cạnh tranh bằng độ rộng** — PredictLeads có 123 triệu công ty. Ta bán **một thuộc
tính không ai tính**: *công ty này thật sự tuyển được ở đâu, và câu nào trong tin chứng minh*.

Toán: 10 khách × 490 USD/tháng = **4.900 USD/tháng**. Đủ sống. Cũng là con số **chưa có một
mẩu bằng chứng nào** — 490 USD là giá PredictLeads cho quy mô gấp 33.000 lần, nên coi là
**trần**, không phải kỳ vọng. Kịch bản thận trọng: 10 × 150 = 1.500 USD/tháng.

---

## 4. Ba kịch bản 18 tháng

| | Xấu | Cơ sở | Tốt |
|---|---|---|---|
| Người dùng/tháng (T18) | < 100 | 2.000 | 15.000 |
| Kho công ty | 4.000 | 8.000 | 12.000 |
| Khách B2B trả tiền | 0 | 3 | 12 |
| Doanh thu/tháng (T18) | 0 | ~800 USD | ~5.000 USD |
| Kết luận | Dừng ở tháng 3 | Dự án phụ có lãi nhỏ | Có thể làm toàn thời gian |

**Kịch bản xấu chỉ tốn ~12 USD và ba tháng.** Đó là điều tốt nhất của cấu trúc chi phí này:
thất bại rẻ, và biết sớm.

---

## 5. Ràng buộc không được vi phạm để lấy doanh thu

| Cấm | Vì sao |
|---|---|
| Đăng tin trả phí trộn vào danh sách đã lọc | Tiền mua vị trí = phá huỷ chính thứ đang bán |
| Bán CV, lead ứng viên | Luật 91/2025 cấm mua bán dữ liệu cá nhân — **phạt tới 10× doanh thu** |
| Thu dữ liệu cá nhân nhạy cảm | Mất miễn trừ DPO/DPIA của NĐ 356/2025 |
| Sửa nhãn theo yêu cầu công ty trả tiền | Thất bại sứ mệnh, không phải bug |

Quy tắc một dòng: **nếu một khoản tiền có thể đổi nội dung được xuất bản, khoản đó bị loại.**

---

## 6. Việc kế tiếp, theo thứ tự

| # | Việc | Ai | Chặn cái gì |
|---|---|---|---|
| 1 | Deploy + tên miền + cron | **Bạn** | Mọi thứ |
| 2 | **A8** — 10 cuộc với kỹ sư Việt | **Bạn** | Biết sản phẩm có đúng vấn đề không |
| 3 | Đăng bài công bố *(đã soạn)* | **Bạn** | Phân phối |
| 4 | **A3** — 10 cuộc với EOR / công ty gia công | **Bạn** | **Toàn bộ GĐ 2** |
| 5 | Mở rộng kho lên 10.000 công ty | Máy | GĐ 2 |

**Việc số 4 quyết định dự án này có mô hình kinh doanh hay chỉ là một đóng góp công cộng.**
Cả hai đều là kết quả chấp nhận được — nhưng phải biết mình đang ở cái nào.
