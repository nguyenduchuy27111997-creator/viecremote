#!/usr/bin/env python3
"""
Cổng 0.1 — kéo mẫu tin remote thật từ 4 ATS công khai, xuất bảng chấm tay.

Chỉ dùng thư viện chuẩn. Không cần cài gì.

    python3 tools/pull_sample.py                    # 200 tin, ghi ra scoring-sheet.csv
    python3 tools/pull_sample.py -n 50              # mẫu nhỏ để thử trước
    python3 tools/pull_sample.py --slugs tools/slugs.txt -o out.csv

Tuân theo PRD FR-2.1/2.3: 1 yêu cầu/giây/miền, User-Agent trung thực có liên hệ.
SỬA CONTACT bên dưới thành email của bạn trước khi chạy thật.
"""
import argparse, csv, html, json, random, re, sys, time, urllib.error, urllib.request
from collections import defaultdict

CONTACT = "you@example.com"          # <-- SỬA
UA = f"cong0-sampler/0.1 (nghien cuu thi truong; lien he: {CONTACT})"
TIMEOUT = 20
DELAY = 1.0                          # giây, mỗi miền

ENDPOINTS = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true",
    "lever":      "https://api.lever.co/v0/postings/{s}?mode=json",
    "ashby":      "https://api.ashbyhq.com/posting-api/job-board/{s}?includeCompensation=true",
    "workable":   "https://apply.workable.com/api/v1/widget/accounts/{s}",
}

# --- gợi ý loại trừ, theo rubric-spec Mục 4 (DQ-01..DQ-04) -------------------
# Đây là GỢI Ý cho người chấm, KHÔNG phải quyết định. Vẫn phải đọc tay.
DQ_HINTS = [
    ("DQ-01", r"authoriz(?:ed|ation) to work|work permit|right to work|eligible to work in"),
    ("DQ-02", r"\bU\.?S\.?[- ]only\b|\bUS[- ]based\b|must reside in|residents? of the|only considering candidates (?:in|located)|\bEU[- ]only\b|\bUK[- ]only\b"),
    ("DQ-03", r"\bW-?2\b|\bPAYE\b|local payroll"),
    ("DQ-04", r"security clearance|\bU\.?S\.? citizen|citizenship required"),
]
DQ_RE = [(cid, re.compile(p, re.I)) for cid, p in DQ_HINTS]
REMOTE_RE = re.compile(r"remote|anywhere|distributed|work from home|\bWFH\b", re.I)
ONSITE_RE = re.compile(r"on[- ]?site|in[- ]?office|in[- ]?person", re.I)
TAG_RE = re.compile(r"<[^>]+>")

_last_hit = defaultdict(float)


def fetch(url):
    """GET trả về text, tự giới hạn 1 req/giây/miền."""
    domain = url.split("/")[2]
    wait = DELAY - (time.monotonic() - _last_hit[domain])
    if wait > 0:
        time.sleep(wait)
    _last_hit[domain] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    """Bỏ thẻ HTML + giải mã entity, gộp khoảng trắng."""
    if not s:
        return ""
    # Một số ATS mã hoá entity hai lần ("&amp;nbsp;"). Giải mã cho tới khi ổn định,
    # nếu không "&nbsp;" sẽ hiện thô trên trang.
    t = str(s)
    for _ in range(3):
        u = html.unescape(t)
        if u == t:
            break
        t = u
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", t)).strip()


# --- adapter: mỗi ATS một hình dạng, không dùng chung -----------------------
def norm_greenhouse(slug, d):
    for j in d.get("jobs", []):
        yield dict(company=slug, title=j.get("title", ""),
                   location=(j.get("location") or {}).get("name", ""),
                   url=j.get("absolute_url", ""), desc=clean(j.get("content")),
                   pay="", updated=j.get("updated_at", ""))


def norm_lever(slug, d):
    for j in (d if isinstance(d, list) else []):
        cat = j.get("categories") or {}
        yield dict(company=slug, title=j.get("text", ""), location=cat.get("location", ""),
                   url=j.get("hostedUrl", ""),
                   desc=clean(j.get("descriptionPlain") or j.get("description")),
                   pay="", updated=str(j.get("createdAt", "")))


def norm_ashby(slug, d):
    for j in d.get("jobs", []):
        comp = j.get("compensation") or {}
        yield dict(company=d.get("name") or slug, title=j.get("title", ""),
                   location=j.get("location", ""), url=j.get("jobUrl", ""),
                   desc=clean(j.get("descriptionPlain") or j.get("descriptionHtml")),
                   pay=clean(comp.get("compensationTierSummary", "")),
                   updated=j.get("publishedAt", ""))


def norm_workable(slug, d):
    for j in d.get("jobs", []):
        loc = j.get("location") or {}
        parts = [loc.get("city"), loc.get("country")] if isinstance(loc, dict) else []
        yield dict(company=(d.get("name") or slug), title=j.get("title", ""),
                   location=", ".join(p for p in parts if p) or ("Remote" if (isinstance(loc, dict) and loc.get("workplace") == "remote") else ""),
                   url=j.get("url") or j.get("shortlink", ""),
                   desc=clean(j.get("description")), pay="", updated=j.get("published", ""))


NORM = {"greenhouse": norm_greenhouse, "lever": norm_lever,
        "ashby": norm_ashby, "workable": norm_workable}


def load_slugs(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line or "," not in line:
            continue
        p, s = (x.strip() for x in line.split(",", 1))
        if p in ENDPOINTS:
            out.append((p, s))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", default="tools/slugs.txt")
    ap.add_argument("-n", type=int, default=200, help="cỡ mẫu (mặc định 200)")
    ap.add_argument("-o", default="scoring-sheet.csv")
    ap.add_argument("--per-company", type=int, default=4,
                    help="tối đa bao nhiêu tin/công ty, tránh một công ty lấn át mẫu")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()

    slugs = load_slugs(a.slugs)
    print(f"{len(slugs)} slug ứng viên. Kéo (1 req/giây/miền, sẽ mất vài phút)...\n")

    rows, ok, dead = [], defaultdict(int), []
    for i, (plat, slug) in enumerate(slugs, 1):
        try:
            data = json.loads(fetch(ENDPOINTS[plat].format(s=slug)))
            got = [j for j in NORM[plat](slug, data) if j["title"]]
            for j in got:
                j["platform"] = plat
                j["slug"] = slug
            rows += got
            ok[plat] += 1
            print(f"  [{i:>2}/{len(slugs)}] {plat:<10} {slug:<16} {len(got):>4} tin")
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            dead.append(f"{plat},{slug}")
            print(f"  [{i:>2}/{len(slugs)}] {plat:<10} {slug:<16}    — bỏ ({type(e).__name__})")

    print(f"\nSlug sống: {sum(ok.values())}/{len(slugs)}  ->  {dict(ok)}")
    if dead:
        print(f"Slug hỏng ({len(dead)}): {' '.join(dead[:12])}{' ...' if len(dead) > 12 else ''}")
        print("  Gỡ chúng khỏi slugs.txt, hoặc tra lại slug đúng trên trang tuyển dụng của công ty.")

    total = len(rows)
    # khử trùng lặp (PRD FR-3.2)
    seen, uniq = set(), []
    for r in rows:
        k = (re.sub(r"\W", "", r["company"].lower()), re.sub(r"\W", "", r["title"].lower()))
        if k not in seen:
            seen.add(k)
            uniq.append(r)

    # lọc remote (PRD FR-4.2)
    # Địa điểm ghi rõ on-site thì mô tả có nhắc "remote" cũng không cứu được.
    remote = [r for r in uniq
              if REMOTE_RE.search(f"{r['title']} {r['location']} {r['desc'][:1500]}")
              and not ONSITE_RE.search(r["location"] or "")]
    print(f"\nTổng {total} tin -> {len(uniq)} sau khử trùng -> {len(remote)} có dấu hiệu remote")

    # lấy mẫu: cân bằng theo nền tảng, giới hạn số tin mỗi công ty
    random.seed(a.seed)
    random.shuffle(remote)
    by_plat, cap = defaultdict(list), defaultdict(int)
    for r in remote:
        if cap[r["company"]] < a.per_company:
            cap[r["company"]] += 1
            by_plat[r["platform"]].append(r)
    sample, idx = [], 0
    while len(sample) < a.n and any(idx < len(v) for v in by_plat.values()):
        for plat in ENDPOINTS:
            if idx < len(by_plat[plat]) and len(sample) < a.n:
                sample.append(by_plat[plat][idx])
        idx += 1

    cols = ["stt", "platform", "company", "title", "location", "url", "pay_from_feed",
            "dq_hint", "desc_500",
            # --- cột chấm tay, để trống ---
            "DQ", "tier", "tier_a_scope", "rules_fired", "quote", "contract_mech",
            "tz_overlap", "has_alr", "on_free_board", "minutes", "notes"]
    with open(a.o, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for i, r in enumerate(sample, 1):
            blob = f"{r['title']} {r['location']} {r['desc']}"
            hints = ";".join(cid for cid, rx in DQ_RE if rx.search(blob))
            w.writerow({"stt": i, "platform": r["platform"], "company": r["company"],
                        "title": r["title"], "location": r["location"], "url": r["url"],
                        "pay_from_feed": r["pay"], "dq_hint": hints,
                        "desc_500": r["desc"][:500]})

    print(f"\n✓ {len(sample)} tin -> {a.o}")
    print(f"  Phân bố: {dict((p, sum(1 for r in sample if r['platform'] == p)) for p in ENDPOINTS)}")
    print(f"  Có gợi ý DQ: {sum(1 for r in sample if any(rx.search(r['title'] + r['desc']) for _, rx in DQ_RE))}")
    print("\nTiếp: mở file, chấm tay theo rubric-spec.md, rồi `python3 tools/tally.py`")


if __name__ == "__main__":
    main()
