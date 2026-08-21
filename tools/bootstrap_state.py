#!/usr/bin/env python3
"""
Khởi tạo tools/slug_state.json từ jobs.json đã có.

Dùng sau một lần chạy poll toàn bộ, để lần chạy sau đã có cơ sở phân bậc mà
không phải kéo lại 68 phút. Slug nào có trong slugs.txt nhưng không có tin
trong jobs.json thì coi như đã poll và không ra tin.
"""
import json, sys
from collections import defaultdict
from datetime import date
sys.path.insert(0, "tools")
import tiering as T
from pull_sample import load_slugs

jobs = json.load(open("jobs.json", encoding="utf-8"))
today = date.today()
agg = defaultdict(lambda: [0, 0])
for j in jobs:
    k = (j["source"], j["company_slug"])
    agg[k][0] += 1
    if j["eligibility"] == "worldwide":
        agg[k][1] += 1

st = {}
for plat, slug in load_slugs("tools/slugs.txt"):
    n, ww = agg.get((plat, slug), (0, 0))
    rec = {"last_polled": today.isoformat(), "fails": 0, "jobs": n}
    if n:
        rec["last_ok"] = today.isoformat()
    if ww:
        rec["worldwide_last"] = today.isoformat()
    st[T.key(plat, slug)] = rec
T.save(st)

due, stat = T.due(load_slugs("tools/slugs.txt"))
print(f"✓ {len(st):,} slug -> {T.STATE}")
print(f"\nLần chạy NGÀY MAI sẽ poll {len(due):,}/{len(st):,} slug "
      f"({100*len(due)/len(st):.0f}%)")
T.report(stat)
