# Mô hình kinh doanh

**Ngày:** 22/08/2026 · **Thay thế** bản 21/08 (viết cho web tra cứu đọc-only)
**Sứ mệnh:** [MISSION.md](MISSION.md) · **Kế hoạch:** [BUSINESS-PLAN.md](BUSINESS-PLAN.md) · **Lý do đổi:** [PIVOT.md](PIVOT.md)

---

## 1. Kết luận trước, lập luận sau

**Doanh thu đến từ phí giới thiệu, công ty trả, mỗi lần nối thành công.**
Kỹ sư không bao giờ trả. Không bán dữ liệu. Không bán vị trí trong danh sách.

Ba con số định hình lựa chọn này:

| | |
|---|---|
| Phí mỗi lần nối (thận trọng) | **3.000–5.000 USD** |
| Vốn ban đầu | **~310 triệu đồng** (ký quỹ 300 triệu chiếm gần hết) |
| Chi phí vận hành hạ tầng | **~12 USD/năm** |

Điều quan trọng nhất: **cả hai cổng quyết định nằm TRƯỚC khoản ký quỹ.** Sai thì mất ~12 USD
và hai tháng, không mất 310 triệu.

---

## 2. Ba ràng buộc đóng cửa hầu hết lựa chọn

Viết ra trước khi bàn phương án, để không tự lừa mình.

| # | Ràng buộc | Nguồn | Đóng cửa cái gì |
|---|---|---|---|
| **R1** | Tiền không được đổi điều được xuất bản | [MISSION.md](MISSION.md) ràng buộc 1 | Bán vị trí trong danh sách, gỡ thông tin bất lợi, xếp hạng theo tiền |
| **R2** | **Cấm mua bán dữ liệu cá nhân**, phạt tới **10× doanh thu** | Luật 91/2025 | Bán hồ sơ, bán lead ứng viên, chia sẻ CV không có đồng ý cụ thể |
| **R3** | Thu phí người lao động bị siết chặt | pháp luật lao động VN | Mọi mô hình lấy tiền từ kỹ sư |

**R2 là ràng buộc mới và nó nguy hiểm nhất.** Ở bản trước, dự án không xử lý dữ liệu cá nhân
nào nên R2 chỉ là lý thuyết. Bây giờ hồ sơ kỹ sư **chính là** thứ đang lưu chuyển — nên ranh
giới giữa *dịch vụ kết nối có đồng ý* và *bán dữ liệu* nằm ngay giữa mô hình doanh thu.

> **Câu hỏi B-Q5 vẫn chưa có lời giải, và giờ nó không tránh được nữa.**
> **Cập nhật 24/08:** ba câu pháp lý đã có lời giải ([legal-research.md](legal-research.md));
> buổi luật sư đổi thành rà soát trước ca nối đầu tiên. Dòng doanh thu chạy TRƯỚC là **Đ3 —
> nghiên cứu bán phía cầu** ([legal-options.md](legal-options.md)), đã live tại `/hiring-in-sea`.

---

## 3. Tám phương án, chấm theo ràng buộc

| # | Mô hình | R1 | R2 | R3 | Trần doanh thu | Phán quyết |
|---|---|:--:|:--:|:--:|---|---|
| A | **Phí giới thiệu, công ty trả** | ✓ | ⚠️ | ✓ | 3–15 nghìn USD/tháng | **Chọn** |
| B | Thuê bao công ty (truy cập mạng lưới) | ✓ | ⚠️ | ✓ | 200–1.000 USD/th/khách | Dòng phụ, sau A |
| C | Cho thuê lại lao động (Andela, Turing) | ✓ | ⚠️ | ✓ | Rất cao | **Rào cứng** — xem dưới |
| D | Bán dữ liệu địa lý tuyển cho EOR | ✓ | ✓ | ✓ | ~490 USD/th/khách | Dòng phụ, giữ lại |
| E | Thu phí kỹ sư | ✓ | ✓ | ❌ | — | **Cấm** — R3 và sứ mệnh |
| F | Bán hồ sơ, bán lead ứng viên | ✓ | ❌ | ✓ | — | **Cấm** — phạt 10× doanh thu |
| G | Công ty trả để lên đầu danh sách | ❌ | ✓ | ✓ | — | **Cấm** — phá thứ đang bán |
| H | Quảng cáo trên trang | ❌ | ✓ | ✓ | Nhỏ | Bỏ — làm bẩn tầng minh bạch |

⚠️ = hợp pháp **nếu** B-Q5 được trả lời đúng hướng. Chưa có câu trả lời thì chưa build.

### Vì sao C là rào cứng, không phải "đắt"

Cho thuê lại lao động cần **ký quỹ 2 tỷ** — gấp gần 7 lần. Nhưng đó không phải phần chặn.

> Người đại diện pháp luật phải có **3 năm trực tiếp làm chuyên môn hoặc quản lý trong lĩnh vực
> cho thuê lại lao động hoặc cung ứng lao động**, trong 5 năm liền kề.

Đây là điều kiện **không mua được bằng tiền**. Muốn đi hướng C thì phải tuyển đúng một người
như vậy làm đại diện pháp luật. Ghi lại để sau này không quên.

### Vì sao D vẫn giữ, dù không còn là chính

Bản kế hoạch trước lấy D làm dòng doanh thu chính: bán hồ sơ địa lý tuyển cho nhà cung cấp EOR.
Giờ nó thành **dòng phụ**, nhưng đừng bỏ:

- Nó **không đụng dữ liệu cá nhân** — R2 không áp dụng, rủi ro gần bằng 0
- Dữ liệu đã có sẵn, `/api/companies` đã chạy
- Người mua (Deel, Remote, Oyster) là **cùng nhóm** với khách hàng của mô hình A

Điểm cần cẩn thận: cùng một cuộc gọi A3 có thể bán cả hai thứ, nhưng **đừng bán cùng lúc**.
Bán dữ liệu trước sẽ làm loãng câu hỏi quan trọng hơn — *"anh có trả tiền để tuyển kỹ sư Việt
không?"*

---

## 4. Nghịch lý vẫn là lý do mô hình này tồn tại

Việt Nam có **530.000 lập trình viên**, top 6 thế giới về gia công. Nhưng đo 150 tin remote:
**0 tin** ghi rõ tuyển được ở Việt Nam.

Hai điều đó không mâu thuẫn — chúng nói rằng **việc tuyển kỹ sư Việt có thật nhưng không đi qua
tin đăng công khai.** Nó đi qua công ty gia công, EOR, hợp đồng nhà thầu, giới thiệu.

Ở bản trước, phát hiện này là **tin xấu**: nó chứng minh không có đủ hàng để làm job board.

Ở hướng mới, nó là **lý do tồn tại**: nếu kênh nối hai bên không có ở nơi cả hai đang tìm, thì
xây đúng cái kênh đó là một business — không phải một trang tra cứu.

---

## 5. Tài sản đang có — phía cầu đã xong

| Tài sản | Vai trò trong mô hình mới |
|---|---|
| **110 công ty tuyển được ở VN** | **Khách hàng ấm nhất.** Đã chứng minh có cơ chế trả lương |
| 3.666 hồ sơ địa lý tuyển | Danh sách khách tiềm năng, đã lọc |
| 2.485 công ty khoá hoàn toàn | Danh sách loại trừ — khỏi gọi |
| Bảng `locked`, 104 nước | Biết ai *sắp* cần mở rộng ra ngoài nước hiện tại |
| Precision 97,5%, đo phân tầng | Thứ làm câu chào khác mọi lời chào khác |
| Trang tra cứu công khai | **Phễu thu hút kỹ sư** — lý do họ vào và quay lại |

Ba tháng vừa rồi xây **đúng một nửa — nửa khó hơn.** Hồ sơ kỹ sư thì họ tự nhập; dữ liệu công
ty phải cào và chấm.

---

## 6. Điều phải nói thẳng về mô hình A

**Nó không mở rộng được.** Mỗi lần nối cần sàng lọc thật, phỏng vấn thật, theo dõi thật. Doanh
thu tăng tuyến tính với giờ làm, không tăng theo số người dùng.

| | Bản trước (dữ liệu B2B) | Bản này (giới thiệu) |
|---|---|---|
| Doanh thu tăng theo | số khách | **giờ làm của bạn** |
| Trần một người | cao | ~3 lần nối/tháng |
| Vốn ban đầu | ~0 | **~310 triệu** |
| Bằng chứng nhu cầu | chưa có | **chưa có** |

Đây không phải điểm trừ — headhunt là một nghề có thật và sống được. Nhưng phải biết mình đang
xây **doanh nghiệp dịch vụ có công cụ dữ liệu tốt**, không phải sản phẩm phần mềm.

Nếu mục tiêu là thứ mở rộng được, mô hình D (bán dữ liệu) mới là hướng — nhưng trần của nó
thấp hơn và cũng chưa có bằng chứng nhu cầu.

---

## 7. Điều tôi có thể sai

**Sai lớn nhất có thể:** giả định công ty chịu trả phí giới thiệu cho kỹ sư Việt. Họ có thể đã
có công ty gia công quen, hoặc thấy tự đăng tin là đủ. **A3 phải chạy trước khi tiêu một đồng
nào** — và nó không tốn gì.

**Sai thứ hai:** phí 3.000–5.000 USD suy từ chuẩn ngành (15–25% lương năm đầu) trên mức lương
30–60 nghìn USD. Cả hai số đều là ước lượng. Con số thật chỉ biết sau ca đầu tiên.

**Sai thứ ba:** giả định lợi thế dữ liệu chuyển được thành lợi thế bán hàng. Biết công ty nào
tuyển được ở VN là thứ **mở cửa**. Giữ cửa phải bằng chất lượng sàng lọc — và đó là năng lực
chưa được kiểm.

**Căng thẳng chưa giải:** tầng minh bạch làm mạng lưới đáng tin, nhưng cũng chính nó có thể
nói điều bất lợi về khách đang trả tiền. [MISSION.md](MISSION.md) ràng buộc 1 nói phải nói
thẳng. **Ngày đầu tiên mất một khách vì điều đó là ngày biết ràng buộc có thật hay không.**

---

## 8. Việc kế tiếp

| # | Việc | Chặn cái gì |
|---|---|---|
| 1 | ~~Buổi luật sư~~ **ĐÃ GỠ 24/08** — ba câu có lời giải, còn rà soát trước ca nối đầu | L2, không chặn Đ3 |
| 2 | Launch trang tra cứu, đo khán giả | Phễu kỹ sư |
| 3 | **A3 — 10 công ty trong danh sách 110** | Quyết định có dựng pháp nhân |
| 4 | Làm thủ công **một ca** trước khi ký quỹ | Biết quy trình vỡ ở đâu |

Việc số 4 là bước rẻ nhất trong cả kế hoạch và dễ bị bỏ qua nhất: **nối một người, thu một lần
phí, xem cái gì hỏng** — trước khi bỏ 300 triệu vào ngân hàng.
