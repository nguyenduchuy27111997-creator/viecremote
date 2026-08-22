# Kế hoạch vận hành

**Ngày:** 21/08/2026 · **Ràng buộc cứng:** một người, **10 giờ/tuần**
Chiến lược: [business-model.md](business-model.md) · Kiến trúc: [ARCHITECTURE-WEB.md](ARCHITECTURE-WEB.md)

---

## 0. Nguyên tắc vận hành

> **Thà site cũ một ngày còn hơn nhãn sai.**

Mọi bước trong `refresh.sh` hỏng đều khôi phục `jobs.json` và thoát mã 1 — **không đẩy gì lên**.
Đây không phải cẩn thận thừa: sứ mệnh nói *thông tin sai mà người ta tin* là thất bại nặng hơn
*thông tin đúng mà không ai đọc*. Vận hành phải phản ánh thứ tự đó.

---

## 1. Nhịp hằng ngày — tự động, 0 phút người

```bash
./refresh.sh --deploy
```

Cron 05:17 mỗi ngày. Bốn bước, mỗi bước là một cổng:

| # | Bước | Thời gian | Hỏng thì sao |
|---|---|---|---|
| 1a | Kéo slug **đến hạn** (~2.450/5.686) | ~16 phút | Khôi phục `jobs.json`, thoát |
| 1b | Đọc `applicantLocationRequirements` 2.500 tin | **~42 phút** | như trên |
| 2 | Xuất SQLite + seed **kèm cổng C1–C5** | ~40 giây | Khôi phục, thoát — **dữ liệu sai không bao giờ tới DB** |
| 3 | Dựng bản tĩnh (đường lui) | ~4 giây | Khôi phục, thoát |
| 4 | Nạp D1 từ xa + deploy Worker | ~6 phút | Khôi phục, thoát |

**Tổng ~60 phút/ngày**, không phải 16 — bước đọc schema (1b) chiếm phần lớn. Đo thật ngày
22/08. Con số này quan trọng cho GitHub Actions: 60 phút × 30 ngày = **1.800 phút/tháng**, sát
trần 2.000 phút của repo private. Vượt thì chuyển repo sang public (dự án vốn không có gì bí mật)
hoặc hạ `--schema-limit`.

**Vì sao chỉ 16 phút cho bước kéo chứ không 110:** phân bậc poll trong `tools/tiering.py` chỉ kéo slug đến hạn.

| Bậc | Nhịp | Điều kiện |
|---|---|---|
| nóng | 1 ngày | sinh tin mở-toàn-cầu trong 90 ngày |
| ấm | 3 ngày | có tin đang mở |
| nguội | 7 ngày | không có tin, hoặc 180 ngày không sinh tin mở |
| chết | 90 ngày | 3 lần gọi liên tiếp lỗi |

Khoảng **1.300/5.700 slug** mỗi ngày. Tin của slug quá **30 ngày** không được hiển thị nữa
(`STALE_DAYS`) — chống tin zombie.

---

## 2. Nhịp hằng tuần — 2 giờ người

| Việc | Thời gian | Vì sao |
|---|---|---|
| Đọc `logs/refresh.log` 7 ngày, tìm dòng `LỖI` | 15 phút | Cron hỏng im lặng là kiểu hỏng tệ nhất |
| Xem **nút báo sai** người dùng gửi | 30 phút | Chỉ số sống còn của sứ mệnh |
| Chấm tay **5 tin ngẫu nhiên** từ nhóm "mở" | 45 phút | Phát hiện trôi nhãn trước khi nó thành hệ thống |
| Ghi số liệu tuần vào `STATUS.md` | 30 phút | Không đo thì không biết đang thắng hay thua |
| `python3 tools/post_numbers.py --check` trước mọi lần đăng bài | 2 phút | Kho đổi mỗi ngày. Chỉ sau MỘT chu kỳ, số công ty mở đã 110 → 103 |

---

## 3. Nhịp hằng tháng — 4 giờ người

| Việc | Vì sao |
|---|---|
| **Audit phân tầng 40 tin** từ nhóm "mở", mẫu không giao đợt trước | Precision là thứ duy nhất đang bán. Đợt 3 rơi xuống 70% mà không ai biết cho tới khi đo |
| Chạy `tools/cc_slugs.py` thu slug mới | Kho phải tăng để tới ngưỡng 10.000 công ty |
| `npm audit` trong `web/` | 288 gói — đây là chi phí đã chọn khi rời bản tĩnh |
| Đối chiếu `tools/gates.py` `TRIGGER` với `score_rules.DQ` | Thêm luật mà quên từ vựng thì C1 chặn build với trích dẫn hợp lệ. **Đã xảy ra một lần** |

---

## 4. Kiểu hỏng đã biết và cách xử

| Triệu chứng | Nguyên nhân thật | Xử |
|---|---|---|
| `refresh.log` không có dòng mới | Cron chết, hoặc máy ngủ | Kiểm `crontab -l`; máy laptop ngủ thì chuyển cron sang máy chủ luôn bật |
| Bước 2 dừng, in `C1 …` | Thêm luật DQ mà quên thêm từ vựng vào `TRIGGER` | Thêm từ vào `tools/gates.py` |
| Bước 2 dừng, in `C5 …` | Nhãn "mở toàn cầu" xung đột với `alr_countries` | `tools/rescore.py --eligibility worldwide` |
| Số tin tụt đột ngột | Một ATS đổi API hoặc chặn | Kiểm log tỉ lệ `sống/tổng`; mất 1 nguồn ≈ mất 1/3 kho |
| D1 trả `SQLITE_TOOBIG` | Câu INSERT quá dài | Giảm `per_stmt` trong `tools/export_db.py` |
| Worker vượt 100k request/ngày | Có lưu lượng thật (tin tốt) | Nâng Workers Paid 5 USD/tháng |

---

## 5. Cái gì KHÔNG tự động — và vì sao

| Việc | Vì sao không tự động |
|---|---|
| Cài cron | Sửa hệ thống của bạn. Lệnh có sẵn ở đầu `refresh.sh`, tự chạy |
| Tạo D1 từ xa, deploy lần đầu | Cần tài khoản Cloudflare của bạn |
| Sửa nhãn sau khi có báo sai | Phải đọc tin gốc. Sửa mù còn tệ hơn để nguyên |
| A3, A8 (nói chuyện với người thật) | Đây là việc quan trọng nhất và không máy nào làm thay được |

---

## 6. Ngân sách thời gian — kiểm tính khả thi

| Nhịp | Giờ/tháng |
|---|---|
| Hằng ngày (tự động) | 0 |
| Hằng tuần × 4 | 8 |
| Hằng tháng | 4 |
| **Tổng vận hành** | **12** |
| Quỹ 10h/tuần | 40 |
| **Còn lại cho phát triển và A3/A8** | **28** |

Vận hành ăn **30%** quỹ thời gian. Nếu vượt 50% thì tự động hoá đang thua và phải cắt bớt —
ứng viên cắt đầu tiên là audit hằng tháng hạ xuống hằng quý, nhưng **chỉ khi** ba đợt liên
tiếp đều ≥95%.

---

## 7. Chi phí tiền mặt

| Khoản | Tháng | Năm |
|---|---|---|
| Cloudflare Workers (free 100k req/ngày) | 0 | 0 |
| Cloudflare D1 (free 5 GB · 5 tr đọc/ngày) | 0 | 0 |
| Tên miền | ~1 | ~12 |
| **Tổng** | **~1 USD** | **~12 USD** |

Không có chi phí LLM: toàn bộ chấm nhãn là quy tắc, không gọi mô hình. Đây là lý do dự án
sống được ở 0 doanh thu vô thời hạn — **thời gian là ràng buộc, không phải tiền**.

---

## 8. Lịch chạy hằng ngày — GitHub Actions

Repo: **github.com/nguyenduchuy27111997-creator/viecremote** (public)
Workflow: `.github/workflows/refresh.yml` · **22:17 UTC = 05:17 giờ VN**

```bash
gh run list --workflow=refresh.yml --limit 5     # 5 lần chạy gần nhất
gh run watch                                     # theo dõi lần đang chạy
gh workflow run "Cập nhật hằng ngày" -f deploy=true   # chạy ngay
gh run view <id> --log-failed                    # xem log bước hỏng
```

**Repo để public** vì Actions free cho private chỉ 2.000 phút/tháng, mà chu kỳ đo được là
~60 phút/ngày = 1.800 phút — sát trần, một lần chạy lại thủ công là vượt. Public thì không
giới hạn phút. Dự án vốn không có gì bí mật; secret nằm ở GitHub Secrets, không trong repo.

### Ba thứ phải có trong repo

| Loại | Tên | Quyền cần |
|---|---|---|
| Secret | `CLOUDFLARE_API_TOKEN` | **Workers Scripts:Edit** + **D1:Edit**, không hơn |
| Secret | `CLOUDFLARE_ACCOUNT_ID` | — |
| Variable | `SITE_URL` | — |

Workflow **kiểm token ngay bước đầu** (`wrangler whoami` + `d1 list`). Sai quyền thì dừng sau
~40 giây thay vì 25 phút — token vốn chỉ được dùng ở bước nạp D1, tức sau cả bước kéo tin.

### Cảnh báo khi hỏng

GitHub gửi email khi job đỏ. Đó là toàn bộ cơ chế cảnh báo hiện có — không có gì khác. Cron
hỏng im lặng là kiểu hỏng tệ nhất, nên đừng tắt thông báo của repo này.

### Đã bỏ: launchd trên máy

Từng cài rồi gỡ. Lý do gỡ: Actions không phụ thuộc máy bật, còn launchd thì máy tắt là không
chạy. Hai lịch chồng nhau chỉ tạo hai nguồn sự thật.

**Hai bẫy macOS đã sập lúc cài, ghi lại phòng khi cần lại:**

1. **TCC chặn launchd thực thi tệp trong `~/Desktop`, `~/Documents`, `~/Downloads`** —
   `bash: ./refresh.sh: Operation not permitted`. Đã kiểm dứt điểm: cùng một job, script ở
   `~/tcc-probe` chạy được, ở `~/Desktop/...` bị chặn. Đây là lý do dự án nằm ở `~/viecremote`.
2. **Log cũng không được để trong thư mục bị TCC.** launchd *tự* mở `StandardOutPath`, và nó
   không có quyền TCC — job chết với `EX_CONFIG (78)` **trước khi chạy dòng nào**, log rỗng nên
   không manh mối gì.
