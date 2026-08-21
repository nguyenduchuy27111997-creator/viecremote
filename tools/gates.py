#!/usr/bin/env python3
"""
Năm cổng chặn xuất bản — C1..C5.

Đặt ở đây, không đặt trong build.py, vì có HAI luồng xuất bản dùng chung dữ
liệu: `build.py` (trang tĩnh) và `tools/export_db.py` (Next.js + D1). Nếu mỗi
luồng tự kiểm, hai bên sẽ trôi khỏi nhau và luồng nào lỏng hơn sẽ là luồng
lên production.

    from gates import validate
    err = validate(jobs)
    if err: dừng, in ra, exit(1)

C2 có hai nửa: nửa dữ liệu (`index_layer`) kiểm ở đây; nửa đầu ra (không có
chuỗi "JobPosting" trong HTML) chỉ kiểm được sau khi dựng, nằm ở build.py.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import country as C

EXCERPT_MAX = 300

# Trích dẫn phải chứa ít nhất một cụm lý giải được nhãn. Không có thì trích dẫn
# đó vô nghĩa với người đọc — và thường là dấu hiệu cửa sổ trích bị cắt lệch.
# Từ vựng ở đây PHẢI theo kịp score_rules.DQ; thêm luật mới thì thêm từ vào đây.
TRIGGER = re.compile(
    r"anywhere|worldwide|global|any location|any country|location[- ]independent|"
    r"APAC|APJ|Asia[- ]Pacific|Southeast Asia|vi[eệ]t ?nam|\bVN\b|remote|distributed|"
    r"\bA-0\d\b|\bDQ-0\d\b|only|must|require|reside|resident|located|location|based in|"
    r"citizen|clearance|\bITAR\b|\bCUI\b|export control|licen[sc]|state[- ]specific|"
    r"hybrid|office|on.?site|in.?person|relocat|commut|stipend|"
    r"authoriz|permit|visa|sponsorship|eligib|\bwork in the\b|\bwork from\b|"
    r"\bW-?2\b|\b1099\b|PAYE|payroll|contractor|"
    r"time ?zone|overlap|\b(?:P|E|C|M)(?:S|D)T\b|\bCET\b|\bCEST\b|\bGMT\b|\bUTC\b|"
    r"Central hours|Pacific|Eastern|core hours|\bclient\b|agency|"
    r"(?:Pacific|Eastern|Central|Mountain) Time|\b(?:EET|EEST|BST|IST|JST|AEST)\b|"
    r"looking for (?:someone|candidates?|a candidate)|candidates? in|"
    r"applicants? (?:from|in)|\bLATAM\b|\bEMEA\b|\bU\.S\.", re.I)


def validate(jobs):
    """-> danh sách chuỗi vi phạm. Rỗng nghĩa là qua cả năm cổng."""
    err = []
    for j in jobs:
        ev = (j.get("evidence") or "").strip()

        # C1 — mọi nhãn phải có trích dẫn nguyên văn lý giải được nó.
        if j["eligibility"] != "unknown":
            if not ev:
                err.append(f"C1 {j['id']}: nhãn '{j['eligibility']}' không có trích dẫn")
            elif not TRIGGER.search(ev):
                err.append(f"C1 {j['id']}: trích dẫn không lý giải nhãn: {ev[:70]!r}")

        # C2 (nửa dữ liệu) — không bao giờ tự nhận là nguồn gốc của tin.
        if j.get("index_layer") != "aggregated":
            err.append(f"C2 {j['id']}: index_layer != aggregated")

        # C3 — tin đã đóng không được nằm trong dữ liệu xuất bản.
        if j.get("status") != "open":
            err.append(f"C3 {j['id']}: tin không mở mà vẫn nằm trong dữ liệu")

        # C4 — bản quyền: trích đoạn có trần cứng.
        if len(j.get("excerpt") or "") > EXCERPT_MAX:
            err.append(f"C4 {j['id']}: trích đoạn {len(j['excerpt'])} > {EXCERPT_MAX}")

        # C5 — không được gán 'mở toàn cầu' khi chính công ty khai danh sách
        # nước nhận ứng viên mà không có Việt Nam. Đây là dương tính giả đắt nhất.
        if j["eligibility"] == "worldwide" and j.get("alr_countries"):
            if C.verdict("; ".join(j["alr_countries"]))[0] == "no":
                err.append(f"C5 {j['id']}: gán 'mở toàn cầu' nhưng công ty khai "
                           f"{j['alr_countries']} — không có Việt Nam")
    return err


def enforce(jobs, where):
    """Kiểm và DỪNG nếu vi phạm. Dùng ở mọi luồng xuất bản."""
    err = validate(jobs)
    if err:
        print(f"{where} DỪNG — {len(err)} vi phạm ràng buộc:", file=sys.stderr)
        for e in err[:20]:
            print("  " + e, file=sys.stderr)
        if len(err) > 20:
            print(f"  … và {len(err)-20} vi phạm nữa", file=sys.stderr)
        sys.exit(1)
    print("   C1 trích dẫn ✓  C2 index_layer ✓  C3 chỉ tin đang mở ✓  "
          f"C4 trích đoạn ≤{EXCERPT_MAX} ✓  C5 không xung đột schema ✓")
