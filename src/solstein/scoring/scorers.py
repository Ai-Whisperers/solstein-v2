"""Scoring functions. Each returns a value in [0, 10] or None if input is insufficient.

Rule: return None if a required signal is missing. Never silently use a default.
v1 used silent-None handling and produced Phoenix classifications from zero data.
"""

from __future__ import annotations

import math

from solstein.domain import Company
from solstein.scoring.thresholds import classify


def growth_score(company: Company) -> float | None:
    """Score growth from YoY revenue growth. Linear up to 30%, capped at 10."""
    if company.growth_yoy is None:
        return None
    # 0% → 0, 10% → 3.3, 20% → 6.7, 30%+ → 10
    return min(10.0, max(0.0, company.growth_yoy * 10.0 / 0.30))


def financial_health_score(company: Company) -> float | None:
    """Proxy: revenue per employee. Favors profitable SMBs."""
    if company.revenue_eur is None or company.employees is None or company.employees <= 0:
        return None
    revenue_per_head_k = company.revenue_eur / company.employees / 1000.0
    # 100k/head → 3.3, 300k/head → 6.7, 500k+/head → 10
    return min(10.0, max(0.0, revenue_per_head_k / 50.0))


def ai_maturity_score(company: Company) -> float | None:
    """Signal from GitHub activity. Stand-in until we wire real AI-specific signals.

    Intentionally conservative: a company without public OSS activity can still be
    AI-mature internally, so this returns None when GitHub data is absent rather
    than penalizing the company.
    """
    if company.github_commits_last_90d is None or company.github_stars_total is None:
        return None
    # log scaling — 100 commits → 3, 500 → 5.4, 2000 → 7.6, 5000 → 9.3
    commit_signal = min(10.0, math.log10(max(company.github_commits_last_90d, 1)) * 2.5)
    # stars are less important (popularity != productivity): weight 20%
    star_signal = min(10.0, math.log10(max(company.github_stars_total, 1)) * 2.0)
    return 0.8 * commit_signal + 0.2 * star_signal


def composite(company: Company) -> float | None:
    """Weighted average of available sub-scores.

    Weights: growth 40%, financial health 40%, AI maturity 20%.
    Returns None if more than one signal is missing — we will not score
    a company on a single dimension.
    """
    parts: list[tuple[float, float]] = []  # (score, weight)
    if (g := growth_score(company)) is not None:
        parts.append((g, 0.4))
    if (f := financial_health_score(company)) is not None:
        parts.append((f, 0.4))
    if (a := ai_maturity_score(company)) is not None:
        parts.append((a, 0.2))

    if len(parts) < 2:
        return None

    total_weight = sum(w for _, w in parts)
    return sum(s * w for s, w in parts) / total_weight


def score_company(company: Company) -> Company:
    """Attach all scores to a company. Idempotent. Never raises."""
    company.growth_score = growth_score(company)
    company.financial_health_score = financial_health_score(company)
    company.ai_maturity_score = ai_maturity_score(company)
    company.composite_score = composite(company)
    if company.composite_score is not None:
        company.tier = classify(company.composite_score)
    return company
