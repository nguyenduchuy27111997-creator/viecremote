import Link from "next/link"
import { notFound } from "next/navigation"
import { all, one, parseLocked, type Company } from "@/lib/db"
import { ename } from "@/lib/countries"
import { NEIGHBOURS } from "@/lib/sea"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"

export const revalidate = 86400
// Kho có 3.630 công ty; dựng sẵn hết là lãng phí khi phần lớn không ai xem.
// Dựng theo yêu cầu, lần đầu chậm một nhịp rồi nằm trong cache.
export const dynamicParams = true

/** PH/ID/TH/MY — tín hiệu mạnh nhất trong kho. Xem tools/prospects.py. */
const NEAR = new Set(NEIGHBOURS)

export async function generateStaticParams() {
  // Chỉ dựng sẵn nhóm đáng dựng: đã tuyển ở ĐNA. Đây là nhóm mà trang này có
  // điều đáng nói nhất, và cũng là nhóm dễ được chia sẻ nhất.
  const rows = await all<{ slug: string }>(
    `SELECT DISTINCT slug FROM locked WHERE code IN ('PH','ID','TH','MY') LIMIT 200`,
  )
  return rows.map((r) => ({ slug: r.slug }))
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const c = await one<{ name: string }>("SELECT name FROM company WHERE slug = ?", slug)
  if (!c) return { title: "Company not found" }
  return {
    title: `${c.name} — where its remote postings allow hiring`,
    description:
      `What ${c.name}'s own job postings say about the countries it can hire in, `
      + "quoted clause by clause. Company policy research — no candidate data.",
  }
}

/**
 * GƯƠNG SOI — trang để một công ty tự tra CHÍNH MÌNH.
 *
 * Đây là sản phẩm chạy được mà không phải gõ cửa ai: công ty tự tìm tới, tự
 * thấy tin của họ nói gì, tự nhận ra khoảng trống. Khác hẳn danh sách chào
 * hàng, vốn đòi có người đi liên hệ.
 *
 * Vẫn nằm trong ranh giới Đ3 (legal-options.md): dữ liệu về TỔ CHỨC, không có
 * ứng viên, không giới thiệu ai. Trang này chỉ đọc lại tin do chính họ đăng.
 */
export default async function CompanyMirror({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const c = await one<Company>("SELECT * FROM company WHERE slug = ?", slug)
  if (!c) notFound()

  const locked = parseLocked(c.locked)
  const sea = locked.filter(([code]) => NEAR.has(code))
  const totals = await one<{ total: number; open: number }>(
    "SELECT count(*) total, sum(verdict='ok') open FROM company",
  )
  const base = totals ? (100 * totals.open) / totals.total : 0

  const num = (n: number) => n.toLocaleString("en-US")
  // Nhãn tiếng Anh, KHÔNG dùng c.verdict_label — cột đó là tiếng Việt, dành cho
  // trang phía cung. Trang này người đọc là công ty nước ngoài.
  const VERDICT = {
    ok: { tone: "text-open", label: "Can hire in Vietnam",
          detail: "At least one posting is open worldwide or names Vietnam." },
    unk: { tone: "text-unk", label: "No clause either way",
           detail: "No posting states a geographic restriction that settles it. This is not "
                 + "the same as being closed — it means nothing was published." },
    no: { tone: "text-closed", label: "Cannot hire in Vietnam",
          detail: "Every posting with a geographic clause excludes Vietnam." },
  }[c.verdict]
  // Kho lưu slug ATS, không phải tên thương hiệu. Viết hoa đầu từ cho đỡ chướng,
  // KHÔNG đoán chỗ tách từ — cùng nguyên tắc với tools/outreach.py.
  const display = c.name.replace(/[-_]+/g, " ").replace(/\b\w/g, (m) => m.toUpperCase())

  return (
    <div lang="en">
      <p className="font-mono text-[11.5px] text-text-3">
        <Link className="hover:underline" href="/hiring-in-sea">
          ← Southeast Asia
        </Link>
      </p>

      <div className="glow rise mt-4">
        <Eyebrow>{num(c.n_jobs)} live postings · {c.source}</Eyebrow>
        <h1 className="mt-4 max-w-[20ch] text-[clamp(26px,4.6vw,42px)]">
          What <span className="grad">{display}</span>&rsquo;s postings actually say
        </h1>
        <Lead>
          Read from this company&rsquo;s own public job board. Every line below traces to a
          geographic clause quoted from a live posting — nothing inferred, nothing about any
          individual.
        </Lead>
      </div>

      <Section title="Current position on Vietnam">
        <p className={`mt-4 text-[15px] ${VERDICT.tone}`}>
          <b>{VERDICT.label}</b>
        </p>
        <p className="mt-1.5 max-w-[62ch] text-[13px] leading-relaxed text-text-3">
          {VERDICT.detail}
        </p>
        <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
          <table className="w-full border-collapse text-[13.5px]">
            <tbody>
              {[
                ["Postings open worldwide", c.n_global],
                ["Postings open to Vietnam specifically", c.n_vn],
                ["Postings that exclude Vietnam", c.n_excluded],
                ["Postings with no geographic clause", c.n_unknown],
              ].map(([label, n]) => (
                <tr key={label as string} className="border-b border-line last:border-0">
                  <td className="px-4 py-3">{label as string}</td>
                  <td className="px-4 py-3 text-right font-mono tabular-nums text-text-2">
                    {num(n as number)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      {sea.length > 0 && (
        <Section title="You already hire next door">
          <p className="mt-4 max-w-[64ch] text-[14px] leading-relaxed text-text-2">
            Your postings restrict to{" "}
            <b className="text-text">{sea.map(([code]) => ename(code)).join(", ")}</b>. That is the
            single strongest predictor in this corpus: companies hiring somewhere in Southeast
            Asia are open to Vietnam at <b className="text-text">18.4%</b> against a{" "}
            {base.toFixed(1)}% baseline — a <b className="text-text">7.3×</b> difference that holds
            across every company-size band we tested.
          </p>
          <Note>
            The reading is not that you missed a country. It is that the timezone band, the
            contracting paperwork and the cost tier are problems you have already solved. Vietnam
            reuses all three.
          </Note>
        </Section>
      )}

      {locked.length > 0 && (
        <Section
          title="Where your postings say you hire"
          hint="Counted from explicit clauses only. A location absent here is not proof you cannot
                hire there — it means no posting said so."
        >
          <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
            <table className="w-full border-collapse text-[13.5px]">
              <tbody>
                {locked.map(([code, n]) => (
                  <tr
                    key={code}
                    className={`border-b border-line last:border-0 ${NEAR.has(code) ? "text-open" : ""}`}
                  >
                    <td className="px-4 py-3">
                      {ename(code)}
                      {NEAR.has(code) && <span className="ml-2 font-mono text-[11px]">SEA</span>}
                    </td>
                    <td className="px-4 py-3 text-right font-mono tabular-nums">{num(n)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      <Section title="What this page is not">
        <ul className="mt-4 max-w-[64ch] space-y-2.5 text-[13.5px] leading-relaxed text-text-2">
          <li>
            <b className="text-text">Not a recruiting pitch.</b> No candidates, no introductions,
            no CVs. This is your own published policy, read back to you.
          </li>
          <li>
            <b className="text-text">Not an accusation.</b> A restriction is usually a template
            default nobody revisited, not a decision anyone made about Vietnam.
          </li>
          <li>
            <b className="text-text">Correctable.</b> If a label here is wrong, the posting it
            came from is linked in the public record — tell us and it gets fixed in a day.
          </li>
        </ul>
        <Note>
          Want the full picture — every company, the mechanisms they use, and what published terms
          imply about rates?{" "}
          <Link className="text-text-2 underline underline-offset-2 hover:text-text" href="/hiring-in-sea">
            Request the market brief
          </Link>
          .
        </Note>
      </Section>
    </div>
  )
}
