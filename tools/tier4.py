#!/usr/bin/env python3
"""
Tầng 4 — điều tra các tin 'Không rõ' ở mức CÔNG TY.
A-04 (pháp nhân VN) và A-06 (EOR phủ VN) là thuộc tính công ty, không phải của một tin.
Nên quét TOÀN BỘ board của công ty đó, không chỉ tin đang xét.
"""
import csv, json, re, sys
sys.path.insert(0, "tools")
from pull_sample import fetch, clean, NORM, ENDPOINTS
from check_schema import find_alr, get

SLUG = {"greenhouse": r"greenhouse\.io/([^/?#]+)", "lever": r"lever\.co/([^/?#]+)",
        "ashby": r"ashbyhq\.com/([^/?#]+)"}
VN   = re.compile(r"\bvi[eệ]t ?nam\b|\bvietnamese\b|ho chi minh|hanoi|đà nẵng|da nang", re.I)
EOR  = re.compile(r"employer of record|\bEOR\b|\bDeel\b|Oyster HR|Velocity Global|Remofirst", re.I)
GLOB = re.compile(r"we hire globally|hire (?:people )?(?:from )?anywhere|"
                  r"anywhere in the world|any country|work from anywhere", re.I)
APAC = re.compile(r"\bAPAC\b|\bAPJ\b|Asia[- ]Pacific|Southeast Asia", re.I)

rows = list(csv.DictReader(open("scoring-sheet.csv", encoding="utf-8-sig")))
todo = [r for r in rows if (r.get("tier") or "").strip() == "unknown"]
seen = {}
print(f"Tầng 4 trên {len(todo)} tin 'Không rõ' — {len({r['company'] for r in todo})} công ty\n" + "="*76)

for r in todo:
    m = re.search(SLUG.get(r["platform"], r"$^"), r["url"] or "")
    key = (r["platform"], m.group(1) if m else r["company"])
    if key not in seen:
        try:
            d = json.loads(fetch(ENDPOINTS[key[0]].format(s=key[1])))
            jobs = list(NORM[key[0]](key[1], d))
        except Exception as e:
            seen[key] = ("lỗi", f"{type(e).__name__}", 0); continue
        allt = " ".join(j["desc"] for j in jobs) + " " + " ".join(j["location"] for j in jobs)
        ev = []
        if VN.search(allt):   ev.append(("A-04/05", VN.search(allt).group(0)))
        if EOR.search(allt):  ev.append(("A-06?",  EOR.search(allt).group(0)))
        if GLOB.search(allt): ev.append(("A-02",   GLOB.search(allt).group(0)))
        if APAC.search(allt): ev.append(("A-03",   APAC.search(allt).group(0)))
        seen[key] = ("ok", ev, len(jobs))
    st, ev, n = seen[key]
    if st == "lỗi":
        print(f"  {r['company'][:18]:<18} {r['title'][:34]:<34} — không tải được board ({ev})")
    elif not ev:
        print(f"  {r['company'][:18]:<18} {r['title'][:34]:<34} [{n:>3} tin board]  không có tín hiệu")
    else:
        print(f"  {r['company'][:18]:<18} {r['title'][:34]:<34} [{n:>3} tin board]  " +
              " · ".join(f"{c}:{t}" for c, t in ev))
