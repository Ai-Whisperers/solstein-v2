"""Core domain types. One module, all the shared shapes.

Keep this tight. Adding a field here has a blast radius across scoring,
export, and every adapter. If a value is only used in one module, keep it there.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

Tier = Literal["phoenix", "diamond", "lead", "salt", "unknown"]


class Citation(BaseModel):
    """Where a specific field came from. Required for any enriched field."""

    model_config = ConfigDict(frozen=True)

    source: str = Field(description="Adapter name: 'github', 'sec_edgar', 'companies_house', etc.")
    url: str | None = None
    retrieved_at: date
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class Company(BaseModel):
    """The unit of work. Populated progressively by adapters + enrichment."""

    model_config = ConfigDict(extra="forbid")

    name: str
    country: str | None = None
    website: HttpUrl | None = None

    revenue_eur: float | None = None
    employees: int | None = None
    growth_yoy: float | None = None
    founded_year: int | None = None

    ticker: str | None = None  # e.g., "AAPL". Enables yfinance enrichment.
    sec_cik: str | None = None  # SEC Central Index Key. Set by SEC adapter.

    github_org: str | None = None
    github_stars_total: int | None = None
    github_commits_last_90d: int | None = None

    ai_maturity_score: float | None = Field(default=None, ge=0, le=10)
    financial_health_score: float | None = Field(default=None, ge=0, le=10)
    growth_score: float | None = Field(default=None, ge=0, le=10)

    composite_score: float | None = Field(default=None, ge=0, le=10)
    tier: Tier = "unknown"

    citations: dict[str, Citation] = Field(default_factory=dict)

    def completeness(self) -> float:
        """Fraction of scorable fields populated."""
        scorable = [
            self.revenue_eur,
            self.employees,
            self.growth_yoy,
            self.github_stars_total,
            self.github_commits_last_90d,
        ]
        return sum(1 for f in scorable if f is not None) / len(scorable)


class Universe(BaseModel):
    """A named set of companies to research."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None
    companies: list[Company]
