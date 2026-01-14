---
description: Run one iteration of the RP loop - research codebase, compare to specs, update IMPLEMENTATION_PLAN.md
---

# Research-Plan Loop

## Configuration

Check for `rp.conf.json` in the project root or `scripts/` directory for project-specific settings.

Defaults:
- Specs file: `specs/README.md`, `SPEC.md`, or `README.md`
- Source directories: `src/`, `lib/`, or root
- Plan file: `IMPLEMENTATION_PLAN.md`

## Phase 1: Gather Context

1a. Read project specifications:
    - Check for `specs/README.md`, `SPEC.md`, or main `README.md`
    - Check for `CLAUDE.md` for project structure hints

1b. Read `IMPLEMENTATION_PLAN.md` if it exists
    - Note: existing plan may be outdated or incorrect - verify against actual code

## Phase 2: Research Current State

Use parallel **codebase-analyzer** subagents to analyze the codebase. Launch all four in parallel:

### 2a. Spec Coverage Analysis
Spawn a **codebase-analyzer** agent:
```
Analyze the codebase to compare against these specifications: [paste key spec points]

For each feature in the specs:
- Check if corresponding code exists
- Identify features mentioned but not implemented
- Identify partial implementations (started but incomplete)

Return findings with file paths and line numbers.
```

### 2b. TODO/FIXME Search
Spawn a **codebase-analyzer** agent:
```
Search the codebase for incomplete work markers:
- TODO, FIXME, XXX, HACK
- "not implemented", "placeholder", "stub"

Document each finding with file path, line number, and surrounding context.
```

### 2c. Placeholder Detection
Spawn a **codebase-analyzer** agent:
```
Find minimal or placeholder implementations in the codebase:
- Functions that throw "not implemented" errors
- Functions returning hardcoded/dummy values
- Empty function bodies or pass-through stubs
- Comments indicating temporary implementations

Return file paths and descriptions of each placeholder found.
```

### 2d. Test Coverage Gaps
Spawn a **codebase-analyzer** agent:
```
Analyze test coverage in the codebase:
- Features with no corresponding tests
- Test files with skipped/pending tests (.skip, @pytest.mark.skip, etc.)
- Areas where tests exist but are incomplete

Return findings with file paths and what's missing.
```

## Phase 3: Synthesize Findings

Wait for all subagents to complete, then:

3a. Compile all findings into categories:
    - **Missing**: Features in specs with no implementation
    - **Incomplete**: Partial implementations, TODOs, placeholders
    - **Untested**: Implemented but lacking tests
    - **Bugs**: Issues discovered during analysis

3b. Prioritize items:
    - P0: Blocking/critical - breaks core functionality
    - P1: High - major features missing
    - P2: Medium - enhancements, non-critical gaps
    - P3: Low - nice-to-haves, cleanup

## Phase 4: Update IMPLEMENTATION_PLAN.md

**Monitor context usage throughout** - check periodically.

Write/update `IMPLEMENTATION_PLAN.md` with this structure:

```markdown
# Implementation Plan

Last updated: [DATE] by RP Loop

## Specifications Reference
- [Link to specs file]

## Priority Tasks

### P0 - Critical
- [ ] Task description
  - Context: [why this is critical]
  - Location: [relevant files]

### P1 - High Priority
- [ ] Task description
  - Context: [brief explanation]
  - Location: [relevant files]

### P2 - Medium Priority
- [ ] Task description

### P3 - Low Priority
- [ ] Task description

## Completed
- [x] Completed task (moved here when done)

## Out of Scope / Future Work
- Items explicitly deferred
```

### Guidelines for the plan:
- Each task should be actionable and specific
- Include file paths where work is needed
- Group related items together
- Mark items `[x]` if already implemented (verify first!)
- Move completed items to the Completed section
- Keep descriptions concise but clear

## Phase 5: Exit

### Exit: Analysis Complete

If you finish analyzing and updating the plan:
1. Run `/ralph_commit` to commit the updated plan
2. Output summary:
   - How many new items added
   - How many items marked complete
   - Top priority items for next RI loop iteration

### Exit: Context Limit (60%)

If context reaches 60% before completion:
1. STOP analyzing immediately
2. Add a handoff section at the top of IMPLEMENTATION_PLAN.md:
   ```markdown
   ## RP Loop Handoff

   **Status:** Partial analysis - next run will continue
   **Last analyzed:**
   - [x] Spec coverage analysis
   - [x] TODO/FIXME search
   - [ ] Placeholder detection (incomplete)
   - [ ] Test coverage gaps (not started)

   **Findings so far:**
   - Summary of what was discovered
   - Categories already processed
   ```
3. Run `/ralph_commit` to commit partial progress
4. Exit - next loop iteration picks up from handoff

## Important Guidelines

1. **Verify before marking complete** - Don't assume items are done, check the code

2. **Be specific** - "Fix authentication" is bad, "Add JWT token refresh in auth/refresh.ts" is good

3. **Include context** - Brief explanation helps the implementing agent understand why

4. **Don't duplicate** - Check if an item already exists before adding

5. **Prune stale items** - Remove items that are no longer relevant

6. **Cross-reference specs** - Link plan items back to spec sections when possible
