# Pricing economics — INTERNAL ONLY

> ⚠️ **This document is internal.** Do not include it in any artifact sent to a counterparty. It contains cost basis, margin assumptions, and capacity constraints that should not be visible to clients or PE firms.

## Why it exists separately

The critic review (2026-04-21) flagged that pricing appendices inside the SOW template and PPA template would leak the firm's cost basis if the "internal only" label were missed during any send. That risk is structural — internal content does not belong in templates that might get auto-emailed. This file is the single location for pricing rationale. It never gets sent.

## Phase 1 diagnostic — €25,000 fixed fee

Target profit at €25K flat:

| Line item | Cost (€) |
|---|---|
| Lead engineer: 10 working days | 6,500 |
| Partner: 4 working days (oversight + presentation) | 4,800 |
| Total direct labor | 11,300 |
| Tooling / API costs | 300 |
| Overhead allocation (25%) | 2,900 |
| **Total cost** | **14,500** |
| **Fee** | **25,000** |
| **Gross margin** | **10,500 (42%)** |

### The critic's concern with this price

Per the 2026-04-21 review: *"€25K for a 2-week engagement by 2 people is self-defeating. That margin does not cover sales cost, no-sale deals, revisions, or a second client's diligence request. It is a €25K loss-leader priced as a product."*

This is a legitimate challenge. Two honest interpretations:

**Interpretation A** — first-engagement pricing. For the first 3-5 engagements, €25K is priced below true sustainable margin in exchange for reference rights, case study production rights, and the structural value of delivered work. Documented as such, explicitly, in the SOW (add a clause: *"Provider may reference this engagement anonymously in future marketing, subject to Client's pre-approval of specific materials"*).

**Interpretation B** — price it properly now. Real sustainable fee for a 2-person, 2-week engagement with partner oversight, insurance coverage, sales cost allocation, and normal margin is probably **€45-60K**. This is what MBB Digital charges for similar-scope engagements; the gap between us and them is credibility, not delivery cost.

### Recommended posture

Go with Interpretation A for the first 3 engagements with explicit labeling, then shift to Interpretation B. The SOW template should support both modes — current version represents the low/early-engagement price. Do not mix them in one proposal.

## Phase 2 pilot — €40,000-€60,000

Per-pilot pricing, sized by scope. Cost breakdown for a 6-week, 2-engineer pilot:

| Line item | Cost (€) |
|---|---|
| 2 engineers × 6 weeks × €1,300/day | 78,000 |
| Partner oversight (20% time × 6 weeks × €1,800/day) | 10,800 |
| Tooling / API costs | 1,500 |
| Overhead allocation (25%) | 22,500 |
| **Total cost** | **112,800** |

At €50K fee, **gross margin is negative** (€62,800 loss). This is obviously untenable. Phase 2 pricing of €40-60K works only if:
- The engineers are internal not contracted (dropping labor cost significantly)
- Partner time is much less than 20% (probably realistic at 5-10%)
- Overhead is lower (defensible only if the firm is very small)

### Honest Phase 2 pricing

A 6-week, 2-engineer pilot delivered with full partner oversight, insurance, and sustainable margin should be **€75-120K**. The "€40-60K" in the pitch deck is aspirational, below true cost.

**Recommended action:** rewrite Phase 2 economics before committing them to a proposal. Current SOW template leaves Phase 2 pricing open; that's the correct move. Do not pre-commit.

## PPA retainer — €10K/month

The critic flagged: *"For Vortex — trivially cheap. For a 2-person firm — reserved capacity you cannot credibly deliver."*

Expected annual economics per PPA at steady state:

| Revenue stream | Low | Expected | High |
|---|---|---|---|
| Retainer (€10K × 12) | €120K | €120K | €120K |
| Phase 1 engagements (3-5/yr × €25K) | €75K | €100K | €125K |
| Phase 2 pilots (1-3/yr × €50K) | €50K | €100K | €150K |
| Phase 3 (0-1/yr, equity-inclusive) | €0 | €50K | €200K |
| **Total annual** | **€245K** | **€370K** | **€595K** |

### The capacity problem

Per the PPA's stated retainer services: *4 readiness assessments per quarter*, *48-hour diligence support*, *quarterly portfolio benchmark reports*, plus *right of first review* on new investments. The critic's math: 3-4 FTE, not 1.5.

Verification:
- 16 readiness assessments per year × ~3 days each = 48 days
- ~8 diligence-support requests × ~2 days each = 16 days  
- Quarterly benchmarks × 5 days each = 20 days
- 3 Phase 1 engagements × 14 days (lead) + 6 days (partner) = 60 days
- 1-2 Phase 2 pilots × 60 days (lead) + 15 days (partner) = 90 days
- Sales / admin / revision overhead ~ 20% of above = ~45 days

Total: ~280 days of lead + ~80 days of partner = roughly 1.5 FTE lead + 0.4 FTE partner = ~2 FTE. The critic was slightly high at 3-4 but directionally correct: the PPA is NOT a 1.5-FTE commitment at our stated volumes. It's ~2 FTE.

### What to change

1. Cap retainer services to make the loading explicit: "up to X assessments per quarter" (current SOW has this; keep it firm)
2. Do not take on a second PPA until capacity is verified at scale
3. Price retainer to reflect the 2-FTE loading: €10K/month × 1 PPA is ~€120K/yr, which at 2 FTE × €100K/yr loaded cost = zero margin. **Retainer should be €15-20K/month**, not €10K/month, for this to be sustainable.

## Risks

- **Single-PPA dependency.** A PE firm that exits 2-3 largest portcos simultaneously drops our engagement pipeline dramatically. Mitigation: 3-5 parallel PPAs, no one PPA above 40% of revenue.
- **Pricing race.** If other transformation-services firms target the same segment with lower prices, we either cut price (unsustainable given cost basis) or invest in differentiation (the methodology, the case studies).
- **Partner time.** Partner oversight is our bottleneck. Every PPA committing to "partner attention" consumes the same finite partner hours. Capacity model must reflect this.

## Break-even

For the firm as a whole (not just one PPA): break-even at ~2 active PPAs + 4-6 standalone Phase 1 engagements per year. Below that, the firm is not self-sustaining; any founder salary or growth investment comes from savings or outside capital.

## Pricing honesty

The package currently presents pricing as confident numbers. Internally we should be explicit that:

- Phase 1 at €25K is loss-leader / reference pricing
- Phase 2 at €40-60K is below true cost and should be re-priced before any live proposal
- PPA at €10K/month is below sustainable for the service commitment
- Equity structures compensate for under-priced cash in later phases, but don't solve the near-term

**Before external pricing discussions, the pricing economics need a human round of review and decision on which direction to go** — under-price as loss-leaders with reference rights baked in, or price honestly at full rate and accept slower commercial momentum.

## Related

- `docs/commercial/phase-1-sow-template.md` — Phase 1 SOW (client-facing)
- `docs/commercial/portfolio-partnership-agreement-template.md` — PPA (client-facing)
- `docs/critique/2026-04-21-hostile-review.md` — where these concerns first surfaced
