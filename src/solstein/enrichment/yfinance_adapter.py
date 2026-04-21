"""yfinance enrichment — public-market financials for companies with a ticker.

Requires `ticker` on the Company. yfinance is sync, so we wrap calls in
asyncio.to_thread to keep the pipeline non-blocking.

Populates: revenue_eur (approx, from totalRevenue), employees (fullTimeEmployees),
growth_yoy (from income statement if ≥2 annual periods).

yfinance is a best-effort scraper of Yahoo Finance; schemas change periodically.
Every field access is tolerant and logs a warning on failure rather than raising.
"""

from __future__ import annotations

import asyncio
from datetime import date
from typing import Any

from loguru import logger

from solstein.domain import Citation, Company

# yfinance is an optional, heavy dep; import lazily so missing install doesn't break
# import time for the whole package.
try:
    import yfinance as yf  # type: ignore[import-untyped]

    _HAS_YFINANCE = True
except ImportError:
    _HAS_YFINANCE = False


class YFinanceAdapter:
    def __init__(self, usd_to_eur: float = 0.92) -> None:
        """usd_to_eur: conversion rate applied when Yahoo returns USD amounts.
        0.92 is a reasonable 2026 approximation; pass a live rate for production.
        """
        self.usd_to_eur = usd_to_eur
        if not _HAS_YFINANCE:
            logger.warning("yfinance not installed — YFinanceAdapter will no-op")

    async def enrich(self, company: Company) -> Company:
        if not _HAS_YFINANCE or not company.ticker:
            return company

        try:
            ticker_obj = await asyncio.to_thread(yf.Ticker, company.ticker)
            info: dict[str, Any] = await asyncio.to_thread(lambda: ticker_obj.info or {})
        except Exception as e:
            logger.warning(f"yfinance failed for {company.ticker}: {e}")
            return company

        citation = Citation(
            source="yfinance",
            url=f"https://finance.yahoo.com/quote/{company.ticker}",
            retrieved_at=date.today(),
        )
        currency = (info.get("financialCurrency") or info.get("currency") or "").upper()
        rate = self.usd_to_eur if currency == "USD" else 1.0  # EUR stays EUR, USD converts

        total_revenue = info.get("totalRevenue")
        if company.revenue_eur is None and isinstance(total_revenue, int | float):
            company.revenue_eur = float(total_revenue) * rate
            company.citations["revenue_eur"] = citation

        employees = info.get("fullTimeEmployees")
        if company.employees is None and isinstance(employees, int):
            company.employees = employees
            company.citations["employees"] = citation

        growth = info.get("revenueGrowth")
        if company.growth_yoy is None and isinstance(growth, int | float):
            company.growth_yoy = float(growth)
            company.citations["growth_yoy"] = citation

        return company
