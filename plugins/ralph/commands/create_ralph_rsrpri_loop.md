---
description: Generate full RS→RP→RI pipeline loop for complete autonomous development
---

# Create Ralph RSRPRI Loop

Generate scripts that run the full Research-Specs-Plan-Implement pipeline continuously.

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
| `plugins/ralph/commands/run_ralph_rs.md` | `${2:-scripts}/RS_LOOP_PROMPT.md` |
| `plugins/ralph/commands/run_ralph_rp.md` | `${2:-scripts}/RP_LOOP_PROMPT.md` |
| `plugins/ralph/commands/run_ralph_ri.md` | `${2:-scripts}/RI_LOOP_PROMPT.md` |

### Step 3: Copy Shell Script

Read `plugins/ralph/scripts/run_rsrpri_loop.sh` and write it to `${2:-scripts}/run_rsrpri_loop.sh`.

If `$1` (model) was provided, replace `opus` in the MODEL default with the provided value.

### Step 4: Create Supporting Directories

```bash
mkdir -p specs
mkdir -p known-issues
```

### Step 5: Make Script Executable

```bash
chmod +x "${2:-scripts}/run_rsrpri_loop.sh"
```

### Step 6: Output Success Message

```
RSRPRI loop created successfully!

Generated:
  - ${2:-scripts}/RS_LOOP_PROMPT.md (Research-to-Specs prompt)
  - ${2:-scripts}/RP_LOOP_PROMPT.md (Research-Plan prompt)
  - ${2:-scripts}/RI_LOOP_PROMPT.md (Research-Implement prompt)
  - ${2:-scripts}/run_rsrpri_loop.sh (combined loop runner)
  - specs/ (specifications directory)
  - known-issues/ (GitHub issues cache)

To start the full pipeline:
  ./scripts/run_rsrpri_loop.sh "your research topic"

Examples:
  ./scripts/run_rsrpri_loop.sh "OAuth 2.0 authentication"
  ./scripts/run_rsrpri_loop.sh "GraphQL API patterns" sonnet

Each iteration runs the full pipeline:
  1. RS: Research external docs → generate/update specs/
  2. RP: Analyze code vs specs → update IMPLEMENTATION_PLAN.md
  3. RI: Implement highest priority task from plan

All phases include 60% context handoff for continuity.

You can also run individual phases:
  ./scripts/run_rs_loop.sh "topic"   # Just RS
  ./scripts/run_rp_loop.sh           # Just RP
  ./scripts/run_ri_loop.sh           # Just RI

Edit the *_PROMPT.md files to customize behavior.
```
