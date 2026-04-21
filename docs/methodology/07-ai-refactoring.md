# Chapter 7 — AI-augmented refactoring

The methodology in chapters 2-6 describes *what* to change. This chapter describes *how* — the specific working pattern we use to execute transformation with AI coding assistants (primarily Claude Code + Claude Opus 4.7 in our current stack).

The working pattern matters because it's the hardest part to transfer to a client team. Telling someone "decompose this god file" is easy. Making them productive at it — at the speed we are — requires discipline about how the human and the AI divide the work.

## The contract between human and AI

### What the AI does well
- Extracts structure from unstructured code at high speed (identify all functions, classes, dependencies in a 1,000-line file)
- Generates a first-draft refactor from a clear specification
- Applies uniform transformations (rename, reformat, replace pattern X with pattern Y) across a large codebase
- Writes tests against specified behavior
- Writes docstrings and documentation
- Catches mechanical errors (wrong import, missing return, type mismatch)

### What the AI does badly
- Deciding *what* to refactor — the AI will cheerfully refactor the wrong thing if asked
- Making architectural tradeoffs ("should this be a class or a function?" — the answer is context-dependent)
- Preserving intentional anomalies (sometimes code is weird *on purpose*; the AI tends to "fix" it)
- Noticing when the instructions were wrong (the AI will execute a bad plan confidently)
- Saying no to scope creep

### The human's job, therefore
- Pick the refactor. Not "make it better" — specific, concrete, with acceptance criteria.
- Constrain the scope. "Don't change anything outside these files."
- Review the diff. Every line. The AI is fast and correct, but not always right.
- Kill bad attempts early. If the first pass is wrong, revert and redirect; don't iterate on a bad foundation.
- Ship each increment. Commit often. Don't accumulate unreviewed AI-generated changes.

## The working session shape

A typical AI-augmented refactoring session runs 2-4 hours. Longer and fatigue degrades review quality. Shorter and you don't get enough done.

**Session structure:**

1. **Scope the session (10 min).** Exactly what gets done today. 1-3 discrete outcomes. Write them down.

2. **Establish baseline (5 min).** Run the tests. Capture the "before" metrics for anything we'll measure: file count, LOC, test count, lint errors.

3. **Work the loop (90-150 min).** Repeatedly:
   - Give the AI a concrete task with constraints
   - AI writes/modifies code
   - Human reviews the diff
   - Run tests
   - If green, commit. If red, revert or fix.
   - Move to the next task

4. **Pause (15 min).** Mid-session, step away. Review what's been done. Re-scope if needed.

5. **Close the session (20 min).** Run all the tests. Run lint. Run typecheck. Write the commit message yourself — the AI writes decent commit messages but you want to be the one who signed off. Capture the "after" metrics. Push.

## Prompting patterns that work

### Imposed constraints over open goals
Bad: *"Clean up this codebase."*
Good: *"We want no file in `src/` to exceed 300 lines. Currently 5 files violate this. Pick the most isolated one — the one with the fewest cross-file dependencies — and decompose it. Propose the split before touching code."*

The AI with open goals will generate sprawling, impressive-looking changes that don't compose. Imposed constraints produce focused, reviewable diffs.

### Require proposal before execution
For any non-trivial refactor, ask the AI to produce a plan first. Read the plan. Either approve, modify, or reject. Only then does code change.

> *"Before you write any code: list the functions in `pipeline.py`, group them into logical clusters, and propose a 4-file split. Include the dependency graph between the proposed files. I'll approve or modify the plan before you execute it."*

This stops about 80% of wasted refactor attempts.

### State the acceptance criteria in tests, not prose
Bad: *"Make sure it still works after the refactor."*
Good: *"All existing tests must pass after the refactor. Additionally, add a behavioral contract test: `test_eneve_scoring_is_deterministic` — feed the Eneve fixture twice, assert same output both times."*

Acceptance criteria expressed as tests are unambiguous and self-verifying.

### Forbid unasked-for changes
Add a line to every prompt for a big session:

> *"Do not modify any file outside `src/solstein/scoring/`. Do not 'while we're at it' any other changes. If you notice unrelated issues, list them in a comment at the end — don't fix them."*

The AI's tendency to "improve while refactoring" is the single biggest source of messy diffs. Lock it down.

### Use git as the safety net, not undo
Commit every 15-30 minutes of successful work. Don't accumulate 3 hours of un-committed changes. When something goes wrong — and it will — `git reset --hard HEAD` is cheap. Rebuilding 3 hours of work from a bad intermediate state is not.

## Review patterns that work

### Read the diff, not the description
The AI will describe its change accurately. That's not the problem. The problem is the description might say *"renamed `process_company` to `score_company`"* and the diff might also include *"added a try/except that swallows errors in 6 places."* Read the diff.

### Check for these specific anti-patterns every time
- `except Exception: pass` or equivalent — silent error swallowing
- New hardcoded values — magic numbers not near the domain
- New imports from unexpected places — cross-layer violations
- Changes to tests that weakened assertions
- Removed `raise` statements
- Changed defaults that could affect production behavior

### If the diff is too large to review properly, it's too large to commit
Real rule, not an aspiration. Target: 200 lines of diff max per commit. If the AI produces 500, break it into 2-3 commits. If it produces 2,000, something went wrong in the session planning.

## When the AI is faster than the human can review

This happens. The AI can produce a 500-line diff in 30 seconds. The human needs 15 minutes to review it properly.

Two rules:
- **The review time is the real throughput.** Measure sessions by reviewed-and-committed LOC, not AI-generated LOC.
- **If you're behind, slow down the AI.** Break the work into smaller tasks, not bigger. Smaller tasks = faster, better review = more throughput overall.

## Evidence — the Solstein v2 session

The v1→v2 rebuild was a single 4-hour focused session. Output:
- 18 source files written from scratch
- 43 tests written and passing
- Full CI config
- Three methodology chapters (simultaneously)
- A commercial SOW template
- A case study document

Total AI-generated LOC (code + docs): ~2,500
Total commits: 5
Average diff per commit: ~500 LOC (higher than the 200-line target, but these were scaffolding commits not refactors of existing code — the ratio is different for green-field work)

Things that went wrong in the session (honest):
- The AI initially wrote a regression test that asserted Eneve's *v1* score (9.03). I caught this in review — v1's 9.03 was synthetic. Fixed by rewriting the test to assert the honest v2 score (5.97).
- The AI proposed using sync `requests` for the GitHub adapter before I stated the httpx-native constraint. Redirected.
- The AI added a commented-out code block; ruff caught it and I removed it.
- The AI's first CI workflow was a copy of v1's, including 3 workflows we'd decided to drop. I made it rewrite to 1 workflow.

Four correctable misdirections in 4 hours. Zero that survived to a commit. That's the discipline this chapter is about.

## What we report to the sponsor

During a Phase 2 pilot:
- **Session length and structure** (is the team running disciplined 2-4 hour sessions or flailing?)
- **Review-to-generation ratio** (how much of what the AI produces is being committed vs. discarded?)
- **Reversions per session** (some is healthy; excessive is a signal that tasks are too big)
- **LOC committed per session** (steady growth is the goal; spikes followed by crashes = session structure problem)

## Anti-patterns to avoid

- **"Just refactor the whole thing."** Produces diffs nobody can review, which produces commits that hide bugs.
- **Unreviewed AI output in main branch.** The AI is fast; that doesn't substitute for review.
- **Accepting changes because the AI said they're correct.** The AI will confidently ship code that looks right and isn't.
- **Using the AI to make architectural decisions.** Ask it for analysis; make the decision yourself.
- **No rollback plan.** Every session should be rollback-able to pre-session state in one command. If it isn't, you're one bad diff away from chaos.
