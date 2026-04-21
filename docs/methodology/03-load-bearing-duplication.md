# Chapter 3 — Load-bearing duplication

## The pattern

A single piece of logic or configuration appears in multiple places in the codebase. When they disagree, the system's behavior depends on *which code path runs first* — and nobody in the team can tell you which that is without reading the source.

This is different from ordinary duplication. Ordinary duplication is *aesthetic* — the code looks similar in two places, violating DRY. Load-bearing duplication is *correctness* — the two (or three, or four) locations define *what the system does*, and they don't agree.

The symptom: the same input produces different outputs depending on the entry point. "It works when run through the pipeline but not through the CLI." "It passes the unit tests but fails in production." "It classified them as Phoenix in the report but as Lead in the dashboard."

## The canonical example — Solstein v1

Solstein v1 had three files defining classification thresholds for the same scoring system:

- `src/solstein/analytics/constants.py` said `PHOENIX_MIN = 8.0`
- `src/solstein/research/classification.py` hardcoded `if score >= 8.5: return "phoenix"` inline
- `src/solstein/domain/tier_registry.py` had its own `TIER_THRESHOLDS = {...}` dictionary

Three files. Three answers to the question: *"at what score is a company a Phoenix?"* A company scoring 8.2 was Phoenix via the first file, Lead via the second, and Phoenix again via the third.

Which answer Solstein actually used depended on *which function the caller happened to import*. The domain model imported from `tier_registry.py`. The report generator imported from `analytics/constants.py`. The classification service imported its own hardcoded values.

The result: audits that traced the bug had to reason about import order and execution flow, not "what does the code say."

STORY-009 was meant to fix this ("Thresholds centralized in `analytics/constants.py`"). It marked itself Done. It didn't actually remove the other two locations.

## Why it happens

Load-bearing duplication is almost never written on purpose. It accumulates through three typical paths:

1. **The "keep backward compatibility" refactor.** An engineer introduces a new canonical location but leaves the old one importing from the new, "just in case." The "just in case" never gets removed, and two releases later someone edits the old one directly.

2. **The "cross-team ownership" split.** Team A owns analytics, Team B owns the classification service, Team C owns the domain model. Each team adds the threshold to their own territory because "we shouldn't depend on their stuff." Three sources of truth, organizational by origin.

3. **The "I couldn't find it" duplicate.** An engineer needs thresholds for a feature. They search, don't find them (or find them in a place that didn't look authoritative), and add new ones. Nobody notices the duplicate until a bug crosses boundaries.

All three paths are repairable — but only if you find them. This chapter is about finding them.

## How to detect it in a codebase

Three techniques, used in order of cost:

### 1. Constant-value archaeology (cheap, fast)
Pick numbers or strings that look like business rules — thresholds, tier names, state codes, maximum retries, timeout values. Grep for literal occurrences across the codebase. If a magic number like `8.0` or a string like `"phoenix"` appears in more than one non-test file, investigate.

```bash
# Example: find load-bearing thresholds in Solstein
grep -rn "8\.0" --include="*.py" src/ | grep -v __pycache__
grep -rn '"phoenix"' --include="*.py" src/ | grep -v __pycache__
```

In Solstein v1, this immediately surfaced the three-file threshold issue.

### 2. Function-name duplication (cheap, fast)
Find identically-named functions across the tree. A `classify_tier()` in one module and a `classify()` in another is suspicious. A `validate_company()` in three different modules is a guarantee of duplication.

```bash
find src -name "*.py" -exec grep -l "def classify" {} \;
```

### 3. Behavioral trace (slower, thorough)
For a specific test input, trace every code path it touches end-to-end. List every location where decisions are made. In legacy codebases this is the only way to find subtle duplication hidden behind polymorphism, dynamic dispatch, or metaprogramming.

Use a debugger with breakpoints on all classification-related functions, or add print statements around suspect areas, run the same input through every entry point (CLI, API, pipeline, report), and check that they agree.

## How to fix it

The pattern is always the same:

1. **Find all locations.** Stop after finding two; there's almost always at least one more. Three is typical. Don't start refactoring until the full list is known.

2. **Pick the canonical one.** Criteria, in order: *(a)* most visible (lives near the domain model); *(b)* most tested; *(c)* most likely to be edited by a future maintainer who wants to change the business rule. A threshold constant belongs near the domain, not deep in an analytics module.

3. **Replace all other locations with imports from the canonical one.** Not copy-paste; real imports. Break the inline hardcoding. Break the duplicate constant.

4. **Delete the shims.** After the next deployment, remove any "for backward compatibility" re-exports. Do this in the *same sprint* as the consolidation. A shim left in for two sprints is a shim left in forever.

5. **Add a CI check.** For thresholds specifically: a grep-based check that fails the build if the threshold constants appear outside the canonical file.

```bash
# Example CI check: fail if PHOENIX_MIN is defined anywhere except thresholds.py
if grep -rn "PHOENIX_MIN\s*=" src/ --include="*.py" | grep -v "scoring/thresholds.py"; then
    echo "FAIL: PHOENIX_MIN defined outside canonical location"
    exit 1
fi
```

## Evidence — Solstein v2

In v2 there is exactly one threshold file: `src/solstein/scoring/thresholds.py`. 19 lines:

```python
PHOENIX_MIN: Final[float] = 8.0
DIAMOND_MIN: Final[float] = 6.0
LEAD_MIN: Final[float] = 4.0

def classify(composite_score: float) -> Tier:
    if composite_score >= PHOENIX_MIN: return "phoenix"
    if composite_score >= DIAMOND_MIN: return "diamond"
    if composite_score >= LEAD_MIN:    return "lead"
    return "salt"
```

The module's docstring is worth copying:

> *v1's fatal bug: three files disagreed on where 'phoenix' starts. Same company landed in different tiers depending on which code path ran. Never again. If you change a number here, change only here.*

That docstring is the point of this chapter in one paragraph.

## What we report to the sponsor

- **Count of load-bearing duplications found, by type** (constant, function, logic block)
- **Risk assessment per duplication** — how many code paths depend on it, which
- **Consolidation plan** with per-duplication estimated effort
- **Progress** — weekly count of remaining duplications (target: 0)

This is usually one of the highest-impact findings in the diagnostic. Sponsors don't know it's there until the audit surfaces it, and the "same input, different output" bug stories land hard.
