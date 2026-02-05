from __future__ import annotations
from typing import List, Dict
from .trend_fetcher import TrendFetcher

class Skill:
    """Base skill interface."""

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class FetchTrendsSkill(Skill):
    """Skill that uses a TrendFetcher to detect high-velocity trends and return them.

    This keeps business logic separate from transport/notifications so it is easy
    to unit test and integrate.
    """

    def __init__(self, fetcher: TrendFetcher, velocity_threshold: float = 10.0):
        self.fetcher = fetcher
        self.velocity_threshold = float(velocity_threshold)

    def detect_and_alert(self, source: str = "moltbook") -> List[Dict]:
        trends = self.fetcher.fetch_trends(source)
        return self.fetcher.detect_high_velocity(trends, self.velocity_threshold)
