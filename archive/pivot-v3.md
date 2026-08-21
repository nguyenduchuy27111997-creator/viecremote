# Đổi định vị v3.0 — từ "bằng chứng Việt Nam" sang "cơ chế trả lương"

**Ngày:** 17/08/2026
**Thay thế:** [brd-v2.md](brd-v2.md) Mục 1.1, 1.2, 2, 12.1, 16.1 — các mục khác giữ nguyên
**Căn cứ:** Cổng 0.1 đã chạy, n=150 chấm tay (BRD Mục 16.1.2)

---

## 1. Cái gì chết, và chết vì con số nào

| Giả định v2 | Đo được | Kết luận |
|---|---|---|
| Có đủ tin có **bằng chứng riêng cho VN** | **0/150** ngẫu nhiên · cận trên 95% = 1,98% | **Chết.** Dưới ngưỡng dừng tự đặt |
| Tin **mở toàn cầu** đủ nhiều | 6/150 = **4,0%** | Sống, nhưng đã có 4 board phát miễn phí (BRD 5.1) |
| **Cơ chế hợp đồng** đọc được từ tin | **7,2%** toàn mẫu · **1/9** tin worldwide | **Chết ở dạng "đọc từ tin"** |

Ba con số này giết cả v2 lẫn phiên bản ngây thơ của phương án C.

## 2. Con số làm phương án C sống lại

Trong mẫu, 9 tin worldwide đến từ **6 công ty**. Sáu công ty đó đang mở **384 tin**.

| | |
|---|---|
| Công ty sinh ra tin worldwide | 6 |
| Tổng tin đang mở của họ | 384 |
| **Đòn bẩy** | **64 : 1** |

Và tầng 4 đã chứng minh: **cơ chế hợp đồng là thuộc tính CÔNG TY, không phải của một tin.** Hỏi một lần, dùng cho mọi tin của họ — hiện tại và tương lai.

Nghĩa là bài toán đổi bản chất:

> Không phải *"gắn nhãn 384 tin"*. Là *"gửi 6 email"*.

## 3. Định vị mới

> Với **kỹ sư Việt Nam đang nhắm việc remote mở toàn cầu** — những người tìm được tin nhưng không biết công ty sẽ trả lương cho họ bằng cách nào —
> **[Tên sản phẩm]** trả lời câu hỏi mà tin tuyển dụng không trả lời: **công ty này trả lương cho người ở Việt Nam qua cơ chế nào**.
> **Khác với** Real Work From Anywhere, TrulyRemoteWork, Truly Remote — những bên đã lọc tốt tập "mở toàn cầu" và phát miễn phí — ở chỗ họ dừng ở *"tin này có mở toàn cầu không"*, còn sản phẩm này đi tiếp một bước: *EOR nào · hợp đồng nhà thầu · hay pháp nhân · và đã có ai ở VN nhận được chưa*.
> **Bằng chứng:** chỉ 7% tin tuyển dụng nêu cơ chế. Phần còn lại phải đi hỏi. Đó chính là công việc.

**Điểm khác biệt cốt lõi so với v2:** v2 định lọc ra thứ hiếm. v3 **tạo ra thông tin chưa tồn tại**.

## 4. Ba thay đổi kéo theo

### 4.1 Nhóm 2 chuyển từ đối thủ sang NHÀ CUNG CẤP

Real Work From Anywhere, TrulyRemoteWork, Truly Remote, We Are Distributed đã duyệt tay tập worldwide, miễn phí, hằng tuần. v2 coi họ là đối thủ. **v3 coi họ là đầu vào.**

Pipeline ATS vẫn giữ — nó tìm được tin họ bỏ sót và cho dữ liệu có cấu trúc. Nhưng cạnh tranh ở tầng lọc là chọn sai trận, và giờ có số liệu chứng minh: tầng lọc chỉ sinh ra 4%, ai cũng làm được.

### 4.2 North Star đổi từ TIN sang CÔNG TY

> **Số công ty có cơ chế trả lương đã xác minh** × **độ tươi của bản ghi**

Vì sao đổi đơn vị đo:
- Cơ chế là thuộc tính công ty → công ty mới là đơn vị tài sản
- Nó **cộng dồn**: hỏi tuần này, dùng được mọi tuần sau
- Nó **không nở giả tạo**: thêm tin của công ty đã biết không làm tăng chỉ số

Cặp số vẫn giữ nguyên tinh thần cũ: số lượng đi kèm chất lượng. "Độ tươi" = % bản ghi được xác nhận lại trong 12 tháng.

### 4.3 Con hào đổi chỗ

| | v2 | v3 |
|---|---|---|
| Con hào | Dữ liệu bằng chứng tích luỹ | **Bộ câu trả lời từ công ty** |
| Nguồn | Suy ra từ tin | **Hỏi trực tiếp** |
| Vì sao khó copy | Cần thời gian | **Cần người chịu gửi email và chờ trả lời** |

Con hào v3 mỏng hơn về công nghệ nhưng dày hơn về công sức — và công sức là thứ đối thủ tự động hoá không bỏ ra.

## 5. Cổng 0 mới — hai phép kiểm, chưa cái nào chạy

Cả hai đều **không cần code**, và cái nào trượt cũng giết v3.

### Cổng A8 — nhãn cơ chế có phải thứ kỹ sư cần?

Đây là giả định nền. Nếu sai, không còn gì.

**Việc làm:** 10 kỹ sư VN từng nộp remote. Hỏi đúng một câu:

> *"Nếu biết trước công ty này trả lương cho bạn qua EOR, hay hợp đồng nhà thầu, hay không trả được — nó có đổi quyết định nộp của bạn không?"*

**Ngưỡng:** ≥ 6/10 nói có, và nói được vì sao → tiếp. ≤ 3/10 → dừng, và lần này là dừng thật.

**Bẫy phải tránh:** đừng hỏi *"thông tin này có hữu ích không"* — ai cũng nói có. Hỏi *"nó đổi hành vi không"*.

### Cổng A9 (mới) — công ty có trả lời không?

Toàn bộ mô hình dựa vào việc hỏi được câu trả lời.

**Việc làm:** email 20 công ty đang đăng tin worldwide. Một câu hỏi, không bán gì:

> *"Chúng tôi đang lập danh sách công ty tuyển được ở Đông Nam Á cho cộng đồng kỹ sư Việt Nam. Nếu tuyển một người ở Việt Nam, bạn dùng cơ chế nào — EOR, hợp đồng nhà thầu, hay chưa làm được?"*

**Ngưỡng:** ≥ 5/20 trả lời trong 2 tuần → mô hình chạy được. ≤ 2/20 → nguồn cung thông tin không tồn tại, dừng.

**Vì sao có cửa:** câu hỏi này rẻ với họ (một dòng trả lời), và có lợi cho họ (được vào danh sách miễn phí). Khác hẳn email bán hàng.

## 6. Điều v3 KHÔNG sửa được

**Quy mô nguồn cung nhỏ.** 4% tin remote là worldwide. Bản tin tuần sẽ có 10–25 tin, không phải 100. Đó là trần, không phải khởi điểm.

**Mật độ VN vẫn là 0.** v3 không làm cho công ty tuyển VN nhiều hơn — nó chỉ làm rõ ai tuyển được. Nếu câu trả lời từ 20 công ty đều là "chưa làm được ở VN", thì v3 tạo ra thông tin thật nhưng thông tin đó là *"không có đường nào"*. Vẫn là sản phẩm — nhưng là sản phẩm khác hẳn, và cần hỏi lại có ai trả tiền cho nó không.

**Chi phí thời gian không giảm.** Hỏi–chờ–ghi là việc tay. Đòn bẩy 64:1 làm nó khả thi, không làm nó tự động.

## 6.5 Tiền lệ đã xác nhận khoảng trống — và cho sẵn danh sách mục tiêu

`remoteintech/remote-jobs` là danh bạ công ty remote-friendly do cộng đồng duy trì, có bot kiểm tra và quy trình PR. Schema đầy đủ của nó:

```yaml
title, slug, website, careers_url,
region:         worldwide | americas | europe | americas-europe | asia-pacific | other
remote_policy:  fully-remote | remote-first | hybrid | remote-friendly
company_size:   tiny | small | medium | large | enterprise
technologies:   [...]
```

**Không có trường nào cho: cơ chế tuyển dụng (EOR / nhà thầu / pháp nhân), quốc gia cụ thể, hay yêu cầu múi giờ.**

`yanirs/established-remote` (~100 công ty) cũng vậy — nó *loại* công ty chỉ tuyển ở vài nước giàu, nhưng **không ghi công ty nào tuyển được ở đâu**.

**Ba hệ quả:**

1. **Khoảng trống của v3 được xác nhận bởi tiền lệ trưởng thành nhất trong ngành.** Danh bạ cộng đồng lâu năm nhất dừng ở đúng ranh giới mà Nhóm 2 dừng: mức vùng, không có cơ chế. Không phải vì họ chưa nghĩ ra — vì **dữ liệu đó phải đi hỏi mới có**.

2. **`region: worldwide` là danh sách mục tiêu A9 làm sẵn.** Đã được cộng đồng lọc, có sẵn `careers_url`, có `slug` ổn định để nối dữ liệu.

3. **Tài sản của v3 không phải một DANH SÁCH — là một TRƯỜNG DỮ LIỆU.** Ba danh bạ đã tồn tại. Bốn board đã lọc. Thứ chưa ai có là cột `hiring_mechanism`.

> **Đừng xây danh bạ thứ tư. Thêm một cột vào danh bạ đã có.**

Cách làm: giữ bộ dữ liệu riêng, **nối bằng `slug` của remoteintech**, và đóng góp ngược lên khi đã đủ chín. Được cả bốn thứ cùng lúc: phân phối (khán giả của họ), uy tín cho email A9, tài sản GEO (dữ liệu gốc — BRD 16.1.1), và lối vào hard side (người đóng góp của họ).

## 6.6 Đã kéo danh sách — và đối chiếu nó lộ ra điều lớn hơn

`remoteintech/remote-jobs`: 882 công ty, **403 gắn nhãn `region: worldwide`** (320 trong đó `fully-remote`/`remote-first`). Đã xuất ra [a9-targets.csv](a9-targets.csv), xếp hạng theo: trùng pipeline ATS · có link ATS · chính sách remote · quy mô · stack.

**22 công ty trùng với pipeline ATS. 10 trong số đó có tin tôi đã chấm tay.** Đối chiếu nhãn của họ với thực tế trên tin:

| Nhãn `worldwide` của remoteintech | Tin thật |
|---|---|
| Khớp (có tin worldwide) | **1** công ty — Supabase |
| Hỗn hợp | 2 — Canonical, PostHog |
| **Mâu thuẫn hoàn toàn** | **7** — Close, DuckDuckGo, GitLab, Linear, Ramp, Replit, Twilio |

Ở mức tin: **4 khớp / 15 mâu thuẫn**. Ví dụ: GitLab `worldwide` nhưng tin ghi `Remote, United States`; Linear `worldwide` nhưng `North America`; Replit `worldwide` nhưng `Remote - United Kingdom`; Ramp `worldwide` nhưng `New York, NY (HQ)`.

### Mẫu hình xuất hiện ở BA nguồn độc lập

| Nguồn | Tuyên bố | Thực tế ở mức tin |
|---|---|---|
| `remoteintech` `region` | worldwide | 79% tin bị giới hạn địa lý |
| Real Work From Anywhere | "no location restrictions" | FAQ thừa nhận múi giờ/thuế khác nhau, tin không ghi |
| `applicantLocationRequirements` | khai quốc gia | chỉ 25% tin khai; `category-labs` khai `United States` nhưng mô tả nói có EOR ngoài Mỹ |

> **Càng xa tin tuyển dụng thật, tuyên bố càng "toàn cầu".**

Đây vừa là bằng chứng mạnh nhất cho v3 — **không ai có dữ liệu đúng ở mức quan trọng** — vừa là cảnh báo: `region: worldwide` là **danh sách đầu mối, không phải danh sách đã xác minh**. Nguồn cung worldwide thật là **4% đo trên tin**, không phải 403 công ty.

### Sửa câu hỏi A9 theo phát hiện này

Đừng hỏi *"công ty có tuyển worldwide không"* — họ sẽ trả lời theo bản mô tả của chính mình, và ta vừa đo được bản mô tả đó sai 79%.

**Neo vào một tin đang mở cụ thể:**

> *"Các bạn đang mở vị trí **[chức danh]** ở **[link tin]**. Nếu người phù hợp nhất đang ở Việt Nam, các bạn trả lương cho họ bằng cơ chế nào — EOR, hợp đồng nhà thầu, hay hiện chưa làm được?"*

Câu này khó trả lời sai. Nó hỏi về một tin thật, không hỏi về chính sách chung.

## 7. Việc tiếp theo, đúng thứ tự

| # | Việc | Chi phí | Cổng |
|---|---|---|---|
| 1 | **A8** — 10 cuộc trò chuyện | 1 buổi | ≤ 3/10 → dừng |
| 2 | **A9** — 20 email, lấy mục tiêu từ `remoteintech` lọc `region: worldwide` | 30 phút + 2 tuần chờ | ≤ 2/20 → dừng |
| 3 | Ghi 6 câu trả lời đầu vào bảng công ty | 0 | — |
| 4 | Bản tin số 1: 10–20 tin worldwide **có cột cơ chế** | 2 giờ | — |

**Không viết code cho tới khi qua bước 2.** Pipeline hiện có ([tools/](tools/)) đã đủ để lấy nguồn cung cho bước 4.

---

## Phụ lục — vì sao ghi lại toàn bộ đường đi

v1 → v2 → v3 là ba định vị khác nhau. Hai lần đổi đều do **số liệu, không do đổi ý**:

- **v1 → v2:** adversarial review tìm ra 21 lỗi nội tại, trong đó ví dụ định vị tự vi phạm ngưỡng dừng của chính nó
- **v2 → v3:** Cổng 0.1 đo được 0/150 — tiêu chí dừng viết ra *trước khi đo* đã kích hoạt đúng như thiết kế

Chi phí để biết cả hai điều: một buổi đọc tin. Nếu bỏ qua Cổng 0 và code trước, cùng bài học đó sẽ đến ở tháng thứ 6.

**Điều đáng giữ nhất từ v2 không phải nội dung, mà là thói quen viết ngưỡng dừng trước khi có dữ liệu.**
