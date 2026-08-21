#!/usr/bin/env bash
# Cập nhật hằng ngày: kéo slug đến hạn -> chấm nhãn -> cổng C1..C5 -> xuất DB -> dựng.
#
# Phân bậc poll (tools/tiering.py) chỉ kéo slug ĐẾN HẠN — khoảng 1.300/5.700
# mỗi ngày, ~16 phút, thay vì 110 phút nếu kéo hết.
#
# Nguyên tắc xuyên suốt: THÀ SITE CŨ MỘT NGÀY CÒN HƠN NHÃN SAI.
# Mọi bước hỏng đều khôi phục jobs.json và thoát mã 1, không đẩy gì lên.
#
# Cài vào cron (KHÔNG tự cài — chạy lệnh này nếu bạn muốn):
#   (crontab -l 2>/dev/null; echo "17 5 * * * cd $PWD && ./refresh.sh >> logs/refresh.log 2>&1") | crontab -
#
#   ./refresh.sh              # kéo + chấm + dựng, KHÔNG deploy
#   ./refresh.sh --deploy     # thêm nạp D1 từ xa + deploy Worker
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p logs
STAMP=$(date +%Y-%m-%d_%H%M)
DEPLOY=0
[ "${1:-}" = "--deploy" ] && DEPLOY=1

say()  { echo "[$(date +%H:%M:%S)] $*"; }
fail() {
    say "LỖI: $1 — giữ nguyên bản đang chạy"
    [ -f "logs/jobs-$STAMP.json.bak" ] && cp "logs/jobs-$STAMP.json.bak" jobs.json
    exit 1
}

say "=== bắt đầu $STAMP ==="

# Giữ bản trước để quay lại được nếu bất kỳ bước nào hỏng
[ -f jobs.json ] && cp jobs.json "logs/jobs-$STAMP.json.bak"

say "1/4 kéo + chấm nhãn (chỉ slug đến hạn)"
python3 -u tools/export_jobs.py -o jobs.json || fail "export thất bại"

# Cổng C1..C5 nằm trong tools/gates.py, cả hai luồng cùng gọi. export_db.py
# tự dừng nếu vi phạm, nên không cần kiểm riêng ở đây.
say "2/4 xuất SQLite + seed D1 (kèm cổng C1..C5)"
python3 -u tools/export_db.py || fail "vi phạm ràng buộc hoặc xuất DB thất bại"

say "3/4 dựng bản tĩnh (đường lui)"
python3 build.py || fail "build tĩnh vi phạm ràng buộc"

if [ "$DEPLOY" = "1" ]; then
    say "4/4 nạp D1 từ xa + deploy"
    for f in data/seed-*.sql; do
        (cd web && npx wrangler d1 execute viec-remote --remote --file="../$f") \
            || fail "nạp D1 thất bại ở $f"
    done
    (cd web && npx opennextjs-cloudflare build && npx opennextjs-cloudflare deploy) \
        || fail "deploy thất bại"
else
    say "4/4 bỏ qua deploy (thêm --deploy để đẩy lên)"
fi

# dọn bản sao lưu cũ hơn 14 ngày
find logs -name "jobs-*.json.bak" -mtime +14 -delete 2>/dev/null

say "xong. $(python3 -c "import json;d=json.load(open('jobs.json'));print(f'{len(d):,} tin')") · $(du -sh site | cut -f1) site"
say "=== kết thúc ==="
