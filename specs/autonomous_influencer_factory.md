# Autonomous Influencer Factory Specification

## Overview
The Autonomous Influencer Factory (AIF) is a hierarchical multi-agent system designed to autonomously discover trends, generate video content, and submit outputs for safety review. The system operates as a factory metaphor where AI agents act as workers in a hierarchical swarm, producing content that is vetted by a Symbolic Guardian before human review.

## System Architecture

### Hierarchical Swarm Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                    GOVERNOR (Human-in-the-Loop)                  │
│                    ┌─────────────────────┐                       │
│                    │  Strategic Oversight │                      │
│                    │  Content Approval    │                      │
│                    │  Policy Enforcement  │                      │
│                    └──────────┬──────────┘                       │
└───────────────────────────────┼──────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                            │
│                    ┌─────────────────────┐                       │
│                    │  Work Distribution  │                       │
│                    │  Quality Gates      │                      │
│                    │  Swarm Coordination │                      │
│                    └──────────┬──────────┘                       │
└───────────────────────────────┼──────────────────────────────────┘
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ TREND AGENT     │   │ CONTENT AGENT   │   │ GUARDIAN AGENT  │
│ WORKER POOL     │   │ WORKER POOL     │   │ WORKER POOL     │
│                 │   │                 │   │                 │
│ • Trend Scout   │   │ • Script Writer │   │ • Brand Sentinel│
│ • Sentiment     │   │ • Video Editor  │   │ • Prompt Shield │
│   Analyzer      │   │ • Voiceover     │   │ • Content       │
│ • Topic Mapper  │   │   Synthesizer   │   │   Validator     │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

## Agent Roles & Responsibilities

### Governor (Human-in-the-Loop)
- **Strategic Oversight**: Define brand guidelines, target audience, and content pillars
- **Content Approval**: Final sign-off on all content before publication
- **Policy Enforcement**: Update safety policies and brand constraints
- **Intervention Authority**: Override any automated decision
- **Metrics Review**: Evaluate system performance and ROI

### Orchestrator Agent
- Receive strategic directives from Governor
- Decompose high-level goals into tasks
- Distribute work across worker pools
- Manage inter-agent communication via MCP
- Enforce quality gates between pipeline stages
- Track lineage of all content artifacts

### Trend Agent Swarm
**Trend Scout Agent**
- Monitor social platforms, news sources, and industry feeds
- Identify emerging topics within defined niches
- Detect viral content patterns
- Score trending potential (reach × engagement × relevance)
- Output: Ranked trend candidates with metadata

**Sentiment Analyzer Agent**
- Analyze sentiment around identified trends
- Detect potential controversy or backlash risk
- Identify sentiment triggers for content angle
- Output: Sentiment profile and risk assessment

**Topic Mapper Agent**
- Map trends to content pillars and brand themes
- Identify content gaps and opportunities
- Suggest content angles aligned with brand voice
- Output: Topic briefs for content generation

### Content Agent Swarm
**Script Writer Agent**
- Generate video scripts based on topic briefs
- Incorporate brand voice and messaging
- Include hooks, calls-to-action, and engagement elements
- Output: Video scripts with timing annotations

**Video Editor Agent**
- Assemble video from stock footage, animations, and graphics
- Apply brand visual identity
- Sync visuals with audio cues
- Output: Raw video cuts ready for review

**Voiceover Synthesizer Agent**
- Generate synthetic voiceovers from scripts
- Apply brand-appropriate voice styles
- Ensure clear diction and pacing
- Output: Audio tracks synchronized to video

### Guardian Agent Swarm
**Brand Sentinel Agent**
- Validate all content against brand guidelines
- Check for brand safety violations
- Ensure consistent brand voice and messaging
- Flag potential brand damage scenarios
- Output: Brand compliance score and issues list

**Prompt Shield Agent**
- Detect and neutralize prompt injection attempts
- Validate all inter-agent communications
- Prevent adversarial inputs from affecting outputs
- Monitor for unusual agent behavior patterns
- Output: Security clearance status per artifact

**Content Validator Agent**
- Verify factual accuracy of claims
- Check for regulatory compliance (FTC, GDPR, etc.)
- Validate copyright and fair use compliance
- Flag sensitive topics requiring Governor review
- Output: Validation report with clearance level

## Data Flow

### Pipeline Stages
```
Trend Discovery → Content Generation → Guardian Review → Governor Approval → Publishing
```

### Stage 1: Trend Discovery
1. Governor sets discovery parameters (niches, platforms, frequency)
2. Trend Scout monitors feeds and identifies candidates
3. Sentiment Analyzer assesses each candidate
4. Topic Mapper aligns candidates with content pillars
5. Orchestrator ranks and prioritizes trend queue

### Stage 2: Content Generation
1. Orchestrator assigns topic to Content Agent Swarm
2. Script Writer produces video script
3. Script passes to Guardian for content review
4. Video Editor assembles visual elements
5. Voiceover Synthesizer produces audio track
6. Final assembly into video artifact

### Stage 3: Guardian Review
1. Brand Sentinel validates brand alignment
2. Prompt Shield validates security integrity
3. Content Validator checks compliance
4. Guardian Swarm produces unified clearance decision
5. Escalate to Governor if issues detected

### Stage 4: Governor Approval
1. Governor receives clearance report
2. Human reviews content artifact
3. Governor approves or requests revisions
4. Approved content moves to publishing queue

### Stage 5: Publishing
1. Orchestrator schedules approved content
2. Content published to designated platforms
3. Performance tracking initiated
4. Metrics fed back to Governor for optimization

## MCP Communication Contracts

### Inter-Agent Message Schema
```json
{
  "mcp_version": "1.0",
  "message_type": "task_request|task_response|approval_request|escalation",
  "sender": "agent_id",
  "recipient": "agent_id",
  "timestamp": "ISO8601",
  "payload": {
    "task_id": "uuid",
    "action": "action_name",
    "parameters": {},
    "artifacts": []
  },
  "trace_id": "correlation_uuid"
}
```

### Standardized I/O Contracts

#### Trend Scout Output
```json
{
  "trends": [
    {
      "id": "uuid",
      "topic": "string",
      "platform": "string",
      "volume": "integer",
      "velocity": "float",
      "relevance_score": "float (0-1)",
      "engagement_rate": "float",
      "discovered_at": "ISO8601"
    }
  ],
  "confidence": "float (0-1)",
  "metadata": {}
}
```

#### Guardian Clearance Output
```json
{
  "clearance_decision": "CLEAR|ESCALATE|REJECT",
  "brand_score": "float (0-1)",
  "security_score": "float (0-1)",
  "compliance_score": "float (0-1)",
  "issues": [
    {
      "severity": "LOW|MEDIUM|HIGH|CRITICAL",
      "category": "string",
      "description": "string",
      "recommendation": "string"
    }
  ],
  "requires_human_review": "boolean",
  "guardian_signature": "hash"
}
```

## Symbolic Guardian Layer

### Purpose
The Symbolic Guardian is a safety-first middleware layer that intercepts all content artifacts and agent communications, validating against symbolic rules and patterns to prevent brand damage, prompt injection, and compliance violations.

### Rule Categories

#### Brand Safety Rules
- Block content mentioning competitors by name
- Enforce no-go topics list
- Validate brand voice consistency
- Check visual brand element compliance

#### Security Rules
- Detect prompt injection patterns in inputs
- Validate agent identity and authorization
- Block suspicious command patterns
- Monitor for cascading failures

#### Compliance Rules
- FTC disclosure requirements
- Platform-specific content policies
- Industry-specific regulations (finance, health, etc.)
- Copyright and fair use checks

#### Quality Rules
- Minimum engagement threshold for trends
- Script length and structure validation
- Video quality metrics
- Voiceover clarity scoring

### Guardian Decision Matrix
| Brand Score | Security Score | Compliance Score | Decision |
|-------------|----------------|-------------------|----------|
| ≥0.9        | ≥0.9           | ≥0.9              | CLEAR    |
| ≥0.7        | ≥0.9           | ≥0.9              | CONDITIONAL |
| <0.7        | Any            | Any               | ESCALATE |
| Any         | <0.7           | Any               | REJECT   |
| Any         | Any            | <0.7              | ESCALATE |

## Governance Integration

### Governor Dashboard
- Real-time pipeline status
- Pending approval queue
- Performance metrics
- Trend discovery analytics
- Guardian alert feed
- Brand safety score trends

### Human-in-the-Loop Interventions
- Approve/reject specific artifacts
- Adjust brand guidelines and safety thresholds
- Override Guardian decisions
- Inject strategic pivots
- Pause/resume pipeline operations

### Escalation Paths
1. **Low Risk**: Guardian Swarm handles internally
2. **Medium Risk**: Escalate to Orchestrator for retry
3. **High Risk**: Governor notification required
4. **Critical**: Immediate pipeline halt, Governor alert

## Implementation Phases

### Phase 1: Foundation
- Deploy Orchestrator and basic MCP infrastructure
- Implement Trend Scout agent
- Create Governor dashboard skeleton
- Establish baseline MCP schemas

### Phase 2: Content Pipeline
- Build Content Agent Swarm
- Implement basic video generation
- Add Guardian Swarm components
- Integrate symbolic rule engine

### Phase 3: Safety & Compliance
- Enhance Guardian layer
- Add compliance validation
- Implement brand safety rules
- Governor approval workflows

### Phase 4: Optimization
- Autonomous trend ranking
- Performance-based agent tuning
- Predictive content scheduling
- Advanced analytics and reporting

## Success Metrics

### Operational Metrics
- Pipeline throughput (content pieces/week)
- Average time-to-approval
- Guardian clearance rate
- Governor intervention frequency

### Quality Metrics
- Engagement rate of published content
- Brand safety incident count
- Compliance violation rate
- Trend-to-content conversion rate

### Efficiency Metrics
- Cost per content piece
- Agent utilization rate
- False positive rate in Guardian
- Retry/revision frequency

## References
- [Functional Spec](functional.md)
- [Technical Spec](technical.md)
- [Meta Spec](meta.md)
- [OpenCLAW Integration](openclaw_integration.md)
