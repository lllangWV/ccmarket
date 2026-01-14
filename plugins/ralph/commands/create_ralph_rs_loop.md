---
description: Generate RS loop scripts for continuous research-to-specs generation
---

# Create Ralph RS Loop

Generate scripts that run the Research-to-Specs loop continuously.

## Arguments

- `$1` = Model (default: `opus`, options: `sonnet`, `opus`, `haiku`)
- `$2` = Output directory (default: `scripts/`)

## Process

### Step 1: Create Output Directory

```bash
mkdir -p "${2:-scripts}"
```

### Step 2: Copy Prompt File

Read `${CLAUDE_PLUGIN_ROOT}/commands/run_ralph_rs.md` and write it to `${2:-scripts}/RS_LOOP_PROMPT.md`.

This makes the prompt local to the project so it can be customized.

### Step 3: Copy Shell Script

Read `${CLAUDE_PLUGIN_ROOT}/scripts/run_rs_loop.sh` and write it to `${2:-scripts}/run_rs_loop.sh`.

If `$1` (model) was provided, replace `opus` in the MODEL default with the provided value.

### Step 4: Make Script Executable

```bash
chmod +x "${2:-scripts}/run_rs_loop.sh"
```

### Step 5: Create specs Directory

```bash
mkdir -p specs
```

### Step 6: Output Success Message

```
RS loop created successfully!

Generated:
  - ${2:-scripts}/RS_LOOP_PROMPT.md (editable prompt)
  - ${2:-scripts}/run_rs_loop.sh (loop runner)
  - specs/ (output directory for specifications)

To start the loop:
  ./scripts/run_rs_loop.sh "your research topic"

Examples:
  ./scripts/run_rs_loop.sh "OAuth 2.0 authentication"
  ./scripts/run_rs_loop.sh "GraphQL query patterns" sonnet
  ./scripts/run_rs_loop.sh "Kubernetes pod lifecycle" haiku

Each iteration will:
  - Research the topic using web-search-researcher agents
  - Generate cleanroom black-box specifications
  - Create/update specs/<topic>.md files
  - Maintain specs/README.md as an index
  - Commit and push changes

You can edit RS_LOOP_PROMPT.md to customize the behavior.

Typical workflow (RS → RP → RI):
  1. RS loop: Research external docs → generate specs/
  2. RP loop: Analyze specs vs code → generate IMPLEMENTATION_PLAN.md
  3. RI loop: Implement items from the plan
```
