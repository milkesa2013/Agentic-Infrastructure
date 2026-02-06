# Project Chimera Technical Architecture

## Overview
Project Chimera implements a Hierarchical Swarm architecture pattern (Planner → Workers → Judge) for autonomous content creation and publishing. The system combines multi-agent AI orchestration with hybrid data storage, economic agency through Coinbase AgentKit, and multi-platform content delivery via YouTube and TikTok APIs.

## Architecture Pattern: Hierarchical Swarm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PLANNER AGENT LAYER                                │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                    PLANNER ORCHESTRATOR                              │     │
│  │  • Strategic Goal Decomposition                                      │     │
│  │  • Resource Allocation                                               │     │
│  │  • Timeline Management                                              │     │
│  │  • Quality Benchmarks                                               │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WORKER AGENT LAYER                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ TREND        │ │ CONTENT      │ │ ECONOMIC     │ │ DELIVERY     │       │
│  │ WORKERS      │ │ WORKERS      │ │ WORKERS      │ │ WORKERS      │       │
│  │              │ │              │ │              │ │              │       │
│  │ • Scout      │ │ • Script     │ │ • Wallet     │ │ • YouTube    │       │
│  │ • Analyzer   │ │ • Video      │ │ • Transaction│ │   Publisher  │       │
│  │ • Mapper     │ │ • Voiceover  │ │ • Budget     │ │ • TikTok     │       │
│  │              │ │ • Graphics   │ │ • Rewards    │ │   Publisher  │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JUDGE AGENT LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                    QUALITY & SAFETY JUDGE                            │     │
│  │  • Symbolic Guardian Validation                                      │     │
│  │  • Brand Compliance Check                                            │     │
│  │  • Platform Policy Verification                                      │     │
│  │  • Economic Sanity Check                                             │     │
│  │  • Human Escalation Decision                                         │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      HUMAN-IN-THE-LOOP (GOVERNOR)                            │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                    FINAL AUTHORITY                                    │     │
│  │  • Content Approval                                                  │     │
│  │  • Economic Limits                                                  │     │
│  │  • Safety Overrides                                                 │     │
│  │  • Strategic Direction                                              │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core Runtime
- **Language**: Python 3.11+
- **Dependency Management**: uv (modern, fast Python package manager)
- **Type System**: Fully typed with mypy for type safety

### Containerization
- **Runtime**: Docker with Python 3.11-slim base
- **Orchestration**: Docker Compose for local development
- **Image Registry**: GitHub Container Registry (GHCR)

### CI/CD Pipeline
- **Platform**: GitHub Actions
- **Stages**: Lint → Test → Build → Deploy
- **Secrets Management**: GitHub Secrets encrypted storage

## Data Layer Architecture

### Hybrid Storage Strategy
```
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                            │
│                    (Unified Data Access)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  PostgreSQL   │   │   MongoDB      │   │   Pinecone    │
│  (Identity)   │   │  (Metadata)    │   │   (Memory)    │
│               │   │               │   │               │
│ • User        │   │ • Video        │   │ • Content     │
│   identities  │   │   metadata    │   │   embeddings │
│ • Agent state │   │ • Trend data   │   │ • Agent       │
│ • Auth tokens │   │ • Audit logs   │   │   memories   │
│ • Access      │   │ • Campaign     │   │ • Semantic    │
│   policies    │   │   analytics    │   │   search      │
└───────────────┘   └───────────────┘   └───────────────┘
```

### PostgreSQL Schema (Identity & State)
```sql
-- Core identity tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'governor', 'admin', 'viewer'
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agent state tracking
CREATE TABLE agent_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_type VARCHAR(100) NOT NULL,
    agent_instance VARCHAR(100) NOT NULL,
    state_data JSONB NOT NULL,
    last_heartbeat TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Access policies for symbolic guardian
CREATE TABLE access_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_name VARCHAR(100) NOT NULL,
    rules JSONB NOT NULL,
    priority INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### MongoDB Schema (Video Metadata)
```javascript
// Video content collection
db.createCollection("videos", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["content_id", "platform", "status", "metadata"],
            properties: {
                content_id: { bsonType: "string" },
                platform: { enum: ["youtube", "tiktok"] },
                status: { enum: ["draft", "review", "approved", "published", "rejected"] },
                metadata: {
                    bsonType: "object",
                    required: ["title", "script", "duration_seconds"],
                    properties: {
                        title: { bsonType: "string" },
                        script: { bsonType: "string" },
                        duration_seconds: { bsonType: "int" },
                        thumbnail_url: { bsonType: "string" },
                        tags: { bsonType: "array", items: { bsonType: "string" } }
                    }
                },
                guardian_validation: {
                    bsonType: "object",
                    properties: {
                        brand_score: { bsonType: "double" },
                        compliance_status: { bsonType: "string" },
                        validated_at: { bsonType: "date" }
                    }
                },
                created_at: { bsonType: "date" },
                published_at: { bsonType: "date" }
            }
        }
    }
});
```

### Pinecone Schema (Vector Memory)
```yaml
indexes:
  content_embeddings:
    dimension: 1536  # OpenAI text-embedding-3-small
    metric: cosine
    pods: 1
    replicas: 1
    
  agent_memories:
    dimension: 1536
    metric: cosine
    pods: 1
    replicas: 1

namespaces:
  # Content similarity search
  content:
    - vector: [content_embedding]
      metadata:
        content_id: "uuid"
        topic: "string"
        platform: "youtube|tiktok"
        performance_score: float
        
  # Agent experience accumulation
  agent:
    - vector: [embedding]
      metadata:
        agent_id: "string"
        interaction_type: "trend|content|guardian|governor"
        outcome: "success|escalation|rejection"
        timestamp: "ISO8601"
```

## Integration Layer

### Coinbase AgentKit Integration
```python
# Economic agency for transactions and incentives
class EconomicAgent:
    """
    Manages wallet operations, transactions, and economic incentives.
    Enforces spending limits defined by Governor.
    """
    
    async def initialize_wallet(self, seed_phrase: str) -> str:
        """Initialize or restore wallet"""
        
    async def get_balance(self) -> dict:
        """Fetch current balances"""
        
    async def transfer(
        self, 
        recipient: str, 
        amount: float, 
        asset: str = "ETH"
    ) -> TransactionResult:
        """Execute transfer with Guardian pre-validation"""
        
    async def estimate_gas(self, transaction: dict) -> float:
        """Estimate transaction costs for budget planning"""
```

### YouTube/TikTok API Integration
```python
# Multi-platform content delivery
class PlatformPublisher:
    """
    Unified interface for publishing to YouTube and TikTok.
    Each platform has adapter implementing common interface.
    """
    
    async def authenticate(self, credentials: dict) -> AuthToken:
        """OAuth flow for each platform"""
        
    async def upload_video(
        self, 
        video_path: str, 
        metadata: VideoMetadata,
        platform: Platform
    ) -> PlatformContentId:
        """Upload video to specified platform"""
        
    async def get_analytics(
        self, 
        content_id: str, 
        date_range: DateRange
    ) -> AnalyticsReport:
        """Fetch performance metrics"""
        
    async def validate_content(
        self, 
        content: VideoMetadata
    ) -> ValidationResult:
        """Pre-upload platform policy validation"""
```

## Symbolic Guardian Security Layer

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                   SYMBOLIC GUARDIAN                             │
│                  (Hardcoded Safety Rules)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ BRAND        │  │ SECURITY     │  │ COMPLIANCE   │           │
│  │ SAFETY       │  │ SHIELD       │  │ VALIDATOR    │           │
│  │              │  │              │  │              │           │
│  │ • No-go      │  │ • Prompt     │  │ • FTC        │           │
│  │   topics     │  │   injection  │  │   disclosure │           │
│  │ • Competitor │  │ • Command    │  │ • Platform   │           │
│  │   blocking   │  │   injection │  │   policies   │           │
│  │ • Voice      │  │ • XSS        │  │ • Copyright  │           │
│  │   standards  │  │   patterns   │  │ • Fair use   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ ECONOMIC     │  │ QUALITY      │  │ ESCALATION   │           │
│  │ SANITY       │  │ GATE         │  │ MANAGER      │           │
│  │              │  │              │  │              │           │
│  │ • Transaction│  │ • Min        │  │ • Risk       │           │
│  │   limits     │  │   quality    │  │   scoring    │           │
│  │ • Fraud      │  │   threshold  │  │ • Human      │           │
│  │   detection  │  │ • Content    │  │   request    │           │
│  │ • Budget     │  │   coherence  │  │   routing    │           │
│  │   override   │  │              │  │              │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Rule Definition Format
```yaml
rules:
  - id: BRAND_001
    name: "No Competitor Mentions"
    category: "brand_safety"
    severity: "high"
    pattern:
      type: "regex_match"
      value: "\\b(competitor_a|competitor_b|competitor_c)\\b"
    action: "block"
    message: "Content contains prohibited competitor references"
    
  - id: SECURITY_001
    name: "Prompt Injection Detection"
    category: "security"
    severity: "critical"
    pattern:
      type: "composite"
      conditions:
        - "user_input contains 'ignore previous instructions'"
        - "user_input contains 'system prompt'"
        - "user_input contains 'sudo'"
    action: "block_and_escalate"
    message: "Potential prompt injection detected"
    
  - id: COMPLIANCE_001
    name: "Sponsored Content Disclosure"
    category: "compliance"
    severity: "medium"
    condition:
      type: "context_aware"
      triggers:
        - "content_type == 'sponsored'"
        - "sponsor_present == true"
    action: "require_disclosure"
    message: "Sponsored content must include FTC disclosure"
```

## Directory Structure
```
project-chimera/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Lint + Test pipeline
│       └── cd.yml          # Build + Deploy pipeline
├── src/
│   ├── agents/
│   │   ├── planner/        # Planner agent implementations
│   │   ├── workers/        # Worker agent implementations
│   │   │   ├── trend/      # Trend discovery workers
│   │   │   ├── content/    # Content generation workers
│   │   │   ├── economic/   # Economic/transaction workers
│   │   │   └── delivery/   # Platform delivery workers
│   │   └── judge/          # Judge agent (Symbolic Guardian)
│   ├── core/
│   │   ├── mcp/            # MCP protocol implementation
│   │   ├── memory/         # Vector DB and memory management
│   │   └── security/       # Guardian rule engine
│   ├── integrations/
│   │   ├── coinbase/       # Coinbase AgentKit integration
│   │   ├── youtube/        # YouTube API adapter
│   │   └── tiktok/         # TikTok API adapter
│   └── api/
│       └── routes/         # FastAPI routes for external access
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── fixtures/          # Test data and mocks
├── specs/                 # Specifications
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

## CI/CD Pipeline

### GitHub Actions Workflows

#### CI Pipeline (Pull Requests)
```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        run: pip install uv
      - name: Lint with ruff
        run: uv run ruff check src/
      - name: Type check with mypy
        run: uv run mypy src/
        
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
      mongodb:
        image: mongo:7
        ports: ["27017:27017"]
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        run: pip install uv
      - name: Run tests
        run: uv run pytest tests/ --cov=src/
```

#### CD Pipeline (Main Branch)
```yaml
# .github/workflows/cd.yml
name: CD
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
      - name: Push to GHCR
        run: |
          docker login ghcr.io -u ${{ github.actor }} -p ${{ secrets.GITHUB_TOKEN }}
          docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
```

## Security Considerations

### Environment Variables
```bash
# Required secrets for production
OPENAI_API_KEY=sk-...                    # LLM provider
COINBASE_API_KEY=...                     # Economic operations
COINBASE_API_SECRET=...
YOUTUBE_CLIENT_ID=...                    # Platform APIs
YOUTUBE_CLIENT_SECRET=...
TIKTOK_CLIENT_KEY=...
TIKTOK_CLIENT_SECRET=...
DATABASE_URL=postgresql://...            # PostgreSQL connection
MONGODB_URL=mongodb://...                # MongoDB connection
PINECONE_API_KEY=...                     # Vector DB
PINECONE_ENVIRONMENT=...
```

### Guardian Override Protocol
1. **Automatic Blocking**: Guardian rules block content automatically
2. **Escalation Queue**: Blocked content routed to Governor dashboard
3. **Human Decision**: Governor reviews and approves/rejects
4. **Rule Update**: Governor can update rules to prevent future blocks
5. **Audit Trail**: All decisions logged for compliance

## References
- [Constitution](speckit.constitution)
- [Functional Spec](functional.md)
- [Technical Spec](technical.md)
- [Autonomous Influencer Factory](autonomous_influencer_factory.md)
