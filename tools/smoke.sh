#!/usr/bin/env bash
# Kiểm khói sau deploy — MỘT nguồn sự thật cho cả hai đường deploy.
#
#     tools/smoke.sh https://viec-remote.….workers.dev
#
# Vì sao tách riêng: deploy.sh (chạy tay) và refresh.yml (cron 22:17 UTC) cùng
# deploy production, nhưng kiểm khói từng chỉ sống trong deploy.sh — nghĩa là
# cron deploy MÙ, một lần refresh hỏng là site chết tới sáng mà không ai biết.
# Hai bản kiểm chép tay sẽ lệch nhau ngay lần thêm trang đầu tiên; một tệp thì
# không lệch được.
#
# Bản vừa deploy cần vài giây để lan ra biên. Không chờ thì kiểm khói báo 404
# cho trang HOÀN TOÀN đúng — đã dính hai lần. Thử lại vài nhịp trước khi kết
# luận hỏng; cổng chỉ có giá trị khi nó không kêu oan.
set -u

URL="${1:?dùng: tools/smoke.sh <url-gốc>}"
URL="${URL%/}"

# Mỗi đường một trang đại diện: tiếng Việt tĩnh, tiếng Việt động (D1),
# tiếng Anh khu vực, tiếng Anh thị trường chấm được + chưa chấm, gương soi,
# API, và hai tệp cho máy đọc.
PAGES=(/ /tin-mo /thay-doi /khoa /lam-gi /phuong-phap /rieng-tu /api
       /hiring-in-sea /hiring-in-sea/changes /hiring-in-sea/vietnam /hiring-in-sea/philippines
       /company/snowflake /sitemap.xml /robots.txt)

probe() { # url mã-mong-đợi
    local code=""
    for _ in 1 2 3 4 5 6; do
        code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 25 "$1")
        [ "$code" = "$2" ] && { printf '%s' "$code"; return 0; }
        sleep 4
    done
    printf '%s' "$code"
    return 1
}

FAIL=0
for p in "${PAGES[@]}"; do
    if CODE=$(probe "$URL$p" 200); then
        printf '  %-32s 200\n' "$p"
    else
        printf '  %-32s %s  ← hỏng\n' "$p" "$CODE"
        FAIL=1
    fi
done

# Trang không tồn tại PHẢI trả 404. Trả 200 thì Google lập chỉ mục rác.
if CODE=$(probe "$URL/khong-co-trang-nay" 404); then
    printf '  %-32s 404 (mong đợi 404)\n' "/404"
else
    printf '  %-32s %s  ← phải là 404\n' "/404" "$CODE"
    FAIL=1
fi

if [ "$FAIL" != "0" ]; then
    echo "✗ kiểm khói thất bại — xem log Worker trên dashboard" >&2
    exit 1
fi
echo "  ✓ tất cả xanh"
