"""Analytical narrative generator.

Reads a scored universe and produces a markdown deal-team brief that includes
qualitative observations — not just a ranked table. The observations are
derived deterministically from the scoring output; no LLM in this path.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from solstein.domain import Company, Universe


def _eur(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value >= 1_000_000_000:
        return f"€{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"€{value / 1_000_000:.0f}M"
    if value >= 1_000:
        return f"€{value / 1_000:.0f}K"
    return f"€{value:.0f}"


def _pct(value: float | None) -> str:
    if value is None:
        return "unknown"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.0%}"


def _score(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "—"


def _revenue_per_head_eur(company: Company) -> float | None:
    if company.revenue_eur is None or not company.employees:
        return None
    return company.revenue_eur / company.employees


def _observations(companies: list[Company]) -> list[str]:
    """Generate qualitative bullets from the scored universe."""
    out: list[str] = []
    scored = [c for c in companies if c.composite_score is not None]
    unscored = [c for c in companies if c.composite_score is None]

    total = len(companies)
    scored_pct = f"{len(scored) / total:.0%}" if total else "n/a"
    out.append(
        f"**Scored: {len(scored)} of {total} ({scored_pct}).** "
        f"{len(unscored)} companies had insufficient real signal to score honestly and "
        "are listed with their completeness but no composite."
    )

    tier_counts = {"phoenix": 0, "diamond": 0, "lead": 0, "salt": 0}
    for c in scored:
        tier_counts[c.tier] = tier_counts.get(c.tier, 0) + 1
    tier_summary = ", ".join(f"{n} {t}" for t, n in tier_counts.items() if n > 0)
    out.append(f"**Tier distribution (of scored):** {tier_summary}.")

    # Growth outliers
    growers = [c for c in scored if c.growth_yoy is not None and c.growth_yoy >= 0.25]
    if growers:
        names = ", ".join(
            f"{c.name} ({_pct(c.growth_yoy)})"
            for c in sorted(growers, key=lambda x: -(x.growth_yoy or 0))[:3]
        )
        out.append(f"**High-growth candidates (YoY ≥ 25%):** {names}.")

    shrinking = [c for c in scored if c.growth_yoy is not None and c.growth_yoy < 0]
    if shrinking:
        names = ", ".join(f"{c.name} ({_pct(c.growth_yoy)})" for c in shrinking)
        out.append(
            f"**Contracting (negative YoY, may indicate consolidation or distress):** {names}."
        )

    # Revenue-per-employee productivity signal
    productivity = [(c, _revenue_per_head_eur(c)) for c in scored]
    productivity_with_data = [(c, r) for c, r in productivity if r is not None]
    if productivity_with_data:
        productivity_with_data.sort(key=lambda x: x[1] or 0, reverse=True)
        high = productivity_with_data[0]
        out.append(
            f"**Highest revenue/employee:** {high[0].name} at "
            f"{_eur(high[1])}/head — signal of tech-leveraged business model."
        )
        if len(productivity_with_data) > 1:
            low = productivity_with_data[-1]
            out.append(
                f"**Lowest revenue/employee (of scored):** {low[0].name} at "
                f"{_eur(low[1])}/head — likely installer-heavy or service-heavy "
                "(higher operational complexity, lower software margins)."
            )

    # GitHub visibility
    on_github = [c for c in companies if c.github_org]
    out.append(
        f"**GitHub visibility:** {len(on_github)} of {len(companies)} companies have a "
        f"public org ({[c.github_org for c in on_github]})."
    )

    # Country distribution
    by_country: dict[str, int] = {}
    for c in companies:
        if c.country:
            by_country[c.country] = by_country.get(c.country, 0) + 1
    if by_country:
        top_countries = sorted(by_country.items(), key=lambda x: -x[1])[:5]
        country_summary = ", ".join(f"{code}: {n}" for code, n in top_countries)
        out.append(f"**Country distribution:** {country_summary}.")

    return out


def _tier_notes(companies: list[Company]) -> list[str]:
    """Per-tier analytical notes."""
    out: list[str] = []
    phoenix_plus_diamond = [c for c in companies if c.tier in ("phoenix", "diamond")]
    if phoenix_plus_diamond:
        out.append(
            "**Phoenix and Diamond tier companies** combine strong growth signals with "
            "healthy productivity. These are typically acquisition candidates or top "
            "transformation partners — already running well, where AI augmentation "
            "delivers incremental gains on an already-solid foundation."
        )
    lead = [c for c in companies if c.tier == "lead"]
    if lead:
        out.append(
            f"**Lead tier ({len(lead)} companies)** have partial signal and mid-band "
            "scores. From a transformation-targeting lens, this is actually the highest "
            "value cohort: the companies where AI-native rebuild delivers the largest "
            "delta. The Solstein v1→v2 case study itself was a lead-tier target before "
            "transformation."
        )
    salt = [c for c in companies if c.tier == "salt"]
    if salt:
        out.append(
            f"**Salt tier ({len(salt)} companies)** score below baseline — negative "
            "growth, weak productivity, or both. For transformation engagements, "
            "these carry execution risk: the underlying business may be structurally "
            "challenged, in which case no amount of AI-native modernization will fix "
            "the root issue. Diligence before pursuing."
        )
    unknowns = [c for c in companies if c.tier == "unknown"]
    if unknowns:
        pct = len(unknowns) / len(companies)
        if pct > 0.3:
            out.append(
                f"**Significant unknown bucket ({len(unknowns)}, {pct:.0%} of universe)** — "
                "most of these are private companies that aren't on GitHub, aren't "
                "publicly listed, and haven't disclosed financials. A deeper enrichment "
                "run (Crunchbase / LinkedIn Talent Insights) or direct outreach would "
                "resolve most of them."
            )
    return out


def _top_candidates_detail(companies: list[Company], n: int = 5) -> list[str]:
    """Narrative detail for the top N scored candidates."""
    out: list[str] = []
    top = [c for c in companies if c.composite_score is not None][:n]
    if not top:
        return ["_No candidates scored; cannot produce a top-N detail section._"]
    for rank, c in enumerate(top, start=1):
        rph = _revenue_per_head_eur(c)
        out.extend(
            [
                f"### {rank}. {c.name} — **{c.tier}** ({_score(c.composite_score)}/10)",
                "",
                f"- **Country:** {c.country or 'unknown'}  "
                f"· **Founded:** {c.founded_year or 'unknown'}  "
                f"· **Website:** {c.website or 'n/a'}",
                f"- **Revenue:** {_eur(c.revenue_eur)}  "
                f"· **Employees:** {c.employees or 'unknown'}  "
                f"· **Rev/head:** {_eur(rph)}  "
                f"· **YoY:** {_pct(c.growth_yoy)}",
                f"- **Sub-scores:** growth {_score(c.growth_score)} / "
                f"financial health {_score(c.financial_health_score)} / "
                f"AI maturity {_score(c.ai_maturity_score)}",
                f"- **Completeness:** {c.completeness():.0%}  "
                f"· **GitHub:** {c.github_org or '—'}  "
                f"· **Ticker:** {c.ticker or 'private'}",
                "",
            ]
        )
    return out


def write_narrative_brief(
    universe: Universe, path: Path, sponsor_company: str | None = None
) -> None:
    """Write an analytical deal-team brief for `universe` to `path`.

    If `sponsor_company` is provided, the brief is framed for a deal-team
    discussion with a specific target company (appears in the executive summary).
    """
    companies = universe.companies
    lines: list[str] = [
        f"# {universe.name} — deal-team brief",
        "",
        f"_Generated {date.today().isoformat()} · Solstein v2 · {len(companies)} companies._",
    ]
    if sponsor_company:
        lines.append(f"_Prepared with context: {sponsor_company}._")
    lines.append("")

    if universe.description:
        lines.extend(["## Context", "", universe.description, ""])

    lines.extend(["## Executive observations", ""])
    for bullet in _observations(companies):
        lines.extend([f"- {bullet}", ""])

    lines.extend(["## Tier analysis", ""])
    for note in _tier_notes(companies):
        lines.extend([note, ""])

    lines.extend(["## Top candidates (detail)", ""])
    lines.extend(_top_candidates_detail(companies, n=5))

    lines.extend(
        [
            "## Full ranking",
            "",
            "| # | Company | Tier | Score | Growth | Fin.Health | AI | Rev/head | Completeness |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for rank, c in enumerate(companies, start=1):
        lines.append(
            f"| {rank} | {c.name} | {c.tier} | {_score(c.composite_score)} | "
            f"{_score(c.growth_score)} | {_score(c.financial_health_score)} | "
            f"{_score(c.ai_maturity_score)} | {_eur(_revenue_per_head_eur(c))} | "
            f"{c.completeness():.0%} |"
        )

    lines.extend(
        [
            "",
            "## Methodology note",
            "",
            "Scoring: composite = 0.4·growth + 0.4·financial_health + 0.2·AI_maturity, "
            "computed only when at least 2 of 3 signals are available. "
            "Classification (scoring/thresholds.py): phoenix ≥ 8.0, diamond ≥ 6.0, "
            "lead ≥ 4.0, salt below. Missing signals are reported as `None` — "
            "never defaulted to 0.",
            "",
            "This brief is produced deterministically from the scored universe. "
            "It contains no LLM-generated text; every observation is derived from "
            "the numeric output of `solstein run`.",
            "",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
