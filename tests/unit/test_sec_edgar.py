"""SEC EDGAR adapter tests."""

from __future__ import annotations

import httpx
import pytest
from pytest_httpx import HTTPXMock

from solstein.adapters.sec_edgar import SEARCH_URL, SecEdgarAdapter
from solstein.domain import Company


class TestSkipLogic:
    @pytest.mark.asyncio
    async def test_skips_non_us(self, httpx_mock: HTTPXMock) -> None:
        async with httpx.AsyncClient() as client:
            adapter = SecEdgarAdapter(client)
            result = await adapter.enrich(Company(name="Eneve", country="NL"))
        assert result.sec_cik is None
        assert not httpx_mock.get_requests()

    @pytest.mark.asyncio
    async def test_skips_if_already_has_cik(self, httpx_mock: HTTPXMock) -> None:
        async with httpx.AsyncClient() as client:
            adapter = SecEdgarAdapter(client)
            result = await adapter.enrich(Company(name="Acme", sec_cik="12345"))
        assert result.sec_cik == "12345"
        assert not httpx_mock.get_requests()


class TestEnrichment:
    @pytest.mark.asyncio
    async def test_populates_cik_from_search(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{SEARCH_URL}?q=%22Snowflake+Inc%22&dateRange=custom",
            json={
                "hits": {
                    "hits": [
                        {
                            "_source": {
                                "display_names": ["SNOWFLAKE INC. (0001640147) (Filer)"],
                            }
                        }
                    ]
                }
            },
        )
        async with httpx.AsyncClient() as client:
            adapter = SecEdgarAdapter(client)
            result = await adapter.enrich(Company(name="Snowflake Inc", country="US"))
        assert result.sec_cik == "1640147"
        assert result.citations["sec_cik"].source == "sec_edgar"

    @pytest.mark.asyncio
    async def test_no_match_leaves_company_unchanged(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{SEARCH_URL}?q=%22Nonexistent+Co%22&dateRange=custom",
            json={"hits": {"hits": []}},
        )
        async with httpx.AsyncClient() as client:
            adapter = SecEdgarAdapter(client)
            result = await adapter.enrich(Company(name="Nonexistent Co", country="US"))
        assert result.sec_cik is None


class TestUserAgent:
    @pytest.mark.asyncio
    async def test_sends_user_agent(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url=f"{SEARCH_URL}?q=%22Acme%22&dateRange=custom",
            json={"hits": {"hits": []}},
        )
        async with httpx.AsyncClient() as client:
            adapter = SecEdgarAdapter(client, user_agent="Test Agent test@example.com")
            await adapter.enrich(Company(name="Acme", country="US"))

        requests = httpx_mock.get_requests()
        assert len(requests) == 1
        assert requests[0].headers["User-Agent"] == "Test Agent test@example.com"
