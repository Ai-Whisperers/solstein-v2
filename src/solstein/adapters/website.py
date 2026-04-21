"""Website adapter — fetches a company's homepage and extracts text signals.

Goal: enrich private companies that have no GitHub org and no public filings.
The adapter is deliberately conservative: one page per company, respect robots.txt,
short timeout, no deep-crawl. We extract text signals; downstream extractors
(e.g., `text_signals.ai_maturity`) derive specific Company fields from them.

Adapter contract reminder:
- Populates Company fields + attaches a Citation per populated field
- Never silently fails; returns company unchanged when fetch fails
- No fake data

This adapter does NOT populate structural fields like revenue/employees/growth
directly from website text — those numbers rarely appear on marketing pages and
when they do they're often out-of-date. Instead it populates the `ai_maturity_score`
via the text signal extractor.
"""

from __future__ import annotations

import re
import urllib.parse
from datetime import date

import httpx
from loguru import logger

from solstein.adapters._retry import http_retry
from solstein.domain import Citation, Company
from solstein.text_signals import ai_maturity_from_text

_UA = "Mozilla/5.0 (compatible; SolsteinBot/2.0; +https://github.com/Ai-Whisperers/solstein-v2)"
_TIMEOUT = 12.0
_MAX_BYTES = 2_000_000  # 2 MB — cut off absurd pages

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)


def _strip_html(html: str) -> str:
    """Minimal HTML → text. Good enough for marketing-page keyword extraction."""
    html = _SCRIPT_STYLE_RE.sub(" ", html)
    text = _TAG_RE.sub(" ", html)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


class WebsiteAdapter:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self._robots_cache: dict[str, bool] = {}

    @property
    def _headers(self) -> dict[str, str]:
        return {"User-Agent": _UA, "Accept": "text/html,application/xhtml+xml"}

    @http_retry
    async def _get(self, url: str) -> httpx.Response:
        response = await self.client.get(
            url, headers=self._headers, timeout=_TIMEOUT, follow_redirects=True
        )
        response.raise_for_status()
        return response

    async def _robots_allows(self, base_url: str) -> bool:
        """Very conservative robots.txt check: if anything disallows everything, skip."""
        if base_url in self._robots_cache:
            return self._robots_cache[base_url]
        robots_url = urllib.parse.urljoin(base_url, "/robots.txt")
        try:
            response = await self.client.get(robots_url, headers=self._headers, timeout=5.0)
        except (httpx.HTTPError, httpx.InvalidURL):
            # No robots.txt reachable → default allow (standard behavior)
            self._robots_cache[base_url] = True
            return True
        if response.status_code != 200:
            self._robots_cache[base_url] = True
            return True
        # Crude parser: look for explicit "Disallow: /" under * UA
        text = response.text.lower()
        allows = True
        in_star_ua = False
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("user-agent:"):
                in_star_ua = line.split(":", 1)[1].strip() == "*"
            elif in_star_ua and line.startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path == "/":
                    allows = False
                    break
        self._robots_cache[base_url] = allows
        return allows

    async def enrich(self, company: Company) -> Company:
        """Fetch homepage, extract text, derive AI-maturity signal."""
        if not company.website:
            return company
        if company.ai_maturity_score is not None:
            return company  # already populated by another adapter

        base_url = str(company.website)
        if not await self._robots_allows(base_url):
            logger.debug(f"robots.txt disallows scraping {base_url}")
            return company

        try:
            response = await self._get(base_url)
        except httpx.HTTPError as e:
            logger.warning(f"website fetch failed for {company.name} ({base_url}): {e}")
            return company

        content_type = response.headers.get("content-type", "")
        if "html" not in content_type.lower():
            return company

        html = response.text[:_MAX_BYTES]
        text = _strip_html(html)

        score, evidence = ai_maturity_from_text(text)
        if score is None:
            return company

        citation = Citation(
            source="website",
            url=base_url,
            retrieved_at=date.today(),
            confidence=min(1.0, evidence / 5.0),
        )
        company.ai_maturity_score = score
        company.citations["ai_maturity_score"] = citation
        return company
