#!/usr/bin/env python3
"""Đọc danh sách doanh nghiệp CÓ GIẤY PHÉP dịch vụ việc làm do Sở công bố.

Dùng cho Đ2 (legal-options.md Mục 3): hợp tác với doanh nghiệp đã có giấy phép
là đường duy nhất chạy được ngay mà không cần 300 triệu ký quỹ và không phải
chờ hai câu pháp lý còn mở.

NĐ 352/2025 Điều 13.3 buộc cơ quan cấp phép đăng công khai Giấy phép trên cổng
thông tin của mình và trên Sàn giao dịch việc làm quốc gia — nên danh sách này
là nguồn công khai, không phải dữ liệu moi được.

Đọc xlsx bằng thư viện chuẩn (xlsx là zip chứa XML). Không cài thêm gói nào.

    python3 tools/licensed_partners.py ds.xlsx            # in ra
    python3 tools/licensed_partners.py ds.xlsx --csv > partners.csv

CẢNH BÁO: tệp Sở đăng có NGÀY CHỐT. Giấy phép có hạn tối đa 60 tháng và có thể
bị thu hồi, nên danh sách chỉ là ĐIỂM BẮT ĐẦU — phải xác minh còn hiệu lực
trước khi ký bất cứ gì.
"""
import argparse
import csv
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# Từ khoá gợi ý doanh nghiệp có khả năng hợp tác về mảng IT/quốc tế. Chỉ là
# GỢI Ý ĐỌC TRƯỚC — không lọc bỏ ai, vì tên công ty nói rất ít về việc họ làm.
HINT = re.compile(
    r"recruit|talent|staffing|human|hr\b|resource|persol|manpower|navigos|adecco|"
    r"robert|michael page|first alliances|hays|tech|it\b|software|digital|global|"
    r"international|nhân sự|nhân lực|nhân tài|tuyển dụng|công nghệ", re.I)


def cells(z, sheet_path, shared):
    for row in ET.fromstring(z.read(sheet_path)).findall(f".//{NS}row"):
        out = {}
        for c in row.findall(f"{NS}c"):
            col = re.match(r"([A-Z]+)", c.get("r", "A1")).group(1)
            v = c.find(f"{NS}v")
            if v is not None and v.text is not None:
                out[col] = (shared[int(v.text)] if c.get("t") == "s" else v.text).strip()
        if out:
            yield out


def parse(path):
    z = zipfile.ZipFile(path)
    shared = ["".join(t.text or "" for t in si.iter(f"{NS}t"))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(f"{NS}si")]

    # Sổ có nhiều sheet (chi nhánh, trung tâm công lập…). Lấy sheet NÀO CÓ hàng
    # tiêu đề đúng, thay vì đoán theo tên hay theo thứ tự — tên sheet đổi mỗi kỳ.
    for name in sorted(n for n in z.namelist()
                       if re.match(r"xl/worksheets/sheet\d+\.xml$", n)):
        rows = list(cells(z, name, shared))
        head = next((i for i, r in enumerate(rows)
                     if "Tên doanh nghiệp" in " ".join(r.values())), None)
        if head is None:
            continue
        cols = {v: k for k, v in rows[head].items()}
        col = lambda *names: next((cols[n] for n in names if n in cols), None)
        c_name = col("Tên doanh nghiệp")
        c_tax = col("Mã số doanh nghiệp", "MST")
        c_addr = col("Địa chỉ")
        c_lic = next((v for k, v in cols.items() if "Số GP" in k or "Giấy phép" in k), None)

        out = []
        for r in rows[head + 1:]:
            nm = (r.get(c_name) or "").strip()
            if not nm or nm.lower().startswith(("tổng", "ghi chú")):
                continue
            out.append({
                "company": nm,
                "tax_id": r.get(c_tax, ""),
                "license": r.get(c_lic, "") if c_lic else "",
                "address": (r.get(c_addr, "") or "")[:90],
                "fit_hint": "yes" if HINT.search(nm) else "",
            })
        if out:
            return out
    return []


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx")
    ap.add_argument("--csv", action="store_true")
    a = ap.parse_args()

    rows = parse(a.xlsx)
    if not rows:
        print("không tìm thấy sheet nào có cột 'Tên doanh nghiệp'", file=sys.stderr)
        return 1

    if a.csv:
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
        return 0

    hinted = [r for r in rows if r["fit_hint"]]
    print(f"\n  {len(rows)} doanh nghiệp có giấy phép · {len(hinted)} khớp từ khoá nhân sự/IT")
    print("  Giấy phép có hạn tối đa 60 tháng — XÁC MINH CÒN HIỆU LỰC trước khi ký.\n")
    print(f"  {'Doanh nghiệp':<52} {'MST':<12} Giấy phép")
    print("  " + "-" * 96)
    for r in hinted:
        print(f"  {r['company'][:51]:<52} {r['tax_id']:<12} {r['license'][:30]}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
