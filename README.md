# Solstein v2

Internal prospecting tool + transformation methodology for AI-Whisperers' equity-for-transformation business.

## What this is (and isn't)

**Is:** a focused internal tool plus a complete documentation package — methodology, case studies, commercial templates, sample assessments — that together support AI-Whisperers' commercial motion to PE firms and their portfolio companies.

**Is not:** a SaaS product sold to PE firms. That was v1. V1 is archived at [`Ai-Whisperers/solstein-v1-archive`](https://github.com/Ai-Whisperers/solstein-v1-archive).

## Repository structure (what's where)

```
.
├── README.md ............................ this file
├── AUTONOMOUS_PLAN.md ................... last autonomous-run plan
├── src/solstein/ ........................ the prospecting tool (Python)
├── tests/ ............................... unit + integration tests + fixtures
├── docs/
│   ├── INDEX.md ......................... master navigation
│   ├── ARCHITECTURE.md .................. engineering rules
│   ├── BUSINESS.md ...................... what AI-Whisperers actually sells
│   ├── universe-schema.md ............... pipeline input format
│   ├── case-studies/ .................... internal v1→v2 rebuild
│   ├── methodology/ ..................... 10-chapter playbook + prompt library
│   ├── assessments/ ..................... Eneve + Vortex outside-in research
│   ├── commercial/ ...................... SOW + PPA + equity + pitch + onboarding + legal/security posture
│   └── critique/ ........................ hostile review of the package
└── .github/workflows/ci.yml ............. lint + typecheck + test
```

**Read [`docs/INDEX.md`](docs/INDEX.md) for audience-keyed navigation paths.**

## Business context

AI-Whisperers' actual business is **taking equity (or fixed fees) in PE portfolio companies in exchange for AI-native transformation** (modernized CICD, ticket lifecycle automation, refactoring-with-AI, quality gates).

Solstein-the-tool finds candidate portcos. Solstein-the-package (everything in `docs/`) supports the engagement once a prospect is identified.

Eneve (€30M revenue Dutch energy software, owned by Vortex Capital Partners) is the first **engagement target** — *not yet a delivered engagement*. See `docs/assessments/eneve/README.md`.

This product serves the deal team. It does not serve external customers. It is small, fast, and honest.

## Current readiness state

Per [`docs/commercial/gaps-before-send.md`](docs/commercial/gaps-before-send.md):

| Layer | State |
|---|---|
| Engineering tool | ✅ Working — 51 tests passing, mypy strict clean |
| Methodology playbook | 🟡 9/10 chapters, evidence from internal v1→v2 only (no external engagements yet) |
| Commercial templates | 🟡 Drafted — pricing not finalized, not legally reviewed |
| Legal posture | 🔴 Not ready — see `docs/commercial/legal-posture.md` |
| Security posture | 🔴 Not ready — see `docs/commercial/security-posture.md` |
| External engagements | 🔴 Zero — Eneve has not been contacted |

**6 P0 pre-send gates open** (see `docs/commercial/gaps-before-send.md`). The package is internal readiness; nothing is ready to send to a counterparty.

## Scope

- 6-8 real data sources (httpx-native, no stubs)
- One canonical scoring pipeline, one place for thresholds
- Excel + Markdown export
- One CLI
- ~15 source files target; hard stop if we approach 30

## What v1 taught us (honest)

- 659 files, 112K LOC, 28% coverage, 73 epics of remediation, 70% pipeline field loss, 7 stub agents returning fake data. Keeping it cost ~33 weeks of remediation. Rebuilding it costs ~6-8.
- The real deliverables — the Eneve case study, the transformation methodology, the equity term sheet — were never engineering problems. Building more pipeline code didn't help.
- Solstein is an internal prospecting tool. That's the whole scope. Anything bigger is sunk-cost reasoning.

## Layout

```
src/solstein/
  adapters/       One module per real data source. httpx-native, typed, tested.
  scoring/        Scoring functions + the single threshold registry.
  enrichment/     Third-party enrichment (Crunchbase, LinkedIn, Yahoo Finance).
  pipeline/       The canonical end-to-end pipeline. One file.
  export/         Excel + Markdown writers.
  cli/            One CLI entrypoint.
tests/
  unit/           Fast, isolated.
  integration/    Real-adapter smoke tests. Gated by env vars.
  fixtures/       Frozen scoring fixtures (Eneve regression harness).
```

## Quickstart

```bash
uv sync
uv run solstein run --universe eneve-competitors --output out/
```

## Development

```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run pytest
uv run mypy src/solstein
```

## CI

GitHub Actions: lint → typecheck → test on every PR. No mystery.

## Honesty about scope

The repository contains substantially more documentation than code. This is intentional — the methodology, case studies, and commercial templates are the primary deliverable for AI-Whisperers' commercial motion. The Solstein code itself is internal tooling that supports them.

The package was reviewed by a hostile critic (see `docs/critique/`) and revised in response. Many gaps remain explicit and tracked — see `docs/commercial/gaps-before-send.md`.

## Related

- [`Ai-Whisperers/solstein-v1-archive`](https://github.com/Ai-Whisperers/solstein-v1-archive) — the v1 codebase, archived read-only
- [`docs/INDEX.md`](docs/INDEX.md) — navigation for everything in this repo
