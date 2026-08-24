#!/usr/bin/env python3
"""
Chấm lại có mục tiêu: chỉ những tin dính một quy tắc cụ thể.

Khi sửa một quy tắc, chạy lại toàn bộ export mất 110 phút. Script này chỉ
kéo lại board của các tin bị ảnh hưởng rồi chấm lại đúng chúng.

    python3 tools/rescore.py --reason DQ-06
    python3 tools/rescore.py --reason DQ-06 --dry-run
"""
import argparse, json, sys
from collections import Counter
sys.path.insert(0, "tools")
from export_jobs import pull_all, score, mechanism, tz_overlap, schema_verdict
from pull_sample import NORM, ENDPOINTS

ap = argparse.ArgumentParser()
ap.add_argument("--reason", help="ví dụ DQ-06")
ap.add_argument("--eligibility", help="ví dụ worldwide — chấm lại theo NHÃN thay vì theo lý do")
ap.add_argument("--jobs", default="jobs.json")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()

jobs = json.load(open(a.jobs, encoding="utf-8"))
if a.eligibility:
    hit = [j for j in jobs if j["eligibility"] == a.eligibility]
    what = f"nhãn {a.eligibility}"
elif a.reason:
    hit = [j for j in jobs if j.get("exclusion_reason") == a.reason]
    what = a.reason
else:
    raise SystemExit("cần --reason hoặc --eligibility")
boards = sorted({(j["source"], j["company_slug"]) for j in hit})
print(f"{len(hit):,} tin dính {what} · {len(boards)} board cần kéo lại\n")

raw, live = pull_all(boards)
by_url = {r["url"]: r for r in raw}
print(f"  {live}/{len(boards)} board sống · {len(raw):,} tin\n")

ch = Counter()
for j in hit:
    r = by_url.get(j["url"])
    if not r:
        ch["không tìm lại được"] += 1
        continue
    el, reason, ev, evsrc = score(r)
    # Bằng chứng schema do CHÍNH công ty khai mạnh hơn mọi suy luận từ văn bản.
    # score() không đọc nó -> phải áp lại, nếu không rescore sẽ xoá mất DQ-09/A-01.
    el, reason, ev, evsrc = schema_verdict(j.get("alr_countries"), el, reason, ev, evsrc)
    same = el == j["eligibility"] and reason == j.get("exclusion_reason")
    ch["giữ nguyên" if same else f"{j['eligibility']} -> {el}"] += 1
    if same and ev != (j.get("evidence") or ""):
        ch["nhãn giữ, bằng chứng đổi"] += 1
    # LUÔN cập nhật bằng chứng, kể cả khi nhãn không đổi — sửa cách diễn đạt
    # bằng chứng cũng là sửa sản phẩm, không chỉ sửa nhãn.
    if not a.dry_run:
        blob = f"{r['title']}. {r['location']}. {r['desc']}"
        j.update(eligibility=el, exclusion_reason=reason, evidence=ev,
                 evidence_source=evsrc, timezone_overlap_gmt7=tz_overlap(blob),
                 contract_mechanism=mechanism(r["desc"], r["title"]))

for k, v in ch.most_common():
    print(f"  {k:<28}{v:>6}")
if not a.dry_run:
    json.dump(jobs, open(a.jobs, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"\n✓ ghi lại {a.jobs}")
