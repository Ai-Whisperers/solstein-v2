"""Text-signal extractors.

Pure functions that take a text blob (from a website, careers page, etc.)
and return structured signals. No network, no I/O, no dependencies on httpx.

Keeping these separate from adapters makes them trivially testable and
reusable across any adapter that can produce text.
"""

from __future__ import annotations

import re

# AI-maturity signal keywords, ranked by how specific they are.
# Higher weights = stronger signal of serious AI work.

_HIGH_SIGNAL = {
    "mlops",
    "llmops",
    "production ml",
    "model serving",
    "feature store",
    "vector database",
    "rag pipeline",
    "fine-tuning",
    "prompt engineering",
    "ml platform",
    "ml infrastructure",
}

_MEDIUM_SIGNAL = {
    "machine learning",
    "deep learning",
    "neural network",
    "ai platform",
    "ml model",
    "predictive analytics",
    "nlp",
    "natural language processing",
    "computer vision",
    "transformer",
    "tensorflow",
    "pytorch",
    "hugging face",
    "langchain",
    "llm",
    "gpt",
    "claude",
}

_LOW_SIGNAL = {
    "artificial intelligence",
    "ai-powered",
    "ai-driven",
    "intelligent",
    "automation",
    "data science",
    "data-driven",
    "algorithm",
}

# Anti-signal — marketing fluff that inflates perceived AI without substance.
# When these dominate and higher-signal terms are absent, we de-rate.
_FLUFF = {
    "revolutionary ai",
    "game-changing ai",
    "next-generation ai",
    "cutting-edge ai",
    "ai-first",
}


def _count_occurrences(text: str, terms: set[str]) -> tuple[int, list[str]]:
    """Count how many terms from the set appear in text (case-insensitive).
    Returns (count_of_distinct_terms_found, list_of_found_terms).
    """
    lower = text.lower()
    found = [term for term in terms if term in lower]
    return len(found), found


def ai_maturity_from_text(text: str) -> tuple[float | None, int]:
    """Derive an AI maturity score in [0, 10] from a text blob.

    Returns (score, evidence_count). Returns (None, 0) when text is too short
    or contains no relevant signal at all — we do not guess.

    Weighting:
    - Each HIGH_SIGNAL term: +2.5 points (max 10 via cap)
    - Each MEDIUM_SIGNAL term: +1.0 points
    - Each LOW_SIGNAL term: +0.3 points
    - Each FLUFF term (without MEDIUM/HIGH terms): -0.5 points
    Score is clipped to [0, 10].

    Evidence count is the total distinct terms found — used for citation confidence.
    """
    if len(text) < 200:
        return None, 0

    high_count, _ = _count_occurrences(text, _HIGH_SIGNAL)
    med_count, _ = _count_occurrences(text, _MEDIUM_SIGNAL)
    low_count, _ = _count_occurrences(text, _LOW_SIGNAL)
    fluff_count, _ = _count_occurrences(text, _FLUFF)

    total_evidence = high_count + med_count + low_count
    if total_evidence == 0:
        return 0.0, 0  # explicitly "no AI signal" rather than None — the text exists

    raw = (2.5 * high_count) + (1.0 * med_count) + (0.3 * low_count)

    # De-rate fluff when substance is missing
    if high_count == 0 and med_count == 0 and fluff_count > 0:
        raw -= 0.5 * fluff_count

    score = max(0.0, min(10.0, raw))
    return score, total_evidence


def tech_stack_hints(text: str) -> list[str]:
    """Extract common tech-stack hints from marketing/careers text.

    Non-exhaustive. Used for color commentary in the narrative brief, not for scoring.
    """
    lower = text.lower()
    stacks = {
        "python",
        "typescript",
        "javascript",
        "go",
        "rust",
        "java",
        "ruby",
        "scala",
        "kotlin",
        "swift",
        "react",
        "vue",
        "angular",
        "next.js",
        "node.js",
        "django",
        "flask",
        "fastapi",
        "spring boot",
        "postgres",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "elasticsearch",
        "kafka",
        "aws",
        "gcp",
        "azure",
        "kubernetes",
        "docker",
        "terraform",
    }
    # Use word boundaries to avoid partial matches ("go" in "google").
    found: list[str] = []
    for stack in stacks:
        pattern = r"\b" + re.escape(stack) + r"\b"
        if re.search(pattern, lower):
            found.append(stack)
    return sorted(found)
