# european-energy-software-2026-enriched — deal-team brief

_Generated 2026-04-21 · Solstein v2 · 13 companies._

## Context

Enriched European energy software universe. 12 companies with fields populated from verified public sources (PitchBook, Crunchbase, Owler, company press releases, GitHub). Every field was individually verified 2026-04-21. Use this universe for sample Solstein runs and the deal-team brief example.

## Executive observations

- **Scored: 5 of 13 (38%).** 8 companies had insufficient real signal to score honestly and are listed with their completeness but no composite.

- **Tier distribution (of scored):** 1 diamond, 3 lead, 1 salt.

- **High-growth candidates (YoY ≥ 25%):** Kraken Technologies (+68%), 1KOMMA5 (+36%).

- **Contracting (negative YoY, may indicate consolidation or distress):** Otovo (-38%), Enpal (-5%).

- **Highest revenue/employee:** Otovo at €3M/head — signal of tech-leveraged business model.

- **Lowest revenue/employee (of scored):** Kraken Technologies at €43K/head — likely installer-heavy or service-heavy (higher operational complexity, lower software margins).

- **GitHub visibility:** 6 of 13 companies have a public org (['1K5-TECH', 'octoenergy', 'otovo', 'tibber', 'NextKraftwerke', 'sonnen']).

- **Country distribution:** DE: 6, GB: 2, NO: 2, SE: 2, NL: 1.

## Tier analysis

**Phoenix and Diamond tier companies** combine strong growth signals with healthy productivity. These are typically acquisition candidates or top transformation partners — already running well, where AI augmentation delivers incremental gains on an already-solid foundation.

**Lead tier (3 companies)** have partial signal and mid-band scores. From a transformation-targeting lens, this is actually the highest value cohort: the companies where AI-native rebuild delivers the largest delta. The Solstein v1→v2 case study itself was a lead-tier target before transformation.

**Salt tier (1 companies)** score below baseline — negative growth, weak productivity, or both. For transformation engagements, these carry execution risk: the underlying business may be structurally challenged, in which case no amount of AI-native modernization will fix the root issue. Diligence before pursuing.

**Significant unknown bucket (8, 62% of universe)** — most of these are private companies that aren't on GitHub, aren't publicly listed, and haven't disclosed financials. A deeper enrichment run (Crunchbase / LinkedIn Talent Insights) or direct outreach would resolve most of them.

## Top candidates (detail)

### 1. 1KOMMA5 — **diamond** (6.73/10)

- **Country:** DE  · **Founded:** 2021  · **Website:** https://1komma5.com/
- **Revenue:** €520M  · **Employees:** 3000  · **Rev/head:** €173K  · **YoY:** +36%
- **Sub-scores:** growth 10.00 / financial health 3.47 / AI maturity —
- **Completeness:** 60%  · **GitHub:** 1K5-TECH  · **Ticker:** private

### 2. Eneve — **lead** (5.97/10)

- **Country:** NL  · **Founded:** 1997  · **Website:** https://eneve.com/
- **Revenue:** €30M  · **Employees:** 130  · **Rev/head:** €231K  · **YoY:** +22%
- **Sub-scores:** growth 7.33 / financial health 4.62 / AI maturity —
- **Completeness:** 60%  · **GitHub:** —  · **Ticker:** private

### 3. Kraken Technologies — **lead** (5.43/10)

- **Country:** GB  · **Founded:** 2010  · **Website:** https://kraken.tech/
- **Revenue:** €108M  · **Employees:** 2500  · **Rev/head:** €43K  · **YoY:** +68%
- **Sub-scores:** growth 10.00 / financial health 0.86 / AI maturity —
- **Completeness:** 60%  · **GitHub:** octoenergy  · **Ticker:** private

### 4. Otovo — **lead** (5.00/10)

- **Country:** NO  · **Founded:** 2015  · **Website:** https://www.otovo.com/
- **Revenue:** €623M  · **Employees:** 209  · **Rev/head:** €3M  · **YoY:** -38%
- **Sub-scores:** growth 0.00 / financial health 10.00 / AI maturity —
- **Completeness:** 60%  · **GitHub:** otovo  · **Ticker:** OTOVO.OL

### 5. Enpal — **salt** (2.46/10)

- **Country:** DE  · **Founded:** 2017  · **Website:** https://www.enpal.com/
- **Revenue:** €860M  · **Employees:** 3500  · **Rev/head:** €246K  · **YoY:** -5%
- **Sub-scores:** growth 0.00 / financial health 4.91 / AI maturity —
- **Completeness:** 60%  · **GitHub:** —  · **Ticker:** private

## Full ranking

| # | Company | Tier | Score | Growth | Fin.Health | AI | Rev/head | Completeness |
|---|---|---|---|---|---|---|---|---|
| 1 | 1KOMMA5 | diamond | 6.73 | 10.00 | 3.47 | — | €173K | 60% |
| 2 | Eneve | lead | 5.97 | 7.33 | 4.62 | — | €231K | 60% |
| 3 | Kraken Technologies | lead | 5.43 | 10.00 | 0.86 | — | €43K | 60% |
| 4 | Otovo | lead | 5.00 | 0.00 | 10.00 | — | €3M | 60% |
| 5 | Enpal | salt | 2.46 | 0.00 | 4.91 | — | €246K | 60% |
| 6 | Tibber | unknown | — | — | 1.81 | — | €91K | 40% |
| 7 | Next Kraftwerke | unknown | — | — | — | — | unknown | 20% |
| 8 | Sonnen | unknown | — | — | — | — | unknown | 20% |
| 9 | Lichtblick | unknown | — | — | 10.00 | — | €2M | 40% |
| 10 | Greenely | unknown | — | — | — | — | unknown | 20% |
| 11 | Ostrom | unknown | — | 10.00 | — | — | unknown | 40% |
| 12 | Svea Solar | unknown | — | — | 2.86 | — | €143K | 40% |
| 13 | Kiwi Power | unknown | — | — | — | — | unknown | 20% |

## Methodology note

Scoring: composite = 0.4·growth + 0.4·financial_health + 0.2·AI_maturity, computed only when at least 2 of 3 signals are available. Classification (scoring/thresholds.py): phoenix ≥ 8.0, diamond ≥ 6.0, lead ≥ 4.0, salt below. Missing signals are reported as `None` — never defaulted to 0.

This brief is produced deterministically from the scored universe. It contains no LLM-generated text; every observation is derived from the numeric output of `solstein run`.

