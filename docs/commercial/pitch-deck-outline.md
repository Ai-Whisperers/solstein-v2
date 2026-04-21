# Pitch deck outline — AI-native transformation for PE portfolios

> Slide-by-slide structure for a 12-slide deck for a 30-45 minute meeting with a PE partner.
> Two versions in one document: the PE-partner deck (for firms like Vortex) and the portco-leadership deck (for a CTO/CEO at a target portco).
> Markdown source — when we need a real deck, convert to Slides / Pitch.com / Keynote / Google Slides by a designer.

---

## Version 1 — PE partner deck (Vortex-style audience)

**Audience:** investment partner at a software-focused mid-market PE firm
**Context:** 30-45 minute meeting, warm intro, first conversation
**Goal:** leave with (a) buy-in to pilot one portco engagement, (b) interest in a Portfolio Partnership Agreement

### Slide 1 — Title

**AI-Whisperers**
*Transforming PE portfolios into AI-native operations*

Minimal slide. Company name, tagline, meeting date, attendee names. Sets professional tone.

### Slide 2 — The opportunity

**Your portfolio is carrying AI-transformation debt.**

One chart: your portfolio vs. the top-quartile software-PE average on three metrics:
- AI tooling deployment across engineering orgs (%)
- Deploy frequency (per week, median across portcos)
- Engineering time on integration / rework (%)

Source the top-quartile data from public signals we've aggregated. Frame it as: *"The AI-native cohort is pulling ahead. The gap widens 2-3× per year."*

Call out: *"Every quarter without transformation is compounding opportunity cost — in engineering velocity, in margin, and in exit valuation multiples."*

### Slide 3 — What AI-native actually looks like

Side-by-side: a legacy engineering org vs. an AI-native one, across 5 dimensions:

| | Legacy | AI-native |
|---|---|---|
| PR cycle time | 7-14 days | 1-3 days |
| Code review | Human-only, bottlenecked | AI-augmented, human-gated |
| Ticket lifecycle | 5-step manual workflow | 2-step, most automated |
| Test coverage | "Good but untrusted" | Measured, behavioral-contract-based |
| Integration effort per change | 15-30% overhead | 2-5% overhead |

Not aspirational. Observed from our engagements and published state-of-software reports.

### Slide 4 — The maturity curve

Diagram: the 5 stages of AI-native transformation:

1. **Pre-AI** — no AI in engineering workflows
2. **Individual adoption** — some engineers use ChatGPT / Claude informally
3. **Team deployment** — shared tooling, shared prompts, still ad-hoc
4. **Process integration** — AI in PR review, ticket triage, code generation flows
5. **Full AI-native** — AI as load-bearing infrastructure; measurable across all engineering KPIs

*"We've found most PE portfolios have 2-4 portcos at stages 1-2, and no portcos at stages 4-5. The gap between stage 2 and stage 4 is 12-18 months of focused work."*

### Slide 5 — Why us

Three bullets. No self-congratulation.

- **We've done this, on ourselves.** The Solstein v1→v2 rebuild is our own case study. 99.2% LOC reduction, 0 stub agents, 0 god files, honest scoring restored. One focused session.
- **Our methodology is published.** 9 chapters, each with measurable before/after. Not consultancy slideware — actual operational playbooks.
- **We sell services, not seats.** Fixed-fee diagnostics, success-criteria-based pilots, optional equity for longer engagements. Aligned incentives, no billable-hours roulette.

### Slide 6 — What we've done for your portfolio — speculatively

Show: an outside-in readiness scorecard applied to 3-5 of their named portcos, using public signals only. Score each on our rubric. Identify the highest-fit candidates for a Phase 1 engagement.

This is the slide that surprises them. We did outside-in research on their portfolio *before* the meeting. Shows preparation, capability, and respect.

If preparing for Vortex: Eneve + Infotopics + Bloxs + Reptune + Kitry, with a per-portco mini-assessment.

### Slide 7 — The offering — Phase 1 diagnostic

**€25K, 10 working days, fixed fee. Standalone value.**

What it is: 2-week on-site engagement. Codebase audit. Delivery-metric baseline. Architecture interviews. Written transformation plan with prioritized pilots. Final presentation.

What makes it different: The deliverable has standalone value. If you decide not to proceed with us to Phase 2, you keep the plan and your team can execute. We charge for the diagnostic alone precisely so our recommendation isn't biased by downstream revenue.

### Slide 8 — Phase 2 — pilots with proof

After Phase 1, 1-3 targeted 6-week pilots. €40-60K each. Success-criteria driven. Produce measurable delta on specific metrics (PR cycle time, deploy frequency, engineering time on integration).

Show sample pilot shape from the methodology (e.g., *"Cross-codebase integration layer + god-file decomposition"* pilot — 6 weeks, €50K, expected outcomes listed).

### Slide 9 — Phase 3 — full transformation (equity-inclusive optional)

For portcos where Phase 2 lands, a 6-12 month full transformation engagement. €500K+ cash-equivalent, with a cash/equity hybrid available.

Optional. Most engagements stop at Phase 2; Phase 3 is for portcos that want AI-native transformation as a strategic initiative.

### Slide 10 — Portfolio Partnership Agreement

For PE firms (not portcos) — the multi-year framework.

- €10K/month retainer
- Quarterly portfolio benchmark reports
- 48-hour diligence-support turnaround
- Priority access for Phase 1-3 engagements at portcos
- Methodology access for operating partners

*"We think the highest-leverage conversation is at the portfolio level, not the portco level. But we can start either way."*

### Slide 11 — The case studies (and the one we don't have yet)

**What we can show:** Solstein v1→v2. AI-Whisperers itself, as the transformation subject. Real metrics, real git history, honest before/after.

**What we don't have yet:** a named third-party case study. We're candid about this — we're early in the commercial motion. If that matters to you, we can discuss a pilot structure that produces a public case study as an output.

Better to surface this honestly than be caught claiming more than we have.

### Slide 12 — Next steps

Three options, same slide:

1. **Phase 1 pilot with one named portco.** Pick one. 14 days from signed SOW to kickoff. €25K fixed. First output in 10 working days after kickoff.
2. **Portfolio Partnership Agreement exploratory conversation.** Schedule 2-3 working meetings to scope. Term sheet in 30 days.
3. **Wait and watch.** Subscribe to our quarterly industry benchmark report (free to PE firms). Re-engage when ready.

End with: *"Which of these is the right next step for your side?"*

---

## Version 2 — Portco leadership deck (CTO/CEO audience)

**Audience:** CTO or CEO at a specific portco, often after a PE-firm introduction
**Context:** 45-60 minute meeting, possibly with the CFO/COO also present
**Goal:** confirm Phase 1 engagement (if sponsored by PE firm) or negotiate Phase 1 scope

### Slide 1 — Title + context

**AI-Whisperers × `{PORTCO}`**
*Phase 1 diagnostic discussion*

Note the PE sponsor in the subtitle. Establishes that this conversation is sponsored, not cold.

### Slide 2 — What we heard from `{PE_FIRM}`

Summarize the sponsor context:
- *"[PE firm] asked us to explore where AI-native transformation would deliver the biggest lift at [PORTCO]."*
- *"Not prescriptive — this meeting is for both sides to see if there's a fit."*
- *"You're not obligated to proceed. If you do, the diagnostic itself produces standalone value."*

This slide de-risks the conversation. The portco isn't being sold a solution; they're being invited to evaluate one.

### Slide 3 — What we already know (public signals)

5-7 bullets from the outside-in assessment we prepared before the meeting:
- Company scale + recent history (M&A, funding, growth)
- Product / customer summary
- Public tech signals we observed (or didn't)
- One or two specific transformation hypotheses

Not over-claiming. Just: *"Here's what we can see from outside. We're curious what we can't see."*

### Slide 4 — What a Phase 1 reveals

Diagram: the structure of a Phase 1.

10 days, 5 sections:
1. Codebase audit (metrics)
2. Architecture interviews (4 × 1 hr)
3. Delivery-signal analysis
4. Transformation plan draft
5. Final presentation (joint with PE sponsor)

Emphasize: *"You control access. You control the interview list. You set the kickoff date."*

### Slide 5 — Sample deliverable

Show the sanitized `phase-1-sample-deliverable.md` for 2-3 slides' worth of content, possibly split across slides 5-7.

Highlight:
- 5-section structure
- Pilot recommendations with success criteria
- 30-60-90 roadmap
- Raw-data appendices

### Slide 8 — The economics

**€25K fixed fee. No hourly billing. 50/50 payment schedule (kickoff + delivery).**

Who pays: either the PE sponsor or the portco, by mutual arrangement. Both common.

What's included vs. what's change-order'd: clear scope boundaries per the Phase 1 SOW.

### Slide 9 — What happens after

Three paths:
1. **No Phase 2.** You keep the plan, we part ways. No commitment.
2. **One or more pilots.** Success-criteria-driven, fixed-fee. Start with one; escalate based on outcomes.
3. **Full transformation partnership.** 6-12 month engagement, optionally equity-inclusive.

*"The diagnostic is designed to be useful even if you don't pick us for what's next."*

### Slide 10 — Team on our side

Named individuals for the engagement (lead engineer + partner). Credentials. What each will spend on your engagement.

Less important slide; skippable if meeting is running over.

### Slide 11 — Your team's time commitment

Be honest about what we need:
- 4-6 hours of read-access setup
- 4 × 1-hour interviews with senior engineers
- 2 × 30-min check-ins with exec sponsor
- 90-minute final presentation

Total: ~10 hours of your team's time across 2 weeks. Deliberately low.

### Slide 12 — Next steps

Specific asks:
1. SOW countersignature (we send after this meeting)
2. Named point-of-contact for engagement coordination
3. Kickoff date (propose 2 options)
4. Interview subject list (we propose, you confirm/modify)

End with a working meeting calendar scheduled before leaving the room. Don't let momentum dissipate.

---

## Design notes (for whoever builds the actual deck)

- **Typography:** high-contrast, sans-serif, large body text. PE partners skim; if a slide can't be read at a glance, it fails.
- **Color:** monochrome with one accent color. Not purple/gold (that was v1's Solstein branding; v2 should look different).
- **Data density:** one main point per slide. Supporting data in smaller type. Never two headline messages on one slide.
- **Chartjunk:** none. Tables and plain numbers beat infographics.
- **Length:** 12 slides for PE partners, 12 for portcos. The deck is a conversation guide, not a document. If you need more slides, you're not ready.

## Do NOT include these slides (common mistakes)

- "Our team" with headshots and resumes. PE partners assume you're credible or you wouldn't be in the room.
- "Our clients" logo parade. We don't have a logo parade yet; don't fake one.
- "Our process" with a 6-step diagram. We have a methodology with 9 chapters — don't reduce it to cartoon form for the deck. Reference the playbook.
- "The market" slide with analyst-report statistics about AI market size. PE partners have already seen those; they're TL;DR'd.
- An overly-cute tagline. *"AI-Whisperers"* is already branded; don't add a layer.

## Version-control note

This outline is the canonical structure. The actual deck files (once produced) live in `docs/commercial/decks/` as:
- `pe-partner-deck.pdf` (for sending)
- `portco-leadership-deck.pdf` (for sending)
- `pe-partner-deck.key` or `.pptx` (for editing)

Design iterations go in `docs/commercial/decks/drafts/`.
