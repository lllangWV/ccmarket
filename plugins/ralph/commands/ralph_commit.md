---
description: Create git commits automatically without user approval (for autonomous loops)
---

# Ralph Commit

Automatically create git commits without asking for user confirmation. Designed for autonomous ralph loops.

## Process:

1. **Analyze changes:**
   - Run `git status` to see current changes
   - Run `git diff --stat` to understand the scope
   - Determine if changes should be one commit or multiple logical commits

2. **Execute immediately:**
   - Stage files with `git add` (use specific files or `-A` for all changes)
   - Create commit with a clear, descriptive message
   - Use imperative mood ("Add feature" not "Added feature")
   - Focus on what was accomplished

3. **Confirm success:**
   - Run `git log --oneline -1` to show the created commit

## Commit Message Format:

For single-purpose changes:
```
<type>: <description>

<optional body with details>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `wip`

For work-in-progress (context limit handoffs):
```
WIP: <what was being worked on>

- Progress made
- What remains
```

## Important:

- **NO user confirmation required** - just do it
- **NEVER add co-author information or Claude attribution**
- Commits should appear as if the user wrote them
- Do not include "Generated with Claude" or "Co-Authored-By" lines
- Keep commits atomic when practical, but don't over-split

## Example:

```bash
git add -A
git commit -m "feat: add OAuth 2.0 authentication flow

- Implement token refresh logic
- Add secure token storage
- Handle expiration gracefully"
git log --oneline -1
```
