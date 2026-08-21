#!/usr/bin/env python3
"""
Tải font về tự host — bỏ phụ thuộc fonts.googleapis.com + fonts.gstatic.com.

Vì sao: người dùng ở Việt Nam phải bắt tay DNS+TLS với HAI miền bên thứ ba
trước khi chữ hiện ra. Tự host = cùng nguồn, cache chung với HTML.

Cả ba font đều giấy phép OFL — tự host được phép. Chạy MỘT LẦN.

    python3 tools/fetch_fonts.py
"""
import os, re, urllib.request

OUT = "site/assets/fonts"
CSS_OUT = "site/assets/fonts.css"
# UA trình duyệt để Google trả woff2 (UA khác sẽ trả ttf, nặng gấp 3)
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SRC = ("https://fonts.googleapis.com/css2?"
       "family=Be+Vietnam+Pro:wght@400;500;600"
       "&family=Newsreader:opsz,wght@6..72,500"
       "&family=IBM+Plex+Mono:wght@400;500&display=swap")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if binary else r.read().decode("utf-8")


def main():
    os.makedirs(OUT, exist_ok=True)
    css = get(SRC)
    blocks = re.split(r"(?=/\*)", css)
    keep, n, total = [], 0, 0
    for b in blocks:
        sub = re.match(r"/\*\s*([\w-]+)\s*\*/", b.strip())
        if not sub:
            continue
        m = re.search(r"url\((https://[^)]+\.woff2)\)", b)
        if not m:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", b).group(1)
        # Bộ ký tự theo TỪNG font, dựa trên chỗ nó thực sự được dùng:
        #   Newsreader chỉ dựng tiêu đề (Việt + Anh) -> không cần latin-ext,
        #   vốn chiếm 37 KB / 48% tổng dung lượng font.
        #   Hai font kia dựng tên công ty và địa điểm -> cần latin-ext
        #   (Kraków, Ł, ș...).
        need = {"Newsreader": ("vietnamese", "latin")}.get(fam, ("vietnamese", "latin", "latin-ext"))
        if sub.group(1) not in need:
            continue
        wgt = re.search(r"font-weight:\s*([\d ]+)", b).group(1).strip()
        name = f"{fam.replace(' ', '')}-{wgt.replace(' ', '_')}-{sub.group(1)}.woff2"
        data = get(m.group(1), binary=True)
        open(os.path.join(OUT, name), "wb").write(data)
        total += len(data)
        n += 1
        keep.append(b.replace(m.group(1), f"fonts/{name}"))
        print(f"  {name:<46}{len(data)/1024:>6.1f} KB")
    open(CSS_OUT, "w", encoding="utf-8").write("".join(keep))
    print(f"\n✓ {n} file · {total/1024:.0f} KB -> {OUT}/")
    print(f"✓ {CSS_OUT}")


if __name__ == "__main__":
    main()
