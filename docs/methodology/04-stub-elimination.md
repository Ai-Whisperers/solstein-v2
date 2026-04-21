# Chapter 4 — Stub elimination

## The pattern

Somewhere in the codebase, a function signature looks like it fetches real data but actually returns a hardcoded dictionary. The signature says `async def fetch_company_financials(company_id: str) -> FinancialData`. The implementation says `return FinancialData(revenue=1_000_000, growth=0.15, ...)`.

These are **stubs** — placeholder implementations that were introduced during development and never replaced with the real thing. When they're documented as stubs (with a `# TODO`, or a method name like `_mock_fetch`, or isolated in a `tests/fixtures/` module) they're harmless.

When they're **not** documented — when they're silently participating in the production pipeline and the output is being reported as real intelligence — they are the single most dangerous form of tech debt we encounter. Stakeholders make decisions based on the output, and the output is fabricated.

## The symptom

You cannot tell, from the pipeline's output, which fields came from real data and which came from stubs. The "enrichment" report shows a full row of numbers. Some of them were fetched from SEC EDGAR. Some were hardcoded in 2024 when the adapter was first being prototyped. The consumers of the report cannot tell which are which.

If you run the pipeline twice with the same company, the stub values are identical (because they're hardcoded), while real fetched values may vary slightly. Consumers mistake this stability for *determinism* and start relying on it.

## The canonical example — Solstein v1

Solstein v1 had seven stub "agents" in `src/solstein/agents/`:

- `financial_news_agent.py` — returned a hardcoded list of 3 "news items"
- `team_intelligence_agent.py` — returned fabricated team composition data
- `competitive_landscape_agent.py` — returned a static set of "competitor" names
- `ai_adoption_agent.py` — returned a randomized-but-deterministic AI maturity score
- `funding_intelligence_agent.py` — returned hardcoded funding round data
- `market_positioning_agent.py` — returned a fixed "market segment" classification
- `patent_intelligence_agent.py` — returned a static patent count

All seven had the async signature, the proper return types, and the right docstrings. They were wired into the main pipeline. Their output was scored, weighted, and included in the Attractiveness Board.

The audit called them "stub agents returning hardcoded mock data as if they were real intelligence sources."

Consequence: Eneve scored 9.03/10 with a tier of Phoenix in every v1 report. The real signals available for Eneve at the time — growth, revenue, employee count — would have produced a score of ~5.97. The extra ~3 points came entirely from the stubs. Stakeholders read "Phoenix" and concluded Eneve was exceptional. Phoenix was fabrication.

## Why it happens

Four typical paths, in decreasing order of how defensibly they begin:

1. **Honest prototyping.** An engineer stubs an adapter while the real API integration is being negotiated. The stub is functional for pipeline development. The API integration gets deprioritized. The stub stays.

2. **"The real API doesn't exist yet."** A product requirement calls for enrichment from a data source that hasn't been purchased, negotiated, or built. Engineering stubs it anyway to unblock other work. The data source never materializes.

3. **"We'll replace it before we ship."** Team ships. Stub wasn't replaced. Nobody noticed because the output *looks* real.

4. **Deliberate deception.** Rare, but we've seen it once. A team under pressure to demo built a "working" integration by hardcoding the demo company's data. The demo landed. The stub stayed. The next engagement's demo broke spectacularly.

Paths 1-3 account for >95% of stubs we find. The engineers involved are usually embarrassed when the stubs surface. Don't shame. Just fix.

## How to detect it

Three techniques, in order of investment:

### 1. Grep for telltale patterns
```bash
# Hardcoded return values in supposedly-external-calling functions
grep -rn "return \[" src/ --include="*.py" | grep -i "agent\|adapter\|fetch\|get_"

# Comments admitting the stub
grep -rn "TODO\|FIXME\|XXX\|HACK\|stub\|mock\|placeholder\|fake" src/ --include="*.py"

# Functions that should be async I/O but have no await
grep -rn "async def " src/ --include="*.py" | while read line; do
    file=$(echo $line | cut -d: -f1)
    func=$(echo $line | sed 's/.*async def //' | cut -d'(' -f1)
    grep -A 20 "async def $func" "$file" | grep -q "await" || echo "No await: $file:$func"
done
```

### 2. Trace a known input
Pick a company that *should* produce sparse data — a tiny newly-incorporated one that won't exist in most external sources. Run the pipeline on it. If the output has rich "enrichment" for every field, those fields are stubbed.

### 3. Disconnect the network
Run the pipeline with no network access. Any adapter that returns data is a stub. (This technique also finds caching bugs; do it twice, once with the cache cleared.)

## How to fix it

**Never "improve" a stub. Delete it.**

The fix is structural:

1. **Identify the stubs.** Count them. Name them. This is the scariest report you'll deliver in the diagnostic because stakeholders will ask how long the stubs have been in production.

2. **Triage: which stubs have *real* adapters possible?** For each, decide: real integration or deletion?
   - If the external source is real (SEC EDGAR, Companies House, Crunchbase) and accessible to the budget: replace with real adapter.
   - If the external source doesn't exist, isn't accessible, or the feature isn't needed: delete the adapter entirely.

3. **In the interim — before replacement is done — the adapter must no-op, not stub.** Replace the hardcoded return with `return None` or `return company_unchanged`. Downstream code must be able to handle missing data (see §Defensive downstream below).

4. **Report the data deletion loudly.** Stakeholders will notice that reports now have blank cells where they used to have numbers. That's correct. Their decision to rely on fabricated data was based on misinformation. The correction is painful and necessary. Frame the reduced output as *"removed fabricated signals; the reports now contain only verifiable intelligence."* Which is true.

5. **Prevent recurrence.** Add a convention: any adapter that returns data must also populate a `Citation` record pointing to the external source. No citation, no data. In v2 this is encoded in the type system — `Company.citations` is a required field with no default, and adapters that populate data without citations fail typecheck or behavioral tests.

## Defensive downstream

After deleting stubs, downstream code (scoring, export, UI) will be handed `None` for fields that used to have values. Downstream must handle this honestly:

- **Scoring:** returns `None` for the composite if a required signal is missing. Does not silently substitute a default. In v2: scorers return `Optional[float]`; composite requires at least 2 signals; classification only runs on non-`None` composites.
- **Export:** surfaces missing fields as "unknown" with a citation pointing to why (e.g., "Crunchbase API key not configured," "SEC search returned no match"). Never fills blanks with zeros.
- **UI / reports:** present a completeness percentage alongside the score, so the reader sees immediately that this row is based on 30% of the signals, not 100%.

## Evidence — Solstein v2

v2 has zero stubs. This is enforced by four conventions, all expressed in `docs/ARCHITECTURE.md`:

1. "**No stub agents.** Adapters hit real services or don't exist."
2. "**No silent defaults.** Scorers return `None` when inputs are missing."
3. "**Every enriched field has a citation.**"
4. "**Adapters no-op gracefully** when their API key is missing. They never fake data."

The GitHub adapter, faced with a 403 rate limit, logs a warning and returns the company unchanged — with no `github_stars_total`, no `github_commits_last_90d`, no citation for those fields. The company's completeness drops. Downstream scoring honestly reflects the missing signal. Reports show the gap.

## What we report to the sponsor

In the diagnostic:
- **Number of stubs found**, with a severity rating (was the stub in production? for how long? what decisions were made based on it?)
- **Recommended action per stub**: real integration, deletion, or (rarely) documented limitation
- **Downstream impact forecast**: which reports / decisions will change after stubs are removed

During the transformation:
- **Weekly stub count**, target: 0
- **Citation coverage** — what % of enriched fields have a Citation attached. Target: 100%.
- **Data completeness distribution** — histogram of "companies with X% of signals present." Removing stubs shifts this distribution left; that's correct.

## The sponsor conversation

Sponsors find this chapter uncomfortable. They have reports with specific numbers in them that were being used to justify decisions. The reports were wrong.

The honest conversation:

> *"Your reports contained fabricated signals. The scoring you based decisions on was partly invented by placeholder code that was supposed to be replaced. We don't know how often this affected your judgment. What we can do now is rebuild the pipeline so that every number is sourced and auditable, and reprocess historical data so you can see which past decisions were based on fabricated inputs."*

Deliver that conversation calmly. The sponsor is on your side in this moment — they were the victims of the fabrication, not its authors. The engineers who wrote the stubs usually wrote them under time pressure and were never given the time to replace them. Nobody in the room is the villain. The system allowed it.

That's why the fix is structural, not cultural.
