---
description: Auto-find and implement the most recent detailed plan from thoughts/shared/plans/
---

# Implement Plan (Auto-Find)

Automatically locate and implement the most recent detailed implementation plan.

## Phase 1: Find the Plan

1a. Search for detailed plans in `thoughts/shared/plans/`:
```bash
ls -t thoughts/shared/plans/*.md 2>/dev/null | head -5
```

1b. Selection logic:
    - If `IMPLEMENTATION_PLAN.md` has a task with `**Detailed Plan:**` reference, use that plan
    - Otherwise, use the most recently modified plan file

1c. If no plans found:
```
No implementation plans found in thoughts/shared/plans/

To create a plan:
1. Run the RP loop to generate IMPLEMENTATION_PLAN.md
2. Run /detailed_plan_auto to create a detailed plan for the top task
```
Exit.

1d. Output selected plan:
```
Found implementation plan: [path]
Created: [date from filename]
Task: [title from plan]

Reading plan...
```

## Phase 2: Parse and Understand Plan

2a. Read the plan file completely (no limit/offset)

2b. Check for existing progress:
    - Look for `[x]` checkmarks in success criteria
    - Look for `## INCOMPLETE - Handoff Required` section
    - Identify which phase to start/resume

2c. Read all files mentioned in the plan:
    - Files in "Changes Required" sections
    - Files in "References" section
    - Any file:line references

2d. Output status:
```
Plan Status:
  Total phases: [N]
  Completed: [X]
  Current phase: [N] - [Phase Name]

Starting implementation...
```

## Phase 3: Implement Current Phase

For the current uncompleted phase:

3a. Read all files that will be modified in this phase

3b. Make the changes described in the plan:
    - Follow the exact code examples when provided
    - Match existing patterns in the codebase
    - Write complete implementations, no placeholders

3c. After making changes, run the automated verification:
    - Execute each command in "Automated Verification"
    - Fix any issues before proceeding

3d. Update the plan file - check off completed items:
```markdown
#### Automated Verification:
- [x] Tests pass: `make test`
- [x] Linting passes: `make lint`
```

3e. Pause for manual verification (unless told to continue):
```
Phase [N] Complete - Ready for Manual Verification

Automated verification passed:
- [x] [List what passed]

Please perform the manual verification steps:
- [ ] [Manual step from plan]
- [ ] [Another manual step]

Let me know when manual testing is complete to proceed to Phase [N+1].
```

## Phase 4: Complete or Handoff

### If All Phases Complete:

4a. Update `IMPLEMENTATION_PLAN.md`:
    - Mark the original task as complete: `- [x]`
    - Move to Completed section if one exists

4b. Run `/ralph_commit` to commit all changes

4c. Output summary:
```
Implementation Complete!

Plan: [filename]
Task: [task description]
Changes:
  - [List of files modified]

Verification:
  - All automated checks passed
  - Manual verification confirmed

The task has been marked complete in IMPLEMENTATION_PLAN.md.
```

### If Context Limit (60%) Reached:

4a. STOP implementing immediately

4b. Add handoff section to the plan file:
```markdown
## Implementation Handoff

**Date:** [DATE]
**Phase:** [Current phase number and name]
**Status:** Partial implementation

**Completed:**
- [What was finished]

**In Progress:**
- [What was being worked on]
- [Current state of the code]

**Remaining:**
- [What still needs to be done]

**Next Steps:**
1. [Specific first action for next agent]
```

4c. Check off any completed items in the plan

4d. Run `/ralph_commit` to commit partial progress

4e. Output:
```
Context limit reached - handoff created

Plan: [filename]
Progress: Phase [N] of [M] - [percentage]%
Handoff notes added to plan file.

Run /implement_plan_auto again to continue.
```

## Handling Mismatches

If the code doesn't match what the plan expects:

1. STOP and assess the situation
2. Present the mismatch:
```
Issue in Phase [N]:
Expected: [what the plan says]
Found: [actual situation]
Why this matters: [explanation]

Options:
1. Adapt implementation to current code state
2. Flag for plan revision

How should I proceed?
```

3. If in automated mode (loop), choose option 1 and document the adaptation

## Important Guidelines

1. **Read before changing** - Always read files completely before modifying
2. **Follow the plan** - The plan was carefully designed, follow its intent
3. **Verify each phase** - Run checks before moving on
4. **Document deviations** - If you must deviate from the plan, document why
5. **Clean commits** - Commit after each phase if multiple phases
6. **No partial implementations** - Either complete a phase or create proper handoff
