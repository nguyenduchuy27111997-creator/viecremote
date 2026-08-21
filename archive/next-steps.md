# Sau BRD thì làm gì — kế hoạch 6 tuần & sổ nghiên cứu còn thiếu

**Ngày:** 17/08/2026
**Đi kèm:** [brd-v2.md](brd-v2.md)

---

## 0. Trả lời thẳng

**BRD không phải nút thắt. Viết thêm tài liệu nữa là hình thức trì hoãn có tổ chức.**

Chuỗi tài liệu chuẩn trong ngành là MRD → BRD → PRD → SRD. Nhưng chuỗi đó sinh ra để **đồng bộ nhiều người và xin ngân sách**. Ở đây chỉ có một người và ngân sách 150–300 USD/tháng. Phần lớn giá trị của PRD/SRD trong bối cảnh này bằng không.

Điều BRD v2.0 chưa trả lời được, và không tài liệu nào trả lời được:

| Câu hỏi | Ai trả lời được |
|---|---|
| Bao nhiêu % tin remote thực sự tuyển được ở VN? | **Chỉ có việc đọc tay 200 tin** |
| Có tự động chấm nhãn được không hay phải điều tra tay? | Cùng phép kiểm đó |
| Công ty nước ngoài có coi đây là vấn đề của họ không? | **Chỉ có 15 cuộc trao đổi** |
| Kỹ sư VN có coi đây là vấn đề đáng giải không? | **Chỉ có 3 lần đăng thủ công** |

Không có nghiên cứu công khai nào trả lời câu 1. Đã tìm — không tồn tại. Nghĩa là **không đọc được, chỉ đo được**.

Quy tắc cho 6 tuần tới: **không viết thêm tài liệu chiến lược nào cho tới khi có ba con số của Cổng 0.**

---

## 1. Chuỗi tài liệu — cái nào giữ, cái nào bỏ

| Tài liệu | Vai trò gốc | Ở dự án này |
|---|---|---|
| MRD | Vì sao thị trường này đáng làm | **Bỏ** — Mục 1, 5, 8 của BRD v2 đã bao |
| BRD | Mục tiêu kinh doanh, ràng buộc | **Xong** (v2.0) |
| PRD | Hành vi sản phẩm, luồng người dùng | **Giữ, nhưng viết SAU Cổng 0 và chỉ ~3 trang** |
| SRD | Kiến trúc, phi chức năng | **Bỏ** — Mục 14 BRD đủ cho một người |
| **Rubric Spec** | Định nghĩa chấm nhãn có thể test được | **Thêm — quan trọng hơn PRD** |
| **Sổ đồng ý & xử lý dữ liệu** | Tuân thủ PDPL | **Thêm — bắt buộc trước khi thu dữ liệu lương** |

Hai tài liệu cần viết không nằm trong chuỗi chuẩn: **Rubric Spec** và **Sổ đồng ý**. Đó là dấu hiệu chuỗi chuẩn không khớp với dự án này.

---

## 2. Kế hoạch 6 tuần

### Tuần 1 — Cổng 0.1: tỷ lệ cơ sở

Lấy 200 tin remote từ 4 nguồn khác nhau. Chấm tay theo rubric. Ghi vào spreadsheet: link, công ty, nguồn, nhãn Tier, **phạm vi Tier A (VN hay Global)**, bằng chứng trích dẫn, thời gian chấm.

**Đầu ra — năm số:**
1. **% Tier A-VN** (bằng chứng A-01/A-04/A-05/A-06) — **số quyết định**
2. % Tier A-Global (chỉ A-02/A-03)
3. % Tier A + B
4. % "Không rõ"
5. **Thời gian trung bình chấm một tin**

Số 5 ít ai nghĩ tới nhưng quan trọng ngang bốn số kia: nếu chấm tay mất 4 phút/tin, thì 100 tin/tuần = 6,7 giờ/tuần chỉ để chấm. Đó là toàn bộ quỹ thời gian.

**Phép kiểm thứ sáu, nửa giờ, có thể đắt hơn cả năm số trên:** lấy danh sách tin Tier A vừa chấm, tra chéo với **Real Work From Anywhere** và **TrulyRemoteWork**. Đếm bao nhiêu tin đã có sẵn ở đó.

- Tỷ lệ trùng cao **và** hầu hết Tier A là Global → sản phẩm sẽ là bản sao kém hơn của một thứ miễn phí. Đọc lại BRD Mục 5.1 trước khi viết dòng code nào
- Tier A-VN gần như không trùng → khoảng trống có thật, đúng chỗ đã dự đoán

**Verify:** spreadsheet 200 dòng, mỗi dòng có trích dẫn bằng chứng và cột phạm vi.
**Cổng:** Tier A-VN < 2% → dừng dự án. "Không rõ" > 60% → đổi mô hình (Mục 4.1). Tier A cao nhưng gần như toàn Global → không phải tín hiệu tốt.

### Tuần 2 — Cổng 0.3 (cung) + bắt đầu Cổng 0.2 (cầu)

- Soạn tay 20 tin Tier A tốt nhất từ tuần 1. Đăng vào 3 cộng đồng dev VN. Form đăng ký bản tin.
- Song song: gửi 15 email cho công ty đang đăng tin remote toàn cầu (câu hỏi ở Mục 3 BRD v2). Gửi tuần 2 để có thời gian chờ hồi đáp.

**Verify:** ≥ 50 đăng ký. **Cổng:** < 15 → vấn đề không đủ đau hoặc kênh sai.

### Tuần 3 — Bản tin số 1, làm hoàn toàn bằng tay

Không code. Không website. Một email.

**Verify:** gửi được, tỷ lệ mở đo được.

### Tuần 4 — Bản tin số 2 + tổng kết Cổng 0.2

Đếm: bao nhiêu công ty trả lời rào cản là **pháp lý/trả lương** chứ không phải chất lượng.

**Cổng:** 0/15 quan tâm → bỏ toàn bộ dự báo doanh thu phía cầu, mô hình còn lại là affiliate + tài trợ bản tin.

### Tuần 5 — Quyết định, rồi viết Rubric Spec

Nếu ba cổng đạt: viết **Rubric Spec** — bản duy nhất cần trước khi code.

Nội dung Rubric Spec (~2 trang):
- Danh sách quy tắc chấm, mỗi quy tắc có ID
- Mỗi quy tắc kèm **3 ví dụ dương + 3 ví dụ âm lấy từ 200 tin tuần 1**
- Định dạng đầu ra JSON
- Bộ test: 50 tin đã chấm tay làm ground truth

Bộ test này là thứ khiến "độ chính xác nhãn" trong North Star đo được thật, thay vì là một con số tự chấm.

### Tuần 6 — Pipeline v0

Chỉ ba việc: kéo tin từ ATS API công khai → chấm theo rubric → đẩy vào bản tin.

**Verify:** chạy trên 50 tin ground truth, khớp ≥ 85% với chấm tay. Không đạt → sửa rubric, không sửa model.

---

## 3. Sổ nghiên cứu còn thiếu

### Tier 0 — Chặn tiến độ, phải đo bằng tay

| # | Chủ đề | Vì sao chưa có câu trả lời | Cách làm | Chi phí |
|---|---|---|---|---|
| R1 | Tỷ lệ tin remote thực sự tuyển được ở VN | **Không tồn tại nghiên cứu công khai nào** | Cổng 0.1 | 1 buổi |
| R2 | Tỷ lệ tin có thể chấm tự động vs phải điều tra tay | Quyết định toàn bộ mô hình chi phí | Cùng buổi với R1 | 0 |
| R3 | Chi phí thời gian chấm một tin | Quyết định trần quy mô | Cùng buổi với R1 | 0 |
| R4 | Rào cản thật phía cầu là gì | Không đọc được, phải hỏi | Cổng 0.2 | 1 tuần |

### Tier 1 — Đổi thiết kế, nghiên cứu bàn giấy làm được

| # | Chủ đề | Trạng thái | Việc cần làm |
|---|---|---|---|
| **R5** | **Cách khám phá slug/board token của công ty trên ATS ở quy mô lớn** | **Đã có hướng giải** — Common Crawl CDX, ~95.000 slug | Xem Mục 4.2. Còn lại: chạy thử và đo tỷ lệ slug hợp lệ |
| R6 | Điều khoản sử dụng của từng ATS API công khai | **Đã tra — kết quả là sự im lặng.** Không bên nào công bố điều khoản cho phép/cấm bên thứ ba tổng hợp | Chuyển thành câu hỏi cho luật sư (PRD Q7). Phần giới hạn tốc độ đã có: Greenhouse trả header `X-RateLimit-Limit` và bóp nghẹt bên lạm dụng; Ashby trả 429 + `Retry-After` nhưng **không công bố ngưỡng và không trả header giới hạn**; Lever không có tài liệu công khai |
| R7 | Danh sách quốc gia EOR lấy tự động được không · **chương trình affiliate** | **Cả hai đã trả lời.** Affiliate: Deel 1.500 USD/khách mới. Danh mục quốc gia: **không lấy tự động được** | Deel có cổng developer công khai + sandbox + webhook (duy nhất trong ngành coi API là sản phẩm), nhưng đó là API vận hành nhân sự, **không có endpoint trả về danh sách quốc gia có EOR**. Deel phủ 150+ nước, Remote ~100. Hệ quả: quy tắc A-06 phải lấy từ câu chữ trang tuyển dụng hoặc danh sách duy trì tay |
| R8 | Thuế & cách nhận tiền cho freelancer VN | **Khung đã tra, bốn câu đã soạn** — vẫn phải để kế toán xác nhận | Đã có: Nghị định 253/2026/NĐ-CP (hiệu lực 01/07/2026); cá nhân cư trú **phải kê khai thu nhập trong và ngoài VN, bất kể nơi trả hay nơi nhận**; giảm trừ 15,5 triệu/tháng; khấu trừ theo Hiệp định tránh đánh thuế hai lần. **Chưa có: đường hộ kinh doanh cá thể** (ngưỡng, thuế suất, điều kiện theo văn bản mới) — câu số một. Bốn câu hỏi ở BRD Mục 4.3. Trả tiền cho một buổi tư vấn; ghi lại có ngày và tên người tư vấn |
| ~~R9~~ | ~~Chi phí LLM thật~~ | **Đã trả lời** — 5–35 USD/tháng tuỳ model (PRD 9.2) | Thay bằng **R9b: model nào đạt ngưỡng phát hành?** Quét 3 model trên 50 tin ground truth |
| R10 | Cộng đồng dev VN: ở đâu, bao lớn, luật tự quảng cáo | **Không giải được bằng nghiên cứu bàn giấy** — dữ liệu công khai quá mỏng | Việc thực địa. Bắt đầu từ danh sách nhóm dev do ITviec và TopDev duy trì, rồi tự vào từng nhóm đếm và đọc luật. **Làm trước tuần 2** |

### Tier 2 — Trước khi ra mắt công khai

| # | Chủ đề | Việc cần làm |
|---|---|---|
| ~~R11~~ | ~~Phạm vi rà soát pháp lý~~ **Đã soạn xong: [legal-brief.md](legal-brief.md)** — 4 câu Google, 7 câu PDPL, 4 câu kế toán, kèm trích dẫn nguyên văn văn bản, thứ tự ưu tiên, danh sách "điều không cần hỏi", và ba mặc định an toàn. Còn lại: đặt lịch và trả tiền. **Câu đắt nhất: dữ liệu lương có phải dữ liệu nhạy cảm không** — quyết định toàn bộ gánh nặng tuân thủ |
| ~~R12~~ | ~~Mô hình kinh doanh Arc.dev~~ **Đã trả lời:** 25–30% trên lương người được tuyển (Arc Connect, dòng chính), 15–20% phí tuyển dụng, 13–22% phí mentor. 3,8 triệu USD ARR, đã có lãi, 750k dev. **Là đối thủ, không phải đối tác** — chính khoản phí đó là thứ JTBD phía cầu muốn tránh |
| **R15** | **(mới) Nhóm 2 có thể là kênh không?** Real Work From Anywhere, TrulyRemoteWork, Truly Remote, We Are Distributed | Họ đã lọc sẵn tập "worldwide" — vừa là nguồn đầu vào chất lượng cao, vừa là nơi đăng chéo. Hỏi thẳng: có nhận nội dung bổ sung về khả năng tuyển theo quốc gia không. **Làm sau Cổng 0.1**, khi đã có số liệu để trao đổi |
| R13 | Định giá đăng tin | Chỉ nghiên cứu sau khi Cổng 0.2 cho tín hiệu dương. Trước đó là lãng phí |
| R14 | Công cụ bản tin & khả năng vào inbox | **Yêu cầu đã rõ** (PRD FR-6.3/6.4/6.7): SPF · DKIM · PTR · TLS · DMARC `p=none` + alignment · `List-Unsubscribe` + `List-Unsubscribe-Post` (RFC 8058), chạy không cần đăng nhập, xử lý ≤ 2 ngày · theo dõi tỷ lệ spam, mục tiêu < 0,10%. Còn lại: chọn nền tảng đáp ứng đủ. Cần trước tuần 3 |

### Tier 3 — Đừng nghiên cứu bây giờ

Định giá chi tiết, thiết kế thương hiệu, mở rộng vai trò/ngôn ngữ, tính năng nền tảng hai chiều, so sánh framework. Tất cả đều phụ thuộc vào kết quả Tier 0. Nghiên cứu bây giờ là nghiên cứu cho một dự án có thể không tồn tại sau tuần 1.

---

## 4. Hai phát hiện mới từ nghiên cứu lần này

### 4.1 Sáu nền tảng ATS có API việc làm công khai, không cần xác thực

Ashby, Greenhouse, Lever, Recruitee, Workable, Personio đều expose endpoint công khai. Ví dụ Ashby:

```
GET https://api.ashbyhq.com/posting-api/job-board/{clientname}?includeCompensation=true
```

**Vì sao điều này quan trọng hơn nó có vẻ:**

1. **Giảm mạnh rủi ro điều khoản sử dụng — nhưng không xoá** (BRD Mục 6.3). Đây là endpoint không xác thực, phục vụ dữ liệu công ty **đã chủ động chọn công khai** — khác hẳn scrape. Nhưng kiểm chứng vòng 2 cho thấy **không nhà cung cấp nào trong bốn bên công bố điều khoản cho phép rõ ràng việc bên thứ ba tổng hợp lại.** "Không bị chặn" ≠ "được cho phép". Xem BRD Mục 6.3 và PRD Q7.
2. **Giải bài toán tin zombie** (BRD Mục 6.1, FR-9.1). Tin biến mất khỏi feed = đã đóng. Không cần đoán. Rủi ro manual action của Google giảm mạnh.
3. **Cho dữ liệu sạch hơn** — có trường lương có cấu trúc, có địa điểm có cấu trúc. Chấm rubric dễ hơn nhiều so với đọc HTML.
4. **Có thể đủ để coi là "được ủy quyền"** cho Lớp 1 trong kiến trúc hai lớp — **cần R11 xác nhận với luật sư, không tự kết luận.**

**Hệ quả:** ưu tiên nguồn ở BRD Mục 6.3 nên đổi — ATS API công khai không chỉ là "bậc 1", nó nên là **nguồn gần như duy nhất** cho v1. Bỏ scraping khỏi phạm vi v1 hoàn toàn.

### 4.2 Nhưng có một bài toán chưa giải: khám phá slug

API công khai cần biết **slug của công ty** (`{clientname}`). Không có endpoint nào liệt kê tất cả công ty dùng Ashby.

**Đây là khoảng trống nghiên cứu lớn nhất còn lại (R5).** Vài hướng cần thử, chưa hướng nào được kiểm chứng:
- Trích slug từ URL nộp hồ sơ trên các board tổng hợp (RemoteOK, WWR, HN Who's Hiring) — tin trỏ về `jobs.ashbyhq.com/xyz` là lộ slug
- Bộ dữ liệu công khai đã có sẵn (một số dự án mã nguồn mở duy trì danh sách này)
- Tìm kiếm theo mẫu URL
- Xây dần: mỗi tin thấy được sinh ra một slug mới cho lần chạy sau

**Đây là bài toán kỹ thuật cốt lõi của v1.** Nếu chỉ tiếp cận được 200 công ty, sản phẩm không có nguồn cung. Nếu tiếp cận được 5.000, có thừa.

**Đề xuất:** dành nửa ngày trong tuần 1 để thử hướng đầu tiên trên 50 tin. Nếu trích được slug từ ≥ 40% tin, hướng này đủ tốt.

### 4.3 GEO: dữ liệu gốc là thứ được trích dẫn, danh sách tin thì không

Nghiên cứu về Generative Engine Optimization 2026 cho ba điểm áp dụng trực tiếp:

1. **Nội dung cập nhật trong 30 ngày được AI trích dẫn nhiều hơn hẳn nội dung cũ.** → nội dung bản địa (thuế, EOR, đàm phán lương) phải có lịch cập nhật, không phải viết một lần.
2. **Nghiên cứu gốc và dữ liệu độc quyền là thứ thu hút trích dẫn** — vì AI không có lý do gì để trích một trang giống mười trang khác.
3. **Google nói rõ: tối ưu cho AI features "vẫn là SEO"**, và loại trừ các mẹo như `llms.txt`, viết lại riêng cho AI, structured data đặc biệt cho AI. Không có đường tắt.
4. Perplexity cho vòng phản hồi nhanh nhất (vài tuần); ChatGPT chậm hơn vì dựa vào chỉ mục Bing.

**Điểm nối quan trọng:** con số của Cổng 0.1 — *"trong 200 tin remote, X% thực sự tuyển được ở Việt Nam"* — **chính là nghiên cứu gốc mà không ai có.**

Nghĩa là Cổng 0.1 sinh ra ba thứ cùng lúc:
- Quyết định đi/dừng
- Ground truth để test rubric
- **Bài nội dung đầu tiên có khả năng được AI trích dẫn**

Đó là lý do mạnh nhất để làm nó ngay tuần này, kể cả nếu kết quả là dừng dự án — dữ liệu vẫn có giá trị công bố.

**Cách kiểm A4 giờ đã có phương pháp cụ thể** — xem BRD Mục 16.1.1: bộ 10–15 prompt cố định × 3 engine (ChatGPT, Perplexity, Google AI Overviews) × đo tay hằng tháng, 30 phút. Ghi *nhắc đến* và *trích dẫn* riêng; cột quan trọng nhất là **ai được trích thay ta**. Đo hằng tháng chứ không hằng quý — Perplexity đánh trọng số độ mới rất cao, mẫu trích dẫn đổi trong 48 giờ.

**Thêm một lý do độc lập để giữ nội dung hiện hành:** luật thuế VN đổi hai lần trong 2026 (Nghị định 253/2026/NĐ-CP hiệu lực 01/07/2026). Nội dung cũ không chỉ mất trích dẫn — nó **sai số liệu**. Con hào nội dung là guồng quay, không phải tài sản (BRD Mục 10.1).

---

## 5. Ba điều dễ làm sai trong 6 tuần tới

1. **Viết PRD trước Cổng 0.** Cảm giác như đang tiến bộ. Thực tế là đặc tả một sản phẩm chưa biết có nên tồn tại không.
2. **Code pipeline trước khi có ground truth.** Không có 50 tin chấm tay, "độ chính xác 90%" là con số tự chấm, vô nghĩa.
3. **Bỏ qua R10 (bản đồ cộng đồng) và đăng bừa.** Bị ban khỏi nhóm Facebook lớn nhất trong tuần 2 là mất kênh chính vĩnh viễn. Đọc luật nhóm, hỏi admin trước.

---

## 6. Một câu để dán lên màn hình

> Sáu tuần tới không sinh ra sản phẩm. Nó sinh ra **bốn con số**: tỷ lệ Tier A, tỷ lệ "Không rõ", số công ty nói rào cản là pháp lý, số người đăng ký bản tin.
>
> Bốn con số đó quyết định 12 tháng sau. Mọi thứ khác làm bây giờ đều là đoán.
