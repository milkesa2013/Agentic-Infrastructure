# MCP Configuration Specification

This document specifies the Model Context Protocol (MCP) configuration for Project Chimera. All MCP servers must be documented here with their purposes, capabilities, and usage patterns.

## Overview

Project Chimera uses MCP to enable secure, standardized communication between AI agents, development tools, and external services. MCP provides a unified interface for agent interactions with the filesystem, databases, APIs, and other resources.

## Server Registry

### 1. Tenx Feedback Analytics Server

| Property | Value |
|----------|-------|
| **Server ID** | `tenxfeedbackanalytics` |
| **Type** | HTTP |
| **URL** | `https://mcppulse.10academy.org/proxy` |
| **Enabled** | `true` |
| **Priority** | Critical |

**Capabilities:**
- Telemetry data collection
- Agent decision traceability
- Real-time event streaming
- Performance metrics aggregation

**Headers:**
```
X-Device: windows
X-Coding-Tool: vscode
```

**Usage Example:**
```python
from chimera.core.mcp import TenxMCPClient

client = TenxMCPClient()
await client.send_event({
    "event_type": "agent_decision",
    "agent_id": "trend_worker_001",
    "decision": "content_approved",
    "confidence": 0.95
})
```

---

### 2. Filesystem Server

| Property | Value |
|----------|-------|
| **Server ID** | `filesystem` |
| **Type** | stdio |
| **Command** | `npx -y @modelcontextprotocol/server-filesystem ./` |
| **Enabled** | `true` |
| **Priority** | Critical |

**Capabilities:**
- Read/write files in project directory
- Directory listing and navigation
- File globbing and search
- Symbolic link resolution

**Allowed Paths:**
```
./                    # Project root (read/write)
./specs/              # Specifications (read/write)
./src/                # Source code (read/write)
./tests/             # Tests (read/write)
./skills/            # Skills directory (read/write)
```

**Restricted Paths:**
```
/etc/                 # System configuration
~/.ssh/              # SSH keys
/root/               # Root directory
```

---

### 3. GitHub Server

| Property | Value |
|----------|-------|
| **Server ID** | `github` |
| **Type** | stdio |
| **Command** | `npx -y @modelcontextprotocol/server-github` |
| **Enabled** | `true` |
| **Priority** | High |

**Capabilities:**
- Repository management
- Pull request creation and review
- Issue tracking
- Commit history access
- Branch management

**Required Permissions:**
```
repo:read    # Read repository contents
repo:write   # Create PRs and issues
```

**Usage Example:**
```python
from chimera.core.mcp import GitHubMCPClient

client = GitHubMCPClient()
pr = await client.create_pull_request(
    title="feat: Add trend detection skill",
    body="Implements SPEC-TREND-001",
    head="feature/trend-detection",
    base="main"
)
```

---

### 4. Memory Server

| Property | Value |
|----------|-------|
| **Server ID** | `memory` |
| **Type** | stdio |
| **Command** | `npx -y @modelcontextprotocol/server-memory` |
| **Enabled** | `true` |
| **Priority** | High |

**Capabilities:**
- Knowledge graph storage
- Entity relationship tracking
- Context persistence across sessions
- Semantic search

**Schema:**
```typescript
interface MemoryNode {
  id: string;
  type: 'agent' | 'task' | 'content' | 'trend';
  properties: Record<string, any>;
  relationships: Relationship[];
}

interface Relationship {
  targetId: string;
  type: 'created_by' | 'depends_on' | 'related_to';
  metadata?: Record<string, any>;
}
```

---

### 5. PostgreSQL Server

| Property | Value |
|----------|-------|
| **Server ID** | `postgres` |
| **Type** | stdio |
| **Command** | `npx -y @modelcontextprotocol/server-postgres <connection_string>` |
| **Enabled** | `false` |
| **Priority** | Medium |

**Connection String:**
```
postgresql://postgres:postgres@localhost:5432/chimera
```

**Capabilities:**
- Database queries
- Schema management
- Transaction support

**Database Schema:**
```sql
-- Agent state tracking
CREATE TABLE agent_state (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) UNIQUE NOT NULL,
    status VARCHAR(32) NOT NULL,
    last_active TIMESTAMP,
    metrics JSONB
);

-- Content moderation queue
CREATE TABLE content_queue (
    id SERIAL PRIMARY KEY,
    content_id VARCHAR(64) UNIQUE NOT NULL,
    platform VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    safety_scores JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Security audit log
CREATE TABLE security_audit (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    agent_id VARCHAR(64),
    event_type VARCHAR(64),
    details JSONB
);
```

---

### 6. Puppeteer Server

| Property | Value |
|----------|-------|
| **Server ID** | `puppeteer` |
| **Type** | stdio |
| **Command** | `npx -y @modelcontextprotocol/server-puppeteer` |
| **Enabled** | `false` |
| **Priority** | Low |

**Capabilities:**
- Browser automation
- Social media platform interactions
- Content preview rendering

**Usage Example:**
```python
from chimera.core.mcp import PuppeteerMCPClient

client = PuppeteerMCPClient()
screenshot = await client.capture_page(
    url="https://tiktok.com/@user/video/123",
    selector=".video-container"
)
```

## Input Streams

### Tenx Events Stream

| Property | Value |
|----------|-------|
| **Type** | SSE (Server-Sent Events) |
| **URL** | `https://mcppulse.10academy.org/events` |
| **Name** | `tenx-events` |

**Event Types:**
```
agent:startup        # Agent initialized
agent:decision       # Agent made a decision
agent:error          # Agent encountered error
content:generated    # Content created
content:published    # Content posted to platform
security:alert       # Security violation detected
```

## Client Configuration

### Application Metadata

```json
{
  "client": {
    "capabilities": {
      "sampling": true,
      "logging": true
    },
    "application": {
      "name": "Project Chimera IDE",
      "version": "1.0.0"
    }
  }
}
```

## Security Considerations

### Authentication
- All HTTP servers use header-based authentication
- Environment variables for sensitive credentials
- No hardcoded API keys in configuration

### Authorization
- Filesystem server restricted to project directory
- Database server uses least-privilege user
- GitHub server uses token with minimal scopes

### Rate Limiting
- Tenx Analytics: 100 requests/minute
- GitHub: 50 requests/minute
- PostgreSQL: 1000 queries/minute

## Installation Instructions

```bash
# Install MCP CLI
npm install -g @modelcontextprotocol/cli

# Install recommended servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-postgres
npm install -g @modelcontextprotocol/server-puppeteer

# Configure VS Code
cp specs/mcp_configuration.md .vscode/mcp.json
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection timeout | Check network connectivity, verify URL |
| Permission denied | Review allowed paths in filesystem config |
| Token expired | Refresh GitHub personal access token |
| Database unreachable | Verify PostgreSQL is running locally |

### Health Check Commands

```bash
# Check filesystem server
mcp-cli filesystem health

# Check GitHub connection
mcp-cli github status

# Verify Tenx endpoint
curl https://mcppulse.10academy.org/health
```
