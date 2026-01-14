---
description: Generate RP loop scripts for continuous planning and spec analysis
---

# Create Ralph RP Loop

Generate scripts that run the Research-Plan loop continuously.

## Arguments

- `$1` = Model (default: `opus`, options: `sonnet`, `opus`, `haiku`)
- `$2` = Output directory (default: `scripts/`)

## Process

### Step 1: Create Output Directory

```bash
mkdir -p "${2:-scripts}"
```

### Step 2: Copy Prompt File

Read `${CLAUDE_PLUGIN_ROOT}/commands/run_ralph_rp.md` and write it to `${2:-scripts}/RP_LOOP_PROMPT.md`.

This makes the prompt local to the project so it can be customized.

### Step 3: Copy Shell Script

Read `${CLAUDE_PLUGIN_ROOT}/scripts/run_rp_loop.sh` and write it to `${2:-scripts}/run_rp_loop.sh`.

If `$1` (model) was provided, replace `opus` in the MODEL default with the provided value.

### Step 4: Make Script Executable

```bash
chmod +x "${2:-scripts}/run_rp_loop.sh"
```

### Step 5: Output Success Message

```
RP loop created successfully!

Generated:
  - ${2:-scripts}/RP_LOOP_PROMPT.md (editable prompt)
  - ${2:-scripts}/run_rp_loop.sh (loop runner)

Before running:
1. Create specs in specs/README.md or SPEC.md
2. Optionally create initial IMPLEMENTATION_PLAN.md

To start the loop:
  ./scripts/run_rp_loop.sh

To use a different model:
  ./scripts/run_rp_loop.sh sonnet
  ./scripts/run_rp_loop.sh haiku

Each iteration will:
  - Read project specifications
  - Research codebase with parallel subagents
  - Find TODOs, placeholders, and spec gaps
  - Create/update IMPLEMENTATION_PLAN.md
  - Prioritize tasks (P0-P3)
  - Commit and push changes

You can edit RP_LOOP_PROMPT.md to customize the behavior.

Typical workflow:
  1. Run RP loop to generate/update IMPLEMENTATION_PLAN.md
  2. Run RI loop to implement items from the plan
  3. Repeat as needed
```
