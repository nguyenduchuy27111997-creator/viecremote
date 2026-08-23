"""Soạn thư chào hàng Đ3 — điền số liệu thật cho từng công ty.

Không gửi. In ra để người đọc lại rồi tự gửi: thư lạnh dưới danh nghĩa ai thì
người đó bấm gửi. Kho cũng không có địa chỉ liên hệ nào — phải tự tìm.

Hai luận điểm khác nhau, dùng nhầm là hỏng:

  --targets  (mặc định)  Công ty có EOR/contractor mà LOẠI Việt Nam.
                         Luận điểm: bạn đã trả tiền cho bộ máy rồi, Việt Nam
                         là một dòng cấu hình, không phải một dự án.
  --proof                Công ty ĐÃ mở cho Việt Nam.
                         Luận điểm KHÁC HẲN: họ không thiếu gì. Bán cho họ là
                         bán so sánh đối thủ, không phải bán cơ hội bỏ lỡ.

Ràng buộc Đ3 (legal-options.md Mục 3) áp thẳng vào câu chữ: KHÔNG hứa ứng
viên, KHÔNG hứa giới thiệu, KHÔNG nhận hồ sơ. Bán nghiên cứu chính sách tuyển
dụng. Thư nào hứa quá là kéo cả sản phẩm vào diện dịch vụ việc làm có điều kiện.

Chạy:  python3 tools/outreach.py -n 7
       python3 tools/outreach.py --proof
"""
import argparse
import json
import re
import sqlite3
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from country import ISO  # noqa: E402

DB = Path(__file__).resolve().parent.parent / "data" / "app.db"
CODE = {v: k.title() for k, v in ISO.items()}
CODE.update({"US": "the US", "GB": "the UK", "AE": "the UAE", "PH": "the Philippines",
             "NL": "the Netherlands", "CZ": "Czechia"})
SITE = "https://viec-remote.nguyenduchuy27111997.workers.dev/hiring-in-vietnam"


def name_of(code):
    return CODE.get(code, code)


# Tên trong kho là SLUG ATS, không phải tên công ty. Gửi thư mở đầu bằng
# "Flyzipline" là hỏng ngay dòng đầu.
#
# Bản đồ này chỉ chứa tên CÓ CĂN CỨ: hoặc suy từ tên miền riêng trong chính
# URL tin tuyển dụng (đánh dấu # url), hoặc là tên thương hiệu phổ biến mà
# cách viết hoa là công khai. Không đoán bừa — slug nào không có ở đây thì
# dọn máy móc rồi ĐÁNH DẤU để người gửi tự kiểm.
NAMES = {
    "flyzipline": "Zipline",            # url: www.zipline.com
    "housecall": "Housecall Pro",       # url: www.housecallpro.com
    "gostudent": "GoStudent",           # url: www.gostudent.org
    "asana": "Asana",                   # url: www.asana.com
    "upstart": "Upstart",               # url: careers.upstart.com
    "lokalise": "Lokalise",             # url: lokalise.com
    "sisense": "Sisense",               # url: www.sisense.com
    "aligned": "Aligned",               # url: alignedup.com
    "twilio": "Twilio",
    "reddit": "Reddit",
    "snowflake": "Snowflake",
    "chainguard": "Chainguard",
    "betterhelp": "BetterHelp",
    "planetlabs": "Planet Labs",
    "chaosindustries": "Chaos Industries",
    "cloverhealth": "Clover Health",
    "pingidentity": "Ping Identity",
    "scaleai": "Scale AI",
    "openloophealth": "OpenLoop Health",
    "nice": "NICE",
    "lilt-production": "Lilt",
    "agency": "Meridial",               # board: <title>Jobs at Meridial</title>, alt="Meridial Logo"
    "bjakcareer": "BJAK",               # bjak.com og:site_name="BJAK"; thân tin viết "ABOUT BJAK"
    "learnlux": "LearnLux",             # board: <title>Jobs at LearnLux</title>
    "lumimeds": "LumiMeds",             # lumimeds.com <title>… | LumiMeds</title>
    "remotecom": "Remote",
    "ashby": "Ashby",
    "watershed": "Watershed",
    "rula": "Rula",
}

# Đuôi do ATS gắn thêm, không thuộc tên công ty. Bóc được mà không phải đoán.
SLUG_TAIL = re.compile(
    r"(?:[-_]?(?:production|staging|careers?|jobs?|talent ?pool|internal ?use ?only|"
    r"corporate ?careers?|referral ?board|hq|inc|llc)\b|\d+)+$", re.I)


def display(slug_name):
    """-> (tên hiển thị, có chắc không).

    Chắc = có trong NAMES. Không chắc = tự dọn từ slug, người gửi phải kiểm.
    KHÔNG đoán chỗ tách từ: "Bjakcareer" -> "Bjak" chứ không thành "BJAK",
    vì viết hoa sai tên thương hiệu đọc còn tệ hơn viết thường."""
    key = (slug_name or "").strip().lower()
    if key in NAMES:
        return NAMES[key], True
    cleaned = SLUG_TAIL.sub("", key)
    return re.sub(r"[-_]+", " ", cleaned or key).strip().title(), False


def wrap(t):
    """Ngắt dòng 78 ký tự, giữ nguyên dòng trống và dòng thụt đầu."""
    out = []
    for para in t.split("\n\n"):
        # Giữ nguyên: dòng chủ đề, dòng có URL (ngắt là hỏng link), và mọi khối
        # có dòng thụt đầu — chữ ký thụt dòng bị gộp lại thì đọc như lỗi.
        if (para.startswith("Subject:") or "://" in para
                or any(l.startswith((" ", "\t")) for l in para.splitlines())):
            out.append(para)
        else:
            out.append(textwrap.fill(para, 78))
    return "\n\n".join(out)


def stats(db):
    g = lambda s: db.execute(s).fetchone()[0]
    return {
        "total": g("SELECT count(*) FROM company"),
        "jobs": g("SELECT count(*) FROM job"),
        "open": g("SELECT count(*) FROM company WHERE verdict='ok'"),
        "mech": g("SELECT count(*) FROM company WHERE mechanism<>'unknown'"),
        "mech_ok": g("SELECT count(*) FROM company WHERE mechanism<>'unknown' AND verdict='ok'"),
    }


# Loại khỏi DANH SÁCH GỬI THƯ, KHÔNG loại khỏi kho.
#
# Phân biệt này quan trọng: cả ba vẫn thật sự mở cho Việt Nam, nên con số
# "9/200 công ty có cơ chế mở cho VN" giữ nguyên — đó là dữ kiện đo được.
# Chỉ là gửi thư chào hàng cho họ thì vô nghĩa.
SKIP = {
    "remotecom": "bán EOR — đối thủ/nhà cung cấp, không phải khách",
    "remotereferralboardinternaluseonly": "bảng nội bộ của chính Remote.com — trùng",
    "enveritas": "phi lợi nhuận, 4 tin — không tuyển ở quy mô cần mua nghiên cứu",
}


# Tín hiệu mạnh nhất trong kho — xem tools/prospects.py để biết cách đo.
SEA = {"PH", "ID", "TH", "MY"}


def pick(db, proof, n):
    v = "verdict='ok'" if proof else "verdict='no'"
    rows = db.execute(
        f"""SELECT name, mechanism, n_jobs, locked FROM company
            WHERE mechanism <> 'unknown' AND {v}""").fetchall()
    # Đã tuyển ở ĐNA lên trước: "bạn đã giải bài này ở Philippines rồi" là câu
    # mở đầu mạnh hơn hẳn một danh sách nước chung chung.
    rows.sort(key=lambda r: (not ({c for c, _ in json.loads(r[3] or "[]")} & SEA),
                             -r[2]))
    keep, dropped = [], []
    for r in rows:
        (dropped if r[0].lower() in SKIP else keep).append(r)
        if len(keep) == n:
            break
    return keep, dropped


def target_mail(name, mech, n_jobs, where, s):
    """Thư cho công ty CÓ bộ máy mà loại Việt Nam."""
    name, _sure = display(name)
    mech_word = "employer-of-record" if mech == "eor" else "contractor"
    mech_label = "an EOR" if mech == "eor" else "contractor"
    sea = sorted(set(where) & SEA)
    if sea:
        # Câu mở mạnh nhất có được: cùng múi giờ, cùng bậc chi phí, cùng kiểu
        # hợp đồng. Không phải "bạn thiếu một nước" mà "bạn đã làm đúng việc này rồi".
        line = (f"You already hire in {' and '.join(name_of(c) for c in sea)} through "
                f"{mech_word} arrangements. Vietnam sits in the same timezone band, the same "
                "cost tier, and takes the same contracting paperwork you have already done — "
                "but it is not in your scope.")
    elif where:
        shown = ", ".join(name_of(c) for c in where[:5])
        line = (f"Your postings show you already hire through {mech_word} arrangements "
                f"in {len(where)} places — {shown}. Vietnam is not among them.")
    else:
        line = (f"Your postings show you already hire through {mech_word} arrangements. "
                "None of them extend to Vietnam.")
    subject = (f"{name} hires in {' and '.join(name_of(c) for c in sea)} — why not Vietnam?"
               if sea else
               f"{name} hires via {mech_label} in {len(where) or 'several'} countries — not Vietnam")
    return wrap(f"""Subject: {subject}

Hi,

I maintain a study of where remote companies are actually allowed to hire. It
reads {s['jobs']:,} live postings across {s['total']:,} companies and records the geographic
clause each one states, quoted verbatim.

{line}

That gap is the finding worth your time: {s['mech']} companies in the corpus already
declare EOR or contractor hiring — the exact machinery needed to hire anywhere —
and only {s['mech_ok']} of them include Vietnam. The constraint is almost never legal or
operational. It is the default scope typed into a job template years ago.

Vietnam has ~530,000 developers and sits in the global top ten for IT
outsourcing, yet fewer than 0.2% of postings name it. If you already run {mech_word} arrangements, adding it is a policy edit, not a project.

The summary is public: {SITE}

I also produce a fuller brief — country-by-country breakdown, the {s['open']} companies
already hiring there, the mechanisms they use, and what their published terms
imply about rates. Happy to send it over if useful.

To be clear about what this is: research into published company policy. I do
not place candidates, make introductions, or hold any candidate data.

— Huy
   Reply "no thanks" and I won't write again.
""")


def proof_mail(name, mech, n_jobs, where, s):
    """Thư cho công ty ĐÃ mở — luận điểm là so sánh đối thủ, không phải cơ hội bỏ lỡ."""
    name, _sure = display(name)
    mech_label = "an EOR" if mech == "eor" else "contractor arrangements"
    return wrap(f"""Subject: {name} is one of {s['mech_ok']} companies hiring in Vietnam via {mech_label}

Hi,

I maintain a study of where remote companies are actually allowed to hire —
{s['jobs']:,} live postings across {s['total']:,} companies, each geographic clause quoted verbatim.

{name} came up because you are unusual. Of the {s['mech']} companies that declare EOR or
contractor hiring, only {s['mech_ok']} extend it to Vietnam. You are one of them.

That means you are competing for those engineers against a field of {s['open']} companies,
not {s['total']:,} — and most of your peers have not noticed the opening yet. The brief
lays out who the other {s['open'] - 1} are, which mechanisms they use, and what their published
terms imply about rates, so you can see where your offer sits.

The summary is public: {SITE}

What this is not: I do not place candidates, make introductions, or hold any
candidate data. It is research into published company policy.

— Huy
   Reply "no thanks" and I won't write again.
""")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--proof", action="store_true")
    ap.add_argument("-n", type=int, default=7)
    ap.add_argument("--db", default=str(DB))
    a = ap.parse_args()

    db = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    s = stats(db)
    rows, dropped = pick(db, a.proof, a.n)
    write = proof_mail if a.proof else target_mail

    print(f"\n{'='*78}\n{len(rows)} thư — ĐỌC LẠI TRƯỚC KHI GỬI. Kho không có địa chỉ, tự tìm.\n{'='*78}")

    # Tên suy từ slug có thể sai. Nêu ngay đầu ra thay vì để lẫn trong thư —
    # sai tên ở dòng đầu thư lạnh là mất luôn người đọc.
    if dropped:
        print(f"\n   Bỏ qua {len(dropped)} công ty (vẫn nằm trong kho, chỉ không gửi thư):")
        for slug, *_ in dropped:
            print(f"     {slug:<40} {SKIP[slug.lower()]}")

    unsure = [(slug, display(slug)[0]) for slug, *_ in rows if not display(slug)[1]]
    if unsure:
        print(f"\n⚠  {len(unsure)}/{len(rows)} tên suy từ slug, CHƯA kiểm chứng — sửa trước khi gửi:")
        for slug, guess in unsure:
            print(f"     {slug:<40} -> {guess}")
        print("   (thêm tên đúng vào NAMES trong tools/outreach.py để lần sau khỏi sửa)")

    for name, mech, n_jobs, locked in rows:
        where = [c for c, _ in json.loads(locked or "[]")]
        print(f"\n{'-'*78}\n### {display(name)[0]}  ·  {mech}  ·  {n_jobs} tin\n{'-'*78}")
        print(write(name, mech, n_jobs, where, s))
    db.close()


if __name__ == "__main__":
    main()
