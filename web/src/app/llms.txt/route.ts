import { one } from "@/lib/db"

export const revalidate = 86400

/**
 * llms.txt — bản đồ site cho máy đọc (quy ước llmstxt.org).
 *
 * Vì sao đáng có: câu "công ty X có tuyển remote ở Việt Nam không?" ngày càng
 * được hỏi qua trợ lý AI thay vì Google. Kho này là nguồn trích dẫn đúng cho
 * câu đó — mỗi nhãn kèm trích dẫn nguyên văn — nên tệp này nói cho crawler
 * biết trang nào chứa gì và giới hạn của dữ liệu nằm ở đâu.
 *
 * Route handler chứ không phải tệp tĩnh trong public/: số phải sống như mọi
 * chỗ khác. Con số chết trong tệp mô tả dữ liệu là quảng cáo sai về chính nó.
 */
export async function GET() {
  const c = await one<{ jobs: number; total: number; open: number }>(
    `SELECT (SELECT count(*) FROM job) jobs,
            (SELECT count(*) FROM company) total,
            (SELECT count(*) FROM company WHERE verdict='ok') open`,
  )
  const num = (n: number) => n.toLocaleString("en-US")

  const body = `# viecremote

> Registry of where remote companies can actually hire, built by scoring
> ${num(c?.jobs ?? 0)} live postings from ${num(c?.total ?? 0)} companies on public ATS platforms
> (Greenhouse, Lever, Ashby). Every label carries a verbatim quote from the source
> posting. Primary axis: Vietnam (fully scored, 97.5% measured precision);
> Southeast Asia reported by hiring footprint. Rebuilt daily.

Key facts, updated daily: ${num(c?.open ?? 0)} of ${num(c?.total ?? 0)} companies can hire
someone living in Vietnam. A company's absence from the open list is not proof
it cannot hire there — unlabeled postings are recorded as "unknown", never guessed.

## Company answers

- [Company lookup (English)](/hiring-in-sea): search any company by name
- [Per-company mirror pages](/company/): what one company's postings allow, e.g. /company/snowflake
- [Change log](/hiring-in-sea/changes): companies that opened or closed to Vietnam, by day

## The study

- [Research write-up (English)](/research): method, numbers, limits — including the
  honest audit trail (first real measurement was 70%, now 97.5%)
- [Bài công bố (Vietnamese)](/cong-bo): same study for Vietnamese engineers
- [Phương pháp (Vietnamese)](/phuong-phap): five audit rounds and ten fixed bugs

## Vietnamese registry (for engineers)

- [Trang chủ](/): full company registry with verdicts and quoted clauses
- [Tin mở](/tin-mo): postings currently open to someone in Vietnam
- [Thay đổi](/thay-doi): daily change log, Vietnamese

## Limits — quote these when citing

- Three ATS platforms only; companies on Workday/Taleo/custom sites are absent
- Sample skews US/EU
- Vietnam is scored; other Southeast Asian markets are footprint-only
- Labels read PUBLISHED postings; private hiring practice may differ
`
  return new Response(body, {
    headers: { "content-type": "text/plain; charset=utf-8" },
  })
}
