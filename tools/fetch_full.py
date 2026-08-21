#!/usr/bin/env python3
"""Tải full mô tả cho các tin trong bảng chấm -> cache JSON (desc_500 quá ngắn để chấm)."""
import csv, json, re, sys, time, urllib.request
from collections import defaultdict
sys.path.insert(0, "tools")
from pull_sample import fetch, clean, NORM, ENDPOINTS

SLUG = {"greenhouse": r"greenhouse\.io/([^/?#]+)", "lever": r"lever\.co/([^/?#]+)",
        "ashby": r"ashbyhq\.com/([^/?#]+)"}

rows = list(csv.DictReader(open("scoring-sheet.csv", encoding="utf-8-sig")))
need = defaultdict(set)
for r in rows:
    m = re.search(SLUG.get(r["platform"], r"$^"), r["url"] or "")
    if m:
        need[r["platform"]].add(m.group(1))

cache = {}
tot = sum(len(v) for v in need.values())
print(f"Tải {tot} board...")
i = 0
for plat, slugs in need.items():
    for s in sorted(slugs):
        i += 1
        try:
            d = json.loads(fetch(ENDPOINTS[plat].format(s=s)))
            for j in NORM[plat](s, d):
                if j["url"]:
                    cache[j["url"]] = j["desc"]
        except Exception as e:
            print(f"  [{i}/{tot}] {plat}/{s} — {type(e).__name__}")
json.dump(cache, open("/tmp/desc_cache.json", "w"), ensure_ascii=False)
hit = sum(1 for r in rows if r["url"] in cache)
print(f"\n✓ {len(cache)} mô tả -> /tmp/desc_cache.json  |  khớp {hit}/{len(rows)} dòng bảng")
