import Link from "next/link"
import { all, one } from "@/lib/db"
import { ename } from "@/lib/countries"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"
import { Lookup } from "@/components/Lookup"

export const revalidate = 86400

export const metadata = {
  title: "I scored 34k remote job posts. 0 of 150 hand-scored said they hire in Vietnam",
  description:
    "The study behind this site: how the corpus is built, what blocks a candidate in Vietnam, "
    + "and why the public-postings channel is structurally closed. Numbers update daily.",
}

/** Nhãn rào cản tiếng Anh — bản Việt nằm ở lib/labels.ts cho trang /vi-sao-bi-loai. */
const REASON_EN: Record<string, string> = {
  "DQ-01": "Requires a work permit in a specific country",
  "DQ-02": "Geo-restricted — hires only in named countries/regions",
  "DQ-03": "Employment form that exists in one country only (US W-2, UK PAYE)",
  "DQ-04": "Citizenship or security-clearance requirement",
  "DQ-05": "Timezone requirement GMT+7 cannot overlap",
  "DQ-06": "Office presence required despite the remote label",
  "DQ-09": "Company's own structured data omits Vietnam",
}

/**
 * BÀI NGHIÊN CỨU TIẾNG ANH — trang đáp cho khách từ Hacker News.
 *
 * Kênh launch đầu tiên theo playbook là HN, mà bản HN của bài công bố trỏ về
 * một site tiếng Việt — người bấm vào thoát ngay. Trang này là bản tiếng Anh
 * của /cong-bo: cùng truy vấn, cùng nguyên tắc số-sống-từ-D1, người đọc khác.
 *
 * Giọng là NGHIÊN CỨU, không phải chào hàng — khác /hiring-in-sea. Người từ
 * HN đến vì tò mò phương pháp; trang bán hàng ở ngay link kế bên khi họ muốn.
 */
export default async function Research({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>
}) {
  const { q } = await searchParams
  const c = await one<{ total: number; jobs: number; open: number; closed: number }>(
    `SELECT (SELECT count(*) FROM company) total, (SELECT count(*) FROM job) jobs,
            (SELECT count(*) FROM company WHERE verdict='ok') open,
            (SELECT count(*) FROM company WHERE verdict='no') closed`,
  )
  const el = await all<{ eligibility: string; n: number }>(
    "SELECT eligibility, count(*) n FROM job GROUP BY eligibility",
  )
  const reasons = await all<{ reason: string; n: number }>(
    `SELECT reason, count(*) n FROM job
     WHERE eligibility='excluded' AND reason IS NOT NULL
     GROUP BY reason ORDER BY n DESC`,
  )
  const locks = await all<{ code: string; n: number }>(
    "SELECT code, sum(n_jobs) n FROM locked GROUP BY code ORDER BY n DESC LIMIT 5",
  )

  const jobs = c?.jobs ?? 0
  const of = (k: string) => el.find((e) => e.eligibility === k)?.n ?? 0
  const num = (n: number) => n.toLocaleString("en-US")
  const pct = (n: number) => `${((100 * n) / jobs).toFixed(1)}%`

  return (
    <article lang="en">
      <div className="glow rise">
        <Eyebrow>The study · numbers update daily</Eyebrow>
        <h1 className="mt-4 max-w-[24ch] text-[clamp(28px,4.8vw,44px)]">
          I scored {num(jobs)} remote job posts. <span className="grad">Zero of 150
          hand-scored</span> said they hire in Vietnam
        </h1>
        <Lead>
          I kept seeing &ldquo;remote means you can work anywhere&rdquo; and wanted to know how
          true that is for someone in Vietnam specifically. So I pulled every remote posting from
          three public ATS platforms — Greenhouse, Lever, Ashby — and checked each one for a
          single thing: <b className="text-text">does any clause block someone living in
          Vietnam?</b>
        </Lead>
      </div>

      <Section title="The numbers">
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <tbody>
              {([
                ["Geo-restricted", of("excluded"), "text-closed"],
                ["No clause either way", of("unknown"), "text-unk"],
                ["No blocking clause", of("worldwide"), "text-open"],
              ] as const).map(([label, n, tone]) => (
                <tr key={label} className="border-b border-line last:border-0">
                  <td className="px-4 py-3">{label}</td>
                  <td className={`px-4 py-3 text-right font-mono tabular-nums ${tone}`}>{num(n)}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-3">{pct(n)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          By <b className="text-text-2">company</b>: of {num(c?.total ?? 0)} companies,{" "}
          <b className="text-open">{num(c?.open ?? 0)} can hire someone in Vietnam</b> and{" "}
          <b className="text-closed">{num(c?.closed ?? 0)} are fully closed</b> — not one open
          position. I also hand-scored 150 random postings end to end:{" "}
          <b className="text-text-2">zero explicitly said they hire in Vietnam.</b> Not
          &ldquo;few&rdquo; — zero.
        </Note>
      </Section>

      <Section
        title="The barriers are concrete, not vibes"
        hint="Every label traces to a clause quoted from the posting."
      >
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <tbody>
              {reasons.filter((r) => r.n > 100).map((r) => (
                <tr key={r.reason} className="border-b border-line last:border-0">
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-2">{num(r.n)}</td>
                  <td className="px-4 py-3">{REASON_EN[r.reason] ?? r.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          Most-restricted-to:{" "}
          {locks.map((l, i) => (
            <span key={l.code}>
              {i > 0 && " · "}
              <b className="text-text-2">{ename(l.code)} {num(l.n)}</b>
            </span>
          ))}
          . The postings labelled remote that require office presence are the most brazen
          time-wasters — the label says one thing, the clause inside says another.
        </Note>
      </Section>

      <Section title="The paradox — and the actual finding">
        <div className="mt-4 max-w-[64ch] space-y-4 text-[14.5px] leading-relaxed text-text-2">
          <p>
            Vietnam has roughly <b className="text-text">530,000 developers</b> and ranks top-6
            globally for software outsourcing. Yet zero of 150 hand-scored postings said they
            hire there.
          </p>
          <p>
            These two facts do not contradict — together they say something else:{" "}
            <b className="text-text">companies do hire Vietnamese engineers, just not through
            public job postings.</b> It happens through outsourcing firms, EOR providers,
            contractor arrangements and referrals. The public-postings channel is structurally
            not the one to fish in.
          </p>
          <p>
            The corollary for employers is the arbitrage this site measures: the machinery for
            hiring in the region is often already paid for and pointed at a single country.{" "}
            <Link className="underline underline-offset-2 hover:text-text" href="/hiring-in-sea">
              Most companies reach Southeast Asia and stop at one country →
            </Link>
          </p>
        </div>
      </Section>

      <Section
        title="Look up any company"
        hint="Every conclusion carries a verbatim quote from the source posting — you read the
              same clause the machine read."
      >
        <div className="mt-5">
          <Lookup q={q} />
        </div>
      </Section>

      <Section title="Method and limits — stated plainly">
        <ul className="mt-4 max-w-[64ch] space-y-2.5 text-[13.5px] leading-relaxed text-text-2">
          <li>
            <b className="text-text">Three platforms only.</b> Greenhouse, Lever, Ashby — public
            APIs, no grey-area scraping. Companies on Workday, Taleo or custom sites are absent,
            and the sample skews US/EU.
          </li>
          <li>
            <b className="text-text">Measured precision: 97.5%</b> — 40 postings pulled from the
            &ldquo;open&rdquo; bucket, blind re-scored against the original page. Roughly 1 in 40
            &ldquo;open&rdquo; labels is wrong.
          </li>
          <li>
            The honest part: <b className="text-text">the first real measurement was 70%.</b> Two
            earlier rounds scored 85% and 90%, but they sampled randomly — and the open bucket is
            ~1% of the corpus, so random sampling barely touched it. Those numbers were not
            wrong; they measured the wrong thing. All five audit rounds and the ten mechanical
            bugs they surfaced are public on the methodology page (in Vietnamese).
          </li>
          <li>
            <b className="text-text">A snapshot, not the whole market</b> — rebuilt daily, and
            every flip in a company&rsquo;s position is kept in the{" "}
            <Link className="underline underline-offset-2 hover:text-text" href="/hiring-in-sea/changes">
              change log
            </Link>
            .
          </li>
        </ul>
        <Note>
          No accounts, no ads, no data selling, no candidate data of any kind. Runs on Cloudflare
          for about $12/year. Vietnamese version of this article:{" "}
          <Link className="underline underline-offset-2 hover:text-text" href="/cong-bo" lang="vi">
            bài công bố
          </Link>
          .
        </Note>
      </Section>
    </article>
  )
}
