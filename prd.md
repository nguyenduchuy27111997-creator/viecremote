# PRD v2.0 — Web tra cứu tin remote

**Ngày:** 17/08/2026 · **Thay thế** PRD v1.0 (viết cho mô hình bản tin, đã bỏ)
**Sứ mệnh:** [MISSION.md](MISSION.md) — làm thị trường minh bạch với kỹ sư Việt
**Quy tắc chấm:** [rubric-spec.md](rubric-spec.md) · **Tuân thủ:** [legal-brief.md](legal-brief.md)

---

## 1. Sản phẩm một câu

> **Tra một công ty bất kỳ và biết ngay họ có tuyển được người ở Việt Nam không — kèm lý do trích dẫn được.**

Trục sản phẩm là **công ty**, không phải tin. Lý do và số liệu: [business-model.md](business-model.md) Mục 1.

Đọc-only. Không tài khoản. Không đăng tin. Không nộp hồ sơ.

## 2. Ràng buộc từ dữ liệu — quyết định sản phẩm chứa gì

Đây là phần quan trọng nhất của tài liệu. **Dữ liệu dồi dào là dữ liệu loại trừ.**

| Nếu trang hứa | Dữ liệu thật có | Kết luận |
|---|---|---|
| "Việc tuyển được ở VN" | **0/150** | **Không được hứa.** Không có gì để hiển thị |
| "Việc mở toàn cầu" | 4% ≈ 150 tin trong kho hiện tại | Hiển thị được, nhưng ít |
| **"Tin này KHÔNG mở cho bạn, vì sao"** | **84%** — có lý do trích dẫn được | **Đây là lõi sản phẩm** |
| "Cơ chế trả lương" | 7,2% | Hiển thị khi có, "Không rõ" khi không |

**Hệ quả:** trang này **không phải bộ lọc tìm việc tốt**. Nó là **bộ kiểm tra loại trừ**. Nếu marketing hứa cái đầu, nó thất bại ngày đầu tiên.

Và đó đúng là sứ mệnh A: *câu trả lời "không" có giá trị ngang câu "có"*.

## 3. Người dùng & việc cần làm

Kỹ sư Việt, đang xem một tin remote, sắp bỏ 40 phút viết cover letter.
**Việc cần làm:** biết trong 10 giây có đáng bỏ 40 phút đó không.
**Thất bại:** trang nói "đủ điều kiện" mà thực ra không → tiêu đúng thứ nó hứa tiết kiệm.

---

## 4. Phạm vi v1

### Trong phạm vi

| # | Tính năng | Ghi chú |
|---|---|---|
| **F0** | **Sổ đăng ký công ty — TRANG CHỦ.** Hồ sơ địa lý tuyển của 2.410 công ty | **Trục chính.** Xem [business-model.md](business-model.md) |
| F1 | **Trang danh sách tin** (`tin-mo.html`) — trục phụ | |
| F2 | **Trang chi tiết tin** — nhãn + lý do + trích dẫn nguyên văn + link gốc | |
| F3 | **Bộ lọc**: trạng thái · lý do loại trừ · overlap múi giờ · có công bố lương | |
| F4 | **Trang "Vì sao bị loại"** — nhóm theo lý do, kèm số lượng | Lõi sản phẩm (Mục 2) |
| F5 | **Hồ sơ công ty** — kết luận, bản đồ nước bị khoá, cơ chế, mọi tin | Đòn bẩy 64:1. Tin đổi hằng ngày, công ty đổi hằng quý |
| F6 | **Trang phương pháp** — rubric công khai, số liệu, giới hạn mẫu | Độ chính xác là sản phẩm → phương pháp phải công khai |
| F7 | Ô đăng ký email, tuỳ chọn, cuối trang | Không bắt buộc để xem gì |

### Ngoài phạm vi v1 — và vì sao

| Không làm | Lý do |
|---|---|
| Tài khoản, đăng nhập | Không có gì sau cổng. Mở rộng bề mặt PDPL vô ích |
| Nộp hồ sơ trong trang | Luôn dẫn về tin gốc |
| Công ty tự đăng tin | A3 chưa bao giờ kiểm |
| Nhận đóng góp cộng đồng | Chờ rà soát pháp lý |
| Bản tin | Chờ có khán giả |
| Tìm kiếm toàn văn | Bộ lọc đủ ở quy mô ~4.000 tin |

---

## 5. Kiến trúc — chọn theo ràng buộc "một người, 10h/tuần"

**Sinh trang tĩnh.** Pipeline chạy → xuất HTML → deploy. Không máy chủ, không database, không ops.

```
tools/pull_sample.py   →  kéo tin từ 3 ATS
tools/score_rules.py   →  chấm nhãn
tools/country.py       →  chuẩn hoá + DQ-09
        ↓
   jobs.json  (một file phẳng, ~4.000 bản ghi)
        ↓
   build.py   →  HTML tĩnh
        ↓
   deploy (Cloudflare Pages / Netlify — free tier)
```

**Vì sao tĩnh:** ~4.000 tin, cập nhật hằng ngày, đọc-only, không cá nhân hoá. Database ở đây là chi phí không mua được gì. Chuyển sang động khi nào cần tài khoản — tức là chưa.

**Chi phí:** tên miền ~12 USD/năm. Hosting 0. LLM 5–35 USD/tháng nếu bật tầng 3.

### Bản ghi tin — schema phẳng

```json
{
  "id": "...", "company": "...", "company_slug": "...",
  "title": "...", "location_raw": "...", "url": "...",
  "source": "greenhouse|lever|ashby",
  "first_seen": "2026-08-17", "last_seen": "2026-08-17",
  "status": "open|closed",

  "eligibility": "worldwide|excluded|unknown",
  "exclusion_reason": "DQ-02|DQ-05|DQ-06|...|null",
  "evidence": "trích dẫn NGUYÊN VĂN từ tin",
  "evidence_source": "location|title|description|schema",

  "timezone_overlap_gmt7": 4,
  "contract_mechanism": "eor|contractor|entity|unknown",
  "pay_disclosed": true,
  "alr_countries": ["United States"],

  "index_layer": "aggregated",
  "rubric_version": "0.4", "scored_at": "..."
}
```

**Ba nhãn hiển thị, không dùng từ nội bộ:**

| Nội bộ | Hiển thị cho người dùng |
|---|---|
| `tier_a` / worldwide | **"Mở toàn cầu"** |
| `no` | **"Không mở cho VN"** + lý do |
| `unknown` | **"Chưa xác định"** — hiển thị thật, không giấu |

---

## 6. Ràng buộc bắt buộc — không được bỏ

Bốn cái này không phải tính năng, là điều kiện để launch.

| # | Ràng buộc | Vì sao |
|---|---|---|
| **C1** | **Mọi nhãn phải có trích dẫn nguyên văn.** Không trích được → `unknown`, không đoán | Độ chính xác là sản phẩm ([MISSION.md](MISSION.md) hệ quả 1) |
| **C2** | **Không phát sinh JobPosting schema. Toàn bộ `index_layer = aggregated`** | Q1 chưa có câu trả lời từ luật sư. Mặc định an toàn |
| **C3** | **Tin biến mất khỏi feed → gỡ khỏi hiển thị trong 48h** | Chính sách Google về tin hết hạn; và tin zombie phá chính giá trị của trang |
| **C4** | **Trích đoạn mô tả ≤ 300 ký tự, có dẫn nguồn** | Bản quyền. Luôn link về tin gốc |

**Kiểm tự động trước mỗi lần deploy** — build fail nếu vi phạm C1 hoặc C2.

---

## 7. Trang phương pháp — không phải trang phụ

Vì độ chính xác là sản phẩm, phương pháp phải kiểm tra được. Trang này chứa:

- Rubric đầy đủ, công khai
- **Số liệu đo được:** 84% loại trừ · 4% mở toàn cầu · 0/150 ghi rõ tuyển VN · 7,2% nêu cơ chế
- **Độ chính xác gần nhất:** đối chứng tay 180 tin — precision 100%, DQ recall 100%
- **Giới hạn mẫu, nói thẳng:** 3 ATS · nguồn slug từ HN → thiên về công ty Mỹ/EU · ảnh chụp thời điểm
- Nút báo sai trên mọi tin

Đây cũng là tài sản GEO — dữ liệu gốc là thứ AI trích dẫn.

---

## 8. Lộ trình launch

| Mốc | Việc | Ước tính |
|---|---|---|
| **M0** | `build.py`: jobs.json → HTML tĩnh. F1, F2. Chưa CSS | 6–8h |
| **M1** | F3 bộ lọc, F4 trang "vì sao bị loại", F5 trang công ty | 6–8h |
| **M2** | F6 trang phương pháp, F7 email, kiểm C1–C4 tự động | 4h |
| **M3** | Tên miền, deploy, job cập nhật hằng ngày | 3h |
| **M4** | **Launch** | — |

**~20–25 giờ ≈ 2–3 tuần ở nhịp 10h/tuần.**

### Điều kiện launch

- [ ] Kiểm C1–C4 chạy sạch
- [ ] ≥ 100 tin "mở toàn cầu" trong kho *(hiện có ~150)*
- [ ] Trang phương pháp có số liệu và **giới hạn mẫu**
- [ ] Lấy mẫu tay 20 tin bất kỳ, xác nhận nhãn đúng
- [ ] Job gỡ tin hết hạn chạy được, có cảnh báo khi lỗi

**Không cần trước khi launch:** buổi luật sư (C2 đã là mặc định an toàn) · bản tin · A8 · đóng góp cộng đồng.

---

## 9. Đo gì sau launch

| Chỉ số | Vì sao |
|---|---|
| **Tỷ lệ báo nhãn sai** | Chỉ số sống còn. Sứ mệnh hỏng nếu số này cao |
| Số lần bấm "xem tin gốc" | Giá trị thật đến tay người dùng |
| Trang "vì sao bị loại" — lượt xem so với trang danh sách | Kiểm giả thuyết lõi ở Mục 2 |
| Đăng ký email | Kênh sở hữu |

**Không đo:** tổng số tin trong kho, tổng lượt xem trang. Chỉ số phù phiếm.

---

## 10. Rủi ro đã biết

| Rủi ro | Xử lý |
|---|---|
| Chỉ ~150 tin "mở toàn cầu" — kho mỏng | Chấp nhận. Thà 150 tin đúng hơn 4.000 tin đoán. Mở rộng slug nếu cần |
| Nhãn sai lọt ra ngoài | C1 + nút báo sai + lấy mẫu tay hằng tháng |
| Bị một ATS chặn | Poll theo bậc (đã có trong `pull_sample`); mất 1 nguồn = mất ~1/3 |
| Không ai dùng | Đó là câu trả lời. Cổng: 30 ngày sau launch, < 100 người dùng duy nhất → xem lại |
