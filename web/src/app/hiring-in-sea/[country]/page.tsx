import Link from "next/link"
import { notFound } from "next/navigation"
import { all, one } from "@/lib/db"
import { SEA, SEA_CODES, NEIGHBOURS, bySlug } from "@/lib/sea"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"
import { Inquiry } from "@/components/Inquiry"

export const revalidate = 86400
export const dynamicParams = false

export async function generateStaticParams() {
  return SEA.map((c) => ({ country: c.slug }))
}

export async function generateMetadata({ params }: { params: Promise<{ country: string }> }) {
  const c = bySlug((await params).country)
  if (!c) return { title: "Market not found" }
  return {
    title: `Hiring remotely in ${c.name} — what postings actually allow`,
    description: c.scored
      ? `Which companies can hire in ${c.name}, read from live postings and quoted clause by `
        + "clause. Company policy research — no candidate data."
      : `Which companies name ${c.name} in their remote job postings, and how many hire nowhere `
        + "else in Southeast Asia.",
  }
}

/**
 * Một thị trường trong khu vực.
 *
 * BẤT ĐỐI XỨNG là chủ ý và phải nhìn thấy được: Việt Nam có bộ chấm đầy đủ
 * (mọi tin được đọc để kết luận có tuyển được không), năm nước còn lại chỉ có
 * dấu chân. Trang này KHÔNG giả vờ hai thứ đó ngang nhau — xem lib/sea.ts.
 */
export default async function Market({ params }: { params: Promise<{ country: string }> }) {
  const c = bySlug((await params).country)
  if (!c) notFound()

  const codes = SEA_CODES.map((x) => `'${x}'`).join(",")
  const num = (n: number) => n.toLocaleString("en-US")

  const foot = await one<{ n: number; jobs: number }>(
    "SELECT count(DISTINCT slug) n, sum(n_jobs) jobs FROM locked WHERE code = ?", c.code,
  )
  const alone = await one<{ n: number }>(
    `SELECT count(*) n FROM (
       SELECT slug FROM locked WHERE code IN (${codes})
       GROUP BY slug HAVING count(DISTINCT code) = 1 AND max(code) = ?)`, c.code,
  )
  const top = await all<{ slug: string; name: string; n: number; mechanism: string }>(
    `SELECT c.slug, c.name, l.n_jobs n, c.mechanism
     FROM locked l JOIN company c ON c.slug = l.slug
     WHERE l.code = ? ORDER BY l.n_jobs DESC LIMIT 25`, c.code,
  )

  // Chỉ Việt Nam mới có dữ liệu này — cột verdict là về Việt Nam.
  const vn = c.scored
    ? await one<{ total: number; open: number; closed: number; unk: number }>(
        `SELECT count(*) total, sum(verdict='ok') open, sum(verdict='no') closed,
                sum(verdict='unk') unk FROM company`)
    : null
  const near = c.scored
    ? await one<{ n: number; o: number }>(
        `SELECT count(*) n, sum(verdict='ok') o FROM company
         WHERE EXISTS (SELECT 1 FROM locked l WHERE l.slug = company.slug
                       AND l.code IN (${NEIGHBOURS.map((x) => `'${x}'`).join(",")}))`)
    : null

  // Bảng cơ chế và danh sách đầy đủ chỉ có nghĩa khi có verdict — tức chỉ VN.
  const mech = c.scored
    ? await all<{ mechanism: string; o: number; u: number; n: number }>(
        `SELECT mechanism, sum(verdict='ok') o, sum(verdict='unk') u, sum(verdict='no') n
         FROM company WHERE mechanism <> 'unknown' GROUP BY mechanism ORDER BY 1`)
    : []
  const openCos = c.scored
    ? await all<{ slug: string; name: string; n_jobs: number; n_vn: number; mechanism: string }>(
        `SELECT slug, name, n_jobs, n_vn, mechanism FROM company
         WHERE verdict='ok' ORDER BY n_jobs DESC`)
    : []

  const base = vn ? (100 * vn.open) / vn.total : 0
  const nearRate = near?.n ? (100 * (near.o ?? 0)) / near.n : 0

  return (
    <div lang="en">
      <p className="font-mono text-[11.5px] text-text-3">
        <Link className="hover:underline" href="/hiring-in-sea">← Southeast Asia</Link>
      </p>

      <div className="glow rise mt-4">
        <Eyebrow>{num(foot?.n ?? 0)} companies · {num(foot?.jobs ?? 0)} postings name it</Eyebrow>
        <h1 className="mt-4 max-w-[20ch] text-[clamp(28px,4.8vw,44px)]">
          Hiring remotely in <span className="grad">{c.name}</span>
        </h1>
        <Lead>
          {c.scored ? (
            <>
              Every posting in this corpus is read for whether it permits hiring here, and labelled
              only when a clause can be quoted. Measured precision on the open bucket:{" "}
              <b className="text-text">97.5%</b>.
            </>
          ) : (
            <>
              This market is reported by <b className="text-text">hiring footprint</b> — which
              companies name it in a geographic clause. It is not scored the way Vietnam is, and
              this page does not pretend otherwise.
            </>
          )}
        </Lead>
      </div>

      {vn && (
        <Section title="Who can hire here">
          <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
            <table className="w-full border-collapse text-[13.5px]">
              <tbody>
                {([
                  ["Companies that can hire here", vn.open, "text-open"],
                  ["Companies that explicitly cannot", vn.closed, "text-closed"],
                  ["Companies with no clause either way", vn.unk, "text-unk"],
                ] as const).map(([label, n, tone]) => (
                  <tr key={label} className="border-b border-line last:border-0">
                    <td className="px-4 py-3">{label}</td>
                    <td className={`px-4 py-3 text-right font-mono tabular-nums ${tone}`}>{num(n)}</td>
                    <td className="px-4 py-3 text-right font-mono tabular-nums text-text-3">
                      {((100 * n) / vn.total).toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {near && (
        <Section
          title="The strongest predictor"
          hint="One signal dominates every other slice of this corpus."
        >
          <p className="mt-4 max-w-[64ch] text-[14px] leading-relaxed text-text-2">
            Companies whose postings already reach elsewhere in Southeast Asia are open to Vietnam
            at <b className="text-text">{nearRate.toFixed(1)}%</b>, against a{" "}
            {base.toFixed(1)}% baseline — a <b className="text-text">{(nearRate / base).toFixed(1)}×</b>{" "}
            difference. It holds across every company-size band we tested, between 3.3× and 7.0×,
            so it is not an artefact of larger firms publishing more.
          </p>
          <Note>
            A company hiring in Manila has already solved the timezone band, the contracting
            paperwork and the cost-tier conversation. Vietnam reuses all three.
          </Note>
        </Section>
      )}

      {mech.length > 0 && (
        <Section
          title="The barrier is scope, not infrastructure"
          hint="This is the finding that should change a hiring plan."
        >
          <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
            <table className="w-full border-collapse text-[13.5px]">
              <thead>
                <tr className="border-b border-line text-left font-mono text-[11px] uppercase tracking-wider text-text-3">
                  <th className="px-4 py-3 font-normal">Mechanism declared</th>
                  <th className="px-4 py-3 text-right font-normal">Open</th>
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
              {mech.reduce((a, m) => a + m.o + m.u + m.n, 0)} companies already state they hire
              through an employer-of-record or contractor arrangement — the machinery needed to
              hire anywhere. Only {mech.reduce((a, m) => a + m.o, 0)} of them include {c.name}.
            </b>{" "}
            They have solved payroll, compliance and cross-border contracting, and still exclude
            this market. The constraint is not legal or operational — it is the default scope
            someone typed into a job template and nobody revisited.
          </Note>
        </Section>
      )}

      {openCos.length > 0 && (
        <Section
          title={`All ${openCos.length} companies that can hire in ${c.name}`}
          hint="The complete list, largest first. A competitive reference: these firms are already
                competing for the same engineers, and their published terms set the market."
        >
          <div className="scroll-x mt-5 max-h-[32rem] overflow-y-auto rounded-lg border border-line bg-card">
            <table className="w-full border-collapse text-[13.5px]">
              <thead className="sticky top-0 bg-card">
                <tr className="border-b border-line text-left font-mono text-[11px] uppercase tracking-wider text-text-3">
                  <th className="px-4 py-3 font-normal">Company</th>
                  <th className="px-4 py-3 text-right font-normal">Postings</th>
                  <th className="px-4 py-3 text-right font-normal">Open here</th>
                  <th className="px-4 py-3 font-normal">Mechanism</th>
                </tr>
              </thead>
              <tbody>
                {openCos.map((o) => (
                  <tr key={o.slug} className="border-b border-line last:border-0">
                    <td className="px-4 py-2.5">
                      <Link className="hover:underline" href={`/company/${o.slug}`}>{o.name}</Link>
                    </td>
                    <td className="px-4 py-2.5 text-right font-mono tabular-nums">{num(o.n_jobs)}</td>
                    <td className="px-4 py-2.5 text-right font-mono tabular-nums text-open">{o.n_vn}</td>
                    <td className="px-4 py-2.5 text-text-3">
                      {o.mechanism === "unknown" ? "—" : o.mechanism}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      <Section
        title={`Companies that stop at ${c.name}`}
        hint={`${num(alone?.n ?? 0)} companies name ${c.name} and no other Southeast Asian market.`}
      >
        <Note>
          They already carry the cost of hiring in the region and draw from one talent pool with
          it. That is the gap this brief measures — not a missing country, an unused capability.
        </Note>
      </Section>

      <Section
        title={`Largest hirers naming ${c.name}`}
        hint="By postings restricted to this market. Click through to see a company's full
              geographic position."
      >
        <div className="scroll-x mt-5 max-h-[30rem] overflow-y-auto rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <thead className="sticky top-0 bg-card">
              <tr className="border-b border-line text-left font-mono text-[11px] uppercase tracking-wider text-text-3">
                <th className="px-4 py-3 font-normal">Company</th>
                <th className="px-4 py-3 text-right font-normal">Postings here</th>
                <th className="px-4 py-3 font-normal">Mechanism</th>
              </tr>
            </thead>
            <tbody>
              {top.map((t) => (
                <tr key={t.slug} className="border-b border-line last:border-0">
                  <td className="px-4 py-2.5">
                    <Link className="hover:underline" href={`/company/${t.slug}`}>{t.name}</Link>
                  </td>
                  <td className="px-4 py-2.5 text-right font-mono tabular-nums">{num(t.n)}</td>
                  <td className="px-4 py-2.5 text-text-3">
                    {t.mechanism === "unknown" ? "—" : t.mechanism}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>
      <Section
        title="Get told when this changes"
        hint="Everything above is on this page, free, no signup. The corpus rebuilds daily — leave
              an address only if you want to hear when a company opens or closes to this market."
      >
        <div className="mt-5">
          <Inquiry />
        </div>
      </Section>
    </div>
  )
}
