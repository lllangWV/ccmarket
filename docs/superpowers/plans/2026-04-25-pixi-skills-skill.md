# pixi-skills Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new Claude Code plugin `pixi-skills` containing one skill that authors skill-forge conda packages (recipe.yaml + pixi.toml + SKILL.md and optional references/, PROMPT.md, fix-skill.patch) for any of three modes: from-scratch, wrap-existing-SKILL.md, or mirror-external-git-repo.

**Architecture:** Static markdown content under `plugins/pixi-skills/skills/pixi-skills/` with a top-level `SKILL.md` for triage and six `references/` files for per-mode procedures and shared resources (templates, frontmatter rules, version-pinning heuristic). The plugin is registered in `.claude-plugin/marketplace.json` and listed in `README.md`. No code is shipped — all logic lives in markdown the agent reads at activation.

**Tech Stack:** Markdown with YAML frontmatter; JSON for plugin/marketplace manifests; bash for verification commands; existing repo conventions (one skill per plugin, `plugin.json` declares `"skills": "./skills/"`).

**Spec:** [docs/superpowers/specs/2026-04-25-pixi-skills-skill-design.md](../specs/2026-04-25-pixi-skills-skill-design.md). When this plan refers to "the spec", that's the file.

---

## File Structure

Files this plan creates:

| Path | Responsibility |
|---|---|
| `plugins/pixi-skills/.claude-plugin/plugin.json` | Plugin manifest (name, version, description, repo, license, skills path). |
| `plugins/pixi-skills/skills/pixi-skills/SKILL.md` | Skill entry point: frontmatter activation contract, mode triage table, output-path detection, hand-off pointers, done-state instructions. |
| `plugins/pixi-skills/skills/pixi-skills/references/authoring-from-scratch.md` | Mode A procedure: topic → research → SKILL.md + recipe.yaml + pixi.toml. |
| `plugins/pixi-skills/skills/pixi-skills/references/wrapping-existing.md` | Mode B procedure: existing SKILL.md path → recipe.yaml + pixi.toml (and optional references/ copy). |
| `plugins/pixi-skills/skills/pixi-skills/references/mirroring-external.md` | Mode C procedure: remote git repo → recipe.yaml with git source + optional fix-skill.patch. |
| `plugins/pixi-skills/skills/pixi-skills/references/recipe-templates.md` | Three concrete recipe.yaml templates (local-source, git-mirror, license-vendoring) plus the shared pixi.toml one-liner. |
| `plugins/pixi-skills/skills/pixi-skills/references/skill-md-format.md` | SKILL.md frontmatter rules, body conventions, reference-linking style, anti-patterns. Owns Template 4 (SKILL.md skeleton). |
| `plugins/pixi-skills/skills/pixi-skills/references/version-pinning.md` | Heuristic + lookup commands for `run_constraints`. |

Files this plan modifies:

| Path | Change |
|---|---|
| `.claude-plugin/marketplace.json` | Append a new plugin entry for `pixi-skills`. |
| `README.md` | Add a one-line entry for `pixi-skills` under the `### Skills` table; bump the `### Skills (N)` count. |

---

## Task 1: Plugin scaffold and manifest

**Files:**
- Create: `plugins/pixi-skills/.claude-plugin/plugin.json`
- Create: `plugins/pixi-skills/skills/pixi-skills/` (empty dir, populated in later tasks)
- Create: `plugins/pixi-skills/skills/pixi-skills/references/` (empty dir, populated in later tasks)

- [ ] **Step 1: Verify the target plugin directory does not exist**

```bash
test ! -e plugins/pixi-skills && echo OK || echo "plugins/pixi-skills already exists - investigate before proceeding"
```

Expected: `OK`

- [ ] **Step 2: Create the directory tree**

```bash
mkdir -p plugins/pixi-skills/.claude-plugin
mkdir -p plugins/pixi-skills/skills/pixi-skills/references
```

- [ ] **Step 3: Write `plugins/pixi-skills/.claude-plugin/plugin.json`**

Content:

```json
{
  "name": "pixi-skills",
  "version": "1.0.0",
  "description": "Author skill-forge conda packages for agent skills - recipe.yaml, SKILL.md, version pinning, and skill-forge conventions",
  "author": {
    "name": "lllangWV"
  },
  "repository": "https://github.com/lllangWV/ccmarket/tree/main/plugins/pixi-skills",
  "license": "MIT",
  "skills": "./skills/"
}
```

- [ ] **Step 4: Verify the JSON parses and has required keys**

```bash
jq -e '.name=="pixi-skills" and .version=="1.0.0" and (.skills|type=="string")' plugins/pixi-skills/.claude-plugin/plugin.json
```

Expected: `true`

- [ ] **Step 5: Commit**

```bash
git add plugins/pixi-skills/.claude-plugin/plugin.json
git commit -m "feat(pixi-skills): add plugin scaffold and manifest"
```

---

## Task 2: Write SKILL.md entry point

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/SKILL.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/SKILL.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
---
name: pixi-skills
description: Use when authoring, wrapping, or mirroring agent skills as conda packages for skill-forge or any pixi-skills compatible channel. Triggers on creating a recipe.yaml for an agent skill, packaging an existing SKILL.md as a conda package, mirroring a skill from skills.sh or another repo, run_constraints version pinning for skill-forge, or when the user mentions skill-forge, agent-skill-*, pixi-skills, or "ship a skill as a conda package".
---

# pixi-skills — Author skill-forge Conda Packages

Skill-forge ships agent skills as conda packages. The `pixi-skills` installer (`pixi skills manage`) reads them from `share/agent-skills/<name>/SKILL.md` inside an installed pixi env and symlinks them into your agent's skills directory. This skill produces the recipe directories that build those packages.

This skill **writes files only**. It does not run `rattler-build build`, `pixi install`, or publish. Build and validation are explicit user actions described in the done-state section.

## Mode Triage

Pick a mode from what the user provides. If their input is ambiguous, ask one clarifying question before proceeding.

| User says... | Mode | Reference |
|---|---|---|
| "create a skill-forge package for X", topic only ("polars", "scikit-learn") | **A: author from scratch** | [references/authoring-from-scratch.md](references/authoring-from-scratch.md) |
| Path to an existing `SKILL.md`, "wrap this skill as a conda package" | **B: wrap existing** | [references/wrapping-existing.md](references/wrapping-existing.md) |
| Git URL, "mirror the polars skill from k-dense-ai", "package this skills.sh entry" | **C: mirror external** | [references/mirroring-external.md](references/mirroring-external.md) |

## Output Path Resolution

Run this algorithm before writing anything:

1. Look in the current working directory for a `recipes/` directory and a `pixi.toml` that mentions `rattler-build` or `pixi-build-rattler-build`.
2. If both are present → propose `recipes/<skill>/` as the output path. Show the resolved absolute path and confirm with the user before writing.
3. If not → ask the user for an output path. Suggest `./recipes/<skill>/` as the default.
4. Refuse to overwrite an existing non-empty target directory. If the directory exists and is non-empty, list its contents and ask the user whether to overwrite, pick a new path, or abort.
5. If the parent of the target does not exist, ask before creating intermediate directories.

Detection command:

```bash
test -d recipes && test -f pixi.toml && grep -qE 'rattler-build|pixi-build-rattler-build' pixi.toml && echo SKILL_FORGE_DETECTED
```

## Required Artifacts

Every recipe directory ends up with at least these files:

- `recipe.yaml` — the rattler-build recipe.
- `pixi.toml` — declares `[package.build.backend]` for `pixi-build-rattler-build`.
- `SKILL.md` (modes A and B) **or** `fix-skill.patch` (mode C, when a patch is needed).

Optional, per mode:

- `references/` directory — when the skill content fans into multiple sub-areas.
- `PROMPT.md` — when the user gives special update/maintenance instructions to remember on future iterations. **Never copy `PROMPT.md` into the package itself.**
- `fix-skill.patch` — only in mode C, only when there are concrete diffs to apply.

## Hand-off to References

| Concern | Reference |
|---|---|
| Recipe variants and the three concrete templates | [references/recipe-templates.md](references/recipe-templates.md) |
| SKILL.md frontmatter rules and body conventions | [references/skill-md-format.md](references/skill-md-format.md) |
| Looking up versions for `run_constraints` | [references/version-pinning.md](references/version-pinning.md) |
| Authoring from scratch (Mode A procedure) | [references/authoring-from-scratch.md](references/authoring-from-scratch.md) |
| Wrapping an existing SKILL.md (Mode B procedure) | [references/wrapping-existing.md](references/wrapping-existing.md) |
| Mirroring an external repo (Mode C procedure) | [references/mirroring-external.md](references/mirroring-external.md) |

## Pre-Write Checklist

Before writing files, confirm with the user:

1. **Mode** — A, B, or C.
2. **Skill name** — must be conda-package-safe: lowercase, hyphens only, no underscores, no spaces. If the topic doesn't match, sanitize and confirm.
3. **Output path** — resolved per the algorithm above; show absolute path.
4. **Version pin** — the proposed `run_constraints` value, or "omitted" with a one-line reason.
5. **File list** — every file that will be created, including any `references/` and `PROMPT.md`.

Only after the user confirms do you write any file.

## Done-State Instructions

After writing files, tell the user exactly what to run next:

```bash
# Build (inside a skill-forge clone or any pixi env with rattler-build + skills-ref):
pixi run rattler-build build -r <output-path>
# Or if inside skill-forge itself, the convenience task:
pixi run build-new

# Validate the built package after install:
agentskills validate $CONDA_PREFIX/share/agent-skills/<skill>
```

Publishing is out of scope for this skill. For pavelzw/skill-forge, maintainers handle publishing through CI; for internal channels, follow your team's existing conda-publish flow.

## Hard Limits

- Do not run `rattler-build build`, `pixi install`, or any network mutation.
- Do not edit `pavelzw/skill-forge`'s `.github/workflows/autobump.yml` — only mention it to the user when relevant (mode C contributions).
- Do not publish or upload packages.
- Do not silently overwrite an existing non-empty target directory.
- Do not write a branch name (e.g. `main`, `master`) into a recipe's `rev:` field — always resolve to a full commit SHA first (mode C).
- Do not fabricate a `run_constraints` for a skill with no clear single-package anchor — omit it.
````

- [ ] **Step 3: Verify the frontmatter parses as YAML**

```bash
python3 -c "
import yaml, sys
content = open('plugins/pixi-skills/skills/pixi-skills/SKILL.md').read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1])
assert fm['name'] == 'pixi-skills', f'name was {fm.get(\"name\")!r}'
assert 'description' in fm and len(fm['description']) > 50, 'description missing or too short'
print('frontmatter OK')
"
```

Expected: `frontmatter OK`

- [ ] **Step 4: Verify all six reference links are present**

```bash
for ref in authoring-from-scratch wrapping-existing mirroring-external recipe-templates skill-md-format version-pinning; do
  grep -q "references/${ref}.md" plugins/pixi-skills/skills/pixi-skills/SKILL.md || { echo "MISSING: $ref"; exit 1; }
done
echo "all reference links present"
```

Expected: `all reference links present`

- [ ] **Step 5: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/SKILL.md
git commit -m "feat(pixi-skills): add SKILL.md entry point"
```

---

## Task 3: Write recipe-templates.md

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/references/recipe-templates.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/references/recipe-templates.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
# Recipe Templates

Three `recipe.yaml` templates plus the shared `pixi.toml`. Pick one based on where the skill source lives:

| Template | When to use |
|---|---|
| **1. Local source** | Skill content lives next to `recipe.yaml` (you authored it or vendored it). Most common. Used by `rattler-build`, `typst`, `sqlalchemy`, `example-skill`. |
| **2. Git mirror** | Skill content lives in a remote repo and is fetched at build time. Used by `polars` (mirroring k-dense-ai). |
| **3. Local source + license URL** | Variant of (1) where the upstream license is fetched separately to populate `license_file`. Used by `rattler-build`, `typst`. |

The shared `pixi.toml` is identical across all three modes.

## Template 1: Local source

```yaml
context:
  skill: <SKILL_NAME>

package:
  name: agent-skill-${{ skill }}
  version: "0.0.1"

build:
  number: 0
  noarch: generic
  script:
    - mkdir -p $PREFIX/share/agent-skills/${{ skill }}
    - cp $RECIPE_DIR/SKILL.md $PREFIX/share/agent-skills/${{ skill }}/SKILL.md
    - cp -R $RECIPE_DIR/references $PREFIX/share/agent-skills/${{ skill }}/

requirements:
  run_constraints:
    - <PKG> >=<MIN>,<<MAX>

tests:
  - package_contents:
      files:
        - share/agent-skills/${{ skill }}/SKILL.md
        - share/agent-skills/${{ skill }}/references/*.md
      strict: true
  - script:
      - agentskills validate $CONDA_PREFIX/share/agent-skills/${{ skill }}
    requirements:
      run:
        - skills-ref

about:
  summary: <ONE_LINE_SUMMARY>
  description: |
    <2-5 LINE DESCRIPTION>
  homepage: <UPSTREAM_HOMEPAGE>
  repository: <UPSTREAM_REPO>
  documentation: <UPSTREAM_DOCS>
  license: <SPDX_LICENSE>
```

**Conditional fields in Template 1:**

| Field | When to omit |
|---|---|
| `cp -R $RECIPE_DIR/references ...` (build script) | No `references/` directory in the skill. |
| `share/agent-skills/${{ skill }}/references/*.md` (test files) | Same — no `references/` directory. |
| `requirements.run_constraints` (entire block) | Skill is not anchored to a single conda-forge package (e.g., `presentation-design`). |
| `about.license_file` | No license file is being vendored (see Template 3 if you want to vendor one). |

## Template 2: Git mirror

```yaml
context:
  skill: <SKILL_NAME>

package:
  name: agent-skill-${{ skill }}
  version: "0.0.1"

source:
  git: <UPSTREAM_GIT_URL>
  rev: <FULL_COMMIT_SHA>
  patches:
    - fix-skill.patch

build:
  number: 0
  noarch: generic
  script:
    - mkdir -p $PREFIX/share/agent-skills/${{ skill }}
    - cp -R <SUBDIR_IN_REPO>/${{ skill }}/* $PREFIX/share/agent-skills/${{ skill }}

requirements:
  run_constraints:
    - <PKG> >=<MIN>,<<MAX>

tests:
  - package_contents:
      files:
        - share/agent-skills/${{ skill }}/SKILL.md
  - script:
      - agentskills validate $CONDA_PREFIX/share/agent-skills/${{ skill }}
    requirements:
      run:
        - skills-ref

about:
  summary: <ONE_LINE_SUMMARY>
  description: |
    <2-5 LINE DESCRIPTION>
  homepage: <UPSTREAM_HOMEPAGE>
  repository: <UPSTREAM_REPO>
  documentation: <UPSTREAM_DOCS>
  license: <SPDX_LICENSE>
  license_file: LICENSE.md
```

**Conditional fields in Template 2:**

| Field | When to omit |
|---|---|
| `source.patches` | No concrete diffs to apply. Never write an empty patch. |
| `requirements.run_constraints` | Same condition as Template 1. |

**Important:**
- `rev:` must be a full commit SHA. Resolve branch/tag names before writing the recipe (see [mirroring-external.md](mirroring-external.md)).
- `<SUBDIR_IN_REPO>` is the directory in the upstream repo that contains the skill (e.g., `scientific-skills` for k-dense-ai/claude-scientific-skills).
- `license_file:` resolves to a path inside the cloned repo, not `$RECIPE_DIR`.

## Template 3: Local source + upstream license URL

Identical to Template 1 except: add a `source:` block that fetches the upstream `LICENSE` file so it can be packaged via `about.license_file`. This is the prevailing skill-forge pattern when the skill targets a public OSS project.

```yaml
context:
  skill: <SKILL_NAME>

package:
  name: agent-skill-${{ skill }}
  version: "0.0.1"

source:
  url: https://raw.githubusercontent.com/<OWNER>/<REPO>/refs/heads/<BRANCH>/LICENSE
  sha256: <SHA256>

build:
  number: 0
  noarch: generic
  script:
    - mkdir -p $PREFIX/share/agent-skills/${{ skill }}
    - cp $RECIPE_DIR/SKILL.md $PREFIX/share/agent-skills/${{ skill }}/SKILL.md
    - cp -R $RECIPE_DIR/references $PREFIX/share/agent-skills/${{ skill }}/

requirements:
  run_constraints:
    - <PKG> >=<MIN>,<<MAX>

tests:
  - package_contents:
      files:
        - share/agent-skills/${{ skill }}/SKILL.md
        - share/agent-skills/${{ skill }}/references/*.md
      strict: true
  - script:
      - agentskills validate $CONDA_PREFIX/share/agent-skills/${{ skill }}
    requirements:
      run:
        - skills-ref

about:
  summary: <ONE_LINE_SUMMARY>
  description: |
    <2-5 LINE DESCRIPTION>
  homepage: <UPSTREAM_HOMEPAGE>
  repository: <UPSTREAM_REPO>
  documentation: <UPSTREAM_DOCS>
  license: <SPDX_LICENSE>
  license_file: LICENSE
```

**Computing the sha256 for the license URL:**

```bash
curl -sL <UPSTREAM_LICENSE_RAW_URL> | sha256sum | cut -d' ' -f1
```

## Shared `pixi.toml`

Identical for all three templates:

```toml
[package.build.backend]
name = "pixi-build-rattler-build"
version = "*"
```

## The `${{ skill }}` Convention

Every recipe uses Jinja interpolation for the skill name:

```yaml
context:
  skill: my-skill
package:
  name: agent-skill-${{ skill }}
```

Never hard-code the skill name inside the recipe body. Use `${{ skill }}` for paths, package names, and test globs. This makes recipes copy-pasteable and keeps name changes to one line.

## The `agentskills validate` Test

Always include this test block. It runs `agentskills validate` (provided by the `skills-ref` package) against the installed prefix to verify the SKILL.md frontmatter is well-formed. The check is cheap and catches regressions across all packages.

```yaml
  - script:
      - agentskills validate $CONDA_PREFIX/share/agent-skills/${{ skill }}
    requirements:
      run:
        - skills-ref
```

No conditional logic — every recipe gets this test regardless of mode.
````

- [ ] **Step 3: Verify the file has all three templates and the shared pixi.toml section**

```bash
f=plugins/pixi-skills/skills/pixi-skills/references/recipe-templates.md
grep -q '^## Template 1: Local source' "$f" && \
grep -q '^## Template 2: Git mirror' "$f" && \
grep -q '^## Template 3: Local source + upstream license URL' "$f" && \
grep -q '^## Shared `pixi.toml`' "$f" && \
grep -q 'pixi-build-rattler-build' "$f" && \
grep -q 'agentskills validate' "$f" && \
echo OK
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/references/recipe-templates.md
git commit -m "feat(pixi-skills): add recipe templates reference"
```

---

## Task 4: Write skill-md-format.md

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/references/skill-md-format.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/references/skill-md-format.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
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
````

- [ ] **Step 3: Verify the file has the required sections**

```bash
f=plugins/pixi-skills/skills/pixi-skills/references/skill-md-format.md
grep -q '^## Frontmatter' "$f" && \
grep -q '^## Description Style' "$f" && \
grep -q '^## Body Conventions' "$f" && \
grep -q '^## Anti-Patterns' "$f" && \
grep -q '^## Template 4: SKILL.md Skeleton' "$f" && \
grep -q '^## When to Use a `references/` Directory' "$f" && \
echo OK
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/references/skill-md-format.md
git commit -m "feat(pixi-skills): add SKILL.md format reference"
```

---

## Task 5: Write version-pinning.md

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/references/version-pinning.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/references/version-pinning.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
# Version Pinning for `run_constraints`

Skill-forge recipes use `requirements.run_constraints` to pin against the targeted library version. This is what makes a skill-forge package valuable — it ensures the skill's API references match the library actually installed in the user's environment.

```yaml
requirements:
  run_constraints:
    - polars >=1.38.0,<2
    - rattler-build >=0.35.0
    - typst >=0.14.2,<0.15
```

## Decision Flow

```
1. Is there a clear single conda-forge package this skill targets?
   - Yes → continue.
   - No → omit run_constraints. Document the reason in the pre-write summary.
2. Look up the latest version of that package on conda-forge.
3. Propose a constraint based on the version's stability tier.
4. Confirm with the user. Allow override.
```

## Step 1: Determine the Target Package Name

Usually inferable from the topic:

| Topic | Conda-forge package |
|---|---|
| polars | `polars` |
| scikit-learn | `scikit-learn` |
| rattler-build | `rattler-build` |
| typst | `typst` |
| pandas | `pandas` |

If the topic doesn't map obviously (e.g., "data engineering best practices"), ask the user explicitly. Don't guess.

If the skill targets multiple packages or is non-tooling (e.g., `presentation-design`, `gws-cli`-style internal tooling without a conda anchor), **omit** `run_constraints`. Skill-forge's own `example-skill` and `gws-cli` recipes have no `run_constraints`.

## Step 2: Look Up the Latest Version

Try these commands in order. Stop at the first that works.

### Option A: `pixi search` (preferred when pixi is on PATH)

```bash
pixi search <pkg> --channel conda-forge --limit 1
```

Output includes the latest version on a line like `Name: <pkg>, Version: 1.38.0, ...`.

### Option B: conda-forge repodata

```bash
curl -sL https://conda.anaconda.org/conda-forge/noarch/repodata.json | \
  jq -r --arg pkg "<pkg>" '
    .packages | to_entries[]
    | select(.value.name == $pkg)
    | .value.version' | sort -V | tail -n1
```

For platform-specific packages, swap `noarch` for `linux-64` (or the relevant arch).

### Option C: Ask the user

If both fail, ask: "What conda-forge version of `<pkg>` should this skill target?"

## Step 3: Propose a Constraint

The constraint format depends on the package's versioning maturity.

| Latest version | Constraint format | Reasoning |
|---|---|---|
| `1.38.0` (stable, semver) | `>=1.38.0,<2` | Minor releases are non-breaking; major bump may break API. |
| `0.35.0` (mature 0.x with stable minor) | `>=0.35.0` | Open upper bound; project signals API stability via no major bump. |
| `0.14.2` (0.x where minor is breaking) | `>=0.14.2,<0.15` | Project bumps minor on breaking changes (typst, polars 0.x). |
| `0.0.7` (very early/unstable) | `>=0.0.7,<0.0.8` | Patch-only window; everything else may break. |

### Common 0.x packages where minor is breaking

| Package | Pattern | Example |
|---|---|---|
| `typst` | `>=<minor>,<<next-minor>` | `>=0.14.2,<0.15` |
| `polars` (pre-1.0) | `>=<minor>,<<next-minor>` | `>=0.20.0,<0.21` |

When in doubt, look at the project's CHANGELOG — does the project bump minor on breaking changes? If yes, treat 0.x minor as breaking.

## Step 4: Confirm with the User

Show the proposal in the pre-write summary:

```
Target package: polars
Latest version on conda-forge: 1.38.0
Proposed run_constraints: polars >=1.38.0,<2
(Reason: stable semver; major bump may break API.)
```

Allow the user to override. Common overrides:

- They want a tighter pin: `polars >=1.38.0,<1.39`.
- They want a looser pin: `polars >=1.0,<2`.
- They want to omit: skill is documentation-only and shouldn't constrain installs.

## Failure Modes

| Failure | Handling |
|---|---|
| `pixi search` not on PATH | Fall through to Option B. |
| Repodata fetch returns 404 | Wrong package name. Ask the user. |
| Repodata fetch returns valid data but no matches | Wrong package name. Ask the user. |
| Network blocked | Ask the user manually. |
| Package version is `0.0.x` | Use the patch-only window (`>=0.0.X,<0.0.<X+1>`). |

## Anti-Patterns

| Anti-pattern | Why |
|---|---|
| Fabricating a `run_constraints` for a skill with no clear anchor. | Misleads the solver and may block valid installs. Omit instead. |
| Pinning to `==<version>` (exact). | Too tight; the skill becomes useless after the next patch release. Always use a range. |
| Open-ended `>=<version>` for unstable 0.x packages. | Lets a breaking minor pull in a skill that no longer matches. Cap the upper bound. |
| Skipping the user confirmation. | The pin is a load-bearing decision; surface it explicitly. |
````

- [ ] **Step 3: Verify the file has the required sections and tables**

```bash
f=plugins/pixi-skills/skills/pixi-skills/references/version-pinning.md
grep -q '^## Decision Flow' "$f" && \
grep -q '^## Step 1: Determine the Target Package Name' "$f" && \
grep -q '^## Step 2: Look Up the Latest Version' "$f" && \
grep -q '^## Step 3: Propose a Constraint' "$f" && \
grep -q '^## Step 4: Confirm with the User' "$f" && \
grep -q '^## Failure Modes' "$f" && \
grep -q 'pixi search' "$f" && \
grep -q 'repodata.json' "$f" && \
echo OK
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/references/version-pinning.md
git commit -m "feat(pixi-skills): add version pinning reference"
```

---

## Task 6: Write authoring-from-scratch.md

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/references/authoring-from-scratch.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/references/authoring-from-scratch.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
# Mode A: Authoring from Scratch

User gave you only a topic ("scikit-learn", "internal data API", "presentation design"). You build everything: SKILL.md, recipe.yaml, pixi.toml, optional references/, optional PROMPT.md.

## Procedure

```
1. Resolve the target conda-forge package name.
2. Look up the latest version (delegate to version-pinning.md).
3. Research the tool — homepage, repo, docs URL, license.
4. Decide single-file vs. references/-augmented SKILL.md.
5. Draft SKILL.md per skill-md-format.md.
6. Generate recipe.yaml from recipe-templates.md (Template 1 or 3).
7. Generate pixi.toml (the shared one-liner).
8. Optionally write PROMPT.md.
9. Pre-write summary + user confirmation.
10. Write all files.
```

## Step 1: Resolve the Target Package Name

The topic usually maps to a conda-forge package. If it doesn't, ask:

> "I want to confirm the conda-forge package this skill targets. For 'scikit-learn', that's the `scikit-learn` package. What's the package for '<topic>'?"

If there's no single anchor (e.g., "presentation-design", "internal API guidelines"), record this and skip `run_constraints` later.

## Step 2: Look Up the Version

Follow [version-pinning.md](version-pinning.md). Capture:

- Latest version on conda-forge.
- Proposed constraint (`>=X,<Y`).
- A one-line justification for the constraint shape.

## Step 3: Research the Tool

Gather authoritative metadata before writing prose:

| Field | Where to get it |
|---|---|
| `summary` (one line) | Project tagline from homepage or repo description. |
| `description` (2-5 lines) | Project's "what it does" paragraph; rewrite to focus on agent-relevant capabilities. |
| `homepage` | Project's official site or repo URL. |
| `repository` | GitHub/GitLab URL. |
| `documentation` | Docs site, often a subdomain or `/docs` page. |
| `license` | SPDX identifier from the repo's LICENSE file. |
| Trigger phrases | Verbs and product names users say (e.g. "build a recipe", "rattler-build", "conda package"). |

**Cap research scope** at what fits in `SKILL.md` plus 2-3 reference files. Don't try to mirror the entire upstream documentation.

## Step 4: Decide Single-File vs. References/

Use `references/` when the topic fans into more than three sub-areas. See [skill-md-format.md](skill-md-format.md) for the full rule. Examples:

| Topic | Layout |
|---|---|
| `sqlalchemy` | Single file (one cohesive ORM). |
| `typst` | `references/` (syntax, scripting, styling, tables, presentations). |
| `rattler-build` | `references/` (new-recipe, build-recipe, debug, create-patch, inspect). |
| `presentation-design` | Single file or `references/` depending on scope. |

## Step 5: Draft SKILL.md

Use Template 4 from [skill-md-format.md](skill-md-format.md). Fill in every placeholder. The frontmatter description is load-bearing — write it in activation-trigger style.

Example frontmatter for a fresh `scikit-learn` skill:

```yaml
---
name: scikit-learn
description: Use when working with scikit-learn estimators, pipelines, model selection, or feature engineering. Triggers on classification, regression, clustering, train_test_split, GridSearchCV, or when the user mentions scikit-learn or sklearn.
license: BSD-3-Clause
---
```

If you create `references/`, populate it with focused files (50-300 lines each). Link each from `SKILL.md`'s "References" section.

## Step 6: Generate `recipe.yaml`

Pick between [recipe-templates.md](recipe-templates.md) Template 1 (no upstream license vendoring) and Template 3 (vendor an upstream LICENSE file).

**Default to Template 3** when the skill targets a public OSS project. The skill-forge convention is to populate `about.license_file` from an upstream raw URL.

Steps:

1. Compute the sha256 of the upstream LICENSE:

   ```bash
   curl -sL https://raw.githubusercontent.com/<OWNER>/<REPO>/refs/heads/<BRANCH>/LICENSE | sha256sum | cut -d' ' -f1
   ```

2. Substitute every placeholder. Especially:
   - `context.skill` → the skill name.
   - `package.version` → start at `"0.0.1"` for new skills.
   - `requirements.run_constraints` → from Step 2 (or omit).
   - `tests.package_contents.files` → include `references/*.md` only when references/ exists.
   - `build.script` → include the `cp -R $RECIPE_DIR/references` line only when references/ exists.

3. Set `about.license_file: LICENSE` if the source URL fetches LICENSE; omit `license_file` if no source block.

## Step 7: Generate `pixi.toml`

Identical for every recipe:

```toml
[package.build.backend]
name = "pixi-build-rattler-build"
version = "*"
```

## Step 8: PROMPT.md (optional)

Write `PROMPT.md` only when the user gave special update or maintenance instructions you should remember on future iterations. Examples:

- "Bump this skill whenever scikit-learn releases a new minor."
- "Re-run the OCR examples on next update; current examples assume MinerU 1.x."

The recipe must **not** copy `PROMPT.md` into the package. Skill-forge's AGENTS.md specifies this.

## Step 9: Pre-Write Summary

Show the user:

```
Mode: A (author from scratch)
Skill name: <skill>
Output path: <absolute path>
Target package: <pkg> (or "no single anchor")
Run constraint: <constraint> (or "omitted - <reason>")
Files to be created:
  - recipe.yaml
  - pixi.toml
  - SKILL.md
  - references/<...>   (only if applicable)
  - PROMPT.md          (only if applicable)

About metadata:
  summary: <summary>
  homepage: <url>
  repository: <url>
  documentation: <url>
  license: <SPDX>
```

Wait for explicit confirmation. If the user wants changes, apply them and re-display.

## Step 10: Write the Files

Use the file-writing tool of your environment. Verify each file exists after writing.

After writing, point the user at the done-state instructions in `SKILL.md` (build, validate).

## Common Pitfalls

| Pitfall | Avoid by |
|---|---|
| Writing prose-heavy SKILL.md instead of tables/code. | Lead with quick-reference content; reserve prose for "When to Use" and overview only. |
| Picking a package version without confirmation. | Always show the proposed pin and wait for ack. |
| Inventing a homepage/docs URL. | Use only URLs you can verify. If unsure, omit the field. |
| Skipping `run_constraints` confirmation. | Even when omitting, document the reason explicitly. |
| Writing the SKILL.md description as a summary. | Use activation-trigger phrasing. |
````

- [ ] **Step 3: Verify the file has the required steps and references**

```bash
f=plugins/pixi-skills/skills/pixi-skills/references/authoring-from-scratch.md
grep -q '^## Procedure' "$f" && \
grep -q '^## Step 1: Resolve the Target Package Name' "$f" && \
grep -q '^## Step 5: Draft SKILL.md' "$f" && \
grep -q '^## Step 6: Generate `recipe.yaml`' "$f" && \
grep -q '^## Step 9: Pre-Write Summary' "$f" && \
grep -q 'recipe-templates.md' "$f" && \
grep -q 'skill-md-format.md' "$f" && \
grep -q 'version-pinning.md' "$f" && \
echo OK
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/references/authoring-from-scratch.md
git commit -m "feat(pixi-skills): add mode A (authoring from scratch) reference"
```

---

## Task 7: Write wrapping-existing.md

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/references/wrapping-existing.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/references/wrapping-existing.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
# Mode B: Wrapping an Existing SKILL.md

User pointed at an existing `SKILL.md` (in this repo's plugins, on disk, or anywhere). You wrap it as a skill-forge recipe by generating `recipe.yaml` and `pixi.toml` and either vendoring the source files into the recipe directory or referencing them via a git source.

## Procedure

```
1. Read the source SKILL.md and validate its frontmatter.
2. Detect a sibling references/ directory.
3. Infer the target conda-forge package; confirm with the user.
4. Look up the latest version (delegate to version-pinning.md).
5. Decide source mode: vendor (local) vs. git-mirror.
6. Generate recipe.yaml from recipe-templates.md.
7. Generate pixi.toml.
8. Copy SKILL.md (and references/) into the output dir if vendoring.
9. Pre-write summary + user confirmation.
10. Write all files.
```

## Step 1: Read and Validate the Source

Read the source `SKILL.md`. Parse its frontmatter:

```bash
python3 -c "
import yaml, sys
content = open('<source-path>').read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1])
print(fm)
"
```

Required fields:

- `name` — used to derive the skill name. If missing, infer from the directory name.
- `description` — used for the recipe's `about.summary` and the new SKILL.md's frontmatter.

Optional but useful: `license`, `metadata.skill-author`.

### Frontmatter Failures

| Failure | Handling |
|---|---|
| File has no `---` fence. | Stop. Tell the user the source SKILL.md has no frontmatter. Offer to generate one from the file's first heading and first paragraph; require user confirmation before proceeding. |
| Frontmatter YAML doesn't parse. | Stop. Report the parse error verbatim. Do not silently fix. |
| Description is missing. | Stop. Ask the user for one in activation-trigger style. |
| Description is a summary, not an activation trigger. | Flag it. Offer to rewrite. Defer to the user — don't force a rewrite. |

## Step 2: Detect Sibling `references/`

Check whether the source SKILL.md has a sibling `references/` directory:

```bash
src_dir=$(dirname "<source-skill-md-path>")
if test -d "$src_dir/references"; then
  echo "references/ detected:"
  ls "$src_dir/references"
fi
```

If yes, the recipe must copy it into the package. The build script needs `cp -R $RECIPE_DIR/references ...` and `package_contents.files` needs the `references/*.md` glob.

If `references/` contains nested directories or non-markdown content, adjust the test glob (`references/**/*.md`) and the copy step accordingly.

## Step 3: Infer the Target Package

Use the source skill's `name` and `description` as hints. Examples:

| Source SKILL.md `name` | Likely conda-forge package |
|---|---|
| `polars` | `polars` |
| `pixi` | `pixi` |
| `data_engineering` | (no single anchor — omit run_constraints) |
| `cadquery-skill` | `cadquery` |

Always confirm with the user before locking it in:

> "Looks like this skill targets the `<pkg>` conda-forge package. Should I use that for `run_constraints`, or omit?"

## Step 4: Look Up the Version

Delegate to [version-pinning.md](version-pinning.md). Output: a proposed `run_constraints` (or "omitted" with a reason).

## Step 5: Decide Source Mode

Two sub-modes within mode B:

### Sub-mode B-vendor

The recipe will copy the source SKILL.md (and references/) into the recipe directory and use Template 1 or 3 from [recipe-templates.md](recipe-templates.md).

**Use this when:**
- The source is in a private repo you don't want to expose.
- The source SKILL.md is something you authored locally and want to ship.
- Reproducibility is more important than freshness.

### Sub-mode B-git

The recipe will pull the source from a remote git repo and use Template 2.

**Use this when:**
- The source already lives in a public git repo and you want updates to come from there.
- You want the package to track upstream content via SHA pinning.

If the user doesn't specify, default to **B-vendor** (it's the simpler path).

## Step 6: Generate `recipe.yaml`

Follow [recipe-templates.md](recipe-templates.md):

- Sub-mode B-vendor → Template 1 (no license fetch) or Template 3 (vendor upstream LICENSE).
- Sub-mode B-git → Template 2.

For sub-mode B-git, you need the user to provide:

- The git URL (`https://github.com/<owner>/<repo>`).
- The subdirectory inside the repo (e.g., `plugins/data/skills/polars`).
- A revision (commit SHA, tag, or branch). If they give a branch/tag, resolve it to a SHA per [mirroring-external.md](mirroring-external.md) Step 2.

## Step 7: Generate `pixi.toml`

```toml
[package.build.backend]
name = "pixi-build-rattler-build"
version = "*"
```

## Step 8: Copy Source Files (Sub-mode B-vendor only)

Copy the source SKILL.md into the output directory:

```bash
cp <source-skill-md-path> <output-dir>/SKILL.md
```

If a sibling references/ exists, copy it recursively:

```bash
cp -R "$(dirname <source-skill-md-path>)/references" <output-dir>/references
```

After copying, re-validate the destination SKILL.md frontmatter to be sure the copy succeeded.

## Step 9: Pre-Write Summary

```
Mode: B-<vendor|git> (wrap existing SKILL.md)
Source: <source-path or git URL + subdir + SHA>
Skill name: <skill>
Output path: <absolute path>
Target package: <pkg> (or "no single anchor")
Run constraint: <constraint> (or "omitted - <reason>")
References dir: <yes/no — count of files>
Files to be created:
  - recipe.yaml
  - pixi.toml
  - SKILL.md   (vendored copy)             [B-vendor only]
  - references/<...>   (vendored copy)     [B-vendor only, if applicable]

About metadata (inferred from source frontmatter):
  summary: <summary>
  license: <SPDX>
```

Confirm. Apply changes. Write.

## Common Pitfalls

| Pitfall | Avoid by |
|---|---|
| Silently fixing malformed frontmatter. | Stop and report. Let the user decide. |
| Forgetting to re-validate the copied SKILL.md. | Run the frontmatter parse check on the destination too. |
| Hardcoding a branch name in `rev:` for sub-mode B-git. | Always resolve to a full SHA. |
| Missing the `references/*.md` test glob when vendoring references/. | Match the build script and the test files exactly. |
| Picking sub-mode B-git when the user hasn't pushed the source yet. | Confirm the source exists at the URL before locking in. |
````

- [ ] **Step 3: Verify the file has the required steps**

```bash
f=plugins/pixi-skills/skills/pixi-skills/references/wrapping-existing.md
grep -q '^## Procedure' "$f" && \
grep -q '^## Step 1: Read and Validate the Source' "$f" && \
grep -q '^### Sub-mode B-vendor' "$f" && \
grep -q '^### Sub-mode B-git' "$f" && \
grep -q '^## Step 9: Pre-Write Summary' "$f" && \
grep -q 'recipe-templates.md' "$f" && \
grep -q 'version-pinning.md' "$f" && \
echo OK
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/references/wrapping-existing.md
git commit -m "feat(pixi-skills): add mode B (wrapping existing) reference"
```

---

## Task 8: Write mirroring-external.md

**Files:**
- Create: `plugins/pixi-skills/skills/pixi-skills/references/mirroring-external.md`

- [ ] **Step 1: Verify the file does not yet exist**

```bash
test ! -e plugins/pixi-skills/skills/pixi-skills/references/mirroring-external.md && echo OK
```

Expected: `OK`

- [ ] **Step 2: Write the file with this exact content**

````markdown
# Mode C: Mirroring an External Repo

User pointed at a remote git repo (e.g., `k-dense-ai/claude-scientific-skills`, `davila7/claude-code-templates`) and wants to mirror a skill that lives in someone else's repo. The recipe pulls source via git with a pinned commit SHA and applies an optional patch.

This is the polars-recipe pattern from skill-forge.

## Procedure

```
1. Identify the skill within the upstream repo.
2. Resolve the rev to a full commit SHA.
3. Decide whether a patch is needed; if so, generate fix-skill.patch.
4. Look up the version (delegate to version-pinning.md).
5. Generate recipe.yaml from Template 2.
6. Generate pixi.toml.
7. Pre-write summary + user confirmation.
8. Write all files.
9. Mention .github/workflows/autobump.yml if contributing to pavelzw/skill-forge.
```

## Step 1: Identify the Skill in the Upstream Repo

User gives:

- Upstream repo URL (e.g., `https://github.com/k-dense-ai/claude-scientific-skills`).
- Skill name and/or path inside the repo (e.g., `polars` lives at `scientific-skills/polars`).

Verify the path exists:

```bash
gh api repos/<owner>/<repo>/contents/<subdir>/<skill> --jq '.[].name'
```

Expect at least `SKILL.md` in the listing. If the path is wrong or doesn't include `SKILL.md`, stop and ask. Don't fabricate a path.

## Step 2: Resolve the rev to a Full Commit SHA

Never write a branch name (`main`, `master`) into the recipe. Always pin to a full SHA.

| Input | Resolution |
|---|---|
| Branch name | `gh api repos/<owner>/<repo>/commits/<branch> --jq .sha` |
| Tag | `gh api repos/<owner>/<repo>/git/refs/tags/<tag> --jq .object.sha` (then dereference if it's an annotated tag) |
| Full SHA | Use as-is. |
| Short SHA | `gh api repos/<owner>/<repo>/commits/<short-sha> --jq .sha` |

Show the resolved SHA to the user before locking it in.

For tags, you may want to record both the tag and the SHA in a comment for human readability — but only the SHA goes into `rev:`.

## Step 3: Decide Whether a Patch is Needed

Common reasons to patch:

- Upstream skill has examples that conflict with the version `run_constraints` will pin.
- Upstream skill has adversarial steering toward commercial products (the K-Dense polars example from the skill-forge article).
- Upstream skill has broken syntax, hallucinated package names, or factual errors.
- License header needs adding.

If you decide to patch:

1. Clone the upstream repo to a temp location.
2. Apply the edits.
3. Generate a unified diff with paths relative to the repo root:

   ```bash
   cd <upstream-clone>
   git diff > fix-skill.patch
   ```

4. Verify the patch applies cleanly:

   ```bash
   git checkout <SHA>
   git apply --check fix-skill.patch
   ```

5. Place `fix-skill.patch` in the recipe output directory.

If you decide **not** to patch, **skip** the `source.patches` field in the recipe. **Never** write an empty patch and never leave a `patches:` field with no entries.

## Step 4: Look Up the Version

Delegate to [version-pinning.md](version-pinning.md). The target package is the library the upstream skill targets (e.g., `polars` for the polars skill).

## Step 5: Generate `recipe.yaml` (Template 2)

Use Template 2 from [recipe-templates.md](recipe-templates.md). Substitutions:

- `context.skill` — the upstream skill name.
- `source.git` — the upstream repo URL.
- `source.rev` — the full commit SHA from Step 2.
- `source.patches` — `[fix-skill.patch]` only when Step 3 produced one.
- `build.script` — replace `<SUBDIR_IN_REPO>/${{ skill }}/*` with the actual subdirectory path. Example: `cp -R scientific-skills/${{ skill }}/* $PREFIX/share/agent-skills/${{ skill }}`.
- `requirements.run_constraints` — from Step 4.
- `about.license_file` — path inside the cloned repo (`LICENSE`, `LICENSE.md`, etc.). Verify it exists upstream.

## Step 6: Generate `pixi.toml`

```toml
[package.build.backend]
name = "pixi-build-rattler-build"
version = "*"
```

## Step 7: Pre-Write Summary

```
Mode: C (mirror external)
Upstream repo: <url>
Upstream subdir: <subdir>/<skill>
Resolved rev: <full SHA>   (was: <user-provided ref>)
Patch: <yes/no>
Skill name: <skill>
Output path: <absolute path>
Target package: <pkg> (or "no single anchor")
Run constraint: <constraint> (or "omitted - <reason>")
Files to be created:
  - recipe.yaml
  - pixi.toml
  - fix-skill.patch   (only if patching)

License:
  about.license: <SPDX>
  about.license_file: <path inside cloned repo>
```

Confirm. Apply changes. Write.

## Step 8: Write the Files

Write `recipe.yaml`, `pixi.toml`, and (if patching) `fix-skill.patch`. Do **not** write a `SKILL.md` — for mode C, the SKILL.md comes from the upstream repo at build time.

## Step 9: autobump.yml (skill-forge contributors only)

If the user is contributing this recipe to `pavelzw/skill-forge`, remind them:

> The skill-forge `AGENTS.md` says to register an update strategy for mirrors in `.github/workflows/autobump.yml`. Two strategies are available:
>
> - **`github-latest-release`** — use when the upstream repo has releases and the latest release is recent.
> - **`git-main`** — use otherwise.
>
> This skill won't edit `autobump.yml` for you. Add the strategy yourself before opening a PR.

For non-skill-forge repos, ignore this.

## License File Resolution

The mode C `license_file:` is a path inside the cloned upstream repo (not `$RECIPE_DIR`). Common cases:

| Upstream layout | `license_file:` value |
|---|---|
| `<repo-root>/LICENSE` | `LICENSE` |
| `<repo-root>/LICENSE.md` | `LICENSE.md` |
| `<repo-root>/COPYING` | `COPYING` |
| `<repo-root>/LICENSES/MIT.txt` | `LICENSES/MIT.txt` |

Verify it exists upstream:

```bash
gh api repos/<owner>/<repo>/contents/<license-path> --jq '.name'
```

If the upstream license file isn't at a standard path, ask the user. If the upstream is closed-source or the license is unclear, stop — skill-forge requires SPDX-compatible licensing.

## Common Pitfalls

| Pitfall | Avoid by |
|---|---|
| Writing a branch name in `rev:`. | Always run `gh api ... --jq .sha` first. |
| Generating an empty patch (`fix-skill.patch` with no diffs). | Skip the `patches:` field if there are no concrete changes. |
| Mistaking `<SUBDIR_IN_REPO>` for `$RECIPE_DIR`. | The git source extracts to a working dir, not `$RECIPE_DIR`. The build script `cp -R` source is relative to the repo root. |
| Forgetting to verify the upstream path exists. | Run the `gh api ... contents/...` check before locking in. |
| Editing `pavelzw/skill-forge`'s autobump.yml. | Mention it; don't write to it. |
````

- [ ] **Step 3: Verify the file has the required steps**

```bash
f=plugins/pixi-skills/skills/pixi-skills/references/mirroring-external.md
grep -q '^## Procedure' "$f" && \
grep -q '^## Step 1: Identify the Skill' "$f" && \
grep -q '^## Step 2: Resolve the rev to a Full Commit SHA' "$f" && \
grep -q '^## Step 3: Decide Whether a Patch is Needed' "$f" && \
grep -q '^## Step 5: Generate `recipe.yaml`' "$f" && \
grep -q '^## Step 9: autobump.yml' "$f" && \
grep -q 'github-latest-release' "$f" && \
grep -q 'git-main' "$f" && \
echo OK
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add plugins/pixi-skills/skills/pixi-skills/references/mirroring-external.md
git commit -m "feat(pixi-skills): add mode C (mirroring external) reference"
```

---

## Task 9: Register the plugin in marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Confirm the plugin is not already registered**

```bash
jq -e '.plugins[] | select(.name=="pixi-skills")' .claude-plugin/marketplace.json && echo "ALREADY REGISTERED" || echo "OK to add"
```

Expected: `OK to add`

- [ ] **Step 2: Look at the existing entries to confirm the structure**

```bash
jq '.plugins | map(select(.name=="pixi" or .name=="rattler"))' .claude-plugin/marketplace.json
```

Expected output: array containing two objects with `name`, `description`, `version`, `source`, `category` keys.

- [ ] **Step 3: Add the new entry using `jq`**

```bash
tmp=$(mktemp)
jq '.plugins += [{
  "name": "pixi-skills",
  "description": "Author skill-forge conda packages for agent skills - recipe.yaml, SKILL.md, version pinning, and skill-forge conventions",
  "version": "1.0.0",
  "source": "./plugins/pixi-skills",
  "category": "development"
}]' .claude-plugin/marketplace.json > "$tmp" && mv "$tmp" .claude-plugin/marketplace.json
```

- [ ] **Step 4: Verify the entry was added correctly**

```bash
jq -e '.plugins[] | select(.name=="pixi-skills") | .source=="./plugins/pixi-skills" and .category=="development" and .version=="1.0.0"' .claude-plugin/marketplace.json
```

Expected: `true`

- [ ] **Step 5: Verify the JSON still parses**

```bash
jq empty .claude-plugin/marketplace.json && echo OK
```

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(marketplace): register pixi-skills plugin"
```

---

## Task 10: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Find the current Skills count and the table location**

```bash
grep -n '^### Skills (' README.md
grep -n '^| `pixi-skill`' README.md
```

Note both line numbers. The current count is `### Skills (25)` per the existing README. The new count after adding `pixi-skills` will be `(26)`.

- [ ] **Step 2: Add a new row to the Skills table**

Insert a new row immediately after the `pixi-skill` row to keep alphabetical-ish grouping. Use the Edit tool with this exact change:

Find:
```
| `pixi-skill` | Package management with Pixi |
```

Replace with:
```
| `pixi-skill` | Package management with Pixi |
| `pixi-skills` | Author skill-forge conda packages for agent skills |
```

- [ ] **Step 3: Bump the count in the section header**

Find:
```
### Skills (25)
```

Replace with:
```
### Skills (26)
```

- [ ] **Step 4: Verify both edits landed**

```bash
grep -q '^### Skills (26)' README.md && \
grep -q '^| `pixi-skills` | Author skill-forge conda packages' README.md && \
echo OK
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: list pixi-skills in README"
```

---

## Task 11: End-to-end verification

**Files:** None (verification only).

- [ ] **Step 1: Verify the full file tree**

```bash
find plugins/pixi-skills -type f | sort
```

Expected output (exactly these 8 files):

```
plugins/pixi-skills/.claude-plugin/plugin.json
plugins/pixi-skills/skills/pixi-skills/SKILL.md
plugins/pixi-skills/skills/pixi-skills/references/authoring-from-scratch.md
plugins/pixi-skills/skills/pixi-skills/references/mirroring-external.md
plugins/pixi-skills/skills/pixi-skills/references/recipe-templates.md
plugins/pixi-skills/skills/pixi-skills/references/skill-md-format.md
plugins/pixi-skills/skills/pixi-skills/references/version-pinning.md
plugins/pixi-skills/skills/pixi-skills/references/wrapping-existing.md
```

- [ ] **Step 2: Verify all SKILL.md / reference files have valid frontmatter or no frontmatter where appropriate**

```bash
python3 - <<'PY'
import yaml, sys
from pathlib import Path

# Only SKILL.md needs frontmatter; reference files are plain markdown.
skill_md = Path("plugins/pixi-skills/skills/pixi-skills/SKILL.md").read_text()
parts = skill_md.split("---", 2)
assert len(parts) >= 3, "SKILL.md missing frontmatter fence"
fm = yaml.safe_load(parts[1])
assert fm["name"] == "pixi-skills"
assert "description" in fm
print("SKILL.md frontmatter OK")

# Verify reference files render as markdown (just check non-empty + start with #)
ref_dir = Path("plugins/pixi-skills/skills/pixi-skills/references")
for f in sorted(ref_dir.glob("*.md")):
    content = f.read_text()
    assert content.strip(), f"{f.name} is empty"
    first_line = content.strip().splitlines()[0]
    assert first_line.startswith("# "), f"{f.name} doesn't start with H1: {first_line!r}"
    print(f"{f.name} OK")
PY
```

Expected: lines for SKILL.md and each reference confirming OK.

- [ ] **Step 3: Verify all internal references resolve**

```bash
python3 - <<'PY'
import re
from pathlib import Path

skill_dir = Path("plugins/pixi-skills/skills/pixi-skills")
md_files = list(skill_dir.rglob("*.md"))
broken = []
for f in md_files:
    text = f.read_text()
    # Find references like (references/foo.md) and (foo.md) inside references/
    for m in re.finditer(r'\]\(([^)]+\.md)\)', text):
        rel = m.group(1)
        target = (f.parent / rel).resolve()
        if not target.exists():
            broken.append(f"{f}: -> {rel}")
if broken:
    print("BROKEN LINKS:")
    for b in broken:
        print(" ", b)
    raise SystemExit(1)
print(f"All {sum(1 for f in md_files for _ in re.finditer(r'\\]\\(([^)]+\\.md)\\)', f.read_text()))} markdown links resolve")
PY
```

Expected: A line saying all links resolve, no broken links.

- [ ] **Step 4: Verify marketplace.json is consistent**

```bash
jq -e '.plugins | map(.name) | contains(["pixi-skills"])' .claude-plugin/marketplace.json && \
jq empty .claude-plugin/marketplace.json && \
echo OK
```

Expected: `true` then `OK`.

- [ ] **Step 5: Verify plugin.json is valid**

```bash
jq -e '.name=="pixi-skills" and .skills=="./skills/" and (.repository|type=="string")' plugins/pixi-skills/.claude-plugin/plugin.json && echo OK
```

Expected: `true` then `OK`.

- [ ] **Step 6: Verify README is updated**

```bash
grep -q '^### Skills (26)' README.md && \
grep -q '^| `pixi-skills` |' README.md && \
echo OK
```

Expected: `OK`

- [ ] **Step 7: Run the existing pre-commit hooks if any are configured**

```bash
test -f .pre-commit-config.yaml && pre-commit run --files \
  plugins/pixi-skills/.claude-plugin/plugin.json \
  plugins/pixi-skills/skills/pixi-skills/SKILL.md \
  plugins/pixi-skills/skills/pixi-skills/references/*.md \
  .claude-plugin/marketplace.json \
  README.md \
  2>&1 || echo "(no pre-commit config or hooks reported issues — review)"
```

Expected: `Passed` for each hook, or a clean message if no hooks are configured.

- [ ] **Step 8: Commit any verification fixes if needed**

If any verification step surfaced an issue (broken link, frontmatter regression, JSON syntax), fix it and create a follow-up commit:

```bash
git add -A
git commit -m "fix(pixi-skills): resolve verification findings"
```

If all verifications passed, no commit is needed.

- [ ] **Step 9: Final state check**

```bash
git log --oneline -n 12
git status
```

Expected:
- The most recent commits are the 10 from this plan (Tasks 1-10) plus any verification fixup.
- `git status` shows a clean working tree on the feature branch.

---

## Self-Review Notes

This plan covers every section of the spec:

| Spec section | Implemented in |
|---|---|
| Plugin layout | Task 1, Task 11 |
| `plugin.json` template | Task 1 |
| `marketplace.json` entry | Task 9 |
| SKILL.md (entry point) | Task 2 |
| `authoring-from-scratch.md` | Task 6 |
| `wrapping-existing.md` | Task 7 |
| `mirroring-external.md` | Task 8 |
| `recipe-templates.md` (3 templates + pixi.toml) | Task 3 |
| `skill-md-format.md` | Task 4 |
| `version-pinning.md` | Task 5 |
| Edge cases & failure modes (overwrite, frontmatter, version-pinning, git mirror, license, PROMPT.md, references/, name collisions) | Distributed across Tasks 2, 4, 5, 6, 7, 8 |
| Success criteria (activation, mode selection, output correctness, build verification, edge cases, hard limits) | Tasks 2, 11; user-driven build verification documented in SKILL.md done-state |

**Type/path consistency check:**

- `plugin.json` declares `"skills": "./skills/"` — matches the directory layout.
- All cross-file references (`SKILL.md` → `references/*.md`, references mutually) are checked by Task 11 Step 3.
- The `${{ skill }}` Jinja convention is consistent across all three templates.
- `agentskills validate` test block is identical across templates and called out as unconditional in `recipe-templates.md`.

**No placeholders remain.** Every step has either:
- An exact command with expected output, or
- An exact code block / file content to write, or
- A specific Edit instruction with the find-string and replace-string.

The plan does not lean on the engineer to "fill in" prose — every file's full contents are specified in their respective tasks.
