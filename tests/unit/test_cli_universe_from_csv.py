"""Tests for `solstein universe-from-csv`."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from solstein.cli.main import cli


def _write_csv(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


class TestBasic:
    def test_minimum_csv_produces_valid_universe(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path, "name\nAcme Corp\nBeta Ltd\n")
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "test",
            ],
        )
        assert result.exit_code == 0, result.output
        data = json.loads(out_path.read_text())
        assert data["name"] == "test"
        assert len(data["companies"]) == 2
        assert {c["name"] for c in data["companies"]} == {"Acme Corp", "Beta Ltd"}


class TestFieldCoercion:
    def test_numeric_fields_are_typed(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "in.csv"
        _write_csv(
            csv_path,
            "name,country,revenue_eur,employees,growth_yoy,founded_year\n"
            "Eneve,NL,30000000,130,0.22,2010\n",
        )
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "eneve",
            ],
        )
        assert result.exit_code == 0
        company = json.loads(out_path.read_text())["companies"][0]
        assert company["revenue_eur"] == 30000000
        assert company["employees"] == 130
        assert company["growth_yoy"] == 0.22
        assert company["founded_year"] == 2010

    def test_empty_cells_become_none(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path, "name,country,revenue_eur\nAcme,,\n")
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "acme",
            ],
        )
        assert result.exit_code == 0
        company = json.loads(out_path.read_text())["companies"][0]
        assert company["country"] is None
        assert company["revenue_eur"] is None


class TestValidation:
    def test_missing_name_column_errors(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path, "country,website\nNL,example.com\n")
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "x",
            ],
        )
        assert result.exit_code != 0
        assert "name" in result.output.lower()

    def test_unknown_columns_warn_but_succeed(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path, "name,nonexistent_field\nAcme,value\n")
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "x",
            ],
        )
        assert result.exit_code == 0
        company = json.loads(out_path.read_text())["companies"][0]
        assert company["name"] == "Acme"
        assert "nonexistent_field" not in company

    def test_empty_name_rows_are_skipped(self, tmp_path: Path) -> None:
        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path, "name\nAcme\n\n   \nBeta\n")
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "x",
            ],
        )
        assert result.exit_code == 0
        data = json.loads(out_path.read_text())
        assert [c["name"] for c in data["companies"]] == ["Acme", "Beta"]


class TestEndToEnd:
    def test_output_is_loadable_as_universe(self, tmp_path: Path) -> None:
        """The produced JSON must parse as a Universe without further edits."""
        from solstein.domain import Universe

        csv_path = tmp_path / "in.csv"
        _write_csv(csv_path, "name,country,ticker\nAcme,US,ACME\nBeta,GB,\n")
        out_path = tmp_path / "out.json"

        result = CliRunner().invoke(
            cli,
            [
                "universe-from-csv",
                "--input",
                str(csv_path),
                "--output",
                str(out_path),
                "--name",
                "roundtrip",
                "--description",
                "test universe",
            ],
        )
        assert result.exit_code == 0
        universe = Universe.model_validate_json(out_path.read_text())
        assert universe.name == "roundtrip"
        assert universe.description == "test universe"
        assert len(universe.companies) == 2
        assert universe.companies[0].ticker == "ACME"
        assert universe.companies[1].ticker is None


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()
