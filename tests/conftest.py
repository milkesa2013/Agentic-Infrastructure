"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import MagicMock, AsyncMock


@pytest.fixture
def mock_mcp_message():
    """Mock MCP message for testing."""
    return {
        "mcp_version": "1.0",
        "message_type": "task_request",
        "sender": "test_agent",
        "recipient": "target_agent",
        "timestamp": "2024-01-01T00:00:00Z",
        "payload": {
            "task_id": "test-uuid",
            "action": "test_action",
            "parameters": {},
            "artifacts": []
        },
        "trace_id": "test-correlation-id"
    }


@pytest.fixture
def sample_trend():
    """Sample trend data for testing."""
    return {
        "id": "trend-uuid",
        "topic": "AI Content Creation",
        "platform": "twitter",
        "volume": 10000,
        "velocity": 0.85,
        "relevance_score": 0.92,
        "engagement_rate": 0.15,
        "discovered_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_script():
    """Sample script data for testing."""
    return {
        "id": "script-uuid",
        "title": "AI Content Creation Guide",
        "content": [
            {"timestamp": 0, "text": "Hook: AI is changing content creation..."},
            {"timestamp": 5, "text": "Main point: Here's how it works..."},
            {"timestamp": 30, "text": "Conclusion: Start today!"}
        ],
        "duration_seconds": 60,
        "style": "educational",
        "platform": "youtube"
    }


@pytest.fixture
def mock_guardian_decision():
    """Sample guardian decision for testing."""
    return {
        "decision": "approve",
        "scores": {
            "brand_safety": 0.95,
            "security": 1.0,
            "compliance": 0.98
        },
        "issues": [],
        "requires_human": False
    }
