/** Mã ISO -> tên tiếng Việt. Sinh từ build.py, đừng sửa tay. */
export const CNAME: Record<string, string> = {
 "US": "Mỹ",
 "CA": "Canada",
 "GB": "Anh",
 "IE": "Ireland",
 "DE": "Đức",
 "FR": "Pháp",
 "ES": "Tây Ban Nha",
 "PT": "Bồ Đào Nha",
 "NL": "Hà Lan",
 "BE": "Bỉ",
 "CH": "Thụy Sĩ",
 "AT": "Áo",
 "IT": "Ý",
 "PL": "Ba Lan",
 "CZ": "Séc",
 "SK": "Slovakia",
 "HU": "Hungary",
 "RO": "Romania",
 "BG": "Bulgaria",
 "GR": "Hy Lạp",
 "EE": "Estonia",
 "LV": "Latvia",
 "LT": "Lithuania",
 "FI": "Phần Lan",
 "SE": "Thụy Điển",
 "NO": "Na Uy",
 "DK": "Đan Mạch",
 "IS": "Iceland",
 "RS": "Serbia",
 "HR": "Croatia",
 "SI": "Slovenia",
 "UA": "Ukraine",
 "RU": "Nga",
 "TR": "Thổ Nhĩ Kỳ",
 "IL": "Israel",
 "AE": "UAE",
 "EG": "Ai Cập",
 "ZA": "Nam Phi",
 "NG": "Nigeria",
 "KE": "Kenya",
 "MA": "Maroc",
 "AU": "Úc",
 "NZ": "New Zealand",
 "JP": "Nhật Bản",
 "SG": "Singapore",
 "IN": "Ấn Độ",
 "CN": "Trung Quốc",
 "HK": "Hồng Kông",
 "TW": "Đài Loan",
 "KR": "Hàn Quốc",
 "PH": "Philippines",
 "ID": "Indonesia",
 "TH": "Thái Lan",
 "MY": "Malaysia",
 "BR": "Brazil",
 "MX": "Mexico",
 "AR": "Argentina",
 "CO": "Colombia",
 "CL": "Chile",
 "PE": "Peru",
 "UY": "Uruguay",
 "CR": "Costa Rica",
 "KY": "Cayman",
 "LU": "Luxembourg",
 "MT": "Malta",
 "CY": "Síp",
 "VN": "Việt Nam",
 "EU": "Liên minh châu Âu",
 "EMEA": "EMEA",
 "LATAM": "Mỹ Latinh",
 "NA": "Bắc Mỹ",
 "AMER": "châu Mỹ",
 "SA": "Nam Mỹ",
 "ME": "Trung Đông",
 "AF": "châu Phi",
 "ANZ": "Úc/NZ"
}

export const cname = (c: string) => CNAME[c] ?? c

/**
 * Tên nước bằng tiếng Anh — cho trang phía cầu (/hiring-in-vietnam), nơi người
 * đọc là công ty nước ngoài.
 *
 * Dùng Intl thay vì bảng ánh xạ thứ hai: runtime đã có sẵn toàn bộ ISO 3166,
 * và một bảng chép tay sẽ lệch khỏi CNAME ngay lần sửa đầu tiên. Mã vùng
 * ("EMEA", "AMER") không phải ISO nên Intl ném lỗi — trả lại chính mã đó.
 */
const EN = new Intl.DisplayNames(["en"], { type: "region", fallback: "code" })

export const ename = (c: string) => {
  try {
    return EN.of(c) ?? c
  } catch {
    return c
  }
}
