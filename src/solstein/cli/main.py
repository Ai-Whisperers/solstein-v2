"""CLI entrypoint. `solstein run` and `solstein universe-from-csv`."""

from __future__ import annotations

import asyncio
import csv
import json
from pathlib import Path
from typing import Any

import click
from loguru import logger

from solstein.domain import Company, Universe
from solstein.export import write_narrative_brief
from solstein.pipeline import run_pipeline


@click.group()
@click.version_option()
def cli() -> None:
    """Solstein — internal prospecting tool."""


@cli.command()
@click.option(
    "--universe",
    "universe_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to a universe JSON file (see docs/universe-schema.md).",
)
@click.option(
    "--output",
    "output_dir",
    required=True,
    type=click.Path(path_type=Path),
    help="Directory for output files (created if absent).",
)
def run(universe_path: Path, output_dir: Path) -> None:
    """Run the pipeline on a universe."""
    logger.info(f"Loading universe from {universe_path}")
    data = json.loads(universe_path.read_text(encoding="utf-8"))
    universe = Universe.model_validate(data)
    asyncio.run(run_pipeline(universe, output_dir))
    click.echo(f"Done → {output_dir}")


_CSV_FIELDS = {
    "name",
    "country",
    "website",
    "ticker",
    "github_org",
    "revenue_eur",
    "employees",
    "growth_yoy",
    "founded_year",
}


def _coerce(field: str, raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return None
    if field in {"revenue_eur", "growth_yoy"}:
        return float(raw)
    if field in {"employees", "founded_year"}:
        return int(raw)
    return raw


@cli.command("universe-from-csv")
@click.option(
    "--input",
    "csv_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="CSV file. Headers must include 'name'. See docs/universe-schema.md for all fields.",
)
@click.option(
    "--output",
    "json_path",
    required=True,
    type=click.Path(path_type=Path),
    help="Output universe JSON path.",
)
@click.option(
    "--name", "universe_name", required=True, help="Name of the universe (used as output prefix)."
)
@click.option("--description", default=None, help="Optional universe description.")
def universe_from_csv(
    csv_path: Path, json_path: Path, universe_name: str, description: str | None
) -> None:
    """Convert a CSV of companies into a universe JSON file.

    CSV must have a 'name' header. Any other recognized header maps to the matching
    Company field; unrecognized headers are ignored with a warning.
    """
    companies: list[Company] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "name" not in reader.fieldnames:
            raise click.UsageError("CSV must include a 'name' column.")

        unknown = set(reader.fieldnames) - _CSV_FIELDS
        if unknown:
            logger.warning(f"Ignoring unknown CSV columns: {sorted(unknown)}")

        for row_num, row in enumerate(reader, start=2):
            if not row.get("name", "").strip():
                logger.warning(f"Skipping row {row_num}: empty name")
                continue
            payload: dict[str, Any] = {}
            for field in _CSV_FIELDS:
                value = row.get(field)
                if value is None:
                    continue
                coerced = _coerce(field, value)
                if coerced is not None:
                    payload[field] = coerced
            companies.append(Company.model_validate(payload))

    universe = Universe(name=universe_name, description=description, companies=companies)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(universe.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    click.echo(f"Wrote {len(companies)} companies → {json_path}")


@cli.command()
@click.option(
    "--universe",
    "universe_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to a universe JSON file (typically produced by `solstein run`).",
)
@click.option(
    "--output",
    "output_path",
    required=True,
    type=click.Path(path_type=Path),
    help="Output markdown file path.",
)
@click.option(
    "--sponsor",
    default=None,
    help="Optional sponsor company name — appears in the brief header.",
)
def narrate(universe_path: Path, output_path: Path, sponsor: str | None) -> None:
    """Generate an analytical narrative brief from a scored universe.

    The input universe should already be scored (i.e., produced by `solstein run`).
    Re-scoring a raw universe is not automatic here; use `solstein run` first.
    """
    data = json.loads(universe_path.read_text(encoding="utf-8"))
    universe = Universe.model_validate(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_narrative_brief(universe, output_path, sponsor_company=sponsor)
    click.echo(f"Wrote narrative brief → {output_path}")


if __name__ == "__main__":
    cli()
