"""
Project Chimera - Skills Framework
Reference: skills/README.md - Skill Interface Contract

This module defines the base skill interfaces, data models, and error handling
for the Project Chimera agent system.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ============================================================================
# Data Models (Input/Output Contracts)
# ============================================================================

class SkillInput(BaseModel):
    """Base input schema for all skills.
    
    Reference: skills/README.md - Skill Interface Contract
    """
    skill_id: str = Field(..., description="Unique identifier for the skill")
    version: str = Field(..., description="Semantic version of the skill")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Skill-specific parameters")


class SkillOutput(BaseModel):
    """Base output schema for all skills.
    
    Reference: skills/README.md - Skill Interface Contract
    """
    status: str = Field(..., description="Status: success, error, partial")
    result: Dict[str, Any] = Field(default_factory=dict, description="Skill execution result")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metadata")


class FetchTrendsInput(SkillInput):
    """Input schema for FetchTrendsSkill.
    
    Reference: skills/skill_fetch_trends/README.md - Input Contract
    """
    parameters: Dict[str, Any] = Field(
        default_factory=lambda: {
            "source": "moltbook",
            "time_window": "1h",
            "velocity_threshold": 100,
            "max_results": 50,
            "include_sentiment": True
        }
    )


class FetchTrendsOutput(SkillOutput):
    """Output schema for FetchTrendsSkill.
    
    Reference: skills/skill_fetch_trends/README.md - Output Contract
    """
    result: Dict[str, Any] = Field(
        default_factory=lambda: {
            "trends": []
        }
    )


# ============================================================================
# Error Classes
# ============================================================================

class SkillError(Exception):
    """Base exception for skill errors.
    
    Reference: skills/README.md - Error Handling
    """
    def __init__(
        self, 
        skill_id: str, 
        message: str, 
        details: Optional[Dict] = None
    ):
        self.skill_id = skill_id
        self.message = message
        self.details = details or {}
        super().__init__(f"[{skill_id}] {message}")


class SkillValidationError(SkillError):
    """Raised when input validation fails.
    
    Reference: skills/README.md - Error Handling
    """
    pass


class SkillExecutionError(SkillError):
    """Raised when skill execution fails.
    
    Reference: skills/README.md - Error Handling
    """
    pass


class SkillTimeoutError(SkillError):
    """Raised when skill exceeds timeout.
    
    Reference: skills/README.md - Error Handling
    """
    pass


# ============================================================================
# Base Skill Interface
# ============================================================================

class BaseSkill(ABC):
    """Abstract base class for all skills.
    
    Reference: skills/README.md - Skill Interface Contract
    """
    
    @property
    @abstractmethod
    def skill_id(self) -> str:
        """Unique identifier for the skill."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Semantic version of the skill."""
        pass
    
    @property
    def config(self) -> Dict[str, Any]:
        """Skill configuration."""
        return {
            "skill_id": self.skill_id,
            "version": self.version
        }
    
    @abstractmethod
    async def execute(self, input: SkillInput) -> SkillOutput:
        """Execute the skill with given input.
        
        Args:
            input: Validated skill input data
            
        Returns:
            SkillOutput with status, result, and metadata
        """
        pass


# ============================================================================
# Skill Registry
# ============================================================================

class SkillRegistry:
    """Central registry for all available skills.
    
    Reference: skills/README.md - Skill Registry
    """
    _skills: Dict[str, BaseSkill] = {}
    
    @classmethod
    def get(cls, skill_id: str) -> Optional[BaseSkill]:
        """Get a skill by ID."""
        return cls._skills.get(skill_id)
    
    @classmethod
    def list(cls) -> List[Dict[str, str]]:
        """List all registered skills."""
        return [
            {"skill_id": s.skill_id, "version": s.version}
            for s in cls._skills.values()
        ]
    
    @classmethod
    def register(cls, skill: BaseSkill) -> None:
        """Register a new skill."""
        cls._skills[skill.skill_id] = skill


# ============================================================================
# Fetch Trends Skill Implementation
# ============================================================================

class FetchTrendsSkill(BaseSkill):
    """Skill that fetches trending topics from social platforms.
    
    Reference: skills/skill_fetch_trends/README.md
    
    Capabilities:
    - Fetch trending topics from MoltBook, Twitter, Instagram
    - Filter by velocity threshold and time window
    - Analyze sentiment of trending content
    
    Attributes:
        fetcher: TrendFetcher instance
        velocity_threshold: Minimum velocity to include
    """
    
    def __init__(
        self, 
        fetcher: "TrendFetcher" = None,
        velocity_threshold: float = 100.0
    ):
        from .trend_fetcher import TrendFetcher, InMemoryTrendFetcher
        
        self.fetcher = fetcher or InMemoryTrendFetcher([])
        self.velocity_threshold = float(velocity_threshold)
    
    @property
    def skill_id(self) -> str:
        return "skill_fetch_trends"
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    @property
    def config(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "version": self.version,
            "name": "Trend Fetcher",
            "category": "Perception",
            "parameters": {
                "source": {
                    "type": "string",
                    "enum": ["moltbook", "twitter", "instagram", "all"],
                    "required": True
                },
                "time_window": {
                    "type": "string",
                    "enum": ["1h", "6h", "24h", "7d"],
                    "default": "1h"
                },
                "velocity_threshold": {
                    "type": "integer",
                    "default": 100
                },
                "max_results": {
                    "type": "integer",
                    "default": 50
                }
            }
        }
    
    async def execute(self, input: SkillInput) -> SkillOutput:
        """Execute the fetch trends skill.
        
        Args:
            input: SkillInput with parameters
            
        Returns:
            FetchTrendsOutput with trends data
        """
        import time
        
        start_time = time.time()
        
        # Extract parameters
        params = input.parameters
        source = params.get("source", "moltbook")
        velocity_threshold = params.get("velocity_threshold", self.velocity_threshold)
        max_results = params.get("max_results", 50)
        
        try:
            # Fetch trends from source
            raw_trends = self.fetcher.fetch_trends(source)
            
            # Detect high velocity trends
            high_velocity_trends = self.fetcher.detect_high_velocity(
                raw_trends, 
                velocity_threshold
            )
            
            # Limit results
            trends = high_velocity_trends[:max_results]
            
            # Calculate metadata
            duration_ms = int((time.time() - start_time) * 1000)
            
            return FetchTrendsOutput(
                status="success",
                result={"trends": trends},
                metadata={
                    "fetch_duration_ms": duration_ms,
                    "total_scanned": len(raw_trends),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
            
        except Exception as e:
            return FetchTrendsOutput(
                status="error",
                result={"error": str(e)},
                metadata={
                    "fetch_duration_ms": int((time.time() - start_time) * 1000),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
    
    def detect_and_alert(self, source: str = "moltbook") -> List[Dict]:
        """Legacy method for detecting high-velocity trends.
        
        This method is kept for backward compatibility.
        """
        trends = self.fetcher.fetch_trends(source)
        return self.fetcher.detect_high_velocity(trends, self.velocity_threshold)
