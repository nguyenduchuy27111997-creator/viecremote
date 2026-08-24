import Link from "next/link"
import { all } from "@/lib/db"
import { Eyebrow, Lead, Note, Section } from "@/components/Page"

export const revalidate = 86400

export const metadata = {
  title: "Companies that opened or closed to Vietnam",
  description:
    "Every change in a company's hiring position on Vietnam, recorded the day the corpus "
    + "rebuild detects it. No other dataset tracks this.",
}

type Change = {
  slug: string
  name: string | null
  from_v: string
  to_v: string
  changed_at: string
}

const LABEL: Record<string, string> = {
  ok: "can hire in Vietnam",
  no: "cannot hire in Vietnam",
  unk: "no clause either way",
}

/**
 * NHẬT KÝ ĐỔI NHÃN — con hào duy nhất tích được theo thời gian.
 *
 * Kho dựng lại mỗi ngày và GHI ĐÈ; verdict_change là thứ duy nhất nhớ hôm qua.
 * Không ai khác thu dữ liệu này, và không mua lại được sau. Trang này dựng
 * TRƯỚC khi có dữ liệu — cố ý: nhật ký không hiện ở đâu thì tích cũng vô hình,
 * và trạng thái rỗng nói thật ngày bắt đầu theo dõi là một lời hứa kiểm được.
 *
 * "Opened" là tin dùng được ngay cho cả hai phía: công ty thấy đối thủ vừa vào,
 * kỹ sư thấy cửa vừa mở. Cùng dữ liệu, hai người đọc.
 */
export default async function Changes() {
  // LEFT JOIN: công ty có thể đã rời kho sau khi đổi nhãn — lịch sử vẫn phải
  // hiện được, không lệ thuộc dòng company còn sống.
  const rows = await all<Change>(
    `SELECT v.slug, c.name, v.from_v, v.to_v, v.changed_at
     FROM verdict_change v LEFT JOIN company c ON c.slug = v.slug
     ORDER BY v.changed_at DESC, v.slug LIMIT 300`,
  )

  const opened = rows.filter((r) => r.to_v === "ok")
  const closed = rows.filter((r) => r.from_v === "ok")
  const shifted = rows.filter((r) => r.to_v !== "ok" && r.from_v !== "ok")

  const day = (iso: string) => iso.slice(0, 10)
  const Row = ({ r }: { r: Change }) => (
    <tr className="border-b border-line last:border-0">
      <td className="whitespace-nowrap px-4 py-2.5 font-mono text-[11.5px] text-text-3">
        {day(r.changed_at)}
      </td>
      <td className="px-4 py-2.5">
        <Link className="hover:underline" href={`/company/${r.slug}`}>
          {r.name ?? r.slug}
        </Link>
      </td>
      <td className="px-4 py-2.5 text-[12.5px] text-text-3">
        {LABEL[r.from_v] ?? r.from_v} → <b className="text-text-2">{LABEL[r.to_v] ?? r.to_v}</b>
      </td>
    </tr>
  )
  const Table = ({ items }: { items: Change[] }) => (
    <div className="scroll-x mt-5 rounded-lg border border-line bg-card">
      <table className="w-full border-collapse text-[13.5px]">
        <tbody>{items.map((r) => <Row key={r.slug + r.changed_at} r={r} />)}</tbody>
      </table>
    </div>
  )

  return (
    <div lang="en">
      <p className="font-mono text-[11.5px] text-text-3">
        <Link className="hover:underline" href="/hiring-in-sea">← Southeast Asia</Link>
      </p>

      <div className="glow rise mt-4">
        <Eyebrow>Change log · rebuilt daily</Eyebrow>
        <h1 className="mt-4 max-w-[20ch] text-[clamp(28px,4.8vw,44px)]">
          Companies that <span className="grad">opened or closed</span> to Vietnam
        </h1>
        <Lead>
          The corpus rebuilds every day and overwrites itself; this page is the only thing that
          remembers yesterday. Every row is a company whose published hiring position on Vietnam
          actually changed — recorded the day the rebuild caught it.
        </Lead>
      </div>

      {rows.length === 0 ? (
        <Section title="Nothing yet — and that is the honest state">
          <p className="mt-4 max-w-[64ch] text-[14px] leading-relaxed text-text-2">
            Tracking began on <b className="text-text">24 August 2026</b>. Positions flip when a
            company edits its postings, so rows appear here the day it happens — typically a
            handful per week across 3,630 companies. Check back, or leave an address on the{" "}
            <Link className="underline underline-offset-2 hover:text-text" href="/hiring-in-sea/vietnam">
              Vietnam page
            </Link>{" "}
            to be told instead of checking.
          </p>
          <Note>
            An empty change log a few days after launch is what a truthful one looks like. A feed
            that was already full would mean the dates were invented.
          </Note>
        </Section>
      ) : (
        <>
          {opened.length > 0 && (
            <Section
              title={`Opened to Vietnam (${opened.length})`}
              hint="The needle-movers: a clause appeared that permits hiring in Vietnam."
            >
              <Table items={opened} />
            </Section>
          )}
          {closed.length > 0 && (
            <Section
              title={`Closed to Vietnam (${closed.length})`}
              hint="A position that previously allowed Vietnam no longer does."
            >
              <Table items={closed} />
            </Section>
          )}
          {shifted.length > 0 && (
            <Section
              title={`Shifted between closed and unclear (${shifted.length})`}
              hint="Movements between an explicit exclusion and no clause at all — weaker signal,
                    kept for completeness."
            >
              <Table items={shifted} />
            </Section>
          )}
          <Note>
            Positions are read from published postings only. A flip here means the{" "}
            <i>published</i> position changed — the underlying policy may have changed earlier
            without a posting saying so.
          </Note>
        </>
      )}
    </div>
  )
}
