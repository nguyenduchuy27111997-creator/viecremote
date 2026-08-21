# Kiến trúc back-end và DevOps

**Ngày:** 21/08/2026 · Rà hiện trạng thật, không phải sơ đồ lý thuyết
Giao diện: [ARCHITECTURE-WEB.md](ARCHITECTURE-WEB.md) · Vận hành: [OPERATIONS.md](OPERATIONS.md)

---

## 0. Đọc trước: back-end ở đây không phải máy chủ

Không có API server, không có ORM, không có hàng đợi, không có worker pool.
**Back-end của dự án này là một pipeline dữ liệu chạy theo lịch** — 3.460 dòng Python,
**không một phụ thuộc ngoài nào**.

Lý do: mọi thứ nặng đều xảy ra **trước** khi có người dùng. Khi người dùng vào trang, tất cả
đã được tính xong và nằm trong SQLite ở biên. Không có gì để tính lúc chạy.

---

## 1. Hình dạng

```
    ┌─ NGUỒN ────────────────────────────────────────────┐
    │  Greenhouse · Lever · Ashby   (API JSON công khai) │
    │  Common Crawl CDX             (thu hoạch slug)      │
    └────────────────────┬───────────────────────────────┘
                         │  1 req/giây/miền · 32 luồng
    ┌────────────────────▼───────────────────────────────┐
    │  TẦNG KÉO        tools/pull_sample · cc_slugs      │
    │                  tools/tiering  ← chỉ slug ĐẾN HẠN │
    └────────────────────┬───────────────────────────────┘
    ┌────────────────────▼───────────────────────────────┐
    │  TẦNG CHẤM       tools/score_rules  (460 dòng luật)│
    │                  tools/country      (ISO + vùng)    │
    │                  tools/export_jobs  (trọng tài)     │
    └────────────────────┬───────────────────────────────┘
                         │
                    jobs.json  ← nguồn sự thật, 34 MB
                         │
    ┌────────────────────▼───────────────────────────────┐
    │  CỔNG            tools/gates.py   C1..C5           │
    │                  vi phạm ⇒ exit 1, KHÔNG xuất gì   │
    └────────────────────┬───────────────────────────────┘
            ┌────────────┴────────────┐
    ┌───────▼────────┐        ┌───────▼─────────────────┐
    │ tools/export_db│        │ build.py                │
    │ → SQLite + SQL │        │ → site/ tĩnh (đường lui)│
    └───────┬────────┘        └─────────────────────────┘
            │ wrangler d1 execute --remote
    ┌───────▼────────────────────────────────────────────┐
    │  Cloudflare D1  (SQLite ở biên)                    │
    │  company · job · company_fts · meta · report       │
    └───────┬────────────────────────────────────────────┘
    ┌───────▼────────────────────────────────────────────┐
    │  Worker (Next.js qua @opennextjs/cloudflare)       │
    │  RSC đọc D1 · /api/companies · /api/bao-sai        │
    └────────────────────────────────────────────────────┘
```

---

## 2. Bốn quyết định back-end

### 2.1 Không phụ thuộc ngoài trong Python

3.460 dòng, chỉ thư viện chuẩn. Không `requests`, không `pandas`, không `beautifulsoup`.

Đổi lại: viết tay nhiều hơn (gate pacing, parser HTML thô). Được lại: **pipeline không bao giờ
hỏng vì một gói bên thứ ba đổi API hay bị bỏ rơi**, và không có bề mặt bảo mật nào cần vá.
Ở dự án một người, chi phí bảo trì phụ thuộc là chi phí thật.

Đối lập rõ rệt: `web/` có **823 MB node_modules**. Đó là cái giá đã chọn khi rời bản tĩnh.

### 2.2 `jobs.json` là nguồn sự thật, D1 là bản phái sinh

D1 dựng lại được hoàn toàn từ `jobs.json` bằng một lệnh. Nghĩa là:

- Seed hỏng ⇒ chạy lại `export_db.py`, không mất gì
- Đổi schema ⇒ sửa `SCHEMA` rồi seed lại, không cần migration
- **Ngoại lệ duy nhất: bảng `report`** — do người dùng ghi, không phái sinh từ đâu cả.
  Đây là dữ liệu duy nhất chỉ tồn tại ở D1. Xoá nó là mất vĩnh viễn.

### 2.3 Cổng nằm giữa pipeline và mọi đầu ra

`tools/gates.py` được **cả hai** luồng gọi. Không phải để gọn code — để **luồng lỏng hơn không
thành luồng lên production**. Đã kiểm đối kháng sáu ca, cả hai luồng thoát mã 1 và không sinh
đầu ra nào.

### 2.4 Trần 1 req/giây/miền là TỐC ĐỘ PHÁT, không phải số kết nối

Bản đầu nối tiếp: ngủ 1 giây **rồi** chờ tải xong 3,5 giây ⇒ đạt 0,28 req/giây, mất 5,4 giờ.
Bản hiện tại tách hai thứ: cổng phát nhịp giữ đúng 1 req/giây/miền, 32 luồng chờ tải song song.
Còn **68 phút** cho toàn kho, **16 phút** khi chỉ kéo slug đến hạn.

---

## 3. Phân bậc poll — thứ làm cron khả thi

| Bậc | Nhịp | Điều kiện |
|---|---|---|
| nóng | 1 ngày | sinh tin mở-toàn-cầu trong 90 ngày |
| ấm | 3 ngày | có tin đang mở |
| nguội | 7 ngày | không có tin, hoặc 180 ngày không sinh tin mở |
| chết | 90 ngày | 3 lần gọi liên tiếp lỗi |

~1.300/5.700 slug mỗi ngày. Không có bậc thì cron 110 phút/ngày — bất khả thi trên laptop.

`STALE_DAYS = 30`: tin của slug quá 30 ngày không được hiển thị. Chống tin zombie.

---

## 4. DevOps — hiện trạng thật

### 4.1 Có gì

| | |
|---|---|
| Triển khai | `refresh.sh --deploy` · 4 bước, mỗi bước là cổng |
| Quay lui dữ liệu | `logs/jobs-*.json.bak`, giữ 14 ngày |
| Nguyên tắc hỏng | Bất kỳ bước nào lỗi ⇒ khôi phục `jobs.json`, exit 1, **không đẩy gì** |
| Đối chứng | `tools/eval.py` — 180 tin, 4 ngưỡng |
| Bí mật | `wrangler secret` cho `TURNSTILE_SECRET` |

### 4.2 Thiếu gì — xếp theo mức nguy hiểm

| # | Lỗ hổng | Trạng thái |
|---|---|---|
| 1 | Không phải git repo | ✅ **xong** — `git init`, 299 tệp, repo 3,4 MB |
| 2 | Cron chạy trên laptop | ✅ **xong** — `.github/workflows/refresh.yml`, cron 22:17 UTC |
| 3 | Không có cảnh báo | ✅ **xong** — Actions gửi email khi job đỏ |
| 4 | Không có CI | ✅ **xong** — `.github/workflows/ci.yml` |
| 5 | Không có staging | ✅ **xong** — `.github/workflows/preview.yml` |
| 6 | Seed D1 không nguyên tử | ✅ **xong** — bảng `*_new` + hoán đổi ở tệp cuối |
| 7 | Build Next chạy trên laptop | ✅ **xong** — chạy trên runner |

### Seed nguyên tử — cách làm và bằng chứng

13 tệp nạp vào `company_new` / `job_new` / `meta_new`. **Chỉ tệp cuối** (`seed-12-swap.sql`)
mới drop bảng cũ và đổi tên. Cửa sổ dữ liệu không nhất quán rút từ *cả quá trình nạp* xuống
*một tệp DROP+RENAME*.

Đã kiểm bằng cách cố ý đứt trước tệp cuối:

| | Trước | Sau khi đứt |
|---|---|---|
| `company` (cũ) | 3.666 | **3.666** — nguyên vẹn |
| `company_new` | — | 3.666 — chờ hoán đổi |
| `report` (người dùng ghi) | 2 | **2** — không mất |

**Một bẫy D1:** khác SQLite mặc định, **D1 THỰC THI foreign key**. Schema cũ có
`job.company_slug REFERENCES company(slug)`, nên drop `company` trước `job` trả
`SQLITE_CONSTRAINT_FOREIGNKEY`. Thứ tự hoán đổi phải là **con trước, cha sau**. Bảng mới bỏ
hẳn FK — SQLite vốn không thực thi nó theo mặc định nên nó chỉ là chú thích tốn phí.

### Điều CI thật sự kiểm

Không chỉ chạy `eval.py`. Nó còn **kiểm chính cái cổng**: sáu ca cố ý làm hỏng dữ liệu
(mất trích dẫn, trích dẫn vô nghĩa, trích đoạn 301 ký tự, tin đã đóng, sai `index_layer`,
xung đột C5) — cả sáu phải bị chặn, nếu không CI đỏ.

Cổng im lặng còn tệ hơn không có cổng.

---

## 5. Đề xuất: chuyển cron sang GitHub Actions

Giải một lúc #2, #3, #4, #7 — và #1 là điều kiện tiên quyết.

```
git repo (private)
   ├── push        → CI: python3 tools/score_rules.py && tools/eval.py
   └── cron 05:17  → refresh.sh --deploy trên runner Ubuntu
                     ├── kéo + chấm (16 phút)
                     ├── cổng C1..C5
                     ├── seed D1 --remote
                     ├── opennextjs deploy
                     └── thất bại ⇒ GitHub gửi email
```

**Chi phí: 0.** GitHub Actions free cho repo private là 2.000 phút/tháng; job này ~25
phút/ngày = 750 phút/tháng. Vừa khít, và nếu vượt thì chuyển repo sang public — dự án này
vốn không có gì bí mật.

Cần đặt ba secret trong repo: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`,
`TURNSTILE_SECRET`.

**Điều cần cân nhắc trung thực:** `jobs.json` 34 MB và `data/` 50 MB. Đừng commit chúng —
runner phải tự dựng lại từ `slugs.txt` mỗi lần, hoặc dùng Actions cache. Trạng thái duy nhất
phải giữ giữa các lần chạy là `tools/slug_state.json` (bậc poll) — nhỏ, commit được.

---

## 6. Điểm hỏng và bán kính ảnh hưởng

| Hỏng ở đâu | Bán kính | Phát hiện thế nào |
|---|---|---|
| Một ATS đổi API | Mất ~1/3 kho | Tỉ lệ `sống/tổng` trong log tụt |
| Common Crawl chặn | Kho ngừng tăng | Log `cc_slugs` |
| D1 vượt hạn mức free | Trang chết | Cloudflare dashboard |
| Worker vượt 100k req/ngày | Trang chết | Cloudflare dashboard |
| Seed hỏng giữa chừng | **DB nửa vời, trang sai** | **Chưa có gì phát hiện** ← lỗ hổng #6 |
| Cron chết | Dữ liệu đóng băng | **Sau 7 ngày** ← lỗ hổng #3 |
| Bug trong luật chấm | Nhãn sai lan ra toàn kho | `eval.py` — nhưng chỉ khi nhớ chạy ← lỗ hổng #4 |

Hai ô đậm là chỗ hệ thống **hỏng im lặng**. Đó là kiểu hỏng tệ nhất với một sản phẩm mà thứ
duy nhất nó bán là độ chính xác.

---

## 7. Thứ tự làm

**Cả năm việc đã xong 22/08.** Còn lại là phần chỉ bạn làm được:

| # | Việc | Ai |
|---|---|---|
| 1 | Tạo repo private trên GitHub, `git push` | **Bạn** |
| 2 | Đặt secret: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `CF_ANALYTICS_TOKEN` | **Bạn** |
| 3 | Đặt biến `SITE_URL` (Settings → Variables) | **Bạn** |
| 4 | Bật Actions, chạy thử `Cập nhật hằng ngày` bằng tay một lần | **Bạn** |

Token Cloudflare cần đúng hai quyền: **Workers Scripts:Edit** và **D1:Edit**. Đừng dùng
Global API Key — nó có toàn quyền tài khoản.
