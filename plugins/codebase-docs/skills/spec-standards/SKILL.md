---
name: spec-standards
description: This skill provides standards and structure for writing specification documents. Use when discussing specs directory organization, design documentation, architecture docs, spec file structure, or how to write effective technical specifications for a project.
---

# Specification Document Structure Guide

This skill provides structure for writing design specifications. Activate AFTER research and discussion when ready to write specs.

## The Two-Tier Model

| Document | Purpose |
|----------|---------|
| **AGENTS.md** | How to work on the project (operational) |
| **specs/** | What the project is and does (architectural) |

AGENTS.md points to specs/. Specs contain the detailed documentation that agents read when relevant.

## specs/README.md Structure

The index file organizes specs by domain with tables linking to documents and code.

```markdown
# [Project Name] Specifications

[1-2 sentence description]

## [Domain Name]

[Optional: 1 sentence describing domain]

| Spec | Code | Purpose |
|------|------|---------|
| [filename.md](./filename.md) | [path/](../src/path/) | Brief description |

## [Another Domain]

| Spec | Code | Purpose |
|------|------|---------|
| [spec.md](./spec.md) | [module/](../src/module/) | Brief description |
```

### Key Principles

- **Group by domain** - Core, API, Data, UI, Infrastructure, etc.
- **Link to code** - Every spec references its implementation location
- **Brief purpose** - One phrase explaining what it does
- **Alphabetize within groups** - For findability

### Common Domains

Adapt to the project:

- **Core Architecture** - Foundational systems, module structure
- **API Layer** - Endpoints, contracts, authentication
- **Data Layer** - Storage, schemas, migrations
- **UI/Frontend** - Components, state, routing
- **Infrastructure** - Deployment, observability, configuration
- **Integrations** - External services, protocols

## Individual Spec Structure

Each `specs/[component].md` follows this template:

```markdown
# [Component Name] Specification

## Overview

[2-3 paragraphs covering:]
- What this component does
- Why it exists (problem it solves)
- Key design principles

## Structure

[Module/directory layout]

```
path/to/component/
├── mod.rs          # Public API
├── types.rs        # Core types
├── impl.rs         # Implementation
└── tests.rs        # Tests
```

## Core Concepts

### [Concept 1]

[Definition and explanation]

### [Concept 2]

[Definition and explanation]

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| [What was chosen] | [Why this over alternatives] |

## Interfaces

[Public API, traits, contracts]

```[language]
pub trait Example {
    fn method(&self) -> Result<T>;
}
```

## Data Flow

[How data moves through the component]

```
Input → Validation → Processing → Output
            ↓             ↓
         Errors      Side Effects
```

## Dependencies

**Depends on:**
- [upstream component] - [why]

**Depended on by:**
- [downstream component] - [how]

## Extension Points

[How to extend this component]

1. To add [X], implement [Y] trait
2. Register in [Z]

## Error Handling

[Error types, how failures propagate]

## Testing Strategy

[How this is tested, what coverage exists]
```

## Section Selection

Not every spec needs every section. Use what's relevant:

| Section | When to Include |
|---------|-----------------|
| Overview | Always |
| Structure | Meaningful directory organization exists |
| Core Concepts | Domain terminology needs definition |
| Design Decisions | Non-obvious choices were made |
| Interfaces | Public API exists |
| Data Flow | Data transformation is complex |
| Dependencies | Relationships matter for understanding |
| Extension Points | Component designed to be extended |
| Error Handling | Defined error strategy exists |
| Testing Strategy | Testing approach is specific |

## Writing Guidelines

### Be Specific

```markdown
# Good
Uses SQLite with WAL mode for concurrent reads

# Bad
Uses a database
```

### Show, Don't Tell

- Include actual code snippets for interfaces
- Use ASCII diagrams for architecture
- Provide concrete examples

### Explain the Why

- Design decisions need rationale
- Link to ADRs if they exist
- Note alternatives considered

### Use File:Line References

For patterns that exist in code:

```markdown
| Pattern | Reference |
|---------|-----------|
| Component structure | `src/components/Button.tsx:15` |
| Error handling | `src/errors/mod.rs:42` |
```

### Keep Current

- Date major revisions
- Mark deprecated sections
- Update when code changes significantly

## After Writing

1. Add entry to `specs/README.md` for new specs
2. Verify code links are accurate
3. Check referenced files/modules exist
4. Add pointer in AGENTS.md Documentation section if not present
5. Consider if related specs need updates

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/spec-examples.md`** - Real-world spec file examples
- **`references/diagrams.md`** - ASCII diagram patterns for specs
