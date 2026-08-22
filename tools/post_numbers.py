#!/usr/bin/env python3
"""
In các con số mà bài công bố dùng, lấy từ kho HIỆN TẠI.

Vì sao cần: kho đổi mỗi ngày. Bài trong content/ ghi cứng số liệu, và chỉ sau
một chu kỳ cập nhật là lệch (110 -> 103 công ty chỉ trong một ngày). Đăng số cũ
thì người đọc mở trang ra thấy số khác — mất đúng thứ duy nhất bài này bán.

    python3 tools/post_numbers.py          # in bảng đối chiếu
    python3 tools/post_numbers.py --check  # so với số trong content/, báo chỗ lệch
"""
import argparse, collections, json, re, sys

a = argparse.ArgumentParser()
a.add_argument("--jobs", default="jobs.json")
a.add_argument("--check", action="store_true")
a = a.parse_args()

d = [j for j in json.load(open(a.jobs, encoding="utf-8")) if j.get("status", "open") == "open"]
n = collections.Counter(j["eligibility"] for j in d)
sc = collections.Counter(
    ("vn" if re.match(r"A-0[13]\b", j["evidence"] or "") else "worldwide")
    if j["eligibility"] == "worldwide" else j["eligibility"] for j in d)
comp = collections.defaultdict(set)
for j in d:
    comp[j["company_slug"]].add(j["eligibility"])
ok = sum(1 for v in comp.values() if "worldwide" in v)

reasons = collections.Counter(j["exclusion_reason"] for j in d if j["eligibility"] == "excluded")
cs = collections.Counter()
for j in d:
    ev = j["evidence"] or ""
    if j["eligibility"] == "excluded" and ev.startswith("DQ-02(location)"):
        for c in (ev.split("|")[-1] or "").split("/"):
            if len(c) == 2:
                cs[c] += 1
mech = sum(1 for j in d if j.get("contract_mechanism") not in (None, "unknown"))

V = {
    "tin":        len(d),
    "cong_ty":    len(comp),
    "cong_ty_mo": ok,
    "cong_ty_khoa": sum(1 for v in comp.values() if v == {"excluded"}),
    "tin_mo":     n["worldwide"],
    "mo_toan_cau": sc["worldwide"],
    "mo_cho_vn":  sc["vn"],
    "bi_loai":    n["excluded"],
    "pc_loai":    100 * n["excluded"] / len(d),
    "pc_mo":      100 * n["worldwide"] / len(d),
    "pc_co_che":  100 * mech / len(d),
    "hybrid":     reasons["DQ-06"],
    "w2_paye":    reasons["DQ-03"],
    "mui_gio":    reasons["DQ-05"],
    "dia_ly":     reasons["DQ-02"],
    "quoc_tich":  reasons["DQ-04"],
    "giay_phep":  reasons["DQ-01"],
    "schema_no_vn": reasons["DQ-09"],
}

fmt = lambda x: f"{x:,.1f}".replace(",", ".").replace(".", ",", 1) if isinstance(x, float) \
    else f"{x:,}".replace(",", ".")

print("Số liệu cho bài công bố — lấy từ kho hiện tại\n")
for k, lab in [
    ("tin", "Tin remote đã chấm"), ("cong_ty", "Công ty"),
    ("cong_ty_mo", "Công ty tuyển được ở VN"), ("cong_ty_khoa", "Công ty khoá hoàn toàn"),
    ("tin_mo", "Tin mở"), ("mo_toan_cau", "  · mở toàn cầu"), ("mo_cho_vn", "  · mở cho VN"),
    ("bi_loai", "Bị giới hạn địa lý"), ("pc_loai", "  · phần trăm"),
    ("pc_mo", "Tin mở, phần trăm"), ("pc_co_che", "Tin nêu cơ chế, phần trăm"),
]:
    print(f"  {lab:<28} {fmt(V[k])}{'%' if k.startswith('pc_') else ''}")

print("\n  Rào cản:")
for k, lab in [("dia_ly", "khoá theo nước/vùng/bang"), ("hybrid", "phải có mặt tại văn phòng"),
               ("giay_phep", "cần giấy phép lao động"), ("quoc_tich", "quốc tịch / clearance"),
               ("schema_no_vn", "công ty tự khai, không có VN"),
               ("w2_paye", "W-2 / PAYE"), ("mui_gio", "bắt buộc múi giờ")]:
    print(f"    {fmt(V[k]):>7}  {lab}")

print("\n  Nước khoá nhiều nhất:", " · ".join(f"{c} {fmt(v)}" for c, v in cs.most_common(5)))

if a.check:
    import os
    stale = []
    for f in ("content/bai-cong-bo.md", "content/bai-cong-bo-ngan.md"):
        if not os.path.exists(f):
            continue
        txt = open(f, encoding="utf-8").read()
        for k in ("tin", "cong_ty", "cong_ty_mo", "bi_loai", "dia_ly", "hybrid"):
            cur = fmt(V[k])
            # tìm số cùng bậc độ lớn nhưng khác giá trị
            for m in re.finditer(r"\b\d{1,3}(?:\.\d{3})+\b|\b\d{2,4}\b", txt):
                pass
        # kiểm đơn giản: số hiện tại có xuất hiện trong bài không
        missing = [k for k in ("tin", "cong_ty", "cong_ty_mo") if fmt(V[k]) not in txt]
        if missing:
            stale.append((f, missing))
    print()
    if stale:
        for f, ks in stale:
            print(f"  ⚠ {f} — không thấy số hiện tại của: {', '.join(ks)}")
        print("\n  Bài đang ghi số CŨ. Cập nhật trước khi đăng.")
        sys.exit(1)
    print("  ✓ số trong bài khớp kho hiện tại")
