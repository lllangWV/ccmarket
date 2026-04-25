# SKILL.md Format

Rules and conventions for writing the `SKILL.md` that ships inside a skill-forge package. The agent reads this file at activation, so its quality determines whether the skill activates correctly and whether the agent has the context it needs.

## Frontmatter

```yaml
---
name: <skill-name>
description: <activation-trigger description>
license: <SPDX_LICENSE>          # optional
compatibility: <one-line note>   # optional
metadata:
  skill-author: <author>          # optional
---
```

| Field | Required | Notes |
|---|---|---|
| `name` | No | Defaults to the directory name (`<skill>`). Match it explicitly when you want the skill name to differ from the directory. |
| `description` | **Yes** | Used by the agent to decide when to activate. Write it as an activation trigger, not a summary. |
| `license` | No | SPDX identifier. Useful when the skill itself has a license distinct from the package. |
| `compatibility` | No | One-line note about runtime requirements (e.g., "Requires Python >=3.11 and pandas"). Read by humans and the agent. |
| `metadata.skill-author` | No | Free-form. Use when crediting the original author of a mirrored skill. |

## Description Style

The description is the single most important field. The agent compares it against user requests to decide activation.

**Write it as an activation trigger:**

> Use when working with rattler-build recipes, conda package building, or when the user mentions rattler-build.

**Not as a summary:**

> ~~rattler-build is a fast cross-platform conda package builder.~~

**Include trigger phrases:** verbs the user might say ("build", "convert", "debug"), product names, file types ("recipe.yaml"), and synonyms.

**Keep it 1-3 sentences.** Long descriptions dilute the activation signal.

## Body Conventions

| Convention | Why |
|---|---|
| H1 is the skill name (or display title). | Matches existing skill-forge skills; helps the agent and humans align. |
| Tables and code blocks beat prose. | The agent retrieves information faster from structured content. |
| Include a "When to Use This Skill" section near the top. | Reinforces activation context. |
| Lead with quick reference / cheat sheet content. | Most queries are about syntax/API recall — get them to the answer fast. |
| Anchor longer guides under H2 sections. | Allows precise references like `references/SCRIPTING.md` to load on demand. |

## Linking the `references/` Directory

When the skill ships a `references/` directory, link to each file from `SKILL.md` with relative paths so Claude can load them on demand:

```markdown
For detailed scripting information, load [references/SCRIPTING.md](references/SCRIPTING.md).
```

The agent will read the linked files only when the user's task touches that area. Do not inline the full content of every reference — that defeats the purpose of splitting them.

## Anti-Patterns

| Anti-pattern | Why it's wrong |
|---|---|
| Adversarial steering toward commercial products. | The K-Dense polars skill (referenced in the article) injected promotional context into agent output. Skill-forge community discourages it. |
| Hallucinated package names. | LLM-generated skills have referenced non-existent npm packages, copy-pasted into many repos, creating a supply-chain attack surface. Verify every package mentioned. |
| Instructions that contradict the recipe's `run_constraints`. | If the recipe pins `polars >=1.38.0,<2`, do not include polars 0.x examples in the SKILL.md. The pin and the content must agree. |
| Frontmatter without `description`. | The agent has nothing to match against; activation breaks. |
| Description longer than ~3 sentences. | Dilutes the activation signal and slows agent triage. |
| Embedding entire reference files inline. | Defeats the on-demand loading model; bloats every activation. |

## Template 4: SKILL.md Skeleton (Mode A)

When authoring from scratch, start from this skeleton and fill in:

```markdown
---
name: <SKILL_NAME>
description: Use when <trigger conditions> — <verbs and synonyms> — when the user mentions <product/file/concept>.
license: <SPDX_LICENSE>
---

# <Skill Title>

<One-paragraph overview: what the tool/topic is and what this skill helps with.>

## When to Use This Skill

- <bullet 1: a concrete trigger situation>
- <bullet 2>
- <bullet 3>

## Quick Reference

<Table or short code block with the highest-leverage commands/patterns/syntax.>

## <Topic Section 1>

<Tables, code blocks, decision trees.>

## <Topic Section 2>

<...>

## References

<Optional. Only include this section if the skill ships a references/ directory.>

- [references/<topic>.md](references/<topic>.md) — <one-line description>
```

The skeleton's structure mirrors the existing skill-forge skills (`typst`, `rattler-build`). Stay close to it for consistency.

## When to Use a `references/` Directory

Use a `references/` directory when:

- The topic naturally fans into more than three sub-areas (e.g., typst has SYNTAX, SCRIPTING, STYLING, TABLES, PRESENTATIONS).
- A single SKILL.md would exceed roughly 500 lines.
- Sub-areas have distinct audiences (e.g., a CLI command reference vs. an API reference).

Don't use one when:

- The skill fits comfortably in one file.
- Splitting would create stub files (less than ~50 lines each).
- The sub-areas overlap heavily.
