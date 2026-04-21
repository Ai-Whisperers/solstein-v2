# Prompt — CI consolidation

**Goal:** Take a sprawling CI configuration (multiple workflows, composite actions, dead scripts, advisory gates) and consolidate to 1-3 honest workflows.
**Source chapter:** [05-cicd-rebuild.md](../05-cicd-rebuild.md)
**Typical runtime:** 2-4 hours — longer than most refactoring prompts because CI changes need to be verified against real runs.
**Prerequisites:** write access to the CI config; ability to trigger test CI runs on a branch without merging; knowledge of what the CI is *supposed* to gate (which the AI cannot infer).

## The prompt (inventory phase)

```
I want to consolidate this repo's CI. First, inventory what exists.

For each file in `.github/workflows/` (or the equivalent for GitLab/Jenkins/etc.), tell me:

1. What triggers the workflow (push, PR, schedule, manual)
2. What jobs it contains and what each job does (1-sentence summary per job)
3. What files/paths each job touches (if scoped via `paths:`)
4. Any `continue-on-error: true`, `if: always()`, or similar flags that make a step non-blocking
5. Any referenced scripts, composite actions, or external services

For each composite action in `.github/workflows/composite/` (or equivalent), tell me:
1. What it does
2. Which workflows use it
3. Whether it's still necessary

Return as a structured markdown table. Do NOT change anything yet.
```

## The prompt (analysis phase)

```
Given the inventory above, answer these questions:

1. **What does CI gate (in aggregate)?** What can/can't merge based on current CI results? Be precise.
2. **Which workflows are load-bearing** (their failure would catch a real regression)?
3. **Which workflows are theatre** (they run but don't actually block a bad merge)?
4. **Are there `continue-on-error` flags on checks that should be blocking?** If yes, those checks are effectively disabled.
5. **Which composite actions are still used?** Which are orphaned?
6. **What's the typical runtime of a PR build (p50)?**
7. **What percentage of PR builds fail for real reasons vs. flaky/infrastructure reasons?**

Return a diagnosis with specific file:line references.
```

## The prompt (consolidation plan phase)

```
Propose a consolidation:

1. What wanted gates should CI have? (e.g., "lint + format + typecheck + test on every PR"; "integration tests on schedule"; "deploy on merge to main")
2. Which existing workflows to delete.
3. Which existing workflows to consolidate into a new structure.
4. The new structure — how many workflows, what each one does, what triggers them.

Propose ONE consolidation. Do not write config yet. I'll approve or revise.

Non-negotiable rules for the new structure:
- No `continue-on-error: true` on any check that's supposed to gate a merge
- Every workflow either blocks a merge or is clearly marked non-blocking (and such workflows should be few)
- Typical PR build runs in under 5 minutes (use fail-fast ordering: lint → typecheck → test)
- Every job can be run locally with the same command (dev parity)
- No orphaned composite actions — delete them as part of the consolidation
```

## The prompt (execution phase)

Once plan is approved:

```
Execute the consolidation plan we agreed.

1. Write the new workflow file(s).
2. Delete the old workflow files.
3. Delete the orphaned composite actions.
4. Delete any scripts referenced only by deleted workflows.

Do not change any test code, source code, or config outside `.github/` (or equivalent) unless it's directly required by the consolidation.

After writing: show me the diff. I'll push to a branch, let CI run, and verify it works before merging.
```

## Post-conditions

- Fewer workflow files (target: 1-3)
- Zero orphaned composite actions
- Zero `continue-on-error: true` on load-bearing checks
- PR build runs in <5 minutes (measured on first run after consolidation)
- Tests that would have failed on the old config still fail on the new config
- Tests that pass on the old config still pass on the new config

## Common failure modes

### Deletion of load-bearing workflows
The AI may delete a workflow it thinks is "advisory" that actually catches real bugs. Always test the consolidation on a branch before merging. If any class of regression appears that the old CI caught, add it back.

### Over-consolidation
Trying to put everything in one workflow to maximize simplicity can produce a 20-minute CI that engineers route around. Keep workflows focused; it's fine to have 3 if they each have a clear purpose.

### Missing matrix / platform coverage
If the old CI ran tests on 3 Python versions and the AI's consolidation runs on 1, that's a silent downgrade. Explicitly specify matrix requirements in the plan.

### CI runs but doesn't gate merge
Workflows must be marked as required in branch protection for them to gate merge. The workflow file change alone doesn't do this. Verify branch protection settings after merging.

## Evidence

- Solstein v1 → v2: went from 5 workflows + 3 composite actions to 1 workflow with 3 jobs. CI runtime dropped from 10-15 min to <2 min. See Ch. 5 evidence section.
- Same approach applied on an internal AI-Whisperers tooling repo with similar results.
- Not yet used in a paid engagement.
