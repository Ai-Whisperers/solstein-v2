# Prompt — Convert structural tests to behavioral contract tests

**Goal:** Replace tests that assert on code shape (`assert hasattr`, `assert method in dir`, `inspect.signature`) with tests that assert on behavior (feed input, check output).
**Source chapter:** [06-test-integrity.md](../06-test-integrity.md)
**Typical runtime:** 1-2 hours per module of tests.
**Prerequisites:** Familiarity with the module being tested — the AI can convert tests, but you need to judge whether the behavioral assertions match the intended behavior.

## The prompt

```
The test file `{TEST_FILE}` currently contains structural tests that assert on code shape rather than behavior. These tests pass when the code looks right, but don't catch real bugs. I want to convert them to behavioral contract tests.

Constraints:
1. Do not delete any test that is actually behavioral. Keep those as-is.
2. For each structural test, write a replacement that:
   - Feeds realistic inputs through the real code path
   - Asserts on the real output
   - Does not mock anything that isn't a true external boundary (network, filesystem, time)
3. Tests should have descriptive names that say what they verify, not what they call.
4. If a structural test doesn't have an obvious behavioral replacement (because the structural thing it tested isn't load-bearing), delete it entirely and note it in your summary.

Before writing any new tests, list:
- Every existing test in the file, classified as: BEHAVIORAL (keep), STRUCTURAL (replace), EMPTY/TAUTOLOGICAL (delete).
- For each STRUCTURAL test, your proposed behavioral replacement in one sentence.

I'll approve the plan, then you execute.

After execution: run the new tests. All must pass. Commit.
```

## Post-conditions

- Test file contains only behavioral or legitimately-retained tests
- All new tests pass
- Coverage measured against public API surface has not decreased
- A short summary documents which tests were converted, which were deleted, and why

## Common failure modes

### "Behavioral" tests that still don't test behavior
The AI may produce a "behavioral" test that calls a function and asserts its return is truthy. That's not behavioral. Override: assert on specific expected outputs, not just existence of output.

### Over-mocking in the conversion
The AI sometimes converts a structural test to a behavioral test by mocking every dependency. The result still doesn't test the integration. Re-prompt: "do not mock anything that isn't a true external boundary."

### Loss of coverage on edge cases
Structural tests sometimes indirectly covered edge cases (e.g., a test that asserted a function exists in both sync and async forms ensured both existed). Behavioral replacements must explicitly cover both. Review the plan before execution.

## Evidence

- Solstein v1 STORY-253 ("Replace Structural Source-Inspection Tests with Behavioral Contract Tests") added 29 behavioral tests as a start. The v2 rebuild made this the only kind of test: all 43 v2 tests are behavioral.
- Example v2 behavioral test (from `tests/unit/test_scoring.py`):
  ```python
  def test_eneve_with_partial_data_scores_honestly(self, eneve):
      scored = score_company(eneve)
      assert scored.composite_score is not None
      assert 5.5 <= scored.composite_score <= 7.0
      assert scored.tier in ("lead", "diamond")
  ```
  Feeds a real input through the real scorer. Asserts on range + tier. No mocks. Tests behavior.
