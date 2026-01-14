---
description: Run one iteration of the implementation loop - select task, research if needed, implement with handoff
---

# Implementation Loop

## Configuration

Check for `impl.conf.json` in the project root or `scripts/` directory for project-specific settings.

Defaults:
- Specs file: `specs/README.md`, `SPEC.md`, or `README.md`
- Source directories: `src/`, `lib/`, or root
- Issues directory: `known-issues/`
- Plan file: `IMPLEMENTATION_PLAN.md`
- Research directory: `thoughts/shared/research/`

## Pre-flight: Sync GitHub Issues

-1a. Detect the GitHub repository from git remote:
```bash
GITHUB_REPO=$(git remote get-url origin 2>/dev/null | sed -E 's|.*github\.com[:/]([^/]+/[^/.]+)(\.git)?|\1|')
echo "Detected repo: $GITHUB_REPO"
```

-1b. List open issues and compare with known-issues/:
```bash
curl -s "https://api.github.com/repos/$GITHUB_REPO/issues?state=open" | jq -r '.[].number'
ls known-issues/ 2>/dev/null || mkdir -p known-issues/
```

-1c. For any issues on GitHub not in known-issues/, fetch and save:
```bash
# Replace N with issue number
curl -s "https://api.github.com/repos/$GITHUB_REPO/issues/N" | \
  jq -r '"# \(.title)\n\n**Issue:** [#\(.number)](\(.html_url))\n**Author:** \(.user.login)\n**Created:** \(.created_at[:10])\n**State:** \(.state)\n\n\(.body)"' \
  > known-issues/issue-N.md
```

-1d. Read any new issues in known-issues/ and incorporate them into IMPLEMENTATION_PLAN.md

## Phase 1: Task Selection

1a. Read `IMPLEMENTATION_PLAN.md` and select the **single highest priority feature**
    - Include anything in "out of scope / future work" - that's now in scope!

1b. Check if the selected task has **prior context** (look for indented bullets under the task):
    - A summary bullet starting with "**Handoff:**" describing where the previous agent left off
    - A link to a research document (e.g., `thoughts/shared/research/...`)

## Phase 2: Research or Resume

**IF the task has prior context (handoff summary + research doc link):**
- Read the linked research document
- Skip to Phase 3 (Implementation) and continue from where the previous agent left off

**IF the task has NO prior context:**
- Run `/research_codebase` with the task description as input
- The research will produce a document in `thoughts/shared/research/`
- Note the path to this research document for later
- After research completes, proceed to Phase 3

## Phase 3: Implementation

Implement the selected feature using up to 5 subagents.
- Use the research document as your guide for where things are in the codebase
- Focus on full implementations, no placeholders
- **Monitor context usage throughout** - check periodically

### Exit: Task Complete

If you finish the task:
1. Run verification commands (check CLAUDE.md or package.json/pyproject.toml/Makefile)
   - Typechecking, testing, linting as applicable
   - Ensure all checks pass
2. Mark the task complete in IMPLEMENTATION_PLAN.md
3. Run `/ralph_commit` to commit changes

### Exit: Context Limit (60%)

If context reaches 60% before completion:
1. STOP implementing immediately
2. Add handoff note under the incomplete task in IMPLEMENTATION_PLAN.md:
   ```markdown
   - [ ] The incomplete task description
     - **Handoff:**
       - What was completed
       - What remains to be done
       - Any blockers or issues discovered
       - Current state of the code
     - **Research:** [path/to/research/document.md]
   ```
3. Run `/ralph_commit` to commit partial progress
4. Exit - next loop iteration picks up where you left off

## Important Guidelines

1. **Keep IMPLEMENTATION_PLAN.md updated** - especially handoff notes for incomplete work

2. **Update CLAUDE.md** when you learn new build/test commands (keep it brief and focused)

3. **Document bugs** in IMPLEMENTATION_PLAN.md even if unrelated to current work

4. **Full implementations only** - no placeholders or minimal implementations

5. **Clean up periodically** - when IMPLEMENTATION_PLAN.md gets large, remove completed items using a subagent

6. **Research documents are reusable** - if a research doc exists for a task, don't re-research
