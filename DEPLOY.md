# Deploy — việc bạn phải tự làm

Hai bước dưới đây cần tài khoản và thanh toán của bạn. Tôi không làm hộ được.

---

## 1. Cloudflare Pages — 0 đồng

Site là HTML tĩnh nên không cần máy chủ. Cloudflare Pages miễn phí, không giới hạn băng thông.

**Cách nhanh nhất (không cần Git):**

```bash
npx wrangler pages deploy site --project-name=viec-remote
```

Lần đầu sẽ mở trình duyệt để đăng nhập Cloudflare. Sau đó mỗi lần deploy chỉ chạy lại lệnh trên.

**Nếu muốn tự động deploy sau mỗi lần build:** thêm dòng cuối vào `refresh.sh`:

```bash
npx wrangler pages deploy site --project-name=viec-remote --commit-dirty=true
```

## 2. Tên miền — ~12 USD/năm

Mua ở đâu cũng được (Cloudflare Registrar bán đúng giá gốc, không đội giá năm sau).
Trỏ về Pages project trong phần **Custom domains**.

Gợi ý đặt tên: nói đúng việc trang làm, không cần sáng tạo.

---

## 3. Cron — chạy nếu bạn muốn

`refresh.sh` đã sẵn sàng. Tôi **không tự cài** vào crontab vì nó đổi cấu hình máy bạn.

```bash
(crontab -l 2>/dev/null; echo "17 5 * * * cd $PWD && ./refresh.sh >> logs/refresh.log 2>&1") | crontab -
```

Chạy 5:17 sáng mỗi ngày. Mất ~16 phút (chỉ kéo slug đến hạn, không kéo hết 5.535).

**An toàn đã cài sẵn:** nếu export lỗi hoặc build vi phạm ràng buộc C1–C4, script **khôi phục `jobs.json`
và giữ nguyên site cũ**. Thà site cũ một ngày còn hơn đẩy nhãn sai lên — đó là kiểu thất bại
"nặng" theo [MISSION.md](MISSION.md).

---

## 4. Trước khi deploy — một việc chưa xong

**Chưa xác nhận lại độ chính xác trên kho mới.**

Bộ đối chứng 180 tin lấy từ kho cũ (376 công ty lớn). Kho hiện tại 2.417 công ty, phần lớn
nhỏ và đuôi dài. Soi mẫu đã tìm ra **5 loại nhãn sai** mà bộ đối chứng cũ không chứa.

Đang chạy đợt chấm tay 40 tin từ kho mới. **Đợi kết quả đó rồi hãy deploy** — đẩy nhãn sai
lên tệ hơn không đẩy gì, vì nó tiêu đúng thứ sản phẩm hứa tiết kiệm.

Trang Phương pháp hiện đã nói thẳng giới hạn này thay vì giấu.
