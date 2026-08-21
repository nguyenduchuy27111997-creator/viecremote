#!/usr/bin/env python3
"""So nhãn máy (auto_tier) với nhãn tay (tier) trên các dòng đã chấm tay."""
import csv, sys
from collections import Counter
rows = [r for r in csv.DictReader(open(sys.argv[1] if len(sys.argv)>1 else "scoring-sheet.csv",
                                       encoding="utf-8-sig"))
        if (r.get("tier") or "").strip() and (r.get("auto_tier") or "").strip()]
if not rows: raise SystemExit("chưa có dòng nào có cả nhãn tay và nhãn máy")
L=["no","A","B","unknown"]
cm=Counter((r["auto_tier"], r["tier"]) for r in rows)
print(f"ĐỐI CHỨNG — {len(rows)} tin\n\n{'máy\\tay':<10}"+"".join(f"{l:>9}" for l in L))
for m in L:
    if any(cm[(m,h)] for h in L): print(f"{m:<10}"+"".join(f"{cm[(m,h)]:>9}" for h in L))
tp=cm[("A","A")]; fp=sum(cm[("A",h)] for h in L if h!="A")
fn=sum(cm[(m,"A")] for m in L if m!="A")
hand_no=sum(1 for r in rows if r["tier"]=="no"); caught=cm[("no","no")]
acc=sum(cm[(l,l)] for l in L)
p=100*tp/(tp+fp) if tp+fp else 0
rc=100*caught/hand_no if hand_no else 0
def mark(v,t): return "✓" if v>=t else "✗"
print(f"\n  Tier A precision  {tp}/{tp+fp} = {p:>5.0f}%   ngưỡng 90%  {mark(p,90)}")
print(f"  Tier A recall     {tp}/{tp+fn} = {100*tp/(tp+fn) if tp+fn else 0:>5.0f}%")
print(f"  DQ recall         {caught}/{hand_no} = {rc:>5.0f}%   ngưỡng 95%  {mark(rc,95)}")
print(f"  Accuracy tổng     {acc}/{len(rows)} = {100*acc/len(rows):>5.0f}%   ngưỡng 85%  {mark(100*acc/len(rows),85)}")
bad=[r for r in rows if r["auto_tier"]!=r["tier"]]
if bad:
    print(f"\n  Còn sai {len(bad)}:")
    for r in bad[:12]:
        print(f"    {r['company'][:16]:<16} máy={r['auto_tier']:<8} tay={r['tier']:<8} [{(r['auto_rules'] or '')[:34]}]")
