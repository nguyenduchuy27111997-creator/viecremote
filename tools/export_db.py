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

# --- Định nghĩa bảng, dùng chung cho SQLite cục bộ và D1 ---------------------
# {S} là hậu tố: rỗng khi dựng bản cục bộ, "_new" khi sinh seed cho D1.
# Không có FOREIGN KEY: nó cản việc đổi tên bảng lúc hoán đổi, và SQLite mặc
# định không thực thi FK — nên nó chỉ là chú thích tốn phí.
TABLES = """
CREATE TABLE IF NOT EXISTS company{S} (
  slug        TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  verdict     TEXT NOT NULL,
  verdict_label TEXT NOT NULL,
  n_jobs      INTEGER NOT NULL,
  n_global    INTEGER NOT NULL,
  n_vn        INTEGER NOT NULL,
  n_excluded  INTEGER NOT NULL,
  n_unknown   INTEGER NOT NULL,
  mechanism   TEXT NOT NULL,
  source      TEXT NOT NULL,
  n_pay       INTEGER NOT NULL,
  locked      TEXT NOT NULL,
  declared    TEXT NOT NULL,
  reasons     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS job{S} (
  id           TEXT PRIMARY KEY,
  company_slug TEXT NOT NULL,
  title        TEXT NOT NULL,
  location_raw TEXT,
  url          TEXT NOT NULL,
  source       TEXT NOT NULL,
  eligibility  TEXT NOT NULL,
  scope        TEXT NOT NULL,
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

CREATE TABLE IF NOT EXISTS meta{S} (k TEXT PRIMARY KEY, v TEXT NOT NULL);
"""

# Chỉ mục và FTS tạo SAU khi hoán đổi — tên chỉ mục là toàn cục trong một CSDL,
# nên không thể tồn tại song song hai bản.
INDEXES = """
CREATE INDEX IF NOT EXISTS company_verdict ON company(verdict, n_global DESC, n_jobs DESC);
CREATE INDEX IF NOT EXISTS company_mech    ON company(mechanism);
CREATE INDEX IF NOT EXISTS job_company     ON job(company_slug, scope);
CREATE INDEX IF NOT EXISTS job_scope       ON job(scope);
DROP TABLE IF EXISTS company_fts;
CREATE VIRTUAL TABLE company_fts USING fts5(slug UNINDEXED, name, tokenize='unicode61');
INSERT INTO company_fts (slug, name) SELECT slug, name FROM company;
"""

# Bảng do NGƯỜI DÙNG ghi. Không phái sinh từ jobs.json, không dựng lại được.
# CREATE IF NOT EXISTS và TUYỆT ĐỐI không nằm trong luồng hoán đổi.
USER_TABLES = """
CREATE TABLE IF NOT EXISTS report (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  kind       TEXT NOT NULL,
  ref        TEXT NOT NULL,
  reason     TEXT NOT NULL,
  note       TEXT,
  created_at TEXT NOT NULL,
  resolved   INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS report_open ON report(resolved, created_at DESC);
"""

SCHEMA = TABLES.replace("{S}", "") + INDEXES + USER_TABLES


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
    """Sinh SQL để nạp vào D1 — NGUYÊN TỬ.

    Vấn đề: 13 tệp seed chạy tuần tự. Đứt giữa chừng (mạng, hết hạn mức, Ctrl-C)
    để lại CSDL nửa vời — và trang production sẽ phục vụ đúng cái nửa vời đó.

    Cách giải: nạp vào bảng `*_new`, chỉ đến TỆP CUỐI mới hoán đổi. Cửa sổ dữ
    liệu không nhất quán rút từ "cả quá trình nạp" xuống "một tệp DROP+RENAME".
    Đứt trước tệp cuối thì bảng cũ còn nguyên, trang vẫn chạy dữ liệu hôm qua.

    Không dùng iterdump: nó xuất bảng bóng FTS5 dưới dạng ghi thẳng vào
    sqlite_master, và D1 từ chối. Hai mức chia: 40 dòng/câu lệnh (D1 trả
    SQLITE_TOOBIG nếu câu quá dài), 4.000 dòng/tệp (một lần execute có trần riêng).
    """
    files, n = [], 0

    def emit(name, lines):
        nonlocal n
        path = os.path.join(outdir, f"seed-{n:02d}-{name}.sql")
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        files.append(path)
        n += 1

    def stmts(sql):
        return [x.strip() + ";" for x in sql.split(";") if x.strip()
                and not x.strip().startswith("PRAGMA")]

    # 1. Bảng người dùng (không bao giờ đụng) + bảng tạm sạch
    emit("schema", stmts(USER_TABLES)
         + [f"DROP TABLE IF EXISTS {t}_new;" for t in ("company", "job", "meta")]
         + stmts(TABLES.replace("{S}", "_new")))

    # 2. Dữ liệu -> bảng tạm
    for table in ("company", "job", "meta"):
        cols = [r[1] for r in db.execute(f"PRAGMA table_info({table})")]
        rows = db.execute(f"SELECT {','.join(cols)} FROM {table}").fetchall()
        for i in range(0, len(rows), per_file):
            part = rows[i:i + per_file]
            emit(table, [
                f"INSERT INTO {table}_new ({','.join(cols)}) VALUES "
                + ",".join("(" + ",".join(q(v) for v in r) + ")" for r in part[k:k + per_stmt])
                + ";"
                for k in range(0, len(part), per_stmt)])

    # 3. Hoán đổi — tệp DUY NHẤT làm dữ liệu cũ biến mất. Chạy cuối cùng.
    #
    # THỨ TỰ QUAN TRỌNG: con trước, cha sau. D1 THỰC THI foreign key (khác
    # SQLite mặc định), và schema cũ có `job.company_slug REFERENCES company`.
    # Drop `company` khi `job` còn tham chiếu -> SQLITE_CONSTRAINT_FOREIGNKEY.
    # Bảng mới không có FK nên đây là vấn đề một lần, nhưng thứ tự phải đúng
    # ở mọi lần chạy vì có thể nạp lên một CSDL còn schema cũ.
    emit("swap",
         [f"DROP TABLE IF EXISTS {t}; ALTER TABLE {t}_new RENAME TO {t};"
          for t in ("job", "company", "meta")]
         + stmts(INDEXES))

    tot = sum(os.path.getsize(f) for f in files)
    print(f"✓ {len(files)} tệp seed trong {outdir}/ — {tot/1e6:.1f} MB tổng")
    print(f"  tệp cuối ({os.path.basename(files[-1])}) là bước hoán đổi — "
          f"đứt trước nó thì dữ liệu cũ còn nguyên")


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
