# Security posture

> **Current state: NOT READY FOR EXTERNAL ENGAGEMENTS that require security-assessed vendors.** Tracks the gap between AI-Whisperers' current security posture and what enterprise clients demand.

## What enterprise clients ask for

Before granting any read access (repos, CI logs, tickets), a typical mid-market enterprise client asks:

1. Do you have SOC 2 Type II or ISO 27001?
2. What is your access control policy for client data?
3. What subprocessors do you use?
4. How do you handle incidents / breaches?
5. What happens to our data when the engagement ends?
6. Do you have secure development practices documented?
7. What's your vendor security review cadence?

Without answers, enterprise IT blocks the engagement. This is not negotiable.

## Current state

### S1 — SOC 2 / ISO 27001

**Status:** None.
**Gap:** Many enterprise clients require one before engagement. Mid-market PE portfolio companies vary — some are stricter than others.
**Decision:** Defer formal certification until revenue supports it (SOC 2 Type II = ~€40-70K, 6-12 months). Meantime, produce a "SOC 2 alignment" document showing which controls we meet and which we don't — gives enterprise-lite clients something to review.

### S2 — Access control policy

**Status:** Implicit in how we work; not documented.
**Gap:** Who at AI-Whisperers can access what client data, under what authorization, with what logging? Not written down.
**What to produce:**
- Named engagement team per client (who has access, when access was granted, by whom)
- Single-sign-on requirement for all client system access
- Multi-factor authentication required for all engagement access
- 90-day access review
- Same-day access revocation on engagement end or team changes

### S3 — Subprocessor register

**Status:** None documented.
**Gap:** Every engagement uses external services: Claude API (for code generation and review), GitHub (for code hosting), Google Drive / Notion (for documents), email providers, etc. Each is a subprocessor that must be disclosed to the client before engagement.
**What to produce:** A subprocessor register listing:
- Service name
- Purpose (what data flows through it)
- Location of processing
- DPA status with that subprocessor
- Alternative if client objects

### S4 — Incident response plan

**Status:** None.
**Gap:** If we discover a breach of client data, or a breach of our own infrastructure affecting client data, what do we do in the first 24 hours?
**What to produce:**
- Breach definition and severity classification
- Immediate containment steps
- Client notification timeline (within 24 hours of confirmed breach)
- Regulatory notification obligations (GDPR requires 72-hour notification to DPA)
- Remediation procedures
- Post-incident review template

### S5 — Secure development lifecycle

**Status:** Ad-hoc.
**Gap:** Clients want evidence that the code we *write for them* is secure — input validation, dependency scanning, secrets management, least-privilege defaults. And the code we write for them *never leaves their environment* unless they approve.
**What to produce:**
- Coding standards document (part of this is in `docs/methodology/09-quality-gates.md`)
- Dependency vulnerability scanning (Dependabot on every repo)
- Secrets management (no secrets committed; we use env vars + a documented vault)
- Code review requirement (no merges without review)

### S6 — Data retention and disposal

**Status:** None.
**Gap:** When an engagement ends, what happens to the client's data we've read? Do we keep copies? If so, where, for how long, under what protection, and when do we destroy them?
**What to produce:** A policy that commits to:
- Default: all engagement data destroyed within 30 days of engagement end
- Exception: data retained for case-study purposes requires written client consent, anonymized, stored in a separate protected location
- Certificate of destruction on request

### S7 — Device security

**Status:** Ad-hoc.
**Gap:** Our team works on laptops. Are those laptops encrypted? Password-protected? Patched? Locked when unattended? Do they connect to client systems only over VPN?
**What to produce:**
- Device inventory
- Mandatory FDE (full-disk encryption), auto-lock, patch cadence
- Mobile device management if team grows beyond 3-4 people

### S8 — Third-party AI tool usage

**Status:** We use Claude API extensively.
**Gap:** Client data passing through Claude API. Claude's data usage policy matters (by default, API usage is not used for model training; confirm this status for our API plan).
**What to produce:** Explicit documentation for clients: *"We use Anthropic Claude API under a zero-retention configuration. Your data is not used to train models and is not retained by Anthropic beyond the API call."*
This is accurate for Claude API with the standard business-tier configuration; confirm in writing with Anthropic before representing it to clients.

## "SOC 2 alignment" document

A pragmatic pre-certification document that answers the enterprise IT questionnaire:

> *"We do not have SOC 2 Type II certification at this time. We expect to pursue it during our first year of enterprise engagements. Meantime, we align our practices to the following SOC 2 controls:*
> *- CC1: Control Environment — documented roles, responsibilities, and access policies*
> *- CC2: Communication and Information — documented procedures, incident response*
> *- CC6: Logical and Physical Access — MFA, SSO, least privilege, access reviews*
> *- CC7: System Operations — change management, monitoring*
> *- PI1: Processing Integrity — code review, CI/CD gates"*

This won't satisfy a strict-compliance client. It will satisfy a reasonable mid-market client. Produce it, keep it current.

## Minimum viable posture before any engagement

Even without SOC 2, the following must be documented and live:

- [ ] Written access control policy (S2)
- [ ] Subprocessor register (S3)
- [ ] Incident response plan (S4)
- [ ] Data retention / disposal policy (S6)
- [ ] Device security baseline (S7)
- [ ] Claude API zero-retention documentation (S8)
- [ ] SOC 2 alignment document (above)

Estimated effort: 3-5 days of focused writing by someone competent, plus review. €2-5K if outsourced to a security consultant. Cheap relative to the commercial gate it unblocks.

## Related

- `docs/commercial/legal-posture.md` — legal side of the same gap
- `docs/commercial/phase-1-sow-template.md` — engagement framework that depends on this
