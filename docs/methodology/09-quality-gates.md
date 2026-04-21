# Chapter 9 — Quality gate hierarchy

## The pattern

A well-governed codebase runs automated checks in a layered hierarchy. Each layer is faster than the next but catches a different class of problem. When everything runs at every commit, CI runs in 30 seconds. When any layer is missing or slow, quality issues leak past.

## The four layers

| Layer | Runs on | Speed | Catches |
|---|---|---|---|
| 1. Format | Pre-commit + CI | <1s | Inconsistent style, whitespace, quote marks |
| 2. Lint | Pre-commit + CI | <5s | Unused imports, dead code, common bugs, magic numbers |
| 3. Typecheck | CI | <30s | Type mismatches, `None` flow bugs, contract violations |
| 4. Tests | CI | <2min | Behavioral regressions |

Each layer has prerequisites: typecheck only runs if lint passes; tests only run if typecheck passes. This fail-fast ordering saves CI minutes and, more importantly, puts useful feedback in front of engineers quickly.

## The recommended stack (Python 2026)

- **Format:** `ruff format` (replaces black)
- **Lint:** `ruff check` with a strict ruleset (replaces flake8/isort/pylint/etc.)
- **Typecheck:** `mypy --strict` (or pyright strict)
- **Tests:** `pytest` with `pytest-asyncio` + `pytest-httpx` for mocked network

Ruff's consolidation of format + lint + isort has significantly changed the economics of quality gates in Python — there's no longer a defensible reason to run 4 tools where 1 suffices. Systems still running black + isort + flake8 + pylint are running old architecture.

## The critical rule: gates must be honest

**A gate that's `continue-on-error: true` is not a gate. It's a suggestion.** Every gate must either pass or fail the build. If a gate is so flaky that it must be advisory, it's not ready to run in CI — fix it or remove it.

v1 had `continue-on-error: true` on its complexity gate, its architecture gate, and its type check. The type check reported "2,000 errors" for 18 months. Nobody looked because it was advisory. The "check" was theatre.

v2 has zero advisory gates. Every one passes or fails.

## Setting strictness

### Ruff
Start with `select = ["E", "W", "F", "I", "B", "UP", "SIM", "RUF", "N", "C4", "ERA"]`. Add more as the team's appetite increases. Do *not* turn off rules in the ruleset without a documented reason — a comment above the config line saying *"we turn off X because Y."*

### Mypy
Start strict (`strict = true`) on new code. On legacy code, use `--check-untyped-defs` as the floor and raise to strict over time. Do not use `# type: ignore` without a reason comment.

### Coverage
Measure, but don't set it as a blocking gate until it's stable. The behavior of "must hit 80% coverage" triggers meaningless tests. Instead: gate on the behavioral contract tests we discussed in Chapter 6.

## Configuration (Solstein v2 example)

```toml
# pyproject.toml

[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E", "W",    # pycodestyle
    "F",         # pyflakes
    "I",         # isort
    "B",         # flake8-bugbear
    "UP",        # pyupgrade
    "SIM",       # flake8-simplify
    "RUF",       # ruff-specific
    "N",         # pep8-naming
    "C4",        # comprehensions
    "ERA",       # no commented-out code
]
ignore = ["E501"]  # line length enforced by formatter

[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
disallow_any_generics = true
plugins = ["pydantic.mypy"]
```

And the CI:

```yaml
jobs:
  lint:
    steps:
      - run: ruff check src/ tests/
      - run: ruff format --check src/ tests/

  typecheck:
    needs: [lint]
    steps:
      - run: mypy src/solstein

  test:
    needs: [lint]  # not typecheck — tests can sometimes surface real bugs even if types don't align
    steps:
      - run: pytest -q --cov=solstein
```

## Evidence — Solstein v1 → v2

| Metric | v1 baseline | v2 |
|---|---|---|
| Ruff errors | 207 (reduced to 0 over 21 days in STORY-272) | 0 from day 1 |
| `continue-on-error` usages | 3 (complexity, architecture, typecheck) | 0 |
| mypy strict | Not enabled | Enforced |
| CI runtime | 10-15 minutes | <2 minutes |
| Gates advisory vs. load-bearing | 3 advisory / 2 load-bearing | 0 / 3 |

## What we report to the sponsor

- **Ruff error count over time** — should trend to 0
- **mypy error count over time** — should trend to 0 (or documented exceptions)
- **CI runtime p50, p95** — should stay under 5 minutes
- **Advisory gate count** — target: 0

## Anti-patterns to avoid

- **Gates that advise but don't block.** Either block or don't exist.
- **Gates that take longer than the tests they're supposed to precede.** Fail-fast ordering is wrong if lint takes 2 minutes and tests take 30 seconds.
- **One-time "lint cleanup" sprints without CI enforcement.** The errors come back in two weeks.
- **Ignoring type errors with `# type: ignore` without a reason.** Every ignore is a pointer to something future-you will need to understand.

## The sponsor conversation

> *"Show me your CI. Which of these checks can fail without blocking a merge?"*

If the answer is any of them, we have a quality gate integrity problem. The gate hierarchy only works if every gate is honest.
