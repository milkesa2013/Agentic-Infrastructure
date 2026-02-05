from __future__ import annotations
from typing import List, Dict, Iterable

class TrendFetcher:
    """Abstract-ish interface for fetching trends from a source.

    Concrete implementations should provide `fetch_trends(source)` which returns
    a list of dicts each containing at least 'keyword' and 'velocity'.
    """

    def fetch_trends(self, source: str) -> List[Dict]:
        raise NotImplementedError

    def detect_high_velocity(self, trends: Iterable[Dict], threshold: float) -> List[Dict]:
        """Return trends with velocity >= threshold."""
        return [t for t in trends if float(t.get("velocity", 0)) >= threshold]


class InMemoryTrendFetcher(TrendFetcher):
    """Simple test-friendly implementation that returns a fixed list of trends."""

    def __init__(self, trends: List[Dict]):
        self._trends = list(trends)

    def fetch_trends(self, source: str = "inmemory") -> List[Dict]:
        # 'source' ignored for this simple implementation
        return list(self._trends)
