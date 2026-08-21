#!/usr/bin/env python3
"""
Thu hoạch slug ATS từ chỉ mục Common Crawl CDX.

Common Crawl yêu cầu KHÔNG làm quá tải máy chủ chỉ mục, và nó trả 503/500
(SlowDown) khi bị gọi dày. Script này đi chậm có chủ ý: nghỉ mặc định 4 giây,
lùi luỹ thừa tới 5 lần, và LƯU TIẾN ĐỘ để chạy tiếp được sau khi dừng.

    python3 tools/cc_slugs.py                     # bản chụp mới nhất, cả 4 mẫu URL
    python3 tools/cc_slugs.py --crawl CC-MAIN-2026-25 --delay 6
    python3 tools/cc_slugs.py --verify            # xác minh + ghi vào slugs.txt
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

UA = "cong0-cc/0.1 (nghien cuu thi truong; lien he: you@example.com)"   # <-- SỬA
IDX = "https://index.commoncrawl.org"
STATE = "/tmp/cc_slugs_state.json"

PATTERNS = [
    ("greenhouse", "boards.greenhouse.io/*",     r"greenhouse\.io/([A-Za-z0-9][\w.-]{1,60})"),
    ("greenhouse", "job-boards.greenhouse.io/*", r"greenhouse\.io/([A-Za-z0-9][\w.-]{1,60})"),
    ("lever",      "jobs.lever.co/*",            r"lever\.co/([A-Za-z0-9][\w.-]{1,60})"),
    ("ashby",      "jobs.ashbyhq.com/*",         r"ashbyhq\.com/([A-Za-z0-9][\w.-]{1,60})"),
]
VERIFY = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs",
    "lever":      "https://api.lever.co/v0/postings/{s}?mode=json",
    "ashby":      "https://api.ashbyhq.com/posting-api/job-board/{s}",
}
STOP = {"jobs", "job", "careers", "search", "www", "api", "embed", "boards",
        "en", "static", "assets", "favicon.ico", "robots.txt"}


def get(url, delay, tries=5):
    """GET có lùi luỹ thừa. Common Crawl trả 500/503 khi bị gọi dày."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                time.sleep(delay)
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                wait = delay * (2 ** i) + 5
                print(f"    {e.code} — nghỉ {wait:.0f}s rồi thử lại ({i+1}/{tries})")
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if i < tries - 1:
                time.sleep(delay * (2 ** i) + 5)
                continue
            raise
    raise RuntimeError("hết lượt thử")


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"done": [], "slugs": {}}


def save_state(st):
    json.dump(st, open(STATE, "w"))


def harvest(crawl, delay, max_pages):
    st = load_state()
    st.setdefault("done", [])
    st.setdefault("slugs", {})
    for plat, pat, rx in PATTERNS:
        rx = re.compile(rx)
        q = urllib.parse.quote(pat, safe="")
        try:
            info = json.loads(get(f"{IDX}/{crawl}-index?url={q}&output=json&showNumPages=true", delay))
        except Exception as e:
            print(f"  {pat:<30} — không đếm được trang ({type(e).__name__})")
            continue
        pages = min(info.get("pages", 1), max_pages)
        print(f"  {pat:<30} {info.get('pages')} trang (lấy {pages})")
        for p in range(pages):
            key = f"{crawl}|{pat}|{p}"
            if key in st["done"]:
                continue
            try:
                body = get(f"{IDX}/{crawl}-index?url={q}&output=json&page={p}", delay)
            except Exception as e:
                print(f"    trang {p}: bỏ ({type(e).__name__})")
                continue
            n0 = len(st["slugs"])
            for line in body.split("\n"):
                if not line.strip():
                    continue
                try:
                    u = json.loads(line).get("url", "")
                except json.JSONDecodeError:
                    continue
                m = rx.search(u)
                if m:
                    s = m.group(1).rstrip(".,);:").lower()
                    if s and s not in STOP and not s.isdigit() and len(s) > 1:
                        st["slugs"][s] = plat
            st["done"].append(key)
            save_state(st)
            print(f"    trang {p+1}/{pages}: +{len(st['slugs'])-n0} slug (tổng {len(st['slugs']):,})")
    return st


def verify(st, delay=1.0):
    have = set()
    for line in open("tools/slugs.txt", encoding="utf-8"):
        t = line.split("#")[0].strip()
        if "," in t:
            have.add(t.split(",", 1)[1].strip().lower())
    new = [(p, s) for s, p in sorted(st["slugs"].items()) if s not in have]
    print(f"\n{len(st['slugs']):,} slug thu được · {len(new):,} chưa có. Xác minh (1 req/giây)...")
    live = []
    for i, (plat, s) in enumerate(new, 1):
        try:
            time.sleep(delay)
            d = json.loads(get(VERIFY[plat].format(s=s), 0, tries=1))
            jobs = d if isinstance(d, list) else (d.get("jobs") or [])
            if jobs:
                live.append((plat, s, len(jobs)))
        except Exception:
            pass
        if i % 100 == 0:
            print(f"  [{i}/{len(new)}] sống {len(live)}")
    if live:
        with open("tools/slugs.txt", "a", encoding="utf-8") as f:
            f.write(f"\n# --- Common Crawl CDX, {time.strftime('%d/%m/%Y')} ---\n")
            for plat, s, _ in live:
                f.write(f"{plat},{s}\n")
        print(f"\n✓ thêm {len(live):,} slug sống · {sum(n for _,_,n in live):,} tin -> tools/slugs.txt")
    return live


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crawl")
    ap.add_argument("--delay", type=float, default=4.0, help="giây nghỉ giữa các lần gọi CDX")
    ap.add_argument("--max-pages", type=int, default=8, help="tối đa số trang mỗi mẫu URL")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--reset", action="store_true")
    a = ap.parse_args()

    if a.reset and os.path.exists(STATE):
        os.remove(STATE)
    crawl = a.crawl
    if not crawl:
        crawl = json.loads(get(f"{IDX}/collinfo.json", a.delay))[0]["id"]
    print(f"Bản chụp: {crawl} · nghỉ {a.delay}s · tối đa {a.max_pages} trang/mẫu")
    print(f"Tiến độ lưu ở {STATE} — dừng giữa chừng chạy lại được.\n")

    st = harvest(crawl, a.delay, a.max_pages)
    print(f"\nTổng slug thu được: {len(st['slugs']):,}")
    if a.verify:
        verify(st)
    else:
        print("Chạy lại với --verify để xác minh và ghi vào slugs.txt")


if __name__ == "__main__":
    import urllib.parse
    main()
