# Hostile review — 2026-04-21

Conducted via `critic` subagent against the full proposal package. Findings preserved verbatim for accountability. **Do not delete this file.** It is the pre-external-motion checkpoint.

## Verdict

> *The package is internally competent but commercially naive. A sharp PE partner reads this and concludes: thoughtful engineering shop, no commercial muscle, no revenue case, no proof of work, pricing too low to be credible, pricing too high to be a pilot, and the Eneve conversation is being planned around an ambiguous intro they can't identify correctly. Do not send.*

## The six pre-send gates

Before any external motion, resolve:

1. **Resolve the Michiel identity question** with a real person check.
2. **Produce one paid (even deeply discounted) external reference engagement.**
3. **Get an EU-qualified lawyer through the SOW, PPA, and equity term sheet.**
4. **Define the legal entity, insurance, and data-processing posture.**
5. **Cut the portfolio-audit slide from the Vortex deck.** Keep it for internal only.
6. **Re-price Phase 1 honestly** — either €50-75K with proper team and insurance, or explicitly labeled "first paid pilot, priced for reference rights."

## Critical findings (summary — full review in `full-review.md`)

### Credibility

- **C1:** "Michiel Kuiper" appears in 3 files; Vortex's investment manager is Michiel Klaps. The package holds two versions of the intro's name unresolved. Fix or delete references.
- **C2:** "First proof case: Eneve" contradicts "Nothing has been sent to Eneve." Fix language.
- **C3:** Solstein v1→v2 as "proof" — it's internal refactoring, not an enterprise engagement. Reframe.
- **C4:** Chapter 8 design-only status is honest in-chapter but ignored by downstream docs (pitch deck, sample deliverable).
- **C5:** Outside-in assessment claims "substantial confidence" on inferences from public signals only. Tone down.
- **C6:** Internal fee-math appendix is inside the SOW template. If the "internal only" line is missed, client sees cost basis.
- **C7:** V2 tier names are being assigned in the presence of a missing AI-maturity sub-score — the same silent-defaults pattern Ch. 4 warns against.

### Commercial

- **CV1:** €25K Phase 1 is neither a credible loss-leader nor a standalone-value product. Pick one.
- **CV2:** €10K/month retainer for a PPA is too low to signal seriousness to a mid-market PE firm, too high for a 2-person firm to honestly reserve capacity.
- **CV3:** Equity vesting gives PE sponsor a 30% clawback by refusing to approve. Structural conflict.
- **CV4:** Liability cap of 2× fees (€50K) will not survive a utility-software PE counterparty's GC review.

### Strategy / Positioning

- **SP1:** No team, references, or delivered engagements. Zero-proof firm cannot underwrite a multi-year PPA.
- **SP2:** No legal entity disclosure, no GDPR posture, no E&O insurance. Dutch PE firm cannot countersign.
- **SP3:** Competitive positioning vs. MBB, Thoughtworks, in-house hire is absent.
- **SP4:** The "AI-native" phrase is used ~40× without definition anywhere.
- **SP5:** The portfolio-audit slide in the Vortex pitch deck condescends and encroaches on operating-partner turf.

### Internal consistency

- **IC1:** Michiel's surname — see C1.
- **IC2:** Phase 1 biased vs. unbiased framing — contradicts equity-for-transformation business model.
- **IC3:** "Eneve is the first proof case" vs. "Nothing sent to Eneve."
- **IC4:** Solstein as internal tool vs. sold as PPA output.
- **IC5:** Over-documentation (30+ docs pre-customer) is the same pattern v1's "more pipeline code" case study warns against.

### Missing artifacts

- **MA1:** Legal entity + insurance + data-processing addendum + GDPR posture
- **MA2:** Actual case study from a paid client (any size)
- **MA3:** Named team + bios
- **MA4:** References willing to take a call
- **MA5:** Eneve-specific (not template) sample deliverable
- **MA6:** Michiel-forward email template (draft for readiness, not send)
- **MA7:** Competitive positioning one-pager
- **MA8:** Security posture one-pager
- **MA9:** SOC 2 / ISO 27001 status (or explicit "none, why not")

## Severity ranking of fixes

| Severity | Fix |
|---|---|
| **P0 — blocks external motion** | C1 (Michiel identity), C2 (first proof case), MA1 (legal posture), MA5 (Eneve-specific deliverable) |
| **P1 — credibility-critical** | C3 (Solstein reframe), C5 (outside-in tone), C6 (fee math out), SP1 (team), MA3 (bios) |
| **P2 — address before external** | C4, C7, CV1, CV2, CV3, CV4, SP2, SP3, SP4, SP5, MA2, MA4, MA6, MA7, MA8, MA9 |
| **P3 — iterate over time** | IC2, IC4, IC5, Ch. 8 removal of projected benchmarks |

## Response plan

`gaps-before-send.md` holds the tracked list of fixes with status. `full-review.md` preserves the full critic output.

Addressed in this commit (round 1):
- C1 (Michiel name fixed — flagged as "unverified" throughout)
- C2 (removed "first proof case" framing)
- C3 (clarified Solstein v1→v2 framing as "internal transformation")
- C4 (Ch. 8 projected-benchmark warning)
- C5 (outside-in tone softened)
- C6 (internal fee math moved out)
- MA1 (legal-posture.md created with explicit "not ready" state)
- MA5 (Eneve-specific deliverable placeholder created)
- MA6 (warm-intro email template — internal, marked NOT READY TO SEND)
- MA7 (competitive-positioning.md created)
- MA8 (security-posture.md created with explicit "not ready" state)

Deferred (documented but not resolved in this commit):
- P1 reframes on Solstein as "proof" (C3 partial — more work needed)
- MA2 (paid client reference) — structural gap, requires external work
- MA3 (named team) — structural gap, requires hiring decisions
- MA4 (references) — blocked on MA2
- CV1-CV4 (commercial terms) — documented as open questions in gaps file
- SP1 (team capacity) — acknowledged as gap in gaps file
