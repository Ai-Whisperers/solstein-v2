# Prompt — Refactor session plan

**Goal:** Given a codebase state and a goal, produce a disciplined 2-4 hour refactoring session plan following the Ch. 7 AI-augmented refactoring discipline.
**Source chapter:** [07-ai-refactoring.md](../07-ai-refactoring.md)
**Typical runtime:** 15-30 minutes to produce the plan; then 2-4 hours to execute.
**Prerequisites:** The goal is specific. "Make it better" is not a goal. "Reduce files >500 LOC from 5 to 0" is a goal.

## The prompt (for planning)

```
I want to plan a focused refactoring session. My goal is: `{SPECIFIC_GOAL}`.

Current state (check these before proposing a plan):
- Run `find src -name "*.py" -exec wc -l {} + | sort -rn | head -20` and report the top 20 files by LOC
- Run `pytest --collect-only 2>&1 | grep -c "error"` to see if any tests fail to collect
- Run `ruff check src/ tests/ --statistics` to see the lint state
- Run `mypy src/` to see the type state

Now propose a session plan with:

1. **Baseline** — the exact metrics at session start. These go in the commit message at session end.
2. **1-3 discrete outcomes** for the session. Each is a committable unit. Don't plan more than can be finished in 2-4 hours.
3. **Execution order** — which outcome first, which last. Easier / more isolated ones first to build momentum.
4. **Per-outcome task list** — the specific prompts I should send the AI for each outcome, and the review checklist I should use on each diff.
5. **Exit criteria** — at the end of the session, what must be true before I commit each outcome? (Tests pass, lint clean, behavior preserved, etc.)
6. **Stop-loss** — if an outcome isn't achievable in the allocated time, what do I revert, what do I keep?

Do NOT execute any work. Return the plan as a structured markdown document. I'll review, adjust, then execute one outcome at a time.
```

## Post-conditions

A session plan document. Zero code changes.

## Common failure modes

### Plan is too ambitious
If the plan lists 8 outcomes for one session, it's wrong. 1-3 is the range. Re-prompt.

### Execution order prioritizes the hard thing first
"Start with the most important" is usually wrong for refactoring. Start with the most *isolated*. Momentum compounds.

### Exit criteria are vague
"All tests pass" is necessary but insufficient. Exit criteria must include: specific metric thresholds, diff-size limit, behavior-preservation check. Re-prompt if missing.

### Stop-loss isn't defined
Without a stop-loss, a refactor that's going badly consumes the whole session before you revert. Every outcome needs a "if X, revert and move on" clause.

## The prompt (for execution, per outcome)

Use this after the plan is approved, for each outcome in order:

```
We're executing outcome {N} of our session plan: `{OUTCOME_DESCRIPTION}`.

Per our plan:
- Acceptance criteria: {ACCEPTANCE_CRITERIA}
- Diff size budget: < {N} lines
- Tests that must still pass: {TEST_SCOPE}
- Forbidden changes: anything outside {SCOPE}

Before any code changes:
1. Read the code in scope
2. Propose the exact changes in plain language (what changes, where, why)
3. Wait for my approval

After approval:
1. Make the changes
2. Run {TEST_COMMAND}
3. If any test fails or if the diff exceeds the budget, stop and show me
4. If all green and budget respected, give me the diff to review

I'll commit if I approve the diff. Then we move to the next outcome.
```

## Evidence

- The Solstein v2 rebuild was one 4-hour session using this discipline.
- 5 commits produced, all green at each commit.
- Four misdirections caught in review (documented in `07-ai-refactoring.md`), zero surviving into committed code.
- Not yet used in a paid engagement, but internally heavily relied on during our own v2 rebuild.
