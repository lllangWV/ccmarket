# Claude Code Extensions

A comprehensive collection of skills, agents, and slash commands for [Claude Code](https://claude.ai/claude-code).

## Quick Install

Clone this repository and copy the `.claude/` directory to your project or user directory:

```bash
# Project-level (shared with team via git)
cp -r .claude/ /path/to/your/project/.claude/

# User-level (available in all projects)
cp -r .claude/* ~/.claude/
```

## What's Included

### Skills (25)

Skills provide specialized knowledge that Claude applies automatically based on context.

| Skill | Description |
|-------|-------------|
| `aesthetic-tui` | Design beautiful terminal UIs with Rich and Click |
| `algorithmic-art` | Create generative art with p5.js |
| `atomic-agents` | Build agents with the Atomic Agents framework |
| `brand-guidelines` | Apply Anthropic brand colors and typography |
| `cadquery-skill` | Create parametric 3D CAD models |
| `canvas-design` | Create visual art and posters |
| `coding-agent` | Guide for building coding agents from scratch |
| `data_engineering` | Data engineering patterns and tools |
| `deltalake` | Delta Lake data lakehouse operations |
| `doc-coauthoring` | Structured documentation co-authoring workflow |
| `docx` | Word document creation and editing |
| `frontend-design` | Production-grade frontend interfaces |
| `internal-comms` | Internal communications templates |
| `mcp-builder` | Create MCP (Model Context Protocol) servers |
| `mineru` | Parse PDFs with MinerU |
| `pdf` | PDF manipulation and form filling |
| `pixi-skill` | Package management with Pixi |
| `pptx` | PowerPoint presentation creation |
| `skill-creator` | Guide for creating new skills |
| `slack-gif-creator` | Create animated GIFs for Slack |
| `testing-python` | Python testing patterns |
| `theme-factory` | Apply themes to artifacts |
| `webapp-testing` | Test web apps with Playwright |
| `web-artifacts-builder` | Build complex web artifacts |
| `xlsx` | Excel spreadsheet creation and analysis |

### Agents (6)

Custom subagents for specialized tasks.

| Agent | Description |
|-------|-------------|
| `codebase-analyzer` | Analyze implementation details with file:line references |
| `codebase-locator` | Find files and components relevant to a feature |
| `codebase-pattern-finder` | Find similar implementations and patterns |
| `thoughts-analyzer` | Deep dive research on topics |
| `thoughts-locator` | Find relevant documents in thoughts/ directory |
| `web-search-researcher` | Research topics using web search |

### Slash Commands (29)

Reusable prompts invoked with `/command-name`.

| Command | Description |
|---------|-------------|
| `/commit` | Create git commits with user approval |
| `/ci_commit` | Create commits for CI with clear messages |
| `/create_plan` | Create detailed implementation plans |
| `/create_plan_nt` | Create plans (no thoughts directory) |
| `/create_plan_generic` | Generic implementation planning |
| `/iterate_plan` | Iterate on existing plans |
| `/iterate_plan_nt` | Iterate plans (no thoughts directory) |
| `/implement_plan` | Implement plans from thoughts/shared/plans |
| `/validate_plan` | Validate implementation against plan |
| `/describe_pr` | Generate PR descriptions |
| `/describe_pr_nt` | Generate PR descriptions (no thoughts) |
| `/ci_describe_pr` | Generate PR descriptions for CI |
| `/research_codebase` | Document codebase with thoughts |
| `/research_codebase_nt` | Document codebase without evaluation |
| `/research_codebase_generic` | Research using parallel sub-agents |
| `/debug` | Debug issues via logs, DB, git history |
| `/linear` | Manage Linear tickets |
| `/ralph_plan` | Plan highest priority Linear ticket |
| `/ralph_impl` | Implement highest priority ticket |
| `/ralph_research` | Research Linear ticket |
| `/oneshot` | Research ticket and launch planning |
| `/oneshot_plan` | Execute ralph plan and implementation |
| `/create_handoff` | Create handoff document |
| `/resume_handoff` | Resume work from handoff document |
| `/create_worktree` | Set up git worktree |
| `/local_review` | Set up worktree for PR review |
| `/founder_mode` | Create Linear ticket and PR for experiments |

### Scripts

Utility scripts in `.claude/scripts/`:

- **hack/** - General utilities (worktree management, port utils, visualization)
- **ralph/** - Automation prompts and loops

## Directory Structure

```
.claude/
├── agents/           # Custom subagents
├── commands/         # Slash commands
├── scripts/          # Utility scripts
│   ├── hack/         # General utilities
│   └── ralph/        # Automation scripts
├── skills/           # Specialized skills
│   ├── docx/
│   ├── pdf/
│   ├── pptx/
│   └── ... (25 total)
└── settings.json     # Configuration
```

## Configuration

The included `settings.json` provides:

```json
{
  "permissions": {
    "allow": [
      "Bash(./.claude/scripts/spec_metadata.sh)"
    ]
  },
  "enableAllProjectMcpServers": false,
  "env": {
    "MAX_THINKING_TOKENS": "32000"
  }
}
```

## Usage

Once installed, skills activate automatically based on context. Use slash commands explicitly:

```bash
# Create a plan for a feature
/create_plan

# Commit changes with approval
/commit

# Research the codebase
/research_codebase

# Debug an issue
/debug
```

## Customization

### Adding Your Own Skills

Create a new directory in `.claude/skills/your-skill/` with a `SKILL.md`:

```markdown
---
name: your-skill
description: When Claude should use this skill
---

# Your Skill

Instructions for Claude...
```

### Adding Slash Commands

Create a new file in `.claude/commands/your-command.md`:

```markdown
---
description: What this command does
---

Prompt for Claude to execute...
```

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Some skills have additional dependencies (e.g., Playwright for webapp-testing)

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](.github/CONTRIBUTING.md) for guidelines.
