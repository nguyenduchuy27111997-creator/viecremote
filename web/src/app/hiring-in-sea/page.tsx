import Link from "next/link"
import { all, one } from "@/lib/db"
import { SEA, SEA_CODES } from "@/lib/sea"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"
import { Lookup } from "@/components/Lookup"

export const revalidate = 86400

export const metadata = {
  title: "Where remote companies can hire in Southeast Asia",
  description:
    "Most companies that reach Southeast Asia stop at one country in it. Built from live "
    + "postings, quoted clause by clause. Company policy research — no candidate data.",
}

/**
 * TRANG CHÍNH PHÍA CẦU sau pivot. Thay /hiring-in-vietnam ở vai trò trang gốc.
 *
 * Luận điểm đổi từ "sao không tuyển ở Việt Nam" — nghe như đi xin — sang "bạn
 * đã ở Đông Nam Á rồi, sao chỉ một nước" — một khoảng trống họ tự thấy và tự
 * thấy tốn tiền. Cùng kho dữ liệu, năm thị trường thay vì một.
 */
export default async function HiringInSEA({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>
}) {
  const { q } = await searchParams
  const codes = SEA_CODES.map((c) => `'${c}'`).join(",")

  const tot = await one<{ companies: number; jobs: number }>(
    "SELECT (SELECT count(*) FROM company) companies, (SELECT count(*) FROM job) jobs",
  )
  const foot = await all<{ code: string; n: number }>(
    `SELECT code, count(DISTINCT slug) n FROM locked
     WHERE code IN (${codes}) GROUP BY code ORDER BY n DESC`,
  )
  const oneOnly = await all<{ code: string; n: number }>(
    `SELECT code, count(*) n FROM (
       SELECT slug, max(code) code FROM locked WHERE code IN (${codes})
       GROUP BY slug HAVING count(DISTINCT code) = 1
     ) GROUP BY code ORDER BY n DESC`,
  )
  const reach = await one<{ n: number }>(
    `SELECT count(DISTINCT slug) n FROM locked WHERE code IN (${codes})`,
  )

  const num = (n: number) => n.toLocaleString("en-US")
  const trapped = oneOnly.reduce((a, r) => a + r.n, 0)
  const footOf = (code: string) => foot.find((f) => f.code === code)?.n ?? 0
  const oneOf = (code: string) => oneOnly.find((f) => f.code === code)?.n ?? 0

  return (
    <div lang="en">
      <div className="glow rise">
        <Eyebrow>Market brief · for companies hiring remotely</Eyebrow>
        <h1 className="mt-4 max-w-[19ch] text-[clamp(30px,5vw,48px)]">
          Most companies reach Southeast Asia <span className="grad">and stop at one country</span>
        </h1>
        <Lead>
          Built from <b className="text-text">{num(tot?.jobs ?? 0)} live postings</b> across{" "}
          <b className="text-text">{num(tot?.companies ?? 0)} companies</b>. Every claim traces to
          a geographic clause quoted from a real posting — nothing modelled, nothing about any
          individual.
        </Lead>
      </div>

      <Section
        title="Start with your own postings"
        hint="The fastest way to see what this corpus holds is to look yourself up."
      >
        <div className="mt-5">
          <Lookup q={q} />
        </div>
      </Section>

      <Section
        title="The one-country trap"
        hint={`Of ${num(reach?.n ?? 0)} companies whose postings reach Southeast Asia at all, `
            + `${num(trapped)} name exactly one country in it.`}
      >
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <thead>
              <tr className="border-b border-line text-left font-mono text-[11px] uppercase tracking-wider text-text-3">
                <th className="px-4 py-3 font-normal">Market</th>
                <th className="px-4 py-3 text-right font-normal">Companies hiring there</th>
                <th className="px-4 py-3 text-right font-normal">…and nowhere else in SEA</th>
              </tr>
            </thead>
            <tbody>
              {SEA.map((c) => (
                <tr key={c.code} className="border-b border-line last:border-0">
                  <td className="px-4 py-3">
                    <Link className="hover:underline" href={`/hiring-in-sea/${c.slug}`}>
                      {c.name}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums">{num(footOf(c.code))}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-3">
                    {num(oneOf(c.code))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          Singapore and the Philippines absorb almost the whole region&rsquo;s attention. Vietnam,
          Indonesia, Thailand and Malaysia sit in the same timezone band, at a lower cost tier,
          and are close to invisible in public postings.
          <br />
          <br />
          A company in this table has already paid for regional hiring — the entity or the EOR,
          the timezone adjustment, the contracting template — and draws from one talent pool with
          it. Adding a second country reuses all of that.
        </Note>
      </Section>

      <Section
        title="Per-market detail"
        hint="Vietnam carries the full analysis: every posting is scored for whether it allows
              hiring there. The other markets show hiring footprint only — see the note below."
      >
        <ul className="mt-5 grid gap-2.5 sm:grid-cols-2">
          {SEA.map((c) => (
            <li key={c.code}>
              <Link
                href={`/hiring-in-sea/${c.slug}`}
                className="block rounded-lg border border-line bg-card p-4 transition-colors hover:border-field"
              >
                <span className="text-[14px] font-medium">{c.name}</span>
                <span className="mt-1 block font-mono text-[11.5px] text-text-3">
                  {num(footOf(c.code))} companies
                  {c.scored && " · fully scored"}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </Section>

      <Section
        title="What changed"
        hint="The corpus rebuilds daily and overwrites itself. One page remembers yesterday."
      >
        <p className="mt-4 max-w-[64ch] text-[14px] leading-relaxed text-text-2">
          Every day a company opens or closes to Vietnam, it is recorded — the only dataset
          tracking these flips at all.{" "}
          <Link className="underline underline-offset-2 hover:text-text" href="/hiring-in-sea/changes">
            See the change log →
          </Link>
        </p>
      </Section>

      <Section title="What this is, and what it is not">
        <ul className="mt-4 max-w-[64ch] space-y-2.5 text-[13.5px] leading-relaxed text-text-2">
          <li>
            <b className="text-text">Vietnam is scored; the rest is footprint.</b> Every posting
            is read for whether it permits hiring in Vietnam, at 97.5% measured precision. For the
            other five markets we report only what postings explicitly name — we do not infer a
            verdict we have not measured.
          </li>
          <li>
            <b className="text-text">Not a recruiting service.</b> No candidates, no
            introductions, no CVs. This is research into published company policy.
          </li>
          <li>
            <b className="text-text">Absence is not proof.</b> A company with no clause may still
            hire anywhere privately. We measure what is <i>published</i>, and label a posting{" "}
            <i>unknown</i> rather than guess.
          </li>
        </ul>
      </Section>
    </div>
  )
}
