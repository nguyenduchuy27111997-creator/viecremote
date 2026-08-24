-- Vệ sinh dữ liệu NGƯỜI DÙNG hằng ngày — mọi lời hứa xoá trên site thi hành ở đây.
-- An toàn khi bảng rỗng.
--
-- Không phải dọn dẹp cho gọn. Đây là NGHĨA VỤ:
--
--   Điều 25.1.c Luật 91/2025 — "Phải xóa, hủy thông tin đã cung cấp của người
--   dự tuyển trong trường hợp không tuyển dụng, trừ trường hợp có thỏa thuận
--   khác với người đã dự tuyển."
--
--   C8 (prd.md Mục 5.2) — rút lui = xoá hẳn trong 24h.
--
-- `tools/gates_l2.py` PHÁT HIỆN quá hạn và làm đỏ build. Tệp này là thứ duy
-- nhất làm nó xanh lại. Thiếu một trong hai thì cái còn lại vô nghĩa.

-- 1. Đồng ý đã rút quá 24h. Xoá bản ghi đồng ý, không xoá kỹ sư — rút đồng ý
--    cho MỘT công ty khác với rút khỏi mạng lưới.
--    transfer trỏ tới consent kèm ON DELETE CASCADE, nên lần chuyển giao gắn
--    với đồng ý này đi theo. Vết cho thanh tra đã nằm ở transfer_audit.
DELETE FROM consent
WHERE revoked_at IS NOT NULL
  AND revoked_at < datetime('now', '-24 hours');

-- 2. Hồ sơ hết hạn giữ. purge_after do luồng ghi đặt lúc tạo, theo thoả thuận
--    với chính kỹ sư — mặc định là "không tuyển thì xoá".
--    CASCADE cuốn theo consent, và consent cuốn theo transfer.
DELETE FROM engineer
WHERE purge_after < datetime('now');

-- 3. Kỹ sư không còn đồng ý nào còn hiệu lực thì không còn cơ sở pháp lý để
--    giữ dữ liệu. Giữ tiếp là xử lý dữ liệu không có căn cứ.
--    Chừa 24h để phân biệt "vừa rút cái cuối" với "chưa kịp đồng ý cái nào".
DELETE FROM engineer
WHERE created_at < datetime('now', '-24 hours')
  AND id NOT IN (SELECT engineer_id FROM consent WHERE revoked_at IS NULL);

-- 4. Email ghi danh CHƯA XÁC NHẬN quá 7 ngày. Thư xác nhận hứa nguyên văn:
--    "địa chỉ của bạn sẽ bị xoá sau 7 ngày" — không có câu lệnh này thì đó là
--    lời hứa suông, và một địa chỉ email chưa xác nhận là dữ liệu cá nhân đang
--    được giữ không có cơ sở (chủ nhân có thể chưa từng đăng ký — ai đó gõ hộ).
DELETE FROM subscriber
WHERE confirmed = 0
  AND created_at < datetime('now', '-7 days');
