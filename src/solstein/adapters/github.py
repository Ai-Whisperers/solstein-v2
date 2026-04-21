"""GitHub adapter — real, httpx-native, no stubs.

Signal extracted: 90-day commit count + total stars across the org.
Auth is via GITHUB_TOKEN env var. Without a token you get unauth rate limits
(60/hour) — fine for dev, do not run a universe of 200 without a token.
"""

from __future__ import annotations

import os
from datetime import UTC, date, datetime, timedelta

import httpx
from loguru import logger

from solstein.adapters._retry import http_retry
from solstein.domain import Citation, Company

GITHUB_API = "https://api.github.com"


class GitHubAdapter:
    def __init__(self, client: httpx.AsyncClient, token: str | None = None) -> None:
        self.client = client
        self.token = token or os.getenv("GITHUB_TOKEN")

    @property
    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    @http_retry
    async def _get(self, path: str, params: dict[str, str] | None = None) -> httpx.Response:
        url = f"{GITHUB_API}{path}"
        response = await self.client.get(url, headers=self._headers, params=params, timeout=15.0)
        response.raise_for_status()
        return response

    async def enrich(self, company: Company) -> Company:
        """Populate github_* fields and citations. Return company unmodified if no org."""
        if not company.github_org:
            return company

        try:
            repos = await self._list_repos(company.github_org)
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 404:
                logger.warning(f"GitHub org '{company.github_org}' not found")
                return company
            if status == 403 and "rate limit" in e.response.text.lower():
                logger.warning(
                    f"GitHub rate-limited while enriching '{company.github_org}' — "
                    "set GITHUB_TOKEN for 5000 req/hour"
                )
                return company
            logger.error(f"GitHub error for {company.github_org}: {e}")
            raise

        stars_total = 0
        for r in repos:
            value = r.get("stargazers_count")
            if isinstance(value, int):
                stars_total += value
        since = (datetime.now(UTC) - timedelta(days=90)).isoformat()
        commits = 0
        for repo in repos[:20]:  # cap: top 20 repos by default sort
            repo_name = str(repo["name"])
            commits += await self._count_recent_commits(company.github_org, repo_name, since)

        today = date.today()
        citation = Citation(
            source="github", url=f"https://github.com/{company.github_org}", retrieved_at=today
        )

        company.github_stars_total = stars_total
        company.github_commits_last_90d = commits
        company.citations["github_stars_total"] = citation
        company.citations["github_commits_last_90d"] = citation
        return company

    async def _list_repos(self, org: str) -> list[dict[str, object]]:
        response = await self._get(
            f"/orgs/{org}/repos", params={"per_page": "100", "type": "public"}
        )
        return list(response.json())

    async def _count_recent_commits(self, org: str, repo: str, since_iso: str) -> int:
        """Count commits in the default branch since a date. Single page (100 max)."""
        try:
            response = await self._get(
                f"/repos/{org}/{repo}/commits",
                params={"since": since_iso, "per_page": "100"},
            )
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            # 409 = empty repo; 404 = gone; 403 rate limit = treat as zero and move on.
            if status in (404, 409):
                return 0
            if status == 403 and "rate limit" in e.response.text.lower():
                logger.warning(f"GitHub rate-limited on {org}/{repo}")
                return 0
            raise
        return len(response.json())
