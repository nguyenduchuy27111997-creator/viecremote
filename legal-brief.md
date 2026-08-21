# Bản tóm tắt cho buổi tư vấn pháp lý

**Ngày soạn:** 17/08/2026
**Mục đích:** rút ngắn buổi tư vấn luật sư/kế toán bằng cách mang sẵn dữ kiện, để buổi đó chỉ dùng cho phần cần chuyên môn.
**Đi kèm:** [brd-v2.md](brd-v2.md) Mục 6 · [prd.md](prd.md) Mục 13

> **Đây không phải tư vấn pháp lý.** Đây là tổng hợp văn bản công khai do một người không có chuyên môn pháp lý thực hiện, để chuẩn bị cho buổi tư vấn. Mọi kết luận trong đây phải được luật sư xác nhận trước khi hành động. Các trích dẫn được ghi nguyên văn kèm nguồn để luật sư kiểm lại.

---

## 0. Tóm tắt một trang

**Hai khối vấn đề, một câu hỏi quyết định cho mỗi khối.**

| Khối | Câu hỏi quyết định | Nếu trả lời một đằng | Nếu trả lời đằng kia |
|---|---|---|---|
| **A. Chính sách Google JobPosting** | Đăng lại tin từ endpoint ATS công khai của chính công ty, ghi rõ nguồn, link về nơi nộp gốc — có phải "đăng tin thay mặt tổ chức mà không có ủy quyền" không? | Được → mở Lớp 1, có kênh Google for Jobs | Không được → bỏ hẳn schema, mất một kênh, sản phẩm vẫn sống |
| **B. Luật BVDLCN** | **Dữ liệu lương có phải "dữ liệu cá nhân nhạy cảm" không?** | Không nhạy cảm → gần như miễn toàn bộ nghĩa vụ DPO và DPIA trong 5 năm | Nhạy cảm → **mất toàn bộ miễn trừ**, phải có DPO và hồ sơ DPIA ngay từ bản ghi đầu tiên |

Câu B là câu đắt nhất trong cả tài liệu. Nó là ranh giới giữa gánh nặng tuân thủ gần bằng không và gánh nặng thật.

> **Cập nhật quan trọng — đọc Phần E trước khi đặt lịch tư vấn.**
> Tự tra văn bản gốc đã đưa câu B đi được ~80%: mục "tài chính" trong danh mục nhạy cảm có phạm vi **hẹp hơn nhiều** so với cách các bài tóm tắt viết tắt — nó là *thông tin khách hàng do tổ chức tín dụng nắm giữ*, và **thu nhập/tiền lương không được liệt kê riêng** (E.2).
> Và **đề xuất ở E.5 xoá hẳn câu B bằng một quyết định phạm vi, chi phí bằng không**: không thu con số lương ở v1. Ba câu hỏi đắt nhất biến mất.

---

# PHẦN A — Chính sách JobPosting của Google

## A.1 Trích dẫn nguyên văn

Nguồn: https://developers.google.com/search/docs/appearance/structured-data/job-posting

**Chính sách chống xuyên tạc (misrepresentation):**

> "We don't allow job postings that attempt to impersonate another person or organization, or otherwise engage in activities intended to deceive, defraud, or mislead others. This includes falsely implying affiliation with, or endorsement by, another individual or organization."

Trong danh sách **ví dụ vi phạm** của chính sách này có mục:

> "Job postings on behalf of an organization or company without authorization."

**Yêu cầu về cách nộp hồ sơ:**

> "We don't allow job postings that don't have a way to apply"

**Tin hết hạn:**

> "Failure to take timely action on expired jobs may result in a manual action."

Ba cách xử lý được chấp nhận: đặt `validThrough` về quá khứ · gỡ hẳn trang · gỡ markup JobPosting.

**Thuộc tính `directApply`:**

> "`directApply`: Indicates whether the URL that's associated with this job posting enables direct application for the job."

**Hướng dẫn kỹ thuật về vị trí đặt markup:**

> "Put structured data on the most detailed leaf page possible. Don't add structured data to pages intended to present a list of jobs (for example, search result pages). Instead, apply structured data to the most specific page describing a single job with its relevant details."

## A.2 Ba quan sát từ văn bản

**Quan sát 1 — điều khoản "không có ủy quyền" nằm dưới mục *xuyên tạc*, không phải mục riêng.** Nó là một **ví dụ** minh hoạ cho quy tắc chống mạo danh và chống ngụ ý sai về liên kết/chứng thực. Điều này gợi ý mục tiêu của quy tắc là hành vi lừa dối, không phải hành vi tổng hợp lại.

**Quan sát 2 — không có quy tắc nào cấm tin trùng lặp hoặc tin tổng hợp.** Tra kỹ toàn bộ chính sách nội dung: **không tồn tại** điều khoản cấm aggregation. Điều này nhất quán với thực tế Indeed, LinkedIn, ZipRecruiter đều tổng hợp và đều xuất hiện trong Google for Jobs.

**Quan sát 3 — yêu cầu "có cách nộp" thoả mãn được bằng cách dẫn về tin gốc.** Chính sách cho phép hoặc nộp trên trang của mình, hoặc cung cấp thông tin liên hệ trực tiếp của công ty tuyển. Và `directApply` là thuộc tính khai báo trung thực, không phải nghĩa vụ — khai `false` khi ta chỉ dẫn link là mô tả đúng sự thật.

**Kết hợp ba quan sát:** đọc theo nghĩa đen, mô hình đề xuất (đăng lại tin từ endmpoint công khai của chính công ty, ghi đúng tên công ty, không ngụ ý liên kết, `directApply: false`, dẫn về URL nộp gốc, gỡ trong 48h khi tin biến mất khỏi feed) **không có dấu hiệu xuyên tạc**. Nhưng đây là cách đọc của người không có chuyên môn, và ranh giới "on behalf of ... without authorization" cần người có chuyên môn xác nhận.

## A.3 Câu hỏi cho luật sư — Phần A

**A-Q1 *(quan trọng nhất)*.** Kịch bản cụ thể: công ty X công khai tin tuyển dụng qua endpoint ATS không cần xác thực của chính họ (ví dụ `boards-api.greenhouse.io/v1/boards/{X}/jobs`). Ta đăng lại tin đó trên trang của mình, ghi đúng tên công ty X, không tuyên bố hay ngụ ý bất kỳ quan hệ nào với X, đặt `directApply: false`, nút nộp dẫn thẳng về URL gốc của X, gỡ trong 48 giờ khi tin biến mất khỏi feed.
→ **Đây có phải "job posting on behalf of an organization without authorization" theo chính sách đã trích không?**

**A-Q2.** Nếu câu A-Q1 là "có rủi ro": việc **xin ủy quyền bằng văn bản** từ công ty có phải cách duy nhất để vào Lớp 1 không? Hay có hình thức nhẹ hơn được chấp nhận (ví dụ: thông báo có cơ chế từ chối, hoặc điều khoản ngầm định của chính endpoint công khai)?

**A-Q3.** Bốn nhà cung cấp ATS (Greenhouse, Lever, Ashby, Workable) **không công bố điều khoản nào cho phép hay cấm** bên thứ ba tổng hợp từ endpoint công khai của họ.
→ Trong pháp luật áp dụng, **sự im lặng đó được hiểu thế nào?** Có tạo ra giấy phép ngầm định không? Có nghĩa vụ hỏi trước không? Rủi ro thực tế là gì — chấm dứt truy cập, hay còn gì khác?

**A-Q4.** Hiển thị **trích đoạn ≤300 ký tự** của mô tả công việc, có dẫn nguồn và link về bản gốc, có nằm trong giới hạn sử dụng hợp lý theo pháp luật Việt Nam không? Mô tả công việc có được bảo hộ quyền tác giả không?

## A.4 Điều KHÔNG cần hỏi — đã xác định

Đừng dùng thời gian tính phí cho những mục này:

- Hạn ngạch Indexing API: 200 yêu cầu `publish`/ngày/project, chỉ dùng cho `JobPosting` và `BroadcastEvent`. Không phải ràng buộc ở quy mô này
- Vị trí đặt markup: chỉ trên trang chi tiết một tin, không trên trang danh sách. Đã rõ
- Cách gỡ tin hết hạn: ba cách, đã rõ
- Google có cấm aggregation không: **không có điều khoản nào**. Đã tra

---

# PHẦN B — Luật Bảo vệ dữ liệu cá nhân

## B.1 Chồng văn bản hiện hành

| Văn bản | Vai trò | Hiệu lực |
|---|---|---|
| **Luật 91/2025/QH15** | Luật Bảo vệ dữ liệu cá nhân | 01/01/2026 |
| **Nghị định 356/2025/NĐ-CP** | Quy định chi tiết và biện pháp thi hành. 5 chương, 42 điều, 1 phụ lục gồm **10 hồ sơ và biểu mẫu** | 01/01/2026, ban hành 31/12/2025 |
| ~~Nghị định 13/2023/NĐ-CP~~ | **Đã bị Nghị định 356/2025 thay thế** | Hết hiệu lực |

*(Lưu ý: nhiều bài viết đang lưu hành vẫn tham chiếu Nghị định 13. Kiểm ngày của mọi nguồn thứ cấp.)*

Nghị định 356 tập trung vào 5 nhóm: quy trình đánh giá tác động (DPIA) · thủ tục chuyển dữ liệu ra nước ngoài · chức năng nhiệm vụ của DPO · hệ thống biểu mẫu mới thay hoàn toàn Nghị định 13 · cơ chế phối hợp kiểm tra thanh tra của Cục An ninh mạng (A05).

## B.2 Cấu trúc miễn trừ — và cái bẫy

**Miễn trừ bổ nhiệm DPO:**
- Doanh nghiệp **siêu nhỏ** và hộ kinh doanh: **miễn hoàn toàn**
- Doanh nghiệp **nhỏ** và khởi nghiệp sáng tạo: hoãn nghĩa vụ **5 năm** kể từ 01/01/2026

**Miễn trừ lập hồ sơ đánh giá tác động (DPIA):**
- Doanh nghiệp nhỏ và khởi nghiệp: được **chọn không lập hồ sơ trong 5 năm đầu** kể từ 01/01/2026

**Cả hai miễn trừ đều MẤT nếu rơi vào một trong ba trường hợp:**

| # | Trường hợp | Áp dụng cho dự án này? |
|---|---|---|
| 1 | Xử lý **dữ liệu cá nhân nhạy cảm** | **← ĐÂY LÀ CÂU HỎI** |
| 2 | Kinh doanh dịch vụ xử lý dữ liệu | Có vẻ không, nhưng cần xác nhận |
| 3 | Xử lý tích luỹ **≥ 100.000 chủ thể dữ liệu** | Không, ở quy mô mục tiêu (600–3.000 người) |

**Điểm mấu chốt:** các bài tóm tắt liệt kê dữ liệu nhạy cảm gồm "y tế, sinh trắc học, **tài chính**…", và thoạt nghe thì lương là dữ liệu tài chính cá nhân. **Nhưng đọc văn bản gốc cho kết quả khác — xem E.2.** Mục "tài chính" thực chất giới hạn ở *thông tin khách hàng của tổ chức tín dụng*: tài khoản, tiền gửi, giao dịch. Thu nhập và tiền lương không nằm trong danh mục liệt kê.

→ Nếu dữ liệu lương do người dùng đóng góp bị xếp là **nhạy cảm**, thì **toàn bộ miễn trừ ở trên không áp dụng**, kể cả cho một dự án một người. Phải có DPO (hoặc bộ phận/dịch vụ thuê ngoài) và hồ sơ DPIA **ngay từ bản ghi lương đầu tiên**.

Đây là ranh giới giữa hai thế giới rất khác nhau về chi phí tuân thủ.

**Chuyển dữ liệu ra nước ngoài:** Nghị định 356 **mở rộng các trường hợp miễn** đánh giá tác động khi chuyển dữ liệu ra nước ngoài, trong đó có "dữ liệu đã được công khai" và một số hoạt động chuyên ngành. Dự án dự kiến hosting ở nước ngoài → cần xác định có thuộc diện miễn không.

**Thời hạn phản hồi yêu cầu của chủ thể dữ liệu:** 10–30 ngày tuỳ loại yêu cầu.
*(Ghi chú thiết kế: PRD FR-8.5 đặt SLA xoá dữ liệu ≤ 7 ngày — chặt hơn luật, cố ý. Không cần đổi.)*

## B.3 Câu hỏi cho luật sư — Phần B

**B-Q1 *(câu đắt nhất trong cả tài liệu)*.** Bản ghi do người dùng tự nguyện đóng góp gồm: tên công ty · chức danh · cấp độ · **mức lương** · cơ chế hợp đồng · chủ lao động trong nước hay nước ngoài. Không thu tên, email bắt buộc, hay số định danh; người đóng góp dùng biệt danh tự chọn.
→ **Đây có phải "dữ liệu cá nhân nhạy cảm" theo Luật 91/2025 không?**
→ Nếu có: **có cách thiết kế nào đưa nó ra khỏi nhóm nhạy cảm không** — ví dụ chỉ thu dải lương thay vì con số chính xác, hoặc tổng hợp ngay tại thời điểm thu (client-side) và không bao giờ lưu bản ghi cá thể?

**B-Q2.** Ngưỡng **k-ẩn danh = 5** (không hiển thị số liệu lương cho tổ hợp công ty × chức danh × cấp độ có dưới 5 bản ghi) có đủ để coi là **đã ẩn danh hoá** theo luật không? Nếu chưa, ngưỡng nào đủ? Ẩn danh hoá có đưa dữ liệu ra khỏi phạm vi luật không?

**B-Q3.** Nếu B-Q1 là "nhạy cảm": dự án một người, chưa thành lập pháp nhân, thì **bổ nhiệm DPO** thực hiện thế nào? Cá nhân tự đảm nhiệm có được không? Chi phí thuê dịch vụ ngoài khoảng bao nhiêu?

**B-Q4.** Hosting ở nước ngoài (nhà cung cấp VPS quốc tế) có phải "chuyển dữ liệu ra nước ngoài" không? Nếu có, thuộc diện miễn đánh giá tác động nào trong Nghị định 356? Cần nộp hồ sơ gì, theo biểu mẫu nào trong phụ lục 10 biểu mẫu?

**B-Q5.** Mô hình **giới thiệu có đồng ý**: ứng viên chủ động bấm "cho phép giới thiệu tôi tới công ty X", nhật ký đồng ý được lưu, ta thu phí *dịch vụ kết nối* từ công ty.
→ Có bị coi là **mua bán dữ liệu cá nhân** (điều bị cấm, phạt tới 10 lần doanh thu từ hành vi vi phạm) không? Ranh giới giữa "bán dữ liệu" và "cung cấp dịch vụ kết nối có đồng ý" nằm ở đâu?

**B-Q6.** Nội dung màn hình đồng ý cần có những gì để hợp lệ, cho mục đích "thu thập và hiển thị tổng hợp dữ liệu lương"? Có mẫu bắt buộc trong phụ lục Nghị định 356 không?

**B-Q7.** Nếu chưa thành lập pháp nhân, cá nhân vận hành một website thu thập dữ liệu người dùng thì nghĩa vụ khác gì so với doanh nghiệp? Có nên thành lập hộ kinh doanh trước khi thu bản ghi đầu tiên không?

## B.4 Điều KHÔNG cần hỏi — đã xác định

- Nghị định 13/2023 còn hiệu lực không: **không**, đã bị 356/2025 thay thế
- Cấm mua bán dữ liệu cá nhân, chế tài tới 10 lần doanh thu từ hành vi vi phạm: đã rõ
- Đồng ý phải rõ ràng, cụ thể theo từng mục đích; cấm ô tick sẵn, im lặng, không hành động: đã rõ
- Ngưỡng 100.000 chủ thể dữ liệu: không áp dụng ở quy mô này
- Thời hạn phản hồi yêu cầu chủ thể dữ liệu: 10–30 ngày. Thiết kế đã đặt chặt hơn

---

# PHẦN C — Kế toán (buổi riêng)

Không hỏi luật sư bốn câu này; hỏi kế toán thuế.

**C-Q1 *(giá trị cao nhất cho nội dung)*.** Hộ kinh doanh cá thể cung cấp dịch vụ phần mềm: ngưỡng doanh thu, thuế suất, điều kiện áp dụng — **theo văn bản đang có hiệu lực**, không theo bài blog cũ.

**C-Q2.** Cá nhân cư trú nhận lương từ chủ lao động nước ngoài không có hiện diện tại Việt Nam: kê khai theo mẫu nào, chu kỳ nào, ai có nghĩa vụ khấu trừ?

**C-Q3.** Cơ chế EOR (chủ lao động là pháp nhân EOR nước ngoài, người lao động ở VN) xử lý thuế khác gì so với hợp đồng nhà thầu trực tiếp?

**C-Q4.** Kênh nhận tiền (Wise, Payoneer, chuyển khoản quốc tế, ví nền tảng EOR) — mỗi kênh tạo nghĩa vụ kê khai gì khác nhau?

**Dữ kiện đã tra, mang theo để đối chiếu:**
- **Nghị định 253/2026/NĐ-CP** hướng dẫn Luật Thuế TNCN, hiệu lực **01/07/2026**
- *"Cá nhân cư trú phải kê khai thu nhập phát sinh trong và ngoài Việt Nam, không phân biệt nơi trả hay nơi nhận thu nhập."*
- Nước có Hiệp định tránh đánh thuế hai lần với VN → được khấu trừ thuế TNCN đã nộp ở nước ngoài
- Giảm trừ gia cảnh từ 01/01/2026: bản thân 15,5 triệu/tháng · người phụ thuộc 6,2 triệu/người/tháng
- Xác định cư trú: ≥183 ngày · hoặc nơi cư trú/tạm trú đăng ký · hoặc hợp đồng thuê nhà ≥183 ngày

---

# PHẦN D — Cách dùng bản tóm tắt này

## D.1 Thứ tự ưu tiên nếu chỉ đủ tiền cho một buổi

1. **B-Q1** — nhạy cảm hay không. Quyết định toàn bộ gánh nặng tuân thủ
2. **A-Q1** — Lớp 1 có tồn tại được không. Quyết định một kênh phân phối
3. **B-Q5** — mô hình giới thiệu có hợp pháp không. Quyết định một dòng doanh thu
4. **B-Q2** — ngưỡng k. Rẻ để phòng: nếu không rõ, nâng lên 10
5. Còn lại

## D.2 Mặc định an toàn cho tới khi có câu trả lời

| Chưa rõ | Hành xử |
|---|---|
| A-Q1, A-Q3 | Mọi tin để `index_layer = 'aggregated'`. **Không tin nào phát sinh JobPosting schema.** Mất kênh Google for Jobs, chấp nhận (PRD FR-9.2/9.3) |
| B-Q1, B-Q2 | **Chưa thu bản ghi lương nào.** Vòng đóng góp cộng đồng chỉ thu *kết quả tuyển dụng* và *cơ chế hợp đồng*, chưa thu con số lương |
| B-Q5 | Không triển khai mô hình giới thiệu dưới bất kỳ hình thức nào |

Ba mặc định này cho phép chạy Cổng 0, M1, M2 và bản tin **mà không chạm vào bất kỳ câu hỏi mở nào**. Buổi tư vấn không chặn tiến độ — nó chỉ chặn M3.

## D.3 Ghi lại thế nào

Với mỗi câu trả lời, ghi: **ngày · tên và chức danh người tư vấn · điều khoản được viện dẫn · câu trả lời nguyên văn**.

Lý do: văn bản pháp luật ở cả hai lĩnh vực vừa đổi trong vòng 8 tháng (PDPL 01/01/2026, thuế TNCN 01/07/2026). Câu trả lời hôm nay có hạn sử dụng. Không ghi điều khoản viện dẫn thì sang năm không biết câu trả lời còn đúng không.

Đặt lịch rà lại: **17/08/2027**, hoặc ngay khi có văn bản mới.

---

# PHẦN E — Tự nghiên cứu tới đâu, và chỗ nào không tự thay được

## E.1 Câu trả lời ngắn

**Tự nghiên cứu giải được phần lớn. Không giải được một thứ — và thứ đó không phải câu trả lời, mà là sự bảo vệ.**

Văn bản gốc ở Việt Nam **miễn phí và công khai**: `vanban.chinhphu.vn` (chính thức) và `thuvienphapluat.vn`. Đọc thẳng văn bản cho ra câu trả lời chính xác hơn mọi bài blog tóm tắt — và phần lớn bài blog đang lưu hành vẫn tham chiếu Nghị định 13 đã hết hiệu lực.

## E.2 Ví dụ đã làm — B-Q1 tự tra được tới 80%

Câu hỏi: *dữ liệu lương có phải dữ liệu cá nhân nhạy cảm không?*

**Định nghĩa trong luật:**

> "Dữ liệu cá nhân nhạy cảm là dữ liệu cá nhân gắn liền với quyền riêng tư của cá nhân, khi bị xâm phạm sẽ gây ảnh hưởng trực tiếp đến quyền, lợi ích hợp pháp của cơ quan, tổ chức, cá nhân, **thuộc danh mục do Chính phủ ban hành**."

Câu cuối là chìa khoá: **danh mục do Chính phủ ban hành**, tức nằm trong nghị định — văn bản công khai đọc được.

**Mục "tài chính" trong danh mục được diễn đạt nguyên văn như sau** (nguồn gốc từ Khoản 4 Điều 2 Nghị định 13/2023, cấu trúc được duy trì):

> "Thông tin khách hàng của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài, tổ chức cung ứng dịch vụ trung gian thanh toán, các tổ chức được phép khác, gồm: thông tin định danh khách hàng theo quy định của pháp luật, thông tin về tài khoản, thông tin về tiền gửi, thông tin về tài sản gửi, thông tin về giao dịch"

**Đọc kỹ: mục này không phải "mọi thông tin tài chính của một người".** Nó là **thông tin khách hàng do tổ chức tín dụng nắm giữ** — tài khoản, tiền gửi, giao dịch. Phạm vi hẹp hơn nhiều so với cách các bài tóm tắt viết tắt thành "tài chính".

**Thu nhập và tiền lương không được liệt kê riêng** trong danh mục nhạy cảm.

**Suy luận sơ bộ:** một con số lương do chính cá nhân tự nguyện gửi cho một website **không phải tổ chức tín dụng** thì không rơi vào mục này.

## E.3 Hai chỗ 20% còn lại nằm — và vì sao chúng đắt

**Lỗ hổng 1 — điều khoản quét.** Danh mục có mục cuối:

> "Dữ liệu cá nhân khác được pháp luật quy định là đặc thù và cần có biện pháp bảo mật cần thiết"

Điều khoản mở. Tự đọc không biết nó có được áp dụng cho dữ liệu lương hay không.

**Lỗ hổng 2 — chưa đối chiếu văn bản đang có hiệu lực.** Danh mục trích ở E.2 bắt nguồn từ Nghị định 13/2023. **Nghị định 356/2025 đã thay thế Nghị định 13.** Các nguồn thứ cấp nói cấu trúc được duy trì, nhưng **chưa đối chiếu trực tiếp với toàn văn Nghị định 356**. Đây là việc tự làm được: tải toàn văn từ `vanban.chinhphu.vn`, tìm điều quy định danh mục nhạy cảm, đối chiếu từng mục.

**Và lỗ hổng thứ ba, không tự lấp được bằng bất kỳ cách đọc nào:**

| Tự nghiên cứu cho bạn | Chỉ luật sư cho bạn |
|---|---|
| Văn bản nói gì | **Cơ quan quản lý thực thi thế nào** — khoảng cách giữa câu chữ và thực tiễn |
| Câu trả lời có khả năng đúng | **Ý kiến bằng văn bản làm bằng chứng thiện chí** nếu bị chất vấn |
| Hiểu biết | **Chuyển một phần rủi ro** sang người có bảo hiểm nghề nghiệp |

Ý kiến luật sư không phải thông tin. Nó là **tấm khiên**. Đó là thứ không đọc mà có được.

## E.4 Năm cách rẻ hơn thuê luật sư, xếp theo giá trị

| # | Cách | Chi phí | Giải được gì |
|---|---|---|---|
| **1** | **Thiết kế vòng qua câu hỏi** — xem E.5 | **0** | **Xoá hẳn câu hỏi, không cần trả lời** |
| 2 | Đọc toàn văn Nghị định 356 trên `vanban.chinhphu.vn`, đối chiếu danh mục nhạy cảm | 0 | Lấp lỗ hổng 2 ở E.3 |
| 3 | Bản tin pháp lý miễn phí của EY / Frasers / Tilleke / KPMG Việt Nam | 0 | Cách hiểu của giới hành nghề, cập nhật |
| 4 | Hỏi thẳng cơ quan quản lý bằng văn bản (Cục An ninh mạng A05) | 0, chờ lâu | Câu trả lời có trọng lượng nhất — và là bằng chứng thiện chí |
| 5 | Buổi tư vấn ngắn 30–60 phút thay vì hợp đồng tư vấn đầy đủ | Thấp | Ba câu đắt nhất, không hơn |

Cách 4 ít người dùng nhưng đáng cân nhắc: hỏi cơ quan quản lý và lưu lại câu hỏi kèm phản hồi tạo ra hồ sơ thiện chí, thứ mà tự đọc không tạo ra được.

## E.5 Đề xuất mạnh nhất — xoá câu hỏi bằng thiết kế

**Không thu con số lương ở v1.**

Vòng đóng góp cộng đồng v1 chỉ thu ba trường: **kết quả tuyển dụng** (có/không được nhận) · **cơ chế hợp đồng** (EOR / nhà thầu / pháp nhân) · **chủ lao động trong nước hay nước ngoài**.

Hệ quả:

| Câu hỏi | Trạng thái |
|---|---|
| B-Q1 dữ liệu lương có nhạy cảm không | **Không còn liên quan** |
| B-Q2 ngưỡng k-ẩn danh | **Không còn liên quan** |
| B-Q3 nghĩa vụ DPO khi xử lý dữ liệu nhạy cảm | **Không còn liên quan** |
| Miễn trừ DPO và DPIA của Nghị định 356 | **Giữ nguyên** — không xử lý dữ liệu nhạy cảm, dưới 100.000 chủ thể |

**Cái giá phải trả gần bằng không.** Tín hiệu North Star là Tier A-VN, và bằng chứng mạnh nhất trong đó là **A-05: đã có người Việt được nhận ở công ty này chưa**. Câu đó trả lời được **không cần một con số lương nào**.

Dữ liệu lương là thứ tốt để có, không phải thứ bắt buộc phải có. Hoãn nó sang v2 — khi đã có khán giả, có doanh thu, và có lý do để trả tiền luật sư.

**Ba câu hỏi đắt nhất bị xoá bằng một quyết định phạm vi, chi phí bằng không.** Còn lại A-Q1, A-Q3, B-Q4, B-Q5 — và cả bốn đều đã có mặc định an toàn ở D.2.

---

## Phụ lục — Nguồn

**Google**
- Chính sách và hướng dẫn JobPosting: https://developers.google.com/search/docs/appearance/structured-data/job-posting
- Hướng dẫn structured data chung: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Hạn ngạch Indexing API: https://developers.google.com/search/apis/indexing-api/v3/quota-pricing

**Luật Bảo vệ dữ liệu cá nhân**
- Luật 91/2025/QH15 toàn văn (tiếng Anh): https://english.luatvietnam.vn/dan-su/law-on-personal-data-protection-law-no-91-2025-qh15-405135-d1.html
- Nghị định 356/2025/NĐ-CP toàn văn: https://vanban.chinhphu.vn/?pageid=27160&docid=216387
- Nghị định 356/2025 trên Thư viện pháp luật: https://thuvienphapluat.vn/van-ban/Quyen-dan-su/Nghi-dinh-356-2025-ND-CP-huong-dan-Luat-Bao-ve-du-lieu-ca-nhan-687428.aspx
- Phân tích miễn trừ DPO và DPIA: https://www.frasersvn.com/vi/legal-updates-and-publications/the-next-chapter-in-data-protection-new-decree-guiding-the-personal-data-protection-law
- Bản tin pháp lý EY về Nghị định 356: https://www.ey.com/vi_vn/technical/tax/tax-and-law-updates/nghi-dinh-so-356-2025-nd-cp-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-bao-ve-du-lieu-ca-nhan
- Ai phải lập hồ sơ DPIA: https://baophutho.vn/ai-phai-lap-ho-so-danh-gia-tac-dong-dpia-theo-nghi-dinh-356-2025-nd-cp-250101.htm
- Lệnh cấm mua bán dữ liệu và chế tài: https://www.tilleke.com/insights/vietnams-new-personal-data-protection-law-a-closer-look/

**Thuế**
- Nghị định 253/2026/NĐ-CP, quy định về cá nhân cư trú: https://lsvn.vn/nghi-dinh-253-2026-nd-cp-quy-dinh-the-nao-ve-ca-nhan-cu-tru-a175324.html
- Hướng dẫn Luật Thuế TNCN từ 01/7/2026: https://ketoanleanh.edu.vn/kinh-nghiem-ke-toan/nghi-dinh-253-2026-nd-cp-huong-dan-luat-thue-tncn.html
