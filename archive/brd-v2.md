# BRD v2.0 — Nền tảng việc làm remote quốc tế cho kỹ sư Việt Nam

**Phiên bản:** 2.5 — **ĐÃ BỊ THAY THẾ MỘT PHẦN bởi [pivot-v3.md](pivot-v3.md)** (Mục 1.1, 1.2, 2, 12.1, 16.1 không còn hiệu lực sau kết quả Cổng 0.1)
**Phiên bản gốc:** 2.5 — v2.0 (viết lại sau adversarial review) + nghiên cứu sâu vòng 2–6. Thay thế v1.0.
**Ngày:** 17/08/2026
**Chủ sở hữu:** Huy
**Trạng thái:** Chưa kiểm chứng thị trường. Mục 3 (Cổng 0) quyết định tài liệu này có giá trị hay không.

> **Cảnh báo đọc:** v1.0 có một mâu thuẫn ở ngay câu định vị (ví dụ "47/1000 tin" = 4,7%, thấp hơn chính ngưỡng dừng 5% của nó), một tầng rủi ro pháp lý bị bỏ trống hoàn toàn, và bảng RICE sắp xếp sai. v2.0 sửa những chỗ đó. Mục 15 liệt kê đầy đủ những gì đã đổi và vì sao.

---

## Mục lục

0. Tóm tắt cho người ra quyết định
1. Định vị chiến lược
2. Định nghĩa vận hành: "tin đủ điều kiện" nghĩa là gì
3. Cổng 0 — ba phép kiểm phải làm trước khi viết code
4. Rào cản thật: đây là bài toán pháp nhân, không phải bài toán múi giờ
5. Bối cảnh cạnh tranh
6. Ràng buộc pháp lý & tuân thủ (mục hoàn toàn mới)
7. Lean Canvas
8. Jobs-to-be-Done
9. Cold Start Theory — lộ trình mạng lưới
10. Phân tích con hào
11. Kinh tế đơn vị & mô hình doanh thu
12. Khung đo lường
13. Yêu cầu sản phẩm
14. Kiến trúc
15. Lộ trình ưu tiên
16. Sổ giả định & tiêu chí dừng
17. Pre-mortem
18. Quyết định cần chốt trước khi bắt đầu
19. Delta v1.0 → v2.0
20. Phụ lục

---

## 0. Tóm tắt cho người ra quyết định

Ý tưởng cốt lõi vẫn đúng: **cạnh tranh ở tỷ lệ tin đáng nộp, không ở số lượng tin.** Nghiên cứu không bác bỏ điều đó.

Nhưng nghiên cứu làm lộ ra bốn điều v1.0 chưa tính:

1. **"Đủ điều kiện" chủ yếu là câu hỏi pháp nhân, không phải múi giờ.** Công ty nước ngoài không thuê được người Việt vì họ không có pháp nhân ở VN, chứ không phải vì lệch giờ. Đường thoát là EOR (300–600 USD/người/tháng) hoặc hợp đồng nhà thầu. Đây vừa là rào cản lớn nhất, vừa là **tín hiệu làm giàu dữ liệu tốt nhất** — và v1.0 gần như không nhắc tới.

2. **Google cấm đăng tin mà không có ủy quyền từ công ty tuyển dụng.** Chính sách nội dung của JobPosting structured data yêu cầu điều này, và tin hết hạn không gỡ có thể bị manual action. Toàn bộ chiến lược SEO của v1.0 dựng trên tin scrape → nằm trên rìa chính sách. **Cách xử lý biến ràng buộc này thành mô hình kinh doanh** (Mục 6.1).

3. **Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 có hiệu lực 01/01/2026 cấm mua bán dữ liệu cá nhân**, phạt tới 10 lần doanh thu thu được từ hành vi đó. Dòng doanh thu "quyền truy cập ứng viên" trong v1.0 phải bỏ hoặc thiết kế lại thành mô hình giới thiệu có đồng ý. Dữ liệu lương do cộng đồng đóng góp cũng là dữ liệu cá nhân, cần đồng ý rõ ràng theo từng mục đích.

4. **Traffic tìm kiếm đã suy giảm, không phải "có thể suy giảm".** Google gửi traffic tới publisher giảm ~33% toàn cầu trong năm tính đến 11/2025 (Mỹ −38%); CTR tự nhiên trên truy vấn có AI Overview giảm ~61–65%. A4 trong v1.0 xếp "rủi ro trung bình" — thực tế là rủi ro cao và đã hiện thực hoá một phần.

**Kết luận:** dự án vẫn đáng thử, nhưng với thứ tự khác. Kênh chính không nên là SEO thuần; kênh chính nên là **bản tin + cộng đồng**, SEO là kênh bồi. Và ba phép kiểm ở Mục 3 phải xong trước khi viết dòng code nào.

---

## 1. Định vị chiến lược

### 1.1 Câu định vị

> Với **kỹ sư phần mềm Việt Nam muốn làm remote cho công ty nước ngoài** — những người đang nộp hồ sơ mù vào các board quốc tế và không biết tin nào thực sự có thể thuê người ở Việt Nam —
> **[Tên sản phẩm]** là nguồn tin việc làm đã kiểm chứng khả năng tuyển
> **khác với** RemoteOK, WeWorkRemotely, Arc.dev, Himalayas — **và khác cả với các board "work from anywhere" tuyển chọn tay như Real Work From Anywhere hay TrulyRemoteWork, những bên đã trả lời tốt câu hỏi "tin này có mở toàn cầu không"** — ở chỗ mỗi tin đều trả lời bốn câu hỏi có bằng chứng: (a) công ty này có **cơ chế pháp lý** nào để trả lương cho người ở Việt Nam, (b) yêu cầu trùng múi giờ bao nhiêu và neo vào múi nào, (c) hình thức hợp đồng gì, (d) đã có người Việt được nhận ở đây chưa.
>
> **Ranh giới trung thực:** ba trong bốn câu trên chưa ai trả lời. Câu "có mở toàn cầu không" thì đã có người trả lời, miễn phí, hằng tuần (Mục 5.1). Định vị này đứng hay đổ ở ba câu còn lại.
> **Bằng chứng:** mỗi trường dữ liệu kèm trích dẫn nguồn và ngày; không có căn cứ thì hiển thị "Không rõ" chứ không đoán.

### 1.2 Chỉ số bán hàng — đã sửa

v1.0 viết: *"1.000 tin remote hôm nay, 47 tin thực sự nhận người Việt."* — con số này (4,7%) **thấp hơn chính ngưỡng dừng 5%** mà v1.0 tự đặt ra. Không được dùng số minh hoạ trước khi đo.

Câu đúng cho tới khi Cổng 0 chạy xong:

> *"Tuần này có N tin remote. X tin có bằng chứng cụ thể là tuyển được người ở Việt Nam. Đây là X tin đó, kèm bằng chứng."*

X là số đo được, không phải số minh hoạ.

### 1.3 Điều KHÔNG phải định vị

Không phải "board việc làm remote". Không cạnh tranh ở **số lượng tin**, cạnh tranh ở **mật độ tin đáng nộp và độ tin của nhãn**.

Cũng không phải "board việc làm cho người Việt". Đó là sân của ITviec/TopDev/VietnamWorks và họ thắng ở đó. Sân này là **giao của hai tập**: việc quốc tế × tuyển được ở VN.

---

## 2. Định nghĩa vận hành: "tin đủ điều kiện" nghĩa là gì

**Đây là mục quan trọng nhất về mặt vận hành, và v1.0 hoàn toàn không có.** North Star Metric, tiêu chí dừng, cờ chất lượng — tất cả đều tham chiếu tới "tin đủ điều kiện" mà không định nghĩa. Không có mục này thì mọi con số trong tài liệu đều vô nghĩa, và chỉ số có thể bị làm đẹp chỉ bằng cách nới định nghĩa.

### 2.1 Năm nhãn bắt buộc trên mỗi tin

| Nhãn | Giá trị | Nguồn bằng chứng |
|---|---|---|
| **Khả năng tuyển VN** | Tier A / Tier B / Không rõ / Không | Bắt buộc trích dẫn |
| **Cơ chế hợp đồng** | EOR / Nhà thầu (B2B) / Pháp nhân VN / Qua agency / Không rõ | Bắt buộc trích dẫn |
| **Yêu cầu múi giờ** | Số giờ trùng + múi neo (vd: "4h trùng, neo CET") | Trích từ mô tả gốc |
| **Công bố lương** | Có dải / Ước lượng / Không công bố | Trích từ mô tả gốc |
| **Tuổi bằng chứng** | Ngày của tín hiệu mới nhất | Tự động |

### 2.2 Thang bằng chứng

**Tier A — bằng chứng cứng (tính vào North Star):**
- Công ty có Việt Nam trong danh sách quốc gia tuyển của họ trên trang tuyển dụng/EOR
- Mô tả tin ghi rõ "worldwide", "anywhere", "any country", hoặc liệt kê VN/APAC
- Công ty có pháp nhân hoặc văn phòng tại VN
- Có bản ghi cộng đồng xác nhận người Việt đã được nhận trong 18 tháng gần nhất

**Tier B — bằng chứng mềm (tính vào North Star, nhưng đếm riêng):**
- Ngôn ngữ "contractor welcome", "we hire globally as contractors", "async-first"
- Công ty đã có nhân sự công khai ở múi giờ GMT+5 đến GMT+9
- Nhà tuyển dụng dùng nền tảng EOR có hỗ trợ VN

**Không rõ:** không có tín hiệu dương và cũng không có tín hiệu loại trừ. **Hiển thị, nhưng KHÔNG tính vào North Star.**

**Loại trừ tự động (Không):**
- "US only", "must be authorized to work in [nước]", "W-2 required", danh sách bang/tiểu bang
- "within N hours of [múi giờ Mỹ]" với N khiến GMT+7 không thể trùng
- Yêu cầu security clearance, quốc tịch, hoặc giấy phép lao động sở tại
- Tin qua agency không tiết lộ công ty cuối

### 2.3 Chống làm đẹp chỉ số

Định nghĩa này **được khoá phiên bản**. Mọi thay đổi rubric phải:
1. Ghi vào changelog có ngày
2. Chạy lại trên 100 tin của tháng trước và báo cáo chênh lệch
3. Không được thay đổi trong tháng đang đo

Không có ba điều này, North Star tự gian lận được — đây là lỗ hổng lớn nhất của v1.0, nơi nó khẳng định chỉ số "không thể gian lận bằng cách scrape thêm" nhưng quên rằng nó gian lận được bằng cách nới rubric.

---

## 3. Cổng 0 — ba phép kiểm phải làm trước khi viết code

Không có phép kiểm nào trong đây cần lập trình. Tổng chi phí: khoảng 3–4 buổi + 1 tuần chờ hồi đáp.

### Cổng 0.1 — Tỷ lệ cơ sở (thay A1)

**Việc làm:** lấy 200 tin remote thật từ 4 nguồn khác nhau (RemoteOK, WWR, Hacker News Who's Hiring, một ATS board như Greenhouse). Chấm tay theo rubric Mục 2.

**Ghi lại bốn số, không phải một:**
- **% Tier A-VN** — bằng chứng riêng cho Việt Nam (A-01/A-04/A-05/A-06). **Đây là số quyết định**
- % Tier A-Global — chỉ có ngôn ngữ toàn cầu (A-02/A-03). Đã có miễn phí ở nơi khác (Mục 5.1)
- % Tier A + B
- % có thể quyết được (không rơi vào "Không rõ") — đo được tính khả thi của việc tự động hoá

**Ngưỡng — keo vào Tier A-VN, không phải Tier A tổng:**

| Kết quả | Hành động |
|---|---|
| Tier A-VN ≥ 5% | Tiếp tục theo kế hoạch |
| Tier A-VN 2–5% | Tiếp tục, nhưng thu hẹp ngách và hạ kỳ vọng doanh thu về kịch bản Xấu |
| **Tier A-VN < 2%** | **Dừng.** Không có gì để xây mà chưa tồn tại |
| Tier A tổng cao nhưng **gần như toàn Tier A-Global** | **Không phải tín hiệu tốt.** Nghĩa là sản phẩm sẽ là bản sao của Real Work From Anywhere. Đọc lại Mục 5.1 trước khi tiếp tục |
| "Không rõ" > 60% | Dừng phần tự động hoá. Bài toán không phải lọc mà là **điều tra** — mô hình chi phí hoàn toàn khác |

*(Ngưỡng dừng hạ từ 4% xuống 2% vì mẫu số đổi: 2% Tier A-VN là hàng hiếm thật, còn 4% Tier A tổng có thể gần như toàn bộ là thứ đã miễn phí.)*

*Lưu ý phương pháp: không có nghiên cứu công khai nào đo được tỷ lệ tin remote thực sự tuyển toàn cầu. Nghĩa là số này chưa ai biết — điều đó vừa là rủi ro (có thể rất thấp) vừa là cơ hội (chưa ai làm rõ).*

### Cổng 0.2 — Nhu cầu phía cầu (thay A3, đẩy lên trước)

v1.0 xếp phép kiểm này ở tháng 4. Sai thứ tự: pre-mortem của chính v1.0 xếp "có traffic nhưng không ai trả tiền" là xác suất cao. Kiểm trước, không kiểm sau.

**Việc làm:** liên hệ 15 công ty đang đăng tin remote toàn cầu. Hỏi ba câu:
1. Anh/chị đã từng thuê ai ở Đông Nam Á chưa? Qua cơ chế nào?
2. Nếu có một danh sách 30 kỹ sư Việt đã sàng lọc, mức phí nào là hợp lý?
3. Rào cản thật là gì — chất lượng, múi giờ, hay pháp lý/trả lương?

**Ngưỡng:** ≥ 3/15 trả lời rằng rào cản là **pháp lý/trả lương** (chứ không phải chất lượng) → mô hình có cửa, và sản phẩm nên nghiêng về giải bài toán cơ chế. 0/15 quan tâm → chỉ còn mô hình affiliate/CPC, hạ toàn bộ dự báo doanh thu.

### Cổng 0.3 — Nhu cầu phía cung (thay A2)

**Việc làm:** tự tay soạn một danh sách 20 tin Tier A, đăng vào 3 cộng đồng dev Việt. Kèm form đăng ký nhận bản tin.

**Ngưỡng:** ≥ 50 đăng ký từ 3 lần đăng → có nhu cầu. < 15 → vấn đề không đủ đau, hoặc kênh sai.

> **Quy tắc:** Cổng 0.1 hoặc 0.2 không đạt → dừng tại đây. Chi phí đã bỏ ra: một tuần. Đây là điểm rẻ nhất trong toàn bộ dự án để sai.

---

## 4. Rào cản thật: đây là bài toán pháp nhân, không phải bài toán múi giờ

v1.0 xử lý "đủ điều kiện" như một bài toán múi giờ và thái độ. Nghiên cứu cho thấy đó không phải rào cản chính.

### 4.1 Bốn cơ chế để công ty nước ngoài trả lương cho kỹ sư ở VN

| Cơ chế | Chi phí cho công ty | Rào cản | Tần suất thực tế |
|---|---|---|---|
| **EOR** (Deel, Remote, Oyster…) | 300–600 USD/người/tháng + ~23,5% đóng góp bảo hiểm xã hội của người sử dụng lao động | Phải có ngân sách và quy trình duyệt nhà cung cấp | Phổ biến với công ty đã có vòng gọi vốn |
| **Hợp đồng nhà thầu (B2B)** | Gần như bằng 0 | Rủi ro phân loại sai lao động; nhiều công ty Mỹ né | Phổ biến nhất với startup nhỏ |
| **Pháp nhân tại VN** | Rất cao | Chỉ đáng với quy mô 10+ người | Hiếm |
| **Qua agency/outsourcing** | 20–40% phí | Không phải "remote job" theo nghĩa người dùng muốn | Phổ biến, nhưng ngoài phạm vi |

### 4.2 Vì sao điều này thay đổi sản phẩm

**Là tín hiệu làm giàu dữ liệu tốt nhất.** Nếu công ty dùng Deel/Remote/Oyster và có VN trong danh sách quốc gia, đó là bằng chứng Tier A cứng hơn bất kỳ câu chữ nào trong mô tả tin. Pipeline nên chủ động đi tìm tín hiệu này.

**Là nội dung có giá trị nhất cho cả hai phía.** Kỹ sư cần biết "hỏi công ty câu gì để biết họ trả được lương cho mình"; công ty cần biết "thuê người VN thì làm thế nào". Đây là nội dung AI trích dẫn được, và không board nào đang làm.

**Là dòng doanh thu hợp pháp và phù hợp nhất** (Mục 11.3): giới thiệu EOR và kênh thanh toán.

### 4.3 Phía kỹ sư: nghĩa vụ thuế và cách nhận tiền

Cần một trang nội dung riêng, và cần **kế toán/luật sư VN rà trước khi xuất bản** — không tự viết từ suy luận.

**Khung pháp lý hiện hành (tra 17/08/2026, vẫn phải để kế toán xác nhận):**

| Nội dung | Trạng thái |
|---|---|
| Văn bản chi phối | **Nghị định 253/2026/NĐ-CP** hướng dẫn Luật Thuế TNCN, hiệu lực **01/07/2026** |
| Nghĩa vụ kê khai | *"Cá nhân cư trú phải kê khai thu nhập phát sinh trong và ngoài Việt Nam, không phân biệt nơi trả hay nơi nhận thu nhập."* **Đây là câu quan trọng nhất với khán giả** — nhận lương nước ngoài vào ví nước ngoài vẫn thuộc diện kê khai |
| Tránh đánh thuế hai lần | Nước có Hiệp định với VN → được khấu trừ thuế TNCN đã nộp ở nước ngoài vào số phải nộp tại VN |
| Giảm trừ gia cảnh (từ 01/01/2026) | Bản thân **15,5 triệu VNĐ/tháng** · người phụ thuộc **6,2 triệu/người/tháng** |
| Xác định cư trú | ≥ 183 ngày trong năm dương lịch hoặc 12 tháng liên tục từ ngày nhập cảnh đầu tiên · hoặc có nơi cư trú/tạm trú đăng ký · hoặc hợp đồng thuê nhà ≥ 183 ngày |
| Đường hộ kinh doanh cá thể | **Chưa xác minh được ngưỡng doanh thu và điều kiện áp dụng theo văn bản mới.** Câu hỏi số một cho kế toán |
| Kênh nhận tiền | Wise, Payoneer, chuyển khoản quốc tế, ví nền tảng EOR — phí và ràng buộc kê khai khác nhau, chưa tra |

**Bốn câu cho buổi tư vấn kế toán (R8), theo thứ tự giá trị:**
1. Hộ kinh doanh cá thể cho dịch vụ phần mềm: ngưỡng doanh thu, thuế suất, điều kiện, **theo văn bản đang có hiệu lực** — không theo bài blog cũ
2. Nhận lương từ chủ lao động nước ngoài không có hiện diện tại VN: kê khai theo mẫu nào, chu kỳ nào, ai khấu trừ
3. Cơ chế EOR (chủ lao động là pháp nhân EOR nước ngoài, người lao động ở VN) xử lý thế nào — khác gì so với hợp đồng nhà thầu trực tiếp
4. Kênh nhận tiền nào tạo nghĩa vụ kê khai gì

> **Cảnh báo pháp lý:** không đăng nội dung thuế dưới dạng tư vấn. Đăng dưới dạng "đây là các lựa chọn, đây là câu hỏi cần hỏi kế toán", kèm miễn trừ trách nhiệm rõ ràng và **ngày rà soát gần nhất**.

**Vì sao mục này là tài sản chứ không phải phụ lục:** luật vừa đổi hai lần trong năm 2026. Phần lớn nội dung tiếng Việt đang lưu hành nói về mức giảm trừ cũ. Nội dung *hiện hành* là hàng hiếm — nhưng chỉ hiếm chừng nào còn được cập nhật (Mục 10.1).

---

## 5. Bối cảnh cạnh tranh

v1.0 viết "RemoteOK đã thắng" rồi bỏ qua các đối thủ thực sự sát. Nghiên cứu cho thấy **đã có nhiều bên phục vụ chính xác truy vấn "remote jobs Vietnam"**.

Ba nhóm, không phải một.

**Nhóm 1 — Board tổng hợp có trang Việt Nam**

| Bên | Họ làm gì | Điểm yếu để khai thác |
|---|---|---|
| **Arc.dev** | Trang `/en-vn/remote-jobs`; hợp tác WWR; có sàng lọc. Doanh thu chính: **25–30% phí trên lương của người được tuyển** (Arc Connect); phí tuyển dụng 15–20%. Đã có lãi, ~3,8 triệu USD ARR, 750k dev | Chính khoản phí đó là thứ JTBD phía cầu (Mục 8.2) muốn tránh. Arc là **bên đương nhiệm mà định vị này tấn công, không phải đối tác**. Tin của họ không gắn nhãn cơ chế hợp đồng |
| **Himalayas** | Trang theo quốc gia sinh tự động, kể cả VN | Trang sinh theo chương trình, mỏng; không kiểm chứng khả năng tuyển thật |
| **Jobgether** | Trang remote VN cho senior | Lọc theo từ khoá, không theo bằng chứng |
| **DailyRemote, RubyOnRemote** | Tổng hợp | Không có tầng bản địa |
| **VietnamDevs** | Board VN, có mục remote | Nhỏ, chủ yếu việc trong nước |

**Nhóm 2 — Board "work from anywhere" tuyển chọn tay** *(v2.0 bỏ sót hoàn toàn — đây là nhóm sát nhất)*

| Bên | Họ làm gì |
|---|---|
| **Real Work From Anywhere** | Chỉ tin từ công ty remote 100% toàn cầu, "không giới hạn địa điểm". Bản tin hằng tuần. Miễn phí. ~292 tin tại thời điểm kiểm |
| **TrulyRemoteWork** | **Duyệt tay từng tin**, kiểm "không có giới hạn quốc gia ẩn, yêu cầu múi giờ, hay điều khoản chuyển chỗ ở". Bản tin tổng hợp hằng tuần |
| **Truly Remote (trulyremote.co)** | Danh sách tuyển chọn hằng tuần, có bộ lọc `Worldwide` |
| **We Are Distributed** | Việc work-from-anywhere, cập nhật hằng ngày |

**Nhóm 3 — Cộng đồng.** Nhóm Facebook (VietAssist v.v.): có hard side thật, nhưng không tìm kiếm được, không cấu trúc, không lưu trữ.

### 5.1 Nhóm 2 đổi kết luận chiến lược

Phương pháp công bố của TrulyRemoteWork — duyệt tay, loại tin có giới hạn quốc gia ẩn / yêu cầu múi giờ / điều khoản chuyển chỗ — **trùng gần như từng chữ với các quy tắc DQ-01, DQ-02, DQ-05, DQ-06 của [rubric-spec.md](rubric-spec.md).** Họ đã làm tầng lọc đó, hằng tuần, miễn phí, bằng tay.

**Hệ quả 1 — tầng lọc "worldwide" đã là hàng hoá phổ thông.** Một kỹ sư VN chỉ muốn danh sách việc toàn cầu đã có ít nhất bốn nguồn miễn phí. Xuất bản một tin mà bằng chứng duy nhất là ngôn ngữ "work from anywhere" (quy tắc A-02/A-03) là **đăng lại thứ đã có sẵn miễn phí ở nơi khác.**

**Hệ quả 2 — nhưng tầng bằng chứng thì chưa ai làm.** Kiểm trực tiếp Real Work From Anywhere cho thấy họ **không** gắn nhãn cơ chế hợp đồng (EOR / nhà thầu / pháp nhân), **không** ghi số giờ trùng múi giờ yêu cầu, **không** nêu công ty tuyển được hợp pháp ở những nước nào. FAQ của họ thừa nhận nghĩa vụ thuế và yêu cầu múi giờ khác nhau theo vị trí, nhưng bản thân các tin không ghi nhất quán. Việt Nam và Đông Nam Á không xuất hiện ở đâu trên trang.

Nói cách khác: **họ trả lời "tin này có mở toàn cầu không". Không ai trả lời "công ty này trả lương cho tôi ở Việt Nam bằng cơ chế nào".** Đó đúng là rào cản đã xác định ở Mục 4.

**Hệ quả 3 — khác biệt dịch chỗ.** Không còn là "chúng tôi lọc tốt hơn". Là **"chúng tôi gắn nhãn cơ chế"**. Kéo theo thay đổi định nghĩa North Star ở Mục 12.1.

**Hệ quả 4 — Nhóm 2 là kênh, không chỉ là đối thủ.** Họ đã lọc sẵn tập "worldwide". Đó là **nguồn tin đầu vào chất lượng cao cho tầng bằng chứng của ta** — và cũng là nơi đăng chéo hợp lý. Cạnh tranh trực diện với họ ở tầng lọc là chọn sai trận.

**Đối thủ nguy hiểm nhất vẫn là nhóm Facebook**, vì họ giữ hard side. Hợp tác hoặc cung cấp thứ họ không làm được: khả năng tìm kiếm và lưu trữ có cấu trúc.

### 5.2 Nhóm 4 — trợ lý AI tìm việc *(mới ở v2.4)*

Không phải board, mà là **hành vi thay thế**: ChatGPT hiện kéo tin tuyển dụng trực tiếp từ Indeed, Upwork, Appcast và web, đối chiếu với hồ sơ người dùng, và dựng CV trong cùng một cuộc trò chuyện. Các trợ lý tự động theo dõi cơ sở dữ liệu việc làm toàn cầu theo tiêu chí người dùng đặt, **bao gồm cả tiêu chí tương thích múi giờ**.

**Đây là mối đe doạ thật với tầng lọc** — cùng tầng mà Nhóm 2 đã làm miễn phí. Nếu người dùng chỉ cần "tìm việc remote hợp múi giờ tôi", trợ lý AI làm được, ngay bây giờ, không cần sản phẩm nào.

**Nhưng nó vấp đúng bức tường mà con người vấp.** Trợ lý đọc tin trên Indeed gặp cùng vấn đề: tin ghi "remote" và **không nói công ty có trả lương được cho người ở Việt Nam hay không**. Thông tin đó không tồn tại trong nguồn có cấu trúc nào để trợ lý đọc. Không mô hình nào suy ra được thứ chưa được viết xuống.

Kết luận trùng với Mục 5.1 nhưng đến từ hướng khác — và sự trùng đó là bằng chứng đáng tin hơn một mình nó: **tầng lọc đã mất, tầng bằng chứng còn nguyên.**

**Hai hệ quả cho phân phối, cần theo dõi chứ chưa hành động:**

1. **Cửa trước đang dịch chuyển.** Nếu trợ lý AI thành nơi người ta bắt đầu tìm việc, thì **được AI trích dẫn quan trọng hơn được người tìm thấy qua Google.** Củng cố lập luận GEO ở Mục 10.1 và làm phép đo A4 (16.1.1) thành chỉ số chiến lược, không phải chỉ số marketing.
2. **Dữ liệu có thể là sản phẩm, không chỉ là website.** Bộ nhãn có cấu trúc về khả năng tuyển theo quốc gia là thứ trợ lý AI cần và không có. **Đây là lựa chọn cần quan sát, không phải hướng đi cần chuyển sang bây giờ** — nó phụ thuộc hoàn toàn vào việc dữ liệu có tồn tại và có đúng không, tức phụ thuộc Cổng 0.1 và A8. Ghi ra để nhận ra khi nó xảy ra, không phải để đuổi theo.

---

## 6. Ràng buộc pháp lý & tuân thủ

**Mục này hoàn toàn không có trong v1.0.** Nó chứa hai ràng buộc có thể phá huỷ mô hình, và một ràng buộc biến thành cơ hội.

### 6.1 Chính sách JobPosting của Google — ràng buộc trở thành mô hình kinh doanh

Chính sách nội dung của Google cho JobPosting structured data yêu cầu:
- **Không đăng tin khi không có ủy quyền** từ tổ chức tuyển dụng; không được ngụ ý sai về liên kết hoặc chứng thực
- Phải có **cách nộp hồ sơ** trên trang, hoặc thông tin liên hệ trực tiếp của công ty tuyển
- **Tin hết hạn phải được gỡ** (đặt `validThrough` về quá khứ, trả 404/410, hoặc xoá structured data). Không làm → **có thể bị manual action**
- Markup chỉ đặt trên trang chi tiết một tin, không đặt trên trang danh sách

Đồng thời: Google đã đóng Google Jobs API (2021) và ngừng chương trình Google Job Ads trả phí (2024). Tính năng tìm việc tự nhiên vẫn còn, nhưng Google rõ ràng đang lùi khỏi mảng này.

**Hệ quả kiến trúc — chia chỉ mục làm hai lớp:**

| | Lớp 1 — Tin được ủy quyền | Lớp 2 — Tin tổng hợp |
|---|---|---|
| Nguồn | Công ty tự đăng (trả phí hoặc miễn phí), feed ATS chính thức, đối tác | Scrape/tổng hợp |
| JobPosting schema | **Có** | **Không** |
| Lập chỉ mục | Có, dùng Indexing API | `noindex`, hoặc canonical về nguồn gốc |
| Vai trò | Kênh Google for Jobs + sản phẩm bán được | Nguyên liệu cho bản tin, bảng lọc, và dữ liệu làm giàu |
| Gỡ khi hết hạn | Trong 48h, bắt buộc | Ẩn khi phát hiện |

**Đây là chuyển đổi quan trọng nhất về mặt kiến trúc so với v1.0** — và nó có một tính chất đẹp: **ràng buộc tuân thủ và mô hình doanh thu trùng nhau.** Công ty trả tiền để đăng → ta có ủy quyền → ta được markup → ta lấy traffic Google Jobs. Không trả tiền, không ủy quyền, không markup. Động cơ thẳng hàng.

### 6.2 Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (hiệu lực 01/01/2026)

Chồng văn bản chính xác *(sửa ở v2.5 — bản trước ghi mơ hồ)*: **Luật 91/2025/QH15** là luật, hiệu lực 01/01/2026. **Nghị định 356/2025/NĐ-CP** (ban hành 31/12/2025, hiệu lực 01/01/2026) quy định chi tiết thi hành, và **thay thế hoàn toàn Nghị định 13/2023/NĐ-CP** — Nghị định 13 đã hết hiệu lực. Nhiều bài viết đang lưu hành vẫn tham chiếu Nghị định 13; kiểm ngày của mọi nguồn thứ cấp.

Nghị định 356 gồm 5 chương, 42 điều, phụ lục **10 hồ sơ và biểu mẫu**, tập trung vào: quy trình đánh giá tác động (DPIA) · thủ tục chuyển dữ liệu ra nước ngoài · chức năng nhiệm vụ DPO · hệ thống biểu mẫu mới · cơ chế kiểm tra thanh tra của Cục An ninh mạng (A05).

#### Cấu trúc miễn trừ — và cái bẫy quyết định

| Nghĩa vụ | Miễn trừ |
|---|---|
| Bổ nhiệm **DPO** | Doanh nghiệp siêu nhỏ và hộ kinh doanh: **miễn hoàn toàn.** Doanh nghiệp nhỏ và khởi nghiệp sáng tạo: hoãn **5 năm** từ 01/01/2026 |
| Lập hồ sơ **DPIA** | Doanh nghiệp nhỏ và khởi nghiệp: được chọn **không lập trong 5 năm đầu** |

**Cả hai miễn trừ mất hiệu lực nếu:** xử lý **dữ liệu cá nhân nhạy cảm** · hoặc kinh doanh dịch vụ xử lý dữ liệu · hoặc xử lý tích luỹ **≥ 100.000 chủ thể dữ liệu**.

Điều kiện thứ ba không áp dụng ở quy mô này. Điều kiện thứ nhất thì **có thể áp dụng**: một nguồn liệt kê dữ liệu nhạy cảm gồm "y tế, sinh trắc học, **tài chính**", và lương là dữ liệu tài chính cá nhân.

> **Câu hỏi đắt nhất trong toàn bộ tài liệu:** dữ liệu lương do người dùng đóng góp có phải dữ liệu cá nhân nhạy cảm không?
>
> **Không** → dự án gần như miễn toàn bộ nghĩa vụ DPO và DPIA trong 5 năm.
> **Có** → mất sạch miễn trừ, phải có DPO và hồ sơ DPIA **ngay từ bản ghi lương đầu tiên**, kể cả với dự án một người.
>
> Đây là ranh giới giữa chi phí tuân thủ gần bằng không và chi phí tuân thủ thật. Câu hỏi đầy đủ và các phương án thiết kế để tránh: [legal-brief.md](legal-brief.md) B-Q1.

**Đọc thẳng văn bản đã thu hẹp câu hỏi đáng kể.** Mục "tài chính" trong danh mục nhạy cảm được diễn đạt nguyên văn là *"Thông tin khách hàng của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài, tổ chức cung ứng dịch vụ trung gian thanh toán... gồm: thông tin định danh khách hàng, thông tin về tài khoản, thông tin về tiền gửi, thông tin về tài sản gửi, thông tin về giao dịch"*. Đó là **thông tin khách hàng do tổ chức tín dụng nắm giữ**, không phải "mọi thông tin tài chính của một người". **Thu nhập và tiền lương không được liệt kê riêng.** Chi tiết và hai lỗ hổng còn lại: [legal-brief.md](legal-brief.md) E.2–E.3.

**Quyết định phạm vi — xoá câu hỏi thay vì trả lời nó.** v1 **không thu con số lương**. Vòng đóng góp cộng đồng chỉ thu *kết quả tuyển dụng*, *cơ chế hợp đồng*, *chủ lao động trong nước hay nước ngoài*.

Cái giá gần bằng không: bằng chứng Tier A-VN mạnh nhất là **A-05 — đã có người Việt được nhận ở công ty này chưa** — và câu đó trả lời được **không cần một con số lương nào**. Dữ liệu lương là thứ tốt để có, không phải thứ bắt buộc. Hoãn sang v2, khi đã có khán giả và có lý do để trả tiền tư vấn.

Ba câu hỏi pháp lý đắt nhất (dữ liệu nhạy cảm · ngưỡng k-ẩn danh · nghĩa vụ DPO) biến mất cùng lúc, chi phí bằng không.

**Ràng buộc trực tiếp lên sản phẩm:**

1. **Cấm mua bán dữ liệu cá nhân**, trừ trường hợp luật định. Chế tài lên tới **10 lần doanh thu thu được từ hành vi vi phạm**.
   → **Dòng doanh thu "quyền truy cập ứng viên" trong Lean Canvas v1.0 phải bỏ.** Thay bằng: mô hình giới thiệu có đồng ý — ứng viên chủ động bấm "cho phép giới thiệu tôi tới công ty X", nhật ký đồng ý được lưu, và ta thu phí cho *dịch vụ kết nối*, không bán *dữ liệu*.

2. **Đồng ý phải rõ ràng, cụ thể theo từng mục đích.** Cấm đồng ý ngầm định (ô tick sẵn, im lặng, không hành động). Dữ liệu nhạy cảm cần đồng ý bằng văn bản hoặc xác thực điện tử.
   → FR-7 (form lương ẩn danh) cần màn hình đồng ý riêng, ghi rõ: thu gì, để làm gì, hiển thị ra sao, ai thấy, giữ bao lâu, rút lại thế nào.

3. **Dữ liệu lương/thu nhập là dữ liệu cá nhân.** "Ẩn danh" trên giao diện không đủ — nếu bản ghi gồm (công ty + chức danh + cấp độ + lương) và chỉ có 1–2 người ở vị trí đó, nó tái định danh được.
   → **Quy tắc k-ẩn danh bắt buộc: không hiển thị số liệu lương cho một tổ hợp (công ty × chức danh × cấp độ) nếu có dưới 5 bản ghi.** Dưới ngưỡng thì chỉ hiển thị ở mức tổng hợp rộng hơn.

4. **Chuyển dữ liệu ra nước ngoài** có nghĩa vụ hồ sơ/thông báo. Hosting ở nước ngoài → phải rà.

### 6.3 Nguồn dữ liệu và điều khoản sử dụng

Ưu tiên theo thứ tự, chỉ xuống bậc dưới khi bậc trên không đủ:

1. **Endpoint công khai của ATS** (Greenhouse, Lever, Ashby, Workable) — không cần xác thực, trả JSON, phục vụ đúng dữ liệu công ty đã chọn công khai trên trang tuyển dụng của họ
2. **Trang tuyển dụng của công ty**, tôn trọng `robots.txt`, giới hạn tốc độ, User-Agent trung thực có thông tin liên hệ
3. **Board có chương trình đối tác/affiliate**
4. **Không scrape LinkedIn.** Rủi ro pháp lý và rủi ro chặn đều cao, và không cần thiết

> **Sửa lại tuyên bố ở bản trước.** Bản v2.1 mô tả các endpoint ATS công khai là "giải phần lớn bài toán điều khoản sử dụng". Kiểm chứng cho thấy **không nhà cung cấp nào trong bốn bên công bố điều khoản cho phép rõ ràng việc bên thứ ba tổng hợp lại**. Điều đúng, hẹp hơn nhiều:
>
> - Đây là endpoint **không xác thực**, phục vụ dữ liệu công ty **đã chủ động chọn công khai** — rất khác về bản chất so với vượt rào đăng nhập hay bỏ qua `robots.txt`
> - Nhưng "không bị chặn" **không đồng nghĩa với "được cho phép"**. Greenhouse không công bố giới hạn tốc độ cứng nhưng **có bóp nghẹt bên gọi lạm dụng**; Ashby giới hạn theo khoá và trả 429; Lever không có điều khoản công khai cho endpoint này, chỉ ghi rằng bên dùng chịu trách nhiệm về cách sử dụng dữ liệu
>
> **Hệ quả:** đây là **giảm rủi ro đáng kể so với scraping, không phải xoá rủi ro.** Câu hỏi Q1 ở PRD (tin từ ATS API có tính là "được ủy quyền" theo chính sách Google không) vẫn mở, và giờ có thêm câu hỏi thứ hai cho luật sư: *bốn nhà cung cấp này im lặng về việc tổng hợp lại — im lặng đó nghĩa là gì?* Cho tới khi có câu trả lời, giữ mặc định an toàn: mọi tin là `aggregated`, không phát sinh schema.

**Không sao chép nguyên văn mô tả công việc.** Lưu để phân tích, hiển thị trích đoạn ngắn có dẫn nguồn + liên kết về tin gốc. Đây vừa là xử lý bản quyền, vừa tránh nội dung trùng lặp.

### 6.4 Danh mục kiểm tuân thủ trước khi ra mắt

- [ ] Chính sách quyền riêng tư + thông báo xử lý dữ liệu theo PDPL, tiếng Việt
- [ ] Màn hình đồng ý riêng cho mỗi mục đích thu thập dữ liệu
- [ ] Cơ chế rút lại đồng ý và xoá dữ liệu, hoạt động thật
- [ ] Ngưỡng k-ẩn danh cài trong code, có test
- [ ] Job tự động gỡ tin hết hạn trong 48h + alert khi job này lỗi
- [ ] Miễn trừ trách nhiệm trên mọi nội dung thuế/pháp lý
- [ ] Nhật ký nguồn cho mọi bản ghi: lấy từ đâu, lúc nào, theo điều khoản nào

---

## 7. Lean Canvas

| Ô | Nội dung |
|---|---|
| **Vấn đề** | 1. Kỹ sư VN không biết công ty nào có **cơ chế pháp lý** để trả lương cho họ → nộp mù, tỷ lệ hồi đáp gần 0<br>2. Không biết cách nhận tiền và nghĩa vụ thuế → người đã có offer vẫn tắc ở bước này<br>3. Công ty nước ngoài muốn thuê nhưng không biết cơ chế, và không muốn trả 20–40% phí agency |
| **Phân khúc khách hàng** | *Đầu cầu:* kỹ sư VN 3–10 năm, tiếng Anh làm việc được, đã từng thử nộp remote và thất bại<br>*Người trả tiền (giả thuyết, chưa kiểm):* công ty 10–200 người đã quen thuê remote nhưng chưa từng thuê ở VN |
| **Giải pháp** | Tin đã gắn nhãn bằng chứng theo rubric Mục 2 + tầng nội dung về cơ chế hợp đồng, thanh toán, thuế |
| **Lợi thế khác biệt** | Tầng bằng chứng tích luỹ về **khả năng tuyển thật** — không phải danh sách tin. Scrape lại không tạo ra được lịch sử "công ty X nói worldwide nhưng đã từ chối GMT+7 vào tháng 3" |
| **Giá trị độc nhất** | "Chỉ những việc thực sự trả lương được cho bạn — kèm bằng chứng vì sao chúng tôi nghĩ vậy" |
| **Kênh** | **Chính:** bản tin + cộng đồng dev VN<br>**Bồi:** SEO trên nội dung bản địa (không phải trang danh sách tin)<br>**Bồi:** Google for Jobs, chỉ cho tin được ủy quyền |
| **Nguồn thu** | Affiliate EOR/thanh toán → đăng tin trả phí (đồng thời là ủy quyền) → tài trợ bản tin → hồ sơ công ty "VN-friendly" đã xác minh. **Không bán dữ liệu ứng viên (bị cấm theo PDPL).** |
| **Cấu trúc chi phí** | Hạ tầng 20–40 USD/tháng; LLM 100–250 USD/tháng (xem 11.1); thời gian một người |
| **Chỉ số then chốt** | Cặp số: tin Tier A/tuần **×** độ chính xác nhãn (Mục 12) |

---

## 8. Jobs-to-be-Done

### 8.1 Phía kỹ sư

> **Khi tôi** muốn tăng thu nhập đáng kể mà không rời Việt Nam,
> **tôi muốn** biết công ty nào thực sự có cách trả lương cho người ở VN và chấp nhận múi giờ của tôi,
> **để tôi** không đốt hàng chục giờ nộp vào những nơi không bao giờ hồi đáp — và khi có offer thì không tắc ở khâu hợp đồng và thuế.

**Cách họ giải quyết hiện nay:** RemoteOK/LinkedIn/Arc + đoán, hoặc hỏi trong nhóm Facebook.
**Chỉ số "khó chịu":** số giờ nộp hồ sơ trên mỗi lần được hồi đáp.

**Hiệu chỉnh kỳ vọng (dữ liệu, không phải marketing):** lương kỹ sư tại VN khoảng 900–3.500 USD/tháng tuỳ cấp; kỹ sư VN làm remote cho nước ngoài trung bình khoảng 45.800 USD/năm; kỹ sư remote tại Mỹ trung bình khoảng 147.500 USD/năm. Nghĩa là **bước nhảy thực tế phổ biến là 1,5–2x, không phải 2–4x**; mức 3–4x có tồn tại nhưng là phần đuôi hiếm. Sản phẩm không được hứa con số đuôi — hứa sai là cách nhanh nhất để mất niềm tin của chính hard side.

### 8.2 Phía nhà tuyển dụng

> **Khi tôi** cần thuê kỹ sư giỏi với ngân sách hạn chế,
> **tôi muốn** biết mình *có thể* thuê ở Việt Nam bằng cơ chế nào và tốn thêm bao nhiêu,
> **để tôi** ra quyết định mà không phải tự đi nghiên cứu luật lao động của một nước tôi không biết gì.

**Cách họ giải quyết:** Toptal, Turing, Arc, hoặc bỏ qua VN vì "phức tạp quá".

**Chi phí của đường hiện tại, đã kiểm chứng:** Arc.dev thu **25–30% trên lương của người được tuyển** (Arc Connect — dòng doanh thu chính của họ), hoặc 15–20% phí tuyển dụng. So sánh: EOR tốn 300–600 USD/người/tháng cộng ~23,5% đóng góp bảo hiểm xã hội — với lương 45.000 USD/năm thì EOR rẻ hơn đáng kể so với 25–30% phí trung gian.

Lưu ý cách phát biểu cho đúng: phí của Arc tính **trên đầu công ty**, không trừ vào lương kỹ sư. Nó không trực tiếp làm giảm lương — nhưng nó **cạnh tranh với lương trên cùng một ngân sách**, nên vẫn ảnh hưởng. Đừng nói "Arc lấy 30% lương của bạn"; nói đúng là "Arc làm bạn đắt hơn 30% với công ty".

### 8.3 Căng thẳng giữa hai phía — phải nói ra

v1.0 không đề cập: **kỹ sư muốn lương cao hơn, công ty muốn chi phí thấp hơn.** Sản phẩm sống nhờ chênh lệch đó. Nếu cả hai bên đọc cùng một website, mâu thuẫn này lộ ra ngay.

**Cách xử lý:** không giả vờ trung lập. **Sản phẩm đứng về phía kỹ sư một cách công khai** — công bố dải lương thật, dạy cách đàm phán, gắn nhãn công ty trả thấp. Phía cầu vẫn trả tiền vì họ mua **khả năng tiếp cận và tính tuân thủ**, không mua giá rẻ. Bên nào không chấp nhận điều đó không phải khách hàng.

Hệ quả: hai bề mặt tách biệt (trang cho kỹ sư tiếng Việt / trang cho nhà tuyển dụng tiếng Anh), thông điệp nhất quán trên cả hai — không nói với công ty rằng "lao động VN rẻ" trong khi nói với kỹ sư rằng "đòi lương cao đi".

---

## 9. Cold Start Theory — áp dụng

Khung của Andrew Chen: **cold start → tipping point → escape velocity → ceiling → moat.** Nguyên tắc: bắt đầu từ **atomic network** nhỏ nhất tự duy trì được; **mật độ quan trọng hơn quy mô.**

### 9.1 Sửa mâu thuẫn của v1.0

v1.0 nói hai điều loại trừ nhau: Mục 2 khẳng định "hiệu ứng mạng = 0 trong 12 tháng đầu", Mục 5.2 khẳng định hard side là những người đóng góp dữ liệu. Nhưng **vòng đóng góp dữ liệu CHÍNH LÀ hiệu ứng mạng** (dạng data network effect), và nếu nó là con hào duy nhất thì nó phải bắt đầu từ tháng 1, không phải tháng 12.

**Cách nói đúng:**

| | Giai đoạn 1 (tháng 1–12) | Giai đoạn 2 (tháng 12+) |
|---|---|---|
| Bản chất | Trang nội dung **có vòng đóng góp dữ liệu chạy song song từ ngày đầu** | Nền tảng hai chiều |
| Hiệu ứng mạng | **Data network effect, yếu nhưng khác 0 và phải nuôi từ tháng 1** | Hiệu ứng mạng hai phía |
| Con hào | Dữ liệu bằng chứng tích luỹ + thẩm quyền nội dung | Cộng thêm mật độ hai phía |
| Rủi ro chính | Không ai đóng góp → không có hào | Không đủ mật độ |

Chỗ v1.0 đúng và cần giữ: **trong 12 tháng đầu đừng tự lừa rằng đang xây nền tảng.** Chỗ cần sửa: **cũng đừng hoãn vòng đóng góp tới tháng 12** — hoãn nó là hoãn con hào duy nhất.

### 9.2 Atomic network

> **Kỹ sư React/Node/Python tại Việt Nam, 3+ năm, tiếng Anh làm việc được, nhắm vị trí trùng múi giờ châu Âu (GMT+1/+2).**

**Vì sao châu Âu — nói rõ phép tính mà v1.0 bỏ qua:**
- GMT+7 vs CET = lệch 5–6h. VN 14:00 = CET 08:00–09:00. **Có 4 giờ trùng trong giờ hành chính hai bên.** Khả thi.
- GMT+7 vs Mỹ (ET) = lệch 11–12h. Gần như không trùng nếu không làm đêm. Loại.
- GMT+8 đến GMT+11 (Singapore/Úc/Nhật) = trùng dễ nhất, **nhưng khối lượng tin remote toàn cầu ít hơn nhiều và mức lương thấp hơn.** Đây là **ngách thứ cấp**, mở sau khi ngách châu Âu chạm trần.

Ước lượng quy mô: vài nghìn người. Đủ nhỏ để phủ hết.

### 9.3 Hard side

Hard side **không phải** kỹ sư đọc tin, cũng **không phải** tin tuyển dụng. Hard side là **người đóng góp bằng chứng mà không ai khác có**:
- Người đã trúng tuyển và chia sẻ cơ chế hợp đồng thật + dải lương
- Người xác nhận công ty X có/không tuyển được ở VN, kèm ngày
- Người chia sẻ quy trình phỏng vấn và lý do bị loại

**Vấn đề cold start của hard side mà v1.0 không nêu:** người đóng góp có ích nhất là người **đã được nhận** — mà lúc đầu chưa ai được nhận qua sản phẩm này. Vòng lặp bị khoá.

**Ba cách phá khoá, theo thứ tự thử:**
1. **Nhập liệu tay từ nguồn công khai** — bài chia sẻ trên nhóm Facebook, blog cá nhân, thread Reddit/Spiderum, kèm dẫn nguồn và xin phép khi cần. 50 bản ghi đầu tiên do người sáng lập gõ tay, không chờ cộng đồng.
2. **Hỏi người đã có việc remote sẵn** — họ tồn tại, chỉ là không tập trung ở đâu. Phỏng vấn 1-1, đổi lại bằng quyền truy cập sớm.
3. **Chỉ sau khi có 50 bản ghi mồi** mới mở form tự phục vụ. Form trống không ai điền.

### 9.4 Cổng chuyển giai đoạn

| Giai đoạn | Cổng để đi tiếp |
|---|---|
| **Cold start** | ≥ 25 tin **Tier A-VN**/tuần *(mốc cần hiệu chỉnh sau Cổng 0.1 — xem 12.2)*, ổn định 4 tuần liên tiếp, **và** độ chính xác nhãn ≥ 85% qua kiểm tay |
| **Tipping point** | Tỷ lệ mở bản tin ≥ 35% trong 3 số liên tiếp **và** tỷ lệ quay lại 30 ngày ≥ 20% trong nhóm atomic |
| **Escape velocity** | ≥ 20% người mới đến từ giới thiệu/chia sẻ trực tiếp |
| **Ceiling** | Tăng trưởng bản tin < 3%/tháng trong 2 tháng → mở ngách GMT+8..+11 hoặc vai trò liền kề |
| **Moat** | ≥ 300 bản ghi bằng chứng do cộng đồng đóng góp, trong đó ≥ 100 là Tier A xác nhận tuyển thật |

*Ghi chú: v1.0 đặt mốc moat là 500 bản ghi/12 tháng trong khi tiêu chí dừng lại là <50 sau 6 tháng — hai con số này không nối được với nhau bằng bất kỳ đường tăng trưởng hợp lý nào. v2.0 hạ mốc moat xuống 300 và thêm điều kiện chất lượng, vì 100 bản ghi Tier A thật có giá trị hơn 500 bản ghi "nghe nói".*

**Quy tắc:** không đầu tư vào giai đoạn sau khi cổng giai đoạn trước chưa đạt.

---

## 10. Phân tích con hào

| Nguồn sức mạnh (Helmer) | Có? | Ghi chú |
|---|---|---|
| Quy mô kinh tế | Không | Chi phí gần tuyến tính |
| Hiệu ứng mạng | **Yếu, dạng dữ liệu** | Bắt đầu từ tháng 1, không phải tháng 12 (Mục 9.1) |
| Chi phí chuyển đổi | Yếu | Người dùng rời đi không mất gì |
| Thương hiệu | **Xây được** | "Nguồn đáng tin cho dev Việt tìm việc quốc tế" — nhưng phải trả giá bằng việc đứng về phía kỹ sư (8.3) |
| Nguồn lực độc quyền | **Có — dữ liệu bằng chứng tích luỹ** | Nguồn hào chính |
| Quy trình vượt trội | **Có — rubric + kỷ luật chất lượng** | Rubric bản thân nó copy được; thứ không copy được là **lịch sử áp dụng nó** |
| Định giá phản công | Không | |

### 10.1 Con hào thật

**(1) Lịch sử bằng chứng.** Không phải "dữ liệu làm giàu" chung chung như v1.0 viết — cụ thể là **chuỗi thời gian các quan sát về hành vi tuyển dụng**: công ty nào nói "worldwide" nhưng từ chối GMT+7 vào ngày nào; công ty nào đổi từ contractor sang EOR; chức danh nào ứng với cấp độ nào. Người mới scrape hôm nay có ảnh chụp hiện tại, **không có lịch sử**. Lịch sử mới là thứ dự báo được.

**(2) Thẩm quyền nội dung bản địa — nhưng là guồng quay, không phải tài sản.** Khi tìm kiếm chuyển sang câu trả lời AI, trang tổng hợp mỏng bị bỏ qua, nội dung có thẩm quyền và có cấu trúc mới được trích dẫn. Nội dung về cơ chế hợp đồng / thanh toán / thuế cho người Việt là thứ trích dẫn được. **Danh sách tin thì không** — đây là lý do phải đảo thứ tự ưu tiên so với v1.0.

**Sửa cách hiểu ở v2.3 (thêm ở v2.4):** gọi nó là "tài sản tích luỹ" là sai. Hai sự thật độc lập cùng chỉ về một hướng:

1. **Luật thuế Việt Nam đổi hai lần trong năm 2026** — mức giảm trừ gia cảnh mới từ 01/01/2026, Nghị định 253/2026/NĐ-CP hướng dẫn Luật Thuế TNCN có hiệu lực **01/07/2026**. Mọi nội dung tiếng Việt viết trước 2026 giờ đã sai số liệu.
2. **Nội dung cập nhật trong 30 ngày được AI trích dẫn nhiều hơn hẳn nội dung cũ** (nghiên cứu GEO, Mục 16 A4). Perplexity đánh trọng số độ mới rất cao — mẫu trích dẫn ở đó **đổi trong vòng 48 giờ**.

Hai điều này nhân với nhau: **giữ nội dung hiện hành phục vụ đồng thời cả con hào lẫn kênh phân phối.** Và nó cũng nói rõ chi phí — đây là công việc định kỳ, không phải viết một lần rồi thu lãi. Đối thủ không chịu guồng quay đó sẽ rơi khỏi trích dẫn; **ta cũng vậy nếu ngừng quay.**

**Hệ quả vận hành:** mỗi bài nội dung bản địa cần chu kỳ rà soát ghi rõ (đề xuất: mỗi quý, và bắt buộc rà khi có văn bản pháp luật mới). Bài quá hạn rà soát phải hiển thị cảnh báo, không im lặng để nguyên.

### 10.2 Con hào KHÔNG nằm ở đâu

- **Không ở việc scrape.** Ai cũng làm được trong một tuần — Arc, Himalayas, Jobgether đã làm rồi.
- **Không ở giao diện.** Copy trong một ngày.
- **Không ở RAG/LLM.** Hàng hoá phổ thông, giá đang giảm.
- **Không ở rubric.** Công khai rubric còn có lợi (tạo niềm tin); thứ giữ được là dữ liệu đã chấm theo rubric qua thời gian.
- **(mới) Không ở việc lọc tin "worldwide".** Ít nhất bốn board đã duyệt tay việc này, hằng tuần, miễn phí (Mục 5.1).
- **(mới) Không ở dữ liệu lương Việt Nam nói chung.** levels.fyi đã có trang Việt Nam với dữ liệu tổng hợp; Glassdoor và Robert Walters cũng vậy. Xem 10.3.

### 10.3 Ranh giới của con hào dữ liệu lương

Kiểm chứng: levels.fyi có trang Việt Nam, tổng thu nhập kỹ sư phần mềm trung bình ~332,8 triệu VNĐ/năm, dải ~213,9–593,5 triệu. Nhưng chính họ ghi nhận **nhiều tổ hợp cấp độ × địa điểm có rất ít hoặc không có dữ liệu hợp lệ** — mỏng đúng ở mức chi tiết mà ngưỡng k-ẩn danh của ta cũng cắt.

**Điều đã có miễn phí:** lương kỹ sư *tại Việt Nam*, ở mức tổng hợp.

**Điều chưa ai có — và là lát cắt thật sự khác:** lương của người Việt làm remote cho **chủ lao động nước ngoài**, phân theo **cơ chế hợp đồng** (EOR / nhà thầu / pháp nhân). Đó là hai chiều mà levels.fyi không thu, vì mô hình dữ liệu của họ giả định quan hệ lao động tại chỗ.

**Hệ quả bắt buộc cho FR-7.2:** form đóng góp **phải** thu (a) chủ lao động là trong nước hay nước ngoài, (b) cơ chế hợp đồng. Thiếu hai trường đó thì đang xây một bản levels.fyi kém hơn, trên tập mẫu nhỏ hơn nhiều.

Con số tham chiếu cho thấy khoảng cách đáng đo: ~13.000 USD/năm (levels.fyi, kỹ sư tại VN) so với ~45.800 USD/năm (Arc, dev VN làm remote cho nước ngoài). Chênh ~3,5 lần — **nhưng hai con số đo hai quần thể khác nhau**, đừng trích chúng cạnh nhau như một so sánh.

**Hệ quả ưu tiên:** mọi giờ dành cho giao diện đẹp là giờ không dành cho hai nguồn hào thật.

---

## 11. Kinh tế đơn vị & mô hình doanh thu

### 11.1 Chi phí — đã sửa ước lượng LLM

| Khoản | v1.0 | v2.1 | Ghi chú |
|---|---|---|---|
| Hạ tầng (VPS, Postgres, CDN) | 20–40 USD | 20–40 USD | Không đổi |
| LLM chấm nhãn | 30–60 USD | **5–35 USD** | Tính lại bằng giá thật — xem dưới |
| Tên miền, công cụ, email | 10 USD | 25 USD | Cần dịch vụ gửi bản tin |
| Rà soát pháp lý (một lần) | — | **300–800 USD** | Chính sách quyền riêng tư PDPL + rà nội dung thuế. Không bỏ qua được |
| **Tổng tiền mặt/tháng** | 60–110 USD | **50–100 USD** | |

**Sửa lại con số LLM.** Bản v2.0 của tài liệu này ghi 100–250 USD/tháng và gọi ước lượng 30–60 USD của v1.0 là "thấp 3x". Tính lại bằng giá công bố và kiến trúc pipeline thật (PRD Mục 9.2) cho khoảng **5–35 USD/tháng** — nghĩa là v2.0 sai theo hướng ngược lại, và sai nhiều hơn v1.0.

Ba yếu tố bị bỏ sót:
- **Khối lượng lấy trước lọc thay vì sau lọc.** Lọc thô xác định (regex loại trừ) chạy trước LLM cắt khoảng 90% khối lượng: ~400 tin/tuần vào LLM, không phải 1.000 tin/ngày
- **Prompt caching** — prompt rubric là tiền tố ổn định, đọc lại tốn ~0,1x giá gốc
- **Batch API** — pipeline chạy đêm không cần trả lời tức thời, giảm 50% mọi token

Ba đòn bẩy này **nhân với nhau**, không cộng. Chi tiết và bảng giá theo model ở [rubric-spec.md](rubric-spec.md) Mục 14.1.

**Hệ quả cho quyết định:** chênh lệch giữa model rẻ nhất và mạnh nhất là ~14 USD/tháng. **Chọn model theo độ chính xác nhãn, không theo giá.**

**Nhận định giữ nguyên và vẫn đúng:** chi phí tiền mặt không đáng kể. **Rủi ro thật là chi phí cơ hội thời gian.** Câu hỏi không phải "có lãi không" mà "12 tháng này có đáng so với việc khác không".

Bài học phương pháp thì vẫn đứng, chỉ đổi hướng: **ước lượng chi phí bằng suy luận thay vì bằng bảng giá sai được cả hai chiều.** Mọi con số tài chính trong tài liệu này chưa đo thì phải coi là giả thuyết — kể cả những con số do bản sửa lỗi đưa vào.

### 11.2 Doanh thu — ba kịch bản đã hạ

| Kịch bản | Tháng 12 | Tháng 18 | Ghi chú |
|---|---|---|---|
| **Xấu** | 0 USD | 100–200 USD/tháng | Chỉ affiliate EOR/thanh toán |
| **Cơ sở** | 150–300 USD/tháng | 800–1.500 USD/tháng | 2–4 khách đăng tin + affiliate |
| **Tốt** | 800 USD/tháng | 3.000–5.000 USD/tháng | 8–10 hồ sơ công ty định kỳ + tài trợ bản tin |

**Cảnh báo đọc bảng:** doanh thu affiliate **cục bộ, không đều** — 1.500 USD một lần rồi có thể sáu tháng không có gì (11.3.1). Chia trung bình theo tháng làm nó trông như dòng tiền định kỳ, nhưng nó không phải. Một lượt chuyển đổi duy nhất trong năm đầu đã vượt toàn bộ cột "Tháng 12" của kịch bản Cơ sở. Đừng lập kế hoạch chi tiêu dựa trên nó, và đừng coi một tháng có chuyển đổi là bằng chứng mô hình đã chạy.

**Về điểm tham chiếu RemoteOK:** v1.0 dẫn con số ~35.000 USD/tháng. Kiểm chứng cho thấy **các nguồn công khai mâu thuẫn nhau nghiêm trọng** — 25.000 USD MRR, 44.000 USD/tháng, 138.000 USD/tháng, và 3,4 triệu USD doanh thu năm 2024, tuỳ nguồn và tuỳ năm. **Không dùng con số này làm mỏ neo.** Điều duy nhất rút ra được: có tồn tại board một người vận hành đạt quy mô đáng kể, sau 8–10 năm và trong bối cảnh SEO của 2015–2020, khác hẳn 2026.

**Kịch bản Tốt của v2.0 thấp hơn v1.0** vì: (a) kênh SEO đã suy yếu có bằng chứng, (b) đã bỏ dòng doanh thu bán dữ liệu ứng viên do PDPL, (c) đối thủ trực tiếp đã có mặt.

### 11.3 Dòng doanh thu — xếp lại theo độ khả thi và tuân thủ

| # | Dòng | Hợp pháp? | Thời điểm | Ghi chú |
|---|---|---|---|---|
| 1 | **Affiliate EOR & thanh toán** (Deel, Oyster, Wise, Payoneer) | Có | Ngay từ tháng 1 | **Dòng thu lớn nhất về mặt đơn giá** — xem 11.3.1. Không cần traffic lớn, không cần phía cầu. **Bắt đầu từ đây.** Bắt buộc công bố quan hệ affiliate |
| 2 | **Đăng tin trả phí** | Có, và **tạo ủy quyền cho schema** (6.1) | Sau khi có bản tin ≥ 500 người | Giá thăm dò 99–199 USD; chưa có cơ sở cho mức 299 USD |
| 3 | **Tài trợ bản tin** | Có | ≥ 1.000 người đăng ký | Dễ bán hơn đăng tin |
| 4 | **Hồ sơ công ty "VN-friendly" đã xác minh** | Có | Tháng 12+ | Bán tính tuân thủ, không bán quảng cáo |
| 5 | **Feed CPC** | Có | Bất cứ lúc nào | Biên thấp, làm bẩn chất lượng. Cân nhắc kỹ |
| 6 | ~~Bán quyền truy cập ứng viên~~ | **Không — PDPL cấm mua bán dữ liệu cá nhân** | — | Thay bằng giới thiệu có đồng ý rõ ràng, thu phí dịch vụ kết nối |

### 11.3.1 Kinh tế của dòng affiliate — đã kiểm chứng điều khoản

Chương trình affiliate của Deel (điều khoản công bố, tra ngày 17/08/2026):

| Khoản | Giá trị |
|---|---|
| Giới thiệu đủ điều kiện bán hàng | **500 USD** |
| Khách trả tiền mới | **1.000 USD** |
| **Tổng mỗi khách mới** | **1.500 USD** |
| Cửa sổ cookie | 90 ngày |
| Nền tảng / thanh toán | PartnerStack · hằng tháng, Net 15 |

**Vì sao con số này đổi mô hình:** một lượt chuyển đổi duy nhất bằng 5–15 lượt đăng tin trả phí ở mức giá đề xuất (99–199 USD). Nếu dòng này chạy được, nó là dòng thu chính, không phải dòng phụ.

**Nhưng lý thuyết thay đổi mới là phần quan trọng — và nó có một lỗ hổng.** Deel trả tiền khi **công ty** trở thành khách hàng, còn khán giả của sản phẩm này chủ yếu là **kỹ sư**. Kỹ sư không mua EOR.

Đường nối duy nhất hợp lý:

```
Kỹ sư nhận offer
  → công ty chưa có cách trả lương cho người ở VN
  → kỹ sư đưa công ty phương án (nội dung Mục 4.2 + link giới thiệu)
  → công ty đăng ký EOR
```

Đường này có thật, và nó khớp chính xác với rào cản đã xác định ở Mục 4. Nhưng nó **phụ thuộc vào kết quả tuyển dụng thành công** — cùng vòng khoá với hard side ở Mục 9.3. Không có ai được nhận thì không có lượt chuyển đổi nào.

**Ba điều kiện để dòng này không phải ảo tưởng:**
1. Nội dung "công ty của bạn trả lương cho bạn bằng cách nào" phải đủ tốt để kỹ sư thực sự chuyển tiếp cho nhà tuyển dụng
2. Phải theo dõi được kết quả (chỉ số FR-10.5 ở PRD) — không đo được thì không biết dòng này có chạy không
3. Công bố quan hệ affiliate rõ ràng ở mọi nơi có link. Che giấu nó phá huỷ vị thế "đứng về phía kỹ sư" ở Mục 8.3 — đó là tài sản đắt hơn nhiều so với 1.500 USD

**Chưa kiểm chứng:** tỷ lệ chuyển đổi. Điều khoản là sự thật đã tra; **số lượt chuyển đổi mỗi năm là con số bịa cho tới khi có lượt đầu tiên.** Không đưa nó vào dự báo cơ sở.

*(Oyster có chương trình affiliate với mô hình CPA/chia doanh thu, mức chưa công bố công khai. Remote.com chưa tìm thấy chương trình công khai — cần hỏi trực tiếp.)*

### 11.4 Chỉ số khi đã có doanh thu

- **Gross retention của nhà tuyển dụng** — mục tiêu > 85%. **Đây là chỉ số thật:** họ có đăng lại lần hai không?
- **Quick Ratio** = (MRR mới + mở rộng) / (MRR mất + thu hẹp) — mục tiêu > 4,0
- **LTV:CAC** — CAC gần bằng 0 nên chỉ số này sẽ đẹp giả tạo. Theo dõi nhưng **không dùng để tự trấn an.** Nếu thấy mình đang trích dẫn LTV:CAC để biện minh cho việc tiếp tục, đó là dấu hiệu cảnh báo

---

## 12. Khung đo lường

### 12.1 North Star Metric — là một cặp số, không phải một số

> **Số tin Tier A-VN xuất bản mỗi tuần × Độ chính xác nhãn (kiểm tay hàng tháng)**

**Vì sao phải là cặp:** v1.0 khẳng định chỉ số của nó "không thể gian lận bằng cách scrape thêm". Đúng — nhưng nó gian lận được bằng cách **nới rubric**. Buộc hai số phải đi cùng nhau, luôn báo cáo cùng nhau, thì nới rubric sẽ làm tụt độ chính xác và lộ ra ngay.

**Vì sao "Tier A-VN" chứ không phải "Tier A" (sửa ở v2.3):** Mục 5.1 cho thấy tin mà bằng chứng duy nhất là ngôn ngữ "work from anywhere" đã có sẵn miễn phí trên ít nhất bốn board tuyển chọn tay. Đếm chúng vào North Star là **tự chấm điểm cho việc đăng lại nội dung miễn phí của người khác.** Tách làm hai:

| Nhãn | Bằng chứng | Tính vào North Star? |
|---|---|---|
| **Tier A-VN** | A-01 (VN trong danh sách nước) · A-04 (pháp nhân VN) · A-05 (bản ghi cộng đồng) · A-06 (EOR phủ VN) | **Có** — không nơi nào khác có |
| **Tier A-Global** | Chỉ A-02 / A-03 (ngôn ngữ toàn cầu, APAC) | Không — theo dõi riêng, vẫn xuất bản |

Vẫn xuất bản cả hai — Tier A-Global có ích cho người đọc. Nhưng **chỉ Tier A-VN là bằng chứng sản phẩm đang tạo ra thứ chưa tồn tại.**

**Đọc cặp số thế nào:**
- 40 tin × 90% chính xác = tốt
- 80 tin × 55% chính xác = **tệ hơn 20 tin × 95%** — sản phẩm bán niềm tin, không bán số lượng
- 60 tin Tier A-Global × 0 tin Tier A-VN = **đang vận hành một bản sao kém hơn của Real Work From Anywhere**

### 12.2 Chỉ số đầu vào

> **Cảnh báo hiệu chỉnh (v2.3):** các mốc "tin Tier A/tuần" dưới đây được đặt khi Tier A còn là một nhóm. Giờ chúng phải đọc là **Tier A-VN**, và **tỷ lệ tách giữa hai phạm vi hiện chưa ai biết** — Cổng 0.1 sẽ đo. Nếu Tier A-VN chỉ chiếm một nửa Tier A, mốc thật là ~12/tuần chứ không phải 25. **Không sửa số ở đây bằng cách đoán; hiệu chỉnh lại sau khi có dữ liệu.**

| Chỉ số | Tháng 6 | Tháng 12 |
|---|---|---|
| Tin Tier A-VN/tuần *(cần hiệu chỉnh)* | 25 | 60 |
| Độ chính xác nhãn (kiểm tay 50 tin/tháng) | ≥ 85% | ≥ 90% |
| Tỷ lệ "Không rõ" trên tổng thu thập | Đo, chưa đặt mục tiêu | Giảm so với tháng 6 |
| Người đăng ký bản tin | 600 | 3.000 |
| Tỷ lệ mở bản tin | ≥ 35% | ≥ 35% |
| Bản ghi bằng chứng cộng đồng | 60 (trong đó ≥ 20 Tier A) | 300 (≥ 100 Tier A) |
| Phiên tự nhiên/tháng | 3.000 | 15.000 |
| **Kết quả thật:** số người báo đã được phỏng vấn/nhận việc qua tin từ sản phẩm | ≥ 3 | ≥ 20 |

*Mục tiêu tháng 12 hạ so với v1.0 (100 tin/tuần → 60; 5.000 người đăng ký → 3.000; 30.000 phiên → 15.000) vì v1.0 không nêu cơ chế nào để supply tăng 3,3x, và vì dữ liệu suy giảm traffic tìm kiếm.*

**Dòng cuối bảng là chỉ số quan trọng nhất mà v1.0 không có:** tất cả các chỉ số khác đo *sản xuất*; dòng này đo *giá trị thực sự đến tay người dùng*. Nếu sau 12 tháng chưa có ai được phỏng vấn qua sản phẩm, các con số còn lại không có ý nghĩa.

### 12.3 Chỉ số phản biện

Bắt buộc theo dõi:
- **Tỷ lệ tin bị báo sai** — người dùng báo "tin này không tuyển được ở VN"
- **Tỷ lệ zombie** — tin đã lấp nhưng còn hiển thị. **Đây là vấn đề tuân thủ, không chỉ vấn đề chất lượng** (Mục 6.1)
- **Độ trễ gỡ tin hết hạn** — mục tiêu < 48h, có cảnh báo khi job gỡ tin lỗi
- **Độ chính xác nhãn theo nguồn** — nguồn nào sai nhiều thì giảm trọng số hoặc bỏ

### 12.4 Chỉ số cấm dùng

Không báo cáo, không ăn mừng: **tổng số tin trong database, tổng lượt xem trang, số trang đã xuất bản, tổng số người dùng đăng ký cộng dồn.**

*Về con số "96,5% trang web không có traffic" mà v1.0 trích: nghiên cứu này có thật (Ahrefs), nhưng chính Ahrefs ghi nhận hạn chế — mẫu ~14 tỷ trang trên chỉ mục 340,8 tỷ, thiên lệch về "phía chất lượng của web", và số liệu traffic là ước lượng. Dùng nó như một lời nhắc, không như một hằng số.*

---

## 13. Yêu cầu sản phẩm

### FR-1 → FR-6

Giữ từ v0.1/v1.0 (thu thập, chuẩn hoá, khử trùng lặp, làm giàu, hiển thị, tìm kiếm), với hai điều kiện bổ sung bắt buộc:
- Mọi tin phải mang đủ 5 nhãn của Mục 2.1, kể cả khi giá trị là "Không rõ"
- Mọi tin phải thuộc Lớp 1 hoặc Lớp 2 (Mục 6.1) và hành vi lập chỉ mục tuân theo lớp đó

### FR-7 — Vòng đóng góp cộng đồng (giải hard side)

**Nhóm yêu cầu quan trọng nhất về chiến lược.** Nhưng khác v1.0: **phải bắt đầu bằng nhập liệu tay, không bằng form.**

- FR-7.0 **(mới, làm trước tiên)** Công cụ nội bộ để người sáng lập nhập tay bản ghi bằng chứng từ nguồn công khai, kèm dẫn nguồn. **Mục tiêu 50 bản ghi mồi trước khi mở form công khai.**
- FR-7.1 Nút "Tôi đã nộp tin này" → email theo dõi kết quả sau 2 tuần
- FR-7.2 Form đóng góp: cơ chế hợp đồng + dải lương theo vai trò/cấp độ/công ty
  - **Bắt buộc:** màn hình đồng ý riêng theo PDPL (Mục 6.2)
  - **Bắt buộc:** ngưỡng k-ẩn danh — không hiển thị nếu (công ty × chức danh × cấp độ) có < 5 bản ghi
  - **Bắt buộc:** rút lại đồng ý và xoá dữ liệu hoạt động thật
- FR-7.3 Xác nhận cộng đồng: "Công ty này tuyển được ở VN không?" — hiển thị số phiếu **kèm ngày**, vì thông tin này hết hạn
- FR-7.4 Ghi công người đóng góp (huy hiệu, xếp hạng) — động lực phi tiền tệ
- FR-7.5 **(mới)** Mọi bản ghi có ngày hết hạn hiển thị. Sau 18 tháng tự động chuyển sang "cần xác nhận lại"

### FR-8 — Vòng phản hồi chất lượng

- FR-8.1 Nút báo lỗi trên mọi tin, một cú bấm
- FR-8.2 Báo lỗi tự động đưa tin vào hàng chờ duyệt
- FR-8.3 Bảng theo dõi độ chính xác theo nguồn
- FR-8.4 **(mới)** Kiểm tay 50 tin/tháng, kết quả ghi vào bảng độ chính xác của NSM

### FR-9 — Tuân thủ (mới)

- FR-9.1 Job gỡ tin hết hạn chạy hằng ngày; cảnh báo khi lỗi; SLA 48h
- FR-9.2 Cờ Lớp 1/Lớp 2 điều khiển việc phát sinh schema và thẻ `noindex` — không cấu hình tay được
- FR-9.3 Nhật ký nguồn: mọi bản ghi ghi rõ lấy từ đâu, lúc nào, theo điều khoản nào
- FR-9.4 Trang thông báo xử lý dữ liệu + luồng rút đồng ý

---

## 14. Kiến trúc

Giữ thiết kế orchestrator + worker + verifier + human gate. Bốn nguyên tắc:

1. **Orchestrator là code, không phải LLM.** Máy trạng thái trong Postgres, mọi bước idempotent và có checkpoint.
2. **Không có trường dữ liệu nào không có nguồn.** Mọi trường làm giàu kèm trích dẫn câu trong mô tả gốc **và ngày**. Không có căn cứ → "Không rõ". "Không rõ" là giá trị hợp lệ và phải hiển thị ra, không được giấu.
3. **Sự thật cứng không đi qua LLM.** Tên công ty, ngày, URL, trạng thái, cờ Lớp 1/Lớp 2 — truy vấn database.
4. **(mới) Tuân thủ nằm trong schema, không nằm trong quy trình.** Lớp 1/Lớp 2 là cột trong database và nó quyết định render; không phụ thuộc vào việc ai đó nhớ đặt cờ đúng.

---

## 15. Lộ trình ưu tiên

### 15.1 Cổng 0 không nằm trong RICE

Ba phép kiểm ở Mục 3 là **cổng**, không phải hạng mục sản phẩm. v1.0 nhét chúng vào bảng RICE với Reach=10, Confidence=100% — vừa sai thang đo (RICE Reach là số người/kỳ, không phải điểm 1–10) vừa sai logic (một phép kiểm chưa chạy không thể có confidence 100%). Chúng đứng trước bảng.

### 15.2 Bảng RICE — thang đo và phép tính đã sửa

**Thang:** Reach = số người dùng duy nhất chạm tới/quý (ước lượng ở tháng 6). Impact ∈ {0,25 / 0,5 / 1 / 2 / 3}. Confidence = %. Effort = tuần-người.

*(v1.0 có ba lỗi: thang Reach dùng điểm 1–10 khiến điểm không so sánh được với chuẩn RICE; cột "Thứ tự" không khớp cột "Điểm" — bản tin 12,8 xếp thứ 7 trong khi mục 10,8 xếp thứ 2; và schema 21,6 xếp dưới pipeline 10,8.)*

| Hạng mục | R | I | C | E | Điểm | Hạng |
|---|---|---|---|---|---|---|
| Bản tin hằng tuần | 800 | 2 | 90% | 0,5 | **2.880** | 1 |
| Nội dung bản địa (cơ chế hợp đồng, thanh toán, thuế) | 3.000 | 2 | 70% | 3 | **1.400** | 2 |
| Rubric đủ điều kiện + pipeline làm giàu | 2.000 | 3 | 80% | 4 | **1.200** | 3 |
| Schema + Indexing API — **chỉ cho Lớp 1** | 1.500 | 2 | 60% | 2 | **900** | 4 |
| Vòng phản hồi chất lượng (FR-8) | 1.000 | 1 | 80% | 1 | **800** | 5 |
| Trang chuyên đề sinh theo chương trình | 4.000 | 1 | 40% | 3 | **533** | 6 |
| Vòng đóng góp cộng đồng (FR-7) | 500 | 3 | 50% | 3 | **250** | 7 |
| Giao diện đẹp | 2.000 | 0,25 | 90% | 4 | **113** | Cuối |

### 15.3 Thứ tự thi công thật ≠ thứ tự RICE

RICE không mã hoá phụ thuộc. Thứ tự thi công:

```
Cổng 0.1 (tỷ lệ cơ sở)     → verify: đọc tay 200 tin, có ba tỷ lệ
Cổng 0.2 (phía cầu)        → verify: 15 cuộc trao đổi, đếm số nói "rào cản là pháp lý"
Cổng 0.3 (phía cung)       → verify: ≥ 50 đăng ký từ 3 lần đăng thủ công
─────────── cổng: cả ba đạt mới đi tiếp ───────────
1. Rubric + pipeline làm giàu  → verify: 100 tin chấm tự động khớp ≥ 85% với chấm tay
2. Bản tin (chạy tay trước)    → verify: 4 số liên tiếp, tỷ lệ mở ≥ 35%
3. FR-7.0 nhập tay 50 bản ghi  → verify: 50 bản ghi có nguồn, ≥ 15 Tier A
4. Nội dung bản địa 5 bài      → verify: có bài xuất hiện trong câu trả lời AI hoặc top 20 Google sau 60 ngày
5. FR-9 tuân thủ + FR-8        → verify: gỡ tin hết hạn < 48h; kiểm tay tháng đầu ≥ 85%
6. Lớp 1 + schema              → verify: tin đầu tiên xuất hiện trên Google for Jobs
7. FR-7 form công khai         → verify: ≥ 10 bản ghi từ người ngoài trong 30 ngày
8. Trang chuyên đề             → chỉ làm nếu bước 4 chứng minh SEO còn tác dụng
9. Giao diện đẹp               → trần cứng 15% thời gian
```

**Ba nhận xét từ bảng và thứ tự:**
1. **Hai việc đầu tiên trong toàn dự án không cần code.** Không đổi so với v1.0, và đó là kết luận đúng nhất của v1.0.
2. **Bản tin đứng đầu RICE** vì effort cực thấp và nó là kênh không phụ thuộc Google. Trong bối cảnh traffic tìm kiếm giảm 33%, đây không còn là kênh "song song" như v1.0 xếp — **nó là kênh chính**.
3. **Trang chuyên đề sinh theo chương trình bị hạ confidence xuống 40%** vì đây chính xác là loại nội dung mà AI search bỏ qua, và vì Arc/Himalayas/Jobgether đã phủ ô đó.

---

## 16. Sổ giả định & tiêu chí dừng

### 16.1 Sổ giả định

| # | Giả định | Rủi ro | Cách kiểm | Chi phí | Kết quả làm hỏng dự án |
|---|---|---|---|---|---|
| **A1** | Có đủ tin remote quốc tế thực sự tuyển được ở VN | **Sinh tử** | Cổng 0.1 | 1 buổi | Tier A < 4% → dừng |
| **A1b** | **Tự động hoá được việc chấm nhãn** | **Sinh tử** | Cổng 0.1, số "Không rõ" | Cùng buổi | "Không rõ" > 60% → mô hình chi phí sai hoàn toàn |
| **A2** | Kỹ sư VN coi đây là vấn đề đáng tìm giải pháp | Cao | Cổng 0.3 | 2 giờ | < 15 đăng ký → dừng |
| **A3** | Có công ty nước ngoài trả tiền | Cao | Cổng 0.2 | 1 tuần | 0/15 quan tâm → chỉ còn affiliate, hạ toàn bộ dự báo |
| **A4** | **Traffic tự nhiên còn khả thi trong bối cảnh AI search** | **Cao** *(v1.0 xếp "trung bình" — sai, dữ liệu cho thấy suy giảm đã xảy ra)* | **Bộ prompt cố định, đo tay hằng tháng** — xem 16.1.1 | 30 phút/tháng | Sau 90 ngày vẫn 0 trích dẫn → SEO/GEO không phải kênh; dồn vào bản tin/cộng đồng |
| **A5** | Cộng đồng chịu đóng góp dữ liệu | **Cao** | 50 bản ghi mồi (FR-7.0) trước, rồi mở form, đo 30 ngày | 3 tuần | < 10 bản ghi từ người ngoài → không có hào |
| **A6** | **(mới)** Mô hình vận hành được trong khuôn khổ chính sách Google + PDPL | **Cao** | Rà pháp lý + đọc kỹ chính sách trước khi ra mắt | 300–800 USD | Không tuân thủ được → mô hình phải đổi hoặc dừng |
| **A7** | Khác biệt đủ để người dùng đổi sang — **so với Nhóm 2 (Real Work From Anywhere, TrulyRemoteWork), không phải so với Arc** | **Cao** *(nâng ở v2.3)* | Cho 10 kỹ sư xem song song bản tin của ta và **Real Work From Anywhere**, hỏi họ chọn gì và vì sao | 1 tuần | Không ai thấy khác biệt → định vị sai. Đây là phép so đúng: Nhóm 2 miễn phí và đã tồn tại |
| **A8** | **(mới)** Nhãn cơ chế hợp đồng là thứ kỹ sư thực sự quan tâm, không phải thứ ta nghĩ họ quan tâm | **Cao** | Cùng buổi với A7: hỏi 10 kỹ sư "biết công ty này trả lương cho bạn bằng EOR hay hợp đồng nhà thầu có đổi quyết định nộp của bạn không" | 0 (gộp) | Không ai thấy quan trọng → toàn bộ khác biệt còn lại sụp. **Đây giờ là giả định nền của định vị** (Mục 5.1) |

**A1 và A1b phải kiểm trước khi viết một dòng code.**

#### 16.1.2 KẾT QUẢ CỔNG 0.1 (17/08/2026) — n=150, Tier A-VN = 0

Mẫu ngẫu nhiên 150 tin remote từ 3 ATS công khai (Greenhouse/Lever/Ashby, ~100 công ty), chấm tay **từ toàn văn** theo [rubric-spec.md](rubric-spec.md), qua 3 lô độc lập.

| | n=150 | |
|---|---|---|
| Loại trừ | 126 | 84,0% |
| Không rõ | 18 | 12,0% |
| Tier A-Global | 6 | 4,0% |
| **Tier A-VN** | **0** | **0,0%** |

**Cận trên khoảng tin cậy 95% chính xác cho 0/150 = 1,98%.**

| Dải ngưỡng ở Mục 3 | Trạng thái |
|---|---|
| Tier A-VN ≥ 5% — tiếp tục theo kế hoạch | **Loại trừ** |
| Tier A-VN 2–5% — thu hẹp ngách | **Loại trừ** |
| **Tier A-VN < 2% — DỪNG** | **Đạt.** Cận trên 1,98% nằm dưới ngưỡng |

**Tiêu chí dừng do chính tài liệu này đặt ra, trước khi đo, đã được kích hoạt.**

#### Ba đường thoát đều đã đóng

1. **"Số 0 chỉ là cận dưới, 18 tin Không rõ chưa điều tra."** Tầng 4 (điều tra mức công ty, quét toàn bộ board) đã chạy trên 13 tin Không rõ / 10 công ty → **0 tin được nâng lên Tier A-VN**. Một dương tính giả (`cursor` — APJ là thị trường kinh doanh, không phải nơi tuyển), một tín hiệu yếu (`category-labs` — EOR không nêu quốc gia, là B-04).
2. **"Nhãn máy sai."** Đối chứng tay 180 tin: Tier A precision 100%, DQ recall 100%, accuracy 100%.
3. **"Chưa đủ mẫu."** n=150 đưa cận trên xuống dưới ngưỡng do chính tài liệu đặt.

#### Điều CHƯA kết luận được — và nó quan trọng

**Vai trò kỹ thuật riêng (đúng atomic network) chỉ n=68, cận trên 4,31%.** Ngưỡng 2% **chưa** loại trừ được cho nhóm mục tiêu thật. Muốn dứt điểm riêng cho nhóm này cần ~150 tin kỹ thuật ngẫu nhiên.

Đây là mảnh dữ liệu duy nhất còn thiếu trước khi quyết định cuối cùng. Chi phí: khoảng 4 giờ chấm tay.

**Giới hạn mẫu, nêu để không tự lừa:** nguồn slug là Hacker News → thiên về công ty Mỹ/EU. Đây là nơi có mật độ việc remote cao nhất, nhưng chưa chắc là nơi tuyển được ở VN nhiều nhất. Một mẫu từ nguồn châu Á/châu Âu có thể cho kết quả khác — nhưng cũng chính là mẫu có ít việc remote hơn.

#### Điều dữ liệu nói về luận điểm sản phẩm

Thứ **tồn tại** ở mức 4% là Tier A-Global — tin mở toàn cầu. Theo Mục 5.1, đó đúng là thứ Real Work From Anywhere và TrulyRemoteWork **đã xuất bản miễn phí hằng tuần**.

Thứ được cho là **khác biệt** — bằng chứng riêng cho Việt Nam — có **0 quan sát trong 150 tin ngẫu nhiên**. Tin Tier A-VN duy nhất tìm được trong cả quá trình (`colonist`, ~1.900 tin remote đã quét) nằm ở lô lấy phân tầng, không phải mẫu ngẫu nhiên.

Nó tồn tại. Nhưng ở mật độ này, **không đủ để nuôi một bản tin hằng tuần** — mục tiêu 25 tin Tier A-VN/tuần ở Mục 12.2 đòi quét khoảng 12.500 tin remote mỗi tuần ở tỷ lệ 0,2%.

#### Ba lựa chọn, không phải một

| | Nội dung | Điều kiện |
|---|---|---|
| **A. Dừng** | Tiêu chí dừng đã kích hoạt. Chi phí đã bỏ: một buổi | Nếu chấp nhận n=150 là đủ |
| **B. Đo nốt nhóm kỹ thuật** | ~150 tin kỹ thuật ngẫu nhiên, ~4 giờ | Nếu muốn dứt điểm cho đúng atomic network trước khi bỏ |
| **C. Đổi định vị** | Bỏ tầng "bằng chứng VN", chuyển sang tầng **cơ chế hợp đồng** cho tin worldwide (4%) — thứ Nhóm 2 không làm (Mục 5.1) | Nếu tin rằng A8 đúng: nhãn cơ chế là thứ kỹ sư thực sự cần |

Lựa chọn C đáng cân nhắc vì nó dùng đúng dữ liệu **có thật** (4% worldwide) thay vì dữ liệu **không có** (0% VN-specific), và vẫn giữ được điểm khác biệt đã kiểm chứng: không board nào gắn nhãn cơ chế hợp đồng. Nhưng nó **phụ thuộc hoàn toàn vào A8** — giả định chưa từng được hỏi.

### 16.2 Tiêu chí dừng — logic đã sửa

**Lỗi của v1.0:** ngưỡng dừng tháng 6 (1.000 người đăng ký, 5.000 phiên) **trùng đúng bằng mục tiêu tháng 6**, nối bằng "VÀ", và cần cả ba cùng sai. Nghĩa là gần như không bao giờ kích hoạt — đó là tiêu chí dừng để cảm thấy an tâm, không phải để dừng.

**v2.0: logic HOẶC, và ngưỡng dừng đặt ở mức thấp hơn hẳn mục tiêu để có biên.**

**Dừng ở tháng 6 nếu BẤT KỲ điều nào đúng:**
- Người đăng ký bản tin < 250 (mục tiêu 600)
- Độ chính xác nhãn < 70% sau hai tháng cố cải thiện
- Số người báo đã được phỏng vấn qua tin từ sản phẩm = 0
- Bản ghi bằng chứng cộng đồng < 25 (mục tiêu 60)

**Dừng bất kỳ lúc nào nếu:**
- Tier A < 4% và không cải thiện sau 2 tháng
- Nhận manual action từ Google hoặc thông báo vi phạm PDPL
- Nguồn dữ liệu chính bị chặn và không có nguồn thay thế trong 1 tháng
- Tần suất làm việc thực tế < 5h/tuần trong 6 tuần liên tiếp — **đây là tín hiệu dừng, không phải tín hiệu cố thêm**

**Cam kết trước, ghi ngày:** ngày rà tiêu chí dừng là **17/02/2027**. Đặt lịch ngay bây giờ. Tháng thứ 6 sẽ khó khách quan hơn nhiều — v1.0 nói đúng điều này, nhưng rồi lại đặt ngưỡng không thể kích hoạt.

---

## 17. Pre-mortem

*Giả sử 18 tháng nữa dự án thất bại. Nguyên nhân là gì?*

| # | Kịch bản | Xác suất | Dấu hiệu sớm | Phòng ngừa |
|---|---|---|---|---|
| 1 | **Không đủ tin Tier A** — chỉ 2% tin remote tuyển được ở VN | Cao | Cổng 0.1 | Kiểm trước tiên |
| 1b | **Không chấm nhãn tự động được** — quá nhiều "Không rõ", phải điều tra tay từng tin | **Cao** *(mới)* | Tỷ lệ "Không rõ" cao ở Cổng 0.1 | Nếu xảy ra: đổi sang mô hình bản tin thủ công cao cấp, quy mô nhỏ, thu phí người dùng |
| 2 | **Xây tính năng thay vì xây khán giả** | **Rất cao** | Nhiều commit, ít người đăng ký | Mục 15.3; trần cứng 15% cho giao diện |
| 3 | **Traffic tự nhiên không đến** — và cửa trước dịch sang trợ lý AI (Mục 5.2) | **Cao** *(v1.0 xếp trung bình)* | Bộ prompt A4 (16.1.1) cho 0 trích dẫn sau 90 ngày | Bản tin là kênh chính từ đầu, không phải kênh dự phòng. Đo GEO hằng tháng, không hằng quý |
| 4 | **Có traffic nhưng không ai trả tiền** | Cao | Cổng 0.2 cho kết quả nhạt | Bắt đầu bằng affiliate — dòng tiền không phụ thuộc phía cầu |
| 5 | **Bị sao chép** | Trung bình | Xuất hiện board tương tự | Chỉ lịch sử bằng chứng chống được; ưu tiên FR-7.0 |
| 6 | **Cạn kiên nhẫn** | **Rất cao** | Tần suất làm việc giảm | Tiêu chí dừng có ngày cụ thể; mốc thắng nhỏ hằng tháng; affiliate cho dòng tiền sớm dù nhỏ |
| 7 | **Nguồn dữ liệu bị chặn** | Trung bình | Lỗi đồng bộ tăng | Ưu tiên feed ATS chính thức; không phụ thuộc một nguồn |
| 8 | **Google manual action** vì tin không ủy quyền hoặc tin hết hạn | **Trung bình–cao** *(mới)* | Cảnh báo trong Search Console; job gỡ tin lỗi | Kiến trúc hai lớp (6.1); FR-9.1 |
| 9 | **Vi phạm PDPL** ở dữ liệu lương hoặc dòng doanh thu ứng viên | Trung bình *(mới)* | Không có nhật ký đồng ý; hiển thị lương với mẫu quá nhỏ | Mục 6.2; ngưỡng k-ẩn danh trong code |
| 10 | **Đối thủ sẵn có đủ tốt** — Nhóm 2 (Real Work From Anywhere, TrulyRemoteWork) đã giải quyết "đủ tốt", miễn phí | **Cao** *(nâng ở v2.3)* | A7/A8 cho kết quả nhạt · phép kiểm trùng lặp ở Cổng 0.1 cho tỷ lệ trùng cao | Định vị vào **tầng bằng chứng cơ chế**, không vào tầng lọc. Nếu nhãn cơ chế không quan trọng với người dùng (A8 sai) thì không còn gì để dựng |
| 11 | **Tự lừa mình bằng Tier A-Global** — đếm tin đã miễn phí ở nơi khác như thành tích, chỉ số đẹp mà không tạo giá trị mới | **Cao** *(mới)* | Tier A/tuần tăng nhưng Tier A-VN đứng yên | Cặp North Star chỉ đếm Tier A-VN (Mục 12.1); ràng buộc DB-4 ở PRD chặn việc gộp hai phạm vi thành một số |
| 12 | **Mâu thuẫn hai phía lộ ra** — kỹ sư thấy sản phẩm giúp công ty ép giá | Thấp–trung bình *(mới)* | Phản ứng tiêu cực trong cộng đồng | Mục 8.3: đứng công khai về phía kỹ sư, không giả vờ trung lập |

**Nhận định giữ nguyên từ v1.0 và vẫn là câu quan trọng nhất trong tài liệu:** hai kịch bản xác suất cao nhất (#2 và #6) **đều là rủi ro hành vi, không phải rủi ro thị trường.** Mối đe doạ lớn nhất không nằm ở thị trường mà ở việc chọn sai thứ để làm mỗi tuần, và ở việc mất kiên nhẫn.

v2.0 bổ sung một nhận định thứ hai: **các kịch bản mới (#1b, #8, #9, #10) đều là những thứ v1.0 không thấy vì chưa kiểm chứng bên ngoài tài liệu.** Đó là lập luận cho việc chạy Cổng 0 sớm — không phải để xác nhận điều mình tin, mà để tìm ra điều mình chưa biết.

---

## 18. Quyết định cần chốt trước khi bắt đầu

1. **Atomic network.** Đề xuất: React/Node/Python, 3+ năm, nhắm múi giờ châu Âu (lý do trong 9.2). Ngách thứ cấp GMT+8..+11 để dành cho giai đoạn ceiling. **Cần chốt.**

2. **Ngôn ngữ.** v1.0 hỏi "tiếng Việt hay tiếng Anh". Câu trả lời không phải một trong hai — **là tách theo bề mặt:**
   - Nội dung bản địa (thuế, thanh toán, cơ chế hợp đồng, đàm phán lương): **tiếng Việt** — đây là nơi có con hào và nơi không ai cạnh tranh
   - Trang chi tiết tin + trang cho nhà tuyển dụng: **tiếng Anh** — Google for Jobs và phía cầu đều ở tiếng Anh; tiếng Việt cắt mất bề mặt tìm kiếm
   - Bản tin: **tiếng Việt**, tiêu đề tin giữ nguyên tiếng Anh

3. **Điều khoản làm ngoài giờ trong hợp đồng lao động hiện tại** — đọc trước khi bắt đầu. Đặc biệt điều khoản sở hữu trí tuệ và không cạnh tranh.

4. **Ngân sách rà soát pháp lý 300–800 USD** — chấp nhận hay không. Nếu không, mô hình phải thu hẹp về chỉ nội dung + affiliate, bỏ toàn bộ phần thu thập dữ liệu lương.

5. **Khung thời gian 12–24 tháng** — chấp nhận hay không. Nếu mục tiêu là dòng tiền trong 3 tháng, mô hình này sai và nên dừng tại đây.

6. **(mới) Trần thời gian mỗi tuần và ngày rà tiêu chí dừng.** Đề xuất: 10h/tuần, rà ngày 17/02/2027. Ghi vào lịch bây giờ.

---

## 19. Delta v1.0 → v2.0

| # | Vấn đề trong v1.0 | Mức | Đã sửa thế nào |
|---|---|---|---|
| 1 | Ví dụ định vị "47/1000" = 4,7%, thấp hơn chính ngưỡng dừng 5% của nó | Nghiêm trọng | Bỏ số minh hoạ (1.2); ngưỡng đặt lại thành thang ba mức (Cổng 0.1) |
| 2 | "Tin đủ điều kiện" chưa từng được định nghĩa, dù mọi chỉ số phụ thuộc vào nó | Nghiêm trọng | Mục 2 mới: 5 nhãn, thang Tier A/B, quy tắc loại trừ, khoá phiên bản rubric |
| 3 | Không có tầng pháp lý: chính sách Google, PDPL, điều khoản nguồn | Nghiêm trọng | Mục 6 mới; kiến trúc hai lớp; FR-9; A6 |
| 4 | Dòng thu "quyền truy cập ứng viên" vi phạm lệnh cấm mua bán dữ liệu cá nhân của PDPL | Nghiêm trọng | Bỏ, thay bằng giới thiệu có đồng ý (11.3) |
| 5 | Bảng RICE: thang Reach sai chuẩn, cột thứ tự không khớp cột điểm, confidence 100% | Nghiêm trọng | Mục 15 tính lại; cổng tách khỏi RICE; thêm thứ tự thi công theo phụ thuộc |
| 6 | Rào cản thật (pháp nhân/EOR) gần như không xuất hiện | Nghiêm trọng | Mục 4 mới; đưa vào rubric và vào mô hình doanh thu |
| 7 | Tiêu chí dừng = mục tiêu, nối bằng "VÀ" → không thể kích hoạt | Cao | 16.2: logic HOẶC, ngưỡng thấp hơn mục tiêu, có ngày rà cụ thể |
| 8 | Mâu thuẫn: "hiệu ứng mạng = 0 trong 12 tháng" vs "hard side là người đóng góp" | Cao | 9.1: gọi đúng tên là data network effect, phải nuôi từ tháng 1 |
| 9 | Vòng lặp cold start của hard side bị khoá (cần người đã được nhận, mà chưa ai được nhận) | Cao | 9.3 + FR-7.0: 50 bản ghi mồi nhập tay trước khi mở form |
| 10 | Không có phân tích đối thủ trực tiếp | Cao | Mục 5: Arc, Himalayas, Jobgether, nhóm Facebook |
| 11 | Mâu thuẫn lợi ích hai phía không được nêu | Cao | 8.3: đứng công khai về phía kỹ sư |
| 12 | A4 (AI search) xếp rủi ro trung bình | Cao | Nâng lên Cao kèm dữ liệu; bản tin thành kênh chính |
| 13 | Chi phí LLM ước lượng thiếu ~3x | Trung bình | 11.1 tính lại; nêu rõ thiên lệch ước lượng |
| 14 | Mỏ neo doanh thu RemoteOK "35.000 USD/tháng" không kiểm chứng được | Trung bình | 11.2: nêu các nguồn mâu thuẫn, bỏ mỏ neo |
| 15 | NSM đo sản xuất, không đo giá trị đến tay người dùng; và gian lận được bằng cách nới rubric | Trung bình | 12.1 thành cặp số; thêm dòng "số người được phỏng vấn qua sản phẩm" |
| 16 | Mục tiêu tháng 12 (100 tin/tuần, 5.000 đăng ký) không có cơ chế | Trung bình | 12.2 hạ mục tiêu, kèm lý do |
| 17 | Mốc moat 500 bản ghi không nối được với ngưỡng dừng 50 bản ghi | Trung bình | 9.4 hạ xuống 300, thêm điều kiện chất lượng Tier A |
| 18 | Chọn múi giờ châu Âu không nêu phép tính | Trung bình | 9.2 nêu rõ phép tính overlap và đánh đổi khối lượng |
| 19 | Câu hỏi ngôn ngữ đặt sai (một trong hai) | Trung bình | 18.2 tách theo bề mặt |
| 20 | Nguồn tham khảo dựa chủ yếu vào blog của một nhà cung cấp phần mềm job board | Trung bình | Phụ lục B: nguồn sơ cấp, kèm ghi chú xung đột lợi ích |
| 21 | Zombie job coi là vấn đề chất lượng | Thấp–TB | Nâng thành vấn đề tuân thủ (6.1, 12.3, FR-9.1) |

### Delta v2.0 → v2.1 (nghiên cứu vòng 2)

| # | Thay đổi | Nguồn |
|---|---|---|
| 22 | **Sửa chính bản sửa lỗi:** chi phí LLM ở v2.0 (100–250 USD/tháng) cao hơn thực tế ~1 bậc độ lớn. Số đúng: 5–35 USD/tháng. v2.0 sai nhiều hơn v1.0, theo hướng ngược lại | Giá công bố + kiến trúc pipeline (Mục 11.1, PRD 9.2) |
| 23 | **Chọn model theo độ chính xác, không theo giá** — chênh lệch model rẻ nhất/mạnh nhất chỉ ~14 USD/tháng | Rubric Spec 14.1 |
| 24 | **Dòng affiliate có đơn giá lớn hơn nhiều so với giả định:** Deel trả 1.500 USD/khách mới. Nhưng nó phụ thuộc kết quả tuyển dụng thành công — cùng vòng khoá với hard side | Điều khoản công bố (Mục 11.3.1) |
| 25 | Cảnh báo doanh thu affiliate là **cục bộ**, không phải dòng tiền định kỳ | Mục 11.2 |
| 26 | R10 (bản đồ cộng đồng dev VN) **không giải được bằng nghiên cứu bàn giấy** — dữ liệu công khai quá mỏng. Vẫn là việc thực địa | next-steps R10 |

### Delta v2.1 → v2.2 (nghiên cứu vòng 3)

| # | Thay đổi | Nguồn |
|---|---|---|
| 27 | **Sửa tuyên bố ATS API "giải bài toán điều khoản sử dụng":** không nhà cung cấp nào công bố điều khoản cho phép bên thứ ba tổng hợp lại. Đúng hơn: giảm rủi ro đáng kể, không xoá rủi ro | Mục 6.3, PRD Q7 |
| 28 | **Poll hằng ngày toàn bộ danh sách là mẫu bị chặn**, không phải mẫu an toàn. Thêm phân bậc slug + tần suất theo bậc; giảm tải 5 lần | PRD Mục 7.1 (hướng dẫn vận hành Greenhouse) |
| 29 | Chế độ giới hạn tốc độ **khác nhau theo ATS** — không viết một lớp lùi dùng chung. Ashby không công bố ngưỡng và không trả header | PRD M2 |
| 30 | Yêu cầu gửi email cụ thể hoá: RFC 8058, DMARC + alignment, tỷ lệ spam mục tiêu < 0,10%. Tuân thủ ≈ 89% vào inbox; không tuân thủ 22–34% vào spam | PRD FR-6.3/6.4/6.7 |
| 31 | Hạn ngạch Indexing API (200/ngày) không phải ràng buộc, nhưng **hạn ngạch co lại theo chất lượng tài liệu** — thêm một lý do độc lập cho kiến trúc hai lớp | PRD FR-9.7 |
| 32 | Cơ chế truy vấn Common Crawl CDX cụ thể hoá (miễn phí, `cdx-index-client`, truy vấn theo bản chụp, tự giới hạn tốc độ) | PRD FR-1.1 |

### Delta v2.2 → v2.3 (nghiên cứu vòng 4 — thay đổi lớn nhất từ v2.0)

| # | Thay đổi | Nguồn |
|---|---|---|
| **33** | **Bỏ sót cả một nhóm đối thủ.** Board "work from anywhere" duyệt tay (Real Work From Anywhere, TrulyRemoteWork, Truly Remote, We Are Distributed) đã làm đúng tầng lọc mà rubric của ta mô tả — hằng tuần, miễn phí, bằng tay | Mục 5, nhóm 2 |
| **34** | **Đổi định nghĩa North Star:** đếm **Tier A-VN**, không đếm Tier A tổng. Tin chỉ có bằng chứng "worldwide" là đăng lại thứ đã miễn phí | Mục 12.1, Rubric Spec 5.1 |
| **35** | **Đổi ngưỡng dừng Cổng 0.1:** keo vào Tier A-VN, hạ từ 4% xuống 2% vì mẫu số đổi. Thêm trạng thái cảnh báo "Tier A cao nhưng gần như toàn Global" | Mục 3 |
| **36** | Khác biệt dịch chỗ: **không phải "lọc tốt hơn", là "gắn nhãn cơ chế"**. Ba trong bốn câu hỏi định vị chưa ai trả lời; câu thứ tư thì đã có, miễn phí | Mục 1.1, 5.1 |
| **37** | Nhóm 2 **là kênh, không chỉ là đối thủ** — họ đã lọc sẵn tập "worldwide", dùng làm nguồn đầu vào chất lượng cao | Mục 5.1 |
| **38** | Arc.dev thu **25–30% trên lương** (dòng doanh thu chính), 3,8 triệu USD ARR, đã có lãi. Là **bên đương nhiệm mà định vị tấn công**, không phải đối tác | Mục 5, 8.2 |
| **39** | **Ranh giới con hào dữ liệu lương:** levels.fyi đã có VN ở mức tổng hợp. Lát cắt chưa ai có là **chủ lao động nước ngoài × cơ chế hợp đồng** — hai trường bắt buộc trong FR-7.2 | Mục 10.3 |
| **40** | Vùng phủ EOR **không lấy tự động được** — không nhà cung cấp nào có endpoint danh mục quốc gia. A-06 là tín hiệu mạnh nhất và khó tự động nhất | Rubric Spec 5.1 |
| **41** | Mốc "tin Tier A/tuần" ở 9.4 và 12.2 **phải hiệu chỉnh lại** sau Cổng 0.1 — tỷ lệ tách hai phạm vi chưa ai biết. Không đoán | Mục 12.2 |

### Delta v2.3 → v2.4 (nghiên cứu vòng 5)

| # | Thay đổi | Nguồn |
|---|---|---|
| **42** | **Con hào nội dung là guồng quay, không phải tài sản.** Luật thuế VN đổi hai lần trong 2026; nội dung <30 ngày được AI trích dẫn nhiều hơn hẳn. Hai sự thật nhân với nhau: giữ hiện hành phục vụ cả con hào lẫn kênh — và ngừng quay là mất cả hai | Mục 10.1 |
| **43** | **A4 lần đầu có phương pháp đo:** bộ 10–15 prompt cố định, 3 engine, đo tay hằng tháng, 30 phút. Công cụ chuyên dụng (~150 USD/tháng) vượt toàn bộ ngân sách | Mục 16.1.1 |
| **44** | Tách **nhắc đến** và **trích dẫn** — trích dẫn mới là tín hiệu thẩm quyền. Đo nhầm hai cái này là đo sai | Mục 16.1.1 |
| **45** | Nhịp đo GEO là **hằng tháng, không hằng quý** — Perplexity đánh trọng số độ mới rất cao, mẫu trích dẫn đổi trong 48 giờ | Mục 16.1.1 |
| **46** | **Nhóm đối thủ thứ 4: trợ lý AI tìm việc.** ChatGPT đã kéo tin trực tiếp từ Indeed/Upwork/Appcast và lọc theo múi giờ. Đe doạ tầng lọc, **không chạm được tầng bằng chứng** — không mô hình nào suy ra thứ chưa được viết xuống | Mục 5.2 |
| **47** | Khung thuế VN cụ thể hoá: **Nghị định 253/2026/NĐ-CP** (hiệu lực 01/07/2026), nghĩa vụ kê khai thu nhập toàn cầu bất kể nơi trả/nơi nhận, giảm trừ 15,5 triệu/tháng, khấu trừ theo Hiệp định tránh đánh thuế hai lần. Đường hộ kinh doanh **vẫn chưa xác minh** — câu số một cho kế toán | Mục 4.3 |
| **48** | Bốn câu hỏi cho buổi tư vấn kế toán, xếp theo giá trị | Mục 4.3 |

### Delta v2.4 → v2.5 (đọc toàn văn hai khối văn bản)

| # | Thay đổi | Nguồn |
|---|---|---|
| **49** | **Sửa chồng văn bản PDPL:** Nghị định 356/2025 **thay thế hoàn toàn** Nghị định 13/2023 — bản trước ghi mơ hồ "thay thế/kế thừa". Nghị định 13 đã hết hiệu lực; nhiều bài viết đang lưu hành vẫn tham chiếu nó | Mục 6.2 |
| **50** | **Phát hiện cấu trúc miễn trừ:** doanh nghiệp siêu nhỏ/hộ kinh doanh miễn DPO hoàn toàn; doanh nghiệp nhỏ hoãn 5 năm; DPIA được chọn không lập 5 năm đầu. **Nhưng mất sạch nếu xử lý dữ liệu nhạy cảm** | Mục 6.2 |
| **51** | **Xác định câu hỏi pháp lý đắt nhất:** dữ liệu lương có phải dữ liệu nhạy cảm không. Là ranh giới giữa chi phí tuân thủ gần bằng không và chi phí thật | Mục 6.2, legal-brief B-Q1 |
| **52** | **Google không có điều khoản nào cấm tin trùng lặp hay tin tổng hợp.** Điều khoản "không có ủy quyền" nằm dưới mục *xuyên tạc* như một ví dụ, không phải quy tắc riêng — gợi ý mục tiêu là hành vi lừa dối, không phải tổng hợp | legal-brief A.2 |
| **53** | **Mặc định an toàn cho phép chạy tới hết M2 mà không chạm câu hỏi mở nào.** Buổi tư vấn chặn M3, không chặn tiến độ | legal-brief D.2 |
| **54** | Soạn xong [legal-brief.md](legal-brief.md): 15 câu hỏi có trích dẫn nguyên văn, thứ tự ưu tiên, và danh sách "điều không cần hỏi" | R11 đóng |

---

## 20. Phụ lục

### Phụ lục A — Framework đã dùng

| Framework | Mục | Nguồn |
|---|---|---|
| Lean Canvas | 7 | Ash Maurya |
| Jobs-to-be-Done | 8 | Clayton Christensen |
| Cold Start Theory | 9 | Andrew Chen, *The Cold Start Problem* |
| 7 Powers | 10 | Hamilton Helmer |
| Unit economics | 11 | Chuẩn ngành SaaS/marketplace |
| North Star + counter-metrics | 12 | Amplitude / Sean Ellis |
| RICE | 15 | Intercom |
| Pre-mortem | 17 | Gary Klein |

### Phụ lục B — Nguồn sơ cấp đã kiểm chứng cho v2.0

**Chính sách Google**
- Chính sách nội dung & hướng dẫn kỹ thuật JobPosting (ủy quyền, cách nộp hồ sơ, gỡ tin hết hạn, manual action): https://developers.google.com/search/docs/appearance/structured-data/job-posting
- Hướng dẫn structured data chung: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google ngừng Job Ads trả phí (2024): https://www.talivity.com/industry-insights/breaking-google-to-discontinue-google-job-ads-amidst-recent-layoffs/

**Pháp lý Việt Nam**
- Luật BVDLCN 91/2025/QH15 (toàn văn tiếng Anh): https://english.luatvietnam.vn/dan-su/law-on-personal-data-protection-law-no-91-2025-qh15-405135-d1.html
- Phân tích lệnh cấm mua bán dữ liệu cá nhân & chế tài: https://www.tilleke.com/insights/vietnams-new-personal-data-protection-law-a-closer-look/
- Tổng quan tuân thủ: https://rouse.com/insights/news/2025/vietnam-s-new-personal-data-protection-law-what-businesses-need-to-know
- Bảo vệ dữ liệu tại VN (tổng hợp): https://www.dlapiperdataprotection.com/?t=law&c=VN

**Cơ chế tuyển dụng & chi phí**
- EOR tại Việt Nam, chi phí và đóng góp: https://www.deel.com/blog/employer-of-record-vietnam/
- Hướng dẫn tuân thủ khi tuyển tại VN: https://www.unkoa.com/how-to-hire-in-vietnam-without-breaking-four-laws-at-once-2026-guide/

**Suy giảm traffic tìm kiếm**
- Báo cáo khủng hoảng traffic tự nhiên 2026: https://thedigitalbloom.com/learn/organic-traffic-crisis-report-2026-update/
- Thống kê AI Overviews 2026: https://quickseo.ai/blog/google-ai-overviews-statistics-2026-60-data-points-every-seo-should-know
- Tác động lên publisher và cách thích ứng: https://www.searchenginejournal.com/impact-of-ai-overviews-how-publishers-need-to-adapt/556843/
- Nghiên cứu Ahrefs 96,55% (kèm phần tự nêu hạn chế): https://ahrefs.com/blog/search-traffic-study/

**Đối thủ**
- Arc.dev trang remote VN: https://arc.dev/en-vn/remote-jobs
- Mô hình doanh thu Arc.dev (25–30% Arc Connect, 15–20% tuyển dụng, 3,8 triệu USD ARR): https://talmatic.com/blog/review/arc-dev-reviews/
- Himalayas trang theo quốc gia: https://himalayas.app/jobs/countries/vietnam/software-development
- Jobgether trang remote VN: https://jobgether.com/remote-jobs/vietnam
- VietnamDevs: https://vietnamdevs.com/remote-jobs

**Đối thủ nhóm 2 — board "work from anywhere" duyệt tay** *(bổ sung v2.3)*
- Real Work From Anywhere (~292 tin, miễn phí, bản tin tuần): https://www.realworkfromanywhere.com/
- TrulyRemoteWork (duyệt tay từng tin, kiểm giới hạn quốc gia/múi giờ/chuyển chỗ ẩn): https://trulyremotework.com/
- Truly Remote: https://trulyremote.co/?locations=Worldwide
- We Are Distributed: https://wearedistributed.org/jobs

**Thuế Việt Nam** *(bổ sung v2.4 — vẫn cần kế toán xác nhận, không dùng làm nguồn xuất bản)*
- Nghị định 253/2026/NĐ-CP, quy định về cá nhân cư trú: https://lsvn.vn/nghi-dinh-253-2026-nd-cp-quy-dinh-the-nao-ve-ca-nhan-cu-tru-a175324.html
- Hướng dẫn Luật Thuế TNCN từ 01/7/2026: https://ketoanleanh.edu.vn/kinh-nghiem-ke-toan/nghi-dinh-253-2026-nd-cp-huong-dan-luat-thue-tncn.html
- Thay đổi về giảm trừ, miễn thuế và quyết toán: https://easyhrm.vn/tin-tuc/nghi-dinh-so-253-2026-nd-cp/

**Đo lường AI search** *(bổ sung v2.4)*
- Khung theo dõi trích dẫn AI và share of voice: https://www.digitalapplied.com/blog/ai-share-of-voice-tracking-brand-citations-framework-2026
- So sánh công cụ giám sát AI search (giá, phủ engine): https://www.useomnia.com/blog/ai-search-monitoring-tools
- Trợ lý AI tìm việc kéo tin trực tiếp: https://findskill.ai/blog/chatgpt-job-search-resume-15-minutes/

**Ranh giới dữ liệu lương** *(bổ sung v2.3)*
- levels.fyi trang Việt Nam: https://www.levels.fyi/t/software-engineer/locations/vietnam
- Cổng developer Deel (API vận hành, không phải danh mục vùng phủ): https://developer.deel.com/api/global-payroll/introduction

**Affiliate / đối tác** *(bổ sung v2.1)*
- Chương trình affiliate Deel (500 + 1.000 USD, cookie 90 ngày, PartnerStack): https://www.deel.com/partner/affiliates/
- Chương trình đối tác Deel (chia doanh thu, nhiều bậc): https://www.deel.com/partner-program/
- Chương trình affiliate Oyster (CPA / chia doanh thu, mức chưa công bố): https://theaffiliatemonkey.com/affiliate/oyster-affiliate-program/

**Nguồn dữ liệu ATS** *(bổ sung v2.1, mở rộng v2.2)*
- 6 nền tảng ATS có API việc làm công khai: https://fantastic.jobs/article/ats-with-api
- So sánh API đăng tin của Workday, Greenhouse, Lever, Ashby, SmartRecruiters, Recruitee: https://cavuno.com/blog/ats-platforms-public-job-posting-apis
- Tài liệu Job Board API của Greenhouse: https://developers.greenhouse.io/job-board.html
- Greenhouse: giới hạn tốc độ và hành vi bóp nghẹt bên gọi lạm dụng: https://jobspipe.dev/guides/greenhouse-jobs-api
- Ashby: giới hạn theo khoá, 429 + `Retry-After`, ngưỡng không công bố: https://apis.io/rate-limits/ashby/ashby-rate-limits/
- Máy chủ chỉ mục Common Crawl: https://index.commoncrawl.org/
- `cdx-index-client` (CLI truy vấn hàng loạt): https://github.com/ikreymer/cdx-index-client

**Hạ tầng kênh** *(bổ sung v2.2)*
- Yêu cầu người gửi hàng loạt của Gmail (ngưỡng 5.000/ngày, DMARC, tỷ lệ spam, RFC 8058): https://support.google.com/a/answer/14229414
- Danh sách kiểm tuân thủ Microsoft/Google/Yahoo 2026: https://redsift.com/guides/bulk-email-sender-requirements
- Hạn ngạch Indexing API và cách xin tăng: https://developers.google.com/search/apis/indexing-api/v3/quota-pricing

**Lương**
- Lương dev remote tại VN: https://arc.dev/salaries/software-engineers-in-vietnam
- Lương dev VN cho nhà tuyển dụng quốc tế: https://vietnamdevs.com/blog/vietnam-software-developer-salaries-2026-guide-for-international-recruiters
- Khảo sát lương Robert Walters VN: https://www.robertwalters.com.vn/our-services/salary-survey/software-engineer-salaries.html

### Phụ lục C — Ghi chú về chất lượng bằng chứng

**Nguồn đã bị hạ trọng số so với v1.0:**
- **Cavuno** — v1.0 dùng làm nguồn cho 3/8 tuyên bố thị trường. Cavuno bán phần mềm job board; họ có động cơ thương mại để kết luận rằng job board là mô hình tốt. Không dùng làm nguồn duy nhất cho bất kỳ quyết định nào.
- **Con số doanh thu RemoteOK** — các nguồn công khai mâu thuẫn nhau 5 lần (25k / 44k / 138k USD/tháng). Không dùng làm mỏ neo.
- **Số liệu SEO từ blog công cụ SEO** — mọi công cụ SEO đều có động cơ khiến SEO trông vừa quan trọng vừa khó. Số liệu suy giảm traffic ở Mục 0 và 16 được lấy từ nhiều nguồn độc lập, nhưng vẫn nên coi là chỉ dấu về hướng, không phải con số chính xác.

**Điều chưa ai biết:**
- **Không có nghiên cứu công khai nào đo tỷ lệ tin remote thực sự tuyển được toàn cầu.** Cổng 0.1 sẽ tạo ra con số này. Nếu dự án chỉ tạo ra một thứ có giá trị, có thể chính là con số đó.
