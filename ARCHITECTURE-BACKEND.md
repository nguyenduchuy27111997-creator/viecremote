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

| # | Lỗ hổng | Hậu quả thật | Sửa |
|---|---|---|---|
| **1** | **Không phải git repo** | Không có lịch sử, không quay lui được code, một `rm` sai là mất hết. 3.460 dòng Python + toàn bộ tài liệu đang **không được bảo vệ** | `git init` + push private. **~15 phút** |
| **2** | **Cron chạy trên laptop** | Máy ngủ ⇒ không cập nhật. **Đã xảy ra trong phiên này** | Chuyển sang GitHub Actions hoặc một VPS luôn bật |
| **3** | **Không có cảnh báo** | Cron chết thì phát hiện sau **7 ngày** (đọc log hằng tuần) | Healthcheck: cron ping một URL sau khi chạy xong; không ping thì báo |
| **4** | **Không có CI** | `eval.py` chỉ chạy khi nhớ. Sửa luật làm tụt precision mà không ai biết | GitHub Actions chạy `eval.py` mỗi lần push |
| **5** | **Không có staging** | Deploy thẳng lên production | Cloudflare Workers có preview URL — dùng trước khi promote |
| **6** | **Seed D1 không nguyên tử** | 13 tệp seed chạy tuần tự; đứt giữa chừng để lại DB nửa vời | Seed vào bảng tạm rồi `ALTER TABLE ... RENAME` |
| **7** | **Build Next chạy trên laptop** | Deploy cần node + mạng + ~1 phút | Cùng lời giải với #2 |

**#1 nguy hiểm nhất và rẻ nhất.** Mọi thứ khác trong bảng này đều giả định code còn tồn tại.

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

| # | Việc | Thời gian | Giải lỗ hổng |
|---|---|---|---|
| 1 | `git init` + push private | 15 phút | #1 |
| 2 | GitHub Actions: CI chạy `eval.py` | 30 phút | #4 |
| 3 | GitHub Actions: cron `refresh.sh --deploy` | 1 giờ | #2, #3, #7 |
| 4 | Seed D1 vào bảng tạm rồi rename | 1 giờ | #6 |
| 5 | Preview URL trước khi promote | 30 phút | #5 |

**Tổng ~3 giờ.** Không nằm trong 8 giờ chặn launch — nhưng **việc #1 nên làm ngay hôm nay**,
trước cả deploy. Mọi thứ khác giả định code còn tồn tại.
