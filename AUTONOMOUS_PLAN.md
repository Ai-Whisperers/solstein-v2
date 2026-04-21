# Autonomous work plan — 2026-04-21

**Goal:** during a 5+ hour autonomous run, advance the Eneve proposal package from "readiness artifacts drafted" to "sendable package with real data, tested, peer-reviewed." Include Vortex-focused materials discovered during the research phase.

**Ground rules**
- No external messaging (user has been explicit)
- No destructive operations
- Commit every ~30 min of progress
- No fake data — if an enrichment can't be verified, flag `None` with reason
- Honest about gaps — don't paper over

## Work items

### Block A — Real data for the universe
- [ ] A1: Outside-in research on 12-15 highest-signal universe companies; produce structured fixture data for each (revenue, employees, founded_year, country, ticker if public, github_org if public)
- [ ] A2: Promote researched fixtures into a new enriched universe JSON
- [ ] A3: Run Solstein pipeline on the enriched universe; capture output

### Block B — Engineering: narrative generator
- [ ] B1: Add a `solstein narrate` CLI that takes a pipeline output universe JSON and produces an analytical deal-team brief with qualitative observations (not just tables)
- [ ] B2: Tests for the narrative generator
- [ ] B3: Rerun the pipeline + narrate on the enriched universe → sample brief

### Block C — Vortex-angle reframe
- [ ] C1: Outside-in research on Vortex Capital Partners' known portfolio
- [ ] C2: Portfolio-level transformation-readiness brief — a Solstein-ish assessment of Vortex's portcos, not just Eneve
- [ ] C3: Variant SOW for a PE-portfolio engagement (vs. single-company engagement)

### Block D — Commercial kit expansion
- [ ] D1: Equity term sheet template (flagged "legal review required")
- [ ] D2: Pitch deck outline (markdown; slide-by-slide structure)
- [ ] D3: Engagement onboarding checklist — what we need from day 1

### Block E — Methodology
- [ ] E1: Chapter 8 (ticket lifecycle automation) — written as a design doc, clearly labeled "not yet executed in a real engagement"
- [ ] E2: Sample prompt library for AI-augmented refactoring (one file per pattern)

### Block F — Self-critique pass
- [ ] F1: Critic-agent review of the full package; produce a findings doc
- [ ] F2: Address top critiques; strengthen weakest sections

### Block G — Repo hygiene
- [ ] G1: Top-level README updated to reflect all docs
- [ ] G2: docs/INDEX.md — single entry point for the proposal package
- [ ] G3: Ensure all cross-links work

## Acceptance criteria

Each block produces committed artifacts on `main`. All engineering changes keep `pytest`, `ruff`, and `mypy` clean. The final state of the repo is browseable end-to-end — a hostile reader could navigate from `README.md` to every other document without dead links.

## Stop conditions

- User interrupts
- Same error repeated 3× across fix attempts
- Blast-radius actions needed (credential rotation, deletion of shared infra)
- All blocks complete

## What is explicitly NOT in scope

- Sending anything externally
- Creating fake data to look impressive
- Recommending destructive architectural changes to v1 (v1 is archived)
- Engineering changes that would require paid API keys (Crunchbase, LinkedIn Talent Insights)
