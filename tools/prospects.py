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


def rows(db, where, limit):
    q = f"""SELECT name, mechanism, verdict, n_jobs, locked
            FROM company
            WHERE mechanism <> 'unknown' AND {where}
            ORDER BY n_jobs DESC LIMIT ?"""
    out = []
    for name, mech, verdict, n, locked in db.execute(q, (limit,)):
        where_list = [c for c, _ in json.loads(locked or "[]")]
        out.append({
            "company": name,
            "mechanism": mech,
            "postings": n,
            "evidence": "clause excludes VN" if verdict == "no" else "no clause found",
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
    data = rows(db, "verdict='ok'" if a.proof else "verdict IN ('no','unk')", a.n)
    if not a.proof:
        data.sort(key=lambda r: (r["evidence"] != "clause excludes VN", -r["postings"]))
    db.close()

    if a.csv:
        w = csv.DictWriter(sys.stdout, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)
        return

    title = "ĐÃ MỞ CHO VIỆT NAM — dùng làm bằng chứng, không phải người mua" \
        if a.proof else "MỤC TIÊU — có bộ máy xuyên biên giới, chưa dùng ở Việt Nam"
    print(f"\n{title}\n")
    print(f"{'Company':<24} {'Mech':<11} {'Jobs':>5}  {'Evidence':<19} Already hires in")
    print("-" * 108)
    for r in data:
        print(f"{r['company'][:23]:<24} {r['mechanism']:<11} {r['postings']:>5}  "
              f"{r['evidence']:<19} {r['hires_in']}")
    print()


if __name__ == "__main__":
    main()
