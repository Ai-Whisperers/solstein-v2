"""Tests for the website adapter. Network mocked via pytest-httpx."""

from __future__ import annotations

import httpx
import pytest
from pytest_httpx import HTTPXMock

from solstein.adapters.website import WebsiteAdapter
from solstein.domain import Company


class TestSkipLogic:
    @pytest.mark.asyncio
    async def test_noop_without_website(self, httpx_mock: HTTPXMock) -> None:
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="No-website"))
        assert result.ai_maturity_score is None
        assert not httpx_mock.get_requests()

    @pytest.mark.asyncio
    async def test_noop_when_ai_maturity_already_set(self, httpx_mock: HTTPXMock) -> None:
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(
                Company(
                    name="Prescored",
                    website="https://example.com",
                    ai_maturity_score=7.5,
                )
            )
        assert result.ai_maturity_score == 7.5
        assert not httpx_mock.get_requests()


class TestRobotsHandling:
    @pytest.mark.asyncio
    async def test_robots_disallow_all_skips_fetch(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://example.com/robots.txt",
            text="User-agent: *\nDisallow: /",
        )
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="Forbidden", website="https://example.com"))
        assert result.ai_maturity_score is None
        # robots.txt was fetched but the homepage was not
        urls = [str(req.url) for req in httpx_mock.get_requests()]
        assert "robots.txt" in "".join(urls)
        assert not any(u.endswith("example.com/") or u == "https://example.com" for u in urls)

    @pytest.mark.asyncio
    async def test_missing_robots_defaults_to_allow(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            url="https://example.com/robots.txt",
            status_code=404,
        )
        httpx_mock.add_response(
            url="https://example.com/",
            headers={"content-type": "text/html"},
            text="<html><body>"
            + "We use machine learning and build LLM applications with PyTorch. " * 10
            + "</body></html>",
        )
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="Acme", website="https://example.com"))
        assert result.ai_maturity_score is not None
        assert result.ai_maturity_score > 0


class TestEnrichment:
    @pytest.mark.asyncio
    async def test_high_signal_page_populates_score(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://example.com/robots.txt", status_code=404)
        httpx_mock.add_response(
            url="https://example.com/",
            headers={"content-type": "text/html"},
            text=(
                "<html><body>"
                "<p>MLOps feature store vector database production ML model serving RAG pipeline "
                "fine-tuning prompt engineering ML platform ML infrastructure "
                "machine learning deep learning LLMOps with transformers and LLM agents. "
                "We deploy Claude and GPT models in production.</p>" * 3 + "</body></html>"
            ),
        )
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="AI-native", website="https://example.com"))

        assert result.ai_maturity_score is not None
        assert result.ai_maturity_score >= 7.0
        assert "ai_maturity_score" in result.citations
        citation = result.citations["ai_maturity_score"]
        assert citation.source == "website"

    @pytest.mark.asyncio
    async def test_empty_page_returns_unchanged(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://example.com/robots.txt", status_code=404)
        httpx_mock.add_response(
            url="https://example.com/",
            headers={"content-type": "text/html"},
            text="<html><body></body></html>",
        )
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="Empty", website="https://example.com"))
        assert result.ai_maturity_score is None

    @pytest.mark.asyncio
    async def test_non_html_content_skipped(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://example.com/robots.txt", status_code=404)
        httpx_mock.add_response(
            url="https://example.com/",
            headers={"content-type": "application/pdf"},
            content=b"%PDF-1.4 not html",
        )
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="PDF", website="https://example.com"))
        assert result.ai_maturity_score is None

    @pytest.mark.asyncio
    async def test_fetch_failure_graceful(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://example.com/robots.txt", status_code=404)
        # Use 404 rather than 500 — our retry policy retries 5xx, which would
        # require registering the response N times. 404 is non-transient → fails fast.
        httpx_mock.add_response(url="https://example.com/", status_code=404)
        async with httpx.AsyncClient() as client:
            adapter = WebsiteAdapter(client)
            result = await adapter.enrich(Company(name="Broken", website="https://example.com"))
        assert result.ai_maturity_score is None
