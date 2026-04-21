"""Tests for the HTTP cache."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from pytest_httpx import HTTPXMock

from solstein.http_cache import CachedClient, _canonical_key


class TestCanonicalKey:
    def test_same_request_same_key(self) -> None:
        k1 = _canonical_key("GET", "https://example.com", {"q": "test"}, has_auth=False)
        k2 = _canonical_key("GET", "https://example.com", {"q": "test"}, has_auth=False)
        assert k1 == k2

    def test_different_url_different_key(self) -> None:
        k1 = _canonical_key("GET", "https://a.com", None, has_auth=False)
        k2 = _canonical_key("GET", "https://b.com", None, has_auth=False)
        assert k1 != k2

    def test_different_params_different_key(self) -> None:
        k1 = _canonical_key("GET", "https://example.com", {"q": "a"}, has_auth=False)
        k2 = _canonical_key("GET", "https://example.com", {"q": "b"}, has_auth=False)
        assert k1 != k2

    def test_auth_presence_affects_key(self) -> None:
        k1 = _canonical_key("GET", "https://example.com", None, has_auth=False)
        k2 = _canonical_key("GET", "https://example.com", None, has_auth=True)
        assert k1 != k2


class TestCachedClient:
    @pytest.mark.asyncio
    async def test_bypasses_when_no_cache_dir(self, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(url="https://example.com/", text="body", status_code=200)
        async with httpx.AsyncClient() as inner:
            cached = CachedClient(inner, cache_dir=None)
            response = await cached.get("https://example.com/")
        assert response.status_code == 200
        assert response.text == "body"

    @pytest.mark.asyncio
    async def test_first_request_hits_network_second_uses_cache(
        self,
        httpx_mock: HTTPXMock,
        tmp_path: Path,
    ) -> None:
        httpx_mock.add_response(url="https://example.com/", text="hello", status_code=200)

        async with httpx.AsyncClient() as inner:
            cached = CachedClient(inner, cache_dir=tmp_path / "cache")
            first = await cached.get("https://example.com/")
            second = await cached.get("https://example.com/")

        assert first.status_code == 200
        assert first.text == "hello"
        assert second.status_code == 200
        assert second.text == "hello"
        # Network was hit exactly once; second call came from cache
        assert len(httpx_mock.get_requests()) == 1

    @pytest.mark.asyncio
    async def test_caches_4xx_not_5xx(
        self,
        httpx_mock: HTTPXMock,
        tmp_path: Path,
    ) -> None:
        # 404 should be cached (stable non-error)
        httpx_mock.add_response(url="https://example.com/missing", status_code=404)
        async with httpx.AsyncClient() as inner:
            cached = CachedClient(inner, cache_dir=tmp_path / "cache")
            r1 = await cached.get("https://example.com/missing")
            r2 = await cached.get("https://example.com/missing")
        assert r1.status_code == 404
        assert r2.status_code == 404
        assert len(httpx_mock.get_requests()) == 1

    @pytest.mark.asyncio
    async def test_different_params_cache_separately(
        self,
        httpx_mock: HTTPXMock,
        tmp_path: Path,
    ) -> None:
        httpx_mock.add_response(url="https://example.com/?q=a", text="A")
        httpx_mock.add_response(url="https://example.com/?q=b", text="B")

        async with httpx.AsyncClient() as inner:
            cached = CachedClient(inner, cache_dir=tmp_path / "cache")
            r1 = await cached.get("https://example.com/", params={"q": "a"})
            r2 = await cached.get("https://example.com/", params={"q": "b"})

        assert r1.text == "A"
        assert r2.text == "B"

    @pytest.mark.asyncio
    async def test_stale_entries_refetch(
        self,
        httpx_mock: HTTPXMock,
        tmp_path: Path,
    ) -> None:
        httpx_mock.add_response(url="https://example.com/", text="first")
        httpx_mock.add_response(url="https://example.com/", text="second")

        async with httpx.AsyncClient() as inner:
            cached = CachedClient(inner, cache_dir=tmp_path / "cache", ttl_seconds=-1)
            # ttl < 0 → every entry stale, every request refetches
            r1 = await cached.get("https://example.com/")
            r2 = await cached.get("https://example.com/")

        assert r1.text == "first"
        assert r2.text == "second"
        assert len(httpx_mock.get_requests()) == 2
