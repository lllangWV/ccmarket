# Spec File Examples

Real-world examples of well-structured specification documents.

## Example: Architecture Spec

```markdown
# Architecture Specification

## Overview

Loom is an AI-powered coding agent built in Rust. The system uses a
workspace of interconnected crates that separate concerns while
maintaining clear dependency boundaries.

The architecture follows three principles:
1. **Modularity** - Each crate has a single responsibility
2. **Extensibility** - New providers and tools plug in via traits
3. **Reliability** - Errors are typed and recoverable

## Structure

```
crates/
├── loom-core/       # Shared types and traits
├── loom-llm/        # LLM client abstractions
├── loom-tools/      # Tool registry and execution
├── loom-agent/      # Agent state machine
├── loom-tui/        # Terminal UI
└── loom-server/     # HTTP API server
```

## Core Concepts

### Crate

A Rust compilation unit with defined public API. Each crate exposes
types and functions through its lib.rs.

### Workspace

The collection of crates that compile together. Defined in root
Cargo.toml with shared dependencies.

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Workspace over single crate | Faster incremental builds, clearer boundaries |
| Traits for providers | Easy to add new LLM providers without touching core |
| Typed errors with thiserror | Compile-time error handling, good error messages |

## Dependency Flow

```
loom-core (no deps)
    ↓
loom-llm (depends on core)
loom-tools (depends on core)
    ↓
loom-agent (depends on llm, tools)
    ↓
loom-tui (depends on agent)
loom-server (depends on agent)
```

Dependencies flow downward only. No cycles allowed.

## Extension Points

### Adding an LLM Provider

1. Implement `LlmClient` trait in `loom-llm/src/providers/`
2. Add variant to `Provider` enum
3. Register in `create_client()` factory

See `loom-llm/src/providers/anthropic.rs:25` for reference.

### Adding a Tool

1. Implement `Tool` trait in `loom-tools/src/tools/`
2. Add to `ToolRegistry` in `loom-tools/src/registry.rs`

See `loom-tools/src/tools/read_file.rs:1` for reference.
```

## Example: State Machine Spec

```markdown
# Agent State Machine Specification

## Overview

The agent operates as a finite state machine, transitioning between
states based on LLM responses and tool execution results. This ensures
predictable behavior and enables proper error recovery.

## States

```
                    ┌─────────────┐
                    │   Idle      │
                    └──────┬──────┘
                           │ user message
                           ▼
                    ┌─────────────┐
          ┌────────│  Thinking   │────────┐
          │        └─────────────┘        │
          │ tool call                     │ text response
          ▼                               ▼
    ┌─────────────┐                ┌─────────────┐
    │  Executing  │                │  Responding │
    └──────┬──────┘                └──────┬──────┘
           │ tool result                  │
           └──────────┬───────────────────┘
                      ▼
               ┌─────────────┐
               │   Idle      │
               └─────────────┘
```

## Core Concepts

### State

Current phase of agent operation. Determines valid transitions and
available actions.

### Transition

Movement from one state to another, triggered by events. Each
transition may have side effects.

### Event

Input that causes state transition: user message, LLM response,
tool result, error.

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| Explicit state enum | Compiler enforces valid states |
| Transition functions return new state | Immutable, testable |
| Events as enum variants | Exhaustive matching prevents missed cases |

## Interfaces

```rust
pub enum AgentState {
    Idle,
    Thinking { context: Context },
    Executing { tool: ToolCall },
    Responding { content: String },
}

pub enum Event {
    UserMessage(String),
    LlmResponse(Response),
    ToolResult(Result<Value, Error>),
}

impl AgentState {
    pub fn transition(self, event: Event) -> AgentState {
        // State machine logic
    }
}
```

## Error Handling

Errors don't break the state machine. Instead:

1. Tool errors → Transition to Thinking with error context
2. LLM errors → Retry with backoff, then transition to Idle with error
3. Parse errors → Transition to Thinking with clarification request

## Testing Strategy

Each transition is unit tested:
- `Idle + UserMessage → Thinking`
- `Thinking + ToolCall → Executing`
- `Executing + ToolResult → Thinking`
- `Thinking + TextResponse → Responding`
- `Responding → Idle`

See `loom-agent/src/state/tests.rs` for complete test suite.
```

## Example: API Spec

```markdown
# API Specification

## Overview

The HTTP API provides programmatic access to the agent. All endpoints
return JSON and use standard HTTP status codes.

## Base URL

```
http://localhost:3000/api/v1
```

## Authentication

Bearer token in Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### POST /threads

Create a new conversation thread.

**Request:**
```json
{
  "model": "claude-3-opus",
  "system": "Optional system prompt"
}
```

**Response:**
```json
{
  "id": "thread_abc123",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### POST /threads/{id}/messages

Send a message to a thread.

**Request:**
```json
{
  "content": "User message text"
}
```

**Response:** Server-Sent Events stream

```
event: thinking
data: {"status": "processing"}

event: tool_use
data: {"tool": "read_file", "input": {"path": "src/main.rs"}}

event: message
data: {"content": "Here's what I found..."}

event: done
data: {}
```

## Error Responses

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Thread not found"
  }
}
```

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| invalid_request | 400 | Malformed request |
| unauthorized | 401 | Missing/invalid token |
| not_found | 404 | Resource doesn't exist |
| rate_limited | 429 | Too many requests |
| internal_error | 500 | Server error |

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| SSE for streaming | Simple, works everywhere, no WebSocket complexity |
| Thread-based model | Matches mental model of conversations |
| JSON everywhere | Universal, debuggable |
```

## Tips for Good Specs

1. **Start with Overview** - Reader should understand purpose in 30 seconds
2. **Include diagrams** - ASCII art works everywhere, easy to update
3. **Show real code** - Interfaces section with actual signatures
4. **Explain decisions** - The "why" is often more valuable than "what"
5. **Link to code** - `file:line` references keep spec connected to reality
6. **Keep updated** - Stale specs are worse than no specs
