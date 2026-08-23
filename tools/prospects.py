"""Danh sách chào hàng Đ3 — công ty đã có cơ chế tuyển xuyên biên giới.

Hai danh sách khác nhau, đừng gộp:

  --targets  (mặc định)  Công ty có EOR/contractor NHƯNG loại Việt Nam.
                         Đây là người mua: họ đã trả tiền cho bộ máy tuyển
                         xuyên biên giới rồi mà không dùng được ở Việt Nam.
  --proof                Công ty có EOR/contractor VÀ đã mở cho Việt Nam.
                         Đây KHÔNG phải người mua — họ không thiếu gì. Dùng
                         làm bằng chứng trong thư: "những công ty này đã làm".

Phân biệt verdict:
  no   = có mệnh đề trích dẫn được loại Việt Nam  -> chào được, có cứ liệu
  unk  = KHÔNG có mệnh đề nào                     -> không biết, đừng khẳng định

Chỉ đọc dữ liệu tổ chức. Không chạm dữ liệu cá nhân — xem legal-options.md Mục 3.

Chạy:  python3 tools/prospects.py           # 15 mục tiêu hàng đầu
       python3 tools/prospects.py --proof
       python3 tools/prospects.py -n 40 --csv
"""
import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "app.db"


# Đông Nam Á — tín hiệu mạnh nhất tìm được trong kho (23/08).
#
# Công ty đã tuyển ở PH/ID/TH/MY mở cho Việt Nam ở tỉ lệ 18,4% so với nền 2,5%
# — lift 7,3×. Mạnh gấp ba mọi khu vực khác: Ấn Độ 2,4×, Mỹ Latinh 2,6×,
# Đông Âu 4,1×. Giao với "đã khai EOR/contractor" cho 12,5×.
#
# Đã khử nhiễu cỡ công ty: chia bốn bậc theo số tin, lift giữ 3,3×–7,0× ở CẢ
# BỐN bậc. Đối chứng "công ty có mệnh đề khoá bất kỳ" chỉ 2,6% — bằng nền, nên
# đây không phải hiệu ứng "công ty nào chịu viết mệnh đề địa lý".
#
# Vì sao hợp lý: cùng dải múi giờ, cùng bậc chi phí, cùng kiểu hợp đồng nhà
# thầu. Công ty tuyển được ở Philippines đã giải xong đúng bài toán đó rồi.
SEA = {"PH", "ID", "TH", "MY"}


def rows(db, where):
    """Lấy HẾT rồi mới xếp và cắt ở tầng gọi.

    Cắt bằng SQL trước khi xếp theo tín hiệu ĐNA sẽ loại nhầm công ty ĐNA nhỏ —
    mà chính chúng mới là mục tiêu tốt, vì tín hiệu ĐNA giữ nguyên sức mạnh ở
    mọi bậc cỡ công ty (3,3×–7,0×)."""
    q = f"""SELECT name, mechanism, verdict, n_jobs, locked
            FROM company
            WHERE mechanism <> 'unknown' AND {where}"""
    out = []
    for name, mech, verdict, n, locked in db.execute(q):
        where_list = [c for c, _ in json.loads(locked or "[]")]
        sea = sorted(set(where_list) & SEA)
        out.append({
            "company": name,
            "mechanism": mech,
            "postings": n,
            "evidence": "clause excludes VN" if verdict == "no" else "no clause found",
            "sea": ", ".join(sea),
            "hires_in": ", ".join(where_list[:8]) or "—",
            "n_countries": len(where_list),
        })
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--proof", action="store_true", help="công ty ĐÃ mở cho VN")
    p.add_argument("-n", type=int, default=15)
    p.add_argument("--csv", action="store_true")
    p.add_argument("--db", default=str(DB))
    a = p.parse_args()

    db = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    # Mục tiêu xếp 'no' trước 'unk': chỉ 'no' mới có mệnh đề trích dẫn được để
    # mở đầu thư. Với 'unk' mà viết "bạn đang loại Việt Nam" là nói sai sự thật.
    data = rows(db, "verdict='ok'" if a.proof else "verdict IN ('no','unk')")
    data.sort(key=lambda r: -r["postings"])
    if not a.proof:
        # Đã tuyển ở ĐNA đứng TRƯỚC mệnh đề loại trừ: bằng chứng "bạn đã giải
        # bài này ở Philippines rồi" thuyết phục hơn "bạn có viết là loại VN".
        data.sort(key=lambda r: (not r["sea"],
                                 r["evidence"] != "clause excludes VN",
                                 -r["postings"]))
    data = data[:a.n]
    db.close()

    if a.csv:
        w = csv.DictWriter(sys.stdout, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)
        return

    title = "ĐÃ MỞ CHO VIỆT NAM — dùng làm bằng chứng, không phải người mua" \
        if a.proof else "MỤC TIÊU — có bộ máy xuyên biên giới, chưa dùng ở Việt Nam"
    print(f"\n{title}\n")
    print(f"{'Company':<24} {'Mech':<11} {'Jobs':>5}  {'SEA':<12} {'Evidence':<19} Already hires in")
    print("-" * 120)
    for r in data:
        print(f"{r['company'][:23]:<24} {r['mechanism']:<11} {r['postings']:>5}  "
              f"{(r['sea'] or '—'):<12} {r['evidence']:<19} {r['hires_in']}")
    print()


if __name__ == "__main__":
    main()
