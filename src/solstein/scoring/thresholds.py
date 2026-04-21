"""The single source of truth for classification thresholds.

v1's fatal bug: three files disagreed on where 'phoenix' starts. Same company
landed in different tiers depending on which code path ran. Never again.
If you change a number here, change only here.
"""

from __future__ import annotations

from typing import Final

from solstein.domain import Tier

PHOENIX_MIN: Final[float] = 8.0
DIAMOND_MIN: Final[float] = 6.0
LEAD_MIN: Final[float] = 4.0


def classify(composite_score: float) -> Tier:
    if composite_score >= PHOENIX_MIN:
        return "phoenix"
    if composite_score >= DIAMOND_MIN:
        return "diamond"
    if composite_score >= LEAD_MIN:
        return "lead"
    return "salt"
