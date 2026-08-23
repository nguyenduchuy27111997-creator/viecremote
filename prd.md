# PRD v3.0 — Mạng lưới kỹ sư Việt

**Ngày:** 22/08/2026 · **Thay thế** PRD v2.0 (web tra cứu đọc-only)
**Sứ mệnh:** [MISSION.md](MISSION.md) · **Mô hình:** [business-model.md](business-model.md) · **Đổi hướng:** [PIVOT.md](PIVOT.md)
**Quy tắc chấm:** [rubric-spec.md](rubric-spec.md) · **Tuân thủ:** [legal-brief.md](legal-brief.md)

---

## 1. Sản phẩm một câu

> **Kỹ sư Việt được nhìn thấy bởi đúng những công ty thật sự tuyển được họ.**

Hai tầng, và chúng **không cùng trạng thái**:

| Tầng | Là gì | Trạng thái |
|---|---|---|
| **L1 — Minh bạch** | Tra cứu công khai: công ty nào tuyển được ở VN, kèm trích dẫn | ✅ **Đã build, sẵn sàng launch** |
| **L2 — Mạng lưới** | Hồ sơ kỹ sư, đồng ý theo công ty, giới thiệu có thu phí | 🔓 **Mở khoá có điều kiện** — xem Mục 2 |

L1 chạy được **ngay và độc lập**. Nó không giới thiệu ai cho ai, không thu hồ sơ, không thu phí
— nên **chưa phải dịch vụ việc làm** và không cần pháp nhân hay ký quỹ.

L2 là chỗ có doanh thu, và cũng là chỗ có mọi rủi ro pháp lý.

---

## 2. Điều kiện để build L2 — đọc trước khi viết code

Ba câu từng chặn L2 **đã đối chiếu toàn văn** từ Công báo Chính phủ —
[legal-research.md](legal-research.md). Cả ba đã có lời giải. Nhưng toàn văn làm lộ **hai câu
mới** chưa có lời giải.

### Ba câu cũ — xong

| Câu | Kết quả | Ràng buộc để lại |
|---|---|---|
| **B-Q5** — thu phí có phải mua bán dữ liệu? | **Không.** Điều 17 khoản 2 Luật 91/2025: chuyển giao khi có đồng ý, *"có thu phí hoặc không thu phí thì không được xác định là mua, bán dữ liệu cá nhân"* | NĐ 356 Điều 7.3: đồng ý **theo từng lần chuyển giao**, hiện rõ tên công ty nhận · **không được hình thành kho dữ liệu** · thỏa thuận ký **trước khi** chuyển · mã ngành phải khớp |
| **Xuyên biên giới** | **Phải lập hồ sơ.** Điều 20.2: gửi trong **60 ngày** kể từ lần chuyển đầu. Danh sách miễn trừ (NĐ 356 Điều 17.3) đóng, không mục nào áp dụng | Hồ sơ làm **01 lần** cho suốt thời gian hoạt động, cập nhật 06 tháng khi có thay đổi |
| **Dịch vụ việc làm** | **Vẫn cần Giấy phép** (NĐ 352 Điều 13–20), UBND cấp tỉnh cấp, hạn tối đa 60 tháng | Ký quỹ **300 triệu** · trụ sở thuê **≥24 tháng** · người đại diện có đại học **hoặc** ≥24 tháng kinh nghiệm dịch vụ việc làm |

### Hai câu mới — CHẶN, phải hỏi trước khi ký quỹ

| Câu | Vì sao chặn |
|---|---|
| **Remote cho công ty nước ngoài có bị coi là "việc làm ở nước ngoài"?** NĐ 352 Điều 12.2.b | Nếu **có**: phải giới thiệu **thông qua doanh nghiệp được cấp phép đưa lao động đi nước ngoài** — phá mô hình. Lập luận ngược: luật dùng cụm *"đi làm việc ở nước ngoài theo hợp đồng"*, kỹ sư remote không đi đâu cả |
| **Nền tảng có phải "dịch vụ xử lý dữ liệu cá nhân"?** NĐ 356 Điều 21.3 — *"dịch vụ thu thập, xử lý dữ liệu cá nhân trực tuyến từ trang web, ứng dụng"* | Nếu **có**: thêm một Giấy chứng nhận (Điều 24–27) + **tối thiểu 03 nhân sự** đủ chuẩn Điều 13.2 (cao đẳng+, ≥2 năm kinh nghiệm, đã đào tạo) |

**Chế tài** (Điều 8): mua bán dữ liệu **10× khoản thu**, sàn 3 tỷ · vi phạm chuyển xuyên biên
giới **5% doanh thu năm trước** · vi phạm khác tối đa **3 tỷ**. Có thể truy cứu hình sự.

### Hệ quả kiến trúc phải chốt trước khi code

Điều 20.6.c Luật và NĐ 356 Điều 7.6 đều miễn trừ khi **chủ thể tự chuyển dữ liệu của mình**.
Nền tảng gửi hộ, hay kỹ sư tự gửi — hai kiến trúc khác nhau, gánh nặng pháp lý khác hẳn.
**Quyết định này đi trước dòng code đầu tiên của L2.**

---

## 3. L1 — Minh bạch · đã build

### 3.1 Ràng buộc từ dữ liệu

**Dữ liệu dồi dào là dữ liệu loại trừ.** Đây vẫn là sự thật quyết định L1 chứa gì.

| Nếu trang hứa | Dữ liệu thật | Kết luận |
|---|---|---|
| "Việc tuyển được ở VN" | **0/150** chấm tay | Không được hứa |
| "Công ty tuyển được ở VN" | **110/3.666** (3,0%) | Hiển thị được, và đây là **danh sách khách hàng của L2** |
| **"Công ty này KHÔNG tuyển được, vì sao"** | **67,8%** có trích dẫn | **Lõi của L1** |
| "Cơ chế trả lương" | 3% máy · 7,2% chấm tay | Hiện khi có, "không rõ" khi không |

### 3.2 Tính năng — đã xong

| # | Tính năng | Đường dẫn |
|---|---|---|
| F0 | **Sổ đăng ký công ty** — trục chính | `/` |
| F1 | Hồ sơ công ty: kết luận, bản đồ nước khoá, cơ chế, mọi tin | `/cong-ty/{slug}` |
| F2 | Danh sách tin đang mở — trục phụ | `/tin-mo` |
| F3 | Chi tiết tin, bằng chứng nguyên văn | `/viec/{id}` |
| F4 | Vì sao bị loại — phân loại + nước khoá | `/vi-sao-bi-loai` |
| F5 | **Duyệt theo nước bị khoá** — 104 nước | `/khoa`, `/khoa/{code}` |
| F6 | **Vậy tôi nên làm gì** | `/lam-gi` |
| F7 | Phương pháp: rubric, số liệu, giới hạn | `/phuong-phap` |
| F8 | **Nút báo sai** trên mọi trang tin và công ty | — |
| F9 | Thu email, double opt-in | chân trang |
| F10 | Dữ liệu và riêng tư | `/rieng-tu` |
| F11 | API dữ liệu địa lý tuyển + tài liệu | `/api`, `/api/companies` |

### 3.3 Vai trò mới của L1

L1 không còn là sản phẩm cuối. Nó là **ba thứ cùng lúc**:

1. **Phễu thu hút kỹ sư** — lý do họ vào, và lý do họ tin
2. **Danh sách khách hàng cho L2** — 110 công ty, có tên, có bằng chứng, có URL tin gốc
3. **Bằng chứng năng lực** khi đi bán: *"tôi đã chấm 34.313 tin, precision 97,5%"*

---

## 4. L2 — Mạng lưới · đặc tả, chưa build

Viết ra để biết cần gì, **không phải để build ngay**.

| # | Tính năng | Ghi chú |
|---|---|---|
| G1 | Tài khoản kỹ sư | Bề mặt PDPL đầu tiên. Tối giản: email + mật khẩu |
| G2 | Hồ sơ: kỹ năng, kinh nghiệm, mức mong muốn, múi giờ chấp nhận được | **Không bắt buộc CV** — CV dễ chứa dữ liệu nhạy cảm |
| G3 | **Đồng ý theo từng công ty** | Bấm "cho phép giới thiệu tôi tới X". **Không có** "đồng ý cho mọi đối tác" |
| G4 | **Nhật ký đồng ý** | Ai, công ty nào, lúc nào, IP. Đây là bằng chứng pháp lý |
| G5 | Rút lui một cú bấm | **Xoá hẳn**, không đánh dấu |
| G6 | Bảng công ty: xem hồ sơ đã được đồng ý | Chỉ hồ sơ có đồng ý cho **chính công ty đó** |
| G7 | Theo dõi trạng thái nối | Để tính phí và để biết quy trình vỡ ở đâu |

### Điều KHÔNG build ở L2

| | Vì sao |
|---|---|
| Hồ sơ công khai, ai xem cũng được | Vi phạm G3 — mỗi lần xem phải có đồng ý cụ thể |
| Tự động gợi ý ứng viên cho công ty | Gợi ý = gửi dữ liệu. Cần đồng ý trước |
| Chấm điểm/xếp hạng kỹ sư công khai | Dữ liệu cá nhân + rủi ro phân biệt đối xử |
| Thu CV dạng tệp | Dễ chứa dữ liệu nhạy cảm ⇒ mất miễn trừ DPO/DPIA |
| Công ty trả tiền để lên đầu | Vi phạm [MISSION.md](MISSION.md) ràng buộc 1 |
| Cho thuê lại lao động | Ký quỹ 2 tỷ + đại diện cần 3 năm kinh nghiệm ngành |

---

## 5. Ràng buộc bắt buộc

### 5.1 L1 — năm cổng chặn build, đã chạy

Nằm ở `tools/gates.py`, **cả hai luồng xuất bản cùng gọi**. Vi phạm ⇒ exit 1, không sinh đầu ra.

| # | Ràng buộc |
|---|---|
| **C1** | Mọi nhãn phải có trích dẫn nguyên văn chứa từ khoá đã khớp |
| **C2** | Không phát sinh JobPosting schema · `index_layer = aggregated` |
| **C3** | Tin biến mất khỏi feed ⇒ gỡ trong 48h |
| **C4** | Trích đoạn ≤ 300 ký tự, luôn link về tin gốc |
| **C5** | Không gán "mở toàn cầu" khi công ty tự khai danh sách nước không có VN |

Đã kiểm đối kháng sáu ca; CI chạy lại mỗi lần push.

### 5.2 L2 — bốn ràng buộc mới, chưa có cổng

Đây là món nợ: **chưa có cơ chế nào ép chúng.** Phải build cùng lúc với L2, không phải sau.

| # | Ràng buộc | Kiểm thế nào |
|---|---|---|
| **C6** | Không hồ sơ nào rời hệ thống mà thiếu bản ghi đồng ý cho **đúng công ty đó** | Chặn ở tầng dữ liệu, không phải tầng giao diện |
| **C7** | Kỹ sư không bao giờ bị thu tiền | Không có luồng thanh toán nào hướng vào kỹ sư |
| **C8** | Rút lui = xoá hẳn trong 24h | Kiểm tự động |
| **C9** | Tầng minh bạch không đổi vì công ty trả tiền | Nhãn công ty do pipeline sinh, **không có đường sửa tay** |

**C9 là ràng buộc khó nhất** vì nó chống lại chính động cơ kinh tế. Cách ép duy nhất đáng tin:
giữ nhãn công ty hoàn toàn do `tools/score_rules.py` sinh, và **không xây giao diện sửa nhãn nào cả**.

---

## 6. Lộ trình — gắn với cổng, không gắn với ngày

### Giai đoạn L1 · chi phí ~12 USD

| Mốc | Việc | Ai |
|---|---|---|
| M0 | ✅ Pipeline, chấm nhãn, cổng C1–C5, site | xong |
| M1 | ✅ Analytics, sitemap, OG, báo sai, API | xong |
| M2 | **Rà soát pháp lý — câu chữ đồng ý + Mẫu 09** (trước ca nối đầu tiên) | **Bạn** |
| M3 | Deploy, tên miền, cron | **Bạn** |
| M4 | Đăng bài công bố · A8 với 10 kỹ sư | **Bạn** |

**Cổng:** 30 ngày sau launch, <100 người dùng ⇒ **dừng**. Luật sư nói không hợp pháp ⇒ **dừng
L2 hẳn**, giữ L1 làm đóng góp công cộng.

### Giai đoạn A3 · chi phí 0

| Mốc | Việc |
|---|---|
| M5 | **A3 — 10 công ty trong danh sách 110.** Hỏi: có trả phí giới thiệu không, bao nhiêu |
| M6 | **Làm thủ công một ca** — nối một người, thu một lần phí, xem cái gì vỡ |

**Cổng:** <3/10 nói có ⇒ **không dựng pháp nhân**.

### Giai đoạn L2 · chi phí ~310 triệu

| Mốc | Việc |
|---|---|
| M7 | Pháp nhân, ký quỹ 300 triệu, trụ sở |
| M8 | Hồ sơ Mẫu 09, thoả thuận với bên nhận, DPO nếu cần |
| M9 | Build G1–G7 **kèm cổng C6–C9** |
| M10 | Chạy thật |

**M6 phải xong trước M7.** Nối thủ công một ca là bước rẻ nhất trong cả lộ trình và dễ bị bỏ
qua nhất.

---

## 7. Đo gì

### L1

| Chỉ số | Vì sao |
|---|---|
| **Tỷ lệ báo nhãn sai** | Chỉ số sống còn. Sứ mệnh hỏng nếu số này cao |
| Người dùng duy nhất / tháng | Cổng GĐ 0 |
| Đăng ký email | Hạt giống của L2 |
| Lượt xem `/khoa` và `/lam-gi` | Kiểm giả thuyết "câu không cũng có giá trị" |

### L2

| Chỉ số | Vì sao |
|---|---|
| **Lần nối thành công / tháng** | Doanh thu tăng theo đúng số này |
| Tỷ lệ hồ sơ gửi đi được phỏng vấn | Chất lượng sàng lọc — thứ giữ cửa |
| Số kỹ sư rút lui | Nếu cao, mạng lưới đang làm gì đó sai |
| Thời gian từ đồng ý tới phản hồi | Trải nghiệm phía kỹ sư |

**Không đo:** tổng số tin trong kho, tổng lượt xem, số hồ sơ đã thu. Chỉ số phù phiếm.

---

## 8. Rủi ro đã biết

| Rủi ro | Xử lý |
|---|---|
| **Cold start hai phía** | Bắt đầu từ **phía cầu** — 110 công ty đã có tên, có bằng chứng |
| B-Q5 trả lời là "bán dữ liệu" | Hỏi **trước** khi build. Nếu xấu, dừng L2 và giữ L1 |
| Nhãn sai lọt ra ngoài | C1 + nút báo sai + audit phân tầng hằng tháng |
| Không mở rộng được | Chấp nhận. Đây là doanh nghiệp dịch vụ |
| Áp lực uốn dữ liệu cho khách lớn | C9 — không xây giao diện sửa nhãn nào cả |
| Bị một ATS chặn | Poll theo bậc; mất 1 nguồn ≈ mất 1/3 kho |
