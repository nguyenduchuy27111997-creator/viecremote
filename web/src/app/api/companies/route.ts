import { all, parseDeclared, parseLocked, parseReasons, type Company } from "@/lib/db"

/**
 * Mặt hàng của giai đoạn 2 trong business-model.md: địa lý tuyển dụng theo CÔNG TY.
 *
 * Dữ liệu ở đây là về công ty, không về cá nhân — PDPL không áp dụng, và bán nó
 * không đổi được nội dung xuất bản. Đó là hai ràng buộc đóng cửa mọi dòng doanh
 * thu khác (R1, R2 trong tài liệu đó).
 *
 *   GET /api/companies?verdict=ok&limit=100&cursor=<slug>
 */
const MAX = 500

export async function GET(req: Request) {
  const u = new URL(req.url)
  const verdict = u.searchParams.get("verdict")
  const mech = u.searchParams.get("mech")
  const cursor = u.searchParams.get("cursor") ?? ""
  const limit = Math.min(MAX, Math.max(1, +(u.searchParams.get("limit") ?? 100) || 100))

  if (verdict && !["ok", "unk", "no"].includes(verdict))
    return Response.json({ error: "verdict phải là ok | unk | no" }, { status: 400 })

  const where = ["slug > ?"]
  const args: unknown[] = [cursor]
  if (verdict) { where.push("verdict = ?"); args.push(verdict) }
  if (mech) { where.push("mechanism = ?"); args.push(mech) }

  const rows = await all<Company>(
    `SELECT * FROM company WHERE ${where.join(" AND ")} ORDER BY slug LIMIT ?`,
    ...args, limit,
  )

  return Response.json(
    {
      data: rows.map((c) => ({
        slug: c.slug,
        name: c.name,
        verdict: c.verdict,
        verdict_label: c.verdict_label,
        jobs: { total: c.n_jobs, global: c.n_global, vn: c.n_vn, excluded: c.n_excluded, unknown: c.n_unknown },
        mechanism: c.mechanism,
        source: c.source,
        locked_countries: parseLocked(c.locked).map(([code, n]) => ({ code, jobs: n })),
        declared_countries: parseDeclared(c.declared),
        exclusion_reasons: parseReasons(c.reasons).map(([code, n]) => ({ code, jobs: n })),
      })),
      next_cursor: rows.length === limit ? rows[rows.length - 1].slug : null,
      license: "Dữ liệu suy ra từ tin tuyển dụng công khai. Mỗi kết luận có trích dẫn nguyên văn tại /cong-ty/{slug}.",
    },
    { headers: { "cache-control": "public, max-age=3600, s-maxage=86400" } },
  )
}
