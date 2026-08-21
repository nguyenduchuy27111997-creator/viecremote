# Còn phải build gì

**Ngày:** 21/08/2026 · Rà đối chiếu [BUSINESS-PLAN.md](BUSINESS-PLAN.md), [OPERATIONS.md](OPERATIONS.md), [MISSION.md](MISSION.md)

---

## 0. Cách xếp ưu tiên

Không xếp theo "nghe hay". Xếp theo một câu hỏi:

> **Thiếu cái này thì cổng quyết định nào không bấm được?**

Kế hoạch có ba cổng. Cổng nào không đo được thì cả kế hoạch thành cảm tính.

---

## 1. Nhóm A — CHẶN CỔNG. Phải có trước khi đăng bài công bố

### A1. Analytics · ~1 giờ · **chặn cổng GĐ 0**

Cổng GĐ 0 ghi: *"ngày thứ 30: <100 người dùng duy nhất → **dừng lại**"*.

**Hiện không có gì đo được con số đó.** Nghĩa là cổng quan trọng nhất — cổng quyết định có nên
đi tiếp hay không — hiện **không bấm được**. Đăng bài rồi mới cài thì mất đúng đợt lưu lượng
duy nhất mà bài mang lại.

**Chọn: Cloudflare Web Analytics.** Miễn phí, không cookie, không cần banner đồng ý, đã nằm sẵn
trong stack. Một thẻ `<script>`.

*Lưu ý trung thực:* nó vẫn ghi IP và user-agent — theo GDPR đó vẫn là dữ liệu cá nhân dù không
có cookie. Với PDPL thì đây là xử lý tối thiểu và không lưu trạng thái, nhưng **phải ghi vào
trang riêng tư**. Và nó không theo được phễu — đủ cho "bao nhiêu người duy nhất", không đủ cho
"bao nhiêu người bấm sang tin gốc".

Nếu cần đo phễu (chỉ số "số lần bấm xem tin gốc" trong PRD Mục 9) thì phải thêm event thủ công —
Cloudflare không làm được, cần Plausible hoặc Umami tự host. **Hoãn tới GĐ 1.**

### A2. Nút báo sai · ~3 giờ · **chặn chỉ số sống còn của sứ mệnh**

[MISSION.md](MISSION.md) gọi tỷ lệ báo nhãn sai là **chỉ số sống còn**.
[OPERATIONS.md](OPERATIONS.md) đã xếp sẵn **30 phút/tuần** để xử lý báo sai.
[prd.md](prd.md) Mục 7 ghi *"nút báo sai trên mọi tin"*.

**Nút đó không tồn tại.** Ta đang lên lịch xử lý cho một thứ chưa build.

Cách làm tối giản, không đụng PDPL:

- Form trên trang tin và trang công ty: chọn lý do + ô ghi chú, **không thu email, không tài khoản**
- Route handler ghi vào bảng D1 `report` — chỉ `job_id`, `reason`, `note`, `created_at`
- Turnstile chống spam (Cloudflare, miễn phí, không cookie)
- Trang `/bao-sai` liệt kê báo cáo chưa xử — cho chính bạn đọc hằng tuần

**Không thu dữ liệu cá nhân nào** thì miễn trừ DPO/DPIA của NĐ 356/2025 giữ nguyên.

---

## 2. Nhóm B — CHẶN PHÂN PHỐI. Bài công bố phụ thuộc vào

### B1. Ảnh OG · ~2 giờ

Bài công bố sống bằng chia sẻ trên Facebook, LinkedIn, HN. Không có ảnh OG thì mọi lượt chia sẻ
hiện thẻ trắng — **trông như link hỏng**, và tỉ lệ bấm rơi thẳng.

Next 16 có `opengraph-image.tsx` sinh ảnh ngay lúc build. Nội dung nên là **con số**, không phải
logo: *"110/3.666 công ty tuyển được người ở Việt Nam"* trên nền tối. Trang công ty sinh ảnh
riêng theo `slug`.

### B2. `sitemap.xml` + `robots.txt` · ~1 giờ

Sứ mệnh là **để người ta tìm thấy sự thật**. Không có sitemap thì 3.666 trang công ty phải chờ
Google tự bò tới — mất hàng tháng, và trang sâu có thể không bao giờ được lập chỉ mục.

Next có `sitemap.ts` và `robots.ts` dựng sẵn. Sitemap phải chia mảnh: giới hạn 50.000 URL/tệp,
ta có ~4.100 nên một tệp đủ, nhưng khi lên 10.000 công ty thì cần chia.

### B3. Trang 404 · ~30 phút

3.666 URL công ty. Link cũ, gõ sai, công ty bị gỡ khỏi kho — tất cả đổ về 404. Hiện là trang
mặc định của Next, không có điều hướng, không có ô tra cứu.

404 nên: nói rõ *"công ty này không có trong kho, hoặc đã bị gỡ"*, kèm ô tra cứu và link về
sổ đăng ký.

---

## 3. Nhóm C — chặn GĐ 1 và GĐ 2

### C1. Thu email · ~2 giờ · GĐ 1

[prd.md](prd.md) F7. Kênh sở hữu duy nhất — không có thì mọi lưu lượng từ bài công bố **bay
hết sau một tuần**.

Tối giản: một ô email cuối trang, lưu vào D1, xác nhận double opt-in. **Chưa gửi gì cả** cho
tới khi có nội dung đáng gửi. Thu email rồi im lặng ba tháng còn tệ hơn không thu.

*Cảnh báo PDPL:* email **là** dữ liệu cá nhân. Thu email làm ta bước vào phạm vi xử lý dữ liệu
cá nhân — vẫn dưới ngưỡng 100.000 chủ thể nên giữ được miễn trừ, nhưng phải có thông báo xử lý
và cơ chế rút lui. Đọc lại [legal-brief.md](legal-brief.md) trước khi bật.

### C2. Bảo vệ + tài liệu API · ~3 giờ · GĐ 2

`/api/companies` hiện **mở toang, không giới hạn, không tài liệu**. Hai vấn đề:

- Ai cũng có thể vét sạch dữ liệu bằng một vòng lặp — chính là thứ định bán ở GĐ 2
- 100.000 request/ngày của Workers free bị một script đốt trong vài phút

Cần: khoá API đơn giản cho khách trả tiền, giới hạn nhịp bằng Cloudflare Rate Limiting (miễn
phí), và một trang `/api` mô tả trường dữ liệu. Trang tài liệu **cũng chính là trang bán hàng**
khi đi A3.

---

## 4. Nhóm D — ý tưởng nghe hay nhưng DỮ LIỆU KHÔNG ĐỠ

Đây là phần quan trọng nhất của tài liệu này. **Đừng build những thứ dưới đây.**

| Ý tưởng | Độ phủ dữ liệu thật | Phán quyết |
|---|---|---|
| Lọc theo **cơ chế hợp đồng** | **10/110** công ty mở có dữ liệu (91% "không rõ") | Bộ lọc hiện tại **gần như trang trí** — nên bỏ hoặc ghi rõ độ phủ |
| Lọc theo **múi giờ** | **5/409** tin mở (1,2%) | Không đủ. Đừng làm |
| **Xu hướng theo thời gian** | `first_seen` chỉ có **2 ngày khác nhau** | Bất khả thi **bây giờ**. Sau ~3 tháng chạy cron mới có |
| Cảnh báo tin mới qua email | Cần lịch sử + email | Chờ C1 và ≥3 tháng dữ liệu |
| Lọc theo **công bố lương** | 48/409 tin mở (11,7%) | Yếu nhưng dùng được — ghi rõ độ phủ |

**Phát hiện đáng nói:** bộ lọc "Cơ chế" đang hiện trên trang chủ cho người dùng cảm giác họ
lọc được một thứ mà 91% dữ liệu là "không rõ". Đó là **hứa quá khả năng** — đúng thứ sứ mệnh
cấm. Sửa: hoặc bỏ, hoặc ghi ngay cạnh *"chỉ 3% tin nêu cơ chế"*.

---

## 5. Nhóm E — dữ liệu ĐỠ ĐƯỢC, chưa khai thác

| Tính năng | Độ phủ | Vì sao đáng làm |
|---|---|---|
| **Duyệt theo nước bị khoá** | **2.324/3.666** công ty (63%) | Đây là dữ liệu giàu nhất ta có, và chưa có đường nào vào nó. Trang `/khoa/{nuoc}`: *"1.589 công ty khoá vào Mỹ"* — vừa là nội dung SEO, vừa trả lời câu người ta thật sự hỏi |
| **Trang "vậy tôi làm gì"** | — | Bài công bố nói *kênh tin công khai về cấu trúc không dành cho bạn*. Người đọc gật đầu xong **không có bước tiếp theo nào trên trang**. Đây là lỗ hổng lớn nhất về sản phẩm, không phải về kỹ thuật |

Trang "vậy tôi làm gì" **không phải mồi giữ chân** — sứ mệnh nói người dùng *nên rời đi* sau khi
có câu trả lời. Nó là phần **hoàn tất câu trả lời**: 110 công ty này tuyển bằng cơ chế nào,
tại sao 92% tin không nói, và điều đó nghĩa là gì khi bạn thương lượng.

---

## 6. Không nên build

| | Vì sao |
|---|---|
| Tài khoản, đăng nhập | Không có gì sau cổng. Mở rộng bề mặt PDPL vô ích |
| Nộp hồ sơ trong trang | Luôn dẫn về tin gốc |
| Công ty tự đăng tin | Tiền mua vị trí = phá huỷ thứ đang bán |
| Tìm kiếm toàn văn mô tả | FTS theo tên công ty đủ ở quy mô này; toàn văn làm DB phình gấp nhiều lần |
| Ứng dụng di động | Web đã responsive. Không có gì cần native |

---

## 7. Thứ tự làm

| # | Việc | Giờ | Trạng thái |
|---|---|---|---|
| 1 | A1 Analytics | 1 | ✅ **xong** — cần dán token vào `.env` |
| 2 | B2 sitemap + robots | 1 | ✅ **xong** — 4.079 URL |
| 3 | B3 trang 404 | 0,5 | ✅ **xong** |
| 4 | B1 ảnh OG | 2 | ✅ **xong** — trang chủ + từng công ty |
| 5 | A2 nút báo sai | 3 | ✅ **xong** — API + form + `/bao-sai` |
| 6 | D-sửa: ghi độ phủ cạnh bộ lọc cơ chế | 0,5 | ✅ **xong** |
| — | *↑ 8 giờ chặn launch — **HOÀN TẤT** 21/08 ↑* | | |
| 7 | E1 duyệt theo nước bị khoá | 4 | SEO + giá trị |
| 8 | E2 trang "vậy tôi làm gì" | 3 | Lỗ hổng sản phẩm |
| 9 | C1 thu email | 2 | GĐ 1 |
| 10 | C2 bảo vệ + tài liệu API | 3 | GĐ 2 |

**8 giờ chặn launch.** Vừa đúng một tuần ở nhịp 10h/tuần — nhưng tuần đó cũng phải deploy và
chạy A8, nên thực tế là **hai tuần**.

Mục 7–10 làm sau khi có số liệu từ cổng GĐ 0. Đừng build chúng trước: nếu cổng bấm "dừng" thì
toàn bộ 12 giờ đó là lãng phí.
