#!/usr/bin/env python3
"""
jobs.json -> SQLite (data/app.db) + seed.sql cho Cloudflare D1.

Vì sao có tầng này: ở 2.410 công ty, nhét cả kho vào bundle còn được. Ở 10.000+
thì không — và trang phải tra cứu được theo tên, theo nước bị khoá, theo cơ chế.
Đó là truy vấn, không phải lọc mảng trong trình duyệt.

Bảng `company` là TRỤC CHÍNH (xem business-model.md Mục 1). Bảng `job` là lá.

    python3 tools/export_db.py                 # ghi data/app.db + data/seed.sql
    python3 tools/export_db.py --no-sql        # chỉ SQLite, bỏ qua seed.sql
"""
import argparse, glob, html, json, os, re, sqlite3, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gates import enforce

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS company (
  slug        TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  verdict     TEXT NOT NULL,          -- ok | unk | no
  verdict_label TEXT NOT NULL,
  n_jobs      INTEGER NOT NULL,
  n_global    INTEGER NOT NULL,       -- vị trí mở toàn cầu
  n_vn        INTEGER NOT NULL,       -- vị trí mở cho vùng/nước có VN
  n_excluded  INTEGER NOT NULL,
  n_unknown   INTEGER NOT NULL,
  mechanism   TEXT NOT NULL,
  source      TEXT NOT NULL,
  n_pay       INTEGER NOT NULL,
  locked      TEXT NOT NULL,          -- JSON [[mã nước, số tin], ...]
  declared    TEXT NOT NULL,          -- JSON [tên nước công ty tự khai]
  reasons     TEXT NOT NULL           -- JSON [[mã DQ, số tin], ...]
);
CREATE INDEX IF NOT EXISTS company_verdict ON company(verdict, n_global DESC, n_jobs DESC);
CREATE INDEX IF NOT EXISTS company_mech    ON company(mechanism);

CREATE TABLE IF NOT EXISTS job (
  id           TEXT PRIMARY KEY,
  company_slug TEXT NOT NULL REFERENCES company(slug),
  title        TEXT NOT NULL,
  location_raw TEXT,
  url          TEXT NOT NULL,
  source       TEXT NOT NULL,
  eligibility  TEXT NOT NULL,
  scope        TEXT NOT NULL,         -- worldwide | vn | excluded | unknown
  reason       TEXT,
  evidence     TEXT,
  evidence_src TEXT,
  tz_overlap   INTEGER,
  mechanism    TEXT,
  pay          INTEGER NOT NULL,
  excerpt      TEXT,
  first_seen   TEXT,
  last_seen    TEXT
);
CREATE INDEX IF NOT EXISTS job_company ON job(company_slug, scope);
CREATE INDEX IF NOT EXISTS job_scope   ON job(scope);

-- tra cứu tên công ty: FTS5 rẻ hơn LIKE '%x%' ở 10.000+ dòng
CREATE VIRTUAL TABLE IF NOT EXISTS company_fts USING fts5(
  slug UNINDEXED, name, tokenize='unicode61'
);

CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT NOT NULL);

-- Báo sai nhãn. Sứ mệnh gọi tỷ lệ báo sai là CHỈ SỐ SỐNG CÒN.
-- KHÔNG có cột nào chứa dữ liệu cá nhân: không email, không IP, không tài khoản.
-- Nhờ đó giữ nguyên miễn trừ DPO/DPIA của Nghị định 356/2025.
CREATE TABLE IF NOT EXISTS report (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  kind       TEXT NOT NULL,          -- job | company
  ref        TEXT NOT NULL,          -- job.id hoặc company.slug
  reason     TEXT NOT NULL,
  note       TEXT,
  created_at TEXT NOT NULL,
  resolved   INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS report_open ON report(resolved, created_at DESC);
"""


def unent(v):
    """Gỡ entity HTML còn sót.

    Một số ATS mã hoá hai lần ("&amp;nbsp;"), nên giải một lần vẫn còn "&nbsp;"
    và nó hiện thô trên trang. Giải cho tới khi ổn định."""
    if not isinstance(v, str):
        return v
    for _ in range(3):
        u = html.unescape(v)
        if u == v:
            break
        v = u
    return re.sub(r"\s+", " ", v).strip()


def job_scope(j):
    """A-01/A-03 = mở cho VN nhưng KHÔNG phải toàn cầu. Gộp chung là sai sự thật."""
    if j["eligibility"] != "worldwide":
        return j["eligibility"]
    return "vn" if re.match(r"A-0[13]\b", j.get("evidence") or "") else "worldwide"


def locked_codes(j):
    ev = j.get("evidence") or ""
    if not ev.startswith("DQ-02(location)") or "|" not in ev:
        return []
    return [c for c in ev.split("|")[-1].split("/") if c]


def profile(js):
    sc = Counter(job_scope(j) for j in js)
    locked = Counter()
    for j in js:
        locked.update(locked_codes(j))
    declared = []
    for j in js:
        for c in (j.get("alr_countries") or []):
            if c not in declared:
                declared.append(c)
    if sc["worldwide"]:
        v, lab = "ok", "Tuyển toàn cầu"
    elif sc["vn"]:
        v, lab = "ok", "Tuyển được ở Việt Nam"
    elif sc["unknown"] and not sc["excluded"]:
        v, lab = "unk", "Chưa xác định"
    elif sc["unknown"]:
        v, lab = "unk", "Phần lớn khoá, còn tin chưa rõ"
    else:
        v, lab = "no", "Không tuyển ở Việt Nam"
    return dict(
        slug=js[0]["company_slug"], name=unent(js[0]["company"]), verdict=v, verdict_label=lab,
        n_jobs=len(js), n_global=sc["worldwide"], n_vn=sc["vn"],
        n_excluded=sc["excluded"], n_unknown=sc["unknown"],
        mechanism=next((j["contract_mechanism"] for j in js
                        if j["contract_mechanism"] != "unknown"), "unknown"),
        source=js[0]["source"],
        n_pay=sum(1 for j in js if j.get("pay_disclosed")),
        locked=json.dumps(locked.most_common(), ensure_ascii=False),
        declared=json.dumps(declared[:20], ensure_ascii=False),
        reasons=json.dumps(Counter(j["exclusion_reason"] for j in js
                                   if j["exclusion_reason"]).most_common(),
                           ensure_ascii=False),
    )


def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def write_seed(db, outdir, per_file=4000, per_stmt=40):
    """Sinh SQL tường minh, chia mảnh.

    Không dùng iterdump: nó xuất cả bảng bóng của FTS5 dưới dạng ghi thẳng vào
    sqlite_master, và D1 từ chối ('table sqlite_master may not be modified').
    Hai mức chia: mỗi CÂU LỆNH tối đa 40 dòng (D1 trả SQLITE_TOOBIG nếu câu quá
    dài), mỗi TỆP tối đa 4.000 dòng (một lần execute có trần riêng)."""
    # Xoá seed cũ trước: số tệp đổi theo kích thước kho, nên lần chạy sau có thể
    # để lại tệp thừa của lần trước và nạp meta/fts hai lần.
    for old in glob.glob(os.path.join(outdir, "seed-*.sql")):
        os.remove(old)
    files, n = [], 0

    def emit(name, lines):
        nonlocal n
        path = os.path.join(outdir, f"seed-{n:02d}-{name}.sql")
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        files.append(path)
        n += 1

    emit("schema", [ln.strip() + ";" for ln in SCHEMA.split(";")
                    if ln.strip() and not ln.strip().startswith("PRAGMA")])

    for table in ("company", "job", "meta"):
        cols = [r[1] for r in db.execute(f"PRAGMA table_info({table})")]
        rows = db.execute(f"SELECT {','.join(cols)} FROM {table}").fetchall()
        for i in range(0, len(rows), per_file):
            part = rows[i:i + per_file]
            emit(table, [
                f"INSERT INTO {table} ({','.join(cols)}) VALUES "
                + ",".join("(" + ",".join(q(v) for v in r) + ")" for r in part[k:k + per_stmt])
                + ";"
                for k in range(0, len(part), per_stmt)])

    emit("fts", ["INSERT INTO company_fts (slug, name) SELECT slug, name FROM company;"])
    # `report` do người dùng ghi — schema tạo nếu chưa có, nhưng KHÔNG bao giờ
    # xoá hay ghi đè. Seed hằng ngày không được làm mất báo cáo.
    tot = sum(os.path.getsize(f) for f in files)
    print(f"✓ {len(files)} tệp seed trong {outdir}/ — {tot/1e6:.1f} MB tổng")
    print(f"  nạp: for f in {outdir}/seed-*.sql; do npx wrangler d1 execute "
          f"viec-remote --local --file=../$f; done")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default="jobs.json")
    ap.add_argument("--out", default="data/app.db")
    ap.add_argument("--no-sql", action="store_true")
    a = ap.parse_args()

    jobs = json.load(open(a.jobs, encoding="utf-8"))
    jobs = [j for j in jobs if j.get("status", "open") == "open"]
    # Cùng năm cổng mà build.py dùng. Không có bản này thì luồng Next.js là
    # đường vòng lách qua ràng buộc — luồng lỏng hơn sẽ là luồng lên production.
    enforce(jobs, "XUẤT DB")
    by = defaultdict(list)
    for j in jobs:
        by[j["company_slug"]].append(j)
    profs = [profile(v) for v in by.values()]

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    if os.path.exists(a.out):
        os.remove(a.out)
    db = sqlite3.connect(a.out)
    db.executescript(SCHEMA)

    cols = list(profs[0].keys())
    db.executemany(f"INSERT INTO company ({','.join(cols)}) VALUES ({','.join('?'*len(cols))})",
                   [tuple(p[c] for c in cols) for p in profs])
    db.executemany("INSERT INTO company_fts (slug, name) VALUES (?,?)",
                   [(p["slug"], p["name"]) for p in profs])   # bản cục bộ; D1 nạp riêng
    db.executemany(
        "INSERT INTO job (id,company_slug,title,location_raw,url,source,eligibility,scope,"
        "reason,evidence,evidence_src,tz_overlap,mechanism,pay,excerpt,first_seen,last_seen) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [(j["id"], j["company_slug"], unent(j["title"]), unent(j.get("location_raw")),
          j["url"], j["source"],
          j["eligibility"], job_scope(j), j.get("exclusion_reason"), unent(j.get("evidence")),
          j.get("evidence_source"), j.get("timezone_overlap_gmt7"),
          j.get("contract_mechanism"), 1 if j.get("pay_disclosed") else 0,
          unent(j.get("excerpt")), j.get("first_seen"), j.get("last_seen")) for j in jobs])

    nv = Counter(p["verdict"] for p in profs)
    nsc = Counter(job_scope(j) for j in jobs)
    db.executemany("INSERT INTO meta (k,v) VALUES (?,?)", [
        ("built_at", __import__("datetime").date.today().isoformat()),
        ("n_companies", str(len(profs))), ("n_jobs", str(len(jobs))),
        ("n_comp_ok", str(nv["ok"])), ("n_comp_unk", str(nv["unk"])),
        ("n_comp_no", str(nv["no"])),
        ("n_job_global", str(nsc["worldwide"])), ("n_job_vn", str(nsc["vn"])),
        ("n_job_excluded", str(nsc["excluded"])), ("n_job_unknown", str(nsc["unknown"])),
    ])
    db.commit()

    print(f"✓ {a.out} — {len(profs):,} công ty ({nv['ok']} tuyển được ở VN) · {len(jobs):,} tin")
    if not a.no_sql:
        write_seed(db, os.path.dirname(a.out) or ".")
    db.close()


if __name__ == "__main__":
    main()
