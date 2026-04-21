# Case study template — anonymized engagement

> Used after a paid engagement closes and the client has approved (or by default, all anonymizations land). Produces a public-shareable case study that becomes a reference asset for the next engagement.
>
> **Confidentiality default:** all client-identifying details anonymized unless we have explicit written permission to name them. This includes: company name, sector specifics that would identify the firm, named individuals, internal product names, customer lists, and unique financial figures.

---

# Case study — `{Anonymized engagement name}`

**Client profile:** `{e.g., "European mid-market PE-backed energy software, ~150 employees, €30M revenue"}` — vague enough to obscure identity, specific enough to give context.
**Engagement type:** `{Phase 1 / Phase 2 pilot / Phase 3 transformation}`
**Engagement duration:** `{2 weeks / 6 weeks / 6 months}`
**Date completed:** `{month-year only — no specific dates}`
**Sponsor:** `{e.g., "PE firm operating partner with technical background"}` — anonymized

---

## Executive summary

Two paragraphs.

Paragraph 1: the situation. What did the client face? What was the strategic question that led to the engagement? Anonymized but specific enough that a similar PE partner reading this recognizes the pattern.

Paragraph 2: the outcome. What changed? Key metrics with deltas. One sentence on the engagement structure that produced it.

---

## The situation

3-4 paragraphs of context. Cover:

- The client's stage (post-merger? mid-rollup? pre-IPO? pre-exit?)
- The strategic concern that triggered the engagement
- What they had tried before (or hadn't, and why)
- Why they engaged us specifically — what was the warm intro / decision criterion?

Anonymize freely. The reader should learn the *pattern*, not identify the *company*.

---

## What we found

This is the diagnostic-equivalent section. What did the audit + interviews reveal? Specific findings, anonymized.

Use the methodology chapter framework to organize:

- **Codebase shape:** how many files, how many god files, file size distribution, complexity. Numeric ranges if exact figures would identify.
- **Load-bearing duplication count:** if material.
- **Stub density:** if any.
- **Test integrity:** specific findings.
- **CI maturity:** workflow count, runtime, advisory-vs-blocking.
- **AI maturity:** what was deployed, what wasn't.
- **Team composition observations:** anonymized themes from interviews.

Keep the framing factual and clinical. No drama. No "shocking discovery." The methodology produces these findings reliably; the case study should demonstrate that, not perform surprise.

---

## What we did

Per pilot or workstream:

### Pilot 1 — `{name}`
- **Scope:** what we did
- **Duration:** how long
- **Team committed:** named roles (not named individuals unless permission)
- **Methodology references:** which chapters
- **Outcome (with metrics):** before/after specific numbers

### Pilot 2 — etc.

For Phase 1 only-engagements, this section is the transformation plan delivered. For Phase 2/3, this section is what was actually executed.

---

## Outcomes

The numbers. With deltas. With absolute values where the absolute matters.

| Metric | Before | After | Delta |
|---|---|---|---|
| | | | |

Notes:
- Always cite the measurement methodology. "Median PR cycle time, calculated as the median of `merged_at - opened_at` across all merged PRs to main branch in the 30 days preceding/following measurement points."
- Distinguish *what we changed directly* from *what changed adjacent* (correlation vs. causation). The case study is more credible when it acknowledges the limits of attribution.
- Where a metric didn't move as predicted, say so. "Deploy frequency targeted +2× actually achieved +1.4× — the gap was due to `{specific reason}`." Honest case studies are more valuable than perfect-looking ones.

---

## What didn't work

Mandatory section. Every engagement has at least one thing that didn't go as expected.

Examples:
- A pilot scoped for 4 weeks took 7 because of access delays
- A predicted ROI didn't materialize in one specific area
- A team's adoption of new tooling was slower than expected
- A specific recommendation was rejected by the client and we agreed they were right

Be specific. Be brief. The credibility this section produces dwarfs the discomfort of writing it.

---

## What the client said (with permission)

Optional section. If the client has provided a quote (and explicitly approved its use), include it here. Verify exact wording with the named individual; don't paraphrase quotes.

If no quote is available, omit the section entirely. Don't invent or imply quotes.

---

## What the client kept (post-engagement)

What did the client get to keep that they're using independently?

- The methodology playbook chapters relevant to their work
- The custom analysis scripts produced during the engagement
- The transformation plan
- Whatever tooling we deployed
- The instrumentation dashboards

This section signals our IP posture: we don't lock clients in. They keep what they need.

---

## Lessons for AI-Whisperers (internal note)

Write this section internally. Do not include in the client-facing version.

What did we learn? What patterns emerged that update the methodology? What gotchas should the next engagement watch for? What pricing or scoping mistakes did we make?

Updates to the methodology playbook get linked from here, with PR or commit references.

---

## How this case study is shared

| Audience | Version |
|---|---|
| Public (web, anonymous) | `client-facing.md` — fully anonymized, this template's structure |
| Specific PE partner (under NDA) | `under-nda.md` — same as public + named client + specific quotes |
| Internal AI-Whisperers | `internal.md` — full case study including "lessons for AI-Whisperers" + financials + lessons we got wrong |
| Client themselves | `client-record.md` — the engagement closeout document, formal |

Each version lives in a separate file in the same case-study directory, with clear naming.

---

## Anonymization checklist

Before publishing the public version:

- [ ] Company name removed
- [ ] Specific industry sub-sector vague enough to not identify
- [ ] No customer names mentioned
- [ ] No specific product / brand names from the client
- [ ] Specific financial figures rounded or ranged
- [ ] No named individuals
- [ ] No identifying timeline (use "month-year" not specific dates)
- [ ] No identifying team-size if unique
- [ ] No identifying tech stack details if proprietary

Run the document through this checklist with a second pair of eyes before publishing.

---

## Related

- `docs/methodology/` — the chapters this engagement applied
- `docs/commercial/phase-1-sow-template.md` — the SOW that would have governed a Phase 1 like this
- `docs/critique/` — the critic frameworks we apply to our own case studies before publishing
