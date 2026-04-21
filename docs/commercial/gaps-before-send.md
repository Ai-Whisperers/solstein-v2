# Gaps before external send

Single source of truth for "what must be true before any external commercial motion begins." Updated as gaps are closed or surfaced.

**Status as of 2026-04-21:** NOT READY. 6 P0 gaps and 12 P1 gaps open.

## The six pre-send gates (from critic review)

These are non-negotiable. All must be green before external motion.

| Gate | Status | Owner | Blocker |
|---|---|---|---|
| G1. Michiel identity resolved | 🔴 Open | Founders | Need to contact Michiel directly and confirm full name + role |
| G2. One paid external reference engagement complete | 🔴 Open | Founders + commercial | No engagement signed yet |
| G3. SOW + PPA + equity term sheet legally reviewed | 🔴 Open | Founders + EU counsel | Counsel not retained |
| G4. Legal entity + insurance + DPA / GDPR posture defined | 🔴 Open | Founders + EU counsel | Paraguay-only currently |
| G5. Pitch deck portfolio-audit slide restructured | 🟡 Open | Content | Awaiting full deck build (currently only outline) |
| G6. Phase 1 repricing decision | 🔴 Open | Founders | Not yet made: loss-leader with reference rights, OR full-price at €50-75K? |

## P0 gaps (blocks external motion)

- **P0.1** — Michiel identity (G1 above)
- **P0.2** — Eneve-specific Phase 1 sample deliverable (not the generic template)
- **P0.3** — Legal posture per `legal-posture.md` minimum viable (L1-L6 + L10 + L14)
- **P0.4** — Security posture per `security-posture.md` minimum viable (S2-S4 + S6 + S8 + SOC 2 alignment doc)
- **P0.5** — First external paid reference (G2)
- **P0.6** — Pricing decision (G6)

## P1 gaps (credibility-critical)

- **P1.1** — Named team filled in (`team-capacity.md`)
- **P1.2** — Warm-intro email templates reviewed and locked (see `email-templates.md`)
- **P1.3** — References willing to take a call (blocked on P0.5)
- **P1.4** — Competitive positioning (done: `competitive-positioning.md`)
- **P1.5** — Repository visibility decision: public or private? Currently private. When does Vortex see our methodology — before or after NDA?
- **P1.6** — Case study anonymization guide for future engagement write-ups
- **P1.7** — Phase 2 pricing decision (see `internal/pricing-economics.md`)
- **P1.8** — PPA retainer repricing decision (€10K → €15-20K?)
- **P1.9** — Liability cap strategy for utility/regulated-sector engagements
- **P1.10** — Equity term sheet sponsor-conflict clause rewrite (see critic finding CV3)
- **P1.11** — Ch. 8 (ticket automation) benchmark claims removed from pitch deck / sample deliverable (replaced with "design-stage, not yet executed")
- **P1.12** — "AI-native" definition page or remove the phrase from 30+ of its 40+ uses

## P2 gaps (should-have)

- **P2.1** — Data-processing addendum (DPA) template
- **P2.2** — Master services agreement template (vs. per-engagement SOW)
- **P2.3** — Post-engagement close-out checklist
- **P2.4** — Refresh of Solstein universe enrichment with verified real data on 50 companies (currently 13 verified)
- **P2.5** — Proof of insurance certificate
- **P2.6** — Subprocessor register
- **P2.7** — Incident response plan

## What closing each gate unlocks

- G1 + P1.2 → warm-intro motion can activate
- G2 → every conversation becomes credible (or at least verifiable)
- G3 + G4 + P0.3 → we can countersign SOWs
- G5 → pitch deck can be built for live use
- G6 + P1.7 + P1.8 → pricing is defensible in negotiation
- P0.2 → Eneve conversation has a concrete artifact, not a template

## Decisions required from founders

These are the decisions I (the autonomous writer) cannot make:

1. **Jurisdiction / entity strategy** — establish EU entity, partner with EU-domiciled firm, or stay Paraguay-only?
2. **Insurance spend** — €2-5K/year for E&O + CGL, commit before engagements?
3. **First-engagement pricing** — loss-leader at €25K with reference rights OR full-priced at €50-75K?
4. **Retainer pricing** — €10K/month or €15-20K/month?
5. **Team commitment** — who is named as Lead and Partner on engagement SOWs, with what FTE allocation?
6. **Hiring plan** — when does the team grow? What's the revenue gate?
7. **External reference strategy** — do we seek a friendly below-cost first engagement, or wait for a full-price first engagement?

None of these are AI-automatable. All need founders' time.

## Gap-close cadence

This file is updated by anyone who closes a gap or surfaces a new one. Git commit message: *"gaps: {gap-id} closed — {brief reason}"* or *"gaps: {gap-id} opened — {context}"*.

Review cadence: every week, walk through the list. If a gap has been open for >30 days, either resolve it or decide to descope. Don't let gaps age indefinitely.

## Related

- `docs/critique/2026-04-21-hostile-review.md` — source of most P0/P1 gaps
- `docs/commercial/legal-posture.md` — details on legal gaps
- `docs/commercial/security-posture.md` — details on security gaps
- `docs/commercial/team-capacity.md` — details on team gaps
- `docs/commercial/internal/pricing-economics.md` — details on pricing gaps
