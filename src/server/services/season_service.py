"""
Season Service

Provides season detection and season-specific fashion keywords.
"""

from datetime import datetime
from typing import List


def get_current_season() -> str:
    """Get current season based on month."""
    month = datetime.now().month
    
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:  # 9, 10, 11
        return "fall"


def get_season_keywords(season: str) -> List[str]:
    """Get fashion keywords for a season."""
    keywords = {
        "winter": ["coat", "jacket", "sweater", "layer", "warm", "boot", "scarf"],
        "spring": ["light", "transitional", "jacket", "layer", "fresh", "pastel"],
        "summer": ["short", "linen", "light", "breathable", "sandal", "dress"],
        "fall": ["layer", "jacket", "boot", "sweater", "earth tone", "cozy"]
    }
    return keywords.get(season.lower(), [])

