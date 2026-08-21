import "server-only"
import { getCloudflareContext } from "@opennextjs/cloudflare"

/**
 * Một cửa duy nhất ra dữ liệu.
 *
 * Kho là chỉ-đọc và dựng lại mỗi ngày, nên mọi thứ ở đây đều cache được.
 * Không có ghi, không có giao dịch, không có phân trang phía máy chủ phức tạp.
 */
export type Verdict = "ok" | "unk" | "no"
export type Scope = "worldwide" | "vn" | "excluded" | "unknown"

export type Company = {
  slug: string
  name: string
  verdict: Verdict
  verdict_label: string
  n_jobs: number
  n_global: number
  n_vn: number
  n_excluded: number
  n_unknown: number
  mechanism: string
  source: string
  n_pay: number
  locked: string
  declared: string
  reasons: string
}

export type Job = {
  id: string
  company_slug: string
  title: string
  location_raw: string | null
  url: string
  source: string
  eligibility: string
  scope: Scope
  reason: string | null
  evidence: string | null
  evidence_src: string | null
  tz_overlap: number | null
  mechanism: string | null
  pay: number
  excerpt: string | null
}

async function d1() {
  const { env } = await getCloudflareContext({ async: true })
  const db = env.DB
  if (!db) throw new Error("Thiếu binding D1 'DB' — xem wrangler.jsonc")
  return db
}

export async function all<T>(sql: string, ...args: unknown[]): Promise<T[]> {
  const r = await (await d1()).prepare(sql).bind(...args).all<T>()
  return r.results ?? []
}

export async function one<T>(sql: string, ...args: unknown[]): Promise<T | null> {
  const r = await (await d1()).prepare(sql).bind(...args).first<T>()
  return r ?? null
}

/** Đếm tổng, đọc một lần rồi cache — dùng cho dải mật độ trên mọi trang. */
export async function meta(): Promise<Record<string, string>> {
  const rows = await all<{ k: string; v: string }>("SELECT k, v FROM meta")
  return Object.fromEntries(rows.map((r) => [r.k, r.v]))
}

/** JSON đã tuần tự hoá trong cột — giải ở tầng này để trang không phải biết. */
export const parseLocked = (s: string) => JSON.parse(s || "[]") as [string, number][]
export const parseDeclared = (s: string) => JSON.parse(s || "[]") as string[]
export const parseReasons = (s: string) => JSON.parse(s || "[]") as [string, number][]
