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

-- Bảng nối công ty <-> nước bị khoá, tính sẵn từ cột `locked` (JSON).
-- Vì sao không truy vấn json_each lúc chạy: nó quét toàn bảng, không dùng được
-- chỉ mục. Đây là dữ liệu GIÀU NHẤT ta có (2.324/3.666 công ty) và trước đó
-- không có đường nào vào nó.
CREATE TABLE IF NOT EXISTS locked{S} (
  code    TEXT NOT NULL,
  slug    TEXT NOT NULL,
  n_jobs  INTEGER NOT NULL,
  PRIMARY KEY (code, slug)
);
"""

# Chỉ mục và FTS tạo SAU khi hoán đổi — tên chỉ mục là toàn cục trong một CSDL,
# nên không thể tồn tại song song hai bản.
INDEXES = """
CREATE INDEX IF NOT EXISTS company_verdict ON company(verdict, n_global DESC, n_jobs DESC);
CREATE INDEX IF NOT EXISTS company_mech    ON company(mechanism);
CREATE INDEX IF NOT EXISTS job_company     ON job(company_slug, scope);
CREATE INDEX IF NOT EXISTS job_scope       ON job(scope);
CREATE INDEX IF NOT EXISTS locked_code      ON locked(code, n_jobs DESC);
CREATE INDEX IF NOT EXISTS locked_slug      ON locked(slug);
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

-- Đăng ký nhận tin. KHÁC MỌI BẢNG KHÁC: email LÀ dữ liệu cá nhân.
-- Hệ quả (xem legal-brief.md): phải có double opt-in, phải có đường rút lui
-- một cú bấm, và phải nêu trong trang riêng tư. Dưới 100.000 chủ thể nên vẫn
-- giữ được miễn trừ DPO/DPIA của Nghị định 356/2025 — theo dõi con số này.
CREATE TABLE IF NOT EXISTS subscriber (
  email        TEXT PRIMARY KEY,
  token        TEXT NOT NULL UNIQUE,
  confirmed    INTEGER NOT NULL DEFAULT 0,
  created_at   TEXT NOT NULL,
  confirmed_at TEXT
);
CREATE INDEX IF NOT EXISTS subscriber_token ON subscriber(token);

-- Khoá API. Lưu SHA-256 của khoá, không lưu khoá thô: rò cơ sở dữ liệu thì
-- kẻ lấy được cũng không gọi API được.
--
-- CẢNH BÁO PHÁP LÝ trước khi bán API: Điều 27.1 Luật Việc làm 74/2025 xếp
-- "thu thập, phân tích, lưu trữ, cung cấp thông tin về thị trường lao động"
-- vào dịch vụ việc làm — cần giấy phép. API miễn phí thì ngoài phạm vi;
-- API TRẢ PHÍ kích hoạt nhóm này. Xem legal-options.md Mục 2.
CREATE TABLE IF NOT EXISTS api_key (
  hash       TEXT PRIMARY KEY,
  label      TEXT NOT NULL,
  created_at TEXT NOT NULL,
  revoked    INTEGER NOT NULL DEFAULT 0
);

-- Yêu cầu báo cáo thị trường từ công ty nước ngoài — sản phẩm Đ3.
--
-- Chỉ dữ liệu TỔ CHỨC và một email liên hệ công việc. KHÔNG có trường nào cho
-- dữ liệu kỹ sư, và không được thêm: Đ3 hợp pháp không cần giấy phép CHÍNH VÌ
-- nó không chạm dữ liệu người lao động và không giới thiệu ai (legal-options.md
-- Mục 3). Thêm một cột "ứng viên" vào đây là đổi hẳn chế độ pháp lý áp dụng.
CREATE TABLE IF NOT EXISTS inquiry (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  company    TEXT NOT NULL,
  email      TEXT NOT NULL,
  role       TEXT,
  note       TEXT,
  created_at TEXT NOT NULL,
  handled    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS inquiry_open ON inquiry(handled, created_at DESC);

-- Lịch sử ĐỔI NHÃN công ty. Chỉ ghi khi có thay đổi, không chụp ảnh mỗi ngày.
--
-- Kho dựng lại mỗi ngày và GHI ĐÈ, nên nếu không ghi ở đây thì mỗi ngày trôi
-- qua là một ngày lịch sử mất vĩnh viễn. Không ai khác đang thu dữ liệu này:
-- "công ty nào vừa mở, vừa đóng cho Việt Nam" là thứ chỉ có được bằng cách
-- quan sát liên tục, không mua lại được sau.
--
-- Ba tháng nữa nó trả lời được câu mà hôm nay không ai trả lời được.
CREATE TABLE IF NOT EXISTS verdict_change (
  slug       TEXT NOT NULL,
  from_v     TEXT NOT NULL,
  to_v       TEXT NOT NULL,
  changed_at TEXT NOT NULL,
  PRIMARY KEY (slug, changed_at)
);
CREATE INDEX IF NOT EXISTS verdict_change_when ON verdict_change(changed_at DESC);

-- ------------------------------------------------------------------ L2, TẮT
-- Bảng dựng sẵn, KHÔNG có dòng nào cho tới khi L2_ENABLED được bật (web/src/lib/l2.ts).
--
-- Ràng buộc C6 ("không hồ sơ nào rời hệ thống mà thiếu đồng ý cho ĐÚNG công ty
-- đó") được ép bằng KHOÁ NGOẠI GHÉP, không phải bằng kiểm tra ở tầng ứng dụng:
-- transfer trỏ tới (consent_id, company_slug) và (agreement_id, company_slug),
-- nên không thể ghi một lần chuyển giao mà đồng ý lại thuộc công ty khác.
-- D1 CÓ bật khoá ngoại, khác SQLite mặc định — nên đây là ràng buộc thật.

CREATE TABLE IF NOT EXISTS engineer (
  id          TEXT PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  created_at  TEXT NOT NULL,
  -- Điều 25.1.c Luật 91/2025: không tuyển thì phải xoá. Cột này là hạn chót,
  -- không phải gợi ý — tools/gates_l2.py chặn build nếu quá hạn mà còn dữ liệu.
  purge_after TEXT NOT NULL
);

-- Đồng ý THEO TỪNG LẦN CHUYỂN GIAO, đúng NĐ 356 Điều 7.3.a. Một dòng cho một
-- (kỹ sư, công ty, mục đích). KHÔNG có dạng "đồng ý cho mọi đối tác" — muốn có
-- cũng không biểu diễn được trong lược đồ này, và đó là chủ ý.
CREATE TABLE IF NOT EXISTS consent (
  id            TEXT PRIMARY KEY,
  engineer_id   TEXT NOT NULL REFERENCES engineer(id) ON DELETE CASCADE,
  company_slug  TEXT NOT NULL,
  purpose       TEXT NOT NULL,
  -- Nguyên văn màn hình kỹ sư đã đọc lúc bấm đồng ý. Điều 7.3.a buộc họ "được
  -- biết chính xác mục đích chuyển giao, tổ chức tiếp nhận" — lưu lại thì mới
  -- chứng minh được là đã cho biết.
  shown_text    TEXT NOT NULL,
  granted_at    TEXT NOT NULL,
  revoked_at    TEXT,
  UNIQUE (id, company_slug)
);
CREATE INDEX IF NOT EXISTS consent_eng ON consent(engineer_id, granted_at DESC);

-- Thoả thuận với bên nhận ở nước ngoài. Bảy cột nội dung = bảy mục a..g của
-- NĐ 356 Điều 7.1, NOT NULL từng cái: thiếu một mục thì không ghi được dòng nào.
CREATE TABLE IF NOT EXISTS company_agreement (
  id             TEXT PRIMARY KEY,
  company_slug   TEXT NOT NULL,
  purpose        TEXT NOT NULL,   -- a) mục đích chuyển giao
  subjects_types TEXT NOT NULL,   -- b) đối tượng chủ thể và loại dữ liệu
  retention      TEXT NOT NULL,   -- c) thời hạn xử lý, yêu cầu xoá sau khi xong
  legal_basis    TEXT NOT NULL,   -- d) cơ sở pháp lý
  protection     TEXT NOT NULL,   -- đ) trách nhiệm bảo vệ dữ liệu
  subject_rights TEXT NOT NULL,   -- e) trách nhiệm thực hiện quyền của chủ thể
  breach_duty    TEXT NOT NULL,   -- g) trách nhiệm phối hợp khi có vi phạm
  signed_at      TEXT NOT NULL,
  UNIQUE (id, company_slug)
);

-- Lần chuyển giao thật. Khoá ngoại ghép ép cả hai điều kiện cùng lúc:
-- đồng ý phải thuộc đúng công ty đó, VÀ thoả thuận phải thuộc đúng công ty đó.
--
-- ON DELETE CASCADE là quyết định có cân nhắc, không phải cho tiện: quyền được
-- xoá (Điều 25.1.c) THẮNG nhu cầu lưu vết. Lý do lưu vết vẫn đủ mà không cần
-- giữ dòng này: Điều 20.3 nói hồ sơ đánh giá tác động làm 01 LẦN cho suốt thời
-- gian hoạt động, không phải mỗi lần chuyển một hồ sơ. Vết cần cho thanh tra
-- nằm ở transfer_audit dưới đây — nơi không có dữ liệu cá nhân nào để mà xoá.
CREATE TABLE IF NOT EXISTS transfer (
  id            TEXT PRIMARY KEY,
  company_slug  TEXT NOT NULL,
  consent_id    TEXT NOT NULL,
  agreement_id  TEXT NOT NULL,
  transferred_at TEXT NOT NULL,
  FOREIGN KEY (consent_id,   company_slug) REFERENCES consent(id, company_slug)
    ON DELETE CASCADE,
  FOREIGN KEY (agreement_id, company_slug) REFERENCES company_agreement(id, company_slug)
);
CREATE INDEX IF NOT EXISTS transfer_when ON transfer(transferred_at DESC);

-- Vết chỉ-thêm, KHÔNG có dữ liệu cá nhân: công ty nào, theo thoả thuận nào,
-- lúc nào. Không tham chiếu tới kỹ sư, nên không nằm trong phạm vi quyền xoá
-- và cũng không cần cascade. Đây là thứ trả lời được câu thanh tra hỏi —
-- "đã chuyển ra nước ngoài bao nhiêu lần, theo cơ sở nào" — sau khi mọi hồ sơ
-- cá nhân đã bị xoá đúng luật.
CREATE TABLE IF NOT EXISTS transfer_audit (
  id             TEXT PRIMARY KEY,
  company_slug   TEXT NOT NULL,
  agreement_id   TEXT NOT NULL,
  transferred_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS transfer_audit_when ON transfer_audit(transferred_at DESC);
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
         + [f"DROP TABLE IF EXISTS {t}_new;" for t in ("company", "job", "meta", "locked")]
         + stmts(TABLES.replace("{S}", "_new")))

    # 2. Dữ liệu -> bảng tạm
    for table in ("company", "job", "meta", "locked"):
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
    # Ghi lịch sử TRƯỚC khi hoán đổi: sau DROP thì không còn nhãn cũ để so.
    # Chỉ ghi công ty ĐÃ TỒN TẠI và có nhãn khác — công ty mới xuất hiện không
    # phải "đổi nhãn", và ghi cả 3.630 dòng ở lần chạy đầu là rác.
    history = [
        # Kho trống (lần nạp đầu, hoặc CSDL mới) thì `company` chưa tồn tại và
        # câu INSERT dưới sẽ làm HỎNG CẢ TỆP khi chạy qua wrangler d1 execute —
        # sqlite3 CLI chỉ cảnh báo rồi đi tiếp nên lỗi này không lộ ở local.
        # Bảng cọc hai cột là đủ cho câu SELECT, và bị DROP ngay sau đó.
        "CREATE TABLE IF NOT EXISTS company (slug TEXT PRIMARY KEY, verdict TEXT);",
        "INSERT OR IGNORE INTO verdict_change (slug, from_v, to_v, changed_at) "
        "SELECT o.slug, o.verdict, n.verdict, datetime('now') "
        "FROM company o JOIN company_new n ON n.slug = o.slug "
        "WHERE o.verdict <> n.verdict;"
    ]
    emit("swap",
         stmts(USER_TABLES)          # bảng lịch sử phải tồn tại trước khi ghi
         + history
         + [f"DROP TABLE IF EXISTS {t}; ALTER TABLE {t}_new RENAME TO {t};"
            for t in ("job", "locked", "company", "meta")]
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
    db.executemany(
        "INSERT INTO locked (code, slug, n_jobs) VALUES (?,?,?)",
        [(code, p["slug"], n) for p in profs for code, n in json.loads(p["locked"])])
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
