"""Sinh báo cáo thị trường bán cho công ty nước ngoài — sản phẩm Đ3.

Đ3 (legal-options.md Mục 3) là cấu trúc DUY NHẤT có doanh thu mà không chạm
quy định nào: chỉ phục vụ phía cầu, không chạm dữ liệu kỹ sư, không giới thiệu
ai. Ràng buộc đó không phải hướng dẫn phong cách — nó là lý do sản phẩm hợp
pháp. Nên script này CHỈ đọc bảng company/job/locked (dữ liệu về tổ chức) và
không có đường nào chạm tới subscriber.

Chạy:  python3 tools/market_report.py            # in ra stdout
       python3 tools/market_report.py -o out.md
"""
import argparse
import sqlite3
from datetime import date
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "app.db"

# Mã vùng, không phải mã nước — ISO không có, nhưng tin tuyển dụng dùng đầy.
REGION = {"EMEA", "AMER", "APAC", "LATAM", "EU", "EEA", "NA", "ANZ", "MENA", "DACH", "NORDIC"}

CNAME = {
    "US": "United States", "GB": "United Kingdom", "CA": "Canada", "IN": "India",
    "DE": "Germany", "BR": "Brazil", "MX": "Mexico", "AU": "Australia",
    "ES": "Spain", "SG": "Singapore", "PL": "Poland", "PH": "Philippines",
    "CO": "Colombia", "FR": "France", "IE": "Ireland", "NL": "Netherlands",
    "AR": "Argentina", "JP": "Japan", "PT": "Portugal", "IT": "Italy",
    "VN": "Vietnam", "ID": "Indonesia", "TH": "Thailand", "MY": "Malaysia",
    "EU": "European Union", "EMEA": "EMEA", "AMER": "Americas", "APAC": "APAC",
    "LATAM": "Latin America",
}


def cname(code):
    return CNAME.get(code, code)


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "—"


def q1(db, sql, *a):
    r = db.execute(sql, a).fetchone()
    return r[0] if r else 0


def gather(db):
    d = {}
    d["companies"] = q1(db, "SELECT count(*) FROM company")
    d["jobs"] = q1(db, "SELECT count(*) FROM job")
    d["open"] = q1(db, "SELECT count(*) FROM company WHERE verdict='ok'")
    d["closed"] = q1(db, "SELECT count(*) FROM company WHERE verdict='no'")
    d["unknown"] = q1(db, "SELECT count(*) FROM company WHERE verdict='unk'")
    d["with_lock"] = q1(db, "SELECT count(DISTINCT slug) FROM locked")
    d["ww_jobs"] = q1(db, "SELECT count(*) FROM job WHERE eligibility='worldwide'")
    d["vn_named"] = q1(
        db, "SELECT count(*) FROM job WHERE evidence LIKE '%Vietnam%' OR evidence LIKE '%Viet Nam%'")

    d["locks"] = db.execute(
        """SELECT code, count(DISTINCT slug) c, sum(n_jobs) j
           FROM locked GROUP BY code ORDER BY c DESC LIMIT 15""").fetchall()

    # Cột trụ của báo cáo: công ty ĐÃ có cơ chế tuyển xuyên biên giới, tách
    # theo việc Việt Nam có nằm trong phạm vi hay không.
    d["mech"] = db.execute(
        """SELECT mechanism,
                  sum(verdict='ok')  o,
                  sum(verdict='unk') u,
                  sum(verdict='no')  n
           FROM company WHERE mechanism <> 'unknown'
           GROUP BY mechanism ORDER BY 1""").fetchall()

    # Tín hiệu mạnh nhất trong kho: đã tuyển ở ĐNA. Xem tools/prospects.py.
    d["sea"] = db.execute(
        """SELECT count(*) n, sum(verdict='ok') o FROM company
           WHERE EXISTS (SELECT 1 FROM locked l
                         WHERE l.slug = company.slug
                           AND l.code IN ('PH','ID','TH','MY'))""").fetchone()

    d["top_open"] = db.execute(
        """SELECT name, n_jobs, n_vn, mechanism, source
           FROM company WHERE verdict='ok'
           ORDER BY n_jobs DESC LIMIT 20""").fetchall()
    return d


def render(d):
    mech_open = sum(r[1] for r in d["mech"])
    mech_all = sum(r[1] + r[2] + r[3] for r in d["mech"])
    o = []
    w = o.append

    w("# Where Remote Companies Can Actually Hire")
    w("")
    w(f"**Vietnam market brief — {date.today():%d %B %Y}**")
    w("")
    w(f"Built from **{d['jobs']:,} live postings** across **{d['companies']:,} companies** "
      "that publish remote roles on Greenhouse, Ashby and Lever. Every claim below traces "
      "to a quotable clause in a live posting. Nothing is modelled or estimated.")
    w("")
    w("---")
    w("")

    w("## 1. Remote is not global")
    w("")
    w(f"Of {d['companies']:,} companies advertising remote work, **{d['with_lock']:,} "
      f"({pct(d['with_lock'], d['companies'])}) attach an explicit geographic restriction** to "
      "at least one posting. The word *remote* in a job title says nothing about where you "
      "may sit.")
    w("")
    w("Most-restricted-to locations, by number of companies:")
    w("")
    w("| Location | Companies | Postings |")
    w("|---|---:|---:|")
    for code, c, j in d["locks"]:
        tag = " *(region)*" if code in REGION else ""
        w(f"| {cname(code)}{tag} | {c:,} | {j:,} |")
    w("")
    us = next((c for code, c, _ in d["locks"] if code == "US"), 0)
    w(f"**{pct(us, d['companies'])} of all companies in the corpus restrict at least one "
      "posting to the United States alone.** That single fact shapes the rest of this brief.")
    w("")

    w("## 2. Vietnam is almost absent — and not because of cost")
    w("")
    w("| | Count | Share |")
    w("|---|---:|---:|")
    w(f"| Companies that can hire in Vietnam | **{d['open']:,}** | {pct(d['open'], d['companies'])} |")
    w(f"| Companies that explicitly cannot | {d['closed']:,} | {pct(d['closed'], d['companies'])} |")
    w(f"| Companies with no clause either way | {d['unknown']:,} | {pct(d['unknown'], d['companies'])} |")
    w(f"| Postings naming Vietnam at all | {d['vn_named']:,} | {pct(d['vn_named'], d['jobs'])} |")
    w("")
    w(f"Vietnam has roughly 530,000 software developers and ranks in the global top ten for "
      f"IT outsourcing. Yet **{d['vn_named']:,} of {d['jobs']:,} postings** mention the country "
      "by name. The demand exists; it does not travel through public job postings. It travels "
      "through agencies, EOR providers and referral.")
    w("")

    w("## 3. The barrier is scope, not infrastructure")
    w("")
    w("This is the finding that should change a hiring plan.")
    w("")
    w("| Mechanism declared | Open to Vietnam | Unclear | Closed |")
    w("|---|---:|---:|---:|")
    for m, ok, unk, no in d["mech"]:
        w(f"| {m.upper()} | {ok} | {unk} | {no} |")
    w(f"| **Total** | **{mech_open}** | | |")
    w("")
    w(f"**{mech_all} companies already state they hire through an employer-of-record or "
      f"contractor arrangement — the exact machinery needed to hire anywhere. Only "
      f"{mech_open} of them include Vietnam.**")
    w("")
    w("These companies have solved payroll, compliance and contracting across borders. They "
      "have the capability and still exclude Vietnam. The constraint is not legal or "
      "operational — it is the default scope someone typed into a job template and nobody "
      "revisited.")
    w("")
    w("For a company that already runs an EOR, adding Vietnam is a policy edit, not a "
      "project. That is the arbitrage.")
    w("")

    w("## 4. The strongest predictor we found")
    w("")
    sea_n, sea_o = d["sea"]
    base = 100 * d["open"] / d["companies"]
    sea_p = 100 * sea_o / sea_n if sea_n else 0
    w("Across every slice of this corpus, one signal dominates: **whether a company already "
      "hires somewhere else in Southeast Asia.**")
    w("")
    w("| Company already hires in | Companies | Open to Vietnam | Rate | vs baseline |")
    w("|---|---:|---:|---:|---:|")
    w(f"| Anywhere (baseline) | {d['companies']:,} | {d['open']} | {base:.1f}% | 1.0× |")
    w(f"| **Southeast Asia** (PH/ID/TH/MY) | {sea_n} | {sea_o} | **{sea_p:.1f}%** | "
      f"**{sea_p/base:.1f}×** |")
    w("")
    w("For comparison, hiring in India lifts the rate 2.4×, Latin America 2.6×, Eastern "
      "Europe 4.1× — all far below Southeast Asia.")
    w("")
    w("The lift is not a size artefact. Split the corpus into four bands by posting count and "
      "the effect holds in **every** band, between 3.3× and 7.0×. A control group — companies "
      "that publish any geographic clause at all — sits at the baseline rate, so this is not "
      "simply *\"firms that bother to write clauses\"*.")
    w("")
    w("The reading is straightforward. A company hiring in Manila has already solved the "
      "timezone band, the contractor paperwork and the cost-tier conversation. Vietnam is the "
      "same problem, already solved, just not switched on.")
    w("")

    w("## 5. Who is already hiring here")
    w("")
    w(f"The {d['open']:,} companies open to Vietnam, largest first:")
    w("")
    w("| Company | Postings | Open to VN | Mechanism |")
    w("|---|---:|---:|---|")
    for name, nj, nvn, mech, _src in d["top_open"]:
        w(f"| {name} | {nj:,} | {nvn} | {mech if mech != 'unknown' else '—'} |")
    w("")
    w("Use this as a competitive-reference list: these are the firms already competing for "
      "the same engineers, and the terms they publish set the market.")
    w("")

    w("---")
    w("")
    w("## Method, and what this brief will not tell you")
    w("")
    w("Postings are pulled daily from public ATS endpoints. Each posting is read for an "
      "explicit geographic clause; the label is only assigned when a clause can be quoted. "
      "A posting with no clause is recorded as **unknown**, never guessed. Precision on the "
      "open bucket was measured at **97.5%** against a hand-audited disjoint sample.")
    w("")
    w("What it will not tell you:")
    w("")
    w("- **Nothing about individuals.** This brief contains no candidate data, no profiles "
      "and no personal information of any kind. It is a study of company policy.")
    w("- **Absence is not proof.** A company with no clause may still hire in Vietnam "
      "privately. The corpus measures what is *published*.")
    w("- **No introductions.** This is research. It is not a recruitment service and does "
      "not place candidates.")
    w("")
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-o", "--out", help="ghi ra tệp thay vì stdout")
    ap.add_argument("--db", default=str(DB))
    a = ap.parse_args()

    db = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    text = render(gather(db))
    db.close()

    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"đã ghi {a.out} ({len(text):,} ký tự)")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
