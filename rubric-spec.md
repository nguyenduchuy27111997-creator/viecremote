# Rubric Spec v0.1 — Chấm nhãn "tin đủ điều kiện"

**Phiên bản:** 0.4 (DỰ THẢO — chưa hiệu chỉnh bằng dữ liệu thật)
**Ngày:** 17/08/2026
**Trạng thái:** Dùng làm dụng cụ đo cho Cổng 0.1. Nâng lên 1.0 sau khi điền Mục 11.
**Đi kèm:** [brd-v2.md](archive/brd-v2.md) Mục 2 · [next-steps.md](archive/next-steps.md)

---

## 1. Mục đích

Biến định nghĩa "tin đủ điều kiện" ở BRD Mục 2 thành **quy tắc kiểm được**, để:

1. Chấm tay 200 tin ở Cổng 0.1 **nhất quán** — không có tài liệu này, cùng một người chấm hai lần sẽ ra hai kết quả khác nhau, và ground truth bị nhiễu
2. Đo được "độ chính xác nhãn" trong North Star — nửa sau của cặp số ở BRD Mục 12.1
3. Chống nới rubric âm thầm — mọi thay đổi phải qua Mục 10

**Phạm vi:** chỉ chấm nhãn. Không bao gồm thu thập, khử trùng lặp, hiển thị.

---

## 2. Sáu nguyên tắc

| # | Nguyên tắc | Hệ quả |
|---|---|---|
| N1 | **Bằng chứng hoặc không có gì** | Mỗi quy tắc kích hoạt phải kèm trích dẫn nguyên văn. Không trích được → coi như không kích hoạt |
| N2 | **"Không rõ" là câu trả lời đúng** | Không phải thất bại. Ép ra Tier A/B khi thiếu bằng chứng là lỗi nặng nhất |
| N3 | **Không suy diễn** | "Công ty châu Âu nên chắc thoáng về múi giờ" — không phải bằng chứng |
| N4 | **Bằng chứng có tuổi** | Mọi bằng chứng mang ngày. Hết hạn thì hạ nhãn, không giữ nguyên |
| N5 | **Loại trừ thắng mọi thứ** | Một quy tắc DQ kích hoạt → "Không", bất kể có bao nhiêu bằng chứng dương |
| N6 | **Sai Tier A đắt hơn sai "Không rõ"** | Ngưỡng phát hành bất đối xứng (Mục 9.3). Sản phẩm bán niềm tin |

---

## 3. Đầu vào

### 3.1 Trường bắt buộc

| Trường | Nguồn | Bắt buộc |
|---|---|---|
| `job_id` | Sinh nội bộ | Có |
| `source` | `ashby` \| `greenhouse` \| `lever` \| `workable` \| `recruitee` \| `personio` \| `manual` | Có |
| `source_url` | URL tin gốc | Có |
| `company_name` | Feed | Có |
| `title` | Feed | Có |
| `description_raw` | Feed, giữ nguyên văn | Có |
| `location_raw` | Feed | Không |
| `compensation_raw` | Feed (Ashby có, đa số không) | Không |
| `first_seen_at`, `last_seen_at` | Sinh nội bộ | Có |

### 3.2 Nguồn phụ (tra khi cần, không bắt buộc)

- Trang tuyển dụng công ty (mục "where we hire" / "how we work")
- Trang About/Contact — tìm pháp nhân VN
- Bản ghi bằng chứng cộng đồng trong database nội bộ

**Quy tắc chi phí:** chỉ tra nguồn phụ khi tin **không bị DQ** và **chưa đạt Tier A** từ mô tả gốc. Tra hết mọi tin sẽ làm nổ ngân sách thời gian (xem R3 ở next-steps).

---

## 4. Quy tắc loại trừ — DQ

Kích hoạt bất kỳ quy tắc nào → `eligibility = "no"`. Dừng chấm.

| ID | Điều kiện | Ví dụ mẫu ngôn ngữ |
|---|---|---|
| **DQ-01** | Yêu cầu quyền làm việc tại một quốc gia cụ thể | "must be authorized to work in the US", "valid EU work permit required", "right to work in the UK" |
| **DQ-02** | Giới hạn địa lý cứng loại trừ VN | "US only", "EU residents only", "must reside in [nước/bang]", danh sách bang/tỉnh cụ thể |
| **DQ-03** | Hình thức lao động chỉ tồn tại ở một nước | "W-2 employment", "PAYE", "must be on local payroll in [nước]" |
| **DQ-04** | Yêu cầu security clearance hoặc quốc tịch | "US citizens only", "security clearance required" |
| **DQ-05** | Yêu cầu trùng múi giờ khiến overlap với GMT+7 < 2h (Mục 6) | "within 3 hours of PST", "core hours 9am–5pm EST" |
| **DQ-06** | Yêu cầu có mặt vật lý định kỳ ≥ 1 lần/tháng | "hybrid", "2 days in office", "must be commutable to [thành phố]" |
| **DQ-07** | Tin qua agency không tiết lộ công ty cuối | "our client, a leading fintech…" |
| **DQ-08** | Tin đã biến mất khỏi feed nguồn hoặc `validThrough` đã qua | — |
| **DQ-09** | Trường `applicantLocationRequirements` **có liệt kê quốc gia và Việt Nam không nằm trong đó** | vd `"United States"` · `"European Union; United States"` |

**Ghi chú DQ-09 — loại trừ có cấu trúc, chắc hơn mọi suy luận văn xuôi.** Chạy thử `tools/check_schema.py` trên mẫu nhỏ cho **5/6 trang có trường này**, và cả 5 đều liệt kê `United States` hoặc `European Union` — **không trang nào có Việt Nam**.

Nghĩa là `applicantLocationRequirements` là nguồn có cấu trúc cho **cả hai chiều**: A-01 khi có Việt Nam, DQ-09 khi liệt kê rõ mà không có. Cả hai đều **không cần LLM và không cần suy diễn** — chỉ tra cứu.

**Quan sát sơ bộ trên mẫu cân bằng, 80 tin (17/08/2026):** 20/80 tin (**25%**) có khai trường này. Trong 20 tin đó, **0 tin liệt kê Việt Nam** — `United States`(15), `USA`(3), `Canada`(2), `Switzerland`(2), `United Kingdom`(2), và lẻ tẻ `Cayman Islands`, `Slovakia`, `Spain`, `Czechia`, `Estonia`. Tức **1/4 mẫu loại trừ được bằng tra cứu, không cần LLM**.

*(Lần đo đầu trên mẫu lệch — 67% Greenhouse, thiên về công ty Mỹ quy mô lớn — cho 37%. Con số đó cao giả tạo: công ty lớn khai schema đầy đủ hơn startup. 25% trên mẫu cân bằng là số đáng tin hơn.)*

**Yêu cầu thi hành — chuẩn hoá tên quốc gia trước khi so khớp.** Giá trị trong thực tế không nhất quán: `United States` · `USA` · `US` cùng một nước; `Canada` · `CA` cũng vậy (và `CA` còn trùng mã bang California — phải xử theo ngữ cảnh). So khớp chuỗi thô sẽ sai. Dùng bảng ánh xạ về ISO 3166-1 alpha-2 (`tools/country.py`).

**Quy tắc phân giải bất đối xứng — phát hiện khi chạy thật:**

| Chiều | Điều kiện |
|---|---|
| **A-01** (dương) | Chỉ cần **thấy Việt Nam**. Không phụ thuộc các giá trị khác trong danh sách |
| **DQ-09** (âm) | Phải phân giải được **toàn bộ** giá trị. Thiếu một giá trị → `unknown`, **không** → `no` (nguyên tắc N2) |

Vì sao bất đối xứng: bản đầu tiên yêu cầu phân giải hết cho cả hai chiều, và **suýt bỏ sót bằng chứng A-01 thật**. Tin `colonist` khai `Serbia; Poland; Turkey; Vietnam; Russia; Malaysia; Romania; Any Location` — vì `Serbia`, `Russia`, `Any Location` chưa có trong bảng ánh xạ nên toàn dòng bị trả `unknown`, dù **`Vietnam` nằm ngay trong đó**.

N2 đã cứu khỏi kết luận sai, nhưng cũng che mất một tín hiệu dương. Sự có mặt của `Vietnam` là **văn bản tường minh**, không phải suy diễn — nó không cần các giá trị khác phân giải được. Tìm Việt Nam trước, rồi mới xét loại trừ.

**Giá trị mang nghĩa toàn cầu** (`Any Location`, `Worldwide`, `Anywhere`, `Global`…) → **không kích hoạt DQ-09**. Danh sách có giá trị toàn cầu là danh sách không loại trừ ai.

Cảnh báo phạm vi: 25% là quan sát về *một tín hiệu*, **không phải tỷ lệ cơ sở**. Số quyết định vẫn là % Tier A-VN và chỉ chấm tay mới ra. Nếu phủ cao, phần lớn công việc chấm nhãn chuyển từ tầng 3 (LLM) xuống tầng 1 (xác định) — đổi cả mô hình chi phí lẫn độ chính xác.

**Ghi chú DQ-06:** offsite/retreat theo quý hoặc theo năm **không** kích hoạt DQ-06. Đó là công tác, không phải nơi cư trú. Ghi vào trường `notes`, không loại.

**Ghi chú DQ-05:** chỉ kích hoạt khi tin **yêu cầu** (require/must). Nếu là **ưu tiên** (prefer/nice to have) thì không DQ — ghi vào `timezone` và để quy tắc B xử lý.

---

## 5. Quy tắc bằng chứng dương

### 5.1 Tier A — bằng chứng cứng

Kích hoạt **≥ 1 quy tắc** → `eligibility = "tier_a"`.

| ID | Điều kiện | Nguồn chấp nhận | Phạm vi |
|---|---|---|---|
| **A-01** | Việt Nam có tên trong danh sách quốc gia tuyển | Tin gốc · trang tuyển dụng · **hoặc trường `applicantLocationRequirements` trong JobPosting schema của chính công ty** | **VN** |
| **A-02** | Ngôn ngữ toàn cầu tuyệt đối, **và không có quy tắc DQ nào** | "work from anywhere", "anywhere in the world", "any country", "fully global, no restrictions" | Global |
| **A-03** | APAC / Southeast Asia / Asia được nêu là vùng chấp nhận | Tin gốc hoặc trang tuyển dụng | Global |
| **A-04** | Công ty có pháp nhân hoặc văn phòng tại VN | Trang About/Contact/LinkedIn công ty | **VN** |
| **A-05** | Bản ghi cộng đồng xác nhận người Việt được nhận, trong 18 tháng | Database nội bộ, có nguồn | **VN** |
| **A-06** | Trang tuyển dụng nêu rõ dùng EOR **và** liệt kê VN trong vùng phủ | Trang tuyển dụng | **VN** |

**Ghi chú A-01 — nguồn có cấu trúc, rẻ nhất và chắc nhất:** schema JobPosting của Google có trường **`applicantLocationRequirements`** — "the geographic location(s) in which employees may be located for work from home jobs", **bắt buộc ít nhất một quốc gia** khi được dùng. Công ty nào tự khai trường này thì A-01 đọc được **trực tiếp từ dữ liệu có cấu trúc**, không cần LLM đọc văn xuôi, không cần tra nguồn phụ.

Đây là tín hiệu Tier A-VN rẻ nhất trong toàn bộ rubric. **Đo tỷ lệ phủ của trường này ở Cổng 0.1** — nếu một phần đáng kể tin có nó, phần lớn bài toán chấm A-01 chuyển từ suy luận sang tra cứu, và cả mô hình chi phí lẫn độ chính xác đều tốt lên.

**Ghi chú A-02:** "remote" đơn thuần **không** kích hoạt A-02. "Remote (US)" cũng không. Phải là ngôn ngữ toàn cầu tuyệt đối và không kèm bất kỳ giới hạn nào.

#### Cột "Phạm vi" — tách Tier A làm hai

Trường `tier_a_scope` sinh tự động từ tập quy tắc đã kích hoạt:

| Giá trị | Điều kiện | Ý nghĩa |
|---|---|---|
| `vn_specific` | Có ≥ 1 quy tắc phạm vi **VN** (A-01/A-04/A-05/A-06) | Bằng chứng riêng cho Việt Nam. **Chỉ giá trị này tính vào North Star** |
| `global_only` | Chỉ có A-02 và/hoặc A-03 | Ngôn ngữ toàn cầu chung chung |

**Vì sao tách:** BRD Mục 5.1 — tin mà bằng chứng duy nhất là "work from anywhere" đã được ít nhất bốn board tuyển chọn tay xuất bản miễn phí hằng tuần (Real Work From Anywhere, TrulyRemoteWork, Truly Remote, We Are Distributed). Đếm chúng như thành tích là tự chấm điểm cho việc đăng lại nội dung có sẵn.

`global_only` **vẫn xuất bản** — có ích cho người đọc. Nhưng nó không phải bằng chứng sản phẩm đang tạo ra thứ chưa tồn tại.

**Ghi chú A-06 — giới hạn tự động hoá:** không nhà cung cấp EOR nào công bố endpoint trả về "những nước nào có EOR". Deel có cổng developer công khai (`developer.deel.com`), sandbox và webhook — nhà cung cấp duy nhất coi API là sản phẩm — nhưng đó là API vận hành nhân sự, không phải danh mục vùng phủ. Nghĩa là **A-06 phải lấy từ câu chữ trên trang tuyển dụng của công ty, hoặc từ danh sách duy trì tay.** Đây là tín hiệu mạnh nhất trong rubric và cũng là tín hiệu khó tự động nhất. Đưa vào ước lượng chi phí thời gian ở Cổng 0.1.

### 5.2 Tier B — bằng chứng mềm

Kích hoạt **≥ 2 quy tắc** → `eligibility = "tier_b"`.
Kích hoạt **đúng 1 quy tắc** → `eligibility = "unknown"`, cờ `leaning_positive = true`.

| ID | Điều kiện | Ví dụ mẫu ngôn ngữ |
|---|---|---|
| **B-01** | Ngôn ngữ chấp nhận nhà thầu toàn cầu | "contractor welcome", "we hire globally as contractors", "B2B contract" |
| **B-02** | Có nhân sự công khai ở GMT+5..GMT+9 | Team page, LinkedIn |
| **B-03** | Văn hoá async rõ ràng | "async-first", "fully distributed across N timezones", "no core hours" |
| **B-04** | Công ty dùng nền tảng EOR có hỗ trợ VN, nhưng không xác nhận VN cụ thể | URL nộp hồ sơ, trang tuyển dụng |
| **B-05** | Ưu tiên (không yêu cầu) múi giờ mà GMT+7 trùng được ≥ 4h | "European timezone preferred" |

**Vì sao cần 2 quy tắc thay vì 1:** Tier B được tính vào North Star (BRD Mục 2.2). Một tín hiệu mềm đơn lẻ có tỷ lệ dương tính giả cao — "async-first" phổ biến ở cả công ty chỉ tuyển ở Mỹ. Đây là **siết chặt so với BRD v2.0**; ghi vào changelog.

### 5.3 Không rõ

Không có DQ, không đủ A, không đủ B → `eligibility = "unknown"`.

**Đây là nhãn hợp lệ và phải hiển thị.** Tỷ lệ "Không rõ" là chỉ số Tier 0 (R2) — nếu > 60% thì mô hình chi phí sai hoàn toàn.

### 5.4 Thứ tự đánh giá

```
1. Chạy toàn bộ DQ-01..DQ-08
   → có hit ⇒ "no", DỪNG
2. Chạy toàn bộ A-01..A-06
   → có hit ⇒ "tier_a", ghi mọi quy tắc hit, DỪNG
3. Chạy toàn bộ B-01..B-05
   → ≥2 hit ⇒ "tier_b"
   → 1 hit  ⇒ "unknown" + leaning_positive
   → 0 hit  ⇒ "unknown"
```

---

## 6. Nhãn múi giờ

**Neo tính toán:** GMT+7. Giờ hành chính hai bên: 09:00–18:00.

Overlap tính theo giờ hành chính chồng nhau, không tính giờ đêm.

| Múi neo | Lệch với GMT+7 | Overlap giờ hành chính | Kết luận |
|---|---|---|---|
| GMT+1 (CET) | −6h | 09:00–12:00 CET = 15:00–18:00 VN → **3h** | Khả thi |
| GMT+2 (EET/CEST) | −5h | **4h** | Khả thi, tốt nhất trong nhóm châu Âu |
| GMT+0 (UK) | −7h | **2h** | Sát ngưỡng |
| GMT−5 (ET) | −12h | **0h** | DQ-05 |
| GMT−8 (PT) | −15h | **0h** | DQ-05 |
| GMT+8..+11 | +1..+4h | **5–8h** | Dễ nhất, nhưng khối lượng tin ít hơn |

Đầu ra:

```json
"timezone": {
  "requirement_type": "required" | "preferred" | "none",
  "anchor_tz": "CET",
  "required_overlap_hours": 4,
  "computed_overlap_with_gmt7": 4,
  "source_quote": "…"
}
```

---

## 7. Nhãn cơ chế hợp đồng và công bố lương

### 7.1 Cơ chế hợp đồng

| ID | Giá trị | Điều kiện |
|---|---|---|
| C-01 | `eor` | Nêu tên nền tảng EOR hoặc cụm "employer of record" |
| C-02 | `contractor` | "contractor", "B2B", "invoice", "freelance agreement" |
| C-03 | `local_entity` | Công ty có pháp nhân VN (kéo từ A-04) |
| C-04 | `agency` | Qua agency (thường đã bị DQ-07) |
| C-05 | `unknown` | Mặc định |

**Bẫy:** `1099` là biểu mẫu thuế Mỹ, ngụ ý người nộp thuế Mỹ. **Không** dùng "1099" làm bằng chứng cho C-02. Nếu chỉ có "1099" → thường là tín hiệu DQ-02, không phải tín hiệu contractor toàn cầu.

### 7.2 Công bố lương

| Giá trị | Điều kiện |
|---|---|
| `range` | Có dải số + đơn vị tiền + chu kỳ |
| `single_figure` | Một con số duy nhất |
| `none` | Không có gì, hoặc chỉ "competitive" |

---

## 8. Định dạng bằng chứng

Mỗi quy tắc kích hoạt sinh đúng một bản ghi bằng chứng:

```json
{
  "rule_id": "A-02",
  "quote": "This role is open to candidates anywhere in the world.",
  "source_type": "job_description",
  "source_url": "https://jobs.ashbyhq.com/acme/abc-123",
  "observed_at": "2026-08-17"
}
```

**Ràng buộc:**
- `quote` là **nguyên văn**, ≤ 200 ký tự, phải khớp chuỗi con của văn bản nguồn. Test tự động kiểm điều này.
- Không trích được nguyên văn → quy tắc **không** được kích hoạt (N1)
- `source_type` ∈ `job_description` | `careers_page` | `company_site` | `community_record`

> **Cảnh báo thi hành:** giới hạn 200 ký tự **không đặt được trong JSON Schema** của structured outputs — `maxLength` (và mọi ràng buộc độ dài chuỗi / giới hạn số) không được hỗ trợ. Phải kiểm ở tầng ứng dụng cùng với INV-6. Xem Mục 14.2.

### 8.1 Hết hạn bằng chứng

| Loại | Hạn | Khi hết hạn |
|---|---|---|
| A-05 (bản ghi cộng đồng) | 18 tháng | Bỏ khỏi tính toán, đánh dấu `needs_reconfirmation` |
| A-04 / C-03 (pháp nhân) | 12 tháng | Tra lại |
| A-01, A-03, A-06 (trang tuyển dụng) | 6 tháng | Tra lại |
| A-02, B-xx (mô tả tin) | Theo tuổi tin | Tin không còn trong feed → DQ-08 |

Tin `last_seen_at` cũ hơn 45 ngày → tự động chuyển `needs_reconfirmation`, **không tính vào North Star**.

---

## 9. Bộ test và cách đo độ chính xác

### 9.1 Ground truth

50 tin lấy ngẫu nhiên từ 200 tin của Cổng 0.1. Chấm tay theo spec này.

**Bắt buộc: chấm hai lượt, cách nhau ≥ 3 ngày, không xem kết quả lượt trước.**

Đo **độ nhất quán nội bộ** = % tin có nhãn giống nhau giữa hai lượt.

| Nhất quán nội bộ | Ý nghĩa |
|---|---|
| ≥ 90% | Rubric đủ rõ. Dùng làm ground truth |
| 80–90% | Rà lại các quy tắc gây bất đồng, làm rõ, chấm lại |
| < 80% | **Rubric mơ hồ. Sửa rubric trước, tuyệt đối không test model** |

Bỏ qua bước này là lỗi phổ biến nhất: đo model bằng thước dây co giãn thì con số không có nghĩa gì.

### 9.2 Chỉ số

| Chỉ số | Công thức | Vì sao |
|---|---|---|
| **Tier A precision** | Đúng Tier A / Tổng model gán Tier A | **Quan trọng nhất.** Dương tính giả = người dùng nộp vào chỗ vô vọng = mất niềm tin |
| Tier A recall | Đúng Tier A / Tổng Tier A thật | Bỏ sót = mất tin tốt. Tệ, nhưng người dùng không thấy |
| **DQ recall** | DQ bắt được / Tổng DQ thật | Lọt tin rác vào danh sách phá hỏng định vị |
| Accuracy tổng | Nhãn khớp / 50 | Chỉ số nền |
| Tỷ lệ "Không rõ" | Unknown / 50 | R2 — chỉ số sinh tử của mô hình chi phí |

### 9.3 Ngưỡng phát hành

Cả ba phải đạt:

- **Tier A precision ≥ 90%**
- **DQ recall ≥ 95%**
- **Accuracy tổng ≥ 85%**

Bất đối xứng có chủ ý (N6). Không đạt → **sửa rubric, không sửa model.** Nếu model không áp dụng được quy tắc, gần như luôn là do quy tắc mơ hồ.

---

## 9.4 Kết quả đo thật lần đầu (17/08/2026) — tầng quy tắc TRƯỢT cả ba ngưỡng

Chạy `tools/score_rules.py` (tầng xác định: DQ-01..07 regex + A-02/A-03 + B) trên 200 tin thật, rồi **đọc tay 30 tin** phân tầng theo nhãn máy (10 `no` / 10 `A` / 10 `unknown`).

| Chỉ số | Đo được | Ngưỡng | |
|---|---|---|---|
| **Tier A precision** | **30%** | ≥ 90% | ✗ trượt nặng |
| **DQ recall** | **39%** | ≥ 95% | ✗ trượt nặng |
| Accuracy tổng | 47% | ≥ 85% | ✗ |

Ma trận (máy \ tay): trong 10 tin máy gán Tier A, **7 sai** — 6 thực ra bị loại trừ, 1 là `unknown`.

### Năm nguyên nhân gốc — đều là lỗi quy tắc, không phải lỗi model

**1. Quy tắc dương chạy trên văn xuôi mà bỏ qua trường `location` có cấu trúc.** Đây là nguyên nhân lớn nhất. Phần lớn tin bị bỏ sót có đáp án nằm sẵn trong `location`: `Remote - USA` · `Remote within Canada` · `India` · `Dallas, TX - US (Remote)` · `Remote - The Netherlands`.
→ **Sửa: `location` phải được xét như DQ TRƯỚC mọi quy tắc văn xuôi.** Một trường có cấu trúc luôn thắng một câu văn.

**2. A-02 khớp vào văn quảng cáo, không phải phạm vi tuyển.** `"improve patient outcomes worldwide"` · `"thrive from any location"` (văn hoá công ty) · `"Asia-Pacific"` trong đoạn giới thiệu công ty (khớp A-03).
→ **Sửa: A-02/A-03 chỉ tính khi cụm từ đứng trong ngữ cảnh điều kiện tuyển dụng** (gần "hire", "role is open to", "eligible", "we hire"), không tính khi nằm trong câu sứ mệnh.

**3. A-02 bỏ qua mệnh đề giới hạn ngay sau nó.** `"work from anywhere within NI"` khớp `work from anywhere` rồi dừng — bỏ mất `within NI`.
→ **Sửa: sau khi khớp, phải soi tiếp 40 ký tự tìm `within|in|across` + địa danh. Có thì huỷ A-02 và chuyển thành DQ-02.**

**4. DQ bỏ qua tín hiệu nằm trong tiêu đề.** `"Learning and Support Specialist (PST Timezone)"` — yêu cầu múi giờ nằm ở tiêu đề, DQ-05 chỉ quét mô tả.
→ **Sửa: quét DQ trên `title` + `location` + `description`, không chỉ mô tả.**

**5. Tiền nghiệm theo ngành.** Nhà thầu quốc phòng (Shield AI) gần như chắc chắn yêu cầu clearance/quốc tịch kể cả khi tin không ghi. DQ-04 kích hoạt ở một tin của họ nhưng không ở tin khác.
→ **Sửa: cờ theo công ty, không theo từng tin.** Một công ty đã DQ-04 một lần thì mọi tin của họ mang cờ đó cho tới khi có bằng chứng ngược.

### Vì sao kết quả này có giá trị chứ không phải thất bại

Nó chứng minh đúng điều Mục 9.3 đặt ra: **không đạt ngưỡng thì sửa rubric, không đổi model.** Cả năm nguyên nhân đều là lỗi thiết kế quy tắc — thứ tự đánh giá, ưu tiên trường, phạm vi quét. Không cái nào cần model thông minh hơn.

Và nó chứng minh vì sao Cổng 0.1 **phải làm tay**. Nếu tin tầng quy tắc mà bỏ qua bước đối chứng, sản phẩm sẽ xuất bản danh sách "đủ điều kiện" mà **7/10 sai** — phá huỷ đúng thứ duy nhất nó bán.

### Sau khi sửa năm lỗi (cùng ngày)

| Chỉ số | Trước | Sau | Ngưỡng |
|---|---|---|---|
| Tier A precision | 30% | **100%** | ≥ 90% ✓ |
| DQ recall | 39% | **100%** | ≥ 95% ✓ |
| Accuracy tổng | 47% | **100%** | ≥ 85% ✓ |

Bản sửa nằm ở `tools/score_rules.py` v2. Thay đổi lớn nhất: **thêm tầng 0 — phân tích trường `location` (và đuôi `title`) như DQ trước mọi quy tắc văn xuôi.**

### ⚠️ 100% này CHƯA phải bằng chứng — mới là kết quả trên tập đã dùng để tinh chỉnh

Ba mươi tin này vừa là tập đối chứng, vừa là tập tôi dò lỗi và sửa quy tắc dựa trên nó. **Đo lại trên chính nó thì con số bị thổi phồng có hệ thống.** Đây là overfitting theo đúng nghĩa.

**Điều kiện để tin con số:** chấm tay một **mẫu mới, ngẫu nhiên** (không phân tầng theo nhãn máy), chưa từng dùng để sửa quy tắc, rồi đo lại. Chỉ khi đó ngưỡng phát hành ở Mục 9.3 mới có ý nghĩa.

### Bài học phương pháp: chấm tay từ đoạn trích là không đủ

Trong 30 nhãn tay ban đầu, **một nhãn sai** — tin `codeorg` bị chấm `unknown` trong khi mô tả có câu *"candidates must: Be a U.S. Citizen or Permanent Resident. Work within the continental United States"*. Người chấm không thấy câu đó vì chấm từ đoạn trích rút gọn, không đọc toàn văn.

Máy đúng, người sai. Nếu không soi từng bất đồng thì lỗi này sẽ đi thẳng vào ground truth và làm hỏng mọi phép đo sau.

**Hệ quả bắt buộc cho quy trình:** chấm tay phải đọc **toàn văn mô tả**, không đọc đoạn trích. Và mọi bất đồng máy-người phải được soi lại thủ công — vì bên sai có thể là người.

Điều này cũng là lý do Mục 9.1 yêu cầu chấm hai lượt cách nhau ≥ 3 ngày và đo độ nhất quán nội bộ trước khi dùng làm ground truth. Bước đó chưa chạy.

### Lô 2 — mẫu ngẫu nhiên MỚI (xác nhận độc lập)

30 tin ngẫu nhiên, không phân tầng, chưa từng dùng để sửa quy tắc. Chấm tay từ **toàn văn**.

| Chỉ số | Lô 1 (tập tinh chỉnh) | **Lô 2 (mẫu mới)** | Ngưỡng |
|---|---|---|---|
| Accuracy tổng | 100% | **90%** | ≥ 85% ✓ |
| DQ recall | 100% | **96%** | ≥ 95% ✓ |
| Tier A precision | 100% | **0/0 — vô nghĩa** | ≥ 90% |
| **Tier A recall** | 100% | **0%** | — |

**Kết luận thật, và nó xấu theo cách khác lần trước:** bản sửa đã đẩy quy tắc sang **quá bảo thủ**. Trên 30 tin ngẫu nhiên nó **không gán Tier A cho tin nào** — precision "100%" chỉ là mẫu số bằng 0. Một pipeline không bao giờ nói "đủ điều kiện" thì không có sản phẩm.

Chênh 100% → 90% giữa hai lô cũng chính là **mức thổi phồng do overfitting**, đo được.

### Ba lỗi còn lại, ba nguyên nhân khác nhau

**1. `metabase` — `location='Global Remote'`, máy trả `unknown`, đúng phải là Tier A-Global.**
Bản sửa trước đưa `location` vào tầng DQ nhưng **chỉ chiều âm**. Trường có cấu trúc phải dùng cho **cả hai chiều** — `Global Remote`, `Any Location`, `Worldwide` trong `location` là bằng chứng A-02 mạnh hơn mọi câu văn.

**2. `mapbox` — `location='Mapbox Germany'`, máy trả `unknown`, đúng phải là loại trừ.**
Tra quốc gia đang so khớp **toàn phần** nên `mapbox germany` không khớp `germany`. Cần dò **chuỗi con** theo ranh giới từ.

**3. `category-labs` — lỗi THIẾT KẾ rubric, không phải lỗi code.**
`applicantLocationRequirements = "United States"` → DQ-09 loại trừ. Nhưng mô tả ghi rõ: *"Benefits for employees hired through an **EOR (outside of the US)**"*. Công ty **có** tuyển ngoài Mỹ; trường schema chỉ phản ánh nơi tin được nhắm tới, không phải toàn bộ chính sách tuyển dụng.

Nguyên tắc N5 ("loại trừ thắng mọi thứ") khiến DQ-09 không thể kháng, và sinh ra âm tính giả.

> **Sửa N5 cho riêng DQ-09:** DQ-09 là **tín hiệu mạnh nhưng có thể bị bác** bởi bằng chứng văn xuôi tường minh ngược lại (nêu EOR/tuyển ngoài nước được liệt kê, hoặc ngôn ngữ toàn cầu trong ngữ cảnh tuyển dụng). Bị bác → hạ xuống `unknown`, **không** nâng thẳng lên Tier A.
> Các DQ-01..08 vẫn giữ nguyên N5 — chúng là câu chữ do chính công ty viết về điều kiện, còn DQ-09 là suy ra từ một trường có thể khai thiếu.

### Tín hiệu tỷ lệ cơ sở đầu tiên dùng được

Lô 2 là mẫu **ngẫu nhiên thật**, nên đọc được như tỷ lệ cơ sở sơ bộ:

| | n=30 |
|---|---|
| Loại trừ | 24 (80%) |
| Không rõ | 5 (17%) |
| Tier A-Global | 1 (3,3%) |
| **Tier A-VN** | **0 (0%)** |

n=30 là quá nhỏ để kết luận — cận trên khoảng tin cậy 95% cho 0/30 vào khoảng 11%, nên chưa loại trừ được ngưỡng 2% ở BRD Mục 3. Nhưng đây là **số liệu ngẫu nhiên đầu tiên**, và nó **không thuận chiều**. Phải chấm đủ mẫu lớn hơn trước khi kết luận.

### Cảnh báo diễn giải

Ba mươi tin này **lấy phân tầng theo nhãn máy** (10/10/10), **không phải mẫu ngẫu nhiên**. Tỷ lệ Tier A-VN tính từ đây (1/30) **không phải tỷ lệ cơ sở** — mẫu đã bơm nhóm máy-gán-A lên quá tỷ trọng thật. Tỷ lệ cơ sở chỉ ra từ mẫu ngẫu nhiên chấm tay đầy đủ.

---

## 10. Phiên bản và thay đổi

Theo BRD Mục 2.3, mọi thay đổi rubric phải:

1. Tăng phiên bản (`MAJOR.MINOR`) — MAJOR khi đổi ngưỡng hoặc thêm/bớt quy tắc; MINOR khi làm rõ câu chữ
2. Ghi changelog có ngày và lý do
3. **Chạy lại trên 100 tin của tháng trước, báo cáo chênh lệch nhãn**
4. **Không thay đổi trong tháng đang đo**

### Changelog

| Phiên bản | Ngày | Thay đổi |
|---|---|---|
| 0.1 | 17/08/2026 | Bản đầu. Siết Tier B từ "≥1 tín hiệu" (BRD v2.0) lên "≥2 tín hiệu"; thêm bậc `leaning_positive`. Lý do: tín hiệu mềm đơn lẻ có tỷ lệ dương tính giả cao |
| 0.2 | 17/08/2026 | Thêm Mục 14 (thi hành: chọn model, structured outputs, prompt caching, Batch API). Sửa hai lỗi kỹ thuật ở 0.1: (a) `temperature: 0` **bị từ chối 400** trên Opus 5 / Sonnet 5 — chỉ hợp lệ trên Haiku 4.5; (b) giới hạn `maxLength` 200 ký tự **không đặt được trong JSON Schema** — phải kiểm ở tầng ứng dụng. Không đổi quy tắc chấm |
| 0.4 | 17/08/2026 | Thêm **DQ-09**: `applicantLocationRequirements` liệt kê quốc gia mà không có Việt Nam = loại trừ có cấu trúc. Phát hiện khi chạy thử `tools/check_schema.py`. Cùng trường này đã là nguồn cho A-01 (chiều dương) — giờ dùng cả chiều âm |
| 0.3 | 17/08/2026 | **Tách Tier A làm hai phạm vi** — `vn_specific` (A-01/A-04/A-05/A-06) và `global_only` (A-02/A-03). Thêm trường `tier_a_scope`, INV-8, INV-9. Lý do: bằng chứng "worldwide" chung chung đã có sẵn miễn phí trên ≥ 4 board tuyển chọn tay (BRD Mục 5.1) — đếm nó vào North Star là tự chấm điểm cho việc đăng lại. **Quy tắc chấm không đổi**, chỉ thêm một chiều phân loại trên kết quả. Thêm ghi chú A-06: vùng phủ EOR không lấy tự động được |

---

## 11. Chỗ trống — điền sau Cổng 0.1

Bốn phần chỉ dữ liệu thật mới điền được. **Rubric chưa lên 1.0 khi bốn phần này còn trống.**

| # | Cần điền | Lấy từ |
|---|---|---|
| **T1** | 3 ví dụ dương + 3 ví dụ âm cho **mỗi** quy tắc DQ/A/B | 200 tin của Cổng 0.1 |
| **T2** | Tần suất kích hoạt của mỗi quy tắc | Đếm trên 200 tin. **Quy tắc không bao giờ kích hoạt thì xoá** — mỗi quy tắc thừa làm tăng chi phí token và tăng nhiễu |
| **T3** | Hiệu chỉnh DQ-05: ngưỡng 2h có đúng không | Xem các tin biên trong 200 tin |
| **T4** | Hiệu chỉnh 5.2: "≥2 tín hiệu B" có đúng không | So Tier B chấm tay với kết quả thực tế nếu theo dõi được |

---

## 12. Lược đồ đầu ra

```json
{
  "job_id": "string",
  "rubric_version": "0.1",
  "scored_at": "2026-08-17T10:00:00Z",

  "eligibility": "tier_a | tier_b | unknown | no",
  "tier_a_scope": "vn_specific | global_only | null",
  "leaning_positive": false,
  "needs_reconfirmation": false,

  "contract_mechanism": "eor | contractor | local_entity | agency | unknown",

  "timezone": {
    "requirement_type": "required | preferred | none",
    "anchor_tz": "string | null",
    "required_overlap_hours": 0,
    "computed_overlap_with_gmt7": 0,
    "source_quote": "string | null"
  },

  "pay_disclosure": "range | single_figure | none",

  "rules_fired": ["A-02", "B-03"],
  "evidence": [
    {
      "rule_id": "A-02",
      "quote": "string (≤200 ký tự, nguyên văn)",
      "source_type": "job_description",
      "source_url": "string",
      "observed_at": "2026-08-17"
    }
  ],

  "notes": "string | null"
}
```

### 12.1 Bất biến — kiểm bằng test tự động

| ID | Bất biến |
|---|---|
| INV-1 | `eligibility == "tier_a"` ⟹ `rules_fired` chứa ≥ 1 mã `A-*` |
| INV-2 | `eligibility == "tier_b"` ⟹ `rules_fired` chứa ≥ 2 mã `B-*` |
| INV-3 | `eligibility == "no"` ⟹ `rules_fired` chứa ≥ 1 mã `DQ-*` |
| INV-4 | `rules_fired` chứa mã `DQ-*` ⟹ `eligibility == "no"` (N5) |
| INV-5 | Mọi mã trong `rules_fired` có đúng một bản ghi trong `evidence` |
| INV-6 | Mọi `quote` là chuỗi con nguyên văn của văn bản nguồn |
| INV-7 | `needs_reconfirmation == true` ⟹ không tính vào North Star |
| INV-8 | `tier_a_scope` **không null khi và chỉ khi** `eligibility == "tier_a"`. `vn_specific` ⟺ `rules_fired` chứa ≥ 1 trong {A-01, A-04, A-05, A-06}; ngược lại `global_only` |
| INV-9 | Chỉ `tier_a_scope == "vn_specific"` được tính vào North Star (BRD Mục 12.1) |

INV-6 là bất biến quan trọng nhất — nó chặn model bịa trích dẫn. Vi phạm INV-6 → loại kết quả, chấm lại.

---

## 13. Prompt chấm (LLM)

```
Bạn chấm nhãn một tin tuyển dụng theo Rubric Spec v0.1.

NGUYÊN TẮC BẮT BUỘC
1. Chỉ kích hoạt một quy tắc khi trích được NGUYÊN VĂN từ văn bản dưới đây.
   Không trích được → không kích hoạt quy tắc đó.
2. "unknown" là câu trả lời ĐÚNG khi thiếu bằng chứng. Không đoán.
3. Không suy diễn từ quốc tịch công ty, ngành, hay quy mô.
4. Bất kỳ quy tắc DQ nào kích hoạt → eligibility = "no", bỏ qua mọi bằng chứng dương.
5. Mọi quote phải khớp chính xác chuỗi con của văn bản gốc. Không diễn đạt lại.

THỨ TỰ ĐÁNH GIÁ
1) DQ-01..DQ-08 → có hit thì trả "no" và dừng
2) A-01..A-06   → có hit thì trả "tier_a" và dừng
3) B-01..B-05   → ≥2 hit: "tier_b" | 1 hit: "unknown" + leaning_positive | 0: "unknown"

<danh sách quy tắc — dán từ Mục 4, 5, 7>

VĂN BẢN TIN
company: {company_name}
title: {title}
location: {location_raw}
description:
{description_raw}

Trả về DUY NHẤT một JSON theo lược đồ Mục 12. Không giải thích.
```

**Ghi chú vận hành:**
- Không đưa tên công ty vào phần suy luận về Tier — model biết công ty nổi tiếng sẽ đoán. Chỉ dùng tên để tra nguồn phụ ở bước riêng
- Tra nguồn phụ (A-01, A-04, A-06, B-02, B-04) là **lượt gọi thứ hai**, chỉ chạy khi lượt một trả `unknown` và không có DQ
- **Không đặt `temperature`.** Xem Mục 14.3 — tham số này bị từ chối trên các model hiện hành

---

## 14. Thi hành kỹ thuật

Mục này ghi các ràng buộc của API chấm nhãn. Sai một trong số này thì hoặc lỗi 400, hoặc **hỏng âm thầm** (không cache, không cắt được chuỗi) — loại thứ hai nguy hiểm hơn.

### 14.1 Chọn model — quyết bằng độ chính xác, không bằng giá

Ở khối lượng của dự án này (BRD Mục 11.1: ~400 tin/tuần vào LLM sau lọc thô), **chi phí không phải yếu tố quyết định.** Giả định mỗi tin: ~5.000 token prompt rubric (đã cache, đọc ở 0,1x) + ~1.500 token mô tả tin + ~400 token JSON đầu ra.

| Model | Vào $/MTok | Ra $/MTok | ~$/tin | ~1.720 tin/tháng | Kèm Batch API (−50%) |
|---|---|---|---|---|---|
| `claude-haiku-4-5` | 1 | 5 | 0,004 | ~7 USD | **~3,5 USD** |
| `claude-sonnet-5` | 3 *(2 khuyến mại đến 31/08/2026)* | 15 *(10)* | 0,012 | ~21 USD | **~10 USD** |
| `claude-opus-5` | 5 | 25 | 0,020 | ~34 USD | **~17 USD** |

**Kết luận: chênh lệch giữa model rẻ nhất và mạnh nhất là ~14 USD/tháng.** So với trần chi phí 300 USD/tháng (PRD NFR-2), chọn model theo giá là tối ưu sai chỗ. **Chọn theo Tier A precision đo trên 50 tin ground truth (Mục 9).**

**Quy trình chọn (chạy ở bước 1 của lộ trình thi công):**
1. Chạy cả ba model trên cùng 50 tin ground truth, cùng prompt
2. Ghi Tier A precision, DQ recall, accuracy tổng cho từng model
3. Chọn model rẻ nhất **đạt cả ba ngưỡng phát hành** (Mục 9.3)
4. Không model nào đạt → **sửa rubric, không đổi model** (Mục 9.3)

Nếu chỉ model mạnh nhất đạt ngưỡng, dùng nó — 17 USD/tháng không phải lý do để hạ chất lượng nhãn khi nhãn chính là sản phẩm.

**Lượt gọi thứ hai (tra nguồn phụ, ≤20% tin)** là bài toán khó hơn: phải đọc trang tuyển dụng dài, ít cấu trúc. Cân nhắc dùng model mạnh hơn cho riêng lượt này, đo riêng.

**Chi phí một lần cho lần chạy đầu:** 3.000–8.000 tin qua LLM (sau lọc remote + lọc DQ). Khoảng 12–160 USD tuỳ model, giảm một nửa nếu chạy qua Batch API. Đây là khoản lớn nhất trong toàn bộ ngân sách LLM, và nó chỉ trả một lần.

### 14.2 Structured outputs — giới hạn của JSON Schema

Dùng `output_config.format` với `type: "json_schema"`. **Không dùng `output_format`** — tham số đó đã ngừng dùng.

Ràng buộc schema phải biết:

| Được hỗ trợ | **Không** hỗ trợ |
|---|---|
| `enum`, `const`, `anyOf`, `$ref` | Schema đệ quy |
| `additionalProperties: false` (**bắt buộc** cho mọi object) | `minLength` / `maxLength` |
| `required` | `minimum` / `maximum` / `multipleOf` |
| Định dạng chuỗi: `date`, `date-time`, `uri`, `uuid` | Ràng buộc mảng phức tạp |

**Hệ quả trực tiếp lên spec này:**

| Ràng buộc trong spec | Đặt được trong schema? | Thi hành ở đâu |
|---|---|---|
| `eligibility` ∈ 4 giá trị | Có — `enum` | Schema |
| `contract_mechanism` ∈ 5 giá trị | Có — `enum` | Schema |
| `observed_at` là ngày | Có — `format: "date"` | Schema |
| **`quote` ≤ 200 ký tự** | **Không** | Tầng ứng dụng |
| **INV-1..INV-7** (Mục 12.1) | **Không** | Tầng ứng dụng |
| **INV-6** (trích dẫn nguyên văn) | **Không** | Tầng ứng dụng |

Nghĩa là **schema không thay thế được bộ kiểm bất biến** — nó chỉ đảm bảo hình dạng JSON hợp lệ. Mọi ràng buộc về nội dung vẫn phải kiểm bằng code sau khi nhận kết quả.

**Ghi chú độ trễ:** schema mới phải biên dịch một lần ở lượt gọi đầu; sau đó cache 24 giờ. Đổi schema (kể cả đổi một dòng mô tả) khởi động lại chu kỳ đó.

**Cũng phải xử lý:** `stop_reason: "refusal"` — kiểm **trước khi** đọc nội dung phản hồi. Tin tuyển dụng bình thường hiếm khi kích hoạt, nhưng code đọc thẳng phần tử đầu của `content` sẽ vỡ khi xảy ra.

### 14.3 Không đặt `temperature`

`temperature`, `top_p`, `top_k` **bị từ chối với lỗi 400** trên Opus 5, Sonnet 5, Opus 4.7/4.8. Chúng chỉ còn hợp lệ trên các model cũ hơn như Haiku 4.5.

Phiên bản 0.1 của spec này ghi "chạy ở temperature 0" — **sai** với hai trong ba model ứng viên. Bỏ hoàn toàn tham số này. Tính xác định đến từ structured outputs + prompt cố định + effort thấp, không từ `temperature`.

Trên Opus 5: đặt `output_config: {effort: "low"}`. Không tắt thinking bằng `thinking: {type: "disabled"}` cho tác vụ này — thinking đang bật mặc định và tắt nó có thể khiến model rò thẻ `<thinking>` vào phần văn bản. Hạ `effort` là đòn bẩy đúng.

### 14.4 Prompt caching — ngưỡng khác nhau theo model

Prompt rubric (toàn bộ quy tắc Mục 4, 5, 7 + ví dụ T1) là tiền tố ổn định, giống nhau ở mọi lượt gọi. Đặt `cache_control` ở cuối khối đó: đọc từ cache tốn ~0,1x, ghi tốn 1,25x (TTL 5 phút).

**Ngưỡng tối thiểu để cache được, khác nhau theo model:**

| Model | Tiền tố tối thiểu |
|---|---|
| `claude-opus-5` | 512 token |
| `claude-sonnet-5` | 1.024 token |
| `claude-haiku-4-5` | **4.096 token** |

**Đây là cái bẫy âm thầm:** prompt ngắn hơn ngưỡng **không báo lỗi** — nó chỉ đơn giản không cache, và `cache_creation_input_tokens` trả về 0. Trên Haiku 4.5 ngưỡng cao gấp 8 lần Opus 5.

**Hệ quả thiết kế:** đây là lý do kỹ thuật để **giữ đủ ví dụ T1 trong prompt** thay vì cắt gọn cho ngắn. Prompt rubric đầy đủ (3 ví dụ dương + 3 ví dụ âm cho mỗi quy tắc) vượt 4.096 token dễ dàng — cache được trên mọi model, và chất lượng chấm cũng tốt hơn. Cắt prompt để "tiết kiệm token" ở đây làm mất cache và **tăng** chi phí.

**Kiểm:** sau lượt gọi thứ hai, `cache_read_input_tokens` phải > 0. Bằng 0 qua nhiều lượt liên tiếp nghĩa là tiền tố đang bị vô hiệu hoá — thường do có gì đó thay đổi ở đầu prompt (ngày, ID, thứ tự khoá JSON không ổn định).

### 14.5 Batch API cho lần chạy đêm

Pipeline chạy theo lô hằng đêm, không cần trả lời tức thời — hợp với Batch API.

| Đặc tính | Giá trị |
|---|---|
| Giảm giá | **50% mọi token** |
| Sức chứa | 100.000 yêu cầu hoặc 256 MB/lô |
| Thời gian | Phần lớn xong trong 1 giờ; tối đa 24 giờ |
| Giữ kết quả | 29 ngày |
| Tương thích | Structured outputs ✓ · Prompt caching ✓ |

**Hai điều bắt buộc:**
1. **Kết quả trả về theo thứ tự bất kỳ.** Khớp bằng `custom_id`, tuyệt đối không khớp theo vị trí. Dùng `job_id` làm `custom_id`.
2. Mỗi kết quả có trạng thái riêng — `succeeded` / `errored` / `canceled` / `expired`. Xử lý cả bốn; `expired` phải nộp lại.

Tiền tố cache dùng chung được cho toàn bộ lô — đặt `cache_control` trên phần rubric dùng chung, phần riêng của từng tin đặt sau.

Với SLA gỡ tin hết hạn 48h (PRD FR-9.1), độ trễ tối đa 24h của Batch API vẫn nằm trong ngân sách — nhưng phải tính vào, không được coi là 0.
