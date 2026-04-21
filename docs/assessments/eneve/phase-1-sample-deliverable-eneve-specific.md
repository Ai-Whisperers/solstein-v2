# Phase 1 — what an Eneve-specific deliverable would look like

> **READ FIRST.** This document is a *populated mock* of the Phase 1 deliverable AI-Whisperers would produce after a 10-day on-site engagement at Eneve. It is **not** a real deliverable — we have not been on-site, we have not interviewed Eneve engineers, we have not seen Eneve's code. Every section below is therefore based on **public signals only** and is explicitly labeled where inference replaces evidence.
>
> Use this document for two purposes only:
> 1. To show a Vortex partner / Eneve CTO what the *shape and depth* of a real Phase 1 output would look like (tone, structure, level of specificity). It is more credible than a generic template precisely because it engages with their company by name.
> 2. As a working artifact internally — the things this document gets *wrong* are the things a real Phase 1 would discover and correct.
>
> Every claim labeled with `(public-signal)` is from the outside-in assessment (`outside-in-assessment.md`). Every claim labeled with `(inferred)` is pattern-matching from public writeups of comparable rollups, not direct evidence about Eneve. Every claim labeled with `(would-resolve-on-site)` is something we explicitly cannot answer without access.

---

# AI-transformation diagnostic — Eneve

**Prepared by:** AI-Whisperers
**For:** Eneve leadership + Vortex Capital Partners (sponsor)
**Engagement:** Phase 1 diagnostic (mock — not an actual delivered engagement)
**Document version:** 0.1 — populated mock for discussion purposes

---

## Executive summary

Eneve is a Vortex-backed European energy-software rollup, 18 months past its formal merger of four predecessor companies (Energy21, Ecedo, Jules, Gridhub) plus a March 2026 add-on (Nemon). 130+ specialists across NL/PT/UK serve 50+ enterprise energy clients including Eneco, Essent, Vattenfall, BASF, Engie, AXPO, and TotalEnergies — supporting 20M+ energy connections. `(public-signal)`

This is the engineering profile of a company in mid-consolidation — the typical operating state for a Vortex platform investment ~3.5 years in. Public signals suggest Eneve has not yet completed the AI-native transformation that comparable software-PE portfolios are pursuing. `(inferred)`

If our engagement hypothesis holds, Eneve has three structural opportunities:

**Opportunity 1 — Platform unification across the five predecessor codebases.** Public product portfolio (`EBASE Portfolio Management`, `Onboarding`, `Contract & Billing`, `Customer Trading`, `Sourcing & Pricing`, `Balancing & Shipping`, `BRP-as-a-Service`) implies separate product lines from each predecessor. Whether these run on shared infrastructure or operate independently underneath unified branding is `(would-resolve-on-site)`. In comparable rollups at month 18, the typical state is "separate codebases, unified UI/branding, mapped workflows" — significant integration overhead. `(inferred)`

**Opportunity 2 — Quality and tooling consistency across teams of different vintages.** Energy21's anchor codebase (descended from EBASE, launched 2002) and Gridhub (2023) almost certainly inherit very different engineering cultures. Cross-team change cycles, test integrity, and CI consistency would all benefit from harmonization. `(inferred)`

**Opportunity 3 — AI integration as greenfield, not retrofit.** No public evidence of operational AI tooling — no engineering blog discussing it, no AI/ML roles in the 5 currently-open positions, no public GitHub presence for any predecessor brand `(public-signal)`. The literature on energy-sector software suggests this is consistent with the sector's caution; it is also consistent with not-yet-invested. The honest position: this is the gap that an internal diagnostic would resolve.

We recommend Eneve and Vortex consider three pilots, prioritized by impact-per-dollar, described in §4. Targets are drawn from publicly-reported comparable engagements — not from engagements AI-Whisperers has personally delivered (we are early in our commercial motion and disclose this).

| Metric | Target after 6 months |
|---|---|
| Cross-codebase integration overhead | Reduce by 20-40 percentage points of engineering time |
| Median PR cycle time | Reduce by 40-60% on instrumented teams |
| Files > 500 LOC across primary codebases | Reduce by ≥50% |
| Test collection success across all repos | 100% |
| Daily AI-tool adoption (Claude Code / Cursor) | >80% across engineering |

These are target ranges from comparable engagements, not commitments. The Phase 1 diagnostic establishes whether they are achievable for Eneve specifically.

---

## 1. What we observed (or, in this mock, inferred from public signals)

### 1.1 Codebase shape

`(would-resolve-on-site)` In a real Phase 1, this section contains specific repository names, LOC counts, file size distributions, complexity metrics, and import-cycle counts — all extracted in Days 2-3 from read access to Eneve's repositories.

In this mock, we cannot populate the table. Instead, we describe what we would expect to find based on the rollup pattern, and how those expectations would either be confirmed or revised on-site.

| Expected (inferred) | Why we expect it | What real Phase 1 would do |
|---|---|---|
| 4-6 primary repositories descended from predecessor companies | Each predecessor had its own product line; consolidation rarely collapses to 1 repo in 18 months | Audit + name them, count LOC each |
| Cross-repo identity/auth shim added 2024-2025 | Standard post-merger pattern; allows multi-product login | Verify or refute via codebase exploration |
| God files in the older codebases (1000+ LOC) | EBASE descended from a 2002 codebase; god files almost guaranteed | Find and rank by LOC |
| Quality practices vary by team-of-origin | Energy21's old culture vs. Gridhub's newer practices | Per-repo lint/test-pass-rate audit |
| Integration via background jobs / shared message bus | Standard post-merger integration pattern | Document the integration topology |

`(inferred)` These are educated hypotheses, not findings.

### 1.2 Delivery metrics (last 6 months)

`(would-resolve-on-site)` This section requires read access to CI logs, git history, ticket tracker, and incident reports. None of which we have for Eneve.

A real Phase 1 would produce this table populated with Eneve's actual numbers. Comparison columns ("industry p50") are aggregated from public writeups of comparable PE-backed software companies — not benchmarks we have personally measured.

| Metric | Eneve actual | Industry p50 reference |
|---|---|---|
| Commits per week (org total) | `?` | ~600 for a 130-person eng org |
| PRs merged per week | `?` | ~250 |
| Median PR size (lines touched) | `?` | 100-300 |
| Median PR cycle time (open to merge) | `?` | 1-3 days for top-quartile, 7-14 for legacy |
| Revert rate | `?` | <2% healthy, >5% concerning |
| Deploy frequency (production) | `?` | Daily for top-quartile, weekly+ for legacy |
| CI runtime (p50 across repos) | `?` | <5 min top-quartile, 15+ min concerning |

Industry p50 reference values are from publicly-reported case studies; AI-Whisperers has not personally measured a portfolio of 130-person energy software companies.

### 1.3 Team composition and process

`(would-resolve-on-site)` This section requires the four senior-engineer interviews that Day 4-5 of Phase 1 produces. The interview protocol (see `methodology/01-diagnostic.md`) asks the four standard questions; anonymized themes appear here.

In a real Phase 1, this section would say something like:
> *"Across 4 interviews with senior engineers, three themes emerged. (1) Cross-team coordination friction was named by all four. (2) Confidence in test coverage varied widely between teams from different predecessors. (3) Three of four reported using AI tools individually but with no shared workflow."*

Without those interviews, we have nothing to put here.

### 1.4 AI and tooling maturity

| Signal | What we can see externally | Interpretation |
|---|---|---|
| Public GitHub org | None for "Eneve" or any predecessor brand `(public-signal)` | Either no public OSS posture (typical for energy-sector B2B) or no internal OSS culture either. Can't tell from outside. |
| Open AI / ML roles | Zero of 5 current postings are technical `(public-signal)` | Could mean: no AI hiring, or hiring through other channels. Both common. |
| AI in product marketing | None — language is "smart software" not "AI" `(public-signal)` | Energy-sector buyers are AI-cautious; not necessarily diagnostic of internal AI maturity |
| Engineering blog | None visible | Not unusual for energy-sector B2B |
| Conference talks / public engineering signals | None we found | Not unusual |
| Production AI features in product | Unknown from outside | `(would-resolve-on-site)` |

**Honest assessment**: every individual signal could be explained by sector convention rather than absence of AI capability. The *aggregate* of all signals being absent suggests early-stage rather than mature, but we are pattern-matching, not measuring. This is exactly the question Phase 1 would resolve.

---

## 2. What we would conclude (or hypothesize, in this mock)

### 2.1 The rollup is in mid-consolidation, on-schedule for its vintage

`(inferred)` 18 months post-merger, 3.5 years post-Vortex acquisition — Eneve sits roughly where Vortex's typical platform investment sits at this stage. By comparison with other PE-backed buy-and-build software companies at similar vintage, Eneve is neither ahead of nor behind the typical curve.

This is not a critique. It is a baseline. The opportunity is not to fix something broken; it is to accelerate through the next 12-18 months of evolution that would otherwise take 24-36.

### 2.2 Three structural bottlenecks (hypothesized)

`(inferred)` Based on the rollup pattern; subject to revision after on-site work.

**Bottleneck A: cross-codebase integration**. Five predecessor codebases means many features touch multiple repositories. Engineering hours lost to coordination, integration tests, and cross-team PR threading typically 20-30% of total engineering time at this stage. (Reference: comparable software rollups in public writeups; not personally measured at Eneve.)

**Bottleneck B: quality drift across teams of different vintages**. Energy21's anchor culture (descended from a 2002 codebase) likely differs significantly from Gridhub's (2023-founded, plausibly more modern). Standardizing without disruption is the work.

**Bottleneck C: AI tooling not operationally integrated**. Greenfield opportunity — no existing tooling to displace, just installation work. (See §1.4 caveats; this could be wrong if Eneve has more internal AI capability than public signals suggest.)

### 2.3 Greenfield AI integration is a positive constraint

`(inferred)` If §1.4's read is correct, Eneve has not deployed Claude Code, Cursor, or equivalent at organizational scale. This means there is no existing tooling to migrate from — the work is installation, not replacement. Greenfield AI rollouts in our experience (limited to internal AI-Whisperers work) and in public writeups of comparable engagements (more common reference) tend to have cleaner cost-benefit profiles than mid-stream replacements.

---

## 3. Archive vs. refactor recommendation

`(would-resolve-on-site)` This section requires the codebase audit results from §1.1.

Predicted scoring on the Ch. 10 framework:

| Dimension | Predicted score (1-5) | Reasoning |
|---|---|---|
| Audit backlog size | 2-3 (estimated) | Vortex-backed companies typically have managed backlogs |
| Load-bearing duplication | 4 (estimated) | Almost guaranteed in 5-codebase rollup |
| Stub density | 1-2 (estimated) | Energy software is too critical for stubs to survive long |
| Test integrity debt | 3 (estimated) | Mixed cultures from predecessors |
| Architectural confusion | 4 (estimated) | Multiple architectures coexist in any rollup pre-unification |
| Team consensus | `(would-resolve-on-site)` | Interviews would reveal this |

**Predicted total: 14-17 — aggressive refactor, not archive-and-rebuild**.

This is exactly the band where in-place transformation delivers high ROI. Eneve is not broken; it needs accelerated unification. Archive-and-rebuild would be inappropriate for software running utility billing for Vattenfall.

---

## 4. Recommended pilots (predicted, not finalized)

Pilots would be finalized after Day 7 of a real Phase 1 based on what the audit and interviews reveal. The pilots below are educated hypotheses.

### Predicted Pilot A — Cross-codebase integration layer + god-file decomposition

**Predicted shape:** 6 weeks, 2 AI-Whisperers engineers + 1 Eneve engineer (part-time).
**Predicted price:** €50-60K fixed.
**Predicted scope:** Apply Ch. 2 (god-file decomposition) to top 5 most-modified files across the 3 largest codebases. Identify and consolidate the 5-10 load-bearing duplications we expect to find. Build a thin integration-layer API to reduce coupling between the two codebases that share the most cross-cutting features.

**Predicted success criteria:**
- Files >500 LOC: reduce by ≥50% across the 3 audited repos
- All identified load-bearing duplications consolidated to canonical locations with CI gates
- Cross-codebase PR count (PRs touching 2+ repos) reduces by ≥20% over the following quarter
- Zero production regressions

**Predicted ROI:** 10-20% reduction in engineering time on integration work within 6 months of pilot completion. If Eneve has ~70 engineers, that's ~7-14 FTE-equivalents of recovered capacity over a year — significant relative to the €50-60K pilot cost.

### Predicted Pilot B — CICD consolidation + quality gate rollout

**Predicted shape:** 3 weeks, 1 AI-Whisperers engineer + 1 Eneve DevOps engineer (part-time).
**Predicted price:** €25-30K fixed.
**Predicted scope:** Apply Ch. 5 (CICD rebuild) and Ch. 9 (quality gate hierarchy) across the 5 primary repos. Consolidate workflow sprawl to ≤3 workflows per repo. Eliminate `continue-on-error: true` on load-bearing checks. Standardize lint + typecheck + test gates across teams.

**Predicted success criteria:**
- CI runtime (p50) reduces by ≥50% in repos where it's currently >10 minutes
- Test collection success reaches 100% across all primary repos
- Advisory-gate count reaches 0
- All teams converge on the same lint + typecheck + test baseline

**Predicted ROI:** 3-5% recovered engineering time within 3 months. Lower-headline than Pilot A but cheaper and faster, with measurable infra outcomes.

### Predicted Pilot C — AI-native deployment with one team

**Predicted shape:** 4 weeks, 1 AI-Whisperers engineer embedded with 1 Eneve team.
**Predicted price:** €25-35K fixed.
**Predicted scope:** Apply Ch. 7 (AI-augmented refactoring) to one team's working rhythm. Train the team on session shape, prompting patterns, review discipline. Produce 20-30 committed PRs during the pilot as training artifacts. Measure pre/post on cycle time, LOC delivered, review-to-generation ratio.

**Predicted success criteria:**
- Team's median PR cycle time reduces by ≥30%
- Team's deploy frequency increases by ≥50%
- Team reports (3-question retrospective at end) improved confidence
- Documentation produced locally so the team continues post-pilot

**Predicted ROI:** Smaller direct ROI than A or B; the larger value is the template for org-wide rollout.

### Not recommended (and why)

- **Large-scale architectural rewrite.** Predicted Ch. 10 score (14-17) is in the in-place band. Archive-and-rebuild is inappropriate for utility-critical software.
- **Immediate ML/AI product feature work.** Foundations not ready. Sequence after operational pilots.
- **Replacement of EBASE.** EBASE is the load-bearing platform for the largest customer base. Any wholesale replacement is multi-year strategic work, not a 6-week pilot.

---

## 5. 30-60-90 day roadmap (predicted)

| Days | Activity |
|---|---|
| 0-14 | Phase 1 contract countersignature + kickoff for predicted Pilot A |
| 15-30 | Predicted Pilot A mid-point: first 3 god files decomposed, first 2 load-bearing duplications consolidated |
| 31-60 | Predicted Pilot A completion + Pilot B kickoff |
| 61-90 | Predicted Pilot B completion + Pilot C kickoff, Pilot A sustain review |
| 90 | Joint review with Eneve leadership + Vortex sponsor: assess results, decide on extending |

If all three pilots land, the natural next step is an org-wide transformation engagement (12-month scope). That engagement is not in this Phase 1 SOW and would be a separate agreement.

---

## 6. Interview notes

`(would-resolve-on-site)` Real Phase 1 has 4 anonymized interview transcripts attached as a separate document.

In this mock, we have nothing to attach. This is the single most important section that public-signal analysis cannot replace.

---

## What this mock makes possible

This is what a Vortex partner can hand to their Eneve contact and say: *"This is what an actual Phase 1 from these people would produce. 80% of this would be replaced with real numbers and real interview themes. The structure is the deliverable."*

It demonstrates:
- We can produce a high-quality structured deliverable
- We are honest about what's known vs. inferred vs. requires-on-site
- We have a methodology behind every recommendation, with cross-links
- Our pilot recommendations are sized, scoped, and priced

It does not demonstrate:
- That we have been on-site
- That we know Eneve's actual codebase state
- That we have personally delivered comparable transformations elsewhere

The first two are addressed by an actual Phase 1. The third is addressed by completing one or two such engagements (not yet done).

## Companion documents

- `outside-in-assessment.md` — the public-signal research this mock builds on
- `../../methodology/` — the 10 chapters this mock cross-references
- `../../commercial/phase-1-sow-template.md` — the legal SOW that would govern a real engagement
- `../../commercial/gaps-before-send.md` — what must be true before this mock becomes a real proposal
