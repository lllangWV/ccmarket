# ASCII Diagram Patterns for Specs

Patterns for creating clear ASCII diagrams in specification documents.

## Box Diagrams

### Simple Box

```
┌─────────────┐
│   Module    │
└─────────────┘
```

### Box with Sections

```
┌─────────────────┐
│     Header      │
├─────────────────┤
│     Body        │
├─────────────────┤
│     Footer      │
└─────────────────┘
```

### Connected Boxes

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Input   │────▶│ Process │────▶│ Output  │
└─────────┘     └─────────┘     └─────────┘
```

## Flow Diagrams

### Linear Flow

```
Start → Step 1 → Step 2 → Step 3 → End
```

### Flow with Branching

```
        ┌─────────┐
        │  Start  │
        └────┬────┘
             │
             ▼
        ┌─────────┐
        │ Check   │
        └────┬────┘
             │
     ┌───────┴───────┐
     │               │
     ▼               ▼
┌─────────┐     ┌─────────┐
│  Yes    │     │   No    │
└────┬────┘     └────┬────┘
     │               │
     └───────┬───────┘
             │
             ▼
        ┌─────────┐
        │   End   │
        └─────────┘
```

### Parallel Paths

```
             ┌─────────┐
             │  Input  │
             └────┬────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │ Path A │ │ Path B │ │ Path C │
   └────┬───┘ └────┬───┘ └────┬───┘
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
             ┌─────────┐
             │  Merge  │
             └─────────┘
```

## State Machines

### Simple State Machine

```
     ┌──────────────────────────────────┐
     │                                  │
     ▼                                  │
┌─────────┐  event   ┌─────────┐       │
│ State A │─────────▶│ State B │───────┘
└─────────┘          └─────────┘
```

### Complex State Machine

```
                ┌─────────────┐
                │    Idle     │◀──────────────────┐
                └──────┬──────┘                   │
                       │ start                    │
                       ▼                          │
                ┌─────────────┐                   │
      ┌────────▶│  Running    │────────┐          │
      │         └──────┬──────┘        │          │
      │                │               │          │
      │ retry          │ error         │ complete │
      │                ▼               │          │
      │         ┌─────────────┐        │          │
      └─────────│   Error     │        │          │
                └─────────────┘        │          │
                                       ▼          │
                                ┌─────────────┐   │
                                │  Complete   │───┘
                                └─────────────┘
```

## Architecture Diagrams

### Layered Architecture

```
┌─────────────────────────────────────┐
│           Presentation              │
├─────────────────────────────────────┤
│           Application               │
├─────────────────────────────────────┤
│             Domain                  │
├─────────────────────────────────────┤
│          Infrastructure             │
└─────────────────────────────────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────┐
│                    System                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │ Component │  │ Component │  │ Component │   │
│  │     A     │──│     B     │──│     C     │   │
│  └───────────┘  └───────────┘  └───────────┘   │
│        │              │              │          │
│        └──────────────┼──────────────┘          │
│                       │                         │
│                ┌──────┴──────┐                  │
│                │   Shared    │                  │
│                │   Service   │                  │
│                └─────────────┘                  │
└─────────────────────────────────────────────────┘
```

### Dependency Graph

```
        core
       /    \
      /      \
    llm     tools
      \      /
       \    /
       agent
       /    \
      /      \
    tui    server
```

## Data Flow Diagrams

### Simple Transform

```
Input → Validate → Transform → Output
           │            │
           ▼            ▼
        Errors      Side Effects
```

### Pipeline

```
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│ Source │───▶│ Parse  │───▶│Process │───▶│  Sink  │
└────────┘    └────────┘    └────────┘    └────────┘
                  │              │
                  ▼              ▼
              ┌────────┐    ┌────────┐
              │ Errors │    │  Logs  │
              └────────┘    └────────┘
```

### Request/Response

```
┌────────┐         ┌────────┐         ┌────────┐
│ Client │────────▶│ Server │────────▶│   DB   │
│        │◀────────│        │◀────────│        │
└────────┘ request └────────┘  query  └────────┘
           response            result
```

## Sequence Diagrams

### Simple Sequence

```
Client          Server          Database
   │               │                │
   │── request ──▶│                │
   │               │── query ─────▶│
   │               │◀── result ────│
   │◀── response ──│                │
   │               │                │
```

### With Async

```
User            Agent           LLM            Tool
  │               │              │               │
  │── message ──▶│              │               │
  │               │── prompt ──▶│               │
  │               │◀── tool ────│               │
  │               │              │               │
  │               │─────── execute ────────────▶│
  │               │◀────── result ──────────────│
  │               │              │               │
  │               │── continue ─▶│               │
  │               │◀── text ────│               │
  │◀── response ──│              │               │
  │               │              │               │
```

## Characters Reference

### Box Drawing

```
Corners:  ┌ ┐ └ ┘
Lines:    ─ │
T-joins:  ┬ ┴ ├ ┤
Cross:    ┼
```

### Arrows

```
Simple:   → ← ↑ ↓
Triangle: ▶ ◀ ▲ ▼
Double:   ⇒ ⇐ ⇑ ⇓
```

### Other Useful

```
Bullets:  • ○ ◆ ◇
Marks:    ✓ ✗ ★ ☆
Math:     ∞ ≈ ≠ ≤ ≥
```

## Tips

1. **Consistent sizing** - Keep boxes roughly the same size
2. **Align elements** - Use monospace font alignment
3. **Label connections** - Add text near arrows when meaning isn't obvious
4. **Keep simple** - Complex diagrams are hard to maintain
5. **Test rendering** - Check diagram looks right in target format
