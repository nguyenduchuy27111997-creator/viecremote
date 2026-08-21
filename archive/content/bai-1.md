# Tôi đọc tay 150 tin tuyển remote quốc tế. Không tin nào tuyển được ở Việt Nam.

Tôi bỏ một buổi đọc tay 150 tin tuyển dụng remote từ các công ty công nghệ nước ngoài, chấm từng tin theo một bộ quy tắc cố định.

Kết quả:

| | 150 tin |
|---|---|
| Bị giới hạn địa lý (bạn không nộp được) | **126 — 84%** |
| Không đủ thông tin để kết luận | 18 — 12% |
| Mở toàn cầu | 6 — **4%** |
| **Ghi rõ tuyển được ở Việt Nam** | **0** |

Nếu bạn từng nộp ba mươi hồ sơ remote và được hồi đáp một lần — **vấn đề nhiều khả năng không nằm ở CV của bạn.**

---

## Cách tôi đo

Nói trước để bạn tự đánh giá con số có đáng tin không.

**Nguồn.** 150 tin lấy ngẫu nhiên từ hơn 3.700 tin remote, thu qua endpoint công khai của ba nền tảng ATS (Greenhouse, Lever, Ashby) — cùng dữ liệu công ty tự công bố trên trang tuyển dụng của họ. 287 công ty.

**Cách chấm.** Đọc **toàn văn** mô tả, không đọc đoạn trích. Mỗi kết luận phải trích được nguyên văn một câu làm bằng chứng. Không trích được thì ghi "không rõ" — không đoán.

**Loại trừ khi** tin yêu cầu quyền làm việc tại một nước cụ thể, giới hạn địa lý cứng, yêu cầu có mặt tại văn phòng, yêu cầu múi giờ mà GMT+7 không trùng nổi 2 tiếng, hoặc yêu cầu quốc tịch/security clearance.

**Kiểm chéo.** Tôi viết một bộ quy tắc tự động rồi so với bản chấm tay. Lần đầu nó **sai 7/10** ở nhóm "đủ điều kiện". Phải sửa năm lỗi mới khớp. Con số trong bài là **bản chấm tay**, không phải bản máy.

Tôi cũng chấm ba lô riêng biệt để tự kiểm — và có một lần **tôi chấm sai, máy chấm đúng**: một tin tôi ghi "không rõ" thực ra có câu *"candidates must: Be a U.S. Citizen or Permanent Resident"* nằm giữa bài mà tôi đọc lướt qua. Đó là lý do tôi đọc toàn văn ở các lô sau.

---

## Phát hiện 1 — "Remote" gần như không bao giờ có nghĩa "toàn cầu"

84% tin có chữ "remote" bị khoá vào một nước, một vùng, hoặc một danh sách bang.

Các dạng hay gặp:

- `Remote - US` · `Remote, United States` · `USA - Remote`
- `Remote - Canada` · `Remote, Poland; Remote, United Kingdom`
- `Anywhere - US` — chữ "anywhere" ở đây nghĩa là *bất kỳ đâu trong nước Mỹ*
- `Home Based - Americas` · `North America` · `Remote - EMEA`
- Loại trừ theo bang: *"nếu bạn ở Alaska, Delaware, Hawaii… bạn không đủ điều kiện"*
- Múi giờ: `(PST Timezone)` ngay trong tiêu đề, hoặc *"core hours 9:30am–2:30pm Pacific"*

Cái cuối đáng chú ý: **yêu cầu múi giờ là một dạng giới hạn địa lý trá hình.** "Core hours 9:30–14:30 giờ Thái Bình Dương" nghĩa là 23:30–04:30 giờ Việt Nam. Không ai duy trì được lịch đó lâu dài.

## Phát hiện 2 — Nhãn "worldwide" ở cấp công ty không đáng tin ở cấp tin

`remoteintech/remote-jobs` là danh bạ công ty remote-friendly do cộng đồng duy trì, 882 công ty. **403 công ty được gắn nhãn `region: worldwide`.**

Tôi lấy 10 công ty trong số đó có tin nằm trong mẫu đã chấm tay, rồi so.

**Chỉ 1 công ty thực sự có tin mở toàn cầu.**

Kiểm lại trên **toàn bộ** board của họ (không chỉ mẫu), tại thời điểm viết bài:

| Công ty | Tin đang mở | Tin ghi "worldwide" | Địa điểm phổ biến nhất |
|---|---|---|---|
| GitLab | 197 | 0 | `Remote, United States` (27) · `Bangalore, India` (24) |
| Twilio | 157 | 0 | `Remote - US` (76) · `Remote - India` (19) |
| Ramp | 136 | 0 | `New York, NY (HQ)` (102) |
| Replit | 78 | 0 | `Foster City, CA` (58) |
| Linear | 33 | 0 | `North America` (24) · `Europe` (8) |
| Close | 7 | 0 | `USA - Remote` (7) |

**Nói cho công bằng: các công ty này không nói dối.** Nhãn `worldwide` do một danh bạ cộng đồng gắn, không phải do họ tuyên bố. Nhiều công ty trong đó **có** tuyển ở nhiều nước — Twilio đăng tin ở Mỹ, Ấn Độ, Colombia, Ireland — nhưng **từng tin lại khoá vào một nước.**

Đó chính là cái bẫy: *"công ty tuyển nhiều nước"* và *"tin này mở cho bạn"* là hai chuyện khác nhau.

**Mẫu hình lặp lại ở ba nguồn độc lập:**

| Nguồn | Tuyên bố | Thực tế ở mức tin |
|---|---|---|
| Danh bạ cộng đồng | `region: worldwide` | phần lớn tin bị giới hạn |
| Board "work from anywhere" | "no location restrictions" | FAQ thừa nhận múi giờ/thuế khác nhau; tin không ghi |
| Dữ liệu có cấu trúc của chính công ty | khai quốc gia | chỉ 25% tin khai |

> **Càng xa tin tuyển dụng thật, tuyên bố càng "toàn cầu".**

## Phát hiện 3 — Câu hỏi quan trọng nhất gần như không tin nào trả lời

Giả sử bạn qua được vòng đó và công ty muốn tuyển bạn. Câu tiếp theo: **họ trả lương cho bạn bằng cách nào?**

Ba đường: qua **EOR** (Deel, Remote, Oyster… — công ty thuê một pháp nhân trung gian tuyển bạn), **hợp đồng nhà thầu** (bạn tự xuất hoá đơn, tự lo thuế), hoặc công ty **có pháp nhân tại Việt Nam** (hiếm).

Tôi đếm xem bao nhiêu tin nêu rõ điều này.

**7,2%.** Trong nhóm tin mở toàn cầu: **1 trên 9.**

Nghĩa là ngay cả khi bạn tìm được tin hiếm hoi mở toàn cầu, bạn vẫn **không biết họ có cách nào trả lương cho bạn không** cho tới khi đi sâu vào quy trình.

---

## Phần dùng được ngay: kiểm một tin trong 10 giây

Google có một chuẩn dữ liệu cho tin tuyển dụng, và nhiều công ty khai trường `applicantLocationRequirements` — **danh sách quốc gia họ nhận ứng viên**. Nó nằm trong mã nguồn trang, không hiện ra màn hình.

Cách xem:

1. Mở trang tin tuyển dụng
2. `Ctrl+U` (xem mã nguồn) hoặc `Ctrl+F` trong DevTools
3. Tìm `applicantLocationRequirements`

Thấy gì:

```json
"applicantLocationRequirements": [{"@type":"Country","name":"United States"}]
```
→ Chỉ Mỹ. Đừng nộp.

```json
"applicantLocationRequirements": [
  {"name":"Serbia"},{"name":"Poland"},{"name":"Turkey"},
  {"name":"Vietnam"},{"name":"Malaysia"},{"name":"Any Location"}
]
```
→ **Có Việt Nam.** Đây là tin đáng bỏ 40 phút viết cover letter.

Ví dụ thứ hai là thật — một công ty trong mẫu của tôi. Trong 150 tin ngẫu nhiên, tôi không gặp tin nào như vậy; tôi tìm thấy nó ở một mẫu khác.

**Giới hạn của mẹo này:** chỉ **25%** tin khai trường đó. Và nó có thể khai thiếu — tôi gặp một công ty khai `United States` nhưng trong mô tả lại ghi *"Benefits for employees hired through an EOR (outside of the US)"*, tức họ **có** tuyển ngoài Mỹ.

Nên: có trường đó và không có Việt Nam → **khả năng cao là không**, nhưng chưa chắc chắn tuyệt đối. Không có trường đó → phải đọc mô tả.

---

## Vậy nên làm gì

**1. Đọc `location` trước khi đọc mô tả.** 84% câu trả lời nằm ngay ở đó. Tiết kiệm được phần lớn thời gian.

**2. Coi yêu cầu múi giờ là giới hạn địa lý.** "Trùng 4 tiếng với giờ Thái Bình Dương" = không khả thi từ Việt Nam.

**3. Đừng tin nhãn cấp công ty.** "Công ty này remote toàn cầu" không có nghĩa *tin này* mở cho bạn. Kiểm từng tin.

**4. Hỏi về cơ chế trả lương sớm, đừng đợi tới lúc nhận offer.** Một câu trong email đầu tiên:

> *"Nếu tôi ở Việt Nam, công ty sẽ ký hợp đồng qua EOR hay hợp đồng nhà thầu?"*

Câu này lọc bớt vô số vòng phỏng vấn vô ích. Và nếu họ không trả lời được, đó cũng là một câu trả lời.

**5. Nhắm vào múi giờ châu Âu, không phải Mỹ.** GMT+7 lệch CET 5–6 tiếng → còn 3–4 giờ trùng trong giờ hành chính hai bên. Lệch giờ Mỹ 11–15 tiếng → gần như bằng không.

---

## Những điều tôi KHÔNG biết

Viết ra để bạn cân được con số này nặng tới đâu.

- **n = 150.** Đủ để nói tỷ lệ tin ghi rõ tuyển được ở VN là **dưới 2%**, không đủ để nói nó bằng 0.
- **Mẫu lệch.** Nguồn công ty đến từ Hacker News → thiên về công ty Mỹ/châu Âu. Đây là nơi có nhiều việc remote nhất, nhưng chưa chắc là nơi tuyển người Việt nhiều nhất.
- **Chỉ 3 nền tảng ATS.** Không có Workday, SmartRecruiters, và các công ty tuyển qua trang riêng.
- **Riêng vai trò kỹ thuật chỉ có 68 tin** — quá ít để kết luận riêng cho nhóm này.
- **Đây là ảnh chụp một thời điểm.** Tin tuyển dụng đổi liên tục.

Nếu bạn nghĩ mẫu của tôi lệch, **bạn đúng — vấn đề là lệch bao nhiêu.** Tôi công khai phương pháp để ai cũng kiểm lại được.

---

## Tôi đang làm tiếp

Tôi đang lập một danh sách: **công ty nào trả lương được cho người ở Việt Nam, qua cơ chế nào.** Không phải danh sách việc — danh sách *cơ chế*, vì đó là thứ chưa ai có và không tin tuyển dụng nào trả lời.

Một điểm khiến việc này khả thi: **cơ chế là thuộc tính của công ty, không phải của từng tin.** Hỏi một lần, dùng được cho mọi tin của họ. Trong mẫu của tôi, 6 công ty tương ứng 384 tin đang mở.

Nếu bạn **đang làm remote cho công ty nước ngoài** — bạn biết cơ chế của chính mình, và một dòng của bạn giúp được nhiều người. Nếu bạn **đang tìm** — tôi gửi bản tin hằng tuần các tin mở toàn cầu, kèm cột cơ chế khi biết.

*[link đăng ký]*

Không thu CV. Không thu mức lương. Huỷ đăng ký một cú bấm.
