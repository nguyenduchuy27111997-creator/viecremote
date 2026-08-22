# Triển khai — Next.js trên Cloudflare Workers

> **Dùng `./deploy.sh`.** Nó làm toàn bộ các bước dưới đây, idempotent, chạy lại
> được nếu đứt giữa chừng. Tài liệu này giữ lại để hiểu từng bước làm gì.
>
> ```bash
> cd web && npx wrangler login   # một lần duy nhất
> cd .. && ./deploy.sh
> ```

Mọi bước dưới đây **cần tài khoản Cloudflare của bạn**. Tôi không chạy được.

---

## 1. Đăng nhập

```bash
cd web && npx wrangler login
```

## 2. Tạo D1 từ xa

```bash
cd web && npx wrangler d1 create viec-remote
```

Chép `database_id` trả về, thay `PLACEHOLDER` trong `web/wrangler.jsonc`.

## 3. Nạp dữ liệu

```bash
cd web && for f in ../data/seed-*.sql; do npx wrangler d1 execute viec-remote --remote --file="$f"; done
```

Mười tệp, ~15 MB. Chia sẵn thành từng câu 40 dòng vì D1 trả `SQLITE_TOOBIG` với câu dài hơn.

## 4. Triển khai

```bash
cd web && npx opennextjs-cloudflare build && npx opennextjs-cloudflare deploy
```

## 4b. Biến môi trường — làm trước khi deploy

Chép `web/.env.example` thành `web/.env.local` rồi điền:

| Biến | Lấy ở đâu | Thiếu thì sao |
|---|---|---|
| `NEXT_PUBLIC_CF_ANALYTICS_TOKEN` | Dashboard → Analytics → Web Analytics | **Không đo được cổng GĐ 0** — cổng quan trọng nhất của kế hoạch |
| `NEXT_PUBLIC_SITE_URL` | Tên miền của bạn | Sitemap và ảnh OG trỏ sai miền |
| `TURNSTILE_SECRET` *(tuỳ chọn)* | Dashboard → Turnstile | Vẫn còn honeypot + kiểm thời gian, đủ dùng lúc đầu |

Turnstile là secret phía máy chủ, đặt bằng lệnh riêng:

```bash
cd web && npx wrangler secret put TURNSTILE_SECRET
```

**Bảng `report` do người dùng ghi — đừng bao giờ xoá khi seed lại.** `data/seed-00-schema.sql`
dùng `CREATE TABLE IF NOT EXISTS` nên chạy lại an toàn, nhưng đừng `DROP` bảng đó.

---

## 5. Tên miền

Cloudflare dashboard → Workers → `viec-remote` → Settings → Domains & Routes.

---

## Làm mới hằng ngày

```bash
python3 tools/export_jobs.py --refresh && python3 tools/export_db.py && \
  cd web && for f in ../data/seed-*.sql; do npx wrangler d1 execute viec-remote --remote --file="$f"; done
```

**Chưa tối ưu:** hiện là nạp đè toàn bộ. Ở 10.000 công ty nên chuyển sang nạp chênh lệch
(so `last_seen`, chỉ `UPSERT` bản ghi đổi). Chưa cần ở quy mô này.

---

## Chi phí

| | |
|---|---|
| Workers free | 100.000 request/ngày, rồi 0,50 USD/triệu |
| D1 free | 5 GB lưu trữ · 5 triệu lượt đọc/ngày |
| Tên miền | ~12 USD/năm |

Ở lưu lượng dự kiến năm đầu: **0 đồng ngoài tên miền.**

---

## Bản tĩnh vẫn còn

`python3 build.py` vẫn dựng `site/` và vẫn qua cả 5 cổng C1–C5. Giữ nó làm đường lui cho
tới khi bản Next.js chạy production ổn định ít nhất một tháng. Xem
[ARCHITECTURE-WEB.md](ARCHITECTURE-WEB.md) Mục 6 — ba trong năm cổng **chưa** chuyển sang
luồng mới.
