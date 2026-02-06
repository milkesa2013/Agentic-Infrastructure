# Skill: Fetch Trends

## Overview
Monitors social media platforms for trending topics and high-velocity keywords. This is the primary perception skill for Chimera's content pipeline.

## Skill Information
- **Skill ID**: `skill_fetch_trends`
- **Version**: `0.1.0`
- **Category**: Perception
- **Author**: Project Chimera Team

## Capabilities
- Fetch trending topics from MoltBook, Twitter, Instagram
- Filter by velocity threshold and time window
- Analyze sentiment of trending content
- Track hashtag performance

## Input Contract

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FetchTrendsInput",
  "type": "object",
  "properties": {
    "source": {
      "type": "string",
      "enum": ["moltbook", "twitter", "instagram", "all"],
      "description": "Platform to fetch trends from"
    },
    "time_window": {
      "type": "string",
      "enum": ["1h", "6h", "24h", "7d"],
      "default": "1h",
      "description": "Time window for trend detection"
    },
    "velocity_threshold": {
      "type": "integer",
      "minimum": 0,
      "default": 100,
      "description": "Minimum velocity score to include"
    },
    "max_results": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 50,
      "description": "Maximum number of trends to return"
    },
    "include_sentiment": {
      "type": "boolean",
      "default": true,
      "description": "Include sentiment analysis"
    }
  },
  "required": ["source"]
}
```

### Example Input
```json
{
  "source": "moltbook",
  "time_window": "1h",
  "velocity_threshold": 150,
  "max_results": 30,
  "include_sentiment": true
}
```

## Output Contract

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FetchTrendsOutput",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "error", "partial"]
    },
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "trend_id": {"type": "string"},
          "keyword": {"type": "string"},
          "velocity": {"type": "integer"},
          "sentiment": {"type": "number"},
          "source": {"type": "string"},
          "detected_at": {"type": "string", "format": "date-time"},
          "metadata": {"type": "object"}
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "fetch_duration_ms": {"type": "integer"},
        "total_scanned": {"type": "integer"},
        "timestamp": {"type": "string", "format": "date-time"}
      }
    }
  },
  "required": ["status", "trends"]
}
```

### Example Output
```json
{
  "status": "success",
  "trends": [
    {
      "trend_id": "trend_001",
      "keyword": "autonomous_ai",
      "velocity": 1500,
      "sentiment": 0.75,
      "source": "moltbook",
      "detected_at": "2024-01-15T10:30:00Z",
      "metadata": {
        "hashtag_volume": 50000,
        "growth_rate": 2.5
      }
    }
  ],
  "metadata": {
    "fetch_duration_ms": 245,
    "total_scanned": 10000,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Usage Example

```python
from skills.skill_fetch_trends import SkillFetchTrends

skill = SkillFetchTrends(config={"source": "moltbook"})

result = await skill.execute({
    "source": "moltbook",
    "time_window": "1h",
    "velocity_threshold": 100,
    "max_results": 50
})

if result["status"] == "success":
    for trend in result["trends"]:
        print(f"{trend['keyword']}: {trend['velocity']}")
```

## Dependencies
- `requests>=2.31.0`
- `beautifulsoup4>=4.12.0`
- `python-dateutil>=2.8.2`

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `NETWORK_ERROR` | Failed to connect to platform | Retry with backoff |
| `RATE_LIMITED` | API rate limit exceeded | Wait and retry |
| `INVALID_SOURCE` | Unknown platform specified | Validate input |
| `TIMEOUT` | Request exceeded timeout | Retry with longer timeout |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2024-01-15 | Initial implementation |

## Next Steps
- [ ] Implement MoltBook API integration
- [ ] Add Twitter API support
- [ ] Add Instagram API support
- [ ] Implement sentiment analysis
- [ ] Add caching layer
