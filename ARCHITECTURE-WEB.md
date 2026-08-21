# Kiến trúc web — Next.js 16

**Ngày:** 21/08/2026 · **Thay thế** trang tĩnh sinh bằng `build.py` cho phần giao diện
**Pipeline dữ liệu Python giữ nguyên** — chỉ thêm một bước xuất.

---

## 1. Vì sao đổi (và vì sao trước đó tôi nói không nên)

Trước đây tôi lập luận trang tĩnh là đúng, và ở thời điểm đó lập luận đó đúng: 329 tin,
2.410 công ty, không tài khoản, không cá nhân hoá. Ba thay đổi làm nó hết đúng:

| Thay đổi | Hệ quả kỹ thuật |
|---|---|
| **Trục chuyển sang công ty**, đích 10.000+ hồ sơ | Không nhét cả kho vào bundle được nữa |
| **Cần tra cứu thật** theo tên, kết luận, cơ chế | Đây là truy vấn, không phải lọc mảng trong trình duyệt |
| **API là mặt hàng B2B** ([business-model.md](business-model.md) GĐ2) | Cần route handler, không phải tệp tĩnh |

Đây là **yêu cầu đổi**, không phải quan điểm đổi. Ở 329 tin thì tĩnh vẫn thắng.

---

## 2. Hình dạng

```
tools/pull_sample · discover_slugs · cc_slugs      kéo tin
        ↓
tools/export_jobs · score_rules · country          chấm nhãn
        ↓
   jobs.json                                       nguồn sự thật
        ↓
tools/export_db.py                                 gộp tin -> HỒ SƠ CÔNG TY
        ↓
   data/app.db  +  data/seed-*.sql
        ↓
   Cloudflare D1 (SQLite ở biên)
        ↓
   Next.js 16 App Router — RSC + Cache Components + PPR
        ↓
   @opennextjs/cloudflare  ->  Cloudflare Workers
```

**Python vẫn là nơi chấm nhãn.** Toàn bộ bộ quy tắc, 5 đợt audit, và các cổng C1–C5 nằm
nguyên ở đó. Next.js chỉ đọc kết quả. Không nhân đôi logic sang TypeScript — nhân đôi là
cách chắc chắn nhất để hai bên trôi khỏi nhau.

---

## 3. Bốn quyết định, và lý do

### 3.1 D1 thay vì JSON nhúng

10.000 công ty × ~1 KB = 10 MB. Không thể là bundle. Và tra cứu theo tên ở quy mô đó cần
chỉ mục, không phải `Array.filter`.

D1 là SQLite chạy ở biên. Bảng `company_fts` dùng **FTS5** — `LIKE '%x%'` quét toàn bảng,
không dùng được. Free tier 5 GB, 5 triệu lượt đọc/ngày.

### 3.2 Cache Components + PPR

Bật một cờ `cacheComponents: true` là PPR thành mặc định. Mỗi trang tách làm hai:

- **Vỏ tĩnh** — tiêu đề, dải mật độ, điều hướng. Phục vụ ở tốc độ CDN.
- **Lỗ động** — kết quả tra cứu, hồ sơ theo slug. Stream vào sau.

Quy tắc phải tuân, cả hai đều bị vi phạm ở lần viết đầu và build bắt được:

1. `useSearchParams()` phải nằm **trong** `<Suspense>`. Ngoài ra là chặn prerender.
2. `await params` cũng phải nằm **trong** `<Suspense>` — **kể cả với slug đã dựng sẵn**.
   Await ở ngoài trói App Shell vào một URL cụ thể.

### 3.3 Dựng sẵn 110, App Shell cho 3.556 còn lại

```ts
export async function generateStaticParams() {
  const rows = await all("SELECT slug FROM company WHERE verdict = 'ok' ...")
  return rows.map((r) => ({ slug: r.slug }))
}
```

Cộng `partialPrefetching: true`: URL nằm trong danh sách được phục vụ đầy đủ từ cache;
URL lạ nhận App Shell tức thì rồi được nâng cấp ngầm, lần sau lấy từ cache.

**Build không phình theo kho.** Đây là điều kiện để đi tới 10.000 công ty.

### 3.4 `cacheLife("days")` ở mọi `use cache`

Kho dựng lại mỗi ngày, nên `days` (revalidate 1 ngày, expire 1 tuần) khớp đúng nhịp.
Docs yêu cầu nêu tường minh tại chỗ gọi thay vì dựa vào profile `default` — làm vậy thì
đọc code là biết vòng đời cache, không phải tra ngược.

---

## 4. Ba lỗi gặp khi dựng, và cách sửa

| Lỗi | Nguyên nhân | Sửa |
|---|---|---|
| `table sqlite_master may not be modified` | `sqlite3.iterdump()` xuất bảng bóng FTS5 dưới dạng ghi thẳng vào `sqlite_master` | Sinh SQL tường minh, tạo FTS rỗng rồi `INSERT ... SELECT` |
| `SQLITE_TOOBIG` | Một `INSERT` gộp 4.000 dòng vượt trần câu lệnh của D1 | Hai mức chia: 40 dòng/câu, 4.000 dòng/tệp |
| `D1_ERROR: internal error` lúc build | 11 worker build đập vào D1 cục bộ (miniflare, một tiến trình) | `experimental: { cpus: 1 }` |

Và một lỗi **dữ liệu** mà tầng D1 phơi ra, tầng tĩnh thì giấu:

> `UNIQUE constraint failed: job.id` — `id` cắt cứng 90 ký tự nên tiêu đề dài đụng nhau.
> `legionhealth` đăng cùng vai trò **57 lần với 57 URL khác nhau**, tất cả rút về một `id`.
> `build.py` ghi `viec/{id}.html` nên chúng ghi đè lẫn nhau — **86 tin biến mất âm thầm.**
> Sửa: gắn 6 ký tự băm SHA-1 của URL. Ràng buộc khoá chính bắt được thứ mà hệ thống tệp
> chỉ lặng lẽ ghi đè.

---

## 5. So sánh trung thực với bản tĩnh

| | `build.py` (tĩnh) | Next.js 16 + D1 |
|---|---|---|
| Thời gian build | 3,4 giây | ~30 giây |
| Phụ thuộc ngoài | **0** | 288 gói |
| Trang dựng sẵn | 4.190 (tất cả) | 112 + App Shell |
| Tra cứu | Không có | FTS5 phía máy chủ |
| API | Không có | `/api/companies` |
| Chi phí | 0 đồng | 0 đồng (Workers free: 100k req/ngày) |
| Điểm hỏng | Không | D1, Worker |
| Bảo trì | Không | Cập nhật bảo mật của 288 gói |

**Cái mất là thật.** Bản tĩnh không bao giờ hỏng và không bao giờ cần vá. Cái được — tra
cứu, API, build không phình — chỉ đáng giá **nếu** thật sự đi tới 10.000 công ty và **nếu**
A3 xác nhận có người mua API. Cả hai đều chưa chắc.

`build.py` vẫn chạy được và vẫn qua cả 5 cổng. Giữ nó cho tới khi Next.js chạy trên
production ít nhất một tháng.

---

## 6. Ràng buộc tuân thủ — một bộ luật, hai luồng

Cổng nằm ở **`tools/gates.py`**, không nằm trong `build.py`. Lý do: có hai luồng xuất bản
dùng chung dữ liệu. Nếu mỗi luồng tự kiểm, hai bên sẽ trôi khỏi nhau — và **luồng lỏng hơn
sẽ là luồng lên production**.

```
tools/gates.py  →  validate(jobs)  →  enforce(jobs, where)
        ↑                                    ↑
   build.py                        tools/export_db.py
   (trang tĩnh)                    (Next.js + D1)
```

| Cổng | Kiểm ở đâu | Cả hai luồng |
|---|---|---|
| C1 trích dẫn nguyên văn lý giải được nhãn | `gates.py` | ✅ |
| C2 `index_layer = aggregated` | `gates.py` | ✅ |
| C2 không chuỗi "JobPosting" trong HTML | `build.py` | chỉ bản tĩnh¹ |
| C3 chỉ tin đang mở | `gates.py` | ✅ |
| C4 trích đoạn ≤300 ký tự | `gates.py` | ✅ |
| C5 không xung đột với schema công ty khai | `gates.py` | ✅ |

¹ Bản Next.js không có mã nào phát sinh JSON-LD, nên không có gì để kiểm ở đầu ra. Nếu sau
này thêm structured data, phải thêm bước kiểm tương đương.

**Đã đối kháng.** Sáu ca cố ý làm hỏng dữ liệu — mất trích dẫn, trích dẫn vô nghĩa, trích
đoạn 301 ký tự, xung đột C5, tin đã đóng, sai `index_layer` — cả sáu đều bị chặn, và cả hai
luồng thoát mã 1 mà **không sinh đầu ra nào**. Dữ liệu sạch vẫn qua.

`TRIGGER` trong `gates.py` phải theo kịp `score_rules.DQ`: thêm luật mới mà quên thêm từ
vựng thì C1 sẽ chặn build với trích dẫn hoàn toàn hợp lệ. Đã xảy ra một lần khi thêm các
luật L4/L5.
