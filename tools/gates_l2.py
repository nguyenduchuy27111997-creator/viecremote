#!/usr/bin/env python3
"""Bốn cổng L2 (C6..C9) — prd.md Mục 5.2. Vi phạm ⇒ exit 1.

`gates.py` chặn xuất bản SAI NHÃN. Cái này chặn xuất bản SAI LUẬT, và nó phải
chạy được cả khi L2 đang tắt — vì thứ nó canh chủ yếu là **lược đồ và mã nguồn**,
không phải dữ liệu. Dữ liệu lúc tắt thì rỗng; ràng buộc thì đã phải đúng từ trước.

    python3 tools/gates_l2.py

CI gọi nó mỗi lần push. Xoá một khoá ngoại hay thêm một luồng thu tiền từ kỹ sư
sẽ làm đỏ build, không phải làm đỏ một buổi thanh tra.
"""
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "app.db"
WEB = ROOT / "web" / "src"


def sources():
    return [p for p in WEB.rglob("*.ts*") if "node_modules" not in str(p)]


def c6_schema_enforces_consent(db, err):
    """C6 — không hồ sơ nào rời hệ thống mà thiếu đồng ý cho ĐÚNG công ty đó.

    Kiểm ở tầng lược đồ, đúng như prd.md yêu cầu ("chặn ở tầng dữ liệu, không
    phải tầng giao diện"). Kiểm bằng cách THỬ VI PHẠM trên bản sao trong bộ nhớ:
    đọc DDL rồi tin nó là chưa đủ — chỉ khi cơ sở dữ liệu thật sự từ chối thì
    ràng buộc mới có thật."""
    row = db.execute(
        "SELECT sql FROM sqlite_master WHERE name='transfer'").fetchone()
    if not row:
        err.append("C6: không có bảng transfer — L2 mất toàn bộ ràng buộc đồng ý")
        return

    mem = sqlite3.connect(":memory:")
    mem.execute("PRAGMA foreign_keys=ON")
    for t in ("engineer", "consent", "company_agreement", "transfer"):
        d = db.execute("SELECT sql FROM sqlite_master WHERE name=?", (t,)).fetchone()
        if d and d[0]:
            mem.executescript(d[0] + ";")
    N = "2026-01-01T00:00:00Z"
    try:
        mem.execute("INSERT INTO engineer VALUES ('e','a@b.c',?,?)", (N, N))
        mem.execute("INSERT INTO consent VALUES ('c','e','alpha','p','s',?,NULL)", (N,))
        mem.execute("INSERT INTO company_agreement VALUES "
                    "('g','alpha','a','b','c','d','e','f','g',?)", (N,))
    except sqlite3.Error as e:
        err.append(f"C6: không dựng lại được lược đồ để kiểm — {e}")
        return

    for label, sql in [
        ("đồng ý của công ty KHÁC", "INSERT INTO transfer VALUES ('t','beta','c','g',?)"),
        ("KHÔNG có đồng ý", "INSERT INTO transfer VALUES ('t','alpha','khong','g',?)"),
        ("CHƯA ký thoả thuận", "INSERT INTO transfer VALUES ('t','alpha','c','chua',?)"),
    ]:
        try:
            mem.execute(sql, (N,))
            err.append(f"C6: ghi được lần chuyển giao với {label} — khoá ngoại đã mất")
            mem.rollback()
        except sqlite3.IntegrityError:
            pass        # đúng: phải bị chặn


def c7_no_charge_to_engineer(err):
    """C7 — kỹ sư không bao giờ bị thu tiền.

    Bộ luật Lao động 2019: người lao động không phải trả chi phí tuyển dụng.
    Đây là LUẬT, không phải lựa chọn đạo đức — nên phải có cổng, không phải
    chỉ có lời hứa trong tài liệu."""
    pay = re.compile(r"\b(stripe|paddle|lemonsqueez|vnpay|momo|zalopay|checkout|"
                     r"createPayment|charge\w*|price_id|subscription)\b", re.I)
    eng = re.compile(r"\bengineer|ung[- ]?vien|ứng viên|candidate|kysu|kỹ sư\b", re.I)
    for p in sources():
        t = p.read_text(encoding="utf-8", errors="ignore")
        if pay.search(t) and eng.search(t):
            err.append(f"C7: {p.relative_to(ROOT)} có cả luồng thanh toán lẫn khái niệm "
                       "kỹ sư/ứng viên — đọc lại, kỹ sư không được trả tiền")


def c8_erasure(db, err):
    """C8 — rút lui = xoá hẳn trong 24h, và không chuyển sau khi đã rút."""
    n = db.execute(
        """SELECT count(*) FROM transfer t JOIN consent c ON c.id = t.consent_id
           WHERE c.revoked_at IS NOT NULL AND t.transferred_at > c.revoked_at""").fetchone()[0]
    if n:
        err.append(f"C8: {n} lần chuyển giao xảy ra SAU khi đồng ý đã bị rút")

    # Điều 25.1.c: không tuyển thì xoá. purge_after là hạn chót, quá hạn mà còn
    # dòng nghĩa là công việc xoá không chạy.
    n = db.execute(
        "SELECT count(*) FROM engineer WHERE purge_after < datetime('now')").fetchone()[0]
    if n:
        err.append(f"C8: {n} hồ sơ kỹ sư quá hạn purge_after mà chưa bị xoá")


def c9_labels_are_machine_only(err):
    """C9 — tầng minh bạch không đổi vì công ty trả tiền.

    Cách ép duy nhất đáng tin: nhãn công ty chỉ do pipeline sinh, và KHÔNG tồn
    tại đường sửa tay nào. Nên cổng này tìm mọi câu ghi vào bảng company/job
    trong mã web — đúng ra không được có câu nào."""
    write = re.compile(r"(INSERT\s+INTO|UPDATE|DELETE\s+FROM)\s+[\"'`]?(company|job)\b", re.I)
    for p in sources():
        for m in write.finditer(p.read_text(encoding="utf-8", errors="ignore")):
            err.append(f"C9: {p.relative_to(ROOT)} ghi vào bảng {m.group(2)} "
                       f"({m.group(1).upper()}) — nhãn phải do pipeline sinh, không sửa tay")


def c_switch_defaults_off(err):
    """Công tắc phải mặc định TẮT và phải là biến môi trường, không phải cờ trong DB."""
    f = WEB / "lib" / "l2.ts"
    if not f.exists():
        err.append("CÔNG TẮC: thiếu web/src/lib/l2.ts")
        return
    t = f.read_text(encoding="utf-8")
    if "process.env.L2_ENABLED" not in t:
        err.append("CÔNG TẮC: l2.ts không đọc process.env.L2_ENABLED")
    if re.search(r"L2_ON\s*=\s*true", t):
        err.append("CÔNG TẮC: L2_ON bị đặt cứng thành true")


def main():
    if not DB.exists():
        print(f"không thấy {DB} — chạy tools/export_db.py trước", file=sys.stderr)
        return 1
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    err = []
    c6_schema_enforces_consent(db, err)
    c7_no_charge_to_engineer(err)
    c8_erasure(db, err)
    c9_labels_are_machine_only(err)
    c_switch_defaults_off(err)
    db.close()

    if err:
        print(f"\n  {len(err)} vi phạm cổng L2:\n", file=sys.stderr)
        for e in err:
            print(f"   ✗ {e}", file=sys.stderr)
        return 1
    print("   C6 đồng ý-theo-công-ty ✓  C7 kỹ sư không trả tiền ✓  "
          "C8 xoá ✓  C9 nhãn do máy sinh ✓  công tắc tắt ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
