# Chapter 1 — Diagnostic framework

The diagnostic is the paid Phase 1 engagement. Ten working days inside the sponsor's engineering organization. Output: a written transformation plan with prioritized pilots, measurable ROI estimates per pilot, and a baseline the team can use even if they don't proceed with us.

## Deliverables

1. **Baseline metrics snapshot** — instrumentation report (see §Metrics below)
2. **Architecture read** — where the load-bearing complexity actually lives
3. **Transformation plan** — 3-5 specific pilots, each with scope, cost, duration, and ROI estimate
4. **Archive-vs-refactor recommendation** — per Ch. 10 framework
5. **30-60-90 day roadmap** — what happens if we execute the plan

## Timeline (10 working days)

| Day | Activity | Deliverable |
|---|---|---|
| 1 | Kickoff + repo read access + Slack/Jira access | Diagnostic kickoff memo |
| 2-3 | Instrumentation scripts run, metrics captured | Baseline metrics draft |
| 4-5 | Architecture interviews (2-3 senior engineers, 1 hour each) | Architecture notes |
| 6 | Audit synthesis — what's real vs. reported | Audit doc (internal draft) |
| 7 | Pilot scoping — identify 5-8 candidate pilots | Pilot longlist |
| 8 | Pilot prioritization — pick 3-5 to recommend | Prioritized pilot list w/ ROI |
| 9 | Write the plan | Transformation plan draft |
| 10 | Present findings + plan | Final deliverable + recorded presentation |

## Metrics we capture

All auto-extractable from a git checkout + CI/test logs + Jira/Linear export:

**Codebase shape**
- Total LOC, language mix
- File size distribution (files > 500 LOC count)
- Largest file, largest class, largest function
- Cyclomatic complexity per file (radon)
- Import cycles count

**Change velocity**
- Commits / week over last 12 months
- Average PR cycle time (open to merge)
- Average PR size (LOC touched)
- Reverts count in last 6 months
- Files touched per merged PR (median)

**Quality signal**
- Test count, test pass rate, test collection success rate
- Line coverage (where measurable)
- Lint error count (ruff/eslint/whatever)
- Type coverage (mypy/pyright strict)

**Delivery signal**
- Deploy frequency (from CI)
- Mean time to recovery (from incident tracker)
- Build time (from CI)
- CI failure rate

**Backlog signal**
- Open tickets by age, by component
- Tickets tagged "tech debt" or equivalent
- Tickets with "blocked" status
- Ratio of bugfix to feature tickets

## Architecture interviews

Two to three senior engineers, one hour each, done 1-on-1. Same four questions, in order:

1. *Walk me through a feature delivery. Use one that shipped recently. What slowed it down?*
2. *If I gave you one month to change one thing in this codebase, with a magic button that changed it safely, what would you change?*
3. *What part of the system are you most afraid to touch? Why?*
4. *What part works well? What are we not allowed to break?*

Let them talk. Take notes. Don't argue. Anonymize the transcripts before distribution.

Q1 surfaces real bottlenecks. Q2 surfaces aspirational priorities (often contradictory between engineers — that itself is signal). Q3 surfaces god files and load-bearing cruft. Q4 prevents us from recommending demolition of actually-valuable work.

## Pilot scoping

We scope candidate pilots using three criteria:

- **Visible** — the outcome is observable to leadership, not just the team
- **Measurable** — has at least one concrete before/after metric
- **Bounded** — can ship in 4-6 weeks with 1-2 engineers

Good pilot shapes:
- *"Automate the ticket → PR workflow with Claude Code for a specific repo"* — measurable (PR cycle time), visible (engineering leads see it), bounded (one repo, 4 weeks).
- *"Decompose the top 3 god files using the Ch. 2 method"* — measurable (files > 500 LOC count), visible (dashboard), bounded (6 weeks).
- *"Rebuild CICD from N workflows to 1-3"* — measurable (CI runtime, workflow count), visible (every engineer feels it), bounded (3 weeks).

Bad pilot shapes:
- *"Improve code quality"* — not measurable.
- *"Rewrite the platform"* — not bounded.
- *"Introduce AI tooling team-wide"* — not visible to leadership as a distinct outcome.

## Transformation plan structure

The plan document is what the sponsor reads. It has five sections:

1. **What we found** — one page, plain language, the three most important observations
2. **Baseline metrics** — the numbers, no narrative
3. **Recommended pilots** — 3-5 pilots, each with: scope, duration, cost, owner, expected metric deltas, success criteria
4. **Archive-vs-refactor recommendation** — our call, with the Ch. 10 score
5. **Next steps** — what happens in the 30/60/90 days after the plan lands

Length target: 15-20 pages. PE-partner-readable. Includes an executive summary at the start that a CEO could read in 5 minutes and understand the recommended action.

## What the sponsor keeps if they don't proceed

This is the key commercial design: the diagnostic has standalone value even without Phase 2. If the sponsor decides not to engage us for the pilots, they walk away with:

- The baseline metrics report (their team can continue tracking)
- The audit (revealing things the team already suspected but hadn't measured)
- The pilot recommendations (they can execute these in-house or with another vendor)
- The 30-60-90 roadmap

We charge for the diagnostic alone precisely because it's valuable alone. Pricing: €20-30K, 2 people × 2 weeks. If we're only paid when they proceed to Phase 2, we become biased toward recommending Phase 2 regardless of whether it's the right call.
