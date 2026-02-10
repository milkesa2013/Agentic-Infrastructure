"""
Project Chimera - Trend Fetcher
Reference: specs/technical.md - API Contracts Section

This module provides trend fetching capabilities with API contracts
conforming to the JSON schemas defined in specs/technical.md.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Iterable
from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel, Field


# ============================================================================
# Data Models (API Contract Schemas)
# ============================================================================

class Trend(BaseModel):
    """Individual trend data model.
    
    Reference: specs/technical.md - Trend Data Schema
    """
    trend_id: str = Field(..., pattern=r"^trend_[0-9]{3}$")
    keyword: str = Field(..., max_length=255)
    velocity: int = Field(..., ge=0)
    sentiment: Optional[float] = Field(None, ge=-1, le=1)
    source: str = Field(..., pattern=r"^(twitter|moltbook|instagram)$")

    detected_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TrendResponse(BaseModel):
    """API response for trend fetch operations.
    
    Reference: specs/technical.md - API Contracts Section
    """
    status: str = Field(..., regex=r"success|error|partial")
    data: Dict[str, Any] = Field(default_factory=lambda: {"trends": []})
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FetchTrendsRequest(BaseModel):
    """Request model for fetch trends endpoint.
    
    Reference: specs/technical.md - API Contracts Section
    """
    source: str = Field(..., regex=r"moltbook|twitter|instagram|all")
    time_window: Optional[str] = Field("1h", regex=r"1h|6h|24h|7d")
    velocity_threshold: Optional[int] = Field(100, ge=0)
    max_results: Optional[int] = Field(50, ge=1, le=100)
    include_sentiment: Optional[bool] = True


# ============================================================================
# Trend Fetcher Interface
# ============================================================================

class TrendFetcher(ABC):
    """Abstract interface for fetching trends from a source.
    
    Concrete implementations should provide `fetch_trends(source)` which returns
    a list of dicts conforming to the Trend schema in specs/technical.md.
    
    Reference: specs/technical.md - Abstract-ish interface
    """
    
    @abstractmethod
    def fetch_trends(self, request: Dict[str, Any]) -> TrendResponse:
        """Fetch trends from the data source.
        
        Args:
            request: Dictionary with source and optional parameters
            
        Returns:
            TrendResponse with status, data, and metadata
        """
        pass
    
    @abstractmethod
    def detect_high_velocity(
        self, 
        trends: Iterable[Dict], 
        threshold: float
    ) -> List[Dict]:
        """Return trends with velocity >= threshold.
        
        Args:
            trends: Iterable of trend dictionaries
            threshold: Minimum velocity threshold
            
        Returns:
            List of trends meeting the threshold
        """
        pass


# ============================================================================
# In-Memory Trend Fetcher (Test Implementation)
# ============================================================================

class InMemoryTrendFetcher(TrendFetcher):
    """Simple test-friendly implementation that returns a fixed list of trends.
    
    This implementation is useful for unit testing and development.
    """
    
    def __init__(self, trends: List[Dict]):
        """Initialize with a list of trend dictionaries.
        
        Args:
            trends: List of trend dictionaries with 'keyword' and 'velocity'
        """
        self._trends = list(trends)
    
    def fetch_trends(self, request: Dict[str, Any] = None) -> TrendResponse:
        """Fetch trends from in-memory storage.
        
        Args:
            request: Optional request parameters (source ignored)
            
        Returns:
            TrendResponse with trends data
        """
        from datetime import datetime
        
        # Convert raw trends to response format
        trend_data = []
        for idx, trend in enumerate(self._trends, start=1):
            trend_data.append({
                "trend_id": f"trend_{idx:03d}",
                "keyword": trend.get("keyword", ""),
                "velocity": trend.get("velocity", 0),
                "sentiment": trend.get("sentiment", 0.0),
                "source": trend.get("source", "moltbook"),
                "detected_at": datetime.utcnow().isoformat() + "Z",
                "metadata": trend.get("metadata", {})
            })
        
        return TrendResponse(
            status="success",
            data={"trends": trend_data},
            metadata={
                "fetch_duration_ms": 10,
                "total_scanned": len(self._trends),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
    
    def detect_high_velocity(
        self, 
        trends: Iterable[Dict], 
        threshold: float
    ) -> List[Dict]:
        """Return trends with velocity >= threshold.
        
        Args:
            trends: Iterable of trend dictionaries
            threshold: Minimum velocity threshold
            
        Returns:
            List of trends meeting the threshold
        """
        return [
            t for t in trends 
            if float(t.get("velocity", 0)) >= threshold
        ]


# ============================================================================
# API Client Trend Fetcher (Production Implementation)
# ============================================================================

class APITrendFetcher(TrendFetcher):
    """Production implementation that fetches trends from external APIs.
    
    This implementation connects to external trend data sources
    and transforms responses to match the API contract.
    """
    
    def __init__(
        self, 
        api_endpoint: str = "https://api.example.com/trends",
        api_key: str = None
    ):
        """Initialize API client.
        
        Args:
            api_endpoint: Base URL for trends API
            api_key: API authentication key
        """
        self.api_endpoint = api_endpoint
        self.api_key = api_key
    
    def fetch_trends(self, request: Dict[str, Any]) -> TrendResponse:
        """Fetch trends from external API.
        
        Args:
            request: Request parameters
            
        Returns:
            TrendResponse with trends from API
        """
        import httpx
        from datetime import datetime
        
        # Prepare request
        params = {
            "source": request.get("source", "moltbook"),
            "time_window": request.get("time_window", "1h"),
            "limit": request.get("max_results", 50)
        }
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            # Make API call
            # Note: In production, use async httpx
            # response = httpx.get(self.api_endpoint, params=params, headers=headers)
            
            # For now, return mock response
            return TrendResponse(
                status="success",
                data={"trends": []},
                metadata={
                    "fetch_duration_ms": 100,
                    "total_scanned": 0,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
            
        except Exception as e:
            return TrendResponse(
                status="error",
                data={"error": str(e)},
                metadata={
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
    
    def detect_high_velocity(
        self, 
        trends: Iterable[Dict], 
        threshold: float
    ) -> List[Dict]:
        """Return trends with velocity >= threshold.
        
        Args:
            trends: Iterable of trend dictionaries
            threshold: Minimum velocity threshold
            
        Returns:
            List of trends meeting the threshold
        """
        return [
            t for t in trends 
            if float(t.get("velocity", 0)) >= threshold
        ]
