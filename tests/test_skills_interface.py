from agentic.trend_fetcher import InMemoryTrendFetcher
from agentic.skills import FetchTrendsSkill


def test_fetch_trends_skill_detects_and_returns_trends():
    trends = [{"keyword": "x", "velocity": 15}]
    fetcher = InMemoryTrendFetcher(trends)
    skill = FetchTrendsSkill(fetcher, velocity_threshold=10)

    results = skill.detect_and_alert()

    assert results == trends
