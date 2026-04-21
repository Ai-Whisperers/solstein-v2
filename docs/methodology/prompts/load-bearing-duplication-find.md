# Prompt — Find load-bearing duplication

**Goal:** Identify places where the same business rule, threshold, or constant appears in multiple files, potentially producing inconsistent behavior.
**Source chapter:** [03-load-bearing-duplication.md](../03-load-bearing-duplication.md)
**Typical runtime:** 30-60 minutes for a mid-size codebase.
**Prerequisites:** read access to the full codebase (`src/` and `tests/`).

## The prompt

```
Your task: find load-bearing duplication in this codebase. "Load-bearing" means the same business rule or constant is defined in multiple places, and if the definitions disagree, system behavior depends on which code path runs first.

Look for these specific patterns:

1. **Numeric thresholds defined more than once.** Grep for any floats or ints that look like business rules (tier cutoffs, retry counts, timeouts, validation limits). Flag any that appear in more than one non-test file.

2. **Magic strings defined more than once.** Tier names, state codes, category labels, enum values. Flag any string that appears in more than 3 non-test places and isn't trivially one-off (like an error message).

3. **Duplicate function names across modules.** If two modules both have `classify_tier()` or `validate_company()` or `parse_date()`, they may be doing the same work differently. Flag and investigate.

4. **Hardcoded values that look like config.** Magic values that should arguably be in settings/constants but are inlined. Flag where they appear.

5. **Copy-pasted logic blocks.** Sequences of 10+ lines that appear >1 time with minor variation. Flag and report where.

For each finding, return:
- What is duplicated
- Where it is (file paths + line numbers)
- Whether the definitions agree or disagree
- Severity: CRITICAL (behavior diverges), HIGH (will diverge soon), MEDIUM (aesthetic duplication), LOW (trivial)

Do NOT fix anything yet. Just report.

Return findings ranked by severity.
```

## Post-conditions

- A report listing all detected duplication with severity ratings
- Zero code changes

## Common failure modes

### False positives on legitimate redundancy
Some duplication is intentional — e.g., constants redefined in a test module for test independence. Judge each finding; don't treat the AI's report as authoritative.

### Misses duplication across different representations
A threshold defined as `8.0` in one file and `8.00` in another. The AI's grep-based detection may miss these. Always follow up with manual review on the most-critical constants.

### AI tries to fix immediately
Some AI tools default to "find and fix." Be explicit that this prompt is investigation-only. Fixes are a separate prompt after human review.

## Follow-up prompt — fixing

After the report lands and you've chosen which duplications to consolidate:

```
For the duplication `{DUPLICATION_NAME}` at locations:
- {FILE_A}:{LINE_A}
- {FILE_B}:{LINE_B}
- {FILE_C}:{LINE_C}

Consolidate to a single canonical location at `{TARGET_FILE}`. Replace the other occurrences with imports from the canonical location. Do not leave backward-compat shims. Delete the shims entirely after confirming nothing outside this refactor relies on the old import paths.

Add a CI check that fails if this constant / function / value is redefined outside the canonical location.

All existing tests must still pass.
```

## Evidence

- Solstein v1: three-file classification threshold bug was the textbook case. Detected by grep for `"phoenix"` and for `8.0` across the codebase. Consolidated in v2 to `src/solstein/scoring/thresholds.py` — single source of truth.
- Not yet used in a paid engagement.
