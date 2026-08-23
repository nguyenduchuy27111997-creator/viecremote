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
CODE.update({"US": "the US", "GB": "the UK", "AE": "the UAE"})
SITE = "https://viec-remote.nguyenduchuy27111997.workers.dev/hiring-in-vietnam"


def name_of(code):
    return CODE.get(code, code)


def display(slug_name):
    """Tên trong kho là slug ATS ("chaosindustries"). Làm cho đọc được, nhưng
    KHÔNG đoán chỗ tách từ — "Chaosindustries" sai ít hơn "Chaos Industries"
    đoán bừa. Người gửi phải sửa lại cho đúng trước khi bấm gửi."""
    return re.sub(r"[-_]+", " ", slug_name).strip().title()


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


def pick(db, proof, n):
    v = "verdict='ok'" if proof else "verdict='no'"
    return db.execute(
        f"""SELECT name, mechanism, n_jobs, locked FROM company
            WHERE mechanism <> 'unknown' AND {v}
            ORDER BY n_jobs DESC LIMIT ?""", (n,)).fetchall()


def target_mail(name, mech, n_jobs, where, s):
    """Thư cho công ty CÓ bộ máy mà loại Việt Nam."""
    name = display(name)
    mech_word = "employer-of-record" if mech == "eor" else "contractor"
    mech_label = "an EOR" if mech == "eor" else "contractor"
    if where:
        shown = ", ".join(name_of(c) for c in where[:5])
        line = (f"Your postings show you already hire through {mech_word} arrangements "
                f"in {len(where)} places — {shown}. Vietnam is not among them.")
    else:
        line = (f"Your postings show you already hire through {mech_word} arrangements. "
                "None of them extend to Vietnam.")
    return wrap(f"""Subject: {name} hires via {mech_label} in {len(where) or 'several'} countries — not Vietnam

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
    name = display(name)
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
    rows = pick(db, a.proof, a.n)
    write = proof_mail if a.proof else target_mail

    print(f"\n{'='*78}\n{len(rows)} thư — ĐỌC LẠI TRƯỚC KHI GỬI. Kho không có địa chỉ, tự tìm.\n{'='*78}")
    for name, mech, n_jobs, locked in rows:
        where = [c for c, _ in json.loads(locked or "[]")]
        print(f"\n{'-'*78}\n### {display(name)}  ·  {mech}  ·  {n_jobs} tin\n{'-'*78}")
        print(write(name, mech, n_jobs, where, s))
    db.close()


if __name__ == "__main__":
    main()
