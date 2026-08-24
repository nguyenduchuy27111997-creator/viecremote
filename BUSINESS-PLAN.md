# Kế hoạch kinh doanh — mạng lưới kỹ sư Việt

**Ngày:** 22/08/2026 · **Cập nhật:** 24/08/2026 · **Sứ mệnh:** [MISSION.md](MISSION.md) · **Lý do đổi hướng:** [PIVOT.md](PIVOT.md)
**Trạng thái:** L1 + Đ3 **đã live** · doanh thu 0 · chưa có pháp nhân · A3 chưa bao giờ chạy

> **CẬP NHẬT 24/08 — hai điều đổi so với thân bài:**
> 1. Ba câu pháp lý ở Mục 2 **đã có lời giải** bằng đối chiếu toàn văn Công báo —
>    [legal-research.md](legal-research.md). Không còn "chưa rõ": kết nối có đồng ý, thu phí
>    **không phải** mua bán dữ liệu (Điều 17.2 Luật 91/2025); **Giấy phép dịch vụ việc làm
>    VẪN CÒN** (NĐ 352 Điều 13–20 — dòng "đã bãi bỏ" trong bảng dưới là SAI, giữ để đối chiếu);
>    xuyên biên giới phải lập hồ sơ, không miễn trừ nào áp dụng. Hai câu MỚI thay chỗ —
>    [prd.md](prd.md) Mục 2. Buổi luật sư đổi từ "chặn tất cả" thành **rà soát trước ca nối
>    đầu tiên**.
> 2. Thứ tự làm đổi: **Đ3 đi trước** — bán nghiên cứu phía cầu, trục Đông Nam Á, đã live tại
>    `/hiring-in-sea` — vì nó có doanh thu với rủi ro thấp nhất và trả lời câu quan trọng hơn
>    mọi câu pháp lý: *có ai trả tiền không*. Bốn cấu trúc và cửa nào đã đóng:
>    [legal-options.md](legal-options.md). Đường chạy ngay không cần ký quỹ: **Đ2 — hợp tác
>    doanh nghiệp có giấy phép** (danh sách 141 doanh nghiệp: `content/licensed-partners-hcm.csv`).

---

## 0. Đọc cái này trước

Hai thứ mà kế hoạch kinh doanh thường trộn lẫn, ở đây tách bảng riêng:

1. **Điều đã biết** — số đo được, ghi rõ nguồn
2. **Điều đang cược** — giả định chưa kiểm, ghi rõ là giả định

Và một thứ thứ ba mà bản trước không có: **điều pháp luật bắt buộc**. Không phải giả định,
không phải lựa chọn.

---

## 1. Điều đã biết

| Số | Giá trị | Nguồn |
|---|---|---|
| Công ty có hồ sơ địa lý tuyển | **3.666** | đo |
| **Công ty tuyển được ở VN** | **110** | đo — đây là danh sách khách hàng |
| Công ty khoá hoàn toàn | 2.485 (67,8%) | đo — danh sách loại trừ |
| Tin remote đã chấm | 34.313 | đo |
| Tin khoá theo địa lý | 86,3% | đo |
| Tin ghi rõ tuyển được ở VN | **0/150** | chấm tay |
| Precision nhãn "mở" | 97,5% · KTC 87–100% | audit phân tầng, n=40 |
| Lập trình viên VN | 530.000 | báo cáo ngành |
| Chi phí hạ tầng | ~12 USD/năm | tính |
| Ký quỹ dịch vụ việc làm | **300.000.000 đ** | NĐ 352/2025 |
| Ký quỹ cho thuê lại lao động | **2.000.000.000 đ** | quy định hiện hành |

---

## 2. Điều pháp luật bắt buộc — không phải lựa chọn

| Ràng buộc | Nguồn | Hệ quả |
|---|---|---|
| Ký quỹ **300 triệu**, pháp nhân, trụ sở thuê ≥24 tháng | NĐ 352/2025 | Không làm với tư cách cá nhân được |
| Thủ tục cấp phép **đã bãi bỏ** 01/07/2026, chuyển **hậu kiểm** | Luật Đầu tư sửa đổi 2025 | Không phải xin phép, nhưng phải **duy trì đủ điều kiện** mọi lúc |
| Hồ sơ chuyển dữ liệu xuyên biên giới (Mẫu 09) + báo Bộ Công an trong 60 ngày + **thoả thuận ràng buộc với từng bên nhận** | Điều 18 NĐ 356/2025 | Không thể "đăng hồ sơ cho ai xem cũng được" |
| **Cấm mua bán dữ liệu cá nhân**, phạt tới **10× doanh thu** | Luật 91/2025 | Ranh giới "kết nối có đồng ý" vs "bán dữ liệu" **chưa rõ** |
| Mất miễn trừ DPO/DPIA khi vượt 100.000 chủ thể hoặc xử lý dữ liệu nhạy cảm | NĐ 356/2025 | Phải có DPO khi lớn |

**Ba câu này đã có lời giải — xem biển cập nhật đầu tài liệu.** Buổi luật sư giờ là **rà
soát câu chữ trước ca nối đầu tiên**, không phải câu hỏi sống còn chặn tất cả.

---

## 3. Chọn mô hình — hai đường, chênh nhau 7 lần

| | **A. Giới thiệu** *(đề xuất)* | **B. Cho thuê lại lao động** |
|---|---|---|
| Ai ký hợp đồng với kỹ sư | Công ty khách | **Bạn** |
| Ký quỹ | **300 triệu** | **2 tỷ** |
| Người đại diện | đủ năng lực theo quy định | **3 năm kinh nghiệm ngành** trong 5 năm gần nhất |
| Doanh thu/người | phí một lần | hằng tháng, liên tục |
| Rủi ro | thấp — không giữ hợp đồng lao động | cao — chịu trách nhiệm sử dụng lao động |
| Ví dụ | headhunt truyền thống | Andela, Turing |
| Vốn ban đầu | ~310 triệu | ~2,1 tỷ |

**Chọn A.** Ba lý do:

1. **Điều kiện người đại diện ở B là rào cứng** — 3 năm kinh nghiệm trực tiếp ngành cho thuê
   lại lao động. Không có thì không mở được, dù có đủ tiền.
2. Vốn chênh gần 7 lần, trong khi chưa có bằng chứng nào về nhu cầu.
3. B là mô hình vận hành nặng: chấm công, bảo hiểm, tranh chấp lao động. Một người 10h/tuần
   không làm được.

Ghi lại để sau này không quên: **nếu muốn sang B, phải tuyển người có 3 năm kinh nghiệm ngành
làm đại diện pháp luật.** Đó là điều kiện, không phải tuỳ chọn.

---

## 4. Doanh thu — toán và tham chiếu thị trường

Tham chiếu (mức khách nước ngoài đang trả cho kỹ sư offshore, 2026):

| Nền tảng | Mô hình | Giá |
|---|---|---|
| Toptal | freelance theo giờ | 60–200 USD/giờ, cộng 500 USD đặt cọc + 79 USD/tháng |
| Turing | theo giờ, tối thiểu 3–6 tháng | senior 5–10 nghìn USD/tháng |
| Andela | staffing, tối thiểu 12 tháng | senior 12–15 nghìn USD/tháng, phí chuyển sang in-house ~50 nghìn USD |

Ba cái trên đều là **mô hình B**. Chúng cho biết **trần giá thị trường**, không phải mô hình
của ta.

**Mô hình A — phí giới thiệu một lần:**

| | |
|---|---|
| Lương năm kỹ sư Việt từ công ty nước ngoài | 30.000–60.000 USD |
| Phí giới thiệu tiêu chuẩn ngành | 15–25% lương năm đầu |
| **Phí mỗi lần nối thành công** | **4.500–15.000 USD** |
| Thận trọng, khoán phẳng | **3.000–5.000 USD** |

**Toán ở nhịp một người:**

| Nhịp | Doanh thu/tháng |
|---|---|
| 1 lần nối/tháng | 3.000–5.000 USD |
| 2 lần | 6.000–10.000 USD |
| 3 lần | 9.000–15.000 USD |

**Điều phải nói thẳng:** đây **không phải sản phẩm mở rộng được**. Mỗi lần nối cần sàng lọc
thật, phỏng vấn thật, theo dõi thật — công của người. Doanh thu tăng tuyến tính với giờ làm,
không tăng theo số người dùng.

Đó không phải điểm trừ, nhưng phải biết mình đang xây cái gì: **một doanh nghiệp dịch vụ có
công cụ dữ liệu tốt**, không phải một sản phẩm phần mềm.

---

## 5. Ba giai đoạn, có cổng thoát

### GĐ 0 — Launch tra cứu, thu email · tháng 0–2 · **~12 USD** · doanh thu 0

**Không đổi gì về pháp lý.** Bản tra cứu hiện tại không giới thiệu ai cho ai, không thu hồ sơ,
không thu phí — nó chưa phải dịch vụ việc làm.

| Việc | Ai |
|---|---|
| Deploy Cloudflare + tên miền + cron | **Bạn** |
| Đăng [bài công bố](content/bai-cong-bo.md) | **Bạn** |
| A8 — 10 cuộc với kỹ sư Việt thật | **Bạn** |
| **Buổi luật sư — 3 câu hỏi ở Mục 2** | **Bạn** |

**Cổng ra:**

| Kết quả 30 ngày | Hành động |
|---|---|
| ≥ 500 người dùng duy nhất | Đi tiếp |
| 100–500 | Đi tiếp, nhưng dồn sức vào phân phối trước |
| < 100 | **Dừng.** Mạng lưới không có người thì không thành mạng lưới |
| **Luật sư nói mô hình không hợp pháp** | **Dừng hẳn**, giữ bản tra cứu làm đóng góp công cộng |

### GĐ 1 — A3 với chính 110 công ty đó · tháng 2–4 · **0 đồng**

Đây là giai đoạn quyết định, và nó **không tốn tiền**.

Bạn đã có: tên công ty, bằng chứng họ tuyển được ở Việt Nam, URL tin gốc, và số vị trí đang mở.

> *"Anh đang tuyển remote toàn cầu — tôi thấy N vị trí. Nếu tôi đưa 20 kỹ sư Việt đã sàng lọc,
> anh có trả phí giới thiệu không, và bao nhiêu?"*

Song song: mở đăng ký cho kỹ sư quan tâm — **chưa gửi hồ sơ đi đâu cả**, chỉ ghi danh.

**Cổng ra:**

| Kết quả A3 | Hành động |
|---|---|
| ≥ 3/10 nói sẽ trả ≥ 3.000 USD/lần nối | Vào GĐ 2 |
| 1–2/10 | Làm **thủ công một ca** trước khi dựng pháp nhân |
| 0/10 | **Không dựng pháp nhân.** Giữ bản tra cứu, hoặc dừng |

**Làm thủ công một ca trước** là bước rẻ nhất trong cả kế hoạch: nối một người, thu một lần
phí, xem toàn bộ quy trình vỡ ở đâu — trước khi tiêu 300 triệu.

### GĐ 2 — Dựng pháp nhân, chạy thật · tháng 4+ · **~310 triệu**

Chỉ vào khi GĐ 0 và GĐ 1 đều qua cổng.

| Khoản | Ước tính |
|---|---|
| Thành lập công ty | 3–10 triệu |
| **Ký quỹ** (giữ trong ngân hàng, không mất) | **300 triệu** |
| Trụ sở 24 tháng | tuỳ |
| Luật sư: hồ sơ Mẫu 09, thoả thuận với bên nhận, DPO | cần thật |
| Kế toán | hằng tháng |

Build thêm: hồ sơ kỹ sư, luồng đồng ý theo từng công ty, nhật ký đồng ý, luồng rút lui.
**Tất cả đều là bề mặt PDPL** — không tự viết ẩu.

---

## 6. Ba kịch bản 18 tháng

| | Xấu | Cơ sở | Tốt |
|---|---|---|---|
| Người dùng trang tra cứu | < 100 | 2.000 | 15.000 |
| Kỹ sư ghi danh | 0 | 300 | 2.000 |
| Công ty trả tiền | 0 | 2 | 8 |
| Lần nối thành công/tháng | 0 | 1 | 3 |
| Doanh thu/tháng (T18) | 0 | ~4.000 USD | ~12.000 USD |
| Vốn đã tiêu | ~12 USD | ~310 triệu | ~310 triệu |
| Kết luận | Dừng ở tháng 2, gần như không mất gì | Đủ sống một người | Tuyển thêm người |

**Kịch bản xấu vẫn chỉ tốn ~12 USD** — vì cổng GĐ 0 và GĐ 1 đều nằm **trước** khoản ký quỹ.
Đó là điều quan trọng nhất của cách sắp xếp này.

---

## 7. Rủi ro, xếp theo mức nguy hiểm thật

| # | Rủi ro | Vì sao nguy hiểm | Giảm thế nào |
|---|---|---|---|
| 1 | **Cold start hai phía** | Kỹ sư không vào nếu chưa có công ty; công ty không trả nếu chưa có kỹ sư | Dùng dữ liệu 110 công ty đi trước — bắt đầu từ phía cầu, không phải phía cung |
| 2 | ~~B-Q5 trả lời là "bán dữ liệu"~~ **ĐÃ GỠ 24/08**: Điều 17.2 Luật 91/2025 nói thẳng chuyển giao có đồng ý, thu phí **không phải** mua bán | Rủi ro còn lại là câu chữ đồng ý sai chuẩn NĐ 356 Điều 7.3 | Rà soát pháp lý trước ca nối đầu tiên |
| 3 | Đối thủ đã có sẵn quan hệ | Công ty gia công VN đã làm việc này nhiều năm | Lợi thế duy nhất: biết công ty nào tuyển được, có bằng chứng |
| 4 | Không mở rộng được | Doanh thu tăng theo giờ làm, không theo người dùng | Chấp nhận. Đây là doanh nghiệp dịch vụ |
| 5 | Uốn dữ liệu cho khách lớn | Mất tài sản duy nhất | [MISSION.md](MISSION.md) ràng buộc 1 — không ngoại lệ |

**Rủi ro số 1 không phải rủi ro kỹ thuật, và không code nào giải được.**

---

## 8. Việc kế tiếp, theo thứ tự

| # | Việc | Ai | Chặn cái gì |
|---|---|---|---|
| 1 | Đăng bài công bố (HN sáng thứ Ba giờ Mỹ, rồi nhóm Việt) | **Bạn** | Phân phối — mọi thứ phía sau |
| 2 | A8 — 10 kỹ sư Việt (nghe từ bình luận bài công bố) | **Bạn** | Biết có đúng vấn đề không |
| 3 | A3 — chào Đ3 tới các mục tiêu trong `content/outreach-targets.txt` | **Bạn** | Biết có ai trả tiền không |
| 4 | Tên miền (mở khoá gửi thư xác nhận) | **Bạn** | Kênh sở hữu |
| 5 | Rà soát pháp lý — trước **ca nối đầu tiên**, không phải bây giờ | **Bạn** | L2 |

*(Bản 22/08 đặt "buổi luật sư" ở #1 chặn tất cả — đã gỡ sau đối chiếu toàn văn 23–24/08.
Deploy + cron đã xong, không còn trong danh sách.)*

Cả năm đều là việc của bạn, không phải của máy.
