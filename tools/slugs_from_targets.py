#!/usr/bin/env python3
"""
Đào slug ATS từ a9-targets.csv (403 công ty remoteintech gắn nhãn region=worldwide).

Nhắm thẳng vào vấn đề tập trung nguồn: đây là danh sách công ty ĐÃ được cộng đồng
lọc là tuyển toàn cầu — đúng nhóm sinh ra tin "mở toàn cầu".

Hai tầng: (1) careers_url đã là URL ATS -> lấy slug luôn
          (2) không phải -> tải trang, tìm link ATS trong HTML
"""
import csv, re, sys, time, urllib.error, urllib.request
from collections import defaultdict

UA = "cong0-discover/0.1 (nghien cuu thi truong)"
PAT = {
    "greenhouse": r"(?:boards|job-boards)\.greenhouse\.io/(?:embed/job_board\?for=)?([A-Za-z0-9][\w.-]{1,60})",
    "lever":      r"jobs\.lever\.co/([A-Za-z0-9][\w.-]{1,60})",
    "ashby":      r"jobs\.ashbyhq\.com/([A-Za-z0-9][\w.-]{1,60})",
}
VERIFY = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs",
    "lever":      "https://api.lever.co/v0/postings/{s}?mode=json",
    "ashby":      "https://api.ashbyhq.com/posting-api/job-board/{s}",
}
STOP = {"jobs", "job", "careers", "search", "www", "api", "embed", "boards", "en"}
_last = defaultdict(float)


def get(url, json_=False):
    d = url.split("/")[2]
    w = 1.0 - (time.monotonic() - _last[d])
    if w > 0:
        time.sleep(w)
    _last[d] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def find(text):
    for plat, rx in PAT.items():
        m = re.search(rx, text or "")
        if m:
            s = m.group(1).rstrip(".,);:").lower()
            if s and s not in STOP and not s.isdigit():
                return plat, s
    return None


def main():
    rows = list(csv.DictReader(open("a9-targets.csv", encoding="utf-8-sig")))
    have = set()
    for line in open("tools/slugs.txt", encoding="utf-8"):
        t = line.split("#")[0].strip()
        if "," in t:
            have.add(tuple(x.strip().lower() for x in t.split(",", 1)))

    direct, need_fetch = [], []
    for r in rows:
        hit = find(r.get("careers_url", "")) or find(r.get("ats_on_page", ""))
        (direct if hit else need_fetch).append((r, hit))
    print(f"{len(rows)} công ty · {len(direct)} có URL ATS sẵn · {len(need_fetch)} phải tải trang\n")

    found = {h for _, h in direct if h}
    print(f"Tải {len(need_fetch)} trang tuyển dụng (1 req/giây/miền)...")
    for i, (r, _) in enumerate(need_fetch, 1):
        u = r.get("careers_url") or r.get("website")
        if not u:
            continue
        if not u.startswith("http"):
            u = "https://" + u
        try:
            hit = find(get(u))
            if hit:
                found.add(hit)
        except Exception:
            pass
        if i % 50 == 0:
            print(f"  [{i}/{len(need_fetch)}] tìm được {len(found)} slug")

    new = sorted(found - have)
    print(f"\n{len(found)} slug ATS · {len(new)} slug MỚI. Xác minh...")
    live = []
    for plat, s in new:
        try:
            import json as J
            d = J.loads(get(VERIFY[plat].format(s=s)))
            jobs = d if isinstance(d, list) else (d.get("jobs") or [])
            if jobs:
                live.append((plat, s, len(jobs)))
                print(f"  ✓ {plat:<11}{s:<28}{len(jobs):>4} tin")
        except Exception:
            pass

    if live:
        with open("tools/slugs.txt", "a", encoding="utf-8") as f:
            f.write(f"\n# --- từ a9-targets.csv (remoteintech region=worldwide), {time.strftime('%d/%m/%Y')} ---\n")
            for plat, s, _ in live:
                f.write(f"{plat},{s}\n")
        print(f"\n✓ thêm {len(live)} slug sống · {sum(n for _,_,n in live):,} tin -> tools/slugs.txt")
    else:
        print("\nKhông có slug mới nào sống.")


if __name__ == "__main__":
    main()
