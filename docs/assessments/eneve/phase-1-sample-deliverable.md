# Example Phase 1 diagnostic deliverable — sanitized

> **This is a template / sample, not a real client deliverable.** It shows the shape, depth, and tone of what Eneve's leadership would receive at the end of a Phase 1 engagement. The scenario is a synthesized composite of Vortex-backed rollups at Eneve's stage; no specific client is depicted.
>
> A real Phase 1 deliverable for Eneve would replace every finding and metric in this document with verified, auditable numbers from 10 days of on-site work. The structure and depth of the document itself would match this template.

---

# AI-transformation diagnostic — [Client]

**Prepared by:** AI-Whisperers
**For:** [Client CEO/CTO]
**Engagement period:** [Date range, 10 working days]
**Prepared for:** distribution to [Client] leadership + [PE firm] investment team

---

## Executive summary

[Client] is a [€X]M revenue European B2B software rollup, [Y] years into PE ownership, integrating [N] predecessor companies. Our 10-day diagnostic found an engineering organization in a predictable mid-consolidation state: real product, real customers, real engineering talent, and a real gap between where the company's tooling is today and where comparable top-quartile PE-backed software companies operate.

Three findings are load-bearing for the recommendations below:

**Finding 1 — The platform is partly unified, fully under strain.** [Client] operates [N] production codebases inherited from the predecessor companies. A shared identity/auth layer was added in [year], and [X]% of customer-facing features now cross codebases. The remaining [Y]% live inside their predecessor-of-origin and cannot currently be moved without breaking customer integrations. Engineering time allocated to cross-system integration and bug-fixing currently estimated at [XX%] of total engineering effort, based on ticket categorization over the last 6 months.

**Finding 2 — Quality practice is uneven across teams.** Legacy teams inherit deep domain knowledge but traditional practices. Newer teams inherit modern tooling but thin coverage. Test integrity (see Methodology Ch. 6) varies from "behavioral contract tests dominate" in one codebase to "structural-inspection tests and broken test collection" in another. CI pipelines similarly vary from 2-minute modern shape in one repo to 18-minute legacy shape in another.

**Finding 3 — AI is not yet operationally integrated.** Individual engineers use AI tools informally. No org-wide adoption of Claude Code, Cursor, or equivalent. No LLM-based product features. No ML models in production decision-making. The surface area of potential productivity gains is large.

On all three fronts, [Client] is not in an unusual or concerning position — it is in the *typical* position of a PE-backed rollup at month [X]. The opportunity is not to fix something broken; it is to accelerate through the next 12 months of evolution that would otherwise take 24-36.

We recommend [Client] proceed with three pilots, prioritized by impact-per-dollar, described in §4. If executed in sequence over 6 months, we project:

| Metric | Baseline | 6-month target |
|---|---|---|
| Deploy frequency (median team) | [X]/week | [Y]/week (+2× to +4×) |
| PR cycle time (open to merge, median) | [X] days | [Y] days (−40 to −60%) |
| Engineering time on cross-system integration | [X]% | [Y]% (−20 to −40 percentage points) |
| Test collection success | [X]% | 100% |
| Load-bearing duplications (threshold values, config constants) | [X] | 0 |
| Files > 500 LOC | [X] | [Y] (−50% minimum) |
| AI-tool adoption (engineers using Claude Code / Cursor daily) | ~[X]% | >80% |

These targets are set to what we have seen delivered at comparable companies — not optimistic forecasts. The pilots are designed to make each metric measurable in isolation.

---

## 1. What we observed

### 1.1 Codebase shape

Ten primary repositories and [N] secondary repositories audited.

| Repo | LOC | Largest file | Files >500 LOC | Test count | Test pass rate | Predecessor |
|---|---|---|---|---|---|---|
| [repo-1] | [X]K | [Y] lines | [N] | [M] | [%] | [predecessor A] |
| [repo-2] | [X]K | [Y] lines | [N] | [M] | [%] | [predecessor B] |
| [repo-3] | [X]K | [Y] lines | [N] | [M] | [%] | [predecessor C] |
| [repo-4] | [X]K | [Y] lines | [N] | [M] | [%] | [predecessor D] |
| [repo-5] | [X]K | [Y] lines | [N] | [M] | [%] | [new, post-merger] |

Key observations:
- [Client] has at least [X] files exceeding 500 lines across all repositories. Largest: [Y] lines in [repo]. Industry-standard ceiling is 300-500 lines; at this scale, decomposition delivers measurable velocity improvement. See Methodology Ch. 2.
- We identified [N] load-bearing duplications — pieces of business logic or configuration that exist in more than one place. The most significant: [specific example, e.g., "tariff calculation logic exists in 3 different repos with subtle differences"]. See Methodology Ch. 3.
- [N] stub implementations were found — code that looks like real external integration but returns hardcoded values. Noted and flagged for immediate review. See Methodology Ch. 4.

### 1.2 Delivery metrics (last 6 months)

| Metric | Value | Industry p50 (PE SaaS at similar scale) |
|---|---|---|
| Commits per week (org total) | [X] | [~X] |
| PRs merged per week | [X] | [~X] |
| Median PR size (lines touched) | [X] | [100-300] |
| Median PR cycle time (open to merge) | [X] days | [1-3 days] |
| Revert rate (reverts / merges) | [X]% | [<2%] |
| Deploy frequency (production) | [X]/week | [daily or better] |
| CI runtime (p50 across repos) | [X] minutes | [<5 minutes] |
| Build/test flakiness incidents per week | [X] | [<1] |

### 1.3 Team composition and process

Interviewed [N] senior engineers, 1 hour each. Composite observations (attributed anonymously per §6):
- *"The thing that slows us down most is [X]."* — [common thread across N of M interviews]
- *"If I could change one thing with a magic button, it would be [Y]."* — [frequency]
- *"The part I'm most afraid to touch is [Z]."* — [frequency; usually points to a god file or a load-bearing duplication]

Ticket/issue analysis across [tracker] for last 6 months:
- [X]% of tickets tagged "tech debt" (vs. industry norm [Y]%)
- [X]% of tickets "blocked" at any given time (vs. [Y]%)
- [X] incidents of production regressions introduced and reverted within [Z] hours

### 1.4 AI and tooling maturity

- **Individual adoption:** [N of M] interviewed engineers use Claude, ChatGPT, or Cursor informally. No consistent workflow across the team.
- **Organizational adoption:** No deployment of Claude Code, Cursor, or equivalent as a team-wide tool. No shared prompt library. No internal documentation on AI-assisted refactoring practices.
- **Production AI features:** None in the user-facing product. No ML models, no LLM integrations, no AI-driven decision support.
- **Data infrastructure:** [Assessment of data lake / warehouse / pipelines]. Current state is [X]; baseline for any future ML work would require [Y].

---

## 2. What we concluded

### 2.1 The rollup is in mid-consolidation, on-schedule for its vintage

[Client] is [N] months post-merger (or [Y] years into Vortex ownership for the anchor company). By comparison with [3-4 named anonymized comparables], they are at the stage we expect. Nothing is on fire. Nothing is catastrophically mismanaged. The assessment is *"on track for this vintage, accelerable"* — not *"behind"* and not *"ahead."*

### 2.2 Three structural bottlenecks account for most of the engineering time loss

Based on ticket analysis, interview triangulation, and codebase patterns:

**Bottleneck A (~[X]% of engineering time): cross-codebase integration work.** When a customer-facing change touches two or more predecessor codebases, the work crosses team boundaries, requires coordinated PRs, and is prone to regression. Estimated engineering hours lost to this per sprint: [N]. This is the single largest productivity drag.

**Bottleneck B (~[X]% of engineering time): long PR cycle times.** Median PR open-to-merge is [X] days. Industry norm for companies at similar scale is [Y] days. The gap is typically driven by manual review bandwidth, not CI speed (CI is [Z] minutes, fast enough). Automating the review and triage workflow with AI-assisted tooling typically halves this gap.

**Bottleneck C (~[X]% of engineering time): operational firefighting across legacy systems.** Older codebases generate a disproportionate share of production incidents. We observed [X]% of incidents in the last 6 months originated in [Y]% of the code (the oldest predecessor's codebase). This is the textbook legacy-concentration pattern.

### 2.3 AI is a greenfield opportunity, not a salvage operation

Because AI is not yet operationally integrated at [Client], we are not replacing or upgrading existing tooling. We are installing for the first time. Greenfield AI integration at this scale and this post-merger vintage has a cleaner cost-benefit profile than mid-stream upgrades of entrenched tooling.

---

## 3. Archive vs. refactor recommendation

Applying the Ch. 10 scoring framework:

| Dimension | Score (1-5) | Reasoning |
|---|---|---|
| Audit backlog size | [X] | [One-line reasoning] |
| Load-bearing duplication | [X] | [One-line reasoning] |
| Stub density | [X] | [One-line reasoning] |
| Test integrity debt | [X] | [One-line reasoning] |
| Architectural confusion | [X] | [One-line reasoning] |
| Team consensus | [X] | [One-line reasoning] |
| **Total** | **[XX]** | |

**Recommendation:** [refactor in place / aggressive refactor / archive-and-rebuild — likely the middle option for [Client]].

This call applies to the platform as a whole. Individual sub-systems may warrant different treatment — in particular the oldest predecessor's codebase may warrant archive-and-rebuild of specific modules.

---

## 4. Recommended pilots (ranked by impact-per-dollar)

### Pilot A — Cross-codebase integration layer + god-file decomposition
**Duration:** 6 weeks | **Cost:** €[40-60]K | **Team:** 2 AI-Whisperers engineers + 1 [Client] engineer (part-time)

**Scope:** Apply Chapter 2 (god-file decomposition) and Chapter 3 (load-bearing duplication) to the top 5 most-modified files across the 3 largest codebases. Establish a shared canonical location for the [N] load-bearing duplications we identified. Build an integration-layer API that reduces the coupling between [codebase A] and [codebase B].

**Success criteria:**
- Files >500 LOC count reduces from [X] to [Y]
- All [N] load-bearing duplications consolidated to single sources of truth, with CI gates preventing regression
- Cross-codebase PR count (PRs touching 2+ repos) reduces by at least [X]% over the following quarter
- Zero production regressions introduced by the pilot

**ROI estimate:** Based on comparable engagements, we estimate 10-20% reduction in engineering time on integration work within 6 months, translating to ~[X] FTE equivalents of freed capacity.

### Pilot B — CICD consolidation + quality gate rollout
**Duration:** 3 weeks | **Cost:** €[20-30]K | **Team:** 1 AI-Whisperers engineer + 1 [Client] DevOps engineer (part-time)

**Scope:** Apply Chapter 5 (CICD rebuild) and Chapter 9 (quality gate hierarchy) across all [N] repositories. Consolidate workflow sprawl. Eliminate `continue-on-error: true` on load-bearing checks. Establish unified lint + typecheck + test standards.

**Success criteria:**
- CI runtime (p50) reduces by at least 50% in the repos it's long in
- Test collection success reaches 100%
- Advisory-gate count reaches 0
- Ruff/mypy/equivalent errors reach 0 and are enforced

**ROI estimate:** Direct engineering time savings from faster, more trustworthy CI. Typical range: 3-5% of total engineering time recovered within 3 months.

### Pilot C — AI-native refactoring deployment across 1 team
**Duration:** 4 weeks | **Cost:** €[25-35]K | **Team:** 1 AI-Whisperers engineer embedded with 1 [Client] team

**Scope:** Apply Chapter 7 (AI-augmented refactoring) to one specific team's working rhythm. Train the team on the session shape, the prompting patterns, and the review discipline. Produce 20-30 committed PRs during the pilot as the training artifacts. Measure pre/post metrics on that team's cycle time, LOC delivered, and review-to-generation ratio.

**Success criteria:**
- Team's median PR cycle time reduces by at least [X]%
- Team's deploy frequency increases by at least [Y]%
- Team reports (via 3 retro questions at end of pilot) improved confidence in their workflow
- Methodology documented locally so the team can continue the practice without us

**ROI estimate:** The first team sets the pattern for org-wide rollout. Direct ROI of the pilot is smaller than A or B; the larger value is the template for extending to all teams.

### Not recommended (and why)
- **Large-scale architectural rewrite.** [Client] scores [XX] on the Ch. 10 framework — below the rebuild threshold. An in-place transformation approach is correct.
- **Immediate ML/AI product feature work.** The infrastructure and data foundations are not ready. Sequence it after the operational pilots land.
- **CRM / billing system replacement.** Out of scope for this engagement and would require specialized partner.

---

## 5. 30-60-90 day roadmap (if [Client] proceeds)

| Days | Activity |
|---|---|
| 0-14 | Contract countersignature, kickoff for Pilot A (highest-impact) |
| 15-30 | Pilot A mid-point: first 3 god files decomposed, first 2 load-bearing duplications consolidated |
| 31-60 | Pilot A completion + Pilot B kickoff |
| 61-90 | Pilot B completion + Pilot C kickoff, Pilot A sustain review |
| 90 | Joint review with [Client] + Vortex: assess results, decide on extending to org-wide transformation |

If all three pilots land their success criteria, the natural next step is an org-wide transformation engagement (12-month scope). That engagement is not in this SOW and would be a separate agreement, sized and structured at that point.

---

## 6. Interview notes (anonymized)

[Per §3 of the SOW, raw anonymized interview notes are attached as a separate PDF. In the sample deliverable they are redacted; in a real deliverable each interviewee's observations are grouped around the four standard questions.]

---

## Appendix — methodology references

Each finding above maps to one or more chapters of our methodology playbook:

| Finding | Methodology Chapter |
|---|---|
| Codebase shape, file size ceiling | [Ch. 2: God-file decomposition](../../methodology/02-god-files.md) |
| Load-bearing duplications | [Ch. 3: Load-bearing duplication](../../methodology/03-load-bearing-duplication.md) |
| Stub implementations | [Ch. 4: Stub elimination](../../methodology/04-stub-elimination.md) |
| CICD + workflow sprawl | [Ch. 5: CICD rebuild](../../methodology/05-cicd-rebuild.md) |
| Test integrity, coverage-of-public-surface | [Ch. 6: Test integrity](../../methodology/06-test-integrity.md) |
| AI-augmented refactoring session discipline | [Ch. 7: AI-augmented refactoring](../../methodology/07-ai-refactoring.md) |
| Quality gate hierarchy | [Ch. 9: Quality gate hierarchy](../../methodology/09-quality-gates.md) |
| Archive-vs-refactor decision | [Ch. 10: Archive vs. refactor](../../methodology/10-archive-vs-refactor.md) |

## Appendix — raw data

Separate attachments at delivery:
- Metrics CSV (all figures in this document, in tabular form, with query source)
- Interview transcripts (anonymized)
- Repository-level audit reports (one per audited repo)
- Ticket categorization data
