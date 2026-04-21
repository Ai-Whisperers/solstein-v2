"""SEC EDGAR adapter — US public company filings.

MVP: resolve company name → CIK (Central Index Key) and ticker. That alone is
a strong signal (the company is US-listed and SEC-registered). Deeper extraction
of revenue/employees from company-facts XBRL is deferred until a universe needs it.

Auth: none required, but SEC requires a descriptive User-Agent with contact info.
Set SEC_EDGAR_USER_AGENT env var or override via constructor.

Docs: https://www.sec.gov/edgar/sec-api-documentation
"""

from __future__ import annotations

import os
import re
from datetime import date
from typing import Any

import httpx
from loguru import logger

from solstein.adapters._retry import http_retry
from solstein.domain import Citation, Company

SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
_CIK_IN_DISPLAY_NAME = re.compile(r"\((\d{6,10})\)")


class SecEdgarAdapter:
    def __init__(self, client: httpx.AsyncClient, user_agent: str | None = None) -> None:
        self.client = client
        self.user_agent: str = (
            user_agent
            or os.getenv("SEC_EDGAR_USER_AGENT")
            or "AI-Whisperers Solstein team@ai-whisperers.com"
        )

    @property
    def _headers(self) -> dict[str, str]:
        return {"User-Agent": self.user_agent, "Accept": "application/json"}

    @http_retry
    async def _get(self, url: str, params: dict[str, str] | None = None) -> httpx.Response:
        response = await self.client.get(url, headers=self._headers, params=params, timeout=15.0)
        response.raise_for_status()
        return response

    async def enrich(self, company: Company) -> Company:
        """Look up SEC filings by company name. US filers only.

        No-op if the company is explicitly marked non-US, if sec_cik is already
        populated, or if the search returns no match.
        """
        if company.sec_cik is not None:
            return company
        if company.country and company.country.upper() != "US":
            return company

        try:
            match = await self._search_filer(company.name)
        except httpx.HTTPStatusError as e:
            logger.error(f"SEC EDGAR error for '{company.name}': {e}")
            return company

        if match is None:
            return company

        citation_url = (
            f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={match['cik']}"
        )
        citation = Citation(source="sec_edgar", url=citation_url, retrieved_at=date.today())

        company.sec_cik = str(match["cik"])
        company.citations["sec_cik"] = citation

        if company.ticker is None and match.get("ticker"):
            company.ticker = str(match["ticker"]).upper()
            company.citations["ticker"] = citation

        return company

    async def _search_filer(self, name: str) -> dict[str, Any] | None:
        """Full-text search EDGAR for the filer name. Returns top match or None.

        The `efts.sec.gov` endpoint returns hits with entity metadata including
        CIK and the primary ticker. We filter to companies (not individual filers).
        """
        response = await self._get(SEARCH_URL, params={"q": f'"{name}"', "dateRange": "custom"})
        data = response.json()
        hits = data.get("hits", {}).get("hits", [])
        for hit in hits:
            source = hit.get("_source", {})
            entities = source.get("entities") or source.get("display_names") or []
            # entities is either a list of dicts (rich) or list of strings (simple)
            for entity in entities:
                cik: str | None = None
                ticker: str | None = None
                if isinstance(entity, dict):
                    cik = entity.get("cik")
                    ticker = entity.get("ticker")
                elif isinstance(entity, str):
                    match = _CIK_IN_DISPLAY_NAME.search(entity)
                    if match:
                        cik = match.group(1).lstrip("0") or "0"
                if cik:
                    return {"cik": cik, "ticker": ticker}
        return None
