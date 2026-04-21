# Chapter 5 — CICD rebuild

## The pattern

The CI pipeline started sensibly — a single workflow that ran tests. Over time, teams added workflows for "code quality," "security scanning," "dependency checks," "documentation builds," "deploy staging," "deploy prod," "weekly audit," "nightly soak test." The workflows accumulated. They were never consolidated. Some became flaky and were quietly `continue-on-error: true`'d into meaninglessness. Some duplicated checks that already ran in other workflows. Some referenced scripts that no longer existed.

The engineering team stops trusting CI. A red build no longer means "something's broken" — it might just mean "the weekly audit workflow is failing again, ignore it." A green build no longer means "safe to merge" — it might just mean "the checks that would have failed got disabled six months ago."

When CI stops being a signal, changes land without validation, and the quality problems the CI was supposed to catch reappear in production.

## When to rebuild vs. fix

**Fix in place** when:
- Under 10 workflows, mostly green, and the team can explain what each one does.
- Signal trust is intact — people unblock themselves on red.
- The failing steps are tractable (flaky tests, outdated actions).

**Rebuild** when:
- More than ~8 workflows and the team can't list them from memory.
- Any workflow has `continue-on-error: true` on a check that's supposed to be load-bearing.
- "Known flakes" exist — builds expected to fail sometimes.
- Workflows reference deleted scripts, deprecated actions, or dead composite actions.
- The team treats CI failures as noise by default.

Solstein v1 hit every red flag. Rebuild.

## The rebuild sequence

### 1. Inventory what exists
List every workflow file. For each, answer:
- What does it gate? (merge, deploy, notification only?)
- What does it actually run?
- When did it last pass for a non-trivial reason?
- Who owns it?

Most of the workflows won't have owners. Most of the "what does it gate" answers will be vague. That's the diagnosis.

### 2. List what CI should gate
Independent of what exists, list what CI *should* protect:
- Merges to main: code must lint, typecheck, and all tests must pass
- Release: additional gates for versioning, changelog
- Dependency updates: security scan, minimal test matrix
- Scheduled / proactive: stale-branch cleanup, dependency freshness

This is usually 3-5 items. Not 20.

### 3. Map wanted → existing
For each wanted gate, which existing workflow delivers it? Usually some are delivered 3× (over-covered), some are missing entirely, and some workflows deliver nothing wanted.

### 4. Delete everything that isn't needed
The courage step. Start a new branch. Delete every workflow that doesn't map to a wanted gate. Delete the composite actions they reference. Delete the scripts they invoke.

The team will be nervous. That's the emotional signal that *you were right to rebuild* — they had no idea which workflows mattered, which means most of them didn't.

### 5. Build the 1-3 workflows you actually need
From scratch. No copy-paste from the deleted ones. Each new workflow:
- Has a single clear purpose in its name
- Runs in under 5 minutes in the common case
- Exits fast on the first failure
- Can be run locally with the same command (dev parity)

### 6. Merge and watch
Merge the rebuild. Watch the first week. Two kinds of failures will appear:
- **Real failures that CI was hiding.** Fix these; they're the point.
- **False failures from the new workflows' strictness.** Tune the workflow, but err on the side of strict. The team's comfort with failed builds is how you got into this mess.

## Evidence — Solstein v1 → v2

### Before (v1)
Five workflows in `.github/workflows/`:
- `ci.yml` — lint, typecheck, test
- `code-quality.yml` — radon, complexity reports, architectural checks
- `deploy.yml` — deploy staging / prod
- `docs.yml` — mkdocs build
- `weekly.yml` — scheduled audit, unclear purpose

Plus three "composite" actions:
- `setup-python`
- `setup-uv`
- `install-deps`

CI config commits: frequent. Many had messages like *"fix flaky test,"* *"skip docs check,"* *"disable complexity gate temporarily."* Several workflows had `continue-on-error: true` on checks that should have been load-bearing.

Commit `9236848e` explicitly noted: *"ci: rebuild CI/CD from scratch — 20 workflows → 5."* So v1 had already been rebuilt once, from 20 to 5, *before* the v1→v2 rebuild. Even at 5 it was too many.

### After (v2)
One workflow: `ci.yml`. Three jobs:
- `lint` — ruff check + ruff format check
- `typecheck` — mypy strict
- `test` — pytest

Total lines in `.github/workflows/`: 62 (single file). v1 had ~300 lines across 5 files plus the composites.

Runtime: under 2 minutes for a typical PR.
Success rate: 100% since commit `c76c21b` (the v2 initial scaffold).
Load-bearing: yes — no `continue-on-error` anywhere.

## The sponsor conversation

> *"How many CI workflows does your team have, and what does each gate?"*

If the answer is a confident list of 2-5, the CI is probably fine. If the answer involves counting or "let me check," we're rebuilding. The fact of the question surfacing the lack of clarity is itself the diagnosis.

> *"When a CI build fails on main, what do engineers assume?"*

If the answer is "something real broke," CI has signal. If the answer is "probably just the flaky audit workflow," CI has lost signal — and every production incident after this will be partly attributable to that loss.

## What we report to the sponsor

- **CI workflow count** (target: ≤3 for a typical application)
- **Typical PR runtime** (target: under 5 minutes)
- **Percentage of failures fixed vs. retried** (target: >80% fixed)
- **Number of `continue-on-error` occurrences on load-bearing checks** (target: 0)
- **CI config commits per week** (a high and sustained number is a symptom of distrust)

## Anti-patterns to avoid

- **Adding a new workflow instead of fixing an existing one.** Every time someone adds a workflow "because the existing one is too hard to change," the rebuild is inevitable.
- **Using `continue-on-error` as a permanent state.** It's a debugging tool, not a deployment strategy.
- **Gating merge on workflows that take >10 minutes.** People will merge around them.
- **Running the same check in three different workflows.** Triple-covered checks don't make them three times as safe; they make them slower and dilute ownership.
