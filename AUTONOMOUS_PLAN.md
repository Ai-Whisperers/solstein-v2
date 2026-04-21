# Autonomous work plan — round 2 — 2026-04-21

Continuation of the first 5-hour autonomous run. Same ground rules:
no external messaging, no destructive ops, commit every ~30 min of progress, no fake data, honest about gaps.

## Round 1 recap (archived)

19 tasks complete across 7 workstreams. Full log: git log + `docs/critique/2026-04-21-hostile-review.md`. 51 tests passing, mypy strict clean, ruff clean.

## Round 2 goal

Close the genuine engineering and commercial gaps that round 1 identified but didn't resolve. Nothing new that requires human decisions — only work that adds substance without creating new unaddressed promises.

## Work blocks

### Block H — Engineering depth (highest leverage)
- [ ] H1: Website-scraping adapter — enrich private companies from public site + careers/blog. Respects robots.txt, non-aggressive.
- [ ] H2: AI-maturity extractor — derive a signal from website content + job postings (ML role keywords, AI product language, OSS org activity).
- [ ] H3: HTTP cache — re-runs shouldn't hammer external APIs.
- [ ] H4: Excel improvements — conditional formatting, per-tier sheets.
- [ ] H5: Integration test suite for the full pipeline.

### Block I — Commercial completeness
- [ ] I1: RFP response template
- [ ] I2: Objection-handling cheatsheet (internal)
- [ ] I3: Mutual NDA template (draft, flagged for legal review)
- [ ] I4: Partner-meeting prep checklist
- [ ] I5: Change order template (for SOW modifications during engagement)

### Block J — Second universe (prove Solstein isn't energy-specific)
- [ ] J1: Research 10-15 Dutch/Benelux PE-backed B2B SaaS companies (not energy)
- [ ] J2: Populate universe JSON with verified fields
- [ ] J3: Run pipeline, produce sample brief

### Block K — Methodology prompts (deepen the library)
- [ ] K1: Dependency upgrade prompt (safe modernization)
- [ ] K2: Migration-planning prompt (one system → another)
- [ ] K3: Incident postmortem prompt
- [ ] K4: Sponsor communication prompt (weekly brief template)
- [ ] K5: First-week diagnostic kickoff prompt

### Block L — Critic round 2
- [ ] L1: Re-run hostile critic against updated package
- [ ] L2: Address second-round findings

### Block M — Engineer onboarding + governance
- [ ] M1: "First 90 days" runbook for a new AI-Whisperers engineer
- [ ] M2: CONTRIBUTING.md for the repo
- [ ] M3: Architecture decision record (ADR) template + 3 backfill ADRs for v2's core decisions

## Acceptance criteria

Same as round 1: all engineering keeps gates green (pytest / ruff / mypy). All docs honest. Every commit pushes. Final state has cross-links working.

## Stop conditions

Same. Stop on completion, destructive need, repeated error, or resource exhaustion.

## What is explicitly NOT in scope

- Sending anything externally
- Paid API keys (Crunchbase, LinkedIn, etc.) — still out of scope
- New corporate/legal decisions — still out of scope
- Fabricating case studies, clients, or references
