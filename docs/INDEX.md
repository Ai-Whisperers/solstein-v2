# Documentation index

Single entry point for navigating the Solstein v2 repository.

## Audience-keyed reading paths

### "Just tell me what this is"
1. [README.md](../README.md) — what Solstein v2 is and isn't
2. [BUSINESS.md](BUSINESS.md) — the actual business model

### "I'm an engineer onboarding to the codebase"
1. [README.md](../README.md) — quick overview
2. [ARCHITECTURE.md](ARCHITECTURE.md) — the rules + file budget
3. [universe-schema.md](universe-schema.md) — input format
4. [methodology/07-ai-refactoring.md](methodology/07-ai-refactoring.md) — how we work with AI

### "I'm preparing for a commercial conversation"
1. [BUSINESS.md](BUSINESS.md) — what AI-Whisperers actually sells
2. [commercial/competitive-positioning.md](commercial/competitive-positioning.md) — vs. alternatives
3. [commercial/gaps-before-send.md](commercial/gaps-before-send.md) — what must be done first
4. [commercial/legal-posture.md](commercial/legal-posture.md) — legal/insurance gaps
5. [commercial/team-capacity.md](commercial/team-capacity.md) — who's on the engagement
6. [critique/2026-04-21-hostile-review.md](critique/2026-04-21-hostile-review.md) — what a sharp reader will say

### "I want to understand the methodology"
1. [methodology/README.md](methodology/README.md) — the 10-chapter index
2. Chapters 1-10 in order, or pick the one relevant to a specific transformation move
3. [methodology/prompts/README.md](methodology/prompts/README.md) — reusable AI prompts

### "I'm assessing whether AI-Whisperers can deliver this"
1. [case-studies/solstein-v1-to-v2.md](case-studies/solstein-v1-to-v2.md) — internal methodology validation
2. [methodology/README.md](methodology/README.md) — full methodology
3. [critique/full-review.md](critique/full-review.md) — honest hostile review
4. [commercial/team-capacity.md](commercial/team-capacity.md) — who actually delivers

## Map of all documents

### Code-adjacent
- [`../README.md`](../README.md) — repository overview
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — the rules we inherited from v1's mistakes
- [`BUSINESS.md`](BUSINESS.md) — equity-for-transformation thesis
- [`universe-schema.md`](universe-schema.md) — Solstein input format
- [`../AUTONOMOUS_PLAN.md`](../AUTONOMOUS_PLAN.md) — last autonomous run plan

### Case studies
- [`case-studies/solstein-v1-to-v2.md`](case-studies/solstein-v1-to-v2.md) — internal v1→v2 rebuild

### Methodology playbook (10 chapters)
- [`methodology/README.md`](methodology/README.md) — index
- [`methodology/01-diagnostic.md`](methodology/01-diagnostic.md) — Phase 1 framework
- [`methodology/02-god-files.md`](methodology/02-god-files.md) — file decomposition
- [`methodology/03-load-bearing-duplication.md`](methodology/03-load-bearing-duplication.md) — same-rule-multiple-places bug
- [`methodology/04-stub-elimination.md`](methodology/04-stub-elimination.md) — finding fake data
- [`methodology/05-cicd-rebuild.md`](methodology/05-cicd-rebuild.md) — workflow consolidation
- [`methodology/06-test-integrity.md`](methodology/06-test-integrity.md) — behavioral vs. structural
- [`methodology/07-ai-refactoring.md`](methodology/07-ai-refactoring.md) — human+AI working pattern
- [`methodology/08-ticket-lifecycle-automation.md`](methodology/08-ticket-lifecycle-automation.md) — ticket → PR (design only)
- [`methodology/09-quality-gates.md`](methodology/09-quality-gates.md) — lint/typecheck/test hierarchy
- [`methodology/10-archive-vs-refactor.md`](methodology/10-archive-vs-refactor.md) — when to burn it down

### Methodology prompt library
- [`methodology/prompts/README.md`](methodology/prompts/README.md) — index
- [`methodology/prompts/god-file-decompose.md`](methodology/prompts/god-file-decompose.md)
- [`methodology/prompts/load-bearing-duplication-find.md`](methodology/prompts/load-bearing-duplication-find.md)
- [`methodology/prompts/stub-audit.md`](methodology/prompts/stub-audit.md)
- [`methodology/prompts/test-structural-to-behavioral.md`](methodology/prompts/test-structural-to-behavioral.md)
- [`methodology/prompts/refactor-session-plan.md`](methodology/prompts/refactor-session-plan.md)
- [`methodology/prompts/ci-consolidate.md`](methodology/prompts/ci-consolidate.md)

### Assessments
- [`assessments/eneve/README.md`](assessments/eneve/README.md) — Eneve package overview
- [`assessments/eneve/outside-in-assessment.md`](assessments/eneve/outside-in-assessment.md) — public-signal analysis
- [`assessments/eneve/phase-1-sample-deliverable.md`](assessments/eneve/phase-1-sample-deliverable.md) — sample template
- [`assessments/vortex/portfolio-transformation-readiness.md`](assessments/vortex/portfolio-transformation-readiness.md) — portfolio-wide angle
- [`assessments/sample-run/`](assessments/sample-run/) — outputs from `solstein run` on enriched universe

### Commercial kit
- [`commercial/phase-1-sow-template.md`](commercial/phase-1-sow-template.md) — €25K Phase 1 SOW
- [`commercial/portfolio-partnership-agreement-template.md`](commercial/portfolio-partnership-agreement-template.md) — multi-year framework
- [`commercial/equity-term-sheet-template.md`](commercial/equity-term-sheet-template.md) — Phase 3 equity (LEGAL REVIEW REQUIRED)
- [`commercial/pitch-deck-outline.md`](commercial/pitch-deck-outline.md) — slide-by-slide
- [`commercial/engagement-onboarding-checklist.md`](commercial/engagement-onboarding-checklist.md) — kickoff
- [`commercial/competitive-positioning.md`](commercial/competitive-positioning.md) — vs. MBB, Thoughtworks, etc.
- [`commercial/team-capacity.md`](commercial/team-capacity.md) — honest team statement
- [`commercial/legal-posture.md`](commercial/legal-posture.md) — 14 legal gaps
- [`commercial/security-posture.md`](commercial/security-posture.md) — 8 security gaps
- [`commercial/email-templates.md`](commercial/email-templates.md) — DRAFT, not for sending
- [`commercial/gaps-before-send.md`](commercial/gaps-before-send.md) — pre-external-motion checklist
- [`commercial/internal/pricing-economics.md`](commercial/internal/pricing-economics.md) — INTERNAL ONLY

### Critique
- [`critique/2026-04-21-hostile-review.md`](critique/2026-04-21-hostile-review.md) — summary of P0/P1 findings
- [`critique/full-review.md`](critique/full-review.md) — verbatim hostile critique

## Status of the package

| Layer | State |
|---|---|
| Engineering (Solstein v2 tool) | Working: 18 source files, 51 tests passing, mypy strict clean, ruff clean |
| Methodology playbook | 9 of 10 chapters drafted with v1→v2 evidence; Ch. 8 design-only |
| Case studies | One internal (v1→v2). Zero external paid engagements. |
| Sample assessments | Eneve outside-in + Vortex portfolio readiness, both based on public signals |
| Commercial templates | Drafted but not legally reviewed, not pricing-finalized |
| Legal/security posture | NOT READY — see legal-posture.md and security-posture.md |
| External engagements | Zero. Nothing has been sent to Eneve or Vortex. |
| Pre-send gates | 6 of 6 OPEN — see gaps-before-send.md |

## Last updated

2026-04-21 — autonomous run round 1 (creation) + round 2 (critic addressing).

## Conventions

- Files at the root of `docs/` cover repository-wide concerns
- Subdirectories cover specific domains
- `internal/` subdirectories contain documents that should never leave the firm
- Markdown only; no PDF, no Word, no Confluence
- Cross-links use relative paths
