# AI-native transformation methodology

The playbook AI-Whisperers uses to modernize legacy software systems. Each chapter is one reusable pattern, with the evidence (usually from the Solstein v1→v2 rebuild) that it works.

This is an internal document. It is the thing we sell in a Phase 1 diagnostic and execute in a Phase 2 pilot. Do not share externally without redaction.

## Structure

| # | Chapter | What it covers | Source of evidence |
|---|---|---|---|
| 1 | [Diagnostic framework](01-diagnostic.md) | How we assess a codebase in 10 working days | AUDIT-REPORT.md, v1 |
| 2 | [God-file decomposition](02-god-files.md) | 1,168-line files → 134-line ceiling | Solstein v1→v2 |
| 3 | [Load-bearing duplication](03-load-bearing-duplication.md) | Three-file threshold bug pattern | Solstein v1 scoring |
| 4 | [Stub elimination](04-stub-elimination.md) | Finding fake data pretending to be real | Solstein v1 agents |
| 5 | [CICD rebuild](05-cicd-rebuild.md) | 20-workflow sprawl → 5 → 1 | Solstein v1 + v2 |
| 6 | [Test integrity](06-test-integrity.md) | Behavioral contracts vs. structural inspection | Solstein v1 STORY-253 |
| 7 | [AI-augmented refactoring](07-ai-refactoring.md) | Using Claude Code + Opus disciplined | Solstein v2 session |
| 8 | Ticket lifecycle automation | (gap — execute on first portco) | — |
| 9 | [Quality gate hierarchy](09-quality-gates.md) | ruff → mypy → tests → complexity | Solstein v2 |
| 10 | [Archive vs. refactor](10-archive-vs-refactor.md) | When to burn it down instead | Solstein v1 decision |

## Status

| Chapter | State |
|---|---|
| 1, 2, 10 | Draft, ready for review |
| 3, 4, 5, 6, 7, 9 | Outlined, not written |
| 8 | Not yet executed — no evidence to write from |

## Ownership

**Autonomous agent (this Claude) is responsible** for keeping this playbook current. Every time we execute a new transformation move in a real engagement, the relevant chapter is updated with new evidence.
