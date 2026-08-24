import { meta } from "@/lib/db"

export const revalidate = 3600

/**
 * Nhịp tim của kho — cho chim hoàng yến (.github/workflows/canary.yml) và cho
 * bất kỳ ai muốn kiểm site còn tươi không.
 *
 * Bài học sinh ra endpoint này: cron refresh bị HUỶ (không phải fail) ba đêm
 * liên tiếp vì timeout, và GitHub không gửi thư cho run bị huỷ — kho đóng băng
 * mà mọi cổng đều im. Cổng gắn TRONG pipeline chỉ kêu khi pipeline chạy tới
 * nó; thứ duy nhất bắt được mọi kiểu chết là kiểm KẾT QUẢ từ ngoài: production
 * hôm nay có mang dữ liệu hôm nay không.
 *
 * revalidate 3600 chứ không phải 86400: endpoint đo độ tươi mà tự cache một
 * ngày thì nó đo chính cái cache của nó.
 */
export async function GET() {
  const m = await meta()
  return Response.json(
    {
      built_at: m.built_at ?? null,
      n_jobs: +(m.n_jobs ?? 0),
      n_companies: +(m.n_companies ?? 0),
      n_open: +(m.n_comp_ok ?? 0),
    },
    { headers: { "cache-control": "public, max-age=300" } },
  )
}
