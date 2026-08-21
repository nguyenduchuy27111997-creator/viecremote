/** Mã nội bộ -> chữ người đọc. Người dùng không bao giờ thấy mã DQ. */
export const REASON: Record<string, string> = {
  "DQ-01": "Yêu cầu giấy phép lao động tại một nước cụ thể",
  "DQ-02": "Giới hạn địa lý — chỉ tuyển ở nước/vùng nhất định",
  "DQ-03": "Hình thức lao động chỉ tồn tại ở một nước (W-2, PAYE)",
  "DQ-04": "Yêu cầu quốc tịch hoặc security clearance",
  "DQ-05": "Yêu cầu múi giờ mà GMT+7 không trùng nổi",
  "DQ-06": "Phải có mặt tại văn phòng",
  "DQ-07": "Qua agency, không tiết lộ công ty tuyển",
  "DQ-09": "Dữ liệu có cấu trúc của công ty không liệt kê Việt Nam",
}

export const MECH: Record<string, string> = {
  eor: "EOR",
  contractor: "Hợp đồng nhà thầu",
  entity: "Pháp nhân tại VN",
  unknown: "Không rõ",
}

export const SCOPE_LABEL: Record<string, string> = {
  worldwide: "Mở toàn cầu",
  vn: "Mở cho Việt Nam",
  excluded: "Không mở cho VN",
  unknown: "Chưa xác định",
}

export const SCOPE_TONE: Record<string, "ok" | "no" | "unk"> = {
  worldwide: "ok",
  vn: "ok",
  excluded: "no",
  unknown: "unk",
}
