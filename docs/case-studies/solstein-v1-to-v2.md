# Internal methodology validation — Solstein v1 → v2

> **What this is, and what it isn't.** This document records an internal transformation — AI-Whisperers applying our methodology to our own prospecting tool. It is **not** a client engagement. It is not evidence we have modernized an enterprise codebase with external customers, production traffic, or regulatory exposure. It is evidence that we can execute the methodology on a codebase we know. In a Phase 1 diagnostic conversation, it provides a concrete example of what "AI-native rebuild" looks like in small; it does not substitute for external references, which we do not yet have.

**Subject:** Solstein (internal AI-Whisperers prospecting tool)
**Engagement type:** AI-native rebuild. Single focused session, Claude Code + Opus 4.7.
**Date:** 2026-04-21
**Duration:** ~4 hours of focused work (one session).
**Scope:** a single-repo rebuild of a team-internal tool, with no production traffic, no external users, and no data-integrity dependencies that could harm a third party if broken.

---

## Executive summary

An internal AI-prospecting platform accumulated 18 months of unfocused development. By the end it had **659 source files, 112,300 lines of code, 73 open engineering epics, 28% test coverage, demo-grade authentication that accepted any credential, a pipeline that lost 70% of its input fields, seven stub agents returning hardcoded fake data as if it were real intelligence, three separate files defining conflicting classification thresholds, and a verification script that failed on its first assertion.** An internal audit had labelled the system *"load-bearing walls painted cardboard."*

A single AI-augmented rebuild session delivered a replacement: **18 files, 887 LOC, one canonical pipeline, one threshold registry, four real data adapters, strict mypy, zero ruff errors, 36 passing tests, working end-to-end on real data.** The rebuild is the v2 in this repository. The before state is preserved at `github.com/Ai-Whisperers/solstein-v1-archive`.

This document captures the delta and the methodology. It is a *demonstration*, not a reference. Readers evaluating our firm for enterprise engagements should weight this accordingly.

---

## Before / After (verified metrics)

| Metric | v1 (master @ 340b8d7d) | v2 (main @ 7fd92fe) | Delta |
|---|---|---|---|
| Source files | 659 | 18 | **−97.3 %** |
| Source LOC | 112,300 | 887 | **−99.2 %** |
| Test files | 327 | 5 | −98 % |
| Tests passing | 1,434 collected, 14+ failing, 43 files couldn't even collect | 36 / 36 | Clean |
| Largest file | 1,168 lines (`domain/models.py`) | 134 lines (`export/writers.py`) | −88 % |
| Files > 500 LOC ("god files") | 14 | 0 | −100 % |
| Ruff errors | 207 at audit time → 0 after STORY-272 (21 days) | 0 from day 1 | Equal-clean |
| Mypy strict | Not enforced | Clean | New |
| Open engineering epics | 73 | 0 | −100 % |
| CI workflows | 5 workflows + 3 composites | 1 workflow | −83 % |
| Docs directories | 20 | 3 | −85 % |
| Authentication | Demo shim — accepts any credential | None (internal tool, auth deferred) | Scoped out |
| Pipeline field loss | ~70 % | 0 % by design — missing data surfaces as `None` with citation | −100 % |
| Stub agents returning fake data | 7 | 0 | −100 % |
| Conflicting threshold files | 3 | 1 | −67 % |
| Data integrity | `Phoenix` classifications on partly-synthetic data (Eneve scored 9.03/10) | Honest: Eneve scores 5.97/10 on only the signals we actually have | Honesty restored |
| CI runtime | 10-15 min | < 2 min (estimated from workflow shape) | ~6× |
| Git history preserved | — | v1 archived, all 1,230 commits retained | Lossless |

---

## What was kept

- Git history (v1 archived on GitHub, all 1,230 commits retained in `solstein-v1-archive`)
- Dependency selections (httpx, pydantic 2, loguru, tenacity, openpyxl)
- CI-composite actions concept (rewritten as a single uv-native workflow)
- `.gitattributes`, `.gitignore`, `.dockerignore`, `LICENSE`, `dependabot.yml`

## What was eliminated

- All 659 v1 source files
- 73 engineering epics' worth of accumulated half-finished work
- Demo JWT, multi-tenancy scaffolding, dual CLIs, three conflicting threshold files
- Seven stub agents fabricating "data"
- Four "source of truth" documents that disagreed with each other
- Celery, Redis, FastAPI surface, Alembic migrations (none needed for an internal prospecting tool)
- The illusion that "almost-working" is a valid state

---

## Method — the 12 decisions that produced the delta

1. **Defined the real job, then scoped to it.** Solstein is an internal prospecting tool, not a SaaS product sold to PE firms. Every feature that didn't serve "find transformation targets" got cut. (Result: multi-tenancy, auth, API surface, dashboards, 73 epics of accumulated scope — gone.)

2. **One pipeline, one threshold registry, one CLI.** v1 had parallel legacy-and-canonical pipelines, three files with classification thresholds that produced different tier assignments for the same score, and two CLIs. All duplicated load-bearing state was collapsed. If there's one of something, there can only be one place it lives.

3. **No silent defaults.** v1's scorers silently treated missing fields as zero, producing Phoenix classifications on empty data. v2's scorers return `None` when required inputs are missing; `None` composites never get classified. The same Eneve inputs that produced a v1 score of 9.03 produce a v2 score of 5.97. The 5.97 is the honest number.

4. **Every enriched field carries a citation by construction.** v1 could tell you a company's revenue; it couldn't tell you where the number came from. In v2, every adapter populates the field *and* a `Citation` in the same operation. Missing the citation is a type error.

5. **No stub adapters.** Each adapter either hits a real external service or doesn't exist. The seven v1 agents returning hardcoded fake data were all deleted. v2 has four real adapters (GitHub, Companies House, SEC EDGAR, yfinance). Each no-ops gracefully when its API key is missing — never fabricates.

6. **Small files are a contract, not an aspiration.** v2 has a published file budget in `docs/ARCHITECTURE.md`. Target: <15 source files. Hard re-think at 20. Largest file in v2 is 134 lines. v1's largest was 1,168.

7. **Retry only transient errors.** v1 retried every HTTP error three times, burning three attempts on permanent 4xx failures. v2 extracts a shared `http_retry` decorator that retries only timeouts, network errors, and 5xx.

8. **Tests assert behavior, not structure.** v1's tests had been partly replaced (STORY-253) with behavioral contracts but the old structural tests remained. v2's 36 tests describe what the system *does*, not how it's arranged. Refactoring doesn't break them.

9. **Archive, don't migrate.** v1 was not "gradually replaced in place." It was frozen on `master`, the repo was renamed, GitHub-archived, and v2 is a clean new repo. This prevented the usual "keep backward compatibility with the broken thing" trap that produced most of v1's cruft in the first place.

10. **Ship with honest output.** v2's first real run on a 15-company European energy universe scored *only* Eneve (the one row with manually-entered data). The other 14 came back `unknown` with 0% completeness. v1 would have generated scores for all 15 — mostly by inventing data. v2's "unknown" is the correct answer.

11. **CI is not a museum.** v1 had five workflows and three composite actions, much of it orphaned. v2 has one workflow: lint → typecheck → test. If a step can't earn its existence by catching real bugs, it doesn't exist.

12. **Write the README last, against what actually exists.** v1's README described a McKinsey-replacement SaaS. The product that existed was an internal pipeline. v2's README was written after the code, describing what's there.

---

## Observations for future engagements

- **Scope reduction is where 90% of the compression happens.** The v1→v2 LOC delta (−99.2%) came mostly from deleting features we didn't need, not from compressing features we kept.
- **AI-native rebuilds are dramatically faster when constraints are imposed up front.** "15 files, no more" is a more productive instruction than "keep it clean." Concrete numerical constraints force architectural discipline.
- **"Archive and restart" beats "refactor in place"** when the audit backlog exceeds the feature list. v1's 73 open epics would have taken an estimated 33 weeks to close. The rebuild took hours.
- **The single most important refactoring move is collapsing load-bearing duplication.** Three threshold files, two CLIs, duplicate adapter pairs — every such duplication is a correctness bug waiting to be discovered.

---

## Appendix — artifacts

- v1 archive: [github.com/Ai-Whisperers/solstein-v1-archive](https://github.com/Ai-Whisperers/solstein-v1-archive) (master @ 340b8d7d, read-only)
- v2 repository: [github.com/Ai-Whisperers/solstein-v2](https://github.com/Ai-Whisperers/solstein-v2) (main)
- v1 audit report (2026-03-31): `docs/archive/AUDIT-REPORT.md` in v1 archive
- Rebuild commits: `c76c21b` (initial scaffold) → `3c53ca4` (Companies House) → `7fd92fe` (SEC EDGAR + yfinance + sample universe)
