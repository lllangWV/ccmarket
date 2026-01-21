# Progressive Disclosure for Agent Documentation

How to structure documentation so agents load context only when needed.

## The Problem

Stuffing everything into AGENTS.md fails because:
- Context window has limits
- Instruction-following degrades with count
- Most content is irrelevant to any single task
- Irrelevant content causes ignoring of relevant content

## The Solution: Three-Level Loading

```
Level 1: AGENTS.md (always loaded)
    ↓
Level 2: specs/README.md (loaded when exploring)
    ↓
Level 3: specs/*.md, docs/*.md (loaded when relevant)
```

Each level loads only when needed, keeping context focused.

## Directory Structure

```
project/
├── AGENTS.md              # <100 lines, universal, pointers
├── specs/
│   ├── README.md          # Index of all specs
│   ├── architecture.md    # System design
│   ├── database.md        # Data layer
│   ├── api.md             # API contracts
│   └── [component].md     # Per-component specs
└── docs/
    ├── testing.md         # Testing patterns
    ├── git-workflow.md    # Git conventions
    └── deployment.md      # Deployment process
```

## What Goes Where

### AGENTS.md (Always Loaded)

**Include:**
- Project identity (1 sentence)
- Tech stack (1 line)
- Top-level structure (5-10 lines)
- Universal commands (5-10 lines)
- Pointers to specs/docs (5-10 lines)
- Universal boundaries (5-10 lines)

**Target:** <100 lines, <50 instructions

### specs/README.md (Loaded When Exploring)

**Include:**
- Index table of all specs
- Brief description of each
- Links to code locations

**Format:**
```markdown
# Specifications

## Core Architecture

| Spec | Code | Purpose |
|------|------|---------|
| [architecture.md](./architecture.md) | [src/](../src/) | System design |

## Data Layer

| Spec | Code | Purpose |
|------|------|---------|
| [database.md](./database.md) | [src/db/](../src/db/) | Schema and queries |
```

### specs/*.md (Loaded When Relevant)

**Include:**
- Deep documentation for one domain
- Design decisions and rationale
- Interfaces and contracts
- Data flow diagrams
- Extension points

**No length limit** - these load only when agent needs them.

### docs/*.md (Loaded When Relevant)

**Include:**
- Operational guides (testing, deployment)
- Workflow documentation (git, CI/CD)
- Troubleshooting guides

## How Agents Use This

1. **Session starts** → AGENTS.md loaded
2. **Task received** → Agent reads Documentation pointers
3. **Relevant domain identified** → Agent reads specific spec
4. **Implementation begins** → Agent has focused context

Example flow:
```
User: "Add a new API endpoint for user preferences"

Agent thinks:
- AGENTS.md says API docs at specs/api.md
- Read specs/api.md for contracts and patterns
- Implement following established patterns
```

## Pointers vs Copies

**Pointer (good):**
```markdown
| API contracts | `specs/api.md` |
```

**Copy (bad):**
```markdown
## API Patterns

All endpoints should:
```typescript
export const handler = async (req: Request, res: Response) => {
  // ... 20 lines of example
};
```
```

**Why pointers win:**
- Never become stale
- Don't consume AGENTS.md budget
- Agent reads authoritative source
- Can be arbitrarily detailed

## File:Line References

For specific patterns, use precise pointers:

```markdown
## Patterns

| Pattern | Reference |
|---------|-----------|
| Component structure | `src/components/Button.tsx:15` |
| API handler | `src/api/users.ts:42` |
| Test setup | `tests/helpers/setup.ts:1` |
```

Agent reads the actual code, which is always current.

## When to Create New Specs

Create a new spec when:
- Domain has significant complexity
- Multiple files implement the domain
- Design decisions need documentation
- Patterns should be followed consistently

Don't create specs for:
- Trivial modules
- Standard library usage
- Self-explanatory code

## Maintaining the Hierarchy

### Adding New Domains

1. Create `specs/[domain].md`
2. Add entry to `specs/README.md`
3. Add pointer in AGENTS.md Documentation section

### Updating Existing Specs

1. Update the spec file
2. No changes needed to AGENTS.md (pointers don't change)

### Removing Domains

1. Delete spec file
2. Remove from `specs/README.md`
3. Remove pointer from AGENTS.md

## Benefits

1. **Focused context** - Agent only loads what's relevant
2. **Unlimited depth** - Specs can be as detailed as needed
3. **Easy maintenance** - Update specs without touching AGENTS.md
4. **Better instruction-following** - AGENTS.md stays under limits
5. **Authoritative sources** - Pointers lead to current information
