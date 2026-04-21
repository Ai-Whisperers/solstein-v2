"""Shared retry policy for adapters.

Only retry transient errors. A 4xx is almost never transient — don't burn
three attempts on a permanent auth or not-found failure.
"""

from __future__ import annotations

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, httpx.TimeoutException | httpx.NetworkError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return 500 <= exc.response.status_code < 600
    return False


http_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=10),
    retry=retry_if_exception(_is_transient),
    reraise=True,
)
