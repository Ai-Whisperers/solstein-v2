"""CLI entrypoint. One command, `solstein run`."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import click
from loguru import logger

from solstein.domain import Universe
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


if __name__ == "__main__":
    cli()
