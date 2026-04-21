# Prompt — God-file decomposition

**Goal:** Split a single file that exceeds the 500-line ceiling into multiple cohesive sub-files, preserving behavior and git history.
**Source chapter:** [02-god-files.md](../02-god-files.md)
**Typical runtime:** 1-3 hours depending on file size and test coverage.
**Prerequisites:**
- The file has tests (or tests will be written first — if no tests, use `refactor-session-plan.md` to plan that work first).
- Tests pass against the current code.
- You understand the file's domain well enough to judge whether the AI's proposed decomposition makes sense.

## The prompt

```
I want to decompose the file `{FILE_PATH}` ({N} lines). It violates our 500-line ceiling. Here are the constraints:

Constraints:
1. Do not change behavior. All existing tests must still pass after the decomposition.
2. Do not make any changes outside the scope of this decomposition. If you notice unrelated issues (dead code, style, other violations), list them at the end — do not fix them.
3. Preserve git history per file. We'll use `git mv` where possible.
4. Each new file must be under 300 lines ideally, 500 lines as a hard ceiling.
5. Each new file must have a clear single responsibility. Name files after their responsibility, not after the original file.
6. Prefer extraction by cohesion over extraction by type. A class and its helper functions belong together.

Before writing any code:
1. Read {FILE_PATH} end to end.
2. Identify the logical groupings within the file — classes that share state, functions that form a workflow, helpers used by one class only.
3. Propose a specific decomposition: N new files, with each file's name and the functions/classes that would live in it.
4. List the cross-file imports that would exist after the decomposition.
5. Estimate which seam is most isolated (fewest cross-references) — we'll extract that one first.

Return this proposal as a structured response. Do NOT write code yet. I'll approve or modify the proposal, then we execute.
```

## Post-conditions

After the AI's proposal is approved and executed:

- [ ] `{FILE_PATH}` is either deleted or reduced to below the ceiling
- [ ] Each new file is below the ceiling
- [ ] All existing tests pass
- [ ] `git log --follow` on each new file shows its history from the original file
- [ ] No unrelated changes in the diff

## Common failure modes

### The AI decomposes by type, not by cohesion
Produces `models.py`, `views.py`, `services.py` from a single domain file. This is the wrong kind of split — it scatters cohesive workflows across files. Override the proposal; re-prompt emphasizing cohesion.

### The AI "improves while decomposing"
Adds type hints, reformats, removes what it judges to be dead code — all while doing the decomposition. The diff becomes un-reviewable. Re-prompt with stronger forbid-unrelated-changes language.

### The AI proposes too many small files
10 files with 50 lines each is not an improvement over 1 file with 500 lines. If the proposal has >5 new files for a 500-line decomposition, re-prompt to consolidate.

### Tests pass but behavior changes subtly
Integration tests catch this better than unit tests. If you have integration tests, run them. If not, this prompt is riskier than it looks — do the extraction in smaller chunks with manual verification at each step.

## Evidence

- Solstein v1→v2: used this pattern (in manual form, before this prompt existed) to go from `domain/models.py` (1,168 lines) to a set of files all under 135 lines. See Ch. 2 evidence section.
- Used successfully on internal AI-Whisperers code during the v2 rebuild.
- Not yet used in a paid engagement — will be recorded here when it is.
