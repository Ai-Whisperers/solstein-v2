"""Companies House adapter tests. Uses pytest-httpx to mock the API."""

from __future__ import annotations

import httpx
import pytest
from pytest_httpx import HTTPXMock

from solstein.adapters.companies_house import CompaniesHouseAdapter
from solstein.domain import Company


@pytest.fixture
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as c:
        yield c


class TestSkipsWithoutApiKey:
    @pytest.mark.asyncio
    async def test_noop_when_no_key(
        self, httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("COMPANIES_HOUSE_API_KEY", raising=False)
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key=None)
            company = Company(name="Acme Ltd", country="GB")
            result = await adapter.enrich(company)
        assert result.founded_year is None
        assert "founded_year" not in result.citations
        assert not httpx_mock.get_requests()


class TestSkipsNonUkCountries:
    @pytest.mark.asyncio
    async def test_noop_for_non_gb_country(self, httpx_mock: HTTPXMock) -> None:
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key="test-key")
            company = Company(name="Eneve", country="NL")
            result = await adapter.enrich(company)
        assert result.founded_year is None
        assert not httpx_mock.get_requests()


class TestSuccessfulEnrichment:
    @pytest.mark.asyncio
    async def test_populates_founded_year_and_citation(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/search/companies?q=Acme+Energy&items_per_page=10",
            json={
                "items": [
                    {
                        "company_number": "12345678",
                        "company_status": "active",
                        "title": "ACME ENERGY LTD",
                    }
                ]
            },
        )
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/company/12345678",
            json={
                "company_number": "12345678",
                "company_status": "active",
                "date_of_creation": "2015-03-14",
            },
        )
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key="test-key")
            result = await adapter.enrich(Company(name="Acme Energy", country="GB"))

        assert result.founded_year == 2015
        assert result.citations["founded_year"].source == "companies_house"
        assert "12345678" in str(result.citations["founded_year"].url)

    @pytest.mark.asyncio
    async def test_does_not_overwrite_existing_founded_year(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/search/companies?q=Acme+Energy&items_per_page=10",
            json={
                "items": [
                    {"company_number": "12345678", "company_status": "active"},
                ]
            },
        )
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/company/12345678",
            json={"date_of_creation": "2015-03-14"},
        )
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key="test-key")
            result = await adapter.enrich(
                Company(name="Acme Energy", country="GB", founded_year=2010)
            )

        assert result.founded_year == 2010  # user-provided value preserved


class TestHandlesNoMatch:
    @pytest.mark.asyncio
    async def test_empty_search_returns_company_unchanged(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/search/companies?q=Nonexistent&items_per_page=10",
            json={"items": []},
        )
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key="test-key")
            result = await adapter.enrich(Company(name="Nonexistent", country="GB"))
        assert result.founded_year is None

    @pytest.mark.asyncio
    async def test_skips_dissolved_companies(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/search/companies?q=Zombie+Co&items_per_page=10",
            json={
                "items": [
                    {"company_number": "99999999", "company_status": "dissolved"},
                ]
            },
        )
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key="test-key")
            result = await adapter.enrich(Company(name="Zombie Co", country="GB"))
        assert result.founded_year is None


class TestHandlesAuthError:
    @pytest.mark.asyncio
    async def test_401_returns_gracefully(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://api.company-information.service.gov.uk/search/companies?q=Acme&items_per_page=10",
            status_code=401,
        )
        async with httpx.AsyncClient() as client:
            adapter = CompaniesHouseAdapter(client, api_key="bad-key")
            result = await adapter.enrich(Company(name="Acme", country="GB"))
        assert result.founded_year is None
