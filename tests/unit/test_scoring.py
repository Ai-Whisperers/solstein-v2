"""Scoring contract tests.

These are behavioral, not structural. They assert what the scorer does, not how.
"""

from __future__ import annotations

import pytest

from solstein.domain import Company
from solstein.scoring import score_company
from solstein.scoring.scorers import (
    ai_maturity_score,
    composite,
    financial_health_score,
    growth_score,
)
from solstein.scoring.thresholds import DIAMOND_MIN, LEAD_MIN, PHOENIX_MIN, classify


class TestThresholds:
    def test_classify_boundaries(self) -> None:
        assert classify(PHOENIX_MIN) == "phoenix"
        assert classify(PHOENIX_MIN - 0.01) == "diamond"
        assert classify(DIAMOND_MIN) == "diamond"
        assert classify(DIAMOND_MIN - 0.01) == "lead"
        assert classify(LEAD_MIN) == "lead"
        assert classify(LEAD_MIN - 0.01) == "salt"
        assert classify(0) == "salt"
        assert classify(10) == "phoenix"


class TestGrowthScore:
    def test_missing_signal_returns_none(self) -> None:
        assert growth_score(Company(name="X")) is None

    def test_zero_growth_scores_zero(self) -> None:
        assert growth_score(Company(name="X", growth_yoy=0.0)) == 0.0

    def test_30pct_growth_caps_at_10(self) -> None:
        assert growth_score(Company(name="X", growth_yoy=0.30)) == 10.0

    def test_above_30pct_still_capped(self) -> None:
        assert growth_score(Company(name="X", growth_yoy=0.80)) == 10.0


class TestFinancialHealthScore:
    def test_missing_returns_none(self) -> None:
        assert financial_health_score(Company(name="X")) is None
        assert financial_health_score(Company(name="X", revenue_eur=1_000_000)) is None
        assert financial_health_score(Company(name="X", employees=10)) is None

    def test_zero_employees_returns_none(self) -> None:
        assert financial_health_score(Company(name="X", revenue_eur=1_000_000, employees=0)) is None

    def test_healthy_smb_scores_positive(self) -> None:
        score = financial_health_score(Company(name="X", revenue_eur=30_000_000, employees=130))
        assert score is not None and score > 4.0


class TestAIMaturity:
    def test_no_github_signal_returns_none(self) -> None:
        assert ai_maturity_score(Company(name="X")) is None

    def test_active_org_scores_positive(self) -> None:
        company = Company(name="X", github_stars_total=500, github_commits_last_90d=500)
        score = ai_maturity_score(company)
        assert score is not None and score > 4.0


class TestComposite:
    def test_requires_two_signals(self) -> None:
        company = Company(name="X", growth_yoy=0.2)
        assert composite(company) is None

    def test_with_two_signals_produces_score(self) -> None:
        company = Company(name="X", growth_yoy=0.2, revenue_eur=30_000_000, employees=130)
        score = composite(company)
        assert score is not None and 0 <= score <= 10


class TestEndToEndEneve:
    """Regression: Eneve's score must stay stable across refactors."""

    @pytest.fixture
    def eneve(self) -> Company:
        return Company(
            name="Eneve",
            country="NL",
            revenue_eur=30_000_000,
            employees=130,
            growth_yoy=0.22,
        )

    def test_eneve_with_partial_data_scores_honestly(self, eneve: Company) -> None:
        """v1 reported Eneve at 9.03/10 on partly-synthetic data.

        With only 2 real signals (growth, financial health) and no GitHub data,
        the honest composite lands in the lead/diamond border — around 6.0.
        This test locks in the honest behavior, not v1's inflation.
        """
        scored = score_company(eneve)
        assert scored.composite_score is not None
        assert 5.5 <= scored.composite_score <= 7.0
        assert scored.tier in ("lead", "diamond")

    def test_eneve_with_strong_github_moves_to_diamond(self, eneve: Company) -> None:
        """Adding GitHub signal should move Eneve into Diamond or higher."""
        eneve.github_stars_total = 2000
        eneve.github_commits_last_90d = 1500
        scored = score_company(eneve)
        assert scored.composite_score is not None
        assert scored.tier in ("diamond", "phoenix")

    def test_eneve_scoring_is_deterministic(self, eneve: Company) -> None:
        a = score_company(Company.model_validate(eneve.model_dump()))
        b = score_company(Company.model_validate(eneve.model_dump()))
        assert a.composite_score == b.composite_score
        assert a.tier == b.tier
