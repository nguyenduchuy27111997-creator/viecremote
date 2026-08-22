#!/usr/bin/env bash
# Deploy L1 (tầng minh bạch) lên Cloudflare Workers.
#
# CHẠY MỘT LẦN, hoặc chạy lại bao nhiêu lần cũng được — mọi bước đều idempotent.
# Đứt giữa chừng thì chạy lại, nó bỏ qua phần đã xong.
#
#   ./deploy.sh                       # dùng tên miền mặc định trong site.ts
#   SITE_URL=https://abc.com ./deploy.sh
#
# TRƯỚC KHI CHẠY, một lần duy nhất:
#   cd web && npx wrangler login
#
# L1 KHÔNG cần pháp nhân hay ký quỹ: nó không giới thiệu ai cho ai, không thu
# hồ sơ, không thu phí — chưa phải dịch vụ việc làm. Xem prd.md Mục 1.
set -uo pipefail
cd "$(dirname "$0")"

say()  { printf '\n\033[1m[%s] %s\033[0m\n' "$(date +%H:%M:%S)" "$*"; }
die()  { printf '\n\033[31mDỪNG: %s\033[0m\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- 0. kiểm tra
say "0/6  Kiểm điều kiện"

command -v node    >/dev/null || die "chưa có node"
command -v python3 >/dev/null || die "chưa có python3"
[ -f jobs.json ]              || die "không có jobs.json — chạy: python3 tools/export_jobs.py"

cd web
npx wrangler whoami >/dev/null 2>&1 \
  || die "chưa đăng nhập Cloudflare. Chạy: cd web && npx wrangler login"
echo "  ✓ đã đăng nhập: $(npx wrangler whoami 2>/dev/null | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+' | head -1)"
cd ..

# ---------------------------------------------------- 1. dữ liệu + cổng C1..C5
say "1/6  Xuất dữ liệu (kèm cổng C1..C5)"
# export_db.py gọi tools/gates.py. Vi phạm ⇒ exit 1 ở đây, trước khi chạm
# production. Thà không deploy còn hơn deploy nhãn sai.
python3 tools/export_db.py || die "vi phạm ràng buộc hoặc xuất DB thất bại"

# ------------------------------------------------------------- 2. tạo D1 (1 lần)
say "2/6  Cơ sở dữ liệu D1"
cd web
DBID=$(grep -oE '"database_id"[[:space:]]*:[[:space:]]*"[^"]*"' wrangler.jsonc | grep -oE '"[^"]*"$' | tr -d '"')

if [ "$DBID" = "PLACEHOLDER" ] || [ -z "$DBID" ]; then
    echo "  chưa có, tạo mới…"
    OUT=$(npx wrangler d1 create viec-remote 2>&1) || {
        # Đã tồn tại từ lần chạy trước? Lấy id ra dùng lại.
        OUT=$(npx wrangler d1 info viec-remote 2>&1) \
            || die "không tạo được D1: $OUT"
    }
    NEWID=$(echo "$OUT" | grep -oiE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
    [ -n "$NEWID" ] || die "không đọc được database_id từ:\n$OUT"
    python3 - "$NEWID" <<'PY'
import re, sys
p = "wrangler.jsonc"
s = open(p, encoding="utf-8").read()
s = re.sub(r'("database_id"\s*:\s*)"[^"]*"', r'\1"%s"' % sys.argv[1], s)
open(p, "w", encoding="utf-8").write(s)
PY
    echo "  ✓ tạo xong, đã ghi id vào wrangler.jsonc: $NEWID"
else
    echo "  ✓ đã có: $DBID"
fi

# ------------------------------------------------------------------ 3. nạp seed
# Tệp CUỐI là bước hoán đổi (DROP + RENAME). Đứt trước nó ⇒ dữ liệu cũ còn
# nguyên và bảng `report`/`subscriber` do người dùng ghi KHÔNG mất.
say "3/6  Nạp dữ liệu vào D1 (local để build, remote để chạy)"
for scope in local remote; do
    echo "  → $scope"
    for f in ../data/seed-*.sql; do
        npx wrangler d1 execute viec-remote "--$scope" --file="$f" -y >/dev/null 2>&1 \
            || die "nạp thất bại ở $f (--$scope)"
    done
done
echo "  ✓ $(ls ../data/seed-*.sql | wc -l | tr -d ' ') tệp, cả hai môi trường"

# ---------------------------------------------------------------- 4. build + deploy
say "4/6  Build và deploy"
npm ci --silent || die "npm ci thất bại"
export NEXT_PUBLIC_SITE_URL="${SITE_URL:-${NEXT_PUBLIC_SITE_URL:-}}"
npx opennextjs-cloudflare build  || die "build thất bại"
npx opennextjs-cloudflare deploy || die "deploy thất bại"

# --------------------------------------------------------------- 5. kiểm khói
say "5/6  Kiểm khói trên bản vừa deploy"
URL="${SITE_URL:-}"
if [ -z "$URL" ]; then
    URL=$(npx wrangler deployments list 2>/dev/null \
          | grep -oE 'https://[a-z0-9.-]+\.workers\.dev' | head -1)
fi

if [ -z "$URL" ]; then
    echo "  ! không tự tìm được URL — kiểm tay trên dashboard"
else
    FAIL=0
    for p in / /tin-mo /khoa /lam-gi /phuong-phap /rieng-tu /api /sitemap.xml /robots.txt; do
        CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 25 "$URL$p")
        printf '  %-16s %s\n' "$p" "$CODE"
        [ "$CODE" = "200" ] || FAIL=1
    done
    # Trang không tồn tại PHẢI trả 404. Trả 200 thì Google lập chỉ mục rác.
    CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 25 "$URL/khong-co-trang-nay")
    printf '  %-16s %s (mong đợi 404)\n' "/404" "$CODE"
    [ "$CODE" = "404" ] || FAIL=1
    [ "$FAIL" = "0" ] || die "kiểm khói thất bại — xem log Worker trên dashboard"
    echo "  ✓ tất cả xanh"
fi

# ------------------------------------------------------------------ 6. còn lại
say "6/6  Xong"
cat <<EOF

  Trang đang chạy: ${URL:-<xem dashboard>}

  CÒN PHẢI LÀM TAY (không tự động được):

  1. Tên miền
     Dashboard → Workers → viec-remote → Settings → Domains & Routes
     Rồi đặt lại: SITE_URL=https://<tên miền> ./deploy.sh

  2. Analytics — KHÔNG có thì cổng "500 người dùng sau 30 ngày" không bấm được
     Dashboard → Analytics → Web Analytics → lấy token
     Đặt vào web/.env.local:  NEXT_PUBLIC_CF_ANALYTICS_TOKEN=<token>
     Rồi chạy lại deploy.sh

  3. Cập nhật hằng ngày — chọn MỘT:
     a) GitHub Actions (khuyến nghị, máy không cần bật):
        push repo, đặt secret CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID
     b) cron trên máy này:
        (crontab -l 2>/dev/null; echo "17 5 * * * cd $PWD && ./refresh.sh --deploy >> logs/refresh.log 2>&1") | crontab -

  CHƯA BẬT, và đó là chủ ý:
     - Gửi thư xác nhận đăng ký: cần onboard tên miền vào Cloudflare Email Sending.
       Chưa có thì form vẫn lưu email nhưng KHÔNG gửi xác nhận được.
     - Turnstile chống spam: cd web && npx wrangler secret put TURNSTILE_SECRET
       Chưa có thì honeypot + kiểm thời gian vẫn chạy.
     - L2 (mạng lưới): KHOÁ, chờ luật sư. Xem prd.md Mục 2.

EOF
