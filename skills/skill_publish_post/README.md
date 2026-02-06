# Skill: Publish Post

## Overview
Publishes generated content to social media platforms with scheduling, approval workflows, and delivery confirmation. This is the primary action skill for Chimera's content pipeline.

## Skill Information
- **Skill ID**: `skill_publish_post`
- **Version**: `0.1.0`
- **Category**: Action
- **Author**: Project Chimera Team

## Capabilities
- Publish content to multiple platforms simultaneously
- Schedule posts for optimal engagement times
- Handle human approval workflows for high-value content
- Track delivery status and retrieve published URLs
- Manage post edits and deletions

## Input Contract

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PublishPostInput",
  "type": "object",
  "properties": {
    "content_id": {
      "type": "string",
      "description": "Reference to generated content"
    },
    "platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["moltbook", "twitter", "instagram"]
      },
      "minItems": 1,
      "description": "Target platforms for publishing"
    },
    "scheduled_time": {
      "type": "string",
      "format": "date-time",
      "description": "Optional: Schedule for future publishing"
    },
    "approval_id": {
      "type": "string",
      "description": "Required for high-value transactions: Human approval reference"
    },
    "priority": {
      "type": "string",
      "enum": ["low", "normal", "high", "urgent"],
      "default": "normal",
      "description": "Publishing priority"
    },
    "metadata": {
      "type": "object",
      "description": "Additional post metadata"
    }
  },
  "required": ["content_id", "platforms"]
}
```

### Example Input (Immediate Publish)
```json
{
  "content_id": "content_001",
  "platforms": ["moltbook"],
  "priority": "normal"
}
```

### Example Input (Scheduled with Approval)
```json
{
  "content_id": "content_001",
  "platforms": ["moltbook", "twitter"],
  "scheduled_time": "2024-01-15T12:00:00Z",
  "approval_id": "approval_001",
  "priority": "high"
}
```

## Output Contract

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PublishPostOutput",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["published", "scheduled", "pending_approval", "error"]
    },
    "post_id": {
      "type": "string",
      "description": "Unique identifier for the post"
    },
    "published_results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "platform": {"type": "string"},
          "published_url": {"type": "string"},
          "published_at": {"type": "string", "format": "date-time"},
          "status": {"type": "string"}
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "publish_duration_ms": {"type": "integer"},
        "total_platforms": {"type": "integer"},
        "scheduled_for": {"type": "string", "format": "date-time"}
      }
    }
  },
  "required": ["status", "post_id"]
}
```

### Example Output (Published)
```json
{
  "status": "published",
  "post_id": "post_001",
  "published_results": [
    {
      "platform": "moltbook",
      "published_url": "https://moltbook.com/p/12345",
      "published_at": "2024-01-15T10:30:00Z",
      "status": "success"
    }
  ],
  "metadata": {
    "publish_duration_ms": 850,
    "total_platforms": 1
  }
}
```

### Example Output (Pending Approval)
```json
{
  "status": "pending_approval",
  "post_id": "post_001",
  "published_results": [],
  "metadata": {
    "publish_duration_ms": 50,
    "total_platforms": 2,
    "approval_required": {
      "reason": "high_value_campaign",
      "threshold_usdc": 10,
      "contact_discord": "human_approval_channel"
    }
  }
}
```

## Usage Example

```python
from skills.skill_publish_post import SkillPublishPost

skill = SkillPublishPost(config={"default_platform": "moltbook"})

# Immediate publish
result = await skill.execute({
    "content_id": "content_001",
    "platforms": ["moltbook"]
})

if result["status"] == "published":
    print(f"Published: {result['published_results'][0]['published_url']}")

# Scheduled publish
scheduled_result = await skill.execute({
    "content_id": "content_002",
    "platforms": ["moltbook", "twitter"],
    "scheduled_time": "2024-01-15T18:00:00Z",
    "approval_id": "approval_001"
})

if scheduled_result["status"] == "scheduled":
    print(f"Scheduled for: {scheduled_result['metadata']['scheduled_for']}")
```

## Dependencies
- `python-social-auth>=20.0.0`
- `python-dotenv>=1.0.1`
- `httpx>=0.25.0`

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `AUTH_EXPIRED` | Platform OAuth token expired | Refresh token |
| `RATE_LIMITED` | Platform rate limit | Backoff and retry |
| `CONTENT_REJECTED` | Platform rejected content | Review and modify |
| `APPROVAL_REQUIRED` | High-value requires human | Submit for approval |
| `INVALID_CONTENT` | Content not found | Validate content_id |

## Platform-Specific Notes

### MoltBook
- Requires OAuth2 authentication
- Rate limit: 100 posts/hour
- Supports video up to 10 minutes

### Twitter
- Requires OAuth 1.0a or 2.0
- Rate limit: 300 posts/3 hours
- Character limit: 280 (with Twitter Blue: 4000)

### Instagram
- Requires Business/Creator account
- Rate limit: 25 posts/hour
- Image aspect ratio: 1.91:1 to 4:5

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2024-01-15 | Initial implementation |

## Next Steps
- [ ] Implement MoltBook API integration
- [ ] Add Twitter API support
- [ ] Add Instagram API support
- [ ] Implement OAuth token refresh
- [ ] Add post analytics tracking
- [ ] Implement scheduling queue
