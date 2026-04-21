# Business context (why this tool exists)

## What AI-Whisperers actually sells

**Equity-for-transformation**: we take equity in PE portfolio companies in exchange for AI-native transformation services — modernized CICD, ticket lifecycle automation, refactoring-with-AI, quality gates, standardized libraries.

The commercial partner is the PE firm, not the portco. The portco is the execution environment. The exit-driven upside on the equity stake is how we get paid.

## Where Solstein fits

Solstein is the **prospecting tool for our deal team**. Given a market universe (e.g., a PE firm's current portfolio, or a thematic sector cut), Solstein produces a ranked shortlist: which companies look like good transformation targets, with rationale.

It is **not**:
- a product we sell to PE firms
- a competitive intelligence dashboard for customers
- a replacement for McKinsey

It is internal tooling. The deliverables to customers are **case studies, methodology playbooks, and term sheets** — none of which live in this repo.

## The first proof case: Eneve

- €30M revenue, 130 employees, 22% YoY growth. Dutch energy software.
- Introduced by Michiel Kuiper (PE investor).
- Scored 9.03/10 in v1. That scoring was on partly-synthetic data; we need to re-score with real signals in v2.
- **The critical missing deliverable**: the Eneve case study (STORY-163 in v1's backlog, never started). Before/after metrics on velocity, quality, cost per feature, deploy frequency. This document, not any code, is what closes the next 5 portcos.

## How Solstein accelerates this

1. **Find candidates.** Given a PE firm's portfolio, score and rank which portcos are ripe.
2. **Brief the deal team.** Markdown brief + Excel shortlist → the meeting with the PE partner.
3. **Keep the citation trail.** Every number has a source. No "trust the AI" moments in front of a PE principal.

That is the whole scope.
