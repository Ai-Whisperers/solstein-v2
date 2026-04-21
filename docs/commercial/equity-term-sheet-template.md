# Equity-inclusive Phase 3 engagement — term sheet template

> ⚠️ **LEGAL REVIEW REQUIRED BEFORE USE.** This template is engineering-drafted for structural clarity. It is **not** a substitute for counsel review in the governing jurisdiction. Equity compensation structures have material tax, securities-law, and cap-table implications that vary significantly by jurisdiction (NL, DE, FR, GB, ES each have distinct rules on warrants, ESOP, phantom equity). Do not send this template to a counterparty without counsel review first.
>
> **When it's appropriate:** Phase 3 engagements sized above €250K cash-equivalent, where the client is prepared to exchange cash discount for equity alignment. Default position remains cash. Equity structures are the exception, not the rule.

---

**Provider:** AI-Whisperers
**Client company:** `{CLIENT_LEGAL_NAME}` ("Company")
**PE sponsor (if applicable):** `{PE_FIRM}`
**Effective date:** `{DATE}`
**Engagement:** Phase 3 AI-native transformation — full engagement

---

## 1. Structure overview

This term sheet describes a Phase 3 engagement compensated through a hybrid of reduced cash fees and equity in `{CLIENT}`. It is subject to execution of a definitive services agreement, a definitive equity issuance agreement, and all required cap-table approvals.

| Component | Value |
|---|---|
| **Total engagement cost to Company** | Approximately €`{X}` cash-equivalent over `{N}` months |
| **Cash portion** | `{X}`% of total (paid monthly) |
| **Equity portion** | `{Y}`% of total (vested over engagement, see §4) |
| **Total engagement duration** | `{6-12}` months |
| **Team committed from Provider** | `{N}` full-time engineers + `{M}` part-time partners |

## 2. Scope of work

(High-level; definitive services agreement will contain full SOW.)

Provider will deliver an AI-native transformation engagement covering:

- Baseline measurement and diagnostic refresh
- Execution of `{N}` transformation pilots over the engagement
- Team training and methodology transfer
- Ongoing coaching and pair-programming support
- Metrics instrumentation and reporting
- Executive communication and sponsor alignment

Deliverables and milestones are specified in the definitive services agreement. Milestones are directly linked to equity vesting (§4.3).

## 3. Cash compensation

Cash portion: **€`{CASH_TOTAL}`**, paid in monthly installments of **€`{CASH_MONTHLY}`**.

Payment terms: 14-day net. Invoices issued on the last business day of each month. Late payment per EU Directive 2011/7/EU.

Cash is paid regardless of equity vesting outcomes. If Provider terminates early for Provider's convenience, cash already invoiced becomes due pro-rata. If Company terminates early for convenience, Company pays for work performed up to termination date.

## 4. Equity compensation

### 4.1 Instrument
`{One of: Warrants / Stock options / Phantom equity / Direct common equity}`

**Warrants:** recommended default. Tax-neutral at issuance in most jurisdictions. Less complex than direct equity issuance. Can be exercised on a liquidity event or at a defined strike price.

**Stock options:** appropriate if Company has an existing ESOP; Provider's equity is granted from the ESOP pool per its terms.

**Phantom equity:** appropriate if Company wants to preserve cap-table simplicity. Provider receives cash equivalent of the equity's value at liquidity event, no actual share ownership.

**Direct common equity:** appropriate if Company is private and can accept a new shareholder. Dilution calculated on fully-diluted basis.

### 4.2 Size
Equity portion: **`{X}`% fully-diluted equity** in `{CLIENT}`, or the equivalent warrant/option structure pricing to the same fully-diluted position at current round valuation.

Default cap: **1.5% fully-diluted per engagement**. Higher percentages require partner-level approval and extended engagement duration.

Valuation reference: Company's most recent funded round (for private companies) or 20-day VWAP (for public). If neither is available, a mutually-agreed independent valuation within 90 days of effective date.

### 4.3 Vesting
Vesting is **milestone-based**, not time-based. Structure:

| Milestone | % of equity vested |
|---|---|
| Baseline metrics captured + transformation plan signed off by Company | 10% |
| First pilot success criteria met | 20% |
| Second pilot success criteria met | 20% |
| Third pilot success criteria met | 20% |
| Final engagement outcomes report approved by Company exec team + PE sponsor | 30% |

Success criteria for each pilot are defined in the definitive services agreement, signed off by both parties, and verified by mutually-agreed instrumentation (Provider cannot unilaterally declare success).

### 4.4 Acceleration on exit
If Company undergoes a change of control event (acquisition, IPO, merger) during the engagement, unvested equity vests immediately at the value determined by the transaction, subject to:

- Provider having completed at least the first milestone
- Company not being in material breach of the services agreement

### 4.5 Right of first offer / preferred-share protections
Provider's equity shall carry standard tag-along rights, pro-rata participation in future rounds, and information rights consistent with other minority shareholders at similar stake levels. Provider does not seek a board seat.

### 4.6 Vesting cliff and forfeiture
If Provider terminates the engagement for Provider's convenience before the 2nd milestone, all unvested equity is forfeited. If Company terminates for Company's convenience, Provider retains equity already vested plus a pro-rated portion of the then-current milestone, as determined by an independent assessor.

Termination for cause (material breach) forfeits any unvested equity.

## 5. Scope of Provider's commitment

Over the engagement period, Provider commits:

- `{N}` dedicated full-time engineers (named individuals, substitution with 30 days' notice)
- `{M}` part-time partners for oversight, executive communication, and PE sponsor liaison
- Priority access to Provider's methodology and tooling
- Monthly executive briefings with Company leadership
- Quarterly briefings with PE sponsor (if applicable)

## 6. Information rights and reporting

### 6.1 What Provider gets
For the duration of the engagement:
- Read access to Company repositories, CI/CD logs, ticket trackers (under mutual confidentiality)
- Access to engineering leadership for decision-making
- Access to financial metrics relevant to engagement ROI tracking (engineering cost, delivery frequency, etc.)
- Access to PE sponsor's investment thesis and operating plan (if applicable)

Provider does not seek access to customer data, payroll, or materials beyond what's required for engagement delivery.

### 6.2 What Company / sponsor gets
- Monthly engagement progress report (first week of each month)
- All code/artifacts produced under the engagement, licensed per §8
- Baseline + final metrics report (the engagement's "before/after" document)
- Methodology handover documents for Company to continue the transformation independently post-engagement

## 7. Confidentiality and IP

### 7.1 Confidentiality
Each party holds the other's non-public information as confidential. Obligations survive 5 years post-termination.

Company data does not train AI models used beyond the engagement.

### 7.2 IP in deliverables
All code and artifacts produced under the engagement are owned by Company. Company grants Provider a perpetual, worldwide, non-exclusive license to reference the work anonymously in case studies.

### 7.3 Methodology IP
Provider retains ownership of the transformation methodology (playbook, scoring rubrics, diagnostic templates, prompt library) used during the engagement. Company's use of the methodology is limited to Company's internal operations for the duration of the engagement and for 2 years thereafter.

## 8. PE sponsor provisions

(Delete this section if there is no PE sponsor involved.)

`{PE_FIRM}` has reviewed and consented to this engagement structure, including the equity issuance. `{PE_FIRM}` is not a party to this agreement but receives:
- Copies of all engagement progress reports
- Notification of all milestone completions
- A seat at the final engagement outcomes review

`{PE_FIRM}` agrees the equity structure does not trigger any change-of-control or preemptive-rights provisions in existing agreements.

## 9. Warranties

Provider warrants that services will be performed with skill and care reasonably expected of a professional engineering firm. Provider makes no guarantees as to future business outcomes or valuation — equity value at any point depends on Company's broader performance.

## 10. Dispute resolution

Disputes escalated through (a) good-faith discussion between named executives, (b) non-binding mediation, and (c) binding arbitration under `{ARBITRATION_RULES}` before litigation.

## 11. Governing law

`{JURISDICTION}` law. `{JURISDICTION}` courts, exclusive jurisdiction for any matter not resolved through §10.

---

## Signatures

| | |
|---|---|
| For `{CLIENT}` | For AI-Whisperers |
| Name: | Name: |
| Title: | Title: |
| Date: | Date: |
| Signature: | Signature: |

| For `{PE_FIRM}` (consent) | |
| Name: | |
| Title: | |
| Date: | |
| Signature: | |

---

## Appendix A — Structural options (internal drafting aid)

Choose ONE:

### Option 1 — Warrant (recommended default)
Provider receives a warrant to purchase `{X}`% fully-diluted common equity at a strike price of `{STRIKE}`. Warrant term: 10 years. Exercisable on any liquidity event or on net exercise basis any time after the engagement completes.

**Pros:** tax-neutral at issuance; no actual share ownership; cap-table stays clean; flexibility.
**Cons:** requires strike price setting (subject to valuation); may not exercise if liquidity event valuation is below strike.

### Option 2 — Stock options via existing ESOP
Provider's engineers receive options through Company's ESOP. Subject to ESOP plan terms.

**Pros:** uses existing mechanism; aligns Provider's engineers with Company's employees.
**Cons:** typically requires engineers to be treated similarly to employees for tax purposes; Provider (the firm) doesn't own the options.

### Option 3 — Phantom equity
Provider receives a cash payment equal to `{X}`% of Company's enterprise value at a future liquidity event or at a defined calculation point.

**Pros:** no actual share issuance; simplest cap-table impact; works for ESOP-less companies.
**Cons:** tax treatment varies; Provider's upside capped if phantom equity is paid out on an event-triggered basis that doesn't match Provider's optimal exit.

### Option 4 — Direct common equity
Provider receives newly-issued common shares equal to `{X}`% fully-diluted ownership.

**Pros:** genuine alignment; Provider is a shareholder.
**Cons:** requires full issuance formalities; shareholder rights provisions; may trigger preemptive rights in existing agreements.

## Appendix B — Economic modeling (internal only)

For a Phase 3 engagement with total cost €500K cash-equivalent and 1.5% equity:

| Scenario | Company exit value | 1.5% stake value | Provider net |
|---|---|---|---|
| No exit | — | €0 | Cash portion only (e.g., €300K) |
| Modest exit (3×) | €100M | €1.5M | €300K cash + €1.5M equity = €1.8M |
| Good exit (5×) | €250M | €3.75M | €300K cash + €3.75M equity = €4.05M |
| Exceptional (10×) | €1B | €15M | €300K cash + €15M equity = €15.3M |

Risk-adjusted expected value: typically the cash portion + 20-40% of modeled upside. Structure Provider's fee ratios to ensure cash portion alone remains profitable — equity upside is the bonus, not the business.

## Appendix C — Items that must be legally reviewed before send

- Jurisdiction-specific enforceability (NL BV, UK Ltd, DE GmbH, etc. have different equity-issuance requirements)
- Tax treatment of equity to Provider (is Provider a legal entity? which jurisdiction?)
- Securities-law implications (is the instrument an offering that requires prospectus?)
- Interaction with existing cap-table agreements (preemptive rights, tag-along, anti-dilution)
- Anti-money-laundering / KYC obligations
- Treatment on change of control (acceleration clauses, drag-along)
- Recovery on Provider default vs. Company default
- Labor-law implications if structured through ESOP
