# Skill: Generate Content

## Overview
Generates engaging social media content based on trends, keywords, and style preferences. This is the primary creative skill for Chimera's content pipeline.

## Skill Information
- **Skill ID**: `skill_generate_content`
- **Version**: `0.1.0`
- **Category**: Generation
- **Author**: Project Chimera Team

## Capabilities
- Generate short-form video scripts
- Create engaging text posts and threads
- Generate relevant hashtags and mentions
- Adapt content style for different platforms
- Apply viral content patterns

## Input Contract

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GenerateContentInput",
  "type": "object",
  "properties": {
    "trend_id": {
      "type": "string",
      "description": "Reference to the trend being leveraged"
    },
    "content_type": {
      "type": "string",
      "enum": ["short_video", "image", "text", "thread", "story"],
      "description": "Type of content to generate"
    },
    "platform": {
      "type": "string",
      "enum": ["moltbook", "twitter", "instagram", "tiktok"],
      "description": "Target platform"
    },
    "style_presets": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["viral", "educational", "humorous", "inspirational", "news", "casual"]
      },
      "minItems": 1,
      "maxItems": 3,
      "description": "Content style preferences"
    },
    "tone": {
      "type": "string",
      "enum": ["professional", "friendly", "excited", "serious", "witty"],
      "default": "friendly",
      "description": "Voice tone"
    },
    "max_length": {
      "type": "integer",
      "minimum": 50,
      "maximum": 5000,
      "default": 280,
      "description": "Maximum character count"
    },
    "safety_check": {
      "type": "boolean",
      "default": true,
      "description": "Run safety verification"
    }
  },
  "required": ["trend_id", "content_type", "platform"]
}
```

### Example Input
```json
{
  "trend_id": "trend_001",
  "content_type": "short_video",
  "platform": "moltbook",
  "style_presets": ["viral", "educational"],
  "tone": "excited",
  "max_length": 500,
  "safety_check": true
}
```

## Output Contract

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GenerateContentOutput",
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "error", "safety_rejected"]
    },
    "content_id": {
      "type": "string",
      "description": "Unique identifier for generated content"
    },
    "generated_content": {
      "type": "object",
      "properties": {
        "script": {
          "type": "string",
          "description": "Video or post script"
        },
        "text": {
          "type": "string",
          "description": "Final text content"
        },
        "hashtags": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Generated hashtags"
        },
        "cta": {
          "type": "string",
          "description": "Call to action"
        }
      }
    },
    "estimated_engagement": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Predicted engagement rate"
    },
    "safety_verdict": {
      "type": "string",
      "enum": ["approved", "flagged", "rejected"],
      "description": "Safety check result"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "generation_duration_ms": {"type": "integer"},
        "model_used": {"type": "string"},
        "variations_generated": {"type": "integer"}
      }
    }
  },
  "required": ["status", "content_id"]
}
```

### Example Output
```json
{
  "status": "success",
  "content_id": "content_001",
  "generated_content": {
    "script": "Hook: Have you ever wondered... \nMain: AI is changing everything... \nCTA: Follow for more!",
    "text": "🤖 AI is revolutionizing content creation! Here's what's happening... #AITrends #FutureIsNow",
    "hashtags": ["#AI", "#Autonomous", "#ContentCreation"],
    "cta": "Follow for daily AI insights!"
  },
  "estimated_engagement": 0.85,
  "safety_verdict": "approved",
  "metadata": {
    "generation_duration_ms": 1250,
    "model_used": "gpt-4",
    "variations_generated": 3
  }
}
```

## Usage Example

```python
from skills.skill_generate_content import SkillGenerateContent

skill = SkillGenerateContent(config={"platform": "moltbook"})

result = await skill.execute({
    "trend_id": "trend_001",
    "content_type": "short_video",
    "platform": "moltbook",
    "style_presets": ["viral", "educational"],
    "tone": "excited",
    "max_length": 500
})

if result["status"] == "success":
    print(f"Generated content: {result['content_id']}")
    print(f"Estimated engagement: {result['estimated_engagement']}")
```

## Dependencies
- `openai>=1.0.0`
- `python-dotenv>=1.0.1`
- `pydantic>=2.0.0`

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `CONTENT_REJECTED` | Safety check failed | Review and adjust prompts |
| `MODEL_ERROR` | AI model failure | Retry with different model |
| `LENGTH_EXCEEDED` | Generated content too long | Truncate or regenerate |
| `INVALID_PLATFORM` | Unsupported platform | Validate platform param |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2024-01-15 | Initial implementation |

## Next Steps
- [ ] Implement OpenAI integration
- [ ] Add template system for viral patterns
- [ ] Implement A/B variation generation
- [ ] Add brand voice customization
- [ ] Implement content optimization
