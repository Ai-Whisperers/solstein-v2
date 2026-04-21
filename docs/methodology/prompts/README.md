# Prompt library

Reusable prompt templates for the AI-augmented refactoring and transformation patterns described in `07-ai-refactoring.md`. Each prompt is:

- **Constrained** — specifies scope, forbids unasked-for changes
- **Verifiable** — acceptance criteria expressed as tests where possible
- **Reviewable** — asks for a proposal before execution when non-trivial

## How to use

1. Find the pattern in the relevant methodology chapter
2. Copy the prompt from this directory
3. Fill in the `{PLACEHOLDERS}`
4. Paste into Claude Code / Cursor / equivalent
5. Review the proposal before approving execution
6. Review the diff before committing

These prompts are not magic incantations. They are *starting points*. Adapt them to your project's conventions.

## Index

| Prompt | Pattern | Source chapter |
|---|---|---|
| [god-file-decompose.md](god-file-decompose.md) | Split a file > 500 lines into cohesive sub-files | Ch. 2 |
| [load-bearing-duplication-find.md](load-bearing-duplication-find.md) | Detect duplicated business logic | Ch. 3 |
| [stub-audit.md](stub-audit.md) | Find fake-data stubs pretending to be real | Ch. 4 |
| [test-structural-to-behavioral.md](test-structural-to-behavioral.md) | Convert a structural test into a behavioral contract test | Ch. 6 |
| [refactor-session-plan.md](refactor-session-plan.md) | Plan a 2-4 hour refactoring session | Ch. 7 |
| [ci-consolidate.md](ci-consolidate.md) | Consolidate a sprawling CI config | Ch. 5 |

## Writing more prompts

When you develop a prompt that works well in an engagement, add it here:

1. Create a new `.md` file in this directory
2. Follow the template structure below
3. Add it to the index above
4. Commit with a descriptive message

## Prompt template

```markdown
# Prompt — {name}

**Goal:** One sentence describing what this prompt is meant to accomplish.
**Source chapter:** Link to relevant methodology chapter.
**Typical runtime:** 30 min / 2 hours / 1 day — expected scope.
**Prerequisites:** What must be true before running this prompt.

## The prompt

(The actual prompt text, with `{PLACEHOLDERS}`.)

## Post-conditions

What should be true after the AI completes this.

## Common failure modes

What tends to go wrong, and how to spot it.

## Evidence

Where this prompt has been used, with what outcome.
```
