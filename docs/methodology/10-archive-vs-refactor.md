# Chapter 10 — Archive vs. refactor

## The decision

When we take on an engagement, the first major architectural call is: **do we refactor this system in place, or archive it and rebuild?**

Most consultancies default to refactor-in-place because it looks less aggressive, requires less trust from the sponsor, and doesn't ask them to throw away "work already paid for." These are political reasons, not technical ones. Sometimes refactor is correct; often it isn't. This chapter gives the framework to decide honestly.

## The framework

We evaluate six dimensions. Score each 1 (low) to 5 (high). Sum the result.

| Dimension | What high scores look like |
|---|---|
| **Audit backlog size** | Known issues / tech-debt items exceed the feature list |
| **Load-bearing duplication** | Multiple "sources of truth" that disagree (see Ch. 3) |
| **Stub density** | Fake data / placeholder code pretending to be real (see Ch. 4) |
| **Test integrity debt** | Tests pass but don't validate behavior, OR tests can't collect |
| **Architectural confusion** | Multiple architectures coexist (e.g., legacy + "canonical") |
| **Team consensus** | The team itself calls it cardboard / unshippable / broken |

**Scoring guide:**
- **6-12:** Refactor in place. System has real bones.
- **13-20:** Aggressive refactor, likely involving module-level rewrites. Retain architecture but replace implementation.
- **21-30:** **Archive and rebuild.** The cost of carrying legacy through the transformation exceeds the cost of rebuilding clean.

## Case in point — Solstein v1

| Dimension | v1 score | Evidence |
|---|---|---|
| Audit backlog size | 5 | 73 open engineering epics, 265 stories |
| Load-bearing duplication | 5 | Three threshold files producing different tiers for same score |
| Stub density | 5 | Seven agents returning hardcoded fake data as "intelligence" |
| Test integrity debt | 4 | 43 test files couldn't collect; structural-inspection tests |
| Architectural confusion | 5 | "Legacy" + "canonical" pipelines running in parallel, neither clearly chosen |
| Team consensus | 5 | Audit explicitly called it *"load-bearing walls painted cardboard"* |
| **Total** | **29** | |

**Decision: archive and rebuild.**

Time saved: 33 weeks of remediation (per the v1 audit's own estimate) replaced by ~4 hours of rebuild. Work preserved: git history (archived at `solstein-v1-archive`), adapter dependency selections, CI shape, license.

## When refactor-in-place is correct

Don't over-use this framework. Most systems score 10-15 and should be refactored. Archive-and-rebuild is appropriate only when the cost of carrying legacy through the transformation exceeds the cost of rebuilding. Red flags that make refactor the right call even with high scores:

- **External consumers depend on the existing API surface.** Can't break them.
- **Data migrations are required, not just code migrations.** Rebuilding the code doesn't help if the database schema is the problem.
- **The team needs to understand the system they'll maintain.** Archive-and-rebuild done by us leaves the team without the archaeological knowledge a refactor builds.
- **Regulatory / audit requirements.** Some systems can't simply be thrown out; the provenance chain matters.

## Common sponsor objections and honest answers

> *"We paid for all that work. We can't throw it away."*

You're not throwing away the work. You're preserving it in an archive. You're throwing away the *maintenance burden* of code that doesn't serve your current goals. The work you paid for taught the team what doesn't work — that's the value you keep. The code itself was going to be rewritten eventually; we're just admitting it now.

> *"What if we find we needed something from v1?"*

The archive is read-only, not deleted. In practice, 90% of v1 features get identified as out-of-scope for v2 (that's how you get a 99% LOC reduction). The remaining 10% gets re-implemented cleanly, informed by v1's attempt. We've never seen a retrieval from archive go badly — but if it would, refactor was the correct call.

> *"Our team will be demoralized."*

Valid concern, worth addressing directly. Some engineers will be. More will be energized by a clean rebuild. Frame the decision as "we're applying what v1 taught us, at the scale of first principles" — because that's what it is. The team's v1 work informed every decision in v2, even the decision to start over.

## Instrumentation to report

If archive-and-rebuild is chosen:
- Daily LOC delta: v1 decommissioned vs. v2 shipped
- Parity checklist: which v1 features have v2 equivalents, status
- Archive access log: any reads of v1 code during the rebuild (should trend to zero)

If refactor-in-place is chosen:
- See Ch. 2 (god files) for decomposition metrics
- Cyclomatic complexity over time
- Audit backlog burndown
