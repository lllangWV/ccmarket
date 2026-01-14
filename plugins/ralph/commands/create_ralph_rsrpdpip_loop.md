---
description: Generate full RS→RP→DetailedPlan→ImplementPlan pipeline loop for autonomous development
---

# Create Ralph RSRPDPIP Loop

Generate scripts that run the full Research-Specs-Plan-DetailedPlan-Implement pipeline continuously.

## Arguments

- `$1` = Model (default: `opus`, options: `sonnet`, `opus`, `haiku`)
- `$2` = Output directory (default: `scripts/`)

## Process

### Step 1: Create Output Directory

```bash
mkdir -p "${2:-scripts}"
```

### Step 2: Copy All Prompt Files

Read and copy each prompt file to the output directory:

| Source | Destination |
|--------|-------------|
| `${CLAUDE_PLUGIN_ROOT}/commands/run_ralph_rs.md` | `${2:-scripts}/RS_LOOP_PROMPT.md` |
| `${CLAUDE_PLUGIN_ROOT}/commands/run_ralph_rp.md` | `${2:-scripts}/RP_LOOP_PROMPT.md` |
| `${CLAUDE_PLUGIN_ROOT}/commands/detailed_plan_auto.md` | `${2:-scripts}/DP_LOOP_PROMPT.md` |
| `${CLAUDE_PLUGIN_ROOT}/commands/implement_plan_auto.md` | `${2:-scripts}/IP_LOOP_PROMPT.md` |

### Step 3: Copy Shell Script

Read `${CLAUDE_PLUGIN_ROOT}/scripts/run_rsrpdpip_loop.sh` and write it to `${2:-scripts}/run_rsrpdpip_loop.sh`.

If `$1` (model) was provided, replace `opus` in the MODEL default with the provided value.

### Step 4: Create Supporting Directories

```bash
mkdir -p specs
mkdir -p known-issues
mkdir -p thoughts/shared/plans
mkdir -p thoughts/shared/research
```

### Step 5: Make Script Executable

```bash
chmod +x "${2:-scripts}/run_rsrpdpip_loop.sh"
```

### Step 6: Output Success Message

```
RSRPDPIP loop created successfully!

Generated:
  - ${2:-scripts}/RS_LOOP_PROMPT.md (Research-to-Specs prompt)
  - ${2:-scripts}/RP_LOOP_PROMPT.md (Research-Plan prompt)
  - ${2:-scripts}/DP_LOOP_PROMPT.md (Detailed Plan - auto select)
  - ${2:-scripts}/IP_LOOP_PROMPT.md (Implement Plan - auto find)
  - ${2:-scripts}/run_rsrpdpip_loop.sh (combined loop runner)
  - specs/ (specifications directory)
  - known-issues/ (GitHub issues cache)
  - thoughts/shared/plans/ (detailed implementation plans)
  - thoughts/shared/research/ (research documents)

To start the full pipeline:
  ./scripts/run_rsrpdpip_loop.sh "your research topic"

Examples:
  ./scripts/run_rsrpdpip_loop.sh "OAuth 2.0 authentication"
  ./scripts/run_rsrpdpip_loop.sh "GraphQL API patterns" sonnet

Each iteration runs the full pipeline:
  1. RS: Research external docs → generate/update specs/
  2. RP: Analyze code vs specs → update IMPLEMENTATION_PLAN.md (prioritized tasks)
  3. DP: Select highest priority task → create detailed plan in thoughts/shared/plans/
  4. IP: Execute the detailed plan → implement the feature

All phases include 60% context handoff for continuity.

Pipeline Flow:
  specs/ ──► IMPLEMENTATION_PLAN.md ──► thoughts/shared/plans/*.md ──► Code Changes
    ▲              ▲                           ▲                          │
    │              │                           │                          │
    RS            RP                          DP                         IP

Edit the *_PROMPT.md files to customize behavior.
```

## Differences from RSRPRI

This pipeline differs from RSRPRI in the planning phase:

| RSRPRI | RSRPDPIP |
|--------|----------|
| RI selects task and implements directly | DP creates detailed plan first |
| Less upfront planning | More thorough planning with phases |
| Faster for simple tasks | Better for complex features |
| Research inline during implementation | Research happens during planning |

Use RSRPDPIP when:
- Tasks are complex with multiple steps
- You want explicit approval points between phases
- Implementation needs careful coordination
- You're working on unfamiliar code

Use RSRPRI when:
- Tasks are straightforward
- Quick iteration is more important
- The codebase is well-understood
