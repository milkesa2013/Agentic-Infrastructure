# Frontend Specifications

## Overview

This document specifies the frontend requirements for Project Chimera's autonomous influencer management system. The frontend provides a web-based dashboard for monitoring, controlling, and auditing agent operations.

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | React | 18.x |
| Build Tool | Vite | 5.x |
| State Management | Zustand | 4.x |
| Styling | Tailwind CSS | 3.x |
| Charts | Recharts | 2.x |
| Real-time | Socket.io Client | 4.x |

## Architecture

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Dashboard/
│   │   ├── AgentMonitor/
│   │   ├── ContentPreview/
│   │   └── SecurityGate/
│   ├── pages/                # Route pages
│   │   ├── Overview.tsx
│   │   ├── Agents.tsx
│   │   ├── Content.tsx
│   │   ├── Security.tsx
│   │   └── Settings.tsx
│   ├── hooks/                # Custom React hooks
│   │   useAgentStatus.ts
│   │   useWebSocket.ts
│   │   └── useSecurityGate.ts
│   ├── services/             # API clients
│   │   ├── api.ts
│   │   └── websocket.ts
│   ├── store/                # Zustand stores
│   │   ├── agentStore.ts
│   │   ├── contentStore.ts
│   │   └── securityStore.ts
│   ├── types/                # TypeScript definitions
│   │   ├── agent.ts
│   │   ├── content.ts
│   │   └── security.ts
│   └── utils/                # Utility functions
└── package.json
```

## Page Specifications

### 1. Dashboard Overview (`/`)
**Purpose**: High-level system status and key metrics

| Component | Description | Refresh Rate |
|-----------|-------------|--------------|
| Agent Status Panel | Live status of all agents (active/idle/error) | Real-time |
| Content Metrics | Posts today, engagement rate, safety score | 30s |
| Trend Alerts | High-velocity trend notifications | Real-time |
| Recent Activity | Last 10 agent actions with timestamps | Real-time |

### 2. Agent Monitor (`/agents`)
**Purpose**: Detailed view of each agent's state and performance

| Component | Description |
|-----------|-------------|
| Agent List | Filterable list with status badges |
| Agent Detail | Click to expand agent config, logs, and metrics |
| Control Panel | Start/Stop/Pause buttons for each agent |
| Performance Charts | CPU, memory, and task completion rates |

### 3. Content Management (`/content`)
**Purpose**: Review and approve content before publishing

| Component | Description |
|-----------|-------------|
| Pending Queue | Content awaiting approval |
| Content Preview | Full render of generated content |
| Safety Scores | Guardian evaluation results per item |
| Approve/Reject | One-click actions with optional feedback |

### 4. Security Dashboard (`/security`)
**Purpose**: Monitor security posture and audit logs

| Component | Description |
|-----------|-------------|
| Threat Monitor | Real-time security alerts |
| Rule Engine Status | Active/inactive rules and hit counts |
| Audit Log | Complete history of security decisions |
| Compliance Report | SOC2/GDPR compliance status |

### 5. Settings (`/settings`)
**Purpose**: System configuration and user management

| Component | Description |
|-----------|-------------|
| Agent Configuration | Edit thresholds, timeouts, and priorities |
| API Keys | Manage external service credentials |
| User Roles | Admin/Operator/Viewer access levels |
| Webhooks | Configure external notifications |

## API Contracts

### Frontend-Backend Communication

#### WebSocket Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `agent:status` | Server → Client | `{ agentId, status, metrics }` |
| `content:pending` | Server → Client | `{ contentId, preview, safetyScores }` |
| `content:approved` | Client → Server | `{ contentId, approverId }` |
| `security:alert` | Server → Client | `{ alertId, severity, message }` |

#### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List all agents |
| GET | `/api/agents/:id` | Get agent details |
| POST | `/api/agents/:id/start` | Start agent |
| POST | `/api/agents/:id/stop` | Stop agent |
| GET | `/api/content/pending` | Get pending content |
| POST | `/api/content/:id/approve` | Approve content |
| POST | `/api/content/:id/reject` | Reject content |
| GET | `/api/security/logs` | Get security audit log |

## Component Specifications

### AgentCard

```typescript
interface AgentCardProps {
  agentId: string;
  name: string;
  status: 'active' | 'idle' | 'error' | 'maintenance';
  lastActive: ISO8601;
  tasksCompleted: number;
  onStart?: () => void;
  onStop?: () => void;
  onConfigure?: () => void;
}
```

### ContentPreview

```typescript
interface ContentPreviewProps {
  contentId: string;
  platform: 'tiktok' | 'youtube' | 'twitter';
  generatedText: string;
  mediaUrls: string[];
  safetyScore: number;  // 0-100
  brandScore: number;   // 0-100
  onApprove: () => void;
  onReject: (reason?: string) => void;
  onEdit: (changes: string) => void;
}
```

### SecurityGate

```typescript
interface SecurityGateProps {
  contentId: string;
  rules: SecurityRule[];
  scores: {
    brand: number;
    security: number;
    compliance: number;
  };
  clearance: 'approved' | 'flagged' | 'rejected';
}
```

## User Flow Specifications

### Content Approval Flow

```
User navigates to /content
    ↓
System loads pending content queue
    ↓
User clicks content item
    ↓
ContentPreview renders with safety scores
    ↓
User reviews and clicks Approve
    ↓
API receives approval, content scheduled for publishing
    ↓
Dashboard updates with new status
```

### Security Alert Response Flow

```
Security alert triggered
    ↓
WebSocket sends alert to frontend
    ↓
Security dashboard shows toast notification
    ↓
Alert appears in Threat Monitor with severity badge
    ↓
User clicks alert to view details
    ↓
Audit log shows full context and previous decisions
    ↓
User takes action: Acknowledge, Escalate, or Dismiss
```

## State Management

### Agent Store (Zustand)

```typescript
interface AgentState {
  agents: Map<string, AgentStatus>;
  selectedAgent: string | null;
  isLoading: boolean;
  error: string | null;
  actions: {
    fetchAgents: () => Promise<void>;
    selectAgent: (id: string) => void;
    updateAgentStatus: (id: string, status: AgentStatus) => void;
  };
}
```

### Security Store

```typescript
interface SecurityState {
  alerts: SecurityAlert[];
  activeRules: SecurityRule[];
  auditLog: AuditEntry[];
  actions: {
    addAlert: (alert: SecurityAlert) => void;
    dismissAlert: (id: string) => void;
    loadAuditLog: () => Promise<void>;
  };
}
```

## Performance Requirements

| Metric | Target |
|--------|--------|
| Initial Load Time | < 3s |
| Dashboard Refresh | < 500ms |
| WebSocket Reconnection | < 2s |
| Content Preview Render | < 200ms |
| API Response (95th percentile) | < 500ms |

## Accessibility Requirements

- WCAG 2.1 AA compliance
- Keyboard navigation for all interactive elements
- ARIA labels for screen readers
- Color contrast ratio ≥ 4.5:1
- Support for reduced motion preferences

## Security Requirements

- JWT-based authentication with 24-hour expiry
- Role-based access control (RBAC)
- CSP headers configured for frontend assets
- No sensitive data in local storage
- HTTPS mandatory for all connections
