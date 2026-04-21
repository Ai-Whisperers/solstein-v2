# Solstein v2

Internal prospecting tool for AI-Whisperers' equity-for-transformation business.

## What this is (and isn't)

**Is:** a focused, internal tool for the AI-Whisperers deal team. Given a market universe (e.g., "European energy software"), Solstein produces a ranked shortlist of companies worth approaching for AI-native transformation engagements. Output is a deal-team brief: Excel shortlist + Markdown rationale + citation trail.

**Is not:** a SaaS product sold to PE firms. That was v1. V1 is archived.

## Business context

AI-Whisperers' actual business is **taking equity in PE portfolio companies in exchange for AI-native transformation** (modernized CICD, ticket lifecycle automation, refactoring-with-AI, quality gates). Eneve (€30M revenue Dutch energy software) is the first proof case.

Solstein's job is to find the next Eneves: companies in the right size band, in PE ownership or PE-adjacent, where an AI transformation would deliver measurable velocity/quality lift.

This product serves the deal team. It does not serve external customers. It is small, fast, and honest.

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
