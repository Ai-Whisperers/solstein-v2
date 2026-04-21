# Chapter 2 — God-file decomposition

## The pattern

Legacy codebases grow by accretion. A file starts as a sensible 80-line module, then a feature gets added to it, then another, then a refactor that was "too risky to split" left it at 400 lines, then three more features, and now it's 1,168 lines with 12 responsibilities and the one person who understood it left nine months ago.

We call these **god files**. They are the single biggest contributor to the perceived cost of change in a legacy system. Touching them is scary, so teams stop touching them, so they accumulate more responsibilities, so they become scarier.

The transformation move: **declare a file-size ceiling, identify files over it, decompose them along natural seams.**

## When to apply

Every codebase we've audited has god files. Always at least one >800 lines. Usually one >1,000. Apply this chapter's method when:

- You want a demonstrable, measurable win early in an engagement.
- The team reports "we're afraid to touch file X."
- A file's commit history shows edits from 5+ different engineers over 2+ years.

## The rule we impose

**500 lines is the hard ceiling for a Python source file. 300 lines is the target. 200 lines is preferred.**

These numbers are engineering-culture-dependent but the ratios matter more than the absolute values. Published in `docs/ARCHITECTURE.md` as a contract, not an aspiration. Enforced in CI.

## The decomposition sequence

For each file that violates the ceiling:

### 1. Understand before splitting
Read the file end to end. Identify the natural seams:
- Imports grouped by purpose (side-effectful vs. pure vs. third-party)
- Classes that don't share state with other classes in the file
- Functions that form a self-contained workflow
- Helper code that's used only by one class

A 1,000-line file rarely contains 1,000 lines of one thing. It usually contains 200 lines of five things.

### 2. Start with the most isolated seam
Not the biggest — the most *isolated*. A seam that pulls nothing from the rest of the file. This minimizes the refactor's blast radius. Successful small extractions build confidence; a failed big extraction triggers team anxiety.

### 3. Write the tests first (if none exist)
If the god file has no tests, you cannot refactor it safely. Write behavioral tests against the public surface before moving code. The tests should pass against the original, pass after extraction, and be unchanged between the two.

### 4. Move, don't copy
Git move (`git mv`) preserves history. When you split a 1,000-line file into five 200-line files, each should inherit the relevant history. This matters for future `git blame` and for preserving authorship credit.

### 5. Re-export for backward compatibility — briefly
Keep the old module importable, re-exporting from the new locations, for exactly one merge cycle. Remove the shim in the *next* commit. Do not leave shims indefinitely; they become new load-bearing duplication (see Chapter 3).

### 6. Apply the ceiling in CI
After the first file is under the ceiling, add a CI check that fails if any file exceeds it. This locks in the improvement and prevents regression.

## Evidence — Solstein v1→v2

| Metric | Before | After |
|---|---|---|
| Source files | 659 | 18 |
| Largest file | 1,168 lines (`src/solstein/domain/models.py`) | 134 lines (`src/solstein/export/writers.py`) |
| Files > 500 LOC | 14 | 0 |
| Total LOC | 112,300 | 887 |

### What the v1 god files contained

`domain/models.py` (1,168 lines) was nominally a "models" file. It contained: base SQLAlchemy classes, seven domain models, four enrichment models, three research-pipeline models, an outbox model, mixin helpers, and two utility functions. That's eight responsibilities in one file.

`research/pipeline.py` (943 lines) was nominally the pipeline orchestrator. It contained: the pipeline graph, three discovery strategies, a scoring dispatcher, export-format conversion, a retry loop, and manual test fixtures.

Neither file could be confidently edited without reading all of it first, because any change might collide with one of the other seven responsibilities.

### The decomposition in v2

The v1→v2 rebuild took this further than a typical in-place decomposition would — because v2 was a clean rewrite, we could decompose by *first-principles* rather than by archaeology. The result: 18 files, each with one obvious responsibility.

But the observable metrics (largest file, files >500 LOC) are the same metrics you'd track during an in-place decomposition. They are the metrics we put in front of an executive sponsor to show progress.

## Anti-patterns to avoid

- **Splitting by file count rather than by cohesion.** "Just chop it into 200-line chunks" produces five god files instead of one. The seams must be semantic.
- **Leaving the shim in.** "We'll remove the backward-compat re-export later" never happens. Remove it in the same sprint as the extraction.
- **Decomposing without tests.** You will break something, and you will not know which change broke it.
- **Decomposing the scariest file first.** Build confidence on easier targets. The hardest file often reveals itself differently once simpler decompositions have untangled its dependencies.

## Instrumentation we report to the sponsor

- **Files > 500 LOC, count, over time** — this is the headline metric. Goal: 0.
- **Largest file, LOC, over time** — shows the ceiling descending.
- **Average file size** — should decrease as we split large files faster than we create new ones.
- **Files touched per merged PR, average** — should decrease as decomposition progresses (changes get more localized).

All four metrics can be produced from `git log` and `find | wc -l`. Set up a weekly auto-posted report in the sponsor's preferred channel.
