#!/usr/bin/env python3
"""
Chuẩn hoá tên quốc gia -> ISO 3166-1 alpha-2, và áp DQ-09.

Lý do tồn tại: giá trị `applicantLocationRequirements` ngoài đời không nhất quán
(`United States` / `USA` / `US`; `Canada` / `CA`). So khớp chuỗi thô sẽ sai.

Nguyên tắc N2 (rubric-spec): phân giải THẤT BẠI -> `unknown`, KHÔNG -> `no`.
Thà bỏ sót còn hơn loại nhầm.

    python3 tools/country.py            # tự điền cột DQ cho các dòng DQ-09
    python3 tools/country.py --dry-run
"""
import argparse, csv, re, sys

# đủ cho dữ liệu đã gặp; mở rộng khi gặp giá trị mới
ISO = {
    "united states": "US", "usa": "US", "us": "US", "u.s.": "US", "u.s.a.": "US",
    "united states of america": "US", "america": "US",
    "canada": "CA", "united kingdom": "GB", "uk": "GB", "great britain": "GB",
    "britain": "GB", "england": "GB", "ireland": "IE", "germany": "DE",
    "france": "FR", "spain": "ES", "portugal": "PT", "netherlands": "NL",
    "belgium": "BE", "switzerland": "CH", "austria": "AT", "italy": "IT",
    "poland": "PL", "czechia": "CZ", "czech republic": "CZ", "slovakia": "SK",
    "hungary": "HU", "romania": "RO", "bulgaria": "BG", "greece": "GR",
    "estonia": "EE", "latvia": "LV", "lithuania": "LT", "finland": "FI",
    "sweden": "SE", "norway": "NO", "denmark": "DK", "iceland": "IS",
    "australia": "AU", "new zealand": "NZ", "japan": "JP", "singapore": "SG",
    "india": "IN", "vietnam": "VN", "viet nam": "VN", "việt nam": "VN",
    "brazil": "BR", "mexico": "MX", "argentina": "AR", "colombia": "CO",
    "chile": "CL", "israel": "IL", "south africa": "ZA", "nigeria": "NG",
    "kenya": "KE", "egypt": "EG", "turkey": "TR", "ukraine": "UA",
    "philippines": "PH", "indonesia": "ID", "thailand": "TH", "malaysia": "MY",
    "south korea": "KR", "korea": "KR", "china": "CN", "hong kong": "HK",
    "taiwan": "TW", "cayman islands": "KY", "united arab emirates": "AE", "uae": "AE",
    "saudi arabia": "SA", "qatar": "QA", "kuwait": "KW", "bahrain": "BH", "oman": "OM",
    "jordan": "JO", "lebanon": "LB", "iraq": "IQ", "iran": "IR", "afghanistan": "AF",
    "uzbekistan": "UZ", "azerbaijan": "AZ", "belarus": "BY", "montenegro": "ME",
    "cambodia": "KH", "laos": "LA", "myanmar": "MM", "bangladesh": "BD", "mongolia": "MN",
    "ethiopia": "ET", "tanzania": "TZ", "uganda": "UG", "rwanda": "RW", "senegal": "SN",
    "ivory coast": "CI", "cameroon": "CM", "zambia": "ZM", "zimbabwe": "ZW", "botswana": "BW",
    "algeria": "DZ", "libya": "LY", "sudan": "SD", "venezuela": "VE", "paraguay": "PY",
    "panama": "PA", "honduras": "HN", "nicaragua": "NI", "el salvador": "SV",
    "guatemala": "GT", "belize": "BZ", "jamaica": "JM", "trinidad": "TT", "guyana": "GY",
    "bolivia": "BO", "puerto rico": "PR", "fiji": "FJ", "papua new guinea": "PG",
    "serbia": "RS", "russia": "RU", "russian federation": "RU", "croatia": "HR",
    "slovenia": "SI", "bosnia and herzegovina": "BA", "north macedonia": "MK",
    "albania": "AL", "moldova": "MD", "georgia": "GE", "armenia": "AM",
    "kazakhstan": "KZ", "pakistan": "PK", "bangladesh": "BD", "sri lanka": "LK",
    "nepal": "NP", "peru": "PE", "uruguay": "UY", "ecuador": "EC", "costa rica": "CR",
    "guatemala": "GT", "dominican republic": "DO", "ghana": "GH", "morocco": "MA",
    "tunisia": "TN", "luxembourg": "LU", "malta": "MT", "cyprus": "CY",
}
# vùng KHÔNG chứa Việt Nam -> loại trừ được
REGIONS = {"european union": "EU", "eu": "EU", "eea": "EU", "europe": "EU",
           "emea": "EMEA", "latam": "LATAM", "north america": "NA",
           "south america": "SA", "americas": "AMER", "america": "AMER",
           "middle east": "ME", "africa": "AF", "anz": "ANZ",
           "amer": "AMER", "amers": "AMER", "namer": "NA", "na": "NA",
           "latam": "LATAM", "eu/uk": "EU", "uk/eu": "EU", "nam": "NA"}
# vùng CHỨA Việt Nam -> KHÔNG được loại trừ (lỗi tìm thấy ở lô 3: 'APAC')
REGIONS_VN = {"apac", "apj", "apac timezone", "asia", "asia pacific", "asia-pacific",
              "southeast asia", "south-east asia", "south east asia",
              "asia pacific japan", "aspac"}
# thành phố -> nước (lỗi tìm thấy ở lô 3: Bengaluru, Berlin, London)
CITY = {
 "san francisco":"US","new york":"US","nyc":"US","seattle":"US","boston":"US","austin":"US",
 "chicago":"US","los angeles":"US","denver":"US","atlanta":"US","miami":"US","philadelphia":"US",
 "dallas":"US","phoenix":"US","portland":"US","san jose":"US","oakland":"US","washington dc":"US",
 "somerville":"US","redwood city":"US","costa mesa":"US","emeryville":"US","ann arbor":"US",
 "milwaukee":"US","san diego":"US","salt lake city":"US",
 "toronto":"CA","vancouver":"CA","montreal":"CA","ottawa":"CA",
 "london":"GB","manchester":"GB","edinburgh":"GB","belfast":"GB","cambridge":"GB",
 "berlin":"DE","munich":"DE","münchen":"DE","hamburg":"DE","cologne":"DE","köln":"DE",
 "paris":"FR","lyon":"FR","amsterdam":"NL","rotterdam":"NL","brussels":"BE",
 "madrid":"ES","barcelona":"ES","lisbon":"PT","lisboa":"PT","milan":"IT","rome":"IT",
 "zurich":"CH","zürich":"CH","geneva":"CH","vienna":"AT","dublin":"IE",
 "stockholm":"SE","oslo":"NO","copenhagen":"DK","helsinki":"FI",
 "warsaw":"PL","krakow":"PL","kraków":"PL","prague":"CZ","budapest":"HU","bucharest":"RO",
 "tallinn":"EE","riga":"LV","vilnius":"LT","belgrade":"RS","zagreb":"HR",
 "tel aviv":"IL","istanbul":"TR","dubai":"AE","cairo":"EG","lagos":"NG","nairobi":"KE",
 "bengaluru":"IN","bangalore":"IN","mumbai":"IN","delhi":"IN","hyderabad":"IN","pune":"IN",
 "chennai":"IN","gurgaon":"IN","noida":"IN",
 "singapore":"SG","tokyo":"JP","osaka":"JP","seoul":"KR","hong kong":"HK","taipei":"TW",
 "shanghai":"CN","beijing":"CN","shenzhen":"CN","manila":"PH","jakarta":"ID",
 "bangkok":"TH","kuala lumpur":"MY","sydney":"AU","melbourne":"AU","brisbane":"AU",
 "auckland":"NZ","wellington":"NZ",
 "sao paulo":"BR","são paulo":"BR","rio de janeiro":"BR","mexico city":"MX",
 "buenos aires":"AR","bogota":"CO","bogotá":"CO","santiago":"CL","lima":"PE",
 "ho chi minh":"VN","hanoi":"VN","hà nội":"VN","da nang":"VN","đà nẵng":"VN",
 "tp.hcm":"VN","saigon":"VN",
}
# giá trị nghĩa là "toàn cầu" -> KHÔNG loại trừ
GLOBAL = {"worldwide", "anywhere", "global", "remote", "world", "any country",
          "any location", "earth", "all countries", "everywhere"}

AMBIGUOUS = {"ca"}   # Canada hay California? Không đoán.


def resolve(raw):
    """-> ('iso'|'region'|'global', mã) hoặc None nếu không phân giải được."""
    t = re.sub(r"\s+", " ", raw.strip().lower().strip(".,;")).strip()
    if not t:
        return None
    if t in GLOBAL:
        return ("global", t)
    if t in AMBIGUOUS:
        return None
    if t in ISO:
        return ("iso", ISO[t])
    if t in REGIONS_VN:
        return ("iso", "VN")          # vùng chứa VN -> coi như có VN
    if t in REGIONS:
        return ("region", REGIONS[t])
    if t in CITY:
        return ("iso", CITY[t])
    return None


def verdict(field):
    """
    Áp DQ-09 lên chuỗi alr_countries.
    -> ('no', lý do) loại trừ | ('a01', lý do) có VN | ('unknown', lý do)
    """
    vals = [v for v in re.split(r"[;,]", field or "") if v.strip()]
    if not vals:
        return ("unknown", "trường rỗng")
    res = [(v.strip(), resolve(v)) for v in vals]

    # Bất đối xứng có chủ ý:
    #   A-01 (dương) chỉ cần THẤY Việt Nam — không phụ thuộc các giá trị khác
    #   DQ-09 (âm) cần phân giải ĐƯỢC HẾT — thiếu một giá trị là không loại trừ
    if any(r and r[0] == "iso" and r[1] == "VN" for _, r in res):
        return ("a01", "A-01: có Việt Nam trong danh sách")

    unresolved = [v for v, r in res if r is None]
    if unresolved:
        return ("unknown", "không phân giải được: " + ", ".join(unresolved))
    kinds = [r for _, r in res]
    if any(k == "global" for k, _ in kinds):
        return ("unknown", "có giá trị toàn cầu — không loại trừ")
    return ("no", "DQ-09: " + "/".join(c for _, c in kinds) + ", không có VN")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default="scoring-sheet.csv")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.file, encoding="utf-8-sig")))
    if not rows:
        raise SystemExit("bảng rỗng")
    cols = list(rows[0].keys())
    for c in ("dq09_auto", "dq09_why"):
        if c not in cols:
            cols.insert(cols.index("DQ"), c)

    stat = {"no": 0, "a01": 0, "unknown": 0, "skip": 0}
    for r in rows:
        if (r.get("has_alr") or "").strip().lower() != "y":
            r["dq09_auto"], r["dq09_why"] = "", ""
            stat["skip"] += 1
            continue
        v, why = verdict(r.get("alr_countries", ""))
        stat[v] += 1
        r["dq09_why"] = why
        if v == "no":
            r["dq09_auto"] = "no"
            if not (r.get("DQ") or "").strip():
                r["DQ"] = "x"          # tiền điền, người chấm vẫn xác nhận
        elif v == "a01":
            r["dq09_auto"] = "A-01"
        else:
            r["dq09_auto"] = "unknown"

    if not a.dry_run:
        with open(a.file, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows([{c: r.get(c, "") for c in cols} for r in rows])

    n_alr = len(rows) - stat["skip"]
    print(f"Áp DQ-09 lên {n_alr} tin có applicantLocationRequirements:\n")
    print(f"  loại trừ (DQ-09)        {stat['no']:>4}   -> DQ='x' tiền điền")
    print(f"  có Việt Nam (A-01)      {stat['a01']:>4}")
    print(f"  không phân giải được    {stat['unknown']:>4}   -> để trống, chấm tay (N2)")
    print(f"  không khai trường       {stat['skip']:>4}   -> chấm tay từ văn xuôi")
    if a.dry_run:
        print("\n(dry-run — không ghi)")
    else:
        print(f"\n✓ ghi vào {a.file}. Cột dq09_why giải thích từng quyết định — soi lại được.")


if __name__ == "__main__":
    main()
