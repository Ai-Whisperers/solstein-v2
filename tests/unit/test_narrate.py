"""Tests for the narrative brief generator."""

from __future__ import annotations

from pathlib import Path

from solstein.domain import Company, Universe
from solstein.export.narrate import write_narrative_brief
from solstein.scoring import score_company


def _make_scored(**kwargs: object) -> Company:
    c = Company.model_validate(kwargs)
    return score_company(c)


class TestBasic:
    def test_empty_universe_writes_file(self, tmp_path: Path) -> None:
        universe = Universe(name="empty", companies=[])
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "empty" in content
        assert "0 companies" in content
        assert "Scored: 0 of 0" in content

    def test_includes_all_sections(self, tmp_path: Path) -> None:
        universe = Universe(
            name="test",
            companies=[
                _make_scored(
                    name="A", country="DE", revenue_eur=10_000_000, employees=50, growth_yoy=0.3
                ),
            ],
        )
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "# test — deal-team brief" in content
        assert "## Executive observations" in content
        assert "## Tier analysis" in content
        assert "## Top candidates (detail)" in content
        assert "## Full ranking" in content
        assert "## Methodology note" in content


class TestObservations:
    def test_flags_high_growth(self, tmp_path: Path) -> None:
        universe = Universe(
            name="growth",
            companies=[
                _make_scored(
                    name="Grower",
                    country="DE",
                    revenue_eur=10_000_000,
                    employees=50,
                    growth_yoy=0.5,
                ),
                _make_scored(
                    name="Stable",
                    country="DE",
                    revenue_eur=10_000_000,
                    employees=50,
                    growth_yoy=0.1,
                ),
            ],
        )
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "High-growth candidates" in content
        assert "Grower" in content

    def test_flags_contracting_companies(self, tmp_path: Path) -> None:
        universe = Universe(
            name="mixed",
            companies=[
                _make_scored(
                    name="Shrinker",
                    country="DE",
                    revenue_eur=10_000_000,
                    employees=50,
                    growth_yoy=-0.2,
                ),
            ],
        )
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "Contracting" in content
        assert "Shrinker" in content

    def test_reports_github_visibility(self, tmp_path: Path) -> None:
        universe = Universe(
            name="gh",
            companies=[
                _make_scored(name="A", github_org="alpha"),
                _make_scored(name="B"),
            ],
        )
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "GitHub visibility" in content
        assert "alpha" in content


class TestTierAnalysis:
    def test_includes_lead_tier_note_when_present(self, tmp_path: Path) -> None:
        universe = Universe(
            name="leads",
            companies=[
                _make_scored(
                    name="L", country="DE", revenue_eur=10_000_000, employees=50, growth_yoy=0.15
                ),
            ],
        )
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "Lead tier" in content

    def test_large_unknown_bucket_flagged(self, tmp_path: Path) -> None:
        universe = Universe(
            name="unknowns",
            companies=[
                _make_scored(name=f"U{i}")
                for i in range(5)  # all unscored
            ],
        )
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out)
        content = out.read_text()
        assert "Significant unknown bucket" in content


class TestSponsor:
    def test_sponsor_context_appears_in_header(self, tmp_path: Path) -> None:
        universe = Universe(name="x", companies=[])
        out = tmp_path / "brief.md"
        write_narrative_brief(universe, out, sponsor_company="Acme PE")
        content = out.read_text()
        assert "Prepared with context: Acme PE" in content
