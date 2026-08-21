# Mô hình kinh doanh

**Ngày:** 21/08/2026 · **Ràng buộc:** [MISSION.md](MISSION.md) hệ quả 4 · [legal-brief.md](legal-brief.md)
**Trạng thái:** phân tích, chưa kiểm chứng. A3 (phía cầu) **chưa bao giờ chạy**.

---

## 1. Kết luận trước, lập luận sau

**Job board không phải business ở đây.** 409 tin mở trên 34.313 (1,2%) không đủ làm hàng hoá. Playbook chuẩn của
job board — bán chỗ đăng tin và bán quyền truy cập CV — **cả hai đều bị cấm** bởi sứ mệnh và PDPL.

Thứ có giá trị không phải danh sách tin. Là **hồ sơ địa lý tuyển dụng của 3.666 công ty, mỗi
dòng có trích dẫn nguyên văn.** Không ai khác tính được thứ này.

Đề xuất: **chuyển trục sản phẩm từ *tin* sang *công ty*.**

| | Trục tin | Trục công ty |
|---|---|---|
| Số lượng | 409 mở / 34.313 | 110 mở / 3.666 |
| Vòng đời | Đổi hằng ngày | Đổi hằng quý |
| Đòn bẩy | 1:1 | **64:1** (đã đo) |
| Bán được cho B2B | Không | **Có** |
| Dính dữ liệu cá nhân | Không | Không |

---

## 2. Ràng buộc — thứ đóng cửa hầu hết lựa chọn

Viết ra trước khi bàn phương án, để không tự lừa mình.

| # | Ràng buộc | Nguồn | Đóng cửa cái gì |
|---|---|---|---|
| **R1** | Tiền không được đổi nội dung xuất bản | Sứ mệnh, hệ quả 4 | Đăng tin trả phí, featured listing, sponsored placement |
| **R2** | Cấm mua bán dữ liệu cá nhân, phạt tới **10× doanh thu** từ hành vi vi phạm | Luật 91/2025 | Bán quyền truy cập CV, bán lead ứng viên |
| **R3** | Đang được miễn DPO + DPIA (không xử lý dữ liệu nhạy cảm, <100.000 chủ thể) | NĐ 356/2025 | Mọi thứ làm mất miễn trừ này |
| **R4** | Kho chỉ **409 tin mở** (1,2%) | Đo được | Mô hình cần lượng hàng lớn |
| **R5** | Người dùng **nên rời đi** sau khi có câu trả lời | Sứ mệnh, hệ quả 5 | Subscription hướng người dùng cuối |
| **R6** | Một người, 10h/tuần | Thực tế | Dịch vụ tư vấn 1-1, sales outbound nặng |

**R1 + R2 giết luôn 90% doanh thu của job board thông thường.** RemoteOK thu 600 USD/tin đăng.
Job board ngách thu 299–600 USD/tin, 100–300 USD/tháng cho CV database. Cả hai dòng đó bị chặn.

**R5 là cái ít ai để ý và đau nhất.** Sản phẩm trả lời một câu hỏi *một lần*. Trả lời xong,
người dùng đi. Đó là sứ mệnh làm đúng, nhưng là retention tệ nhất có thể cho mô hình thuê bao.
**Đừng xây business dựa trên việc giữ chân kỹ sư.**

---

## 3. Ba tài sản thật sự đang có

| Tài sản | Quy mô | Ai khác có |
|---|---|---|
| **Hồ sơ địa lý tuyển của công ty**, có trích dẫn | 3.666 công ty | Không ai |
| **Vì sao bị loại**, phân loại + trích dẫn | 29.607 tin | Không ai |
| **Phương pháp đã kiểm chứng** — precision 97,5% mẫu phân tầng | 5 đợt audit | Không ai công bố |

Phân rã lý do loại — đây là dataset, không phải nội dung trang web:

| Số tin | Lý do |
|---|---|
| 19.023 | khoá theo nước/vùng/bang |
| 5.466 | hybrid / onsite |
| 1.621 | cần giấy phép lao động sở tại |
| 1.236 | quốc tịch / security clearance |
| 1.085 | công ty tự khai danh sách nước, **không có VN** |
| 793 | bắt buộc trả lương nội địa (W-2/PAYE) |
| 375 | bắt buộc múi giờ |
| 8 | khác |

Nước khoá tuyển nhiều nhất: US 11.589 · CA 933 · GB 850 · IN 607 · DE 431.

**Quan trọng: toàn bộ dữ liệu này là về CÔNG TY, không phải về CÁ NHÂN.** PDPL không áp dụng.
R2 và R3 không chạm tới nó. Đây là lý do nó là tài sản bán được duy nhất.

---

## 4. Nghịch lý cần nhìn thẳng

Việt Nam có **530.000 lập trình viên**, mỗi năm thêm 50.000–60.000 cử nhân IT, và đứng
**top 6 thế giới** về gia công phần mềm.

Nhưng đo 150 tin: **0 tin ghi rõ tuyển được ở Việt Nam.**

Hai điều này không mâu thuẫn. Chúng nói rằng **việc tuyển kỹ sư Việt có thật, nhưng không đi qua
tin đăng ATS công khai.** Nó đi qua công ty gia công, EOR, nhà thầu, giới thiệu nội bộ.

Hệ quả cho business:

- **0/150 không phải "không có cầu".** Là "cầu không xuất hiện ở kênh ta đang đo".
- Danh sách tin công khai vì thế **không bao giờ dày lên được** dù có cào bao nhiêu nguồn.
- Nhưng **110 công ty tuyển trực tiếp được người ở VN** là danh sách thật, hiếm, và đúng thứ kỹ sư cần.

Đây củng cố kết luận Mục 1: sản phẩm nên là **sổ đăng ký công ty**, không phải bảng tin.

---

## 5. Bảy phương án, chấm theo ràng buộc

| # | Mô hình | R1 | R2/R3 | Trần doanh thu | Phán quyết |
|---|---|:--:|:--:|---|---|
| A | Đăng tin trả phí | ❌ | ✓ | 299–600 USD/tin | **Cấm** — tiền mua vị trí |
| B | Bán CV / lead ứng viên | ❌ | ❌ | 100–300 USD/th | **Cấm** — PDPL, phạt 10× |
| C | Affiliate EOR (Deel 1.500 USD/khách) | ✓ | ✓ | Cao | **Hỏng cấu trúc** — xem dưới |
| D | Affiliate cổng thanh toán (Wise/Payoneer) | ✓ | ✓ | ~150 USD/th | Nhỏ nhưng chạy được |
| E | Tài trợ, tách bạch rõ khỏi nội dung | ✓ | ✓ | 200–1.000 USD/th | **Bước đầu đúng** |
| F | Dịch vụ trả phí cho kỹ sư (kiểu Levels.fyi) | ✓ | ✓ | 10–30 USD/lần | Không hợp R6 |
| G | **Dữ liệu B2B — địa lý tuyển dụng** | ✓ | ✓ | 490+ USD/th/khách | **Trần cao nhất** |

### Vì sao C hỏng cấu trúc, không phải "nhỏ"

Deel trả **500 USD/lead đủ điều kiện + 1.000 USD/khách mới**. Nghe rất hấp dẫn. Nhưng:

> **Cookie nằm trên trình duyệt của kỹ sư. Người mua EOR là CÔNG TY.**

Kỹ sư bấm link, ứng tuyển, được nhận. Rồi *công ty* — chưa từng vào trang của ta — mở tài khoản
EOR. Không có đường nào nối hai sự kiện đó. Attribution đứt hoàn toàn.

Ngay cả khi bỏ qua điều đó, phễu vẫn mỏng: 10.000 lượt truy cập/tháng → ~1.500 bấm sang tin gốc
→ ~300 hồ sơ → ~3 người được nhận → ~1 tài khoản EOR mới. **1.500 USD/tháng ở kịch bản lạc quan
nhất, với attribution bằng 0.** Không xây business trên cái này.

### Vì sao G có trần cao nhất

Người mua: **nhà cung cấp EOR** (Deel, Remote, Oyster, Multiplier) làm outbound · công ty gia công
Việt Nam tìm khách · quỹ và hãng nghiên cứu thị trường.

Thị trường này có thật và có giá tham chiếu: PredictLeads bán tín hiệu tuyển dụng từ **490
USD/tháng**; Coresignal bán dataset tin tuyển theo API và file.

**Ta không cạnh tranh bằng độ rộng** — họ có 123 triệu công ty, ta có 3.666. Ta cạnh tranh bằng
**một thuộc tính không ai tính**: *công ty này thật sự tuyển được ở đâu, và câu nào trong tin
chứng minh điều đó.* Họ bán "công ty X đang tuyển". Ta bán "công ty X tuyển được ở 12 nước,
đây là trích dẫn".

---

## 6. Lộ trình đề xuất — ba giai đoạn

### Giai đoạn 0 — không doanh thu (nay → tháng 3)

**Mục tiêu: chứng minh có khán giả. Không kiếm tiền.**

Thứ phát tán được **không phải danh sách tin** — là **phát hiện**:

> *"Đo 34.313 tin remote của 3.666 công ty: 86% khoá theo địa lý. 0/150 ghi rõ tuyển được ở
> Việt Nam. Chỉ 7,2% nói cơ chế trả lương. Đây là 110 công ty tuyển được người ở VN."*

Chưa ai công bố con số này. Đó là mũi nhọn phân phối, và nó **chính là sứ mệnh đang chạy**.

**Cổng:** 30 ngày sau launch, < 100 người dùng duy nhất → dừng lại xem lại toàn bộ.

### Giai đoạn 1 — tiền nhỏ, an toàn sứ mệnh (tháng 3 → 9)

- **E — tài trợ**, tách bạch rõ, nhà cung cấp EOR là người mua tự nhiên. 200–1.000 USD/tháng.
- **D — affiliate cổng thanh toán.** Kỹ sư *chính là* người mua → attribution chạy. ~150 USD/tháng.

Cộng lại ~350–1.150 USD/tháng. **Không đủ sống.** Mục đích không phải sống — là **kiểm xem có ai
quan tâm đủ để trả tiền** trước khi đầu tư vào giai đoạn 2.

### Giai đoạn 2 — dữ liệu B2B (tháng 9 → 18), **chỉ khi A3 xác nhận**

Sản phẩm: **sổ đăng ký địa lý tuyển dụng**, API hoặc file, cập nhật hằng tháng.

Điều kiện vào:
1. **A3 chạy xong** — 10 cuộc nói chuyện với nhà cung cấp EOR / công ty gia công. Hỏi thẳng:
   *"dữ liệu này giải quyết vấn đề gì, trả bao nhiêu?"*
2. Kho ≥ **10.000 công ty** (nay 3.666). Dưới ngưỡng đó không ai mua.
3. Precision giữ ≥ 95% — đây là thứ duy nhất đang bán.

Toán: 10 khách × 490 USD/tháng = **4.900 USD/tháng**. Đó là con số đủ sống. Cũng là con số
**chưa có một mẩu bằng chứng nào**.

---

## 7. Điều tôi có thể sai

**Sai lớn nhất có thể:** giả định nhà cung cấp EOR muốn mua dữ liệu này. Họ có thể tự cào lấy —
rào cản kỹ thuật của ta gần bằng 0. Thứ khó sao chép là **bộ quy tắc đã hiệu chỉnh và 5 đợt
audit**, không phải hạ tầng. Nhưng đó là lợi thế 12 tháng, không phải hào sâu.
**A3 phải chạy trước khi viết một dòng code nào cho giai đoạn 2.**

**Sai thứ hai:** con số 490 USD/tháng lấy từ PredictLeads — quy mô 123 triệu công ty. Giá cho
2.410 công ty gần như chắc chắn thấp hơn nhiều. Coi 490 là **trần**, không phải kỳ vọng.

**Sai thứ ba:** giai đoạn 0 giả định phát hiện "0/150" đủ hấp dẫn để lan. Có thể không. Nó là tin
xấu, và tin xấu về cơ hội việc làm không phải thứ người ta muốn chia sẻ.

**Căng thẳng chưa giải được:** sứ mệnh nói người dùng *nên rời đi*. Mọi mô hình doanh thu hướng
người dùng cuối đều cần họ *ở lại*. Đó là lý do đề xuất nghiêng hẳn về B2B — **không phải vì B2B
kiếm được nhiều hơn, mà vì nó là hướng duy nhất không đòi ta phản bội sứ mệnh.**

---

## 8. Việc kế tiếp, theo thứ tự

| # | Việc | Ai | Chặn cái gì |
|---|---|---|---|
| 1 | **Launch.** Deploy + tên miền + cron | Bạn | Mọi thứ |
| 2 | **A8** — 10 cuộc với kỹ sư Việt thật | Bạn | Biết sản phẩm có đúng vấn đề không |
| 3 | **A3** — 10 cuộc với nhà cung cấp EOR / công ty gia công | Bạn | **Toàn bộ giai đoạn 2** |
| 4 | Mở rộng kho lên 10.000 công ty *(nay 3.666)* | Máy | Giai đoạn 2 |
| 5 | Thêm trang công ty làm trục chính, tin làm phụ | Máy | Trục sản phẩm mới |

**Việc số 3 là việc quan trọng nhất trong tài liệu này, và là việc chưa bao giờ được làm.**
