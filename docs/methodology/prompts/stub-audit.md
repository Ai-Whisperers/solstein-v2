# Prompt — Stub audit

**Goal:** Find fake-data stubs that look like real external integration but return hardcoded values.
**Source chapter:** [04-stub-elimination.md](../04-stub-elimination.md)
**Typical runtime:** 1-2 hours on a large codebase.
**Prerequisites:** read access to `src/` including any `agents/`, `adapters/`, `integrations/`, `clients/` directories.

## The prompt

```
Your task: find stubs in this codebase. A "stub" is a function or class that looks like it performs external integration (fetches data, calls an API, queries a service) but actually returns hardcoded or fabricated values.

Look for these specific signals:

1. **Functions with external-integration signatures but no actual network/IO calls.**
   - Functions named `fetch_*`, `get_*`, `load_*`, `query_*`, `lookup_*`
   - Classes named `*Client`, `*Adapter`, `*Agent`, `*Service`
   - Async functions that never await anything (or only await trivial internal calls)
   - Functions returning what look like external data but with no HTTP client / DB connection / file read involved

2. **Hardcoded return values that pretend to be rich data.**
   - `return [{"id": 1, "name": "..."}, ...]` with more than 2 items in the literal
   - Dataclasses or Pydantic models constructed from literals at function end
   - Dictionaries with realistic-looking keys (revenue, growth, founded_year) but hardcoded values

3. **TODO / FIXME / placeholder comments near integration points.**
   - `# TODO: replace with real API call`
   - `# stub for testing`
   - `# hardcoded, integrate with X when available`

4. **Mock libraries being imported in production code.**
   - `from unittest.mock import ...` outside tests/
   - `MagicMock` or `Mock` instances in production

5. **Environment variable checks that short-circuit to fake data.**
   - `if os.environ.get("USE_REAL_API"): ... else: return FAKE_DATA`
   - Default behavior paths that return hardcoded data

For each finding, return:
- File path + line numbers
- What the signature claims vs. what the implementation does
- Severity: CRITICAL (in production pipeline, output used for decisions), HIGH (in production path but output not load-bearing), MEDIUM (clearly marked as stub), LOW (test-only)
- Honest interpretation: is this a forgotten stub, a documented placeholder, or a legitimate mock boundary?

Do NOT fix anything. Report only.

Return findings ranked by severity. For CRITICAL findings, estimate how long they've been in the codebase (from git blame) if you can tell without running git commands.
```

## Post-conditions

- A list of all stubs in the codebase with severity ratings and git-blame context
- Zero code changes

## Common failure modes

### False positives on legitimate mocks
Test fixtures and documented mock servers aren't stubs. The AI may flag these. Triage the report: legitimate mocks with clear intent stay; anything in production code paths gets promoted to CRITICAL.

### The AI tries to "help" by fixing
Re-prompt with explicit "report only, no changes." Stubs often have subtle history; fixing them without human review can delete important context.

### Missing stubs hidden behind polymorphism
A stub implementation of an abstract interface is easy to miss. After the AI's report lands, manually inspect any abstract classes / protocols in the integration layer.

### "Stub" that's actually a working cache
A function that returns cached values looks like a stub. Check for cache-write logic elsewhere; if writes exist, it's a cache, not a stub.

## Follow-up prompt — deletion

Stubs don't get "improved," they get deleted or replaced. After the report:

```
For the stub at `{FILE}:{LINE}`:

Option A — Real integration is available: replace the stub with a real adapter that hits `{EXTERNAL_SERVICE}`. Follow the adapter contract in `src/solstein/adapters/` (or equivalent): async, httpx-native, proper error handling, returns `None` on not-found, raises on real errors, attaches Citation to populated fields.

Option B — Real integration is not available / not needed: delete the stub entirely. Downstream code must handle the absence of this data (the caller should expect None or handle an empty return).

Do NOT improve or refactor the stub. Stubs don't get maintained; they get deleted.

After the change:
- All existing tests must pass.
- If removing the stub causes tests to fail because they depended on the fake data, rewrite those tests to verify the real behavior (or delete them if they no longer test anything meaningful).
- Callers must honestly handle missing data — no silent defaults.
```

## Evidence

- Solstein v1: had 7 stub "agents" (`financial_news_agent`, `team_intelligence_agent`, `competitive_landscape_agent`, `ai_adoption_agent`, `funding_intelligence_agent`, `market_positioning_agent`, `patent_intelligence_agent`). Each had async signatures and returned hardcoded data as "intelligence." All 7 were deleted in v2.
- These stubs were the root cause of Eneve's inflated v1 score (9.03/10 vs. honest 5.97/10).
- Not yet used in a paid engagement.
