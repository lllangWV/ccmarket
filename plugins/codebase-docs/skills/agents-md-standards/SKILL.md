---
name: agents-md-standards
description: This skill provides standards and best practices for writing AGENTS.md or CLAUDE.md files. Use when discussing AGENTS.md structure, CLAUDE.md best practices, context engineering for AI agents, onboarding agents to codebases, or how to write effective agent instruction files.
---

# AGENTS.md Structure Guide

This skill provides principles and structure for writing AGENTS.md (or CLAUDE.md). Activate this skill AFTER research and discussion when ready to write the file.

## Core Principle: LLMs Are Stateless

AGENTS.md is the **only file** that goes into every conversation with the agent. Critical implications:

1. Agents know nothing about the codebase at session start
2. Agents must be told what's important each time
3. AGENTS.md is the highest leverage point - every line affects every task

Craft it carefully. Keep it short. Make every line count.

## The Three Questions

AGENTS.md onboards the agent by answering:

| Question | Content |
|----------|---------|
| **WHAT** | Tech stack, project structure, codebase map |
| **WHY** | Purpose of project, what different parts do |
| **HOW** | How to work on it, verify changes, run tests |

## Critical Constraints

### Less Is More

Research indicates:
- Frontier LLMs follow ~150-200 instructions reliably
- Claude Code's system prompt uses ~50 instructions already
- Instruction-following degrades uniformly as count increases

**Target: <100 lines. Absolute max: 300 lines.**

### Universal Applicability

Since AGENTS.md goes into every session:
- Include only instructions that apply to all tasks
- Avoid task-specific details (schemas, API specifics)
- If it only matters sometimes, put it elsewhere

Claude ignores AGENTS.md content deemed irrelevant. More irrelevant content causes more ignoring of everything.

### Progressive Disclosure

Tell agents where to find information, not everything they might need:

```markdown
## Documentation

| Topic | Location |
|-------|----------|
| Architecture | `specs/architecture.md` |
| Database | `specs/database.md` |
```

**Prefer pointers to copies.** Use `file:line` references instead of embedding snippets.

### Don't Be a Linter

Never send an LLM to do a linter's job:
- LLMs are expensive and slow compared to linters
- Style guidelines bloat context and degrade performance
- LLMs learn patterns from the codebase itself

Use actual linters. Configure pre-commit hooks. Let agents focus on logic.

## Template

```markdown
# [Project Name]

[One sentence: what this project is]

## Stack

[Tech stack - language, framework, key dependencies]

## Structure

```
[root]/
├── src/           # [Purpose]
├── tests/         # [Purpose]
├── specs/         # Design specifications
└── docs/          # Documentation
```

## Commands

| Task | Command |
|------|---------|
| Build | `[cmd]` |
| Test | `[cmd]` |
| Lint | `[cmd]` |

## Documentation

Read before starting relevant work:

| Topic | Location |
|-------|----------|
| [Domain] | `specs/[file].md` |

## Boundaries

### Always
- [Universal requirements]

### Never
- [Hard prohibitions]
```

Target ~50 lines for the core file.

## Section Guidance

### Stack (2-5 lines)

Be specific but brief:

```markdown
## Stack

Rust 1.75+, Tokio async runtime, SQLite with SQLx, Ratatui TUI
```

Not every dependency. Just enough to orient the agent.

### Structure (5-10 lines)

A map, not an inventory:

```markdown
## Structure

```
project/
├── crates/        # Rust workspace crates
├── specs/         # Design specifications
└── tests/         # Integration tests
```
```

Top-level orientation only.

### Commands (5-10 lines)

Only universally-needed commands:

```markdown
## Commands

| Task | Command |
|------|---------|
| Build | `cargo build` |
| Test | `cargo test` |
| Lint | `cargo clippy -- -D warnings` |
```

File-specific commands belong in progressive disclosure docs.

### Documentation Pointers (5-10 lines)

Direct agents to detailed docs:

```markdown
## Documentation

| Topic | Location |
|-------|----------|
| Architecture | `specs/architecture.md` |
| State machine | `specs/state-machine.md` |
```

This enables progressive disclosure - agents read these when relevant.

### Boundaries (5-10 lines)

Only universal, critical rules:

```markdown
## Boundaries

### Always
- Run tests before committing
- Read relevant specs before implementing

### Never
- Commit secrets or credentials
- Force push to main
```

Keep it tight. Skip "Ask First" unless truly universal.

## What NOT to Include

| Exclude | Why | Where It Belongs |
|---------|-----|------------------|
| Code style guidelines | Use linters instead | `.eslintrc`, `rustfmt.toml` |
| Database schemas | Not universal | `specs/database.md` |
| API details | Task-specific | `specs/api.md` |
| Component patterns | Task-specific | `specs/[component].md` |
| Git workflow details | Only for commits | `docs/git-workflow.md` |
| Code snippets | Become stale | Use `file:line` pointers |

## The Leverage Principle

```
Bad line → Affects every task → Compounds across artifacts → Maximum negative leverage
Good line → Affects every task → Compounds across artifacts → Maximum positive leverage
```

Don't auto-generate AGENTS.md. Craft every line intentionally.

## Checklist Before Writing

- Is this instruction universally applicable?
- Can this be handled by a linter instead?
- Should this be in a spec file instead?
- Is this a pointer or a copy? (prefer pointers)
- Does this fit in <100 lines total?
- Would removing this hurt every task?

If most answers aren't "yes", reconsider including it.

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/anti-patterns.md`** - Common mistakes and why they fail
- **`references/progressive-disclosure.md`** - How to structure docs hierarchy
