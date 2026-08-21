#!/usr/bin/env python3
"""
Phân bậc poll — quyết định slug nào cần kéo hôm nay.

Ở 5.535 slug, poll toàn bộ mỗi ngày mất 110 phút. Phần lớn slug không đổi gì
và chưa bao giờ sinh ra tin mở-toàn-cầu. Phân bậc theo NĂNG SUẤT ĐÃ QUAN SÁT,
không theo phỏng đoán.

Trạng thái lưu ở tools/slug_state.json — mất file này thì lần chạy sau tự
quay về poll toàn bộ, không hỏng gì.
"""
import json, os
from datetime import date, timedelta

STATE = "tools/slug_state.json"

# Bậc: (số ngày giữa hai lần poll, mô tả)
TIERS = {
    "nóng":  (1,  "sinh tin mở-toàn-cầu trong 90 ngày"),
    "ấm":    (3,  "có tin đang mở"),
    "nguội": (7,  "không có tin, hoặc 180 ngày không sinh tin mở-toàn-cầu"),
    "chết":  (90, "3 lần gọi liên tiếp lỗi"),
}
STALE_DAYS = 30      # tin của slug lâu hơn ngần này không được hiển thị nữa


def load():
    if not os.path.exists(STATE):
        return {}
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)


def key(plat, slug):
    return f"{plat}|{slug}"


def _d(s):
    return date.fromisoformat(s) if s else None


def tier_of(rec, today):
    """Bậc của một slug dựa trên những gì đã QUAN SÁT được, không phải phỏng đoán."""
    if not rec:
        return "nóng"                                   # chưa biết gì -> poll
    if rec.get("fails", 0) >= 3:
        return "chết"
    ww = _d(rec.get("worldwide_last"))
    if ww and (today - ww).days <= 90:
        return "nóng"
    if rec.get("jobs", 0) > 0:
        if ww and (today - ww).days > 180:
            return "nguội"
        return "ấm"
    return "nguội"


def due(slugs, today=None, force_all=False):
    """-> (danh sách slug cần poll, thống kê theo bậc)"""
    today = today or date.today()
    st = load()
    out, stat = [], {k: [0, 0] for k in TIERS}     # [tổng, đến hạn]
    for plat, slug in slugs:
        rec = st.get(key(plat, slug))
        t = tier_of(rec, today)
        stat[t][0] += 1
        last = _d((rec or {}).get("last_polled"))
        if force_all or not last or (today - last).days >= TIERS[t][0]:
            out.append((plat, slug))
            stat[t][1] += 1
    return out, stat


def update(polled, results, today=None):
    """polled: [(plat,slug)]  ·  results: {(plat,slug): (số tin, số tin mở toàn cầu) hoặc None nếu lỗi}"""
    today = today or date.today()
    st = load()
    for plat, slug in polled:
        k = key(plat, slug)
        rec = st.get(k, {"fails": 0, "jobs": 0, "worldwide_last": None})
        rec["last_polled"] = today.isoformat()
        r = results.get((plat, slug))
        if r is None:
            rec["fails"] = rec.get("fails", 0) + 1
        else:
            njobs, nww = r
            rec["fails"] = 0
            rec["last_ok"] = today.isoformat()
            rec["jobs"] = njobs
            if nww:
                rec["worldwide_last"] = today.isoformat()
        st[k] = rec
    save(st)


def fresh(plat, slug, today=None):
    """Tin của slug này còn được hiển thị không? Quá STALE_DAYS thì không."""
    today = today or date.today()
    last = _d((load().get(key(plat, slug)) or {}).get("last_ok"))
    return bool(last) and (today - last).days <= STALE_DAYS


def report(stat):
    print("  Phân bậc:")
    for t, (tot, d) in stat.items():
        if tot:
            print(f"    {t:<7}{tot:>6} slug · đến hạn {d:>5}   ({TIERS[t][0]} ngày/lần — {TIERS[t][1]})")
