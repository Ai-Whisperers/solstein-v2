"""YFinance adapter tests. Mocks yf.Ticker entirely — no network calls."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from solstein.domain import Company
from solstein.enrichment.yfinance_adapter import YFinanceAdapter


def _mock_ticker(info: dict[str, Any]) -> MagicMock:
    mock = MagicMock()
    mock.info = info
    return mock


class TestSkipLogic:
    @pytest.mark.asyncio
    async def test_noop_without_ticker(self) -> None:
        adapter = YFinanceAdapter()
        result = await adapter.enrich(Company(name="X"))
        assert result.revenue_eur is None
        assert result.employees is None


class TestEnrichment:
    @pytest.mark.asyncio
    async def test_populates_fields_from_yf_info(self) -> None:
        info = {
            "totalRevenue": 1_000_000_000,
            "fullTimeEmployees": 500,
            "revenueGrowth": 0.25,
            "financialCurrency": "USD",
        }
        with patch("solstein.enrichment.yfinance_adapter.yf") as mock_yf:
            mock_yf.Ticker.return_value = _mock_ticker(info)
            adapter = YFinanceAdapter(usd_to_eur=0.9)
            result = await adapter.enrich(Company(name="Acme", ticker="ACME"))

        assert result.revenue_eur == pytest.approx(900_000_000)  # USD → EUR
        assert result.employees == 500
        assert result.growth_yoy == 0.25
        assert "revenue_eur" in result.citations

    @pytest.mark.asyncio
    async def test_does_not_overwrite_existing_values(self) -> None:
        info = {"totalRevenue": 1_000_000_000, "fullTimeEmployees": 500}
        with patch("solstein.enrichment.yfinance_adapter.yf") as mock_yf:
            mock_yf.Ticker.return_value = _mock_ticker(info)
            adapter = YFinanceAdapter()
            result = await adapter.enrich(
                Company(name="Acme", ticker="ACME", revenue_eur=123.0, employees=42)
            )
        assert result.revenue_eur == 123.0
        assert result.employees == 42

    @pytest.mark.asyncio
    async def test_handles_exception_gracefully(self) -> None:
        with patch("solstein.enrichment.yfinance_adapter.yf") as mock_yf:
            mock_yf.Ticker.side_effect = RuntimeError("yahoo is down")
            adapter = YFinanceAdapter()
            result = await adapter.enrich(Company(name="Acme", ticker="ACME"))
        assert result.revenue_eur is None

    @pytest.mark.asyncio
    async def test_empty_info_leaves_fields_none(self) -> None:
        with patch("solstein.enrichment.yfinance_adapter.yf") as mock_yf:
            mock_yf.Ticker.return_value = _mock_ticker({})
            adapter = YFinanceAdapter()
            result = await adapter.enrich(Company(name="Acme", ticker="ACME"))
        assert result.revenue_eur is None
        assert result.employees is None

    @pytest.mark.asyncio
    async def test_eur_currency_not_converted(self) -> None:
        info = {"totalRevenue": 1_000_000_000, "financialCurrency": "EUR"}
        with patch("solstein.enrichment.yfinance_adapter.yf") as mock_yf:
            mock_yf.Ticker.return_value = _mock_ticker(info)
            adapter = YFinanceAdapter(usd_to_eur=0.9)
            result = await adapter.enrich(Company(name="Acme", ticker="ACME"))
        assert result.revenue_eur == 1_000_000_000  # no conversion
