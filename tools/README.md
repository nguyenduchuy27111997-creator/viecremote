# Công cụ Cổng 0.1

Ba script, không phụ thuộc gì ngoài Python 3 stdlib. Đọc [../rubric-spec.md](../rubric-spec.md) trước khi chấm.

## Trước khi chạy

Sửa `CONTACT` trong `pull_sample.py` và `check_schema.py` thành email của bạn. User-Agent trung thực có liên hệ là điều kiện để không bị chặn (PRD FR-2.3).

## Ba bước

```bash
python3 tools/pull_sample.py                 # 1. kéo mẫu -> scoring-sheet.csv
python3 tools/check_schema.py -n 200         # 2. tự điền cột has_alr (tuỳ chọn, chậm)
python3 tools/tally.py                       # 3. sau khi chấm tay -> sáu con số + phán quyết
```

Bước 1 mất vài phút (tự giới hạn 1 yêu cầu/giây/miền). Bước 2 mất ~4 phút cho 200 tin.
Bước chấm tay ở giữa là việc thật — dự trù một buổi.

## Cột phải điền bằng tay

| Cột | Giá trị | Ghi chú |
|---|---|---|
| `DQ` | `x` nếu bị loại trừ | Cột `dq_hint` chỉ là **gợi ý regex**, vẫn phải đọc |
| `tier` | `A` \| `B` \| `unknown` \| `no` | Theo thứ tự đánh giá ở rubric-spec Mục 5.4 |
| `tier_a_scope` | `vn` \| `global` | Chỉ khi `tier=A`. `vn` = có A-01/04/05/06. Đây là số quyết định |
| `rules_fired` | vd `A-02;B-03` | Để hiệu chỉnh rubric sau (mục T2) |
| `quote` | trích **nguyên văn** | Không trích được -> quy tắc không kích hoạt (nguyên tắc N1) |
| `contract_mech` | `eor`/`contractor`/`entity`/`unknown` | |
| `tz_overlap` | số giờ trùng với GMT+7 | Bảng tra ở rubric-spec Mục 6 |
| `has_alr` | `y`/`n` | `check_schema.py` tự điền |
| `on_free_board` | `y`/`n` | **Chỉ cần điền cho dòng `tier=A`.** Tra trên realworkfromanywhere.com và trulyremotework.com |
| `minutes` | số phút chấm dòng này | Đừng bỏ qua — nó quyết định trần quy mô |

## Slug

`slugs.txt` là **slug phỏng đoán**. Tỷ lệ sống 30–60% ở lần đầu là bình thường; script báo cái nào hỏng.

Mở rộng dần: thấy tin nào có link `job-boards.greenhouse.io/XYZ`, `jobs.lever.co/XYZ`, `jobs.ashbyhq.com/XYZ`, `apply.workable.com/XYZ` thì thêm một dòng. Đây là FR-1.3 làm bằng tay — đủ cho Cổng 0.1. Bản tự động (Common Crawl CDX) chỉ cần khi đã qua cổng.

## Tuỳ chọn hay dùng

```bash
python3 tools/pull_sample.py -n 50                   # thử trước cho nhanh
python3 tools/pull_sample.py --per-company 1         # đa dạng công ty hơn
python3 tools/pull_sample.py --seed 7                # mẫu khác, tái lập được
```

## Lưu ý

- Chỉ đọc endpoint công khai không cần xác thực, đúng 4 nguồn ở PRD Phụ lục A
- Không lưu dữ liệu cá nhân — chỉ tin tuyển dụng
- `desc_500` cắt còn 500 ký tự cho dễ đọc; bằng chứng thật phải tra trên trang gốc qua cột `url`
