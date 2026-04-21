"""File-backed HTTP cache for adapter calls.

Re-running the pipeline against the same universe should not hammer external
APIs. This module provides a simple disk cache keyed on (method, url, params,
auth-presence). TTL defaulted conservatively.

Design notes:
- Filesystem cache, not Redis — we're single-machine and deployment simplicity > scale.
- Cache is keyed by a SHA256 of the canonicalized request; collisions are impossible.
- TTL per adapter: override via env vars if needed.
- Cache respects 4xx responses too (don't re-query a 404 endlessly).
- Cache does NOT store response headers — just body + status. Adapters that need
  header info should not use the cache (or we extend the format).

This is an OPT-IN wrapper: if the env var SOLSTEIN_HTTP_CACHE_DIR is set,
the pipeline wires through the cached client. Otherwise adapters hit the network
directly as before.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from loguru import logger

CACHE_DIR_ENV = "SOLSTEIN_HTTP_CACHE_DIR"
DEFAULT_TTL_SECONDS = 6 * 60 * 60  # 6 hours


@dataclass(frozen=True)
class CacheEntry:
    status_code: int
    body: bytes
    cached_at: float  # unix seconds


def _canonical_key(
    method: str,
    url: str,
    params: dict[str, str] | None,
    has_auth: bool,
) -> str:
    parts = {
        "method": method.upper(),
        "url": url,
        "params": sorted((params or {}).items()),
        "auth": has_auth,
    }
    blob = json.dumps(parts, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


class CachedClient:
    """Thin wrapper around httpx.AsyncClient that caches GET responses on disk.

    Same public surface as the subset of httpx.AsyncClient that adapters use.
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
        cache_dir: Path | None = None,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
    ) -> None:
        self.client = client
        self.cache_dir = cache_dir or _default_cache_dir()
        self.ttl_seconds = ttl_seconds
        if self.cache_dir is not None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, key: str) -> Path | None:
        if self.cache_dir is None:
            return None
        return self.cache_dir / f"{key}.json"

    def _load(self, key: str) -> CacheEntry | None:
        path = self._path_for(key)
        if path is None or not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        entry = CacheEntry(
            status_code=int(data["status_code"]),
            body=bytes.fromhex(data["body_hex"]),
            cached_at=float(data["cached_at"]),
        )
        if time.time() - entry.cached_at > self.ttl_seconds:
            return None  # stale
        return entry

    def _store(self, key: str, entry: CacheEntry) -> None:
        path = self._path_for(key)
        if path is None:
            return
        data = {
            "status_code": entry.status_code,
            "body_hex": entry.body.hex(),
            "cached_at": entry.cached_at,
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data), encoding="utf-8")
        tmp.rename(path)  # atomic on POSIX

    async def get(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        timeout: float = 15.0,
        auth: Any = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Cached GET. Cache bypass if SOLSTEIN_HTTP_CACHE_DIR is unset."""
        if self.cache_dir is None:
            return await self.client.get(
                url, headers=headers, params=params, timeout=timeout, auth=auth, **kwargs
            )

        key = _canonical_key("GET", url, params, has_auth=auth is not None)
        hit = self._load(key)
        if hit is not None:
            logger.debug(f"http_cache HIT {url}")
            # Reconstruct an httpx.Response from cached bytes.
            return httpx.Response(status_code=hit.status_code, content=hit.body)

        logger.debug(f"http_cache MISS {url}")
        response = await self.client.get(
            url, headers=headers, params=params, timeout=timeout, auth=auth, **kwargs
        )
        # Cache both successes and 4xx — 4xx are stable and deserve to avoid re-fetching.
        if 200 <= response.status_code < 500:
            self._store(
                key,
                CacheEntry(
                    status_code=response.status_code,
                    body=response.content,
                    cached_at=time.time(),
                ),
            )
        return response


def _default_cache_dir() -> Path | None:
    raw = os.environ.get(CACHE_DIR_ENV)
    if not raw:
        return None
    return Path(raw).expanduser()
