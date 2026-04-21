# Engagement onboarding checklist

Used at kickoff for every Phase 1 diagnostic. Ensures we have everything in place on Day 1 so Days 2-10 are execution, not procurement.

Sent to client's engagement coordinator within 48 hours of SOW countersignature. Client fills in / confirms / escalates per item.

---

## Client-side kickoff memo

Before Day 1, client provides:

### Access (critical path)

- [ ] **Read access to primary repository**
  - Platform: `{GitHub / GitLab / Bitbucket / other}`
  - Access mechanism: `{SSH key / OAuth app / service account}`
  - Named individual on client side: _________
- [ ] **Read access to 1-2 adjacent repositories** (if dependency structure requires)
  - Client decides which are in scope
  - Same access mechanism as primary
- [ ] **Read access to CI logs for the last 6 months**
  - Platform: `{GitHub Actions / Jenkins / CircleCI / other}`
  - History depth: minimum 6 months
- [ ] **Read access to ticket tracker for the last 12 months**
  - Platform: `{Jira / Linear / Asana / GitHub Issues / other}`
  - Filter / project scope agreed with client
- [ ] **Read access to deploy logs / release notes (if separate from CI)**
- [ ] **Read access to incident tracker (if separate)**
  - Just post-mortem documents; we don't need live incident access

### People (critical path)

- [ ] **Named day-to-day point of contact**
  - Name: _________
  - Role: _________
  - Email / Slack: _________
  - Authority: can decide on practical questions without escalation
- [ ] **Executive sponsor**
  - Name: _________
  - Role: CEO / CTO / COO
  - Availability: minimum 2 × 30-min check-ins during engagement
- [ ] **4 interview subjects scheduled**
  - Senior engineers, ideally 1 per major team
  - 60-minute slots, 1-on-1
  - Scheduled across Days 4-5
  - Calendar invites sent by Day 2

### Logistics (non-critical but needed)

- [ ] **Working location agreed**
  - Remote / on-site / hybrid
  - If on-site: days, hours, badge or guest access
- [ ] **Communication channel agreed**
  - Slack Connect / shared Slack channel / email + Zoom
- [ ] **Document drop location agreed**
  - Where we land PDFs and artifacts: `{SharePoint / Google Drive / Notion / Confluence / other}`
- [ ] **Final presentation date + platform confirmed**
  - Date: End of Day 10 (or specific date)
  - Platform: Zoom / Teams / in-person
  - Attendees list: client side

### Legal (must be complete before kickoff)

- [ ] **SOW countersigned**
  - Countersignature date: _________
- [ ] **NDA in place** (or confidentiality terms in SOW sufficient)
- [ ] **First invoice (50%) issued**
  - Issued to: _________ (finance contact)
  - Payment due: 14 days

---

## Provider-side kickoff memo

Before Day 1, AI-Whisperers confirms:

### Team

- [ ] **Lead engineer assigned and confirmed available for full engagement period**
  - Name: _________
- [ ] **Partner assigned for oversight and final presentation**
  - Name: _________
- [ ] **Backup lead identified** (in case of illness / unavailability)
  - Name: _________

### Tooling

- [ ] **Internal engagement repo created** at `engagements/{client}/`
  - Access restricted to named engagement team
  - Includes: SOW PDF, onboarding checklist, interview schedule, working docs
- [ ] **Analysis tooling installed**
  - Latest Solstein v2
  - `radon`, `ruff`, `mypy`, language-specific equivalents for client's stack
  - Scripts for ticket analysis, CI log parsing
- [ ] **Deliverable template instantiated from `docs/assessments/phase-1-sample-deliverable.md`**
- [ ] **Prompt library reviewed against client's stack** (`docs/methodology/07-ai-refactoring.md` references)

### Calendar

- [ ] **Day 1 kickoff meeting scheduled** (60 min, joint with client)
- [ ] **Days 4-5 interview slots held**
- [ ] **Day 6 mid-engagement internal review scheduled** (Provider-only, 60 min)
- [ ] **Day 9 draft review with executive sponsor scheduled** (30 min)
- [ ] **Day 10 final presentation scheduled** (90 min, joint)

### Communication setup

- [ ] **Shared Slack channel established** (or agreed alternative)
- [ ] **Progress report cadence set**
  - End-of-day updates (brief, Slack)
  - Mid-engagement written update (Day 5, PDF)
  - Final deliverable (Day 10)
- [ ] **Escalation path defined**
  - Day-to-day: client point of contact → lead engineer
  - Escalation: executive sponsor → AI-Whisperers partner

---

## Day 1 kickoff meeting agenda

60 minutes, joint client + provider.

1. **Introductions** (5 min)
2. **Engagement objectives recap** (5 min) — restate what Phase 1 will deliver and what it won't
3. **Scope confirmation** (10 min) — walk through the SOW scope section; any open questions
4. **Access check** (15 min) — verify read access works live; resolve any gaps immediately
5. **Interview subject confirmation** (10 min) — confirm 4 names and timeslots
6. **Communication protocols** (5 min) — channel, cadence, escalation
7. **Next milestones** (5 min) — end-of-Day-5 written update, Day-10 presentation
8. **Questions** (5 min)

Produce a 1-page kickoff memo after the meeting, send same-day. Captures decisions and any open items with owners.

---

## Red flags to watch for during onboarding

If any of these surface, pause and discuss with the client before proceeding:

### Access friction
- "We can't give you repo access for security reasons" → the engagement is unworkable; escalate
- "We can give you read access but only for part of the codebase" → scope the engagement to what we can see
- "Access is delayed by corporate IT; kickoff will slip 2 weeks" → adjust timeline, don't start billing until access lands

### People friction
- The executive sponsor declines to name a day-to-day point of contact → scope the engagement to not require one, or escalate
- Interview subjects decline to participate → escalate to executive sponsor; the engagement's value is reduced without interviews
- The engagement is being driven by one person who isn't authorized to make it stick → surface this with client leadership

### Scope friction
- Client asks for deliverables not in SOW during onboarding → change order or decline, don't absorb
- Client asks us to assess "something else too" ("while you're there...") → formal change order
- Client frames the engagement as outsourced execution rather than diagnosis → reset expectations; Phase 1 is a diagnosis, not a rebuild

### Legal friction
- SOW hasn't been countersigned but client wants us to start → don't start
- Invoice terms get renegotiated after countersignature → escalate to partner
- Client requests amendments that substantially change scope → new SOW, not an amendment

## Non-red flags (these are fine)

- Client reschedules kickoff once → happens
- Client asks us to adjust the interview list → that's their right
- Client requests specific deliverable formats (PDF vs. Confluence) → accommodate
- Client asks for a status update we hadn't committed to → provide if trivial; change order if not
- Client wants executive-summary emphasis vs. technical-depth emphasis → adjust during the engagement, the underlying work is the same

---

## Phase 1 day-by-day (reference)

Pulled from `docs/methodology/01-diagnostic.md` for onboarding context:

| Day | Activity | Provider deliverable (end of day) |
|---|---|---|
| 1 | Kickoff, access check, interview scheduling | Kickoff memo |
| 2 | Instrumentation scripts run, initial metrics capture | — |
| 3 | Continued metrics work, first architecture read | — |
| 4-5 | Interviews (2-3 each day), continued analysis | — |
| 6 | Audit synthesis, internal review | — |
| 7 | Pilot longlist | Internal draft |
| 8 | Pilot prioritization, ROI modeling | Internal draft |
| 9 | Draft plan written; shared with executive sponsor for review | Draft PDF |
| 10 | Final plan polished; presentation | Final deliverable + presentation |

## Post-engagement checklist (2 days after Day 10)

- [ ] **Raw interview notes (anonymized) delivered** to client
- [ ] **Repository-level audit reports** delivered
- [ ] **Metrics CSV** delivered
- [ ] **Final invoice (50%) issued**
- [ ] **Engagement retrospective internal** (Provider-only, 30 min)
- [ ] **Anonymized case study draft** written for Provider's methodology updates
- [ ] **Repository archive on Provider side** (engagement repo marked read-only)
- [ ] **Decision from client** on Phase 2 — yes / no / "think about it" — logged in CRM
