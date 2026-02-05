from agentic.trend_fetcher import InMemoryTrendFetcher


def test_detect_high_velocity():
    trends = [
        {"keyword": "fast", "velocity": 12},
        {"keyword": "slow", "velocity": 3},
    ]
    f = InMemoryTrendFetcher(trends)
    fetched = f.fetch_trends()
    results = f.detect_high_velocity(fetched, threshold=10)

    assert len(results) == 1
    assert results[0]["keyword"] == "fast"
