# Project Chimera - Skills Framework

## Overview

Skills are **reusable capability packages** that agents can invoke to perform specific tasks. Unlike MCP servers (external connectors), Skills are internal, versioned modules that encapsulate domain-specific functionality.

## Philosophy

> **"Skills are what agents DO. MCP servers are what agents USE to connect."**

- **Skills** (`skills/`): Implementation packages called by agents
- **MCP Servers**: External bridges (databases, APIs, file systems)
- **Clear Separation**: Skills should not contain MCP client logic

## Skill Structure

```
skills/
├── README.md                          # This file
├── skill_fetch_trends/               # Trend detection skill
│   ├── README.md                      # Skill documentation
│   ├── __init__.py                    # Skill interface
│   ├── config.json                    # Configuration schema
│   └── requirements.txt               # Skill-specific deps
├── skill_generate_content/           # Content generation skill
│   ├── README.md
│   ├── __init__.py
│   ├── config.json
│   └── requirements.txt
└── skill_publish_post/               # Social posting skill
    ├── README.md
    ├── __init__.py
    ├── config.json
    └── requirements.txt
```

## Skill Interface Contract

Every skill MUST implement:

```python
from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class SkillInput(BaseModel):
    """Base input schema for all skills"""
    skill_id: str
    version: str
    parameters: Dict[str, Any]

class SkillOutput(BaseModel):
    """Base output schema for all skills"""
    status: str
    result: Dict[str, Any]
    metadata: Dict[str, Any]

class BaseSkill(ABC):
    """Abstract base class for all skills"""
    
    @property
    @abstractmethod
    def skill_id(self) -> str:
        """Unique identifier for the skill"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Semantic version of the skill"""
        pass
    
    @abstractmethod
    async def execute(self, input: SkillInput) -> SkillOutput:
        """Execute the skill with given input"""
        pass
```

## Skill Categories

### Category 1: Perception Skills
Skills that gather data from external sources:
- `skill_fetch_trends` - Monitor platforms for trending topics
- `skill_analyze_sentiment` - Analyze sentiment of content
- `skill_transcribe_audio` - Convert audio to text

### Category 2: Generation Skills
Skills that create new content:
- `skill_generate_content` - Create posts, scripts, images
- `skill_summarize_text` - Condense long-form content
- `skill_create_hashtags` - Generate relevant hashtags

### Category 3: Action Skills
Skills that interact with external systems:
- `skill_publish_post` - Post content to social platforms
- `skill_engage_comments` - Respond to audience interactions
- `skill_transfer_funds` - Handle financial transactions

## Configuration Schema

Each skill must have a `config.json`:

```json
{
  "skill_id": "skill_fetch_trends",
  "version": "0.1.0",
  "name": "Trend Fetcher",
  "description": "Fetches trending topics from social platforms",
  "parameters": {
    "source": {
      "type": "string",
      "required": true,
      "enum": ["moltbook", "twitter", "instagram"]
    },
    "time_window": {
      "type": "string",
      "required": false,
      "default": "1h"
    }
  },
  "outputs": {
    "trends": {
      "type": "array",
      "description": "List of trending items"
    }
  },
  "permissions": ["network:read"],
  "rate_limits": {
    "requests_per_minute": 10
  }
}
```

## Usage Example

```python
from agentic.skills import SkillRegistry
from skills.skill_fetch_trends import SkillFetchTrends

# Initialize and execute skill
skill = SkillFetchTrends(config={"source": "moltbook"})
result = await skill.execute(
    SkillInput(
        skill_id="skill_fetch_trends",
        version="0.1.0",
        parameters={"source": "moltbook", "limit": 50}
    )
)
```

## Skill Registry

The global skill registry tracks available skills:

```python
class SkillRegistry:
    """Central registry for all available skills"""
    
    @classmethod
    def get(cls, skill_id: str) -> BaseSkill:
        """Get a skill by ID"""
        pass
    
    @classmethod
    def list(cls) -> List[Dict[str, str]]:
        """List all registered skills"""
        pass
    
    @classmethod
    def register(cls, skill: BaseSkill) -> None:
        """Register a new skill"""
        pass
```

## Development Guidelines

### 1. Single Responsibility
Each skill should do ONE thing well.

### 2. Versioning
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Breaking changes require MAJOR version bump
- Document version history in skill README

### 3. Testing
- Each skill MUST have unit tests
- Tests in `tests/test_skills/` matching skill structure
- Mock external dependencies

### 4. Documentation
Every skill must include:
- Purpose and capabilities
- Input/output JSON schemas
- Example usage
- Error handling guide

## Error Handling

```python
class SkillError(Exception):
    """Base exception for skill errors"""
    def __init__(self, skill_id: str, message: str, details: Dict = None):
        self.skill_id = skill_id
        self.message = message
        self.details = details or {}

class SkillValidationError(SkillError):
    """Raised when input validation fails"""
    pass

class SkillExecutionError(SkillError):
    """Raised when skill execution fails"""
    pass

class SkillTimeoutError(SkillError):
    """Raised when skill exceeds timeout"""
    pass
```

## Next Steps

- [ ] Implement `skill_fetch_trends`
- [ ] Implement `skill_generate_content`
- [ ] Implement `skill_publish_post`
- [ ] Add skill testing framework
- [ ] Create skill discovery service
- [ ] Implement skill versioning system
