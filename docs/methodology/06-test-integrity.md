# Chapter 6 — Test integrity

## The pattern

The test suite has hundreds of tests. They pass. They give green checkmarks. The engineering team reports "good coverage." And then production breaks in ways the tests should have caught.

This chapter is about the gap between **tests exist** and **tests prove the system works**.

We see three failure modes repeatedly:

1. **Structural tests.** Tests that assert the *shape* of the code rather than its *behavior*. `assert hasattr(company, "score")`. `assert "classify" in dir(service)`. These pass whenever the code looks right. They don't run the code. They don't catch bugs.

2. **Over-mocked tests.** Tests that mock so much that they end up testing only that the mocks are configured correctly. The real integration is never exercised. The production code path isn't the path the test exercised.

3. **Tests that can't collect.** Tests that reference modules that have moved, use fixtures that no longer exist, or depend on config that isn't set in CI. The test file exists but pytest skips it. Coverage reports count the file as "not measured" rather than "failing" — so it disappears.

Any of these failures can coexist with a "green" build and high reported coverage.

## The canonical example — Solstein v1

V1 had 327 test files nominally covering 659 source files. Coverage was reported at ~28%.

The audit revealed:

- **43 test files couldn't collect.** They imported modules that had been renamed, used fixtures that had been deleted, or required config the CI didn't set. `pytest` silently skipped them. Coverage reports treated the files as un-measurable, not failing. The "28%" figure was calculated against only the files that actually ran.

- **Structural tests dominated the suite.** A representative v1 test: `assert "AttractiveTier" in str(inspect.signature(classify_company))`. That's an assertion about a type signature string — not behavior. Whether the function correctly classified anything wasn't tested by this file.

- **Threshold regressions passed silently.** When STORY-009 centralized classification thresholds, 14 existing tests that asserted *old* threshold values began producing wrong classifications. The tests still passed (they didn't re-check the thresholds). The production pipeline used the new thresholds. The divergence lived in production for weeks before an auditor noticed.

- **Stub-agent "tests" existed and passed.** The seven stub agents each had unit tests. Every test passed. Every test was meaningless — it tested that a hardcoded dict was the hardcoded dict.

STORY-253 ("Replace Structural Source-Inspection Tests with Behavioral Contract Tests") added 29 real behavioral tests in 2026-03-31. A positive start — but 29 tests against 112,300 LOC is not a safety net.

## How to assess test integrity

### 1. Run the tests and check collection
```bash
pytest --collect-only 2>&1 | grep -i "error\|cannot"
```

Count import errors. Count skipped test files. If the number is non-zero, you don't have a test suite — you have a test file collection.

### 2. Read 10 random tests
Pick 10 tests from the suite uniformly at random. Read each. Categorize:
- **Behavioral**: feeds an input, asserts on the output's behavior.
- **Structural**: asserts on code shape, type signatures, method existence.
- **Over-mocked**: the only real code being tested is framework glue.
- **Empty / tautological**: asserts something trivially true.

A healthy suite has <10% structural and <10% over-mocked. A rotten suite has the inverse.

### 3. Check whether running the test suite actually exercises the production code paths
Instrument coverage *while running tests* but *against the CLI and API surface*, not against every file. If a production code path is never hit by any test, it isn't covered, regardless of what the line-coverage percentage says.

```bash
# Run a realistic end-to-end scenario under coverage
coverage run --source=src/solstein -m solstein run --universe <real-universe> --output out/
coverage report --skip-covered --skip-empty
```

The uncovered lines are your real risk surface.

### 4. Ask: "show me the test that would have caught X"
For any bug that shipped to production in the last 6 months, ask the team: *"show me the test that would have caught it if it existed."* Usually the answer is "we'd have to write a new test." That's your gap.

## How to fix

### Stop writing structural tests immediately
No more `assert hasattr`, no more `assert method in dir(obj)`, no more `inspect.signature` assertions. If a test file contains these patterns, flag it for rewrite.

### Start with behavioral contract tests for the public surface
For the top 10 most-used public functions (CLI entry points, API endpoints, service methods), write tests that:
- Pass realistic inputs
- Assert on realistic outputs
- Do not mock anything that isn't a true external boundary (network, filesystem, time)

### Delete tests that don't test anything
Courageous move. A test file that imports a module, asserts the import succeeded, and exits is noise. Delete it. The team will be uncomfortable. Do it anyway.

### Fix "cannot collect" errors immediately
Every test that pytest skips because of an import error is a test you're not running. Either fix the import or delete the test. Letting them accumulate is what gets you to 43 skip-failures.

### Set a floor, not a ceiling
Don't target "80% coverage." Target "the 10 most important code paths have behavioral contract tests" and measure that specifically.

## Evidence — Solstein v2

v2 has:
- 5 test files, 43 tests, all passing
- 0 collection errors
- 0 structural tests
- 0 over-mocked tests

The tests describe what the system does, not how the modules are arranged. A representative v2 test:

```python
def test_eneve_with_partial_data_scores_honestly(self, eneve: Company) -> None:
    """v1 reported Eneve at 9.03/10 on partly-synthetic data. With only 2 real
    signals (growth, financial health) and no GitHub data, the honest composite
    lands in the lead/diamond border — around 6.0. This test locks in the
    honest behavior, not v1's inflation."""
    scored = score_company(eneve)
    assert scored.composite_score is not None
    assert 5.5 <= scored.composite_score <= 7.0
    assert scored.tier in ("lead", "diamond")
```

Note what this test does *not* do:
- It does not assert on internal method names.
- It does not mock anything.
- It does not check that the code is arranged a particular way.

It just feeds real inputs through the real scorer and asserts that the real output is honest. That's the model.

## What we report to the sponsor

In the diagnostic:
- **Test collection success rate** (target: 100%)
- **Behavioral / structural / over-mocked / empty ratio** (target: >80% behavioral)
- **Bugs-in-last-6-months with no test that would have caught them** (target: 0 going forward)
- **Test runtime** (target: <2 min total)

During the transformation:
- **Weekly behavioral test count** — should grow steadily
- **Structural test count** — should decrease (they get deleted as they're replaced)
- **Coverage-of-public-surface** — percent of public API surface that has at least one behavioral contract test

## The hard conversation

The sponsor has engineers who wrote the structural tests. They were doing what they thought was right — the fashion for type-level safety over behavioral safety came from a real place. But fashion doesn't catch production bugs; behavioral contracts do.

Frame the work as "we're moving from structural safety to behavioral safety" — not as "your existing tests were worthless." They weren't worthless; they caught some real issues (mostly signature changes and import errors). They were just the wrong kind of safety for the risk you actually face.

This framing preserves the team's self-respect while enabling the actual repair.
