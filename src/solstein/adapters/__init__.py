"""Data source adapters. One module per real external source.

Contract for any adapter:
1. Async. Takes httpx.AsyncClient. Returns None if not found, raises on real errors.
2. Populates Company fields *and* attaches a Citation for each field it sets.
3. Never silently fails. Never returns fake data.
"""

from solstein.adapters.companies_house import CompaniesHouseAdapter
from solstein.adapters.github import GitHubAdapter
from solstein.adapters.sec_edgar import SecEdgarAdapter
from solstein.adapters.website import WebsiteAdapter

__all__ = ["CompaniesHouseAdapter", "GitHubAdapter", "SecEdgarAdapter", "WebsiteAdapter"]
