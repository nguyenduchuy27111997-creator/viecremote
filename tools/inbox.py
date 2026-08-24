#!/usr/bin/env python3
"""Hộp thư vận hành — đọc những gì site thu được trên production D1.

Ba bảng do NGƯỜI DÙNG ghi (inquiry, report, subscriber) nằm trên D1 production,
ngoài kho dựng lại hằng ngày. Không có công cụ này thì cách duy nhất để biết có
khách Đ3 gửi yêu cầu là tự gõ SQL — nghĩa là không ai biết, và phễu thu đổ vào
hố đen. Khách trả tiền đầu tiên không đáng bị phát hiện muộn một tuần.

    python3 tools/inbox.py                # xem mọi thứ đang chờ
    python3 tools/inbox.py --handle 3     # đánh dấu inquiry #3 đã xử lý
    python3 tools/inbox.py --resolve 7    # đánh dấu báo sai #7 đã giải quyết

Chạy qua wrangler nên cần đã `npx wrangler login` (giống deploy.sh).
Chỉ đọc và cập nhật cờ — không xoá gì; xoá dữ liệu người dùng là việc phải
làm chậm và có chủ ý, không phải một cờ tiện tay.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "web"


def d1(sql):
    r = subprocess.run(
        ["npx", "wrangler", "d1", "execute", "viec-remote", "--remote",
         "--json", "--command", sql],
        cwd=WEB, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"wrangler lỗi:\n{r.stderr.strip()[:400]}")
    return json.loads(r.stdout)[0]["results"]


def show():
    iq = d1("SELECT id, company, email, role, note, created_at FROM inquiry "
            "WHERE handled = 0 ORDER BY created_at")
    rp = d1("SELECT id, kind, ref, reason, note, created_at FROM report "
            "WHERE resolved = 0 ORDER BY created_at")
    sub = d1("SELECT count(*) n, sum(confirmed) c FROM subscriber")[0]

    print(f"\n{'='*74}")
    print(f"  YÊU CẦU BÁO CÁO (Đ3) — {len(iq)} đang chờ")
    print(f"{'='*74}")
    if not iq:
        print("  (trống)")
    for r in iq:
        print(f"\n  #{r['id']}  {r['created_at'][:16]}  {r['company']}")
        print(f"      {r['email']}" + (f"  ·  tuyển: {r['role']}" if r['role'] else ""))
        if r["note"]:
            print(f"      “{r['note'][:160]}”")
    if iq:
        print(f"\n  -> trả lời email rồi: python3 tools/inbox.py --handle <id>")

    print(f"\n{'='*74}")
    print(f"  BÁO SAI NHÃN — {len(rp)} đang chờ")
    print(f"{'='*74}")
    if not rp:
        print("  (trống)")
    for r in rp:
        print(f"\n  #{r['id']}  {r['created_at'][:16]}  [{r['kind']}] {r['ref']}")
        print(f"      lý do: {r['reason']}" + (f"  ·  “{r['note'][:120]}”" if r['note'] else ""))
    if rp:
        print(f"\n  -> kiểm tin gốc, sửa nếu đúng, rồi: python3 tools/inbox.py --resolve <id>")

    n, c = sub["n"] or 0, sub["c"] or 0
    print(f"\n  Ghi danh nhận tin: {n} địa chỉ · {c} đã xác nhận")
    print()


def flag(table, col, rid):
    d1(f"UPDATE {table} SET {col} = 1 WHERE id = {int(rid)}")
    left = d1(f"SELECT count(*) n FROM {table} WHERE {col} = 0")[0]["n"]
    print(f"  ✓ {table} #{rid} đã đánh dấu · còn {left} đang chờ")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--handle", type=int, metavar="ID", help="inquiry đã xử lý")
    ap.add_argument("--resolve", type=int, metavar="ID", help="báo sai đã giải quyết")
    a = ap.parse_args()

    if a.handle is not None:
        flag("inquiry", "handled", a.handle)
    elif a.resolve is not None:
        flag("report", "resolved", a.resolve)
    else:
        show()


if __name__ == "__main__":
    main()
