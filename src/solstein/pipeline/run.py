"""The canonical pipeline. One function. One flow.

Discover → Enrich → Score → Export. No dual-writes, no side branches.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
from loguru import logger

from solstein.adapters import GitHubAdapter
from solstein.domain import Universe
from solstein.export.writers import write_excel, write_markdown_brief
from solstein.scoring import score_company


async def run_pipeline(universe: Universe, output_dir: Path) -> Universe:
    """Run the full pipeline on a universe. Writes outputs to output_dir.

    Returns the enriched+scored universe for programmatic inspection.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Pipeline starting: universe={universe.name} n={len(universe.companies)}")

    async with httpx.AsyncClient() as client:
        github = GitHubAdapter(client)
        universe.companies = await asyncio.gather(*(github.enrich(c) for c in universe.companies))

    for company in universe.companies:
        score_company(company)

    universe.companies.sort(
        key=lambda c: c.composite_score if c.composite_score is not None else -1.0,
        reverse=True,
    )

    write_excel(universe, output_dir / f"{universe.name}.xlsx")
    write_markdown_brief(universe, output_dir / f"{universe.name}.md")

    scored = sum(1 for c in universe.companies if c.composite_score is not None)
    logger.info(f"Pipeline done: scored={scored}/{len(universe.companies)} → {output_dir}")
    return universe
