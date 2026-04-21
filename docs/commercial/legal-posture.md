# Legal and corporate posture

> **Current state: NOT READY FOR EXTERNAL ENGAGEMENTS.** This document tracks the known gaps between AI-Whisperers' current corporate/legal posture and what a mid-market European PE firm would require before countersigning a services agreement. It is the pre-send checklist for anything commercial.

## Why this document exists

The critic review (2026-04-21) surfaced that the commercial package does not disclose legal entity, jurisdiction, insurance, or data-processing posture to a prospective EU counterparty. This is the first thing a PE firm's General Counsel asks for when a new consultancy is introduced. Without answers, no mid-market PE firm in the Benelux will countersign a services agreement — full stop. This is not an optional gap.

Filling the gaps below requires decisions and spend that sit with the firm's principals, not with the AI-augmented documentation workflow. They are called out here so nobody pretends they're closed when they aren't.

## Required: resolved before any counterparty conversation

### L1 — Operating legal entity in EU or aligned jurisdiction

**Current state:** AI-Whisperers is Paraguay-based.
**Gap:** A Dutch PE firm cannot enter a services agreement with a Paraguay entity without significant additional friction — data transfers governed by GDPR Article 46 (standard contractual clauses), withholding-tax implications, sanctions screening complexity, local-counsel overhead.
**Options:**
- (a) Establish an EU entity (Netherlands BV, Ireland DAC, Estonia OÜ) with AI-Whisperers Paraguay as the parent. Cost: €3-8K in legal fees + €1-2K/year ongoing administration.
- (b) Engage through an existing EU-domiciled partner that handles the contract while we do the work underneath. Faster, but gives away margin and complicates liability.
- (c) Stay Paraguay-only and accept a narrower addressable market (EU PE firms that will work with non-EU counterparties at all).
**Required decision:** founders' call. Not automatable.

### L2 — Professional liability / Errors & Omissions insurance

**Current state:** None disclosed or purchased.
**Gap:** Standard for consulting engagements involving software recommendations is E&O coverage of €1-5M aggregate. Many mid-market PE firms require proof of coverage before engagement.
**Cost:** €1,500-4,000/year for €1-2M coverage, depending on jurisdiction and claims history.
**Required decision:** purchase before any engagement touching production-adjacent systems.

### L3 — General commercial liability

**Current state:** None disclosed.
**Gap:** Separate from E&O, covers on-site incidents, data breach, and third-party claims. Often bundled with E&O.
**Cost:** €500-1,500/year.
**Required decision:** purchase alongside E&O.

### L4 — GDPR data-processing posture

**Current state:** Undefined.
**Gap:** Every engagement involves reading client code, ticket data, and possibly customer records. EU GDPR requires:
- Data-processor agreement (DPA) between us (as processor) and the client (as controller)
- Record of processing activities
- Subprocessor disclosure (if we use Claude API, AWS, Google Drive, etc.)
- Data-breach notification procedures
- Data-residency commitments (EU data stays in EU, or adequate-country equivalents)
- Right-to-be-forgotten procedures
**Artifacts needed:**
- DPA template (EU-approved standard)
- Subprocessor register
- Data-flow diagram for typical engagements
- Breach-response procedure
**Cost:** 4-8 hours of GDPR-qualified counsel + internal documentation. ~€2-5K one-time; ongoing maintenance minimal.

### L5 — Anti-Money-Laundering / KYC / Sanctions

**Current state:** Undefined.
**Gap:** For equity-inclusive engagements (Phase 3), and for any payments above certain thresholds, counterparty due-diligence is required. We should have a documented AML/KYC process for the firms we work with.
**Cost:** Mostly procedural; ~€1-2K for legal template plus internal training.

### L6 — IP / work-for-hire structure

**Current state:** The SOW template says *"deliverables are property of Client upon final payment"* and *"provider retains ownership of the methodology."*
**Gap:** The line between "deliverable IP" (client's) and "methodology IP" (ours) must hold up to legal scrutiny. Some clients will want broader IP assignment; our terms should anticipate and push back. Also: joint-IP scenarios (e.g., a prompt library fine-tuned on client code) need explicit handling.
**Artifact needed:** IP policy document, reviewed by counsel, aligned with SOW template.

## Required: resolved before multi-year / portfolio engagements

### L7 — Sub-contractor / sub-processor arrangements

If we ever subcontract work (additional engineers from a network, translation, design, legal), each sub-contractor must be flowed-down our GDPR, confidentiality, and IP terms.
**Artifact needed:** Sub-contractor agreement template.

### L8 — Equity-holding entity (for Phase 3)

Phase 3 equity-inclusive engagements require us to hold equity as an entity. Personal/founder holdings are simpler but tax-inefficient and do not survive founder turnover.
**Cost:** if L1 produces an EU entity, equity can be held there. Otherwise: small additional structuring decision.

### L9 — Professional indemnity for named individuals

If specific engineers or partners are named in SOWs as engagement leads, personal-indemnification arrangements should be clear (employment contract, consulting agreement, company indemnification). Not urgent but matters as the team grows.

## Required: resolved before high-stakes engagements (utility billing, regulated systems)

### L10 — Higher liability caps than standard templates

Current SOW caps liability at 2× fees (~€50K for Phase 1, ~€100K for Phase 2). For engagements touching systems that handle regulated utility data (Vattenfall, Essent, BASF via Eneve's pipeline), this cap is indefensibly low. Expect counterparty to demand €500K-2M liability cap; price accordingly.

### L11 — Industry-specific compliance

If we work with energy-sector software, we need at minimum an awareness of:
- EU energy market regulations (EED, ACER, etc.)
- Critical infrastructure directive (NIS2) implications for the software
- Sector-specific data obligations
- Expected certifications for service providers

**Artifact needed:** One-pager per sector we operate in, written by someone with that sector's context. Not yet produced.

### L12 — Critical infrastructure access controls

Energy software touches critical infrastructure. Any read-access we receive is subject to heightened audit scrutiny. Our access-management, session-logging, and departure procedures need to exist and be documented before a regulated client grants access.

## Required: resolved before security-conscious engagements

### L13 — SOC 2 Type II or ISO 27001

**Current state:** None.
**Gap:** Enterprise clients increasingly require one or both. Neither is trivial — SOC 2 Type II is a 6-12 month process costing €30-80K. ISO 27001 is comparable.
**Decision:** most mid-market PE firms will not require SOC 2 initially but will ask as engagement depth grows. Decision point: begin the SOC 2 process after the first 2-3 paid engagements, when the revenue justifies the investment.

### L14 — Security policy set

Documented baseline:
- Access control policy
- Incident response plan
- Secure development lifecycle
- Vendor/sub-processor assessment
- Breach notification procedure
- Data retention & disposal
- Device security policy
- Remote-work security

**Current state:** None exist as formal documents.
**Cost:** 2-4 days of writing against a template, probably €1-3K if outsourced to a security consultant.

## The honest commercial gate

Until L1, L2, L3, L4 are resolved, **do not enter external commercial conversations**. Any engagement that would be signed under current conditions leaves the firm exposed in ways that a single claim could collapse.

Until L10, L13, L14 are either resolved or explicitly out of scope (via a narrower engagement framing), **do not engage with energy-sector or regulated-industry clients** — which means Eneve / Vortex is out of scope for this posture.

## Summary of cost + timeline to "ready"

| Requirement | Estimated cost | Timeline | Blocker |
|---|---|---|---|
| L1 (EU entity) | €3-8K + €1-2K/yr | 6-12 weeks | Founders' decision |
| L2 + L3 (insurance) | €2-5K/yr | 2-4 weeks | Need L1 for EU insurer |
| L4 (GDPR posture) | €2-5K one-time | 2-3 weeks | Can parallel with L1 |
| L5 (AML/KYC) | €1-2K | 1-2 weeks | Low blocker |
| L6 (IP policy) | Included in L4 | 1 week | Low blocker |
| L10 (liability caps) | Legal review cost | Same as SOW review | Low blocker |
| L11 (sector-specific) | TBD | 2-4 weeks | Needs sector expertise |
| L14 (security policies) | €1-3K | 2-3 weeks | Can parallel |
| L13 (SOC 2 / ISO 27001) | €30-80K | 6-12 months | Defer until revenue supports |

**Minimum readiness for first external motion:** L1, L2, L3, L4, L5, L6, L10, L14. Roughly €10-20K one-time + €4-8K/year + 10-14 weeks.

This is not an AI-automatable workflow. It needs a human owner and counsel.

## Related

- `docs/commercial/phase-1-sow-template.md` — currently leaves `{JURISDICTION}` unresolved
- `docs/commercial/portfolio-partnership-agreement-template.md` — same
- `docs/commercial/equity-term-sheet-template.md` — flagged "LEGAL REVIEW REQUIRED BEFORE USE"
- `docs/critique/2026-04-21-hostile-review.md` — where these gaps were surfaced
