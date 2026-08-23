#!/usr/bin/env python3
"""
Kho tin -> jobs.json cho build.py

    python3 tools/export_jobs.py                 # toàn bộ slug trong slugs.txt
    python3 tools/export_jobs.py --limit 40      # thử nhanh

Chạy: kéo tin -> khử trùng lặp -> lọc remote -> chấm nhãn -> jobs.json
Mọi nhãn phải kèm trích dẫn nguyên văn (ràng buộc C1 ở prd.md).
"""
import argparse, hashlib, json, os, re, sys, threading, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, "tools")
from pull_sample import (fetch, clean, NORM, ENDPOINTS, load_slugs,
                         REMOTE_RE, ONSITE_RE)
from check_schema import find_alr, get as page_get
import score_rules as S
import country as C
import tiering as T

EXCERPT = 300


# Bằng chứng mạnh hơn thắng. Câu công ty tự viết về ĐIỀU KIỆN (quốc tịch,
# clearance, phải đến văn phòng, múi giờ) mạnh hơn suy ra từ trường địa điểm.
DQ_RANK = ["DQ-04", "DQ-01", "DQ-06", "DQ-05", "DQ-03", "DQ-07", "DQ-09", "DQ-02"]


def score(job):
    """-> (eligibility, reason, evidence, evidence_source)"""
    title, loc, desc = job["title"], job["location"], job["desc"]
    blob = f"{title}. {loc}. {desc}"
    found = []          # (mã, bằng chứng, nguồn)

    lv, lw = S.loc_verdict(loc)
    if lv == "no":
        if S.scope_rebuts_location(desc):
            return "unknown", None, "", ""      # trường location bị mô tả bác bỏ
        found.append(("DQ-02", lw, "location"))
    else:
        tail = re.split(r"[-–—(,]", title)[-1] if re.search(r"[-–—(,]", title) else ""
        tv, tw = S.loc_verdict(tail)
        if tv == "no":
            found.append(("DQ-02", tw.replace("location", "title"), "title"))

    # Danh sách nước ĐÓNG trong thân tin thắng nhãn địa điểm chung chung
    # ("Global" của Testlio vs 15 nước liệt kê tường minh, không có VN).
    cl = S.closed_country_list(blob)
    if cl:
        found.append(("DQ-02", cl[1][:220], "description"))

    # Mệnh đề "chỉ nhận ứng viên <nơi chốn>". Chạy RIÊNG trên tiêu đề rồi tới
    # thân tin, không chạy trên blob: cần biết bằng chứng nằm ở đâu để C1 và
    # trang công ty dẫn đúng nguồn.
    for src, txt in (("title", title), ("description", desc)):
        ao = S.applicants_only(txt)
        if ao:
            found.append(("DQ-02", ao[1][:220], src))
            break

    for cid, rx in S.DQ:
        m = rx.search(blob)
        if not m:
            continue
        if cid == "DQ-02" and S.vn_inclusive(blob[m.end():m.end() + 70]):
            continue
        if cid == "DQ-06" and S.company_level_hybrid(blob[max(0, m.start() - 60):m.end() + 60]):
            continue        # "we are a hybrid team" = mô tả công ty, không phải yêu cầu vai trò
        if cid == "DQ-06" and S.voluntary(blob[max(0, m.start() - 40):m.end() + 80]):
            continue        # "work in person ... as much as you'd like" = mời, không phải buộc
        q = S.quote_around(blob, m, 180)
        found.append((cid, q[:220], "description"))

    if found:
        found.sort(key=lambda x: DQ_RANK.index(x[0]) if x[0] in DQ_RANK else 99)
        cid, q, src = found[0]
        return "excluded", cid, q, src

    if lv == "ok":          # địa điểm CÓ Việt Nam (hoặc vùng chứa VN)
        return "worldwide", None, lw, "location"
    if lv == "global":
        return "worldwide", None, lw, "location"
    # Trường địa điểm nêu nơi chốn cụ thể -> văn xuôi không được nâng lên toàn cầu.
    if S.loc_names_place(loc):
        return "unknown", None, "", ""
    st, sq = S.match_in_hire_ctx(S.A02, blob)
    if st == "limited":
        return "excluded", "DQ-02", sq, "description"
    if st == "ok":
        return "worldwide", None, sq, "description"
    st3, sq3 = S.match_in_hire_ctx(S.A03, blob)
    if st3 == "ok":
        return "worldwide", None, sq3, "description"
    return "unknown", None, "", ""


def mechanism(desc):
    for name, rx in (("eor", S.B04), ("contractor", S.B01)):
        if rx.search(desc):
            return name
    return "unknown"


TZ = {"CET": 3, "CEST": 3, "EET": 4, "CEST/CET": 3, "GMT+1": 3, "GMT+2": 4,
      "UTC+1": 3, "UTC+2": 4, "GMT": 2, "UTC": 2}


def tz_overlap(blob):
    m = re.search(r"\b(CET|CEST|EET|GMT\+[12]|UTC\+[12])\b", blob)
    return TZ.get(m.group(1)) if m else None


def schema_verdict(alr, el, reason, ev, evsrc):
    """Trọng tài giữa nhãn suy từ văn bản và danh sách nước công ty tự khai.

    Tách riêng khỏi apply_schema để rescore.py dùng lại được — trước đây
    rescore chỉ gọi score() nên xoá sạch kết luận DQ-09 từ schema."""
    if not alr:
        return el, reason, ev, evsrc
    v, _ = C.verdict("; ".join(alr))
    if v == "a01":
        return "worldwide", None, "A-01(schema):" + "; ".join(alr), "schema"
    if v == "no":
        if el == "worldwide":
            # Hai nguồn có cấu trúc mâu thuẫn -> không đoán bên nào đúng (N2).
            return ("unknown", None,
                    "XUNG-DOT:" + (ev or "") + "|" + "; ".join(alr), "schema")
        return "excluded", "DQ-09", "DQ-09(schema):" + "; ".join(alr), "schema"
    return el, reason, ev, evsrc


def apply_schema(out, limit=None, verbose=True):
    """Đọc applicantLocationRequirements cho tin CÓ THỂ nộp được.

    Đây là bằng chứng mạnh nhất — công ty tự khai nước nhận ứng viên. Chỉ chạy
    cho nhóm 'worldwide' + 'unknown' (~20% kho) vì nhóm 'excluded' đã có kết
    luận từ trường địa điểm, và mỗi tin tốn một request.
    """
    # Ưu tiên 'worldwide' trước: sai ở nhóm này đắt nhất (dương tính giả).
    todo = ([j for j in out if j["eligibility"] == "worldwide"]
            + [j for j in out if j["eligibility"] == "unknown"])
    if limit and len(todo) > limit:
        print(f"\nGiới hạn schema {limit:,}/{len(todo):,} tin "
              f"({sum(1 for j in todo[:limit] if j['eligibility']=='worldwide'):,} mở toàn cầu trước)")
        todo = todo[:limit]
    print(f"\nĐọc schema cho {len(todo):,} tin (1 req/giây, ~{len(todo)/60:.0f} phút)...")
    st = defaultdict(int)
    for i, j in enumerate(todo, 1):
        try:
            alr = find_alr(page_get(j["url"]))
        except Exception:
            st["lỗi"] += 1
            continue
        if not alr:
            st["không khai"] += 1
            continue
        j["alr_countries"] = alr
        v, why = C.verdict("; ".join(alr))
        if v == "a01":
            # Bằng chứng mạnh nhất trong toàn rubric: công ty tự khai có Việt Nam.
            j.update(eligibility="worldwide", exclusion_reason=None,
                     evidence="A-01(schema):" + "; ".join(alr), evidence_source="schema")
            st["A-01 (có VN)"] += 1
        elif v == "no":
            if j["eligibility"] == "worldwide":
                # Hai nguồn có cấu trúc mâu thuẫn -> không đoán bên nào đúng (N2).
                j.update(eligibility="unknown", exclusion_reason=None,
                         evidence="XUNG-DOT:" + j.get("evidence", "") + "|" + "; ".join(alr),
                         evidence_source="schema")
                st["xung đột"] += 1
            else:
                j.update(eligibility="excluded", exclusion_reason="DQ-09",
                         evidence="DQ-09(schema):" + "; ".join(alr), evidence_source="schema")
                st["DQ-09"] += 1
        else:
            st["không kết luận"] += 1
        if verbose and i % 100 == 0:
            print(f"  [{i}/{len(todo)}] " + " · ".join(f"{k} {v}" for k, v in st.items()))
    print("  " + " · ".join(f"{k}: {v}" for k, v in st.items()))


# --- kéo song song, vẫn giữ trần 1 yêu cầu/giây/miền ------------------------
# Trần 1 req/giây là TỐC ĐỘ PHÁT yêu cầu, không phải số kết nối đồng thời.
# Bản nối tiếp chờ cả thời gian tải (3,5s/slug) nên chỉ đạt 0,28 req/giây.
# Ở đây: giữ khoảng cách >=1s giữa các lần PHÁT, không chặn khi chờ phản hồi.
_gate = defaultdict(lambda: [0.0, threading.Lock()])


def paced_fetch(url):
    dom = url.split("/")[2]
    slot, lock = _gate[dom]
    with lock:
        now = time.monotonic()
        wait = _gate[dom][0] + 1.0 - now
        if wait > 0:
            time.sleep(wait)
        _gate[dom][0] = max(now, _gate[dom][0] + 1.0)
    import urllib.request
    from pull_sample import UA, TIMEOUT
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def pull_all(slugs, workers=32):
    raw, live, done = [], 0, 0
    lk = threading.Lock()

    def one(item):
        plat, slug = item
        try:
            d = json.loads(paced_fetch(ENDPOINTS[plat].format(s=slug)))
            got = [j for j in NORM[plat](slug, d) if j["title"] and j["url"]]
            for j in got:
                j["platform"], j["slug"] = plat, slug
            return got
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for got in ex.map(one, slugs):
            with lk:
                done += 1
                if got is not None:
                    raw += got
                    live += 1
                if done % 250 == 0:
                    print(f"  [{done}/{len(slugs)}] {live} sống · {len(raw):,} tin")
    return raw, live


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slugs", default="tools/slugs.txt")
    ap.add_argument("--limit", type=int)
    ap.add_argument("-o", default="jobs.json")
    ap.add_argument("--no-schema", action="store_true", help="bỏ qua bước đọc applicantLocationRequirements")
    ap.add_argument("--all", action="store_true",
                    help="poll TOÀN BỘ slug, bỏ qua phân bậc (lần chạy đầu / dựng lại kho)")
    ap.add_argument("--schema-limit", type=int, default=2500,
                    help="tối đa số tin đọc schema (ưu tiên nhóm mở toàn cầu). 0 = không giới hạn")
    a = ap.parse_args()

    allslugs = load_slugs(a.slugs)[: a.limit]
    prev = {}
    if os.path.exists(a.o):
        try:
            prev = {j["id"]: j for j in json.load(open(a.o, encoding="utf-8"))}
        except Exception:
            prev = {}

    slugs, stat = T.due(allslugs, force_all=a.all or not prev)
    if a.all or not prev:
        print(f"Kéo TOÀN BỘ {len(slugs):,} board (lần đầu hoặc --all)")
    else:
        print(f"Kéo {len(slugs):,}/{len(allslugs):,} board đến hạn "
              f"({100*len(slugs)/len(allslugs):.0f}%) · giữ lại {len(prev):,} tin từ lần trước")
        T.report(stat)
    print(f"  trần 1 yêu cầu/giây/miền, 32 luồng...")
    raw, live = pull_all(slugs)
    print(f"  slug sống {live}/{len(slugs)} · {len(raw):,} tin")
    polled_slugs = {(p, sl) for p, sl in slugs}

    seen, uniq = set(), []
    for r in raw:
        k = (re.sub(r"\W", "", r["company"].lower()), re.sub(r"\W", "", r["title"].lower()))
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    # Địa điểm ghi rõ on-site thì mô tả có nhắc "remote" cũng không cứu được.
    remote = [r for r in uniq
              if REMOTE_RE.search(f"{r['title']} {r['location']} {r['desc'][:1500]}")
              and not ONSITE_RE.search(r["location"] or "")]
    print(f"  khử trùng {len(uniq)} · remote {len(remote)}")

    today = time.strftime("%Y-%m-%d")
    out, stat = [], defaultdict(int)
    for r in remote:
        el, reason, ev, evsrc = score(r)
        stat[el] += 1
        blob = f"{r['title']}. {r['location']}. {r['desc']}"
        out.append({
            # Cắt 90 ký tự làm tiêu đề dài đụng nhau — legionhealth đăng cùng vai trò
            # 57 lần với 57 URL khác nhau, tất cả rút về một id và ghi đè lẫn nhau.
            # Gắn thêm 6 ký tự băm của URL: ổn định giữa các lần chạy, và duy nhất.
            "id": (re.sub(r"\W+", "-", f"{r['slug']}-{r['title']}".lower())[:84].strip("-")
                   + "-" + hashlib.sha1(r["url"].encode()).hexdigest()[:6]),
            "company": r["company"], "company_slug": r["slug"],
            "title": r["title"], "location_raw": r["location"], "url": r["url"],
            "source": r["platform"], "first_seen": today, "last_seen": today,
            "status": "open",
            "eligibility": el, "exclusion_reason": reason,
            "evidence": ev, "evidence_source": evsrc,
            "timezone_overlap_gmt7": tz_overlap(blob),
            "contract_mechanism": mechanism(r["desc"]),
            "pay_disclosed": bool(r["pay"]) or bool(re.search(r"\$\s?\d{2,3}[,.]?\d{3}", r["desc"])),
            "alr_countries": [],
            "excerpt": r["desc"][:EXCERPT],
            "index_layer": "aggregated",
            "rubric_version": "0.4", "scored_at": today,
        })

    # Slug không được poll lần này thì KHÔNG biết tin của nó còn mở không.
    # Giữ nguyên bản ghi cũ, không đánh dấu đóng. Chỉ slug ĐÃ poll mới có
    # quyền kết luận "tin biến mất khỏi feed = đã đóng" (ràng buộc C3).
    if prev and not a.all:
        newids = {j["id"] for j in out}
        carried = 0
        today = time.strftime("%Y-%m-%d")
        for pid, pj in prev.items():
            k = (pj.get("source"), pj.get("company_slug"))
            if k in polled_slugs:
                continue                      # slug này vừa poll: thiếu nghĩa là đã đóng
            if pid in newids:
                continue
            if not T.fresh(k[0], k[1]):
                continue                      # quá cũ, không hiển thị nữa
            out.append(pj)
            carried += 1
        print(f"  giữ lại {carried:,} tin từ slug chưa đến hạn poll")

    # cập nhật trạng thái phân bậc
    res = defaultdict(lambda: [0, 0])
    for j in out:
        k = (j["source"], j["company_slug"])
        if k in polled_slugs:
            res[k][0] += 1
            if j["eligibility"] == "worldwide":
                res[k][1] += 1
    T.update(slugs, {k: tuple(v) for k, v in res.items()})

    if not a.no_schema:
        apply_schema(out, limit=a.schema_limit or None)
    json.dump(out, open(a.o, "w", encoding="utf-8"), ensure_ascii=False)
    fin = defaultdict(int)
    for j in out:
        fin[j["eligibility"]] += 1
    print(f"\n✓ {len(out)} tin -> {a.o}")
    for k in ("worldwide", "excluded", "unknown"):
        print(f"   {k:<11}{fin[k]:>6}  {100*fin[k]/len(out):>5.1f}%")


if __name__ == "__main__":
    main()
