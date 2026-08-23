# Cấu trúc hợp pháp — cửa nào đóng, cửa nào mở

**Ngày:** 23/08/2026 · Tiếp theo [legal-research.md](legal-research.md), cùng bộ nguồn toàn văn.

---

## 0. Ranh giới

Hai việc khác nhau, hay bị gộp làm một:

| Chọn cấu trúc để **không rơi vào** diện điều chỉnh | Làm hoạt động bị điều chỉnh rồi **che** |
|---|---|
| Hợp pháp. Mọi doanh nghiệp đều làm | 10× khoản thu, sàn 3 tỷ, có thể hình sự |
| Đổi **mô hình kinh doanh** để phù hợp | Giữ nguyên mô hình, đổi **cách gọi tên** |
| Chịu được kiểm tra | Sập ngay lần kiểm tra đầu |

Tài liệu này chỉ làm cột trái. Cột phải không nghiên cứu — với chế tài tính theo bội số doanh
thu, nó không phải lựa chọn kinh tế kể cả khi bỏ qua chuyện đúng sai.

**Kết luận sớm:** ba cửa "lách" hiển nhiên nhất đều đã bị luật bịt sẵn — bịt bằng câu chữ rõ
ràng, không phải bằng suy diễn. Nhưng có **bốn cấu trúc thật sự mở**, và cái rẻ nhất là nhận ra
chi phí tuân thủ **thấp hơn nhiều** so với con số đang bị hiểu nhầm.

---

## 1. Ba cửa đã đóng — đừng mất thời gian

### 1.1 "Đặt pháp nhân ở nước ngoài" — ĐÓNG

Ý tưởng đầu tiên ai cũng nghĩ tới. **NĐ 356/2025 Điều 2 khoản 3** bịt thẳng:

> **3.** Cơ quan, tổ chức, cá nhân **nước ngoài trực tiếp tham gia hoặc có liên quan** đến hoạt
> động xử lý dữ liệu cá nhân của **công dân Việt Nam** […]

Công ty Singapore xử lý hồ sơ kỹ sư Việt vẫn thuộc phạm vi Luật BVDLCN. Toàn bộ nghĩa vụ —
đồng ý theo từng lần chuyển giao, hồ sơ xuyên biên giới, chế tài — đi theo **dữ liệu**, không đi
theo **nơi đăng ký kinh doanh**.

Về dịch vụ việc làm thì còn tệ hơn: doanh nghiệp nước ngoài **không thể** xin Giấy phép (NĐ 352
Điều 15 yêu cầu doanh nghiệp Việt Nam), nên không phải "được miễn" mà là **không được phép**.

### 1.2 "Chỉ là nền tảng công nghệ, không giới thiệu ai" — ĐÓNG

**Luật Việc làm 74/2025 Điều 27 khoản 4**, nguyên văn:

> **4.** Hoạt động kinh doanh dịch vụ việc làm **theo phương thức thương mại điện tử** chỉ được
> thực hiện bởi **doanh nghiệp có giấy phép** hoạt động dịch vụ việc làm khi bảo đảm các điều
> kiện theo quy định của pháp luật về thương mại điện tử.

Nhà lập pháp đã nghĩ tới nền tảng online và viết riêng một khoản cho nó. "Chúng tôi chỉ là phần
mềm" không phải lập luận mới — nó là trường hợp được nêu đích danh.

### 1.3 "Miễn phí nên không phải kinh doanh" — MỎNG, không dựa vào được

Có cơ sở: Điều 27.4 nói *"hoạt động **kinh doanh** dịch vụ việc làm"*, và Điều 28.4 giả định
doanh nghiệp *"tự định giá và niêm yết giá dịch vụ"*. Miễn phí hoàn toàn thì yếu tố kinh doanh mờ.

Nhưng cấu trúc này chết đúng vào ngày có doanh thu — mà doanh thu là mục tiêu. Dùng được như
**giai đoạn**, không dùng được như **mô hình**.

---

## 2. Một phát hiện ngược, phải nói

**Điều 27 khoản 1 Luật Việc làm** định nghĩa dịch vụ việc làm gồm **ba** nhóm:

> **1.** Dịch vụ việc làm bao gồm tư vấn, giới thiệu việc làm; cung ứng và giới thiệu lao động
> cho người sử dụng lao động; **thu thập, phân tích, lưu trữ, cung cấp thông tin về thị trường
> lao động**.

Nhóm thứ ba mô tả **L1** khá sát — L1 thu thập tin tuyển dụng, phân tích, lưu trữ, cung cấp
thông tin về thị trường lao động.

L1 hiện tại nhiều khả năng **ngoài phạm vi**, vì Điều 27.4 và Điều 28 đều gắn với *kinh doanh*
và *định giá dịch vụ*, còn L1 miễn phí, không thu phí ai, không có hợp đồng dịch vụ với ai.

**Nhưng:** ngày L1 có doanh thu trực tiếp từ chính dữ liệu đó — bán API, bán báo cáo thị
trường lao động Việt Nam, thu phí truy cập — thì nhóm thứ ba kích hoạt. Đây là ràng buộc chưa
từng ghi ở đâu trong tài liệu dự án.

> **Hệ quả:** kế hoạch "L1 miễn phí, sau này bán API" có rủi ro pháp lý mà kế hoạch "L1 miễn phí,
> kiếm tiền từ quảng cáo/tài trợ" không có. Ghi vào [prd.md](prd.md) trước khi ai đó build API bán.

---

## 3. Bốn cửa còn mở

### Đ1 — Xin giấy phép. Rẻ hơn bạn nghĩ.

Con số 300 triệu đang bị hiểu sai. **NĐ 352 Điều 16** nguyên văn:

- khoản 1: *"Lãi suất tiền ký quỹ do doanh nghiệp và ngân hàng nhận ký quỹ thỏa thuận […]"* —
  **có lãi**, như tiền gửi.
- khoản 2: chỉ bị dùng khi doanh nghiệp **không thực hiện nghĩa vụ** và cơ quan có thẩm quyền
  yêu cầu.
- khoản 3: **rút được** khi không được cấp phép, bị thu hồi, hết hạn, hoặc chuyển ngân hàng khác.

**Ký quỹ không phải chi phí. Là tiền bị khoá, có lãi, lấy lại được.** Chi phí thật của Đ1:

| Khoản | Bản chất |
|---|---|
| 300 triệu ký quỹ | **Khoá**, có lãi, hoàn lại |
| Thuê trụ sở ≥24 tháng | Chi phí thật, nhưng cần cho mọi phương án có pháp nhân |
| Người đại diện: đại học **hoặc** ≥24 tháng kinh nghiệm dịch vụ việc làm | Không tốn tiền nếu bạn đủ điều kiện |
| Hồ sơ xin phép | Thời gian |

Nếu vốn ~350 triệu khả thi, **đây là phương án đơn giản nhất** — không phải lách gì cả, và giải
quyết luôn câu 4.2 (dịch vụ xử lý DLCN) vì mã ngành khớp theo NĐ 356 Điều 7.3.b.

### Đ2 — Hợp tác với doanh nghiệp đã có giấy phép

Nền tảng bán **phần mềm**; đối tác có giấy phép thực hiện **giới thiệu** và đứng tên nghĩa vụ.
Phổ biến trong HR-tech, hợp pháp, không phải vỏ bọc — miễn là phân vai thật.

- **Vốn:** gần bằng 0
- **Đổi lại:** chia doanh thu, phụ thuộc đối tác
- **Bắt buộc:** phân vai bên kiểm soát / bên xử lý / bên thứ ba theo **NĐ 356 Điều 7.3.đ**, và
  thoả thuận chuyển giao đủ 7 nội dung theo **Điều 7.1**

**Cảnh báo:** nếu hợp đồng ghi đối tác giới thiệu nhưng thực tế nền tảng quyết định ghép ai với
ai và thu tiền, đây là cột phải của Mục 0. Phân vai phải khớp việc làm thật.

### Đ3 — Chỉ phục vụ phía cầu. An toàn hơn nhiều, nhưng KHÔNG ngoài vòng.

> **Sửa lỗi 23/08 — bản trước nói quá chắc.** Tôi đã viết Đ3 "ngoài cả hai chế độ" và "không
> cần giấy phép nào". Đọc kỹ **Điều 20 khoản 1 Luật Việc làm** thì không đứng vững:
>
> > **1.** Thông tin thị trường lao động bao gồm:
> > **a)** Thông tin về cung lao động, **cầu lao động, kết nối cung - cầu lao động**;
> > […] **c)** Thông tin về xu hướng tìm kiếm việc làm và **nhu cầu sử dụng lao động**;
> > **d)** Thông tin về **tiền lương và thu nhập** của người lao động.
>
> Báo cáo Đ3 bán đúng (a), (c) và (d). Và Điều 27.1(c) xếp *"thu thập, phân tích, lưu trữ,
> cung cấp thông tin về thị trường lao động"* vào **dịch vụ việc làm** — mà Điều 27.4 buộc
> hoạt động **kinh doanh** dịch vụ việc làm bằng thương mại điện tử phải có Giấy phép.
>
> **Lập luận ngược, thật chứ không phải bào chữa:** Điều 19–21 nằm trong chương về *hệ thống
> thông tin thị trường lao động của Nhà nước* — "quản lý tập trung, thống nhất trên phạm vi cả
> nước", kết nối cơ sở dữ liệu quốc gia, và Điều 20.2 buộc các Bộ nộp dữ liệu về Bộ Nội vụ.
> Chương đó điều chỉnh **hệ thống nhà nước**, không phải nghiên cứu tư nhân. Thêm nữa Đ3 bán
> **chính sách tuyển dụng của công ty nước ngoài, cho công ty nước ngoài** — không phải dữ liệu
> lao động Việt Nam bán cho thị trường Việt Nam.
>
> **Xếp lại thật:** Đ3 **miễn phí** thì gần như chắc chắn ngoài vòng (thiếu yếu tố *kinh doanh*).
> Đ3 **có thu tiền** thì nằm ở vùng xám, và là câu hỏi luật sư **thứ ba**. Rủi ro thấp hơn L2
> nhiều — chế tài vi phạm điều kiện kinh doanh khác hẳn 10× doanh thu của mua bán dữ liệu — nhưng
> không bằng không.

**Không chạm dữ liệu kỹ sư. Không giới thiệu ai.** Bán cho công ty nước ngoài đúng thứ L1 đã
biết: nước nào tuyển được, rào cản gì, mặt bằng lương, so sánh EOR, cách vào thị trường Việt Nam.

- Không có dữ liệu cá nhân ⇒ **Luật 91/2025 không áp dụng**
- Không tư vấn/giới thiệu cho **người lao động**, không cung ứng lao động ⇒ ngoài Điều 27.1
  nhóm 1 và 2
- Không phải thông tin thị trường lao động **Việt Nam bán cho người Việt** ⇒ tránh nhóm 3

Sản phẩm nghiên cứu, khách hàng doanh nghiệp nước ngoài, thanh toán quốc tế. **Không cần giấy
phép nào.** Và nó kiểm chứng đúng giả thuyết cốt lõi — công ty nước ngoài **có** trả tiền để vào
được nguồn kỹ sư Việt hay không — trước khi bỏ một đồng vào tuân thủ.

### Đ4 — Kỹ sư tự gửi. Có tác dụng, nhưng chỉ một nửa.

**Luật Điều 20.6.c** miễn hồ sơ xuyên biên giới khi *"chủ thể dữ liệu cá nhân tự chuyển dữ liệu
cá nhân của mình"*. **NĐ 356 Điều 7.6** miễn nghĩa vụ chuyển giao khi cung cấp *"dựa trên từng
yêu cầu cụ thể của chủ thể dữ liệu"*.

Giảm được gánh nặng **bảo vệ dữ liệu**. **Không** giảm gánh nặng **dịch vụ việc làm** — nếu nền
tảng vẫn ghép người và thu phí thì vẫn là giới thiệu việc làm theo Điều 27.1.

Dùng Đ4 **kèm** Đ1 hoặc Đ2, không dùng thay.

---

## 4. Khuyến nghị

**Đ3 trước, rồi Đ2 hoặc Đ1.**

| Giai đoạn | Làm gì | Vốn tuân thủ |
|---|---|---|
| Bây giờ | L1 miễn phí (giữ miễn phí) + **Đ3** bán nghiên cứu cho công ty nước ngoài | 0 |
| Có khách trả tiền đầu tiên | Rà soát luật sư 2 câu ở [legal-research.md](legal-research.md) Mục 7 | Phí tư vấn |
| Có nhu cầu ghép người thật | **Đ2** nếu muốn nhanh, **Đ1** nếu muốn tự chủ | 0 / ~350 triệu |

Lý do xếp Đ3 trước: nó **có doanh thu mà không chạm quy định nào**, và trả lời câu hỏi kinh
doanh quan trọng hơn mọi câu hỏi pháp lý — *có ai trả tiền không*. Bỏ 300 triệu ký quỹ trước khi
biết câu trả lời đó là đặt cược sai thứ tự.

Và nếu đến bước ghép người: **Đ1 không phải thất bại của việc lách.** 300 triệu có lãi và lấy
lại được, người đại diện chỉ cần bằng đại học. Rào cản thật thấp hơn hẳn con số nghe thấy.

---

## 5. Giới hạn

- Phân tích này **chưa đọc** pháp luật về **thương mại điện tử** (NĐ về TMĐT) mà Điều 27.4 dẫn
  chiếu, và **Luật Người lao động Việt Nam đi làm việc ở nước ngoài** — văn bản quyết định câu
  hỏi "remote có phải việc làm ở nước ngoài" ở [legal-research.md](legal-research.md) Mục 4.1.
- Đ3 chưa kiểm tra nghĩa vụ **thuế nhà thầu / thuế xuất khẩu dịch vụ** khi bán cho khách nước
  ngoài. Câu hỏi cho kế toán, không phải luật sư.
- Ranh giới Đ2 giữa "phân vai thật" và "vỏ bọc" là chỗ **phải** có luật sư trước khi ký.
- Tôi không phải luật sư. Đây là bản đồ để hỏi đúng câu.
