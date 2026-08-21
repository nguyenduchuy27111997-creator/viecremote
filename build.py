#!/usr/bin/env python3
"""
jobs.json -> web tĩnh. Không phụ thuộc gì ngoài stdlib.

    python3 build.py                 # -> site/
    python3 build.py --out dist

Build DỪNG nếu vi phạm C1 (nhãn không có trích dẫn) hoặc C2 (có JobPosting schema).
Xem prd.md Mục 6.
"""
import argparse, html, json, os, re, shutil, sys
from collections import Counter, defaultdict

sys.path.insert(0, "tools")
from gates import EXCERPT_MAX, TRIGGER, validate      # noqa: E402
from datetime import date

SITE = "Việc remote — tra cứu"
TAGLINE = "Công ty nào thật sự tuyển được người ở Việt Nam"

REASON = {
    "DQ-01": "Yêu cầu giấy phép lao động tại một nước cụ thể",
    "DQ-02": "Giới hạn địa lý — chỉ tuyển ở nước/vùng nhất định",
    "DQ-03": "Hình thức lao động chỉ tồn tại ở một nước (W-2, PAYE)",
    "DQ-04": "Yêu cầu quốc tịch hoặc security clearance",
    "DQ-05": "Yêu cầu múi giờ mà GMT+7 không trùng nổi",
    "DQ-06": "Phải có mặt tại văn phòng",
    "DQ-07": "Qua agency, không tiết lộ công ty tuyển",
    "DQ-09": "Dữ liệu có cấu trúc của công ty không liệt kê Việt Nam",
}
# ISO -> tên tiếng Việt. Chỉ những nước thực sự gặp trong dữ liệu.
CNAME = {
 "US":"Mỹ","CA":"Canada","GB":"Anh","IE":"Ireland","DE":"Đức","FR":"Pháp","ES":"Tây Ban Nha",
 "PT":"Bồ Đào Nha","NL":"Hà Lan","BE":"Bỉ","CH":"Thụy Sĩ","AT":"Áo","IT":"Ý","PL":"Ba Lan",
 "CZ":"Séc","SK":"Slovakia","HU":"Hungary","RO":"Romania","BG":"Bulgaria","GR":"Hy Lạp",
 "EE":"Estonia","LV":"Latvia","LT":"Lithuania","FI":"Phần Lan","SE":"Thụy Điển","NO":"Na Uy",
 "DK":"Đan Mạch","IS":"Iceland","RS":"Serbia","HR":"Croatia","SI":"Slovenia","UA":"Ukraine",
 "RU":"Nga","TR":"Thổ Nhĩ Kỳ","IL":"Israel","AE":"UAE","EG":"Ai Cập","ZA":"Nam Phi",
 "NG":"Nigeria","KE":"Kenya","MA":"Maroc","AU":"Úc","NZ":"New Zealand","JP":"Nhật Bản",
 "SG":"Singapore","IN":"Ấn Độ","CN":"Trung Quốc","HK":"Hồng Kông","TW":"Đài Loan",
 "KR":"Hàn Quốc","PH":"Philippines","ID":"Indonesia","TH":"Thái Lan","MY":"Malaysia",
 "BR":"Brazil","MX":"Mexico","AR":"Argentina","CO":"Colombia","CL":"Chile","PE":"Peru",
 "UY":"Uruguay","CR":"Costa Rica","KY":"Cayman","LU":"Luxembourg","MT":"Malta","CY":"Síp",
 "VN":"Việt Nam","EU":"Liên minh châu Âu","EMEA":"EMEA","LATAM":"Mỹ Latinh",
 "NA":"Bắc Mỹ","AMER":"châu Mỹ","SA":"Nam Mỹ","ME":"Trung Đông","AF":"châu Phi","ANZ":"Úc/NZ",
}


def countries(j):
    """Mã nước mà tin bị giới hạn vào, lấy từ chuỗi bằng chứng máy sinh."""
    ev = j.get("evidence") or ""
    if "|" not in ev or not ev.startswith("DQ-02(location)"):
        return []
    return [c for c in ev.split("|")[-1].split("/") if c]


def human_evidence(j):
    """Chuỗi máy sinh -> câu người đọc được. Người dùng không cần biết mã DQ."""
    ev = (j.get("evidence") or "").strip()
    if not ev:
        return ""
    if ev.startswith("DQ-02(location)"):
        raw = ev[len("DQ-02(location):"):].split("|")[0]
        cs = countries(j)
        names = ", ".join(CNAME.get(c, c) for c in cs)
        return (f"Tin ghi địa điểm: <b>{e(raw)}</b>." +
                (f" Chỉ tuyển ở {e(names)} — không có Việt Nam." if names else ""))
    if ev.startswith("A-02(location)"):
        return f"Tin ghi địa điểm: <b>{e(ev.split(': ', 1)[-1])}</b> — không giới hạn quốc gia."
    if ev.startswith("A-03(location)"):
        raw = ev.split(": ", 1)[-1]
        vn = re.search(r"\bvi[eệ]t ?nam\b", raw, re.I)
        return (f"Tin ghi địa điểm: <b>{e(raw)}</b> — "
                + ("nơi này ở Việt Nam." if vn else "vùng này bao gồm Việt Nam."))
    if ev.startswith("DQ-02(title)"):
        return f"Nơi chốn nằm trong tiêu đề: <b>{e(ev.split(':', 1)[-1].split('->')[0].strip())}</b>."
    if ev.startswith("A-01(schema)"):
        return ("Công ty tự khai danh sách quốc gia nhận ứng viên trong dữ liệu có cấu trúc, "
                f"và <b>có Việt Nam</b>: <b>{e(ev.split(':', 1)[-1])}</b>")
    if ev.startswith("DQ-09(schema)"):
        return ("Công ty tự khai danh sách quốc gia nhận ứng viên, và <b>không có Việt Nam</b>: "
                f"{e(ev.split(':', 1)[-1])}")
    if ev.startswith("XUNG-DOT:"):
        a, b = (ev[len("XUNG-DOT:"):].split("|", 1) + [""])[:2]
        return ("<b>Hai nguồn mâu thuẫn.</b> Trường địa điểm nói không giới hạn, "
                f"nhưng danh sách quốc gia của công ty chỉ có: {e(b)}. "
                "Chưa đủ căn cứ để kết luận bên nào đúng — hỏi thẳng công ty.")
    if ev.startswith("DQ-09"):
        return ("Dữ liệu có cấu trúc của công ty liệt kê quốc gia nhận ứng viên, "
                "và <b>không có Việt Nam</b>.")
    return f"Trích từ tin: <i>{e(ev)}</i>"


LABEL = {"worldwide": ("Mở toàn cầu", "ok"),
         "vn": ("Mở cho Việt Nam", "ok"),
         "excluded": ("Không mở cho VN", "no"),
         "unknown": ("Chưa xác định", "unk")}
MECH = {"eor": "EOR", "contractor": "Hợp đồng nhà thầu",
        "entity": "Pháp nhân tại VN", "unknown": "Không rõ"}

e = lambda s: html.escape(str(s or ""))


def unent(s):
    """Gỡ entity còn sót trong dữ liệu cũ (nguồn mã hoá hai lần)."""
    t = str(s or "")
    for _ in range(2):
        u = html.unescape(t)
        if u == t:
            break
        t = u
    return re.sub(r"\s+", " ", t).strip()


# ---------- C1–C4: kiểm trước khi render ------------------------------------
def check_no_schema(outdir):
    """C2 — tuyệt đối không có JobPosting schema ở bất kỳ trang nào."""
    bad = []
    for root, _, files in os.walk(outdir):
        for f in files:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                if "JobPosting" in open(p, encoding="utf-8").read():
                    bad.append(p)
    return bad


# ---------- khung trang ------------------------------------------------------
def check_links(outdir):
    """Mọi href nội bộ phải trỏ tới file có thật. Link gãy = mất niềm tin."""
    import urllib.parse
    bad = []
    for root, _, files in os.walk(outdir):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            for href in re.findall(r'href="([^"]+)"', open(p, encoding="utf-8").read()):
                if href.startswith(("http", "mailto:", "#")):
                    continue
                t = os.path.normpath(os.path.join(root, urllib.parse.unquote(href.split("#")[0])))
                if not os.path.exists(t):
                    bad.append(f"{os.path.relpath(p, outdir)} -> {href}")
    return bad


def page(title, body, depth=0, desc=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc or TAGLINE)}">
<link rel="stylesheet" href="{up}assets/fonts.css">
<link rel="stylesheet" href="{up}assets/style.css">
</head><body>
<header><div class="hd"><a class="brand" href="{up}index.html">{e(SITE)}</a>
<nav><a href="{up}index.html">Công ty</a><a href="{up}tin-mo.html">Tin mở</a><a href="{up}chua-xac-dinh.html">Chưa xác định</a><a href="{up}vi-sao-bi-loai.html">Vì sao bị loại</a><a href="{up}phuong-phap.html">Phương pháp</a></nav>
</div></header>
<main>{body}</main>
<footer><div class="ft">
<p>Mọi nhãn đều kèm trích dẫn nguyên văn từ tin gốc. Không trích được thì ghi <b>Chưa xác định</b> — không đoán.</p>
<p>Dữ liệu lấy từ endpoint công khai của Greenhouse, Lever, Ashby. Luôn đọc tin gốc trước khi nộp.
Cập nhật {date.today().isoformat()}.</p>
</div></footer></body></html>"""


def scope(j):
    """Phân biệt 'mở toàn cầu' với 'mở cho Việt Nam'.

    A-02 (địa điểm ghi anywhere/global) = thật sự toàn cầu.
    A-01 (công ty khai nhận VN) và A-03 (vùng/nước có VN, ví dụ APAC, Hà Nội)
    = mở cho người ở VN nhưng KHÔNG phải toàn cầu. Trước đây gộp chung, nên tin
    tuyển ở Hà Nội bị hiện 'Mở toàn cầu' — sai sự thật."""
    if j["eligibility"] != "worldwide":
        return j["eligibility"]
    return "vn" if re.match(r"A-0[13]\b", j.get("evidence") or "") else "worldwide"


def badge(el):
    t, c = LABEL[el]
    return f'<span class="badge {c}">{t}</span>'


def has_page(j):
    """Chỉ tin MỞ TOÀN CẦU mới có trang riêng.

    Với tin bị loại, câu trả lời là "đừng nộp, vì X" — vừa đủ một dòng.
    Bắt người dùng bấm vào để đọc "đừng bấm" là thiết kế ngược. Và nó cắt
    ~96% số trang phải sinh."""
    return j["eligibility"] == "worldwide"


def job_row(j, depth=0):
    up = "../" * depth
    tz = f'<span class="meta">trùng {j["timezone_overlap_gmt7"]}h</span>' if j.get("timezone_overlap_gmt7") else ""
    pay = '<span class="meta">có lương</span>' if j.get("pay_disclosed") else ""
    why = f'<div class="why">{human_evidence(j)}</div>' if j.get("exclusion_reason") else ""
    if has_page(j):
        link = f'<a class="t" href="{up}viec/{e(j["id"])}.html">{e(j["title"])}</a>'
    else:
        link = (f'<a class="t ext" href="{e(j["url"])}" rel="nofollow noopener" target="_blank">'
                f'{e(j["title"])} ↗</a>')
    return f"""<li class="job" data-el="{j['eligibility']}" data-reason="{j.get('exclusion_reason') or ''}"
 data-mech="{j['contract_mechanism']}" data-tz="{j.get('timezone_overlap_gmt7') or 0}" data-pay="{int(bool(j.get('pay_disclosed')))}">
{link}
<div class="c">{e(j['company'])} · <span class="meta">{e(j['location_raw'] or '—')}</span> {tz} {pay}</div>
{badge(scope(j))}{why}</li>"""


# ---------- các trang --------------------------------------------------------
def pager(cur, total, name):
    """Điều hướng trang tĩnh: index.html, index-2.html, ..."""
    if total <= 1:
        return ""
    link = lambda p: (f"{name}.html" if p == 1 else f"{name}-{p}.html")
    out = []
    for p in range(1, total + 1):
        if p == cur:
            out.append(f'<span class="pg cur">{p}</span>')
        elif p <= 2 or p >= total - 1 or abs(p - cur) <= 2:
            out.append(f'<a class="pg" href="{link(p)}">{p}</a>')
        elif out and out[-1] != '<span class="pg">…</span>':
            out.append('<span class="pg">…</span>')
    return f'<nav class="pager">{"".join(out)}</nav>'


def chunk(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)] or [[]]


def density_band(n, depth=0, lab="", unit="tin"):
    """Chữ ký của trang: tỉ lệ ba nhóm vẽ đúng thật.

    Không phải trang trí — dải này LÀ luận điểm. Vệt xanh mỏng cạnh khối đỏ
    cho thấy 3,3% nhanh hơn mọi câu chữ."""
    up = "../" * depth
    tot = sum(n.values()) or 1
    seg = [("open", n["worldwide"], lab or "Mở cho người ở VN", f"{up}tin-mo.html"),
           ("unk", n["unknown"], "Chưa xác định", f"{up}chua-xac-dinh.html"),
           ("closed", n["excluded"], "Không mở cho VN", f"{up}vi-sao-bi-loai.html")]
    bars = "".join(
        f'<a class="seg {c}" style="--w:{100*v/tot:.3f}%" href="{h}" '
        f'title="{lab}: {v:,} {unit}"><span class="segfill"></span></a>' for c, v, lab, h in seg)
    keys = "".join(
        f'<a class="key" href="{h}"><i class="dot {c}"></i>{lab}'
        f'<b>{v:,}</b><em>{100*v/tot:.1f}%</em></a>' for c, v, lab, h in seg)
    return f'<div class="band"><div class="bars">{bars}</div><div class="keys">{keys}</div></div>'


def build_index(jobs):
    n = Counter(j["eligibility"] for j in jobs)
    # Chỉ render tin có thể nộp được. 3.000+ tin bị loại nằm ở trang "vì sao bị loại"
    # — vừa giữ index nhẹ, vừa đúng vai trò từng trang.
    shown = [j for j in jobs if j["eligibility"] == "worldwide"]
    pages = chunk(shown, PER_PAGE)
    nsc = Counter(scope(j) for j in jobs)
    body = f"""
{density_band(n)}
<h1>{e(TAGLINE)}</h1>
<p class="lead">Trong <b>{len(jobs):,}</b> tin remote đã chấm, chỉ <b>{n['worldwide']:,}</b> tin
không vướng giới hạn địa lý nào chặn người ở Việt Nam. Trang này liệt kê đúng
{n['worldwide']:,} tin đó — <b>{nsc['worldwide']:,}</b> mở toàn cầu và
<b>{nsc['vn']:,}</b> mở cho vùng hoặc nước có Việt Nam.
Mỗi nhãn kèm trích dẫn nguyên văn từ tin gốc.</p>

<div class="filters">
<label>Cơ chế <select id="f-mech"><option value="">Tất cả</option>
<option value="eor">EOR</option><option value="contractor">Nhà thầu</option>
<option value="unknown">Không rõ</option></select></label>
<label><input type="checkbox" id="f-pay"> Có công bố lương</label>
<span id="count" class="meta"></span>
</div>

<ul class="jobs">{{rows}}</ul>
{{pg}}
<script src="assets/app.js"></script>"""
    return [page(SITE if i == 0 else f"{SITE} — trang {i+1}",
                 body.format(rows="\n".join(job_row(j) for j in part),
                             pg=pager(i + 1, len(pages), "tin-mo")), 0)
            for i, part in enumerate(pages)]


def build_job(j, jobs):
    same = [x for x in jobs if x["company_slug"] == j["company_slug"] and x["id"] != j["id"]][:6]
    ev = f"""<blockquote>{human_evidence(j)}</blockquote>
<p class="meta">Trích từ: {e({'location':'trường địa điểm','title':'tiêu đề','description':'mô tả công việc','schema':'dữ liệu có cấu trúc'}.get(j['evidence_source'], j['evidence_source']))}</p>""" if j.get("evidence") else \
        "<p class='meta'>Không tìm được câu nào đủ rõ để kết luận. Đây là lý do tin được ghi <b>Chưa xác định</b>.</p>"
    rows = [("Trạng thái", badge(scope(j)))]
    if j.get("exclusion_reason"):
        rows.append(("Lý do", e(REASON.get(j["exclusion_reason"], j["exclusion_reason"]))))
    rows += [("Cơ chế hợp đồng", e(MECH.get(j["contract_mechanism"]))),
             ("Địa điểm ghi trên tin", e(j["location_raw"] or "—")),
             ("Trùng múi giờ với GMT+7", f"{j['timezone_overlap_gmt7']} giờ" if j.get("timezone_overlap_gmt7") else "không nêu"),
             ("Công bố lương", "có" if j.get("pay_disclosed") else "không")]
    tbl = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    rel = ("<h2>Tin khác của công ty này</h2><ul class='jobs'>" +
           "".join(job_row(x, 1) for x in same) + "</ul>") if same else ""
    body = f"""
<p class="crumb"><a href="../tin-mo.html">Tin mở</a> › <a href="../cong-ty/{e(j['company_slug'])}.html">{e(j['company'])}</a></p>
<h1>{e(j['title'])}</h1>
<p class="lead">{e(j['company'])}</p>
<table class="kv">{tbl}</table>
<h2>Bằng chứng</h2>{ev}
<h2>Trích đoạn mô tả</h2>
<p class="excerpt">{e(unent(j['excerpt']))}…</p>
<p><a class="btn" href="{e(j['url'])}" rel="nofollow noopener" target="_blank">Xem tin gốc và nộp tại đó →</a></p>
<p class="meta">Chúng tôi không nhận hồ sơ. Mọi thông tin lấy từ tin gốc do công ty tự công bố.
Nhãn có thể sai — <a href="../phuong-phap.html">xem phương pháp và giới hạn</a>.</p>
{rel}"""
    return page(f"{j['title']} — {j['company']}", body, 1,
                f"{j['title']} tại {j['company']}: {LABEL[scope(j)][0]}")


PER_PAGE = 200      # phân trang khi danh sách vượt ngưỡng này
UNK_CAP = 400


def build_group(head, slug, v, jobs):
    pages = chunk(v, PER_PAGE)
    body = f"""
<p class="crumb"><a href="../vi-sao-bi-loai.html">Vì sao bị loại</a> › {e(head)}</p>
<h1>{e(head)}</h1>
<p class="lead">{len(v):,} tin. Mỗi dòng kèm chuỗi địa điểm nguyên văn trên tin gốc —
đó là căn cứ để kết luận. Bấm tiêu đề để mở tin gốc.</p>
<ul class="rows">{{rows}}</ul>
{{pg}}"""
    rows = lambda part: "".join(
        f"<li class='row'><a class='t ext' href='{e(x['url'])}' rel='nofollow noopener' "
        f"target='_blank'>{e(x['title'])} ↗</a><span class='co'>{e(x['company'])}</span>"
        f"<code class='loc'>{e(x['location_raw'] or '—')}</code></li>" for x in part)
    return [page(f"{head} — {SITE}", body.format(rows=rows(part),
                pg=pager(i + 1, len(pages), slug)), 1) for i, part in enumerate(pages)]


def build_unknown(jobs):
    unk = [j for j in jobs if j["eligibility"] == "unknown"]
    pages = chunk(unk, PER_PAGE)
    more = ""
    body = f"""
{density_band(Counter(j["eligibility"] for j in jobs))}
<h1>{len(unk):,} tin chưa xác định</h1>
<p class="lead">Không tìm được câu nào đủ rõ trong tin để kết luận có mở cho Việt Nam hay không.
<b>Chưa xác định không có nghĩa là không mở</b> — chỉ nghĩa là tin không nói.
Đây là nhóm đáng hỏi thẳng công ty nhất.</p>
<p class="lead">Câu hỏi dùng được ngay:
<i>&ldquo;Nếu người phù hợp nhất đang ở Việt Nam, các bạn trả lương qua EOR hay hợp đồng nhà thầu?&rdquo;</i></p>
{more}
<ul class="jobs">{{rows}}</ul>
{{pg}}"""
    return [page("Chưa xác định — " + SITE, body.format(
                     rows="\n".join(job_row(j) for j in part),
                     pg=pager(i + 1, len(pages), "chua-xac-dinh")), 0)
            for i, part in enumerate(pages)]


REASON_SLUG = {"DQ-01":"giay-phep-lao-dong","DQ-02":"gioi-han-dia-ly","DQ-03":"hinh-thuc-lao-dong",
               "DQ-04":"quoc-tich-clearance","DQ-05":"mui-gio","DQ-06":"phai-den-van-phong",
               "DQ-07":"qua-agency","DQ-09":"schema-khong-co-vn"}


MIN_GROUP = 25      # tổ hợp nước ít hơn ngần này gộp vào "nhiều nước"


def group_excluded(jobs):
    """Nhóm tin bị loại. DQ-02 tách theo NƯỚC — 'chỉ tuyển ở Mỹ' là thông tin,
    'giới hạn địa lý' thì không.

    Nhưng tổ hợp nhiều nước có đuôi rất dài (UAE+Bỉ+Anh+BĐN+Mỹ, 2 tin). Gộp
    những tổ hợp hiếm lại — 300 nhóm mỗi nhóm 2 tin không giúp ai."""
    g = defaultdict(list)
    for j in (x for x in jobs if x["eligibility"] == "excluded"):
        r = j["exclusion_reason"]
        cs = "/".join(countries(j)) if r == "DQ-02" else ""
        g[(r, cs)].append(j)
    small = [k for k, v in g.items() if k[0] == "DQ-02" and k[1] and len(v) < MIN_GROUP]
    if small:
        merged = [j for k in small for j in g.pop(k)]
        g[("DQ-02", "*")] = merged
    out = []
    for (r, cs), v in sorted(g.items(), key=lambda x: -len(x[1])):
        if r == "DQ-02" and cs == "*":
            out.append((f"Nhiều nước, không có Việt Nam", "nhieu-nuoc", v))
            continue
        if r == "DQ-02" and cs:
            names = ", ".join(CNAME.get(c, c) for c in cs.split("/"))
            head, slug = f"Chỉ tuyển ở {names}", "chi-" + cs.lower().replace("/", "-")
        elif r == "DQ-02":
            head, slug = "Giới hạn địa lý (nơi chốn không phân giải được)", "gioi-han-khac"
        else:
            head, slug = REASON.get(r, r), REASON_SLUG.get(r, (r or "khac").lower())
        out.append((head, slug, v))
    return out


def build_why(jobs):
    """Trang mục lục: nhóm + số lượng + ví dụ. Danh sách đầy đủ ở trang riêng."""
    ex = [j for j in jobs if j["eligibility"] == "excluded"]
    secs = []
    for head, slug, v in group_excluded(jobs):
        # Tiêu đề nhóm đã nói lý do. Dòng chỉ cần phần KHÁC NHAU: chuỗi địa điểm gốc.
        ex3 = "".join(
            f"<li class='row'><a class='t ext' href='{e(x['url'])}' rel='nofollow noopener' "
            f"target='_blank'>{e(x['title'])} ↗</a>"
            f"<span class='co'>{e(x['company'])}</span>"
            f"<code class='loc'>{e(x['location_raw'] or '—')}</code></li>" for x in v[:5])
        secs.append(f"""<section><h2><a href="khong-mo/{slug}.html">{e(head)}</a>
<span class="meta">{len(v):,} tin</span></h2>
<ul class="rows">{ex3}</ul>
{f'<p class="meta more"><a href="khong-mo/{slug}.html">Xem đủ {len(v):,} tin →</a></p>' if len(v) > 5 else ''}</section>""")
    body = f"""
{density_band(Counter(j["eligibility"] for j in jobs))}
<h1>Vì sao {len(ex):,} tin bị loại</h1>
<p class="lead">Phần lớn tin có chữ &ldquo;remote&rdquo; <b>không</b> mở cho người ở Việt Nam.
Đây là các lý do, kèm ví dụ có trích dẫn. Biết trước lý do tiết kiệm được 40 phút viết cover letter.</p>
{''.join(secs)}"""
    return page("Vì sao bị loại — " + SITE, body, 0)


def build_company(slug, js, prof):
    """Hồ sơ địa lý tuyển dụng của một công ty — trang lõi của sản phẩm."""
    p = prof
    rows = [("Kết luận", f'<span class="badge {p["verdict"]}">{e(p["vlab"])}</span>'),
            ("Tin remote đang mở", f"{p['n']:,}"),
            ("Cơ chế hợp đồng", e(MECH.get(p["mech"]))),
            ("Nguồn", e(p["source"]))]
    if p["declared"]:
        rows.append(("Công ty tự khai nhận ứng viên tại",
                     e(", ".join(CNAME.get(c, c) for c in p["declared"][:14]))))
    if p["pay"]:
        rows.append(("Tin có công bố lương", f"{p['pay']}/{p['n']}"))
    kv = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)

    # bản đồ địa lý: nước công ty KHOÁ tuyển, xếp theo số tin
    geo = ""
    if p["locked"]:
        tot = sum(p["locked"].values())
        bars = "".join(
            f'<tr><th>{e(CNAME.get(c, c))}</th><td>'
            f'<span class="gbar" style="--w:{100*v/tot:.1f}%"></span> {v}</td></tr>'
            for c, v in p["locked"].most_common(12))
        geo = f"""<h2>Công ty này khoá tuyển vào đâu</h2>
<p class="meta">Đếm theo số tin có mệnh đề giới hạn địa lý. Một tin có thể nêu nhiều nước.</p>
<table class="kv geo">{bars}</table>"""

    why = ""
    if p["reasons"]:
        items = "".join(f"<li>{e(REASON.get(k, k))} — <b>{v}</b> tin</li>"
                        for k, v in p["reasons"].most_common())
        why = f'<h2>Vì sao các tin còn lại bị loại</h2><ul class="plain">{items}</ul>'

    op = [j for j in js if j["eligibility"] == "worldwide"]
    rest = [j for j in js if j["eligibility"] != "worldwide"]
    lists = ""
    if op:
        lists += (f'<h2>Vị trí mở cho người ở Việt Nam <span class="meta">{len(op)}</span></h2>'
                  f'<ul class="jobs">{"".join(job_row(j, 1) for j in op[:200])}</ul>')
    if rest:
        lists += (f'<h2>Vị trí khác <span class="meta">{len(rest)}</span></h2>'
                  f'<ul class="jobs">{"".join(job_row(j, 1) for j in rest[:200])}</ul>')

    body = f"""
<p class="crumb"><a href="../index.html">Công ty</a> › {e(p['name'])}</p>
<h1>{e(p['name'])}</h1>
<table class="kv">{kv}</table>
<p class="meta">Cơ chế hợp đồng và địa lý tuyển là thuộc tính của công ty, không phải của từng
tin — biết một lần dùng cho mọi tin.</p>
{geo}
{why}
{lists}"""
    return page(f"{p['name']} — địa lý tuyển dụng — {SITE}", body, 1,
                f"{p['name']}: {p['vlab'].lower()}. {p['n']} tin remote, kèm trích dẫn.")


def company_profile(js):
    """Gộp mọi tin của một công ty thành một hồ sơ địa lý tuyển dụng.

    Đây là trục chính của sản phẩm. Địa lý tuyển và cơ chế hợp đồng là thuộc tính
    của CÔNG TY, không phải của từng tin — biết một lần dùng cho mọi tin. Tin đổi
    hằng ngày, công ty đổi hằng quý."""
    nsc = Counter(scope(j) for j in js)
    op = [j for j in js if j["eligibility"] == "worldwide"]
    locked = Counter()
    for j in js:
        for c in countries(j):
            locked[c] += 1
    declared = []
    for j in js:
        for c in (j.get("alr_countries") or []):
            if c not in declared:
                declared.append(c)
    if nsc["worldwide"]:
        verdict, vlab = "ok", "Tuyển toàn cầu"
    elif nsc["vn"]:
        verdict, vlab = "ok", "Tuyển được ở Việt Nam"
    elif nsc["unknown"] and not nsc["excluded"]:
        verdict, vlab = "unk", "Chưa xác định"
    elif nsc["unknown"]:
        verdict, vlab = "unk", "Phần lớn khoá, còn tin chưa rõ"
    else:
        verdict, vlab = "no", "Không tuyển ở Việt Nam"
    return dict(
        name=js[0]["company"], slug=js[0]["company_slug"], n=len(js),
        open=len(op), nsc=nsc, verdict=verdict, vlab=vlab,
        locked=locked, declared=declared,
        reasons=Counter(j["exclusion_reason"] for j in js if j["exclusion_reason"]),
        mech=next((j["contract_mechanism"] for j in js
                   if j["contract_mechanism"] != "unknown"), "unknown"),
        source=js[0]["source"],
        pay=sum(1 for j in js if j.get("pay_disclosed")),
    )


def comp_row(p, depth=0):
    up = "../" * depth
    geo = []
    if p["nsc"]["worldwide"]:
        geo.append(f"{p['nsc']['worldwide']} vị trí mở toàn cầu")
    if p["nsc"]["vn"]:
        geo.append(f"{p['nsc']['vn']} vị trí mở cho VN")
    if p["locked"]:
        top = ", ".join(CNAME.get(c, c) for c, _ in p["locked"].most_common(4))
        geo.append(f"khoá vào {top}")
    return f"""<li class="job" data-mech="{e(p['mech'])}" data-pay="{1 if p['pay'] else 0}">
<span class="badge {p['verdict']}">{e(p['vlab'])}</span>
<a class="t" href="{up}cong-ty/{e(p['slug'])}.html">{e(p['name'])}</a>
<div class="c">{p['n']} tin remote · {e(MECH.get(p['mech']))}</div>
<div class="why">{e(' · '.join(geo)) if geo else 'không đủ căn cứ về địa lý tuyển'}</div></li>"""


def build_registry(profiles, nj):
    """Trang chủ: sổ đăng ký công ty, xếp công ty tuyển được lên trước."""
    rank = {"ok": 0, "unk": 1, "no": 2}
    ps = sorted(profiles, key=lambda p: (rank[p["verdict"]], -p["open"], -p["n"], p["name"]))
    nv = Counter(p["verdict"] for p in ps)
    pages = chunk(ps, 200)
    out = []
    for i, part in enumerate(pages):
        head = f"""
{density_band(nj, 0, "Công ty tuyển được ở VN", "công ty")}
<h1>{e(TAGLINE)}</h1>
<p class="lead">Hồ sơ địa lý tuyển dụng của <b>{len(ps):,}</b> công ty, dựng từ
<b>{sum(p['n'] for p in ps):,}</b> tin remote. <b>{nv['ok']}</b> công ty tuyển được người ở
Việt Nam. Mỗi kết luận kèm trích dẫn nguyên văn từ tin gốc.</p>
<p class="meta">Địa lý tuyển và cơ chế hợp đồng là thuộc tính của <b>công ty</b>, không phải của
từng tin. Tin đổi hằng ngày; công ty đổi hằng quý. Xem
<a href="tin-mo.html">danh sách tin đang mở</a> nếu cần trục tin.</p>

<div class="filters">
<label>Cơ chế <select id="f-mech"><option value="">Tất cả</option>
<option value="eor">EOR</option><option value="contractor">Nhà thầu</option>
<option value="unknown">Không rõ</option></select></label>
<label><input type="checkbox" id="f-pay"> Có công bố lương</label>
<span id="count" class="meta" data-unit="công ty"></span>
</div>""" if i == 0 else f'<h1>Công ty <span class="meta">trang {i+1}</span></h1>'
        body = (head + f'\n<ul class="jobs">{"".join(comp_row(p) for p in part)}</ul>'
                + pager(i + 1, len(pages), "index")
                + '\n<script src="assets/app.js"></script>')
        out.append(page(f"{TAGLINE} — {SITE}" if i == 0 else f"Công ty (trang {i+1}) — {SITE}",
                        body, 0,
                        "Hồ sơ địa lý tuyển dụng của công ty, kèm trích dẫn từ tin gốc."))
    return out


def build_method(jobs):
    n = Counter(j["eligibility"] for j in jobs)
    nsc = Counter(scope(j) for j in jobs)
    tot = len(jobs)
    ncomp_ok = len({j["company_slug"] for j in jobs if j["eligibility"] == "worldwide"})
    ncomp = len({j["company"] for j in jobs})
    ww = [j for j in jobs if j["eligibility"] == "worldwide"]
    cc = Counter(j["company"] for j in ww)
    top = cc.most_common(3)
    conc = (f"{len(ww)} tin mở toàn cầu đến từ chỉ <b>{len(cc)} công ty</b>. "
            + " · ".join(f"{e(k)} {v} tin ({100*v/len(ww):.0f}%)" for k, v in top)
            + f". Ba công ty đầu chiếm <b>{100*sum(v for _, v in top)/len(ww):.0f}%</b>.") if ww else ""
    body = f"""
<h1>Phương pháp</h1>
<p class="lead">Độ chính xác chính là sản phẩm. Nên phương pháp phải kiểm tra được.</p>

<h2>Cách chấm</h2>
<p>Mỗi tin đi qua ba tầng: <b>trường địa điểm</b> có cấu trúc → <b>quy tắc loại trừ</b> trên tiêu đề và mô tả →
<b>quy tắc bằng chứng dương</b> chỉ tính khi nằm trong câu nói về điều kiện tuyển dụng.</p>
<p><b>Mọi nhãn phải kèm trích dẫn nguyên văn.</b> Không trích được thì ghi <b>Chưa xác định</b> — không đoán.</p>

<h2>Số liệu hiện tại</h2>
<table class="kv">
<tr><th>Công ty có hồ sơ</th><td>{ncomp:,}</td></tr>
<tr><th>Công ty tuyển được ở Việt Nam</th><td>{ncomp_ok:,} ({100*ncomp_ok/ncomp:.1f}%)</td></tr>
<tr><th>Tin đã chấm</th><td>{tot:,}</td></tr>
<tr><th>Mở toàn cầu</th><td>{nsc['worldwide']:,} ({100*nsc['worldwide']/tot:.1f}%)</td></tr>
<tr><th>Mở cho Việt Nam <span class="muted">(vùng hoặc nước có VN)</span></th><td>{nsc['vn']:,} ({100*nsc['vn']/tot:.1f}%)</td></tr>
<tr><th>Bị giới hạn địa lý</th><td>{n['excluded']:,} ({100*n['excluded']/tot:.1f}%)</td></tr>
<tr><th>Chưa xác định</th><td>{n['unknown']:,} ({100*n['unknown']/tot:.1f}%)</td></tr>
</table>

<h2>Đối chứng tay</h2>
<p>Bộ quy tắc được đối chứng bằng <b>chấm mù</b>: người chấm đọc tin gốc và kết luận độc lập,
không nhìn nhãn máy. Bất đồng thì người thứ hai đọc lại từ đầu và phân xử.</p>

<p><b>Đo riêng chiều &ldquo;mở&rdquo;.</b> Mẫu ngẫu nhiên gần như không chạm nhóm mở toàn cầu —
nhóm đó chỉ chiếm hơn 1% kho. Nên phép đo quan trọng nhất phải <b>lấy mẫu phân tầng</b>:
rút thẳng từ nhóm đã gán &ldquo;mở&rdquo;, đúng nơi sai lầm gây thiệt hại lớn nhất.</p>

<table class="kv">
<tr><th>Đợt 1 — 40 tin ngẫu nhiên</th><td>bắt đúng tin bị loại <b>88,6%</b> · tổng thể <b>85,0%</b></td></tr>
<tr><th>Đợt 2 — 30 tin mới</th><td>bắt đúng tin bị loại <b>100%</b> · tổng thể <b>90,0%</b></td></tr>
<tr><th>Đợt 3 — 40 tin <b>phân tầng</b> từ nhóm &ldquo;mở&rdquo;</th><td>độ chính xác <b>70,0%</b></td></tr>
<tr><th>Đợt 4 — 40 tin phân tầng, sau khi sửa</th><td>độ chính xác <b>90,0%</b></td></tr>
<tr><th>Đợt 5 — 40 tin phân tầng <b>hoàn toàn khác</b></th><td>độ chính xác <b>97,5%</b></td></tr>
<tr><th>Đối chứng cố định 180 tin</th><td>bắt đúng tin bị loại <b>100%</b> · tổng thể <b>100%</b></td></tr>
</table>

<p>Mỗi đợt dùng mẫu <b>không giao</b> với đợt trước. Đo trên chính tập đã dùng để sửa thì
con số vô nghĩa.</p>

<p><b>Đợt 3 là lần đo trung thực đầu tiên.</b> Hai đợt trước lấy ngẫu nhiên nên hầu như chỉ
chạm nhóm bị loại — chiều dễ. Khi rút thẳng từ nhóm &ldquo;mở&rdquo;, độ chính xác thật là 70%.
Con số 90% của đợt 2 không sai, nó chỉ <b>đo nhầm thứ</b>.</p>

<p>Mười loại lỗi tìm ra và đã sửa, mỗi loại đều thuần cơ học:</p>
<ul>
<li><code>SEA</code> trong danh sách thành phố Mỹ là <b>Seattle</b>, bị đọc thành Southeast Asia.</li>
<li><code>Anywhere USA</code>, <code>Remote (anywhere in the U.S.)</code> — mệnh đề thu hẹp ngay
sau từ &ldquo;anywhere&rdquo; bị bỏ qua.</li>
<li><code>Anywhere; Europe</code> — thẻ địa điểm, không phải hai lựa chọn ngang hàng. Nay trả
&ldquo;chưa xác định&rdquo; thay vì &ldquo;mở toàn cầu&rdquo;.</li>
<li><code>Remote, Australia, APAC</code> — Greenhouse ghi phân cấp <i>kiểu làm việc, nước, vùng
cha</i>. APAC ở đây là vùng cha của Australia, không phải địa điểm tuyển thứ hai.</li>
<li>Nhãn địa điểm ghi <code>Global</code> nhưng thân tin liệt kê <b>đóng</b> 15 nước, không có
Việt Nam. Danh sách tường minh nay thắng nhãn chung chung.</li>
<li>Chip <code>Home based - Worldwide</code> dùng lại cho mọi tin của một công ty, trong khi thân
tin ghi <i>Location: this role will be based remotely in the EMEA region</i>.</li>
<li>Câu trong mục phúc lợi (&ldquo;WHY JOIN US&rdquo;, &ldquo;What we offer&rdquo;) nói
&ldquo;work from anywhere&rdquo; là <b>đãi ngộ</b>, không phải phạm vi tuyển. Chỉ tuyên bố tuyển
dụng tường minh (&ldquo;we hire globally&rdquo;) mới được tính.</li>
<li>Múi giờ ngoài Mỹ (<code>CET</code>, <code>EET</code>, <code>BST</code>) và dạng viết đủ chữ
(&ldquo;Pacific Time Zone hours&rdquo;) chưa nằm trong bộ luật.</li>
<li>Tin ghi rõ <code>(On-site)</code> ở trường địa điểm vẫn lọt qua bộ lọc remote vì phần mô tả
có nhắc chữ &ldquo;remote&rdquo;.</li>
<li>Cửa sổ trích dẫn cắt cứng 180 ký tự làm mất chính từ khoá đã khớp.</li>
</ul>

<p><b>Điều một yêu cầu múi giờ KHÔNG chứng minh.</b> &ldquo;Làm giờ EST&rdquo; là yêu cầu ca làm,
không phải yêu cầu nơi ở — người tại Việt Nam làm 20:30&ndash;05:30 giờ Việt vẫn đáp ứng được.
Suy &ldquo;phải làm giờ Mỹ&rdquo; thành &ldquo;phải ở Mỹ&rdquo; là lỗi mà chính người chấm mắc
hai lần, máy thì không.</p>

<h2>Còn sai ở đâu</h2>
<p>97,5% nghĩa là <b>cứ 40 tin gắn nhãn &ldquo;mở&rdquo; thì khoảng 1 tin sai</b>. Khoảng tin cậy
95% cho con số này là 87&ndash;100% — mẫu 40 tin không đủ để phân biệt 97,5% với 92%.</p>
<p>Điểm yếu đã biết: nhóm dựa vào bằng chứng <b>văn xuôi</b> thay vì trường địa điểm có cấu trúc
mỏng manh nhất, vì một câu trong mô tả dễ bị đọc lệch ngữ cảnh hơn một trường dữ liệu.
Có nút báo sai trên mọi tin.</p>

<h2>Nghiên cứu nền</h2>
<p>Đọc tay 150 tin remote ngẫu nhiên: <b>84%</b> bị giới hạn địa lý, <b>4%</b> mở toàn cầu,
<b>0 tin</b> ghi rõ tuyển được ở Việt Nam. Chỉ <b>7,2%</b> tin nêu cơ chế trả lương.
Chỉ <b>25%</b> tin khai trường <code>applicantLocationRequirements</code>.</p>

<h2>Tập trung nguồn — hạn chế lớn nhất hiện tại</h2>
<p>{conc}</p>
<p>Nghĩa là danh sách &ldquo;mở toàn cầu&rdquo; hiện <b>chưa đại diện cho thị trường</b> — nó phản ánh
một số ít công ty thật sự tuyển không giới hạn địa lý. Đang mở rộng nguồn.</p>

<h2>Giới hạn — đọc kỹ phần này</h2>
<ul>
<li>Chỉ ba nền tảng ATS: Greenhouse, Lever, Ashby. Không có Workday, SmartRecruiters, hay công ty tuyển qua trang riêng.</li>
<li>Danh sách công ty thiên về công ty Mỹ và châu Âu. Đây là nơi có nhiều việc remote nhất, chưa chắc là nơi tuyển người Việt nhiều nhất.</li>
<li>Đây là ảnh chụp một thời điểm. Tin tuyển dụng đổi liên tục.</li>
<li>Nhãn <b>Chưa xác định</b> nghĩa là chưa đủ bằng chứng — không có nghĩa là không mở.</li>
<li><b>Luôn đọc tin gốc trước khi nộp.</b> Trang này giúp lọc, không thay thế việc đọc.</li>
</ul>

<h2>Thấy nhãn sai?</h2>
<p>Nhãn sai là lỗi nặng nhất trang này có thể mắc — nó tiêu đúng thứ nó hứa tiết kiệm.
Báo lại kèm link tin, sẽ sửa và ghi nhận.</p>"""
    return page("Phương pháp — " + SITE, body, 0)


CSS = """/* Bảng màu: giấy sổ cái xanh-xám + ba sắc tố đất.
   Ba màu phán quyết bão hoà thấp để đọc như MỰC DẤU, không như badge trạng thái. */
:root{
  --paper:#F0F1EC; --card:#FBFBF8; --ink:#14171A; --ink-2:#4B5158; --ink-3:#858C93;
  --rule:#D9DBD3; --rule-2:#E7E9E2;
  --open:#0F6E4A; --open-bg:#E2EDE6; --closed:#8C2F26; --closed-bg:#F1E4E2;
  --unk:#8A6F2F; --unk-bg:#EFE9DA;
  --sans:"Be Vietnam Pro",system-ui,sans-serif;      /* thiết kế riêng cho tiếng Việt */
  --serif:"Newsreader",Georgia,serif;
  --mono:"IBM Plex Mono",ui-monospace,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
  font:400 15.5px/1.65 var(--sans);font-feature-settings:"kern","liga"}

/* ---------- khung ---------- */
header{border-bottom:1px solid var(--rule);background:var(--card);position:sticky;top:0;z-index:5}
.hd{max-width:960px;margin:0 auto;padding:13px 22px;display:flex;gap:26px;align-items:baseline;flex-wrap:wrap}
.brand{font:500 16px/1 var(--serif);letter-spacing:-.01em;color:var(--ink);text-decoration:none}
nav{display:flex;gap:20px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
nav::-webkit-scrollbar{display:none}
nav a{font:500 12.5px/1 var(--sans);letter-spacing:.02em;color:var(--ink-2);text-decoration:none;white-space:nowrap;
  padding-bottom:2px;border-bottom:1.5px solid transparent}
nav a:hover{color:var(--ink);border-bottom-color:var(--ink)}
main{max-width:960px;margin:0 auto;padding:30px 22px 72px}
footer{border-top:1px solid var(--rule);margin-top:56px}
.ft{max-width:960px;margin:0 auto;padding:24px 22px 52px;color:var(--ink-3);
  font:400 12.5px/1.7 var(--mono)}
.ft p{margin:5px 0}

/* ---------- chữ ký: dải mật độ ---------- */
.band{margin:0 0 34px}
.bars{display:flex;height:18px;border:1px solid var(--rule);background:var(--card);overflow:hidden}
.seg{width:var(--w);min-width:2px;display:block;text-decoration:none;position:relative}
.seg+.seg{border-left:1px solid var(--card)}
.segfill{position:absolute;inset:0;transform:scaleX(0);transform-origin:left;
  animation:grow .7s cubic-bezier(.2,.8,.3,1) forwards}
.seg.open .segfill{background:var(--open);animation-delay:.05s}
.seg.unk .segfill{background:var(--unk);animation-delay:.13s}
.seg.closed .segfill{background:var(--closed);animation-delay:.21s}
@keyframes grow{to{transform:scaleX(1)}}
.keys{display:flex;gap:24px;flex-wrap:wrap;margin-top:11px}
.key{display:flex;align-items:baseline;gap:7px;text-decoration:none;color:var(--ink-2);
  font:400 11.5px/1 var(--mono);letter-spacing:.02em}
.key:hover{color:var(--ink)}
.key b{font:500 13px/1 var(--mono);color:var(--ink)}
.key em{font-style:normal;color:var(--ink-3)}
.dot{width:8px;height:8px;border-radius:1px;display:inline-block;transform:translateY(1px)}
.dot.open{background:var(--open)}.dot.closed{background:var(--closed)}.dot.unk{background:var(--unk)}

/* ---------- chữ ---------- */
h1{font:500 clamp(28px,4.6vw,42px)/1.12 var(--serif);letter-spacing:-.022em;margin:0 0 14px;max-width:20ch}
h2{font:500 21px/1.3 var(--serif);letter-spacing:-.012em;margin:38px 0 12px}
.lead{color:var(--ink-2);margin:0 0 14px;max-width:66ch}
.lead a{color:var(--ink);text-decoration-thickness:1px;text-underline-offset:3px}
.crumb{font:400 12px/1 var(--mono);color:var(--ink-3);margin:0 0 16px}
.crumb a{color:var(--ink-3)}
a{color:#0B4F8F}

/* ---------- bộ lọc ---------- */
.filters{display:flex;gap:18px;flex-wrap:wrap;align-items:center;padding:12px 14px;
  background:var(--card);border:1px solid var(--rule);margin:0 0 4px;
  font:400 12.5px/1 var(--mono);color:var(--ink-2)}
.filters select{font:400 12.5px var(--mono);padding:5px 7px;border:1px solid var(--rule);
  background:var(--paper);color:var(--ink)}
#count{margin-left:auto;color:var(--ink-3)}

/* ---------- sổ phán quyết ---------- */
ul.jobs{list-style:none;padding:0;margin:0}
ul.rows{list-style:none;padding:0;margin:0}
li.row{display:grid;grid-template-columns:1fr auto;gap:2px 16px;align-items:baseline;
  padding:8px 0;border-bottom:1px solid var(--rule-2)}
li.row .t{font:400 14.5px/1.4 var(--sans)}
li.row .co{grid-row:2;font:400 12px/1.4 var(--mono);color:var(--ink-3)}
li.row .loc{grid-column:2;grid-row:1/3;align-self:center;background:var(--card);
  border:1px solid var(--rule-2);padding:3px 7px;font:400 11.5px/1.4 var(--mono);
  color:var(--ink-2);max-width:34ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
p.more{margin:10px 0 0;font:400 12px/1 var(--mono)}
@media(max-width:640px){li.row{grid-template-columns:1fr}li.row .loc{grid-column:1;grid-row:auto;max-width:100%}}
li.job{display:grid;grid-template-columns:max-content 1fr;gap:0 18px;
  padding:15px 0;border-bottom:1px solid var(--rule-2);align-items:start}
li.job .t{grid-column:2;font:500 15.5px/1.4 var(--sans);color:var(--ink);text-decoration:none}
li.job .t:hover{text-decoration:underline;text-underline-offset:3px}
li.job .t.ext{color:#0B4F8F}
li.job .c{grid-column:2;font:400 12.5px/1.5 var(--mono);color:var(--ink-3);margin-top:3px}
li.job .why{grid-column:2;font:400 12.5px/1.55 var(--mono);color:var(--ink-2);
  margin-top:7px;padding-left:11px;border-left:2px solid var(--rule)}
li.job .why b{font-weight:500;color:var(--ink)}
.badge{grid-column:1;grid-row:1/99;justify-self:start;
  font:600 10.5px/1 var(--sans);letter-spacing:.055em;text-transform:uppercase;
  padding:5px 8px;border:1px solid currentColor;white-space:nowrap}
.badge.ok{color:var(--open);background:var(--open-bg)}
.badge.no{color:var(--closed);background:var(--closed-bg)}
.badge.unk{color:var(--unk);background:var(--unk-bg)}
.meta{color:var(--ink-3)}
/* thanh mật độ trong bảng địa lý tuyển của công ty */
table.geo td{white-space:nowrap}
.gbar{display:inline-block;height:9px;width:var(--w);min-width:2px;
  background:var(--closed);opacity:.55;vertical-align:middle;margin-right:7px}
ul.plain{list-style:none;padding:0;margin:10px 0}
ul.plain li{padding:6px 0;border-bottom:1px solid var(--rule-2);
  font:400 13.5px/1.5 var(--sans)}

/* ---------- trang chi tiết ---------- */
table.kv{border-collapse:collapse;width:100%;margin:16px 0 4px}
table.kv th{text-align:left;padding:10px 16px 10px 0;width:38%;vertical-align:top;
  border-bottom:1px solid var(--rule-2);
  font:400 11.5px/1.5 var(--mono);letter-spacing:.03em;text-transform:uppercase;color:var(--ink-3)}
table.kv td{padding:10px 0;border-bottom:1px solid var(--rule-2);font:400 14.5px/1.5 var(--sans)}
blockquote{margin:0;padding:15px 18px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--ink);font:400 14px/1.6 var(--mono);color:var(--ink)}
blockquote b{font-weight:500}
.excerpt{color:var(--ink-2);font-size:14.5px;max-width:70ch}
.btn{display:inline-block;background:var(--ink);color:var(--card);padding:12px 20px;
  text-decoration:none;font:600 14px/1 var(--sans);letter-spacing:.01em;margin:6px 0}
.btn:hover{background:#000}
section{margin-bottom:30px}
code{font:400 12.5px var(--mono);background:var(--card);border:1px solid var(--rule-2);padding:1px 5px}
ul li{margin:4px 0}

/* ---------- phân trang ---------- */
.pager{margin:30px 0 0;display:flex;gap:5px;flex-wrap:wrap}
.pg{padding:6px 11px;border:1px solid var(--rule);background:var(--card);
  font:400 12.5px/1 var(--mono);color:#0B4F8F;text-decoration:none}
.pg.cur{background:var(--ink);color:var(--card);border-color:var(--ink)}

:focus-visible{outline:2px solid #0B4F8F;outline-offset:2px}
@media (prefers-reduced-motion:reduce){.segfill{animation:none;transform:scaleX(1)}}
@media (max-width:640px){
  main{padding:22px 16px 56px}
  .hd{padding:12px 16px;gap:12px}
  .ft{padding:20px 16px 44px}
  /* phán quyết đọc TRƯỚC tiêu đề — thứ tự dọc phải khớp thứ tự ưu tiên */
  li.job{grid-template-columns:1fr;gap:0}
  .badge{grid-column:1;grid-row:1;margin-bottom:8px;justify-self:start}
  li.job .t{grid-column:1;grid-row:2}
  li.job .c{grid-column:1;grid-row:3}
  li.job .why{grid-column:1;grid-row:4}
  .keys{gap:6px 16px}
  .filters{gap:12px}
  #count{margin-left:0}
}
"""

JS = """(function(){
// Script nạp trên mọi trang, nhưng chỉ trang danh sách mới có ô lọc.
// Bản cũ tham chiếu thẳng nên ném lỗi và bộ lọc chết trên chính trang chủ.
var items=[].slice.call(document.querySelectorAll('li.job')),
    mech=document.getElementById('f-mech'),
    pay=document.getElementById('f-pay'),
    count=document.getElementById('count'),
    ctl=[mech,pay].filter(Boolean);
if(!ctl.length||!items.length)return;
function apply(){var n=0;
  items.forEach(function(li){
    var ok=(!mech||!mech.value||li.dataset.mech===mech.value)
        && (!pay||!pay.checked||li.dataset.pay==='1');
    li.style.display=ok?'':'none'; if(ok)n++;});
  if(count)count.textContent=n.toLocaleString('vi-VN')+' '+(count.dataset.unit||'tin');}
ctl.forEach(function(x){x.addEventListener('change',apply)});apply();})();"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default="jobs.json")
    ap.add_argument("--out", default="site")
    a = ap.parse_args()

    jobs = json.load(open(a.jobs, encoding="utf-8"))
    jobs = [j for j in jobs if j.get("status") == "open"]          # C3
    jobs.sort(key=lambda j: (j["eligibility"] != "worldwide", j["company"], j["title"]))

    errs = validate(jobs)
    if errs:
        print(f"BUILD DỪNG — {len(errs)} vi phạm ràng buộc:", file=sys.stderr)
        for x in errs[:20]:
            print("  " + x, file=sys.stderr)
        sys.exit(1)

    # Font tải một lần bằng tools/fetch_fonts.py. build.py xoá sạch site/ mỗi
    # lần, nên phải cất font RA NGOÀI thư mục sắp xoá.
    import tempfile
    keep = os.path.join(a.out, "assets", "fonts")
    fcss = os.path.join(a.out, "assets", "fonts.css")
    stash = None
    fcss_data = open(fcss, encoding="utf-8").read() if os.path.exists(fcss) else None
    if os.path.isdir(keep):
        stash = os.path.join(tempfile.gettempdir(), "site-fonts-stash")
        shutil.rmtree(stash, ignore_errors=True)
        shutil.move(keep, stash)
    if os.path.exists(a.out):
        shutil.rmtree(a.out)
    for d in ("", "viec", "cong-ty", "assets"):
        os.makedirs(os.path.join(a.out, d), exist_ok=True)
    w = lambda p, s: open(os.path.join(a.out, p), "w", encoding="utf-8").write(s)

    if stash:
        shutil.move(stash, keep)
    if fcss_data:
        w("assets/fonts.css", fcss_data)
    else:
        print("  ! chưa có assets/fonts.css — chạy tools/fetch_fonts.py", file=sys.stderr)
    w("assets/style.css", CSS)
    w("assets/app.js", JS)
    bycomp = defaultdict(list)
    for j in jobs:
        bycomp[j["company_slug"]].append(j)
    profiles = {k: company_profile(v) for k, v in bycomp.items()}
    nv = Counter(p["verdict"] for p in profiles.values())
    for i, h in enumerate(build_registry(
            list(profiles.values()),
            # dải trên trang chủ đếm CÔNG TY, không phải tin — trang này là trục công ty
            Counter(worldwide=nv["ok"], unknown=nv["unk"], excluded=nv["no"]))):
        w("index.html" if i == 0 else f"index-{i+1}.html", h)
    for i, h in enumerate(build_index(jobs)):
        w("tin-mo.html" if i == 0 else f"tin-mo-{i+1}.html", h)
    w("vi-sao-bi-loai.html", build_why(jobs))
    os.makedirs(os.path.join(a.out, "khong-mo"), exist_ok=True)
    for head, slug, v in group_excluded(jobs):
        for i, h in enumerate(build_group(head, slug, v, jobs)):
            w(f"khong-mo/{slug}.html" if i == 0 else f"khong-mo/{slug}-{i+1}.html", h)
    for i, h in enumerate(build_unknown(jobs)):
        w("chua-xac-dinh.html" if i == 0 else f"chua-xac-dinh-{i+1}.html", h)
    w("phuong-phap.html", build_method(jobs))
    detail = [j for j in jobs if has_page(j)]
    for j in detail:
        w(f"viec/{j['id']}.html", build_job(j, jobs))
    for slug, js in bycomp.items():
        w(f"cong-ty/{slug}.html", build_company(slug, js, profiles[slug]))

    broken = check_links(a.out)
    if broken:
        print(f"BUILD DỪNG — {len(broken)} link nội bộ gãy:", file=sys.stderr)
        for x in broken[:15]:
            print("  " + x, file=sys.stderr)
        sys.exit(1)

    bad = check_no_schema(a.out)
    if bad:
        print(f"BUILD DỪNG — C2: {len(bad)} trang có JobPosting schema", file=sys.stderr)
        sys.exit(1)

    n = Counter(j["eligibility"] for j in jobs)
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(a.out) for f in fs)
    print(f"✓ {a.out}/  —  {len(bycomp):,} công ty · {nv['ok']} tuyển được ở VN · "
          f"{len(jobs):,} tin · {len(detail):,} trang chi tiết · {size/1e6:.1f} MB")
    print(f"   công ty: mở {nv['ok']} · chưa rõ {nv['unk']} · khoá {nv['no']}")
    print(f"   tin: mở toàn cầu {n['worldwide']:,} · bị loại {n['excluded']:,} · chưa xác định {n['unknown']:,}")
    print("   C1 trích dẫn ✓  C2 không schema ✓  C3 chỉ tin đang mở ✓  C4 trích đoạn ≤300 ✓  link nội bộ ✓")


if __name__ == "__main__":
    main()
