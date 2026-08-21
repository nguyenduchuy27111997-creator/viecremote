#!/usr/bin/env python3
"""
Tầng xác định của rubric (FR-4.1/4.2) — bản v2, sửa 5 lỗi tìm thấy khi đối chứng tay.

Thứ tự đánh giá (rubric-spec 5.4), bổ sung tầng 0:
  0. location có cấu trúc  -> DQ-02   (trường có cấu trúc THẮNG văn xuôi)
  1. DQ regex trên title+location+description
  2. cờ DQ theo CÔNG TY (lan từ tin khác cùng công ty)
  3. A / B trên văn xuôi, chỉ trong ngữ cảnh tuyển dụng
"""
import csv, json, re, sys
from collections import defaultdict
sys.path.insert(0, "tools")
from country import ISO, REGIONS, REGIONS_VN, CITY, GLOBAL

R = lambda p: re.compile(p, re.I)

# ---- LỖI 1: phân tích trường location ---------------------------------------
US_ST = {"al","ak","az","ar","ca","co","ct","de","fl","ga","hi","id","il","in","ia","ks",
 "ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj","nm","ny","nc",
 "nd","oh","ok","or","pa","ri","sc","sd","tn","tx","ut","vt","va","wa","wv","wi","wy","dc"}
US_ST_FULL_MAP = {}
US_ST_FULL = {
 "alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware",
 "florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky",
 "louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi",
 "missouri","montana","nebraska","nevada","new hampshire","new jersey","new mexico",
 "new york","north carolina","north dakota","ohio","oklahoma","oregon","pennsylvania",
 "rhode island","south carolina","south dakota","tennessee","texas","utah","vermont",
 "virginia","washington","west virginia","wisconsin","wyoming","district of columbia",
 "washington dc","washington d.c.",
 # tỉnh Canada
 "ontario","quebec","québec","british columbia","alberta","manitoba","saskatchewan",
 "nova scotia","new brunswick","newfoundland","prince edward island"}
US_ST_FULL_MAP = {k: "US" for k in US_ST_FULL}
LOC_GLOBAL = R(r"^(?:fully )?remote$|anywhere|any location|worldwide|global|distributed|home[- ]based$|^remote[- ]first$|^$")
# CHỈ những cụm này trong `location` mới là bằng chứng A-02. "Remote" trần và
# "Distributed" KHÔNG tính — phần lớn tin chỉ tuyển trong một nước vẫn ghi "Remote".
VN_REGION = R(r"\bAPAC\b|\bAPJ\b|Asia[- ]Pacific|South[- ]?east Asia|\bSEA region\b|worldwide|globally|anywhere")
LOC_A02 = R(r"\banywhere\b|\bany location\b|\bworldwide\b|\bglobal(?:ly)?\b|\binternational(?:ly)?\b|\bany country\b|\bno location restriction")
REGION_W = R(r"\b(americas?|emea|latam|apac|north america|south america|europe(?:an)?)\b")

REMOTE_WITHIN = R(r"remote\s+(?:within|in|across)\s+(.+)$")

def loc_verdict(loc):
    """-> ('no',mã nước) | ('global',..) | ('ok',..) | (None,'')

    Dấu ';' ngăn cách các LỰA CHỌN địa điểm, không phải các điều kiện cộng dồn.
    'Palo Alto, US; Remote, Global; US Remote' = ba lựa chọn, một trong đó là toàn cầu
    -> KHÔNG loại trừ. Lỗi tìm thấy khi soi trang thật."""
    t = re.sub(r"\s+", " ", (loc or "").strip())
    if not t: return (None, "")
    if ";" in t:
        alts = [loc_verdict(x) for x in t.split(";") if x.strip()]
        if any(v == "ok" for v, _ in alts):     return ("ok", f"A-03(location): {t}")
        if any(v == "global" for v, _ in alts):
            # "Anywhere; Europe" = thẻ địa điểm, không phải hai lựa chọn ngang hàng.
            # Trộn từ toàn cầu với một vùng hẹp hơn thì mơ hồ -> không dám gán toàn cầu.
            if any(v == "no" for v, _ in alts):
                return (None, f"trộn toàn cầu với vùng hẹp: {t}")
            return ("global", f"A-02(location): {t}")
        if any(v is None for v, _ in alts):     return (None, "lựa chọn hỗn hợp")
        codes = sorted({c for v, w in alts if v == "no" for c in w.split("|")[-1].split("/") if c})
        return ("no", f"DQ-02(location):{t}|" + "/".join(codes)) if codes else (None, "")
    low = t.lower()
    # "remote WITHIN X" = X giới hạn remote -> luôn hạn chế, kể cả khi có " or "
    mw = REMOTE_WITHIN.search(low)
    if mw and not re.search(r"\bvi[eệ]t ?nam\b", mw.group(1)):
        inner = loc_verdict(mw.group(1))      # phân giải nơi chốn bên trong để hiện tên nước
        code = inner[1].split("|")[-1] if inner[0] == "no" else ""
        return ("no", f"DQ-02(location):{t}|{code}")
    # "Remote OR <nơi>" = lựa chọn thay thế, không phải điều kiện -> không loại
    # "New York / Remote" = hai lựa chọn, giống "New York or Remote".
    # Trước đây chỉ ' or ' được coi là lựa chọn -> '/' bị xử như điều kiện cộng dồn.
    alt = bool(re.search(r"\bor\b|[/|]", low)) and bool(re.search(r"\bremote\b", low))
    parts = [p.strip() for p in re.split(r"[,|/;·\-–—()]| or ", low) if p.strip()]
    places, globals_, vn_src = [], [], []
    for p in parts:
        p = p.strip()
        p = re.sub(r"\bu\.s\.a?\.?", lambda m: "usa" if "a" in m.group(0) else "us", p)
        p = re.sub(r"^(?:the|in|within)\s+", "", p.strip(". "))
        # "Remote UK" / "USA Remote" -> tách chữ remote ra để lộ tên nước
        p = re.sub(r"^remote\s+|\s+remote$", "", p).strip()
        p = re.sub(r"\bunited states?\b", "united states", p)
        if LOC_GLOBAL.search(p) or p in GLOBAL:
            # "Anywhere USA" = thu hẹp, không phải toàn cầu. Bỏ chữ toàn cầu ra,
            # phần còn lại nếu là tên nơi chốn thì chính nó mới là điều kiện.
            rest = LOC_GLOBAL.sub(" ", p)
            rest = re.sub(r"\b(?:remote|based|home|work|from|hiring)\b", " ", rest)
            rest = re.sub(r"\s+", " ", rest).strip(" -.,")
            if rest and rest not in GLOBAL:
                if rest in REGIONS_VN: places.append("VN"); vn_src.append("region"); continue
                if rest in ISO: places.append(ISO[rest]); continue
                if rest in REGIONS: places.append(REGIONS[rest]); continue
                if rest in CITY: places.append(CITY[rest]); continue
                if rest in US_ST or rest in US_ST_FULL: places.append("US"); continue
            globals_.append(p); continue
        if p in ISO: places.append(ISO[p]); continue
        if p in REGIONS_VN: places.append("VN"); vn_src.append("region"); continue   # APAC/Asia chứa VN
        if p in REGIONS: places.append(REGIONS[p]); continue
        if p in CITY: places.append(CITY[p]); continue
        if p in US_ST or p in US_ST_FULL: places.append("US"); continue
        # LỖI 2: dò chuỗi con — "Mapbox Germany" phải khớp "Germany"
        sub = next((v for k, v in ISO.items()
                    if len(k) > 3 and re.search(rf"\b{re.escape(k)}\b", p)), None)
        if sub: places.append(sub); continue
        sub = next((v for k, v in US_ST_FULL_MAP.items()
                    if re.search(rf"\b{re.escape(k)}\b", p)), None)
        if sub: places.append(sub); continue
        sub = next((v for k, v in CITY.items()
                    if re.search(rf"\b{re.escape(k)}\b", p)), None)   # "Bengaluru, Karnataka"
        if sub: places.append(sub); continue
        m = REGION_W.search(p)
        if m: places.append(m.group(1).upper()[:6]); continue
    if "VN" in places:
        # Greenhouse ghi office theo phân cấp "kiểu làm việc, nước, vùng cha":
        # "Remote, Australia, APAC" -> APAC là vùng cha của Australia, KHÔNG phải
        # lựa chọn thứ hai. Khi không có dấu hiệu lựa chọn thay thế, NƯỚC CỤ THỂ thắng.
        others = [x for x in places if x != "VN"]
        if others and not alt and vn_src and all(v == "region" for v in vn_src):
            places = others
        else:
            return ("ok", f"A-03(location): {t}")
    if not places and LOC_A02.search(low):
        m = LOC_A02.search(low)
        rest = low[m.end():].strip(" ,-–—")
        if re.match(r"^(?:in|within|across)\b", rest):
            inner = loc_verdict(re.sub(r"^(?:in|within|across)\s+(?:the\s+)?", "", rest))
            if inner[0] == "no":
                return ("no", f"DQ-02(location):{t}|" + inner[1].split("|")[-1])
            if inner[0] == "ok":
                return ("ok", f"A-03(location): {t}")
            # có mệnh đề thu hẹp mà không phân giải được nơi chốn -> KHÔNG được
            # coi là toàn cầu. "Remote (anywhere in the U.S.)" từng lọt vì chỗ này.
            return (None, f"mệnh đề thu hẹp không phân giải được: {t}")
        return ("global", f"A-02(location): {t}")
    if places and not alt:
        return ("no", f"DQ-02(location):{t}|" + "/".join(sorted(set(places))))
    if places and alt:
        return (None, f"location vừa remote vừa có nơi cụ thể ({t}) — nhập nhằng")
    return (None, "")

# ---- LỖI 4: quét DQ trên title+location+description --------------------------
DQ = [
 ("DQ-01", R(r"(?:must (?:be|have)|require[sd]?)[^.]{0,40}(?:authoriz\w+ to work|work (?:permit|visa|authoriz)|right to work)|legally authorized to work|eligible to work in the (?:US|United States|UK|EU)")),
 ("DQ-02", R(r"\blocation\s*:[^.]{0,60}\b(?:will be |is )?based\b[^.]{0,25}\bin (?:the )?(?=[A-Z])|"
             r"\b(?:based|located) in (?:the )?(?:LATAM|EMEA|USA?|EU|UK|Europe|North America|South America)\b|"
             r"fully remote \((?:US|USA|UK|EU|Canada)\)|"
             r"(?:primarily )?looking for (?:someone|candidates?|a candidate) (?:in|based in)\s+[A-Z]|"
             r"licen[sc]ed?\s+(?:mental health |healthcare |clinical )?(?:provider|professional|therapist|nurse|physician|attorney)?[^.]{0,30}\bin\s+(?:the\s+)?[A-Z][\w ]{2,24}|"
             r"(?:state|provincial|country) licen[sc]ure|licen[sc]ure in [A-Z]|"
             r"must (?:hold|have|maintain) (?:an? )?(?:active |valid )?licen[sc]e[^.]{0,40}\bin\b|"
             r"\b(?:US|U\.S\.|USA|UK|EU|EEA|Canada|Australia|India|Germany|France|Poland|Brazil|Mexico)[- ]only\b|must (?:be )?(?:reside|live|be located|be based)[^.]{0,30}\b(?:in|within)\b|only (?:accepting|considering|open to)[^.]{0,40}(?:candidates|applicants)|residents? of the (?:US|United States|UK|EU)|you will not be eligible for employment|within the country of employment")),
 ("DQ-03", R(r"\bW-?2\b|\bPAYE\b|(?:on|added to) (?:our |the )?local payroll|1099 (?:contractor|basis)")),
 ("DQ-04", R(r"(?:active|obtain|maintain|hold|require\w*|eligib\w*|must)[^.]{0,40}security clearance|"
             r"security clearance (?:is )?(?:required|mandatory)|"
             r"\b(?:US|U\.S\.|American)\s+citizen(?:s|ship)?\b|citizenship (?:is )?required|"
             r"(?:subject to|governed by|requires?)[^.]{0,30}\bITAR\b|\bITAR[- ]restricted\b")),
 ("DQ-05", R(r"\(\s*(?:PST|PDT|EST|EDT|CST|MST)\s*time ?zone\s*\)|"
             r"(?:within|±|\+/-)\s*\d\s*(?:-|to)?\s*\d?\s*hours? of (?:PST|PDT|EST|EDT|CST|MST|Pacific|Eastern)|"
             r"core (?:business )?hours[^.]{0,40}(?:PST|PDT|EST|EDT|CST|Pacific|Eastern)|"
             r"(?:overlap|work|available)[^.]{0,30}\b(?:PST|PDT|EST|EDT|CST|MST)\b[^.]{0,20}(?:time ?zone|hours)|"
             r"\b(?:PST|PDT|EST|EDT)\s+time ?zone\b|"
             r"\d{1,2}(?::\d\d)?\s*(?:AM|PM)?\s*(?:PST|PDT|EST|EDT|CST|CDT|MST|MDT)?\s*"
             r"[-–—to]{1,3}\s*\d{1,2}(?::\d\d)?\s*(?:AM|PM)?\s*"
             r"(?:PST|PDT|EST|EDT|CST|CDT|MST|MDT)\b|"
             r"\b(?:CET|CEST|EET|EEST|BST|IST|JST|AEST)\b[^.]{0,20}(?:hours|time ?zone|compatible)|"
             r"(?:based|located|reside)[^.]{0,25}(?:in or near )?[^.]{0,15}"
             r"(?:CET|CEST|EST|PST|GMT[+-]\d)[- ]?compatible|"
             r"(?:Pacific|Eastern|Central|Mountain) Time(?: Zone)? hours")),
 ("DQ-06", R(r"\bhybrid\b|\d\s*(?:days?|x)\s*(?:per|a|/)\s*week in (?:the )?office|commutable|"
             r"office\s+\d(?:\s*-\s*\d)?\s*(?:days?|x)\s*(?:a|per)\s*week|"
             r"\d(?:\s*-\s*\d)?\s*(?:days?|x)\s*(?:a|per)\s*week[^.]{0,30}\boffice\b|"
             r"\b[A-Z][\w.]+-based\b[^.]{0,40}(?:office|in[- ]person)|on[- ]?site (?:presence )?(?:required|expected)|in[- ]?person at our|work (?:full[- ]time and )?in[- ]person")),
 ("DQ-07", R(r"our client,\s+(?:a|an|the)\s+\w|confidential client|"
             r"on behalf of (?:our|a) client\b(?!s)|client company (?:is|remains) confidential")),
]

# ---- LỖI 2: A/B chỉ tính trong ngữ cảnh tuyển dụng ---------------------------
# Siết: chỉ những cụm THẬT SỰ nói về phạm vi tuyển. Bản cũ có "remote|work from|
# location" nên gần như câu nào cũng lọt.
HIRE_CTX = R(r"\bwe (?:hire|recruit|employ)\b|open to (?:candidates|applicants)|"
             r"candidates? (?:can|may|must) be (?:based|located)|"
             r"(?:this )?(?:role|position) is open to|eligible to apply|"
             r"applicants? (?:from|in)\b|hiring (?:in|from|anywhere)|"
             r"you (?:can|may) (?:be based|work from|live)")
# tiêu đề mục phúc lợi — mọi thứ sau đó là đãi ngộ, không phải điều kiện tuyển
PERK_HEAD = R(r"why (?:join|work|should you join|it.?s exciting)|what we offer|"
              r"what.?s in it for you|perks? (?:and|&) benefits|benefits? (?:and|&) perks?|"
              r"our benefits|compensation (?:and|&) benefits|why you.?ll love")
MISSION  = R(r"\b(?:patients?|customers?|users?|players?|our (?:mission|technology|products?|platform|network)|"
             r"clients?|enterprises?|markets?|operations? (?:worldwide|globally))\b")
# Câu về phúc lợi. "Work from anywhere" ở đây là ĐÃI NGỘ, không phải điều kiện
# tuyển. Lỗi lộ ra ở kho 23k tin: mục Benefits của rất nhiều công ty có cụm này.
# Văn bản pháp lý mẫu. "in any location" trong câu EEO/polygraph không phải
# phạm vi tuyển. Lỗi lộ ra ở mẫu kiểm chứng đợt 2 (zoominfo).
LEGALESE = R(r"lie detector|polygraph|equal (?:employment )?opportunit|\bEEO\b|"
             r"without regard to|discriminat|reasonable accommodation|"
             r"protected (?:class|veteran|status)|background check|"
             r"fair chance|ban the box|E-Verify|applicable law")
PERKS    = R(r"\b(?:benefit|perks?|stipend|allowance|paid time off|\bPTO\b|vacation|"
             r"insurance|401\(?k\)?|wellness|equipment budget|home ?office budget|"
             r"what we offer|compensation (?:and|&) benefits|pay (?:and|&) benefits)\b")
A02 = R(r"work from anywhere|anywhere in the world|from any country|fully global|"
        r"location[- ]independent|\bany location\b|we hire globally|hire (?:people )?globally|"
        r"remote[ ,-]*worldwide|open to candidates worldwide")
A03 = R(r"\bAPAC\b|Asia[- ]Pacific|Southeast Asia|South[- ]East Asia")
VN  = R(r"\bVi[eệ]t ?[Nn]am\b|\bVietnamese\b")
# LỖI 3: mệnh đề giới hạn ngay sau cụm toàn cầu
LIMIT = R(r"^\W{0,4}(?:within|in|across|throughout)\s+(?:the\s+)?[A-Z][\w .'-]{1,28}")
B01 = R(r"contractor(?:s)? (?:welcome|role|basis)|hire (?:you )?(?:globally )?as (?:a )?contractor|\bB2B contract\b|independent contractor|invoice (?:us|monthly)")
B03 = R(r"async[- ]first|asynchronous(?:ly)?|no core hours|fully distributed|work(?:ing)? asynchronously")
B04 = R(r"\bDeel\b|Oyster HR|employer of record|\bEOR\b|Velocity Global|Remofirst")
TZP = R(r"(CET|CEST|EET|GMT\+[12]\b|UTC\+[12]\b|European time ?zones?)")

# bằng chứng tường minh bác DQ-09: công ty nói rõ họ tuyển/trả lương ngoài nước đã liệt kê
REBUT = R(r"hired through an EOR|employer of record[^.]{0,60}outside|EOR \(outside|"
          r"we hire (?:people )?globally|hire(?:d)? (?:anywhere|worldwide|in any country)|"
          r"employ(?:ees|ed)?[^.]{0,40}outside (?:of )?the (?:US|United States|country)")

OPTIONAL = R(r"as much as you.?d like|as often as you|if you (?:want|like|prefer)|optional|"
             r"encouraged|welcome to|you can|flexible|no requirement|not required")


COMPANY_DESC = R(r"\b(?:we are|we're|our (?:team|company|culture)|the company) (?:is |a |an )?[^.]{0,25}hybrid|"
                 r"hybrid (?:team|culture|company|workplace|environment)\b")


def company_level_hybrid(sent):
    """'we are a hybrid team' mô tả CÔNG TY, không phải yêu cầu với vai trò này."""
    return bool(COMPANY_DESC.search(sent))


def voluntary(tail):
    """Câu nói về có mặt tại văn phòng nhưng là TỰ NGUYỆN, không phải bắt buộc.
    Lỗi tìm thấy ở quy mô 23k tin: 'work in person ... as much as you'd like'."""
    return bool(OPTIONAL.search(tail))


def vn_inclusive(tail):
    """Nơi chốn ngay sau mệnh đề hạn chế có bao gồm Việt Nam không?
    Lỗi lô 3: 'must be based in an APJ / APAC timezone' bị coi là loại trừ."""
    low = tail.lower()
    if re.search(r"\bvi[eệ]t ?nam\b", low): return True
    if any(re.search(rf"\b{re.escape(k)}\b", low) for k in REGIONS_VN): return True
    return bool(re.search(r"\banywhere\b|\bworldwide\b|\bany country\b", low))

SCOPE_REBUT = R(r"(?:may be |can be )?performed remotely from any location worldwide|"
                r"open to (?:candidates|applicants) (?:worldwide|globally|in any country)|"
                r"we hire (?:globally|worldwide|in any country)|"
                r"from any location worldwide|anywhere in the world, subject to|"
                r"international candidates")


def scope_rebuts_location(desc):
    """Mô tả có tuyên bố TƯỜNG MINH về phạm vi tuyển toàn cầu không?

    Nếu có, DQ-02 suy ra từ TRƯỜNG `location` bị bác — hạ xuống unknown, không
    nâng thẳng lên Tier A. (`location` là trường ATS sinh, không phải câu chữ
    công ty viết về điều kiện, nên chịu đúng điểm yếu như DQ-09.)"""
    return bool(SCOPE_REBUT.search(desc or ""))


def loc_names_place(loc):
    """Trường địa điểm CÓ nêu nơi chốn cụ thể không (dù cả chuỗi không phân giải được)?

    Nếu có, văn xuôi KHÔNG được phép nâng lên 'mở toàn cầu'. Trường có cấu trúc
    thắng văn xuôi — nguyên tắc này đã áp cho DQ, đây là lần áp cho A.
    Lỗi lộ ra ở kho 23k: loc='Saudi Arabia' và loc='Remote (US (ET or CT))'
    bị nâng lên worldwide bởi câu mô tả công ty."""
    low = re.sub(r"\s+", " ", (loc or "").lower())
    if not low:
        return False
    for p in re.split(r"[,|/;·\-–—()]| or ", low):
        p = p.strip()
        p = re.sub(r"\bu\.s\.a?\.?", lambda m: "usa" if "a" in m.group(0) else "us", p)
        p = re.sub(r"^(?:the|in|within)\s+", "", p.strip(". "))
        # "Remote UK" / "USA Remote" -> tách chữ remote ra để lộ tên nước
        p = re.sub(r"^remote\s+|\s+remote$", "", p).strip()
        p = re.sub(r"\bunited states?\b", "united states", p)
        if not p or LOC_GLOBAL.search(p) or p in GLOBAL:
            continue
        if (p in ISO or p in REGIONS or p in REGIONS_VN or p in CITY
                or p in US_ST or p in US_ST_FULL
                or any(re.search(rf"\b{re.escape(k)}\b", p) for k in CITY if len(k) > 4)
                or any(re.search(rf"\b{re.escape(k)}\b", p) for k in ISO if len(k) > 4)):
            return True
    return False


def sentences(t): return re.split(r"(?<=[.!?])\s+|\n+", t)

EXPLICIT_HIRE = R(r"we hire (?:globally|worldwide|internationally|anywhere|in any country)|"
                  r"we (?:recruit|employ) (?:globally|worldwide)|"
                  r"open to (?:candidates|applicants) (?:worldwide|globally|anywhere|in any country)|"
                  r"hire(?:d)? from anywhere|hiring (?:globally|worldwide)")


def _strip_perk_block(txt):
    """Cắt bỏ từ tiêu đề mục phúc lợi trở đi.

    Khối phúc lợi thường là gạch đầu dòng không có dấu chấm, nên tách câu không
    nhìn thấy nó. Cắt theo tiêu đề mục mới bắt được."""
    m = PERK_HEAD.search(txt)
    if not m:
        return txt
    # giữ lại phần sau tiêu đề nếu ở đó có tuyên bố tuyển dụng tường minh
    tail = txt[m.start():]
    return txt if EXPLICIT_HIRE.search(tail) else txt[:m.start()]


# Mệnh đề liệt kê ĐÓNG danh sách nước nhận hồ sơ. Testlio ghi location là
# "Global" nhưng thân tin liệt kê đúng 15 nước, không có Việt Nam. Nhãn địa điểm
# chung chung phải thua danh sách tường minh.
CLOSED_LIST = R(r"(?:open to|considering|hiring|accept(?:ing)?|recruit(?:ing)?)[^.]{0,60}"
                r"(?:candidates?|applicants?|employees?|talent)?[^.]{0,40}"
                r"(?:in |from |located in |residing in )?"
                r"(?:select|the following|these|certain|a limited (?:number|set) of)\s+"
                r"(?:countries|locations|regions|markets)")


def closed_country_list(txt):
    """-> ('no', danh sách) nếu tin liệt kê đóng các nước nhận và KHÔNG có VN.

    Trả None khi không có mệnh đề liệt kê đóng, hoặc khi VN nằm trong danh sách,
    hoặc khi không đọc ra đủ tên nước (không đoán)."""
    m = CLOSED_LIST.search(txt)
    if not m:
        return None
    window = txt[m.end():m.end() + 600]
    if re.search(r"\bvi[eệ]t ?nam\b", window, re.I):
        return None
    if VN_REGION.search(window):          # "select countries in APAC" -> có thể có VN
        return None
    names = [k for k in ISO
             if len(k) > 3 and re.search(rf"\b{re.escape(k)}\b", window, re.I)]
    if len(names) < 3:                    # quá ít tên nước -> không đủ căn cứ
        return None
    return ("no", re.sub(r"\s+", " ", txt[m.start():m.end() + 300]).strip())


def quote_around(txt, m, cap=180):
    """Trích một cửa sổ quanh chỗ khớp, BẢO ĐẢM chứa trọn đoạn đã khớp.

    Bản cũ lấy 60 ký tự mỗi bên rồi cắt [:cap] — với khớp dài thì đuôi bị cắt
    mất chính từ khoá, khiến cổng C1 bắt lỗi 'trích dẫn không lý giải nhãn'."""
    core = re.sub(r"\s+", " ", txt[m.start():m.end()]).strip()
    if len(core) >= cap:
        return core[:cap]
    pad = (cap - len(core)) // 2
    lo, hi = max(0, m.start() - pad), m.end() + pad
    # né cắt giữa từ
    if lo > 0:
        sp = txt.find(" ", lo, m.start())
        if sp != -1: lo = sp + 1
    return re.sub(r"\s+", " ", txt[lo:hi]).strip()


def match_in_hire_ctx(rx, txt):
    """LỖI 2 + 3: khớp phải nằm trong câu nói về tuyển dụng, và không bị mệnh đề giới hạn."""
    for s in sentences(_strip_perk_block(txt)):
        m = rx.search(s)
        if not m: continue
        if MISSION.search(s) and not HIRE_CTX.search(s): continue
        if not EXPLICIT_HIRE.search(s) and (PERKS.search(s) or PERK_HEAD.search(s)):
            continue                          # đãi ngộ, không phải phạm vi tuyển
        if LEGALESE.search(s): continue       # câu pháp lý mẫu, không phải phạm vi tuyển
        if not HIRE_CTX.search(s): continue
        win = re.sub(r"\s+", " ", s[max(0, m.start()-70):m.end()+90]).strip()
        if LIMIT.match(s[m.end():m.end()+40]):          # "work from anywhere within NI"
            return ("limited", win)
        return ("ok", win)
    return (None, "")

def main():
    rows = list(csv.DictReader(open("scoring-sheet.csv", encoding="utf-8-sig")))
    cache = json.load(open("/tmp/desc_cache.json"))
    cols = list(rows[0].keys())

    # --- LỖI 5: cờ DQ theo công ty (chạy trước, lan cho mọi tin cùng công ty) -----
    comp_flag = defaultdict(set)
    for r in rows:
        txt = cache.get(r["url"]) or ""
        for cid, rx in DQ:
            if cid in ("DQ-04",) and rx.search(f"{r['title']} {txt}"):
                comp_flag[r["company"]].add(cid)

    stat = defaultdict(int)
    for r in rows:
        txt = cache.get(r["url"]) or ""
        if not txt:
            r["auto_tier"] = r["auto_rules"] = r["auto_quote"] = ""
            stat["nodesc"] += 1; continue
        blob = f"{r['title']}. {r['location']}. {txt}"
        fired, q = [], ""

        # tầng 0: dq09 + location có cấu trúc
        if (r.get("dq09_auto") or "") == "no" and not REBUT.search(txt):
            fired, q = ["DQ-09"], r.get("dq09_why", "")
        elif (r.get("dq09_auto") or "") == "no":
            # schema loại trừ nhưng mô tả nói ngược -> hạ xuống unknown, KHÔNG nâng lên A
            m = REBUT.search(txt)
            r.update(auto_tier="unknown", auto_rules="DQ-09(bị bác)",
                     auto_quote=quote_around(txt, m, 190))
            stat["unknown"] += 1; continue
        else:
            lv, lw = loc_verdict(r["location"])
            if lv != "no":                    # nơi chốn nằm trong TIÊU ĐỀ ("... - Texas")
                tail = re.split(r"[-–—(,]", r["title"])[-1] if re.search(r"[-–—(,]", r["title"]) else ""
                tv, tw = loc_verdict(tail)
                if tv == "no":
                    lv, lw = "no", tw.replace("location", "title")
            if lv == "no":
                fired, q = ["DQ-02"], lw
            else:
                for cid, rx in DQ:                                    # tầng 1
                    m = rx.search(blob)
                    if m and cid == "DQ-02" and vn_inclusive(blob[m.end():m.end()+70]):
                        continue        # "must be based in APAC" — VN NẰM TRONG đó, không loại
                    if m:
                        fired.append(cid)
                        if not q: q = quote_around(blob, m)
                for cid in comp_flag.get(r["company"], ()):           # tầng 2
                    if cid not in fired:
                        fired.append(cid + "(công ty)"); q = q or f"cờ công ty {r['company']}"
        if fired:
            r.update(auto_tier="no", auto_rules=";".join(fired), auto_quote=q)
            stat["no"] += 1; continue

        # tầng 3
        if (r.get("dq09_auto") or "") == "A-01":
            fired.append("A-01"); q = r.get("alr_countries", "")
        lg, lgw = loc_verdict(r["location"])          # LỖI 1: location chiều DƯƠNG
        if lg == "global":
            fired.append("A-02"); q = q or lgw
        st, sq = match_in_hire_ctx(A02, blob)
        if st == "limited":
            r.update(auto_tier="no", auto_rules="DQ-02(mệnh đề giới hạn)", auto_quote=sq)
            stat["no"] += 1; continue
        if st == "ok": fired.append("A-02"); q = q or sq
        st3, sq3 = match_in_hire_ctx(A03, blob)
        if st3 == "ok": fired.append("A-03"); q = q or sq3

        b = [c for c, rx in (("B-01",B01),("B-03",B03),("B-04",B04)) if rx.search(blob)]
        if TZP.search(blob): b.append("B-05")
        if any(x.startswith("A-") for x in fired): tier = "A"
        elif len(b) >= 2: tier = "B"; fired += b
        else: tier = "unknown"; fired += b
        r.update(auto_tier=tier, auto_rules=";".join(fired), auto_quote=q)
        stat[{"A":"tier_a","B":"tier_b"}.get(tier,"unknown")] += 1

    with open("scoring-sheet.csv","w",newline="",encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        w.writerows([{c: r.get(c,"") for c in cols} for r in rows])
    print("TẦNG QUY TẮC v2\n" + "="*34)
    for k in ("no","tier_a","tier_b","unknown","nodesc"): print(f"  {k:<10} {stat[k]:>4}")


if __name__ == "__main__":
    main()
