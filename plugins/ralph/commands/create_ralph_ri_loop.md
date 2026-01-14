---
description: Generate RI loop scripts for continuous autonomous coding
---

# Create Ralph RI Loop

Generate scripts that run the Research-Implement loop continuously.

## Arguments

- `$1` = Model (default: `opus`, options: `sonnet`, `opus`, `haiku`)
- `$2` = Output directory (default: `scripts/`)

## Process

### Step 1: Create Output Directory

```bash
mkdir -p "${2:-scripts}"
```

### Step 2: Copy Prompt File

Read `plugins/ralph/commands/run_ralph_ri.md` and write it to `${2:-scripts}/RI_LOOP_PROMPT.md`.

This makes the prompt local to the project so it can be customized.

### Step 3: Copy Shell Script

Read `plugins/ralph/scripts/run_ri_loop.sh` and write it to `${2:-scripts}/run_ri_loop.sh`.

If `$1` (model) was provided, replace `opus` in the MODEL default with the provided value.

### Step 4: Make Script Executable

```bash
chmod +x "${2:-scripts}/run_ri_loop.sh"
```

### Step 5: Output Success Message

```
RI loop created successfully!

Generated:
  - ${2:-scripts}/RI_LOOP_PROMPT.md (editable prompt)
  - ${2:-scripts}/run_ri_loop.sh (loop runner)

Before running:
1. Ensure CLAUDE.md has your build/test commands
2. Create IMPLEMENTATION_PLAN.md with prioritized tasks

To start the loop:
  ./scripts/run_ri_loop.sh

To use a different model:
  ./scripts/run_ri_loop.sh sonnet
  ./scripts/run_ri_loop.sh haiku

Each iteration will:
  - Sync GitHub issues to known-issues/
  - Select highest priority task from IMPLEMENTATION_PLAN.md
  - Check for prior handoff context (skip research if exists)
  - Run /research_codebase if no prior context
  - Implement the feature using research as guide
  - At 60% context: write handoff notes and exit
  - Run tests, commit, push, and repeat

You can edit RI_LOOP_PROMPT.md to customize the behavior.
```
