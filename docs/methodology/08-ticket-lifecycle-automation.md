# Chapter 8 — Ticket lifecycle automation

> ⚠️ **Status: design document.** Unlike the other chapters in this playbook, we have not yet executed this pattern end-to-end in a client engagement. The design below synthesizes publicly-documented patterns from GitHub (automated PR authoring), Linear (status automation), and internal pilots run on small personal projects. It will be rewritten with measured evidence after the first client pilot.
>
> Why it's in the playbook despite not being executed yet: (a) it's the most-asked-about pattern from PE partners who've read the other chapters, (b) the underlying tools are stable and well-understood, and (c) a thoughtful design gives us a structured conversation starter even in the absence of case evidence. We are honest in Phase 1 conversations about its design-only status.

---

## The pattern

A software engineering organization's ticket lifecycle — the path from "a bug is reported" or "a feature is proposed" to "a change is merged and deployed" — typically spans 10-30 discrete steps: triage, assignment, acceptance, branch creation, code change, PR opening, review, revisions, approval, merge, deploy, close-out. Most of those steps are human-driven. Many should not be.

**The transformation move: automate the steps that are deterministic given context, leaving humans as gates on the decisions that actually require judgment.**

Done well, this collapses the median cycle time (ticket opened → change shipped) from 7-14 days to 1-3 days, *without* removing human judgment from the loop. It removes human *transcription* work.

## Where automation typically wins

Six steps in the ticket lifecycle are high-leverage targets:

### 1. Initial triage
A new ticket arrives. Someone has to decide: is this a bug or a feature? What component does it touch? Who owns it? How urgent is it? Those judgments are 60-80% deterministic from the ticket text + component/owner metadata already in the tracker. An AI-augmented triage step can pre-populate these fields in under 30 seconds, leaving a human to confirm or override.

**Before:** ticket sits in a backlog for 2-5 days until a team lead gets to it during a triage meeting.
**After:** ticket has tentative labels, owner suggestion, and severity within minutes. Team lead reviews and either accepts (80% of cases) or adjusts (20%).

### 2. Duplicate / similarity detection
Large trackers accumulate duplicate tickets and near-duplicate tickets. Before an engineer starts work, they should know: *"this has already been filed 3 times; here's the canonical one"* or *"this is very similar to the issue resolved in PR #2341 — here's why it might be a regression."* Semantic-search against closed tickets and recent PRs surfaces this in seconds.

### 3. First-draft implementation (for bounded, well-specified tickets)
Not every ticket. But about 15-25% of real-world tickets are bounded enough that an AI can produce a first-draft PR — particularly: typos in user-facing copy, small dependency bumps, straightforward test additions for uncovered code paths, linting / formatting sweeps, mechanical refactors.

For these, a bot opens a PR, runs tests, and either marks it ready for review or flags why it couldn't complete. Human reviewer sees a ready PR, not an empty ticket.

**Rule:** the bot never merges. Humans gate the merge. The bot produces the PR; the human reviews like any other contributor.

### 4. PR review assistance
Separate from authoring: AI as a first-pass reviewer on every human-authored PR. Checks for: pattern consistency with the rest of the codebase, missing tests, security anti-patterns, documentation drift, load-bearing duplication (Ch. 3), god-file growth (Ch. 2).

This does not replace human review. It pre-filters obvious issues so human reviewers spend time on judgment, not mechanical checks.

### 5. Status updates and sync
Status transitions (`in progress` → `in review` → `merged`) are almost always derivable from PR state. The PR was opened — ticket is `in review`. Reviewer approved — ticket is `approved`. PR merged — ticket is `done`. Synchronizing these automatically eliminates the "ticket says in-progress but PR has been merged for 3 days" problem.

### 6. Close-out and learning capture
After a ticket ships: did the fix actually resolve the reported issue? An auto-generated "verification" message to the reporter (with a clean repro path) surfaces regressions fast. Closed tickets get auto-categorized for trend analysis — *"this week we fixed 8 bugs; 3 were in component X, 2 were regressions of previously-fixed issues."*

## Where automation loses

Equal space to the failures, which we've observed or read credible accounts of:

### 1. Overly-aggressive triage
Bots that auto-assign tickets to engineers without human gating cause resentment and mis-assignment. Triage *suggestions* work; triage *decisions* don't.

### 2. Bot-authored PRs landing in noise
An LLM that opens 40 small PRs per day floods reviewers. The bot either produces genuinely-ready PRs (good) or becomes noise (bad). The line between the two is: does the bot run your test suite before opening the PR? If tests don't pass, it shouldn't open.

### 3. AI reviewer as gate, not suggestion
A reviewer bot that can block a merge frustrates developers when it's wrong (frequent). Bot comments must be suggestions, not blocking checks. Exception: mechanical gates (lint, typecheck, tests) are fine as blocking because they're deterministic.

### 4. Status sync without reconciliation
Automatic status sync without a human in the loop breaks when the tracker gets into an inconsistent state (rebases, force-pushes, deleted branches). Reconciliation logic for edge cases is non-trivial.

### 5. Metric gaming
The moment cycle-time becomes a measured metric, engineers and bots alike find ways to close tickets faster without shipping anything useful. Track cycle time *alongside* other measures (defect rate, revert rate, customer-reported issues) to prevent gaming.

## Tool stack (what we expect to deploy in a pilot)

Design-phase choices, subject to change based on client environment:

### Foundation layer
- **Claude Code** (or Cursor, or similar) — engineer workstation integration. Each engineer uses daily for pair-programming, refactoring, and code review.
- **GitHub Actions / GitLab CI / Jenkins** — whatever client already has. No new CI platform.
- **Linear / Jira / GitHub Issues** — again, whatever client already has.

### Automation layer
- **GitHub MCP server** or equivalent — allows AI tools to read/write PRs, issues, and reviews.
- **Webhook dispatcher** — receives ticket-tracker events, triggers AI agents, writes back results.
- **Semantic search over closed tickets** (pgvector-backed or Pinecone or Qdrant depending on data volume) — powers duplicate detection.

### Orchestration layer
- **Hermes or n8n or Temporal** — long-running automation workflows (triage → wait for human → proceed) with reliable state.
- **Prompt library** (see `docs/methodology/prompts/`) — version-controlled prompts for each automation path, with the approved Claude / OpenAI / etc. models bound to them.

### Observability layer
- **Cycle time dashboard** — median / p90 ticket-to-shipped time, per team, over time.
- **Revert rate** — reverts / merges, weekly. Spike indicates regression from automation.
- **Bot intervention rate** — % of PRs where the bot contributed something substantive. Too low means under-use; too high means noise.
- **Human override rate** — % of bot suggestions that humans reject. Should be 15-35% steady state; much higher means the bot is wrong, much lower means humans aren't actually reviewing.

## Roll-out sequence (for a Phase 2 pilot)

4-6 weeks, one team at a time:

**Week 1:** instrumentation only. No automation yet. Measure current cycle time, revert rate, status-sync drift, duplicate rate. Establish the baseline.

**Week 2:** deploy #1 (triage assist). AI suggests labels and owners on incoming tickets. Team lead reviews each suggestion for 10 business days. Adjust prompts based on rejection patterns.

**Week 3:** deploy #2 (semantic duplicate detection). Integrate into ticket creation flow — new tickets get "possibly related to" suggestions. Measure how often those are useful.

**Week 4:** deploy #3 (status sync). PR state → ticket state, automatic. Start with one component; expand after a week of clean operation.

**Week 5:** deploy #4 (AI PR reviewer). Suggestions only, not blocking. Team calibrates on what the bot is seeing well and what it's missing.

**Week 6:** deploy #5 (bot-authored PRs for bounded tickets). Start with the 3-5 categories where bot authoring works best for your codebase (deps, copy, test-gap fills). Strict bot-doesn't-merge rule.

Measure the whole time. At the end of week 6, present the team's cycle time, revert rate, and bot-intervention rate to the exec sponsor. Decide: expand, iterate, or roll back.

## Expected metrics deltas (from public benchmarks + internal pilots)

Not promises. Honest ranges:

| Metric | Typical baseline | Typical after 6 weeks | Typical after 6 months |
|---|---|---|---|
| Median ticket cycle time | 7-14 days | 4-8 days | 1-3 days |
| Revert rate | 1-3% | 1-3% (should not rise) | 1-3% |
| Duplicate ticket rate | 5-10% | 2-5% | 2-5% |
| Status-sync drift (stale tickets) | 15-25% | 5-10% | <5% |
| Bot PR authoring volume | 0% | 5-10% of PRs | 15-25% of PRs |
| Human override rate on bot suggestions | — | 40-60% (initial) | 15-35% (calibrated) |

Caveats: these ranges are observed from our own smaller-scale work plus public case studies. Client-specific ranges may vary widely depending on codebase maturity, team size, and prior automation.

## What the sponsor sees weekly

A 1-page dashboard posted to the exec sponsor's preferred channel:

- Cycle time (this week's median, trend arrow vs. last month)
- Revert rate (this week, trend arrow)
- Bot intervention rate (this week)
- Top 3 automation wins this week (with ticket links)
- Top 1-2 automation issues this week (with resolution status)

Single page. Readable in under 2 minutes. Executives don't read dashboards that require more than 2 minutes.

## Anti-patterns we won't do

- **Replace engineers with AI.** The automation removes transcription work, not engineering judgment. We explicitly tell sponsors: your headcount doesn't decrease from this; your engineering velocity increases.
- **Optimize one metric at the expense of others.** Cycle time without revert rate is meaningless.
- **Deploy everything at once.** The 6-week roll-out sequence is deliberately incremental. Faster deployment always produces rollbacks.
- **Gate the pilot on a specific metric target.** We agree success criteria with the sponsor, but we don't promise *"we'll hit 3-day median cycle time."* We promise to measure, execute, and report honestly. Some environments don't get to 3 days; some get there in 3 weeks.

## How this connects to the rest of the playbook

- Ch. 2 (God-files) — ticket lifecycle automation makes small-PR discipline easier, supporting the decomposition cadence.
- Ch. 5 (CICD) — the automation depends on CI being fast and trustworthy (Ch. 5 is a prerequisite).
- Ch. 6 (Test integrity) — bot-authored PRs rely on tests catching bad changes. Without behavioral contract tests, bot PRs are dangerous.
- Ch. 7 (AI-augmented refactoring) — the prompt-library discipline and session-shape patterns apply directly.
- Ch. 9 (Quality gates) — the bot must pass every quality gate a human PR would.

## When we have executed this in a real engagement

Re-write this chapter with:
- Named pilot client (anonymized if required)
- Actual baseline and after metrics
- Specific gotchas encountered
- Specific prompts that worked and didn't
- A case-study sidebar analogous to Ch. 2's "Evidence — Solstein v1→v2"

Until then, this chapter is labeled as design-only at the top. We do not present it to clients as evidence of executed work.
