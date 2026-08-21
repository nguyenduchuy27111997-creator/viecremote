# Kiến trúc

**Ngày:** 19/08/2026 · Số liệu trong tài liệu này **đo được**, không ước lượng.

> **Nói trước cho sòng phẳng:** kiến trúc này được chọn bằng **suy luận**, không bằng đo đạc — và tài liệu này viết *sau khi* đã dựng xong. Một ước lượng của tôi sai **5 lần** (Mục 5). Đọc Mục 5 trước Mục 3.

---

## 1. Hình dạng

```
   discover_slugs.py  (Hacker News)   ─┐
   cc_slugs.py        (Common Crawl)  ─┼→  tools/slugs.txt   5.535 slug
   slugs_from_targets.py (remoteintech)─┘
                                             │
                                             ▼
   export_jobs.py     32 luồng · cổng 1 yêu cầu/giây/MIỀN
      ├── kéo 3 ATS công khai (Greenhouse, Lever, Ashby)
      ├── khử trùng lặp → lọc remote
      ├── chấm nhãn      score_rules.py + country.py
      └── đọc schema     check_schema.py  (giới hạn 2.500 tin, ưu tiên "mở toàn cầu")
                                             │
                                             ▼
                                    jobs.json   ~5 MB
                                             │
                                             ▼
   build.py           0,28 giây · chỉ thư viện chuẩn
      ├── kiểm C1–C4 + link nội bộ  → build DỪNG nếu vi phạm
      └── sinh HTML tĩnh
                                             │
                                             ▼
                                    site/   4,7 MB · 511 file
```

**Không có:** máy chủ · cơ sở dữ liệu · framework · bước biên dịch · phụ thuộc ngoài thư viện chuẩn Python.

---

## 2. Số đo được

| | |
|---|---|
| Thời gian build | **0,28 giây** (5.006 tin → 511 file) |
| Kích thước site | 4,7 MB · 511 file |
| Trang chủ | 49 KB · 754 nút DOM · 3 tài nguyên |
| Tải cục bộ | 70 ms (localhost, không có mạng thật) |
| Trang lớn nhất | **257 KB** — `vi-sao-bi-loai.html` |
| Trang công ty | trung bình 9 KB, lớn nhất 95 KB |
| Trang chi tiết | trung bình 5 KB |
| CSS + JS | 8 KB + 1 KB, không nén |
| **Font tải về** | **18 face** qua 2 miền bên thứ ba |

---

## 3. Vì sao sinh trang tĩnh là đúng cho tải này

Không phải sở thích — bốn tính chất của bài toán loại bỏ mọi kiến trúc khác:

| Tính chất | Hệ quả |
|---|---|
| **Chỉ đọc.** Không tài khoản, không đăng tin, không nộp hồ sơ | Không cần máy chủ ứng dụng |
| **Không cá nhân hoá.** Mọi người thấy cùng nội dung | Mọi byte cache được ở biên |
| **Dữ liệu đổi theo ngày, không theo giây** | Không cần truy vấn lúc chạy |
| **~5.000 trang** | Quá nhỏ để cần chỉ mục hay phân trang phía máy chủ |

Với bốn điều đó, cơ sở dữ liệu là **chi phí không mua được gì**: thêm một tầng phải vận hành, sao lưu, và một truy vấn phải chạy cho mỗi lượt xem — để trả về đúng thứ đã biết trước từ đêm qua.

**So sánh trung thực:**

| | Kiến trúc này | Next.js/SSR + DB |
|---|---|---|
| TTFB | Cache biên, ~10–40 ms | Chạy hàm + truy vấn, ~100–400 ms |
| Chi phí | **0 đồng** (Cloudflare Pages) | 5–25 USD/tháng tối thiểu |
| Cần vận hành | Không | Có |
| Điểm hỏng | Không | DB, hàm, kết nối |
| Thời gian build | 0,28 giây | 30–120 giây |

Không có trường hợp nào ở quy mô này mà máy chủ động nhanh hơn tệp tĩnh trên CDN. Đây là kết luận về **kiến trúc**, không phải về framework.

---

## 4. Ràng buộc tuân thủ nằm TRONG build

Không phải quy trình, không phải danh sách kiểm tay — build **dừng** nếu vi phạm:

| | |
|---|---|
| **C1** | Mọi nhãn phải có trích dẫn nguyên văn *và* trích dẫn phải chứa cụm lý giải nhãn |
| **C2** | Không trang nào phát sinh `JobPosting` schema (Q1 chưa có câu trả lời pháp lý) |
| **C3** | Chỉ tin đang mở lọt vào dữ liệu |
| **C4** | Trích đoạn ≤ 300 ký tự |
| **link** | Mọi `href` nội bộ phải trỏ file có thật |

Đã cứu ít nhất ba lần: hai nhãn sai (`MST` đọc thành múi giờ, `ITAR` đọc thành yêu cầu ứng viên) và 183 link gãy.

---

## 5. Chỗ tôi phân tích SAI

**Ước lượng thời gian kéo sai 5 lần.**

Tôi đặt trần *1 yêu cầu/giây/miền* rồi tính 5.535 slug ≈ 92 phút. Nhưng code vừa nghỉ 1 giây **vừa chờ tải xong**, nối tiếp nhau — nên thực tế chỉ đạt **0,28 yêu cầu/giây**, không phải 1.

Nguyên nhân: Greenhouse `?content=true` trả toàn bộ mô tả HTML. Board lớn mất 10 giây.

```
stripe 9,7s · databricks 10,0s · figma 3,8s  →  trung bình 3,5 s/slug  →  5,4 GIỜ
```

**Sửa:** cổng theo miền chỉ điều tiết *tốc độ phát* yêu cầu, không chặn lúc chờ phản hồi. 32 luồng che độ trễ tải.

| Luồng | s/slug | 5.535 slug |
|---|---|---|
| nối tiếp | 3,50 | 5,4 giờ |
| 8 | 1,40 | 129 phút |
| 20 | 1,19 | 109 phút |
| **32** | **0,74** | **68 phút** |

68 phút là **sàn do phép lịch sự đặt ra**, không phải do code chậm: Greenhouse chiếm ~4.000 slug × 1 giây = 67 phút. Muốn nhanh hơn phải phá trần lịch sự — không làm.

**Bài học lặp lại suốt dự án:** ước lượng bằng suy luận sai theo *cả hai chiều*. Chi phí LLM sai một bậc (hai lần, ngược nhau), tầng quy tắc sai 70%, thời gian kéo sai 5 lần. Mỗi lần chỉ chạy thật mới ra số đúng.

---

## 6. Nút thắt thật, xếp theo mức độ

### 6.1 Chu kỳ làm mới — **nút thắt duy nhất đáng kể**

68 phút kéo + 42 phút schema = **110 phút mỗi lần chạy**. Và nó **tuyến tính theo số slug**: gấp đôi slug là gấp đôi thời gian.

`build.py` chạy 0,28 giây. Toàn bộ chi phí nằm ở khâu kéo dữ liệu.

**Sửa: phân bậc poll** (đã đặc tả ở PRD Mục 7.1, **chưa cài**).

| Bậc | Điều kiện | Tần suất | Ước tính |
|---|---|---|---|
| Nóng | Sinh tin mở-toàn-cầu trong 90 ngày | Hằng ngày | ~300 slug |
| Ấm | Có tin đang mở | 3 ngày/lần | ~1.000 |
| Nguội | Không có tin, hoặc 6 tháng không sinh gì | Hằng tuần | ~2.000 |
| Chết | 3 lần lỗi liên tiếp | Hằng quý | ~2.200 |

Tải hằng ngày: **~1.000 yêu cầu ≈ 12 phút** thay vì 110. Giảm **9 lần**.

Đây là việc kỹ thuật đáng làm nhất còn lại.

### 6.2 Font — 18 face qua hai miền bên thứ ba

Trang tải 18 face từ `fonts.googleapis.com` + `fonts.gstatic.com`. Với người dùng ở Việt Nam đó là **2 lần bắt tay DNS + TLS thêm** trước khi chữ hiện ra.

Và **hai trọng lượng khai báo mà không dùng**: `Be Vietnam Pro 700`, `Newsreader 400`. CSS chỉ dùng 400/500/600.

**Sửa:** bỏ hai trọng lượng thừa, rồi **tự host bản subset** (`unicode-range` cho latin + vietnamese). Kết quả: 0 miền bên thứ ba, cache cùng nguồn, ~40% ít byte font.

### 6.3 `vi-sao-bi-loai.html` — 257 KB

Trang lớn nhất, gấp 5 lần trang chủ. Nó hiện 25 ví dụ cho **mỗi nhóm nước**, và có nhiều nhóm.

**Sửa:** phân trang như các trang khác (`PER_PAGE` đã có sẵn), hoặc tách mỗi nước một trang — `chi-tuyen-o-my.html` — vừa nhẹ vừa tốt cho tìm kiếm.

### 6.4 Không có build tăng dần

Mỗi lần chạy sinh lại toàn bộ 511 file. Ở 0,28 giây thì **không phải vấn đề** và sẽ không thành vấn đề cho tới ~50.000 trang.

**Không sửa.** Tối ưu chỗ này là tối ưu sai chỗ.

---

## 7. Việc nên làm, theo thứ tự

| # | Việc | Tác động | Công |
|---|---|---|---|
| 1 | **Phân bậc poll** | 110 phút → 12 phút mỗi ngày | ~3 giờ |
| 2 | Bỏ 2 trọng lượng font thừa | ~2 request ít hơn | 5 phút |
| 3 | Tự host font subset | Bỏ 2 miền bên thứ ba | ~1 giờ |
| 4 | Phân trang `vi-sao-bi-loai` | 257 KB → ~40 KB/trang | ~30 phút |
| 5 | Deploy Cloudflare Pages | Cache biên, 0 đồng | ~30 phút |

**Không làm:** đổi sang framework · thêm cơ sở dữ liệu · build tăng dần · SSR. Không cái nào giải nút thắt thật, và mọi cái đều thêm thứ phải vận hành.

---

## 8. Điều chưa đo

Nói ra để không nhầm là đã biết:

- **Chưa đo hiệu năng thật từ Việt Nam** — mọi số ở đây là localhost. TTFB thật, thời gian tải font thật, đều chưa biết
- **Chưa đo dưới mạng chậm** (3G, mạng di động)
- **Chưa kiểm khả năng tiếp cận** ngoài focus bàn phím và `prefers-reduced-motion`
- **Chưa biết hành vi ở quy mô mới** — export đang chạy sẽ đưa kho từ 5.000 lên ~25.000 tin; trang chủ và trang lý do sẽ phình theo
