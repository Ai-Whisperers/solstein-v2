# Phase 1 Statement of Work — AI-native transformation diagnostic

> *Template. Replace `{CLIENT}` blocks and populate the scope section before sending.*

**Provider:** AI-Whisperers
**Client:** `{CLIENT_LEGAL_NAME}`
**Effective date:** `{DATE}`
**Engagement:** AI-native transformation diagnostic — Phase 1

---

## 1. Purpose

Client engages Provider to assess Client's engineering organization and codebase, identify where AI-native transformation would deliver the greatest measurable lift in velocity, quality, and cost, and deliver a prioritized transformation plan.

This SOW covers Phase 1 (the diagnostic) only. Any subsequent transformation work (pilots, broader engagement, equity arrangements) is governed by a separate agreement.

## 2. Scope

### In scope
- Codebase audit: one primary repository, optionally up to two adjacent repositories if the dependency structure requires
- Architecture interviews: up to 4 × 1-hour interviews with senior engineers nominated by Client
- Delivery-signal analysis: review of CI logs, ticket history (Jira/Linear/GitHub issues), deploy history, incident reports (last 6 months)
- Written transformation plan with prioritized pilots
- One final presentation (virtual, 90 minutes, recorded)

### Out of scope
- Production access, write access to any Client system
- Any modification of Client code or infrastructure
- Employee evaluations or HR assessments
- Legal, compliance, or security audits (we will flag concerns but do not provide formal opinions on these)
- Work beyond the time and scope listed here

## 3. Deliverables

| # | Deliverable | Format | Due |
|---|---|---|---|
| 1 | Kickoff memo | PDF, 2 pages | End of Day 1 |
| 2 | Baseline metrics snapshot | PDF + CSV | End of Day 5 |
| 3 | Transformation plan | PDF, 15-20 pages | End of Day 9 |
| 4 | Final presentation | Virtual, recorded | Day 10 |
| 5 | Raw interview notes (anonymized) | PDF | Within 2 days after presentation |

All deliverables are property of Client upon final payment. Provider retains the right to produce anonymized case studies (no Client name, no identifying details) from the engagement.

## 4. Timeline

Two calendar weeks, beginning within 10 business days of SOW countersignature. Detailed day-by-day breakdown in the methodology playbook Chapter 1 (provided upon request).

## 5. Fees and payment

**Fixed fee: €25,000** (twenty-five thousand euros), inclusive of all Provider labor, tools, and incidentals.

Payment schedule:
- 50% (€12,500) upon SOW countersignature, within 14 days of invoice
- 50% (€12,500) upon delivery of the final presentation, within 14 days of invoice

Late payment: statutory rate per EU Directive 2011/7/EU on combating late payment.

Expenses over €500 (travel, specialist tools) require prior written approval and are billed at cost.

## 6. Team

Provider will assign:
- 1 × Lead (senior engineer, direct diagnostic work)
- 1 × Partner (oversight, presentation co-lead, signs off on the plan)

Total capacity allocated: 2 people × 2 weeks = ~160 person-hours.

## 7. Client responsibilities

Client agrees to provide, within 2 business days of kickoff:
- Read access to the primary repository (and up to 2 adjacent repos if needed)
- Read access to CI logs / workflow run history for the last 6 months
- Read access to ticket tracker (last 12 months)
- Introductions to the 4 interview subjects
- A named day-to-day point of contact authorized to answer practical questions
- A meeting room / video bridge for the final presentation

Delays in Client-side access extend the timeline by the equivalent number of business days. Each such delay is a change of scope under §10.

## 8. Confidentiality

Each party will treat the other's non-public information as confidential. Provider's obligation survives for 3 years from the termination of the engagement. Client information will not be used to train AI models or shared with third parties without written consent.

Provider may produce anonymized case studies from the engagement (no Client name, no identifying product or market details) for its own marketing purposes.

## 9. IP and licensing

All deliverables produced under this SOW are delivered to Client under a perpetual, worldwide, non-exclusive license for Client's internal use. Provider retains ownership of the methodology (the frameworks, scoring rubrics, and templates used to produce the deliverable) and may reuse it with other clients.

Any tooling Provider writes during the diagnostic (e.g., custom analysis scripts) is delivered under the MIT license.

## 10. Change orders

Any change to scope, timeline, or fee requires a written change order signed by both parties. Scope-expanding change orders are billed at €1,800 / person-day.

## 11. Warranties

Provider warrants that the diagnostic will be performed with the skill and care reasonably expected of a professional engineering consultancy. Provider makes no warranty as to future business outcomes — the plan is a recommendation informed by evidence, not a guarantee of results.

**The diagnostic has standalone value.** If Client chooses not to proceed with Provider to Phase 2 (transformation pilots), Client retains the full deliverable and owes nothing beyond the fixed fee. This design is intentional: we charge for the diagnostic alone so that our recommendation is not biased by downstream revenue.

## 12. Termination

Either party may terminate for material breach with 10 business days' written notice and opportunity to cure.

If Client terminates for convenience, Client pays for work performed up to the termination date, pro-rated based on deliverable completion.

## 13. Liability

Provider's total aggregate liability under this SOW is capped at 2× the fees paid. Neither party is liable for indirect, consequential, or punitive damages.

## 14. Governing law

This SOW is governed by `{JURISDICTION}` law. Any dispute is subject to the exclusive jurisdiction of `{JURISDICTION}` courts.

---

## Signatures

| | |
|---|---|
| For Client | For Provider (AI-Whisperers) |
| Name: | Name: |
| Title: | Title: |
| Date: | Date: |
| Signature: | Signature: |

---

## Appendix A — fee math (internal only, not shared with Client)

Target: profitable at €25K flat.

| Line item | Cost |
|---|---|
| Lead engineer: 10 working days | €6,500 |
| Partner: 4 working days (oversight + presentation) | €4,800 |
| Total direct labor | €11,300 |
| Tooling / API costs | €300 |
| Overhead allocation (25%) | €2,900 |
| **Total cost** | **€14,500** |
| **Fee** | **€25,000** |
| **Gross margin** | **€10,500 (42%)** |

Adjust rates and partner allocation for local market conditions. If local effective billing rates would push cost above ~€18K, raise the fee to €30-35K rather than cutting scope.
