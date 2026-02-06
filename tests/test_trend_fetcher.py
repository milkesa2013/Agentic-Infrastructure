"""
Test: Trend Fetcher API Contract
Reference: specs/technical.md - API Contracts Section

This test verifies that the trend fetcher implementation
conforms to the JSON schema defined in specs/technical.md.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime


# Expected Schema from specs/technical.md
TREND_SCHEMA = {
    "type": "object",
    "properties": {
        "trend_id": {"type": "string", "pattern": "^trend_[0-9]{3}$"},
        "keyword": {"type": "string", "maxLength": 255},
        "velocity": {"type": "integer", "minimum": 0},
        "sentiment": {"type": "number", "minimum": -1, "maximum": 1},
        "source": {"type": "string", "enum": ["twitter", "moltbook", "instagram"]},
        "detected_at": {"type": "string", "format": "date-time"},
        "metadata": {"type": "object"}
    },
    "required": ["trend_id", "keyword", "velocity", "detected_at"]
}


class TestTrendFetcherAPIContract:
    """Test suite for Trend Fetcher API contract compliance."""

    def test_fetch_trends_response_matches_spec_schema(self):
        """
        Test that fetch_trends returns data matching the API contract
        defined in specs/technical.md
        
        Expected Response Schema:
        {
            "status": "success",
            "data": {
                "trends": [...]
            },
            "metadata": {...}
        }
        """
        # Import from the agentic module
        from agentic.trend_fetcher import TrendFetcher
        
        fetcher = TrendFetcher()
        
        # Call the fetch method
        result = fetcher.fetch_trends({"source": "moltbook"})
        
        # Verify response structure matches spec
        assert "status" in result, "Response must have 'status' field"
        assert "data" in result, "Response must have 'data' field"
        assert "metadata" in result, "Response must have 'metadata' field"
        
        assert result["status"] in ["success", "error", "partial"], \
            "Status must be one of: success, error, partial"

    def test_trend_data_structure_conforms_to_schema(self):
        """
        Test that individual trend items conform to the Trend schema
        from specs/technical.md
        """
        from agentic.trend_fetcher import TrendFetcher
        
        fetcher = TrendFetcher()
        result = fetcher.fetch_trends({"source": "moltbook"})
        
        if result["status"] == "success":
            trends = result["data"]["trends"]
            
            for trend in trends:
                # Check required fields exist
                assert "trend_id" in trend, "Trend must have 'trend_id'"
                assert "keyword" in trend, "Trend must have 'keyword'"
                assert "velocity" in trend, "Trend must have 'velocity'"
                assert "detected_at" in trend, "Trend must have 'detected_at'"
                
                # Validate field types
                assert isinstance(trend["trend_id"], str), \
                    "trend_id must be a string"
                assert isinstance(trend["keyword"], str), \
                    "keyword must be a string"
                assert isinstance(trend["velocity"], int), \
                    "velocity must be an integer"
                assert trend["velocity"] >= 0, \
                    "velocity must be non-negative"
                
                # Validate optional fields
                if "sentiment" in trend:
                    assert -1 <= trend["sentiment"] <= 1, \
                        "sentiment must be between -1 and 1"
                
                if "source" in trend:
                    assert trend["source"] in ["twitter", "moltbook", "instagram"], \
                        "source must be a valid platform"

    def test_fetch_request_accepts_valid_parameters(self):
        """
        Test that fetch_trends accepts parameters according to the
        Input Contract in specs/technical.md
        
        Required: source (string)
        Optional: time_window, velocity_threshold, max_results
        """
        from agentic.trend_fetcher import TrendFetcher
        
        fetcher = TrendFetcher()
        
        # Valid requests should not raise
        valid_requests = [
            {"source": "moltbook"},
            {"source": "all"},
            {"source": "twitter", "time_window": "1h"},
            {"source": "instagram", "velocity_threshold": 100},
            {"source": "moltbook", "max_results": 50},
        ]
        
        for request in valid_requests:
            result = fetcher.fetch_trends(request)
            assert "status" in result

    def test_fetch_response_includes_required_metadata(self):
        """
        Test that response metadata includes required fields
        per the API contract.
        """
        from agentic.trend_fetcher import TrendFetcher
        
        fetcher = TrendFetcher()
        result = fetcher.fetch_trends({"source": "moltbook"})
        
        metadata = result.get("metadata", {})
        
        assert "fetch_duration_ms" in metadata, \
            "Metadata must include 'fetch_duration_ms'"
        assert "timestamp" in metadata, \
            "Metadata must include 'timestamp'"


class TestTrendDetection:
    """Test trend detection functionality."""

    def test_detect_high_velocity_trends(self):
        """
        Test that high velocity trends are correctly identified.
        Reference: specs/functional.md - Trend Detection requirement
        """
        from agentic.trend_fetcher import TrendFetcher
        
        fetcher = TrendFetcher()
        
        # Test data with varying velocities
        test_trends = [
            {"keyword": "trending1", "velocity": 500},
            {"keyword": "trending2", "velocity": 150},
            {"keyword": "trending3", "velocity": 50},
        ]
        
        # Configure fetcher with test data
        fetcher.set_trends(test_trends)
        
        # Detect high velocity trends
        high_velocity = fetcher.detect_high_velocity(threshold=100)
        
        # Should identify 2 trends above threshold
        assert len(high_velocity) == 2
        keywords = [t["keyword"] for t in high_velocity]
        assert "trending1" in keywords
        assert "trending2" in keywords
        assert "trending3" not in keywords
