import { all, one } from "@/lib/db"
import { ename } from "@/lib/countries"
import { BarRow, Eyebrow, Lead, Note, Section } from "@/components/Page"
import { Inquiry } from "@/components/Inquiry"

export const revalidate = 86400

export const metadata = {
  title: "Hiring engineers in Vietnam — a market brief",
  description:
    "Of 3,630 companies advertising remote roles, only ~3% can hire in Vietnam. Built from live "
    + "postings, quoted clause by clause. Company policy research — no candidate data.",
}

/**
 * PHÍA CẦU. Trang duy nhất trên site viết cho công ty nước ngoài, và trang duy
 * nhất bằng tiếng Anh — vì người đọc là người trả tiền, và họ không đọc tiếng Việt.
 *
 * Đây là sản phẩm Đ3 (legal-options.md Mục 3): con đường có doanh thu mà không
 * cần Giấy phép dịch vụ việc làm, không cần ký quỹ 300 triệu, không chạm Luật
 * BVDLCN — chính xác vì nó KHÔNG chạm dữ liệu kỹ sư và KHÔNG giới thiệu ai.
 * Bán nghiên cứu về chính sách tuyển dụng của công ty. Dữ liệu tổ chức.
 *
 * Ranh giới đó phải giữ trong chính nội dung trang: không hứa ứng viên, không
 * hứa giới thiệu, không thu hồ sơ. Mục "What this is not" ở cuối không phải
 * khiêm tốn — nó là ranh giới pháp lý viết ra thành chữ.
 */
export default async function HiringInVietnam() {
  const c = await one<{ total: number; open: number; closed: number; unk: number }>(
    `SELECT count(*) total,
            sum(verdict='ok')  open,
            sum(verdict='no')  closed,
            sum(verdict='unk') unk
     FROM company`,
  )
  const j = await one<{ jobs: number; named: number }>(
    `SELECT count(*) jobs,
            sum(evidence LIKE '%Vietnam%' OR evidence LIKE '%Viet Nam%') named
     FROM job`,
  )
  const withLock = await one<{ n: number }>("SELECT count(DISTINCT slug) n FROM locked")
  const locks = await all<{ code: string; n: number }>(
    "SELECT code, count(DISTINCT slug) n FROM locked GROUP BY code ORDER BY n DESC LIMIT 10",
  )
  const mech = await all<{ mechanism: string; o: number; u: number; n: number }>(
    `SELECT mechanism,
            sum(verdict='ok')  o,
            sum(verdict='unk') u,
            sum(verdict='no')  n
     FROM company WHERE mechanism <> 'unknown' GROUP BY mechanism ORDER BY 1`,
  )

  const total = c?.total ?? 0
  const jobs = j?.jobs ?? 0
  const top = locks[0]?.n ?? 1
  const mechAll = mech.reduce((a, m) => a + m.o + m.u + m.n, 0)
  const mechOpen = mech.reduce((a, m) => a + m.o, 0)
  const num = (n: number) => n.toLocaleString("en-US")
  const share = (n: number, d: number) => (d ? `${((100 * n) / d).toFixed(1)}%` : "—")

  return (
    <>
      <div className="glow rise">
        <Eyebrow>Market brief · for companies hiring remotely</Eyebrow>
        <h1 className="mt-4 max-w-[19ch] text-[clamp(30px,5vw,48px)]">
          Where remote companies <span className="grad">can actually hire</span>
        </h1>
        <Lead>
          Built from <b className="text-text">{num(jobs)} live postings</b> across{" "}
          <b className="text-text">{num(total)} companies</b>. Every claim below traces to a
          quotable clause in a real posting. Nothing modelled, nothing estimated, nothing about
          any individual.
        </Lead>
      </div>

      <Section
        title="Remote is not global"
        hint={`${num(withLock?.n ?? 0)} of ${num(total)} companies (${share(withLock?.n ?? 0, total)}) attach an explicit
               geographic restriction to at least one posting. The word "remote" in a job title
               says nothing about where you may sit.`}
      >
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse">
            <caption className="sr-only">Companies restricting hiring, by location</caption>
            <tbody>
              {locks.map((l) => (
                <BarRow key={l.code} label={ename(l.code)} n={l.n} pct={(100 * l.n) / top} locale="en-US" />
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      <Section
        title="Vietnam is almost absent"
        hint="Vietnam has roughly 530,000 software developers and ranks in the global top ten for
              IT outsourcing. That is not what the postings show."
      >
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <tbody>
              {[
                ["Companies that can hire in Vietnam", c?.open ?? 0, total, "text-open"],
                ["Companies that explicitly cannot", c?.closed ?? 0, total, "text-closed"],
                ["Companies with no clause either way", c?.unk ?? 0, total, "text-unk"],
                ["Postings naming Vietnam at all", j?.named ?? 0, jobs, "text-text-2"],
              ].map(([label, n, d, tone]) => (
                <tr key={label as string} className="border-b border-line last:border-0">
                  <td className="px-4 py-3">{label as string}</td>
                  <td className={`px-4 py-3 text-right font-mono tabular-nums ${tone as string}`}>
                    {num(n as number)}
                  </td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-3">
                    {share(n as number, d as number)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          The demand exists. It does not travel through public job postings — it travels through
          agencies, EOR providers and referral. That is exactly why it is hard to see, and why a
          posting-level study is the only way to measure it.
        </Note>
      </Section>

      <Section
        title="The barrier is scope, not infrastructure"
        hint="This is the finding that should change a hiring plan."
      >
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <thead>
              <tr className="border-b border-line text-left font-mono text-[11px] uppercase tracking-wider text-text-3">
                <th className="px-4 py-3 font-normal">Mechanism declared</th>
                <th className="px-4 py-3 text-right font-normal">Open to VN</th>
                <th className="px-4 py-3 text-right font-normal">Unclear</th>
                <th className="px-4 py-3 text-right font-normal">Closed</th>
              </tr>
            </thead>
            <tbody>
              {mech.map((m) => (
                <tr key={m.mechanism} className="border-b border-line last:border-0">
                  <td className="px-4 py-3 uppercase">{m.mechanism}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-open">{m.o}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-unk">{m.u}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-closed">{m.n}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>
          <b className="text-text-2">
            {mechAll} companies already state they hire through an employer-of-record or contractor
            arrangement — the exact machinery needed to hire anywhere. Only {mechOpen} of them
            include Vietnam.
          </b>{" "}
          These firms have solved payroll, compliance and cross-border contracting. They have the
          capability and still exclude Vietnam. The constraint is not legal or operational — it is
          the default scope someone typed into a job template and nobody revisited. If you already
          run an EOR, adding Vietnam is a policy edit, not a project.
        </Note>
      </Section>

      <Section
        title="Request the full brief"
        hint="Country-by-country breakdown, the full list of companies already hiring in Vietnam,
              the mechanisms they use, and what their published terms imply about market rates."
      >
        <div className="mt-5">
          <Inquiry />
        </div>
      </Section>

      <Section title="What this is not">
        <ul className="mt-4 max-w-[64ch] space-y-2.5 text-[13.5px] leading-relaxed text-text-2">
          <li>
            <b className="text-text">Not a recruiting service.</b> We do not place candidates,
            introduce anyone, or accept CVs. This is research into published company policy.
          </li>
          <li>
            <b className="text-text">No candidate data, at all.</b> The corpus contains postings
            and companies. It holds no personal information about any engineer, and no part of
            this product is built to.
          </li>
          <li>
            <b className="text-text">Absence is not proof.</b> A company with no clause may still
            hire in Vietnam privately. We measure what is <i>published</i>, and we label a posting{" "}
            <i>unknown</i> rather than guess.
          </li>
        </ul>
        <Note>
          Postings are pulled daily from public ATS endpoints. A label is assigned only when a
          geographic clause can be quoted. Precision on the open bucket measured{" "}
          <b className="text-text-2">97.5%</b> against a hand-audited disjoint sample.
        </Note>
      </Section>
    </>
  )
}
