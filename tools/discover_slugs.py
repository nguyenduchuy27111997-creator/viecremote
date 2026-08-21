#!/usr/bin/env python3
"""
Khám phá slug ATS THẬT thay vì đoán (FR-1.3, làm tự động).

Nguồn: Hacker News qua Algolia API — công khai, không cần khoá, không giới hạn
điều khoản. Các thread "Who is hiring" đầy link ATS thật.

    python3 tools/discover_slugs.py                      # khám phá + xác minh + ghi vào slugs.txt
    python3 tools/discover_slugs.py --platform lever     # chỉ một nền tảng
    python3 tools/discover_slugs.py -n 80 --dry-run      # xem trước, không ghi

Đây là bản thu nhỏ của FR-1.1 (Common Crawl CDX). Đủ cho Cổng 0.1; bản đầy đủ
chỉ cần khi đã qua cổng.
"""
import argparse, html, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from collections import defaultdict

UA = "cong0-discover/0.1 (nghien cuu thi truong)"
ALGOLIA = "https://hn.algolia.com/api/v1/search?query={q}&tags=comment&hitsPerPage=100&page={p}"

# mẫu URL -> slug, và endpoint để xác minh
PLATFORMS = {
    "greenhouse": (r"(?:boards|job-boards)\.greenhouse\.io/([A-Za-z0-9][\w.-]{1,60})",
                   "https://boards-api.greenhouse.io/v1/boards/{s}/jobs"),
    "lever":      (r"jobs\.lever\.co/([A-Za-z0-9][\w.-]{1,60})",
                   "https://api.lever.co/v0/postings/{s}?mode=json"),
    "ashby":      (r"jobs\.ashbyhq\.com/([A-Za-z0-9][\w.-]{1,60})",
                   "https://api.ashbyhq.com/posting-api/job-board/{s}"),
}
QUERIES = {"greenhouse": ["greenhouse.io", "boards.greenhouse"],
           "lever": ["lever.co", "jobs.lever"],
           "ashby": ["ashbyhq", "jobs.ashbyhq"]}
STOP = {"jobs", "job", "careers", "search", "www", "api", "embed", "boards"}
_last = defaultdict(float)


def get(url):
    d = url.split("/")[2]
    w = 1.0 - (time.monotonic() - _last[d])
    if w > 0:
        time.sleep(w)
    _last[d] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")


def harvest(plat, pages):
    pat = re.compile(PLATFORMS[plat][0])
    found = set()
    for q in QUERIES[plat]:
        for p in range(pages):
            try:
                d = json.loads(get(ALGOLIA.format(q=urllib.parse.quote(q), p=p)))
            except Exception:
                break
            hits = d.get("hits", [])
            if not hits:
                break
            for h in hits:
                txt = html.unescape(h.get("comment_text") or "")
                for m in pat.finditer(txt):
                    s = m.group(1).rstrip(".,);:").lower()
                    if s and s not in STOP and not s.isdigit():
                        found.add(s)
    return found


def verify(plat, slug):
    """Sống = HTTP 200 và có >= 1 tin."""
    try:
        d = json.loads(get(PLATFORMS[plat][1].format(s=slug)))
    except Exception:
        return None
    jobs = d if isinstance(d, list) else (d.get("jobs") or [])
    return len(jobs) if jobs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", choices=list(PLATFORMS), action="append")
    ap.add_argument("--pages", type=int, default=4, help="số trang HN mỗi truy vấn")
    ap.add_argument("-n", type=int, default=60, help="tối đa slug xác minh mỗi nền tảng")
    ap.add_argument("--slugs", default="tools/slugs.txt")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    plats = a.platform or list(PLATFORMS)

    have = set()
    try:
        for line in open(a.slugs, encoding="utf-8"):
            t = line.split("#")[0].strip()
            if "," in t:
                have.add(tuple(x.strip() for x in t.split(",", 1)))
    except FileNotFoundError:
        pass

    new = []
    for plat in plats:
        print(f"\n=== {plat} ===")
        cand = sorted(harvest(plat, a.pages) - {s for p, s in have if p == plat})
        print(f"  HN cho {len(cand)} slug mới. Xác minh {min(len(cand), a.n)} (1 req/giây)...")
        live = 0
        for s in cand[:a.n]:
            n = verify(plat, s)
            if n:
                live += 1
                new.append((plat, s, n))
                print(f"    ✓ {s:<28} {n:>4} tin")
        print(f"  -> {live}/{min(len(cand), a.n)} sống")

    if not new:
        raise SystemExit("\nKhông tìm được slug mới nào.")
    new.sort(key=lambda x: (-x[2]))
    print(f"\n{len(new)} slug mới sống, tổng {sum(n for _,_,n in new):,} tin")

    if a.dry_run:
        print("(dry-run — không ghi)")
    else:
        with open(a.slugs, "a", encoding="utf-8") as f:
            f.write(f"\n# --- khám phá tự động từ HN ({time.strftime('%d/%m/%Y')}) ---\n")
            for plat, s, n in new:
                f.write(f"{plat},{s}\n")
        print(f"✓ đã thêm vào {a.slugs}")


if __name__ == "__main__":
    main()
