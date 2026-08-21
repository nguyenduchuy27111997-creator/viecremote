#!/usr/bin/env python3
"""
Điền cột has_alr tự động: tải trang tin, tìm applicantLocationRequirements
trong JSON-LD JobPosting.

    python3 tools/check_schema.py                 # 40 dòng đầu chưa điền
    python3 tools/check_schema.py -n 200          # cả bảng (chậm: 1 req/giây)

Trả lời số 5 của Cổng 0.1 mà không phải mở 200 tab bằng tay.
Ghi đè cột has_alr (y/n) và alr_countries. KHÔNG đụng các cột chấm tay khác.
"""
import argparse, csv, json, re, sys, time, urllib.error, urllib.request
from collections import defaultdict

CONTACT = "you@example.com"          # <-- SỬA, giống pull_sample.py
UA = f"cong0-sampler/0.1 (nghien cuu thi truong; lien he: {CONTACT})"
LD = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S | re.I)
_last = defaultdict(float)


def get(url):
    d = url.split("/")[2]
    w = 1.0 - (time.monotonic() - _last[d])
    if w > 0:
        time.sleep(w)
    _last[d] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")


def walk(o):
    """JSON-LD hay lồng trong @graph / mảng — duyệt hết."""
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def find_alr(page):
    for m in LD.finditer(page):
        try:
            doc = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        for node in walk(doc):
            t = node.get("@type")
            t = t if isinstance(t, list) else [t]
            if "JobPosting" not in t:
                continue
            alr = node.get("applicantLocationRequirements")
            if not alr:
                continue
            names = [x.get("name", "") for x in (alr if isinstance(alr, list) else [alr])
                     if isinstance(x, dict)]
            return [n for n in names if n]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default="scoring-sheet.csv")
    ap.add_argument("-n", type=int, default=40, help="số dòng xử lý (mặc định 40)")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.file, encoding="utf-8-sig")))
    cols = list(rows[0].keys()) if rows else sys.exit("bảng rỗng")
    if "alr_countries" not in cols:
        cols.insert(cols.index("has_alr") + 1, "alr_countries")

    todo = [r for r in rows if r.get("url") and not (r.get("has_alr") or "").strip()][:a.n]
    print(f"Kiểm {len(todo)} trang (1 req/giây)...\n")
    hit = 0
    for i, r in enumerate(todo, 1):
        try:
            alr = find_alr(get(r["url"]))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            r["has_alr"], r["alr_countries"] = "", f"lỗi: {type(e).__name__}"
            print(f"  [{i:>3}] {r['company'][:18]:<18} — lỗi")
            continue
        if alr:
            hit += 1
            r["has_alr"], r["alr_countries"] = "y", "; ".join(alr)
            vn = any("viet" in x.lower() for x in alr)
            print(f"  [{i:>3}] {r['company'][:18]:<18} y  {'; '.join(alr)[:60]}" + ("   <-- CÓ VIỆT NAM (A-01)" if vn else ""))
        else:
            r["has_alr"], r["alr_countries"] = "n", ""
            print(f"  [{i:>3}] {r['company'][:18]:<18} n")

    with open(a.file, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows([{c: r.get(c, "") for c in cols} for r in rows])

    print(f"\n✓ {hit}/{len(todo)} trang có applicantLocationRequirements ({100*hit/len(todo) if todo else 0:.0f}%)")
    print("  Phủ cao -> A-01 chuyển từ suy luận sang tra cứu (rubric-spec Mục 5.1).")


if __name__ == "__main__":
    main()
