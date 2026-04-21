"""Export writers: Excel shortlist + Markdown brief.

The deal team reads the Markdown. Excel is for anyone who wants to pivot.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from solstein.domain import Universe

TIER_COLORS = {
    "phoenix": "C6EFCE",
    "diamond": "DDEBF7",
    "lead": "FFF2CC",
    "salt": "FCE4D6",
    "unknown": "FFFFFF",
}


def write_excel(universe: Universe, path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    if ws is None:
        raise RuntimeError("openpyxl gave no active sheet")
    ws.title = universe.name[:31]

    headers = [
        "Rank",
        "Company",
        "Tier",
        "Composite",
        "Growth",
        "Financial Health",
        "AI Maturity",
        "Revenue (€)",
        "Employees",
        "YoY Growth",
        "GitHub Stars",
        "GitHub 90d Commits",
        "Completeness",
        "Country",
        "Website",
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for rank, c in enumerate(universe.companies, start=1):
        ws.append(
            [
                rank,
                c.name,
                c.tier,
                c.composite_score,
                c.growth_score,
                c.financial_health_score,
                c.ai_maturity_score,
                c.revenue_eur,
                c.employees,
                c.growth_yoy,
                c.github_stars_total,
                c.github_commits_last_90d,
                round(c.completeness(), 2),
                c.country,
                str(c.website) if c.website else None,
            ]
        )
        fill = PatternFill(start_color=TIER_COLORS.get(c.tier, "FFFFFF"), fill_type="solid")
        for cell in ws[ws.max_row]:
            cell.fill = fill

    wb.save(path)


def write_markdown_brief(universe: Universe, path: Path) -> None:
    lines: list[str] = [
        f"# {universe.name} — deal-team brief",
        "",
        f"_Generated {date.today().isoformat()} · {len(universe.companies)} companies._",
        "",
        "## Top candidates",
        "",
    ]
    top = [c for c in universe.companies if c.tier in ("phoenix", "diamond")][:10]
    if not top:
        lines.append("_No Phoenix or Diamond candidates in this universe._")
    else:
        for c in top:
            score = f"{c.composite_score:.2f}" if c.composite_score is not None else "n/a"
            lines.extend(
                [
                    f"### {c.name} — **{c.tier}** ({score}/10)",
                    "",
                    f"- Country: {c.country or 'unknown'}",
                    f"- Revenue: {_eur(c.revenue_eur)} · Employees: {c.employees or 'unknown'} · YoY: {_pct(c.growth_yoy)}",
                    f"- GitHub: {c.github_stars_total or 0} stars · {c.github_commits_last_90d or 0} commits (90d)",
                    f"- Completeness: {c.completeness():.0%}",
                    "",
                ]
            )

    lines.extend(
        [
            "",
            "## Full ranking",
            "",
            "| # | Company | Tier | Score | Completeness |",
            "|---|---|---|---|---|",
        ]
    )
    for rank, c in enumerate(universe.companies, start=1):
        score = f"{c.composite_score:.2f}" if c.composite_score is not None else "—"
        lines.append(f"| {rank} | {c.name} | {c.tier} | {score} | {c.completeness():.0%} |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _eur(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value >= 1_000_000:
        return f"€{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"€{value / 1_000:.0f}K"
    return f"€{value:.0f}"


def _pct(value: float | None) -> str:
    return f"{value:.0%}" if value is not None else "unknown"
