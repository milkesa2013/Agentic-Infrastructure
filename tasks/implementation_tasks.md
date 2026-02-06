# Project Chimera Implementation Tasks

## Overview
This document outlines the implementation tasks for Project Chimera, organized by phase and priority. All tasks follow the spec-driven development principle from the constitution.

## Phase 1: Specification Foundation

### Task 1.1: Create _meta.md (Priority: Critical)
- [ ] Create `specs/_meta.md` with project metadata
- [ ] Define spec version and last updated timestamp
- [ ] List all spec documents and their relationships
- [ ] Document spec review and approval process
- [ ] Establish change log format

**Acceptance Criteria:**
- `_meta.md` contains valid YAML frontmatter
- All 6 spec documents are listed with status
- Version numbering follows semantic versioning

### Task 1.2: Update functional.md (Priority: Critical)
- [ ] Document system capabilities and features
- [ ] Define user personas (Governor, Viewer, Admin)
- [ ] List functional requirements by priority
- [ ] Map requirements to agent roles
- [ ] Document expected inputs and outputs for each function

**Acceptance Criteria:**
- Functional requirements are traceable to architecture
- User personas have defined permissions
- Each requirement has a unique ID

### Task 1.3: Update technical.md (Priority: Critical)
- [ ] Document API endpoints and schemas
- [ ] Define data models and serialization formats
- [ ] Document inter-service communication protocols
- [ ] Specify performance requirements and SLAs
- [ ] Document error handling and retry policies

**Acceptance Criteria:**
- API schemas are valid OpenAPI 3.0
- Data models match MongoDB/PostgreSQL schemas
- Performance targets are measurable

## Phase 2: Skills Directory Initialization

### Task 2.1: fetch_trends Skill Contract (Priority: High)
- [ ] Create `skills/skill_fetch_trends/README.md`
- [ ] Define MCP input contract:
  ```yaml
  input:
    platforms: list[string]
    niches: list[string]
    time_range: object
    min_engagement: integer
  ```
- [ ] Define MCP output contract:
  ```yaml
  output:
    trends: list[object]
    metadata: object
  ```
- [ ] Document implementation requirements
- [ ] Define failure modes and error handling
- [ ] Specify performance requirements (latency, throughput)

**Acceptance Criteria:**
- README contains runnable example
- All parameters have type hints
- Error conditions are documented

### Task 2.2: generate_script Skill Contract (Priority: High)
- [ ] Create `skills/skill_generate_script/README.md`
- [ ] Define MCP input contract:
  ```yaml
  input:
    topic: string
    target_duration: integer
    style: string
    platform: enum[youtube, tiktok]
    brand_guidelines: object
  ```
- [ ] Define MCP output contract:
  ```yaml
  output:
    script: object
    timing_annotations: list[object]
    estimated_engagement: float
  ```
- [ ] Document script structure requirements
- [ ] Define brand voice compliance checks
- [ ] Specify content safety requirements

**Acceptance Criteria:**
- Script format supports video editing tools
- Timing annotations align with video frames
- Brand guidelines are configurable

### Task 2.3: symbolic_judge Skill Contract (Priority: Critical)
- [ ] Create `skills/skill_symbolic_judge/README.md`
- [ ] Define MCP input contract:
  ```yaml
  input:
    artifact_type: enum[content, transaction, command]
    artifact_content: object
    context: object
    guardian_rules: list[object]
  ```
- [ ] Define MCP output contract:
  ```yaml
  output:
    decision: enum[approve, block, escalate]
    scores: object
    issues: list[object]
    requires_human: boolean
  ```
- [ ] Document rule engine interface
- [ ] Define scoring algorithm
- [ ] Document escalation paths

**Acceptance Criteria:**
- Decision output matches architecture spec
- Rule engine is configurable via file
- Scoring is deterministic and auditable

## Phase 3: Test Suite Creation (TDD Approach)

### Task 3.1: Skills Interface Tests (Priority: High)
- [ ] Create `tests/test_skills_interface.py`
- [ ] Test fetch_trends input validation
- [ ] Test fetch_trends output schema compliance
- [ ] Test generate_script input validation
- [ ] Test generate_script output schema compliance
- [ ] Test symbolic_judge decision logic

**Failing Test Cases:**
```python
def test_fetch_trends_rejects_invalid_platform():
    """Should reject platforms not in allowed list"""
    pass

def test_fetch_trends_returns_valid_trend_schema():
    """Trend output must match MCP schema"""
    pass

def test_symbolic_judge_blocks_competitor_reference():
    """Should block content with competitor mentions"""
    pass

def test_symbolic_judge_approves_clean_content():
    """Should approve content passing all rules"""
    pass

def test_generate_script_enforces_duration_limit():
    """Script must respect target duration"""
    pass
```

### Task 3.2: Data Schema Validation Tests (Priority: High)
- [ ] Create `tests/test_data_schemas.py`
- [ ] Test PostgreSQL schema constraints
- [ ] Test MongoDB collection validators
- [ ] Test Vector DB namespace configuration
- [ ] Test schema migration paths

**Failing Test Cases:**
```python
def test_postgres_users_role_enum():
    """User role must be governor, admin, or viewer"""
    pass

def test_mongodb_videos_validator():
    """Video collection enforces required fields"""
    pass

def test_pinecone_content_namespace():
    """Content embeddings have correct dimension"""
    pass

def test_schema_relationships():
    """Foreign key references are valid"""
    pass
```

### Task 3.3: Agent Integration Tests (Priority: Medium)
- [ ] Create `tests/test_agents.py`
- [ ] Test planner agent goal decomposition
- [ ] Test worker agent task execution
- [ ] Test judge agent decision consistency
- [ ] Test inter-agent MCP communication

### Task 3.4: Guardian Rule Engine Tests (Priority: Medium)
- [ ] Create `tests/test_guardian.py`
- [ ] Test brand safety rule evaluation
- [ ] Test security rule pattern matching
- [ ] Test compliance rule checking
- [ ] Test escalation decision logic

## Phase 4: Infrastructure Configuration

### Task 4.1: Dockerfile Optimization (Priority: High)
- [ ] Update `Dockerfile` with multi-stage build
- [ ] Stage 1: Dependencies (uv install)
- [ ] Stage 2: Build (type checking, linting)
- [ ] Stage 3: Runtime (production image)
- [ ] Configure health checks
- [ ] Optimize image size (<500MB)

**Acceptance Criteria:**
- Multi-stage build reduces final image size
- Health check endpoint responds
- All environment variables documented

### Task 4.2: Makefile Commands (Priority: High)
- [ ] Update `Makefile` with governance commands:
  ```makefile
  lint:  ## Run ruff and mypy
  test:  ## Run test suite with coverage
  format: ## Format code with ruff
  check: ## Run all checks (lint, test, type)
  guardian-check: ## Validate spec compliance
  guard: ## Run symbolic guardian on artifacts
  ```
- [ ] Document each command with docstrings
- [ ] Add dependency ordering

**Acceptance Criteria:**
- `make guard` validates all artifacts
- `make guardian-check` ensures spec alignment
- Help output is descriptive

### Task 4.3: GitHub Actions Workflow (Priority: High)
- [ ] Update `.github/workflows/main.yml` with governance gates:
  - Spec compliance check
  - Symbolic guardian validation
  - TDD test enforcement
  - Docker image scanning

**Workflow Stages:**
```yaml
stages:
  1. lint-and-type     # ruff, mypy
  2. guardian-check    # spec alignment validation
  3. unit-tests        # TDD test suite
  4. integration-tests # Agent communication tests
  5. build             # Docker image
  6. scan              # Security scan
```

**Acceptance Criteria:**
- Guardian check blocks non-compliant PRs
- All tests must pass before merge
- Docker image scanned for vulnerabilities

## Phase 5: Documentation & Governance

### Task 5.1: Project README (Priority: Medium)
- [ ] Update `README.md` with architecture diagram
- [ ] Document quick start guide
- [ ] List all commands with examples
- [ ] Document contribution guidelines
- [ ] Include governance overview

### Task 5.2: Governance Documentation (Priority: Medium)
- [ ] Create `GOVERNANCE.md`
- [ ] Document amendment process
- [ ] List current governors
- [ ] Define escalation procedures
- [ ] Document rule update process

## Task Dependencies

```
Phase 1 (Specs Foundation)
├── 1.1 _meta.md ──────────────────────┐
├── 1.2 functional.md ─────────────────┼──► Required before Phase 2
└── 1.3 technical.md ──────────────────┘

Phase 2 (Skills)
├── 2.1 fetch_trends ───────────────────┐
├── 2.2 generate_script ─────────────────┼──► Requires Phase 1
└── 2.3 symbolic_judge ──────────────────┘

Phase 3 (Tests)
├── 3.1 Skills Interface ──────────────┐
├── 3.2 Data Schemas ───────────────────┼──► Requires Phase 2
├── 3.3 Agent Integration ──────────────┤
└── 3.4 Guardian Rules ─────────────────┘

Phase 4 (Infrastructure)
├── 4.1 Dockerfile ──────────────────────┐
├── 4.2 Makefile ───────────────────────┼──► Can run in parallel
└── 4.3 GitHub Actions ──────────────────┘

Phase 5 (Documentation)
├── 5.1 README ─────────────────────────┤
└── 5.2 GOVERNANCE ─────────────────────┘──► Final step
```

## Success Criteria

### Metric Targets
- [ ] Test coverage: >80%
- [ ] Type safety: 100% mypy compliance
- [ ] Linting: 0 ruff violations
- [ ] Docker image: <500MB
- [ ] Guardian rules: >95% coverage

### Governance Gates
- [ ] All PRs pass guardian check
- [ ] All specs are versioned
- [ ] All tests are in TDD state
- [ ] All infrastructure is automated

## References
- [Constitution](speckit.constitution)
- [Architecture](specs/architecture.md)
- [Autonomous Influencer Factory](specs/autonomous_influencer_factory.md)
