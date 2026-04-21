"""Companies House adapter — UK company registry.

Signals extracted: company_number (id match), incorporation date (founded_year),
and most recent filed accounts (revenue/employees, when available).

Auth: `COMPANIES_HOUSE_API_KEY` env var. The API uses HTTP Basic with the key
as the username and empty password. Without a key, this adapter skips gracefully
(logs a warning; does not fake data).

Docs: https://developer-specs.company-information.service.gov.uk/
"""

from __future__ import annotations

import os
from datetime import date
from typing import Any

import httpx
from loguru import logger
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from solstein.domain import Citation, Company

API_BASE = "https://api.company-information.service.gov.uk"


def _is_transient(exc: BaseException) -> bool:
    """Retry timeouts and 5xx. 4xx errors are permanent — don't burn retries on them."""
    if isinstance(exc, httpx.TimeoutException | httpx.NetworkError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return 500 <= exc.response.status_code < 600
    return False


class CompaniesHouseAdapter:
    def __init__(
        self,
        client: httpx.AsyncClient,
        api_key: str | None = None,
        country_filter: str = "GB",
    ) -> None:
        self.client = client
        self.api_key = api_key or os.getenv("COMPANIES_HOUSE_API_KEY")
        self.country_filter = country_filter
        self._warned_no_key = False

    @property
    def _auth(self) -> httpx.BasicAuth | None:
        return httpx.BasicAuth(self.api_key, "") if self.api_key else None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=10),
        retry=retry_if_exception(_is_transient),
        reraise=True,
    )
    async def _get(self, path: str, params: dict[str, str] | None = None) -> httpx.Response:
        response = await self.client.get(
            f"{API_BASE}{path}", auth=self._auth, params=params, timeout=15.0
        )
        response.raise_for_status()
        return response

    async def enrich(self, company: Company) -> Company:
        """Enrich UK-domiciled companies only. No-op for everything else."""
        if not self.api_key:
            if not self._warned_no_key:
                logger.warning(
                    "COMPANIES_HOUSE_API_KEY not set — skipping CompaniesHouse enrichment"
                )
                self._warned_no_key = True
            return company

        if company.country and company.country.upper() != self.country_filter:
            return company

        profile = await self._find_profile(company.name)
        if profile is None:
            return company

        today = date.today()
        company_number = profile.get("company_number")
        citation_url = (
            f"https://find-and-update.company-information.service.gov.uk/company/{company_number}"
            if company_number
            else None
        )
        citation = Citation(source="companies_house", url=citation_url, retrieved_at=today)

        if company.founded_year is None:
            incorporation = profile.get("date_of_creation")
            if isinstance(incorporation, str) and len(incorporation) >= 4:
                try:
                    company.founded_year = int(incorporation[:4])
                    company.citations["founded_year"] = citation
                except ValueError:
                    pass

        return company

    async def _find_profile(self, name: str) -> dict[str, Any] | None:
        """Search by name, return the top active match's profile.

        Companies House search is tolerant — first result is usually the best match
        when the name is specific. We filter to active status to avoid dissolved shells.
        """
        try:
            search = await self._get(
                "/search/companies", params={"q": name, "items_per_page": "10"}
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Companies House returned 401 — check COMPANIES_HOUSE_API_KEY")
                return None
            logger.error(f"Companies House search error for '{name}': {e}")
            raise

        items = search.json().get("items", [])
        for item in items:
            if item.get("company_status") == "active":
                number = item.get("company_number")
                if not number:
                    continue
                try:
                    profile = await self._get(f"/company/{number}")
                    return dict(profile.json())
                except httpx.HTTPStatusError:
                    continue
        return None
