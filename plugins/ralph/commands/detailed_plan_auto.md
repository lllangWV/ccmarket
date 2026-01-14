---
description: Auto-select highest priority task from IMPLEMENTATION_PLAN.md and create detailed implementation plan
model: opus
---

# Detailed Plan (Auto-Select)

Create a detailed implementation plan by automatically selecting the highest priority uncompleted task from `IMPLEMENTATION_PLAN.md`.

## Phase 1: Load Implementation Plan

1a. Read `IMPLEMENTATION_PLAN.md` from the project root
    - If not found, exit with error: "No IMPLEMENTATION_PLAN.md found. Run the RP loop first."

1b. Parse the priority sections (P0, P1, P2, P3) and find the **first unchecked task** (`- [ ]`)
    - Priority order: P0 → P1 → P2 → P3
    - Skip any tasks marked as `[x]`

1c. Extract task details:
    - Task description
    - Context (if provided)
    - Location/files mentioned
    - Any existing handoff notes or research links

1d. Output selected task:
```
Selected highest priority task:
  Priority: [P0/P1/P2/P3]
  Task: [task description]
  Context: [context if available]
  Files: [relevant files if mentioned]

Proceeding to create detailed implementation plan...
```

## Phase 2: Research & Context Gathering

2a. Read any files mentioned in the task's Location field

2b. Spawn parallel research agents:

### Codebase Analysis
Spawn a **codebase-analyzer** agent:
```
Analyze the codebase to understand how to implement: [TASK DESCRIPTION]

Find:
- Existing code related to this feature
- Patterns to follow
- Dependencies and integration points
- Test patterns used in similar areas

Return findings with file paths and line numbers.
```

### Pattern Finding
Spawn a **codebase-pattern-finder** agent:
```
Find similar implementations in the codebase that we can use as a model for: [TASK DESCRIPTION]

Look for:
- Similar features already implemented
- Common patterns for this type of change
- Test examples we can follow

Return specific examples with file:line references.
```

2c. If specs exist, read relevant spec files from `specs/` directory

## Phase 3: Design Implementation Approach

3a. Synthesize research findings into implementation approach

3b. Identify phases - break the task into logical implementation steps:
    - Each phase should be independently testable
    - Order phases by dependencies
    - Aim for 2-4 phases for most tasks

3c. If there are multiple valid approaches, present options:
```
Design Options:
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]

Recommended: [Option X] because [reasoning]

Proceeding with recommended approach...
```

## Phase 4: Write Detailed Plan

4a. Generate the plan filename:
    - Format: `YYYY-MM-DD-[priority]-[task-slug].md`
    - Example: `2025-01-13-P1-add-user-authentication.md`

4b. Write plan to `thoughts/shared/plans/[filename]`:

```markdown
# [Task Name] Implementation Plan

## Source
- IMPLEMENTATION_PLAN.md task: [exact task text]
- Priority: [P0/P1/P2/P3]
- Generated: [DATE] by detailed_plan_auto

## Overview

[Brief description of what we're implementing]

## Current State Analysis

[What exists now based on research]

### Key Discoveries:
- [Finding with file:line reference]
- [Pattern to follow]

## Desired End State

[Clear specification of what should exist after implementation]

## What We're NOT Doing

[Explicitly list out-of-scope items]

## Implementation Approach

[High-level strategy]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File]
**File**: `path/to/file.ext`
**Changes**: [Summary]

```[language]
// Specific code changes
```

### Success Criteria:

#### Automated Verification:
- [ ] [Command to run]: `make test` or similar

#### Manual Verification:
- [ ] [What to check manually]

---

## Phase 2: [Descriptive Name]

[Similar structure...]

---

## Testing Strategy

### Unit Tests:
- [What to test]

### Integration Tests:
- [End-to-end scenarios]

## References

- Source task: IMPLEMENTATION_PLAN.md
- Related specs: [if applicable]
- Similar implementation: [file:line if found]
```

4c. Create the directories if needed:
```bash
mkdir -p thoughts/shared/plans
```

## Phase 5: Update IMPLEMENTATION_PLAN.md

5a. Add a reference to the detailed plan under the task:
```markdown
- [ ] Original task description
  - **Detailed Plan:** [thoughts/shared/plans/YYYY-MM-DD-priority-slug.md]
```

5b. Run `/ralph_commit` to commit the plan

## Phase 6: Output Summary

```
Detailed plan created successfully!

Plan file: thoughts/shared/plans/[filename]
Task: [task description]
Priority: [priority]
Phases: [number of phases]

Next step: Run /implement_plan_auto to execute this plan
```

## Exit Conditions

### Success: Plan Created
- Detailed plan written to `thoughts/shared/plans/`
- IMPLEMENTATION_PLAN.md updated with reference
- Changes committed

### Exit: Context Limit (60%)
If context reaches 60% before completion:
1. STOP immediately
2. Save partial plan with note at top:
   ```markdown
   ## INCOMPLETE - Handoff Required
   Status: [what's done, what remains]
   ```
3. Run `/ralph_commit` to commit partial progress
4. Exit - next iteration will continue

### Exit: No Tasks Found
If all tasks in IMPLEMENTATION_PLAN.md are marked complete:
```
All tasks in IMPLEMENTATION_PLAN.md are complete!
Run the RP loop to analyze for new tasks, or add tasks manually.
```

## Important Guidelines

1. **Be thorough** - The plan should be detailed enough for any agent to implement
2. **Include code examples** - Show specific changes, not just descriptions
3. **Testable phases** - Each phase should be verifiable before moving on
4. **No open questions** - Research until all decisions are made
5. **File references** - Always include file:line for existing code
