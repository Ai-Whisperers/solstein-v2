"""The canonical pipeline. One function. One flow.

Discover → Enrich → Score → Export. No dual-writes, no side branches.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import httpx
from loguru import logger

from solstein.adapters import CompaniesHouseAdapter, GitHubAdapter, SecEdgarAdapter
from solstein.domain import Company, Universe
from solstein.enrichment import YFinanceAdapter
from solstein.export.narrate import write_narrative_brief
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
        companies_house = CompaniesHouseAdapter(client)
        sec = SecEdgarAdapter(client)
        yfinance = YFinanceAdapter()

        async def enrich_one(c: Company) -> Company:
            c = await github.enrich(c)
            c = await companies_house.enrich(c)
            c = await sec.enrich(c)
            c = await yfinance.enrich(c)
            return c

        universe.companies = await asyncio.gather(*(enrich_one(c) for c in universe.companies))

    for company in universe.companies:
        score_company(company)

    universe.companies.sort(
        key=lambda c: c.composite_score if c.composite_score is not None else -1.0,
        reverse=True,
    )

    write_excel(universe, output_dir / f"{universe.name}.xlsx")
    write_markdown_brief(universe, output_dir / f"{universe.name}.md")
    write_narrative_brief(universe, output_dir / f"{universe.name}-narrative.md")
    (output_dir / f"{universe.name}-scored.json").write_text(
        json.dumps(universe.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    scored = sum(1 for c in universe.companies if c.composite_score is not None)
    logger.info(f"Pipeline done: scored={scored}/{len(universe.companies)} → {output_dir}")
    return universe
