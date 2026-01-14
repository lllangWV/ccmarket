---
description: Run one iteration of the RS loop - research external docs and generate cleanroom specs
---

# Research-to-Specs Loop

Generate cleanroom black-box specifications from external documentation.

## Arguments

- `$ARGUMENTS` = Research goal/topic (required)

Example: `/run_ralph_rs REST API authentication patterns`

## Configuration

Defaults:
- Specs directory: `specs/`
- Index file: `specs/README.md`

## Phase 1: Gather Context

1a. Parse the research goal from `$ARGUMENTS`
    - If no goal provided, ask the user what to research

1b. Read existing specs:
    - Read `specs/README.md` if it exists
    - Scan `specs/` directory for existing spec files
    - Identify what's already documented vs gaps

1c. Determine scope:
    - Is this a new topic or expanding existing coverage?
    - What specific aspects should the research focus on?

## Phase 2: Web Research

Launch parallel **web-search-researcher** agents to gather comprehensive documentation.

### 2a. Core Concepts
Spawn a **web-search-researcher** agent:
```
Research: [TOPIC] - core concepts and terminology

Find official documentation covering:
- Fundamental concepts and definitions
- Key terminology and vocabulary
- High-level architecture/structure

Return: Summarized findings with source URLs
```

### 2b. API/Interface Documentation
Spawn a **web-search-researcher** agent:
```
Research: [TOPIC] - API and interface documentation

Find documentation covering:
- Available operations/methods/endpoints
- Input parameters and formats
- Output/response formats
- Error handling and status codes

Return: Summarized findings with source URLs
```

### 2c. Examples & Use Cases
Spawn a **web-search-researcher** agent:
```
Research: [TOPIC] - examples and use cases

Find documentation covering:
- Common usage patterns
- Code examples and tutorials
- Best practices
- Real-world scenarios

Return: Summarized findings with source URLs
```

### 2d. Edge Cases & Limitations
Spawn a **web-search-researcher** agent:
```
Research: [TOPIC] - limitations and edge cases

Find documentation covering:
- Known limitations and constraints
- Rate limits, quotas, restrictions
- Edge cases and gotchas
- Compatibility considerations

Return: Summarized findings with source URLs
```

## Phase 3: Synthesize into Specs

Wait for all agents to complete, then create/update spec files.

**Monitor context usage throughout** - check periodically.

### 3a. Determine file structure
- Single topic → `specs/<topic-slug>.md`
- Complex topic → multiple files: `specs/<topic>/<subtopic>.md`

### 3b. Write spec file(s)

Use this format for each spec file:

```markdown
# <Topic> Specification

Last updated: [DATE] by RS Loop
Sources:
- [Source 1 URL]
- [Source 2 URL]
- ...

## Overview
Brief description of the feature/component being specified.

## Terminology
| Term | Definition |
|------|------------|
| ... | ... |

## Behavior

### Inputs
Describe all inputs, parameters, and their formats.

### Outputs
Describe all outputs, responses, and their formats.

### Operations
Describe available operations/actions and their behavior.

## Constraints & Limitations
- Known limits
- Restrictions
- Requirements

## Examples
Concrete examples demonstrating typical usage.

## Open Questions
- [ ] Items needing further research
- [ ] Unclear aspects to investigate
```

### 3c. Guidelines for cleanroom specs
- **Black-box only**: Describe external behavior, not internal implementation
- **Observable behavior**: What can be seen from outside the system
- **No implementation details**: Avoid mentioning how things work internally
- **Cite sources**: Always include documentation URLs
- **Be precise**: Use exact terminology from official docs

## Phase 4: Update specs/README.md

Update (or create) `specs/README.md` as the index:

```markdown
# Project Specifications

Last updated: [DATE]

## Overview
[Concise project summary - what is being specified]

## Specifications

| Spec | Description |
|------|-------------|
| [topic-1.md](topic-1.md) | Brief description |
| [topic-2.md](topic-2.md) | Brief description |
| ... | ... |

## Research Goals
- [x] Completed topic 1
- [x] Completed topic 2
- [ ] Pending: topic 3
- [ ] Pending: topic 4

## Sources
Primary documentation sources used:
- [Official Docs](url)
- [API Reference](url)
```

## Phase 5: Exit

### Exit: Research Complete

If you finish researching and writing specs:
1. Create specs directory if needed:
   ```bash
   mkdir -p specs
   ```
2. Run `/ralph_commit` to commit the specs
3. Output summary:
   - What spec files were created/updated
   - Key findings from research
   - Any open questions for follow-up

### Exit: Context Limit (60%)

If context reaches 60% before completion:
1. STOP researching/writing immediately
2. Add a handoff section to `specs/README.md`:
   ```markdown
   ## RS Loop Handoff

   **Topic:** [Current research topic]
   **Status:** Partial research - next run will continue

   **Research completed:**
   - [x] Core concepts & terminology
   - [x] API/interface documentation
   - [ ] Examples & use cases (incomplete)
   - [ ] Edge cases & limitations (not started)

   **Findings so far:**
   - Summary of research gathered
   - Source URLs collected
   - Sections already written to spec files
   ```
3. Run `/ralph_commit` to commit partial progress
4. Exit - next loop iteration picks up from handoff

## Important Guidelines

1. **Cleanroom principle**: Never look at existing implementations while writing specs. Only use external documentation.

2. **Cite everything**: Every claim should trace back to a source URL.

3. **Incremental refinement**: Each run should improve existing specs, not overwrite them blindly.

4. **Flag uncertainty**: Use "Open Questions" section for anything unclear.

5. **Keep README.md current**: Always update the index after modifying specs.

6. **Consistent terminology**: Use the same terms throughout all spec files.
