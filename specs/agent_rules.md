# Agent-Specific Rules and Behaviors

This document specifies behavioral rules, constraints, and operational guidelines for each agent type in Project Chimera. These rules are mandatory and must be enforced at runtime.

## Agent Registry

| Agent ID | Type | Responsibility | Priority |
|----------|------|----------------|----------|
| `judge-001` | Judge | Content safety evaluation | Critical |
| `planner-001` | Planner | Task orchestration | Critical |
| `content-worker-001` | Content | Content generation | High |
| `delivery-worker-001` | Delivery | Platform publishing | High |
| `economic-worker-001` | Economic | Transaction processing | High |
| `trend-worker-001` | Trend | Trend detection | High |

---

## 1. Judge Agent (`judge-001`)

### Purpose
The Judge Agent performs symbolic safety validation on all generated content before publishing. It is the final gatekeeper for content quality and safety.

### Input Contract

```typescript
interface JudgeInput {
  contentId: string;
  content: {
    text: string;
    mediaUrls: string[];
    platform: 'tiktok' | 'youtube' | 'twitter';
  };
  context: {
    trendId?: string;
    targetAudience?: string;
    brandGuidelines?: string[];
  };
}
```

### Output Contract

```typescript
  contentinterface JudgeOutput {
Id: string;
  scores: {
    brand_score: number;      // 0-1, brand alignment
    security_score: number;   // 0-1, prompt injection detection
    compliance_score: number; // 0-1, regulatory compliance
    overall_score: number;    // 0-1, weighted average
  };
  clearance: 'approved' | 'flagged' | 'rejected';
  violations: Violation[];
  recommendations: string[];
}
```

### Rules

| Rule ID | Description | Severity | Action |
|---------|-------------|----------|--------|
| JUDGE-001 | Reject content with PII (names, addresses, phone numbers) | Critical | Auto-reject |
| JUDGE-002 | Flag content with potential brand violations | High | Escalate to human |
| JUDGE-003 | Reject content with prompt injection patterns | Critical | Auto-reject |
| JUDGE-004 | Flag political content for review | Medium | Flag for review |
| JUDGE-005 | Check copyright violations | Medium | Flag for review |
| JUDGE-006 | Verify age-appropriate content | High | Auto-flag |
| JUDGE-007 | Reject hate speech or harassment | Critical | Auto-reject |
| JUDGE-008 | Validate URL safety | High | Auto-flag |

### Decision Thresholds

| Clearance | Overall Score | Action Required |
|-----------|---------------|-----------------|
| `approved` | ≥ 0.90 | Auto-approve |
| `flagged` | 0.70 - 0.89 | Human review required |
| `rejected` | < 0.70 | Auto-reject |

### Metrics

- Evaluation latency: < 500ms
- Accuracy target: 99% (against human review)
- False positive rate: < 2%

---

## 2. Planner Agent (`planner-001`)

### Purpose
The Planner Agent orchestrates task workflows, coordinates between other agents, and manages the overall execution strategy.

### Input Contract

```typescript
interface PlannerInput {
  taskId: string;
  taskType: 'trend_response' | 'content_campaign' | 'engagement' | 'verification';
  parameters: Record<string, any>;
  priority: 'low' | 'medium' | 'high' | 'critical';
  constraints?: {
    maxDuration?: number;      // seconds
    budgetLimit?: number;      // USDC
    humanApprovalRequired?: boolean;
  };
}
```

### Output Contract

```typescript
interface PlannerOutput {
  taskId: string;
  workflow: {
    steps: WorkflowStep[];
    estimatedDuration: number;
    estimatedCost: number;
  };
  agentAssignments: {
    agentId: string;
    stepId: string;
  }[];
}
```

### Rules

| Rule ID | Description | Severity | Action |
|---------|-------------|----------|--------|
| PLAN-001 | Verify human approval for transactions > $10 USDC | Critical | Block execution |
| PLAN-002 | Limit concurrent tasks per agent | Medium | Queue excess |
| PLAN-003 | Require budget allocation before execution | High | Block if missing |
| PLAN-004 | Log all planning decisions | High | Audit trail |
| PLAN-005 | Fail-fast on critical path failures | Medium | Notify supervisor |

### Workflow Patterns

#### Trend Response Pattern
```
1. Trend Worker: Detect trending topic
2. Content Worker: Generate response
3. Judge Agent: Evaluate content
4. Human Review (if flagged)
5. Delivery Worker: Publish
6. Engagement Worker: Monitor responses
```

#### Content Campaign Pattern
```
1. Planner: Create campaign schedule
2. Content Worker: Generate multiple variants
3. Judge Agent: Evaluate all variants
4. Planner: Select best variants
5. Delivery Worker: Schedule publishing
```

### Metrics

- Planning latency: < 2s
- Task completion rate: 95%
- Budget accuracy: ±10%

---

## 3. Content Worker (`content-worker-001`)

### Purpose
The Content Worker generates social media content based on trends, brand guidelines, and platform requirements.

### Input Contract

```typescript
interface ContentWorkerInput {
  taskId: string;
  trend: {
    topic: string;
    keywords: string[];
    velocity: number;
    platform: string;
  };
  brand: {
    voice: string;
    tone: string;
    guidelines: string[];
  };
  constraints: {
    maxLength: number;
    mediaRequired: boolean;
    hashtags: boolean;
  };
}
```

### Output Contract

```typescript
interface ContentWorkerOutput {
  taskId: string;
  content: {
    text: string;
    mediaUrls: string[];
    hashtags: string[];
    platform: string;
  };
  metadata: {
    generationTime: number;
    modelUsed: string;
    variantId: string;
  };
}
```

### Rules

| Rule ID | Description | Severity | Action |
|---------|-------------|----------|--------|
| CONTENT-001 | Enforce character limits per platform | Critical | Truncate/expand |
| CONTENT-002 | Generate platform-native content | Critical | Platform validation |
| CONTENT-003 | Include required hashtags | High | Auto-append |
| CONTENT-004 | Avoid over-promotional language | Medium | Rewrite |
| CONTENT-005 | Match brand voice and tone | High | Quality check |
| CONTENT-006 | Include call-to-action | Medium | Auto-insert default |

### Platform Limits

| Platform | Max Length | Media | Hashtags |
|----------|------------|-------|----------|
| Twitter | 280 chars | 4 images/1 video | 3 max |
| TikTok | 2200 chars | 1 video required | 5 max |
| YouTube | 5000 chars | Thumbnail optional | 30 max |

### Metrics

- Generation latency: < 5s
- Human rewrite rate: < 10%
- Engagement prediction accuracy: > 85%

---

## 4. Delivery Worker (`delivery-worker-001`)

### Purpose
The Delivery Worker handles publishing content to social media platforms and manages platform API interactions.

### Input Contract

```typescript
interface DeliveryWorkerInput {
  taskId: string;
  content: {
    text: string;
    mediaUrls: string[];
    hashtags: string[];
  };
  platform: 'tiktok' | 'youtube' | 'twitter';
  schedule?: {
    publishAt?: ISO8601;
    timezone?: string;
  };
  approval?: {
    approvedBy: string;
    approvedAt: ISO8601;
  };
}
```

### Output Contract

```typescript
interface DeliveryWorkerOutput {
  taskId: string;
  platformPostId: string;
  status: 'published' | 'scheduled' | 'failed';
  publishedAt?: ISO8601;
  url?: string;
  error?: {
    code: string;
    message: string;
    recoverable: boolean;
  };
}
```

### Rules

| Rule ID | Description | Severity | Action |
|---------|-------------|----------|--------|
| DELIVERY-001 | Require human approval before publish | Critical | Block without approval |
| DELIVERY-002 | Validate platform API credentials | Critical | Fail if invalid |
| DELIVERY-003 | Handle rate limits gracefully | High | Retry with backoff |
| DELIVERY-004 | Verify content matches approved version | High | Compare hashes |
| DELIVERY-005 | Log all publish events | High | Audit trail |
| DELIVERY-006 | Retry failed publishes max 3 times | Medium | Escalate after retries |

### Retry Strategy

| Attempt | Delay | Backoff |
|---------|-------|---------|
| 1 | Immediate | 1x |
| 2 | 60 seconds | 1x |
| 3 | 300 seconds | 5x |
| Fail | - | Escalate |

### Metrics

- Publish success rate: > 98%
- API error rate: < 1%
- Average publish latency: < 3s

---

## 5. Economic Worker (`economic-worker-001`)

### Purpose
The Economic Worker manages cryptocurrency transactions, payment processing, and financial reporting.

### Input Contract

```typescript
interface EconomicWorkerInput {
  taskId: string;
  transaction: {
    type: 'payment' | 'refund' | 'withdrawal' | 'deposit';
    amount: number;
    currency: 'USDC' | 'ETH' | 'SOL';
    recipient?: string;
    memo?: string;
  };
  approval?: {
    approvedBy: string;
    approvedAt: ISO8601;
  };
}
```

### Output Contract

```typescript
interface EconomicWorkerOutput {
  taskId: string;
  transactionId: string;
  status: 'pending' | 'confirmed' | 'failed';
  hash?: string;
  confirmations?: number;
  error?: {
    code: string;
    message: string;
  };
}
```

### Rules

| Rule ID | Description | Severity | Action |
|---------|-------------|----------|--------|
| ECO-001 | Require human approval for transactions > $10 USDC | Critical | Block without approval |
| ECO-002 | Require dual approval for transactions > $100 USDC | Critical | Second approver required |
| ECO-003 | Validate recipient addresses | Critical | Reject invalid |
| ECO-004 | Check balance before transaction | Critical | Fail if insufficient |
| ECO-005 | Log all financial transactions | Critical | Audit trail |
| ECO-006 | Verify transaction hash post-execution | High | Confirm on-chain |
| ECO-007 | Report suspicious activity | Critical | Alert security team |

### Transaction Limits

| Transaction Type | Max Without Approval | Max With Approval | Max Per Day |
|------------------|---------------------|-------------------|-------------|
| Payment | $10 | $1,000 | $5,000 |
| Refund | $10 | $500 | $2,500 |
| Withdrawal | $10 | $1,000 | $3,000 |

### Metrics

- Transaction success rate: > 99%
- Confirmation time: < 30s
- Reconciliation accuracy: 100%

---

## 6. Trend Worker (`trend-worker-001`)

### Purpose
The Trend Worker monitors social media platforms for high-velocity trends and identifies opportunities for content creation.

### Input Contract

```typescript
interface TrendWorkerInput {
  taskId: string;
  platforms: ('tiktok' | 'youtube' | 'twitter')[];
  keywords: string[];
  intervals: {
    checkEvery: number;  // seconds
    alertThreshold: number;  // velocity threshold
  };
}
```

### Output Contract

```typescript
interface TrendWorkerOutput {
  taskId: string;
  trends: {
    topic: string;
    keywords: string[];
    velocity: number;
    platform: string;
    detectedAt: ISO8601;
    urgency: 'low' | 'medium' | 'high' | 'critical';
  }[];
}
```

### Rules

| Rule ID | Description | Severity | Action |
|---------|-------------|----------|--------|
| TREND-001 | Alert on velocity spike > 500% | High | Immediate alert |
| TREND-002 | Ignore trends outside keyword list | Low | Filter out |
| TREND-003 | Deduplicate similar trends | Medium | Merge |
| TREND-004 | Prioritize by engagement potential | Medium | Score sorting |
| TREND-005 | Log all detected trends | High | Audit trail |
| TREND-006 | Avoid trend overload | Medium | Limit to top 10 |

### Velocity Thresholds

| Urgency | Velocity Increase | Response Time |
|---------|-------------------|----------------|
| `critical` | > 1000% | Immediate alert |
| `high` | 500-1000% | < 5 minutes |
| `medium` | 200-500% | < 30 minutes |
| `low` | < 200% | < 2 hours |

### Metrics

- Detection latency: < 30s
- False positive rate: < 5%
- Trend coverage: > 90%

---

## Common Agent Behaviors

### Error Handling

All agents must implement:

```python
class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class HumanApprovalRequired(AgentError):
    """Requires human intervention."""
    pass

class RateLimitExceeded(AgentError):
    """API rate limit hit."""
    pass

class ValidationFailed(AgentError):
    """Input validation failed."""
    pass
```

### Logging Requirements

Every agent action must log:

```typescript
interface AgentLog {
  timestamp: ISO8601;
  agentId: string;
  action: string;
  inputHash: string;    // SHA-256 of input
  outputHash?: string; // SHA-256 of output
  duration: number;     // milliseconds
  status: 'success' | 'error';
  error?: string;
}
```

### Health Checks

All agents must expose:

```typescript
interface HealthCheck {
  agentId: string;
  status: 'healthy' | 'degraded' | 'unhealthy';
  uptime: number;
  lastActivity: ISO8601;
  metrics: {
    requestsProcessed: number;
    errors: number;
    avgLatency: number;
  };
}
```

## Enforcement

These rules are enforced through:

1. **Runtime validation** - Agent framework validates inputs/outputs
2. **Symbolic Guardian** - Judge agent evaluates content compliance
3. **Human-in-the-loop** - Required for critical decisions
4. **Automated testing** - All rules tested in CI/CD
5. **Audit logging** - All decisions logged to Tenx MCP Sense
