#!/usr/bin/env python3
"""
Đọc bảng chấm đã điền -> sáu con số của Cổng 0.1 + phán quyết cổng.

    python3 tools/tally.py [scoring-sheet.csv]

Cột cần điền (xem tools/README.md):
  DQ            x nếu bị loại trừ
  tier          A | B | unknown | no
  tier_a_scope  vn | global      (chỉ khi tier=A)
  has_alr       y | n            (có applicantLocationRequirements không)
  on_free_board y | n            (đã có trên Real Work From Anywhere / TrulyRemoteWork)
  minutes       số phút chấm tin này
"""
import csv, sys
from collections import Counter

path = sys.argv[1] if len(sys.argv) > 1 else "scoring-sheet.csv"
rows = [r for r in csv.DictReader(open(path, encoding="utf-8-sig"))]
scored = [r for r in rows if (r.get("tier") or "").strip()]

if not scored:
    sys.exit(f"Chưa có dòng nào điền cột 'tier' trong {path}.")

n = len(scored)
g = lambda r, k: (r.get(k) or "").strip().lower()
tier = Counter(g(r, "tier") for r in scored)
a_rows = [r for r in scored if g(r, "tier") == "a"]
a_vn = sum(1 for r in a_rows if g(r, "tier_a_scope").startswith("vn"))
a_gl = len(a_rows) - a_vn
pct = lambda x: 100.0 * x / n

mins = [float(r["minutes"]) for r in scored if (r.get("minutes") or "").strip().replace(".", "", 1).isdigit()]
alr = [r for r in scored if g(r, "has_alr") in ("y", "n")]
alr_y = sum(1 for r in alr if g(r, "has_alr") == "y")
ofb = [r for r in a_rows if g(r, "on_free_board") in ("y", "n")]
ofb_y = sum(1 for r in ofb if g(r, "on_free_board") == "y")

print(f"\nCỔNG 0.1 — {n} tin đã chấm (trong tổng {len(rows)} dòng)\n" + "=" * 58)
print(f"  1. Tier A-VN            {a_vn:>4}  {pct(a_vn):>5.1f}%   <- SỐ QUYẾT ĐỊNH")
print(f"  2. Tier A-Global        {a_gl:>4}  {pct(a_gl):>5.1f}%")
print(f"     Tier B               {tier['b']:>4}  {pct(tier['b']):>5.1f}%")
print(f"  3. Không rõ             {tier['unknown']:>4}  {pct(tier['unknown']):>5.1f}%")
print(f"     Loại trừ (no)        {tier['no']:>4}  {pct(tier['no']):>5.1f}%")
print(f"  4. Phút/tin             {sum(mins)/len(mins):>9.1f}" if mins else "  4. Phút/tin                   — (chưa điền)")
if mins:
    print(f"     -> 100 tin/tuần = {sum(mins)/len(mins)*100/60:.1f} giờ/tuần chỉ để chấm")
print(f"  5. Có applicantLocationRequirements  {alr_y}/{len(alr)}" + (f"  ({100*alr_y/len(alr):.0f}%)" if alr else "  — (chưa điền)"))
print(f"  6. Tier A đã có trên board miễn phí  {ofb_y}/{len(ofb)}" + (f"  ({100*ofb_y/len(ofb):.0f}%)" if ofb else "  — (chưa điền)"))

# cảnh báo lệch nguồn — ảnh hưởng trực tiếp tới độ tin của tỷ lệ cơ sở
plat = Counter(g(r, "platform") for r in scored)
top, topn = plat.most_common(1)[0]
if topn / n > 0.6:
    print(f"\n  ! LỆCH NGUỒN: {100*topn/n:.0f}% mẫu từ {top}. Tỷ lệ cơ sở tính ra")
    print(f"     phản ánh {top} nhiều hơn phản ánh thị trường. Thêm slug nền tảng khác")
    print("     trước khi coi con số là kết luận.")

print("\nPHÁN QUYẾT\n" + "-" * 58)
p = pct(a_vn)
if p >= 5:      print(f"  Tier A-VN {p:.1f}% >= 5%   -> TIẾP TỤC theo kế hoạch")
elif p >= 2:    print(f"  Tier A-VN {p:.1f}% trong 2-5% -> TIẾP TỤC, thu hẹp ngách,\n     hạ kỳ vọng doanh thu về kịch bản Xấu (BRD 11.2)")
else:           print(f"  Tier A-VN {p:.1f}% < 2%    -> DỪNG. Không có gì để xây mà chưa tồn tại")

if pct(tier["unknown"]) > 60:
    print(f"  ! 'Không rõ' {pct(tier['unknown']):.0f}% > 60% -> bài toán là ĐIỀU TRA, không phải LỌC.")
    print("     Mô hình chi phí sai hoàn toàn. Đọc lại PRD M5 (kịch bản đảo vai).")
if a_gl > a_vn * 2 and a_vn > 0:
    print("  ! Tier A gần như toàn Global -> đang định làm bản sao của thứ miễn phí (BRD 5.1).")
if ofb and ofb_y / len(ofb) > 0.5:
    print(f"  ! {100*ofb_y/len(ofb):.0f}% tin Tier A đã có trên board miễn phí -> khác biệt không nằm ở tầng lọc.")
if mins and sum(mins)/len(mins)*100/60 > 6:
    print("  ! Chấm tay vượt quỹ thời gian. Tự động hoá là bắt buộc, không phải tuỳ chọn.")
print()
