# pixi-skills — Skill for authoring skill-forge conda packages

**Date:** 2026-04-25
**Status:** Design approved, pending implementation
**Owner:** lllangWV

## Summary

A new Claude Code skill, `pixi-skills`, that authors agent skills as conda packages compatible with the [pavelzw/skill-forge](https://github.com/pavelzw/skill-forge) ecosystem and the [pixi-skills](https://github.com/pavelzw/pixi-skills) installer. It generates ready-to-build recipe directories (`recipe.yaml` + `pixi.toml` + `SKILL.md` and optional `references/`, `PROMPT.md`, `fix-skill.patch`) following established skill-forge conventions, supporting three authoring modes: from-scratch, wrap-existing, and mirror-external.

The skill writes files only — it does not run `rattler-build build`, `pixi install`, or publish. Build, validation, and publishing remain explicit user actions documented in the skill's done-state instructions.

## Motivation

Skills as conda packages solve real problems for teams that distribute agent instructions: version pinning to library releases via `run_constraints`, lockfile reproducibility through `pixi.lock`, enterprise-friendly distribution through existing conda channels, and supply-chain security through package review and signing. The skill-forge channel already hosts working examples, and the AGENTS.md in that repo describes the conventions in detail.

Authoring these recipes by hand is error-prone. The frontmatter must follow a specific format, the `${{ skill }}` Jinja convention is easy to miss, the `agentskills validate` test block is consistent across all examples, and the choice between local-source, license-vendoring, and git-mirror recipe variants depends on context. A skill that encodes the conventions and produces correct recipes the first time removes friction and reduces drift across packages.

## Scope

### In scope

- Authoring a complete recipe directory from a topic name (mode A).
- Wrapping an existing local `SKILL.md` (any path) as a recipe (mode B).
- Mirroring a skill from a remote git repo with optional patch (mode C).
- Auto-detecting whether the cwd is a skill-forge-style repo and proposing `recipes/<skill>/` as the output path; falling back to asking when not detected.
- Heuristic version-pinning lookup for `run_constraints` against conda-forge.
- Generating valid skill-forge-compliant `recipe.yaml`, `pixi.toml`, and (for mode A) `SKILL.md`.
- Edge-case handling: overwrite protection, frontmatter validation, branch-to-SHA resolution, license-file path resolution.

### Out of scope

- Running `rattler-build build`, `pixi install`, or any heavy build/test action.
- Editing `pavelzw/skill-forge`'s `autobump.yml` (mentioned in user-facing notes only).
- Publishing or uploading packages to conda channels.
- Supporting non-skill-forge skill formats (Anthropic's official `~/.claude/skills` layout, OpenCode, etc.).
- Slash commands — deliberately deferred. Skill alone is the v1 surface.

## Architecture

### Plugin layout

```
plugins/pixi-skills/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── pixi-skills/
        ├── SKILL.md
        └── references/
            ├── authoring-from-scratch.md
            ├── wrapping-existing.md
            ├── mirroring-external.md
            ├── recipe-templates.md
            ├── skill-md-format.md
            └── version-pinning.md
```

The plugin gets registered in `.claude-plugin/marketplace.json` next to the existing `pixi` plugin, and `README.md` gets a one-line entry.

### `plugin.json`

```json
{
  "name": "pixi-skills",
  "version": "1.0.0",
  "description": "Author skill-forge conda packages for agent skills - recipe.yaml, SKILL.md, version pinning, and skill-forge conventions",
  "author": {
    "name": "lllangWV"
  },
  "repository": "https://github.com/lllangWV/ccmarket/tree/main/plugins/pixi-skills",
  "license": "MIT"
}
```

### `marketplace.json` entry

```json
{
  "name": "pixi-skills",
  "description": "Author skill-forge conda packages for agent skills - recipe.yaml, SKILL.md, version pinning, and skill-forge conventions",
  "version": "1.0.0",
  "source": "./plugins/pixi-skills",
  "category": "development"
}
```

## SKILL.md (entry point)

### Frontmatter

```yaml
---
name: pixi-skills
description: Use when authoring, wrapping, or mirroring agent skills as conda packages for skill-forge or any pixi-skills compatible channel. Triggers on creating a recipe.yaml for an agent skill, packaging an existing SKILL.md as a conda package, mirroring a skill from skills.sh or another repo, run_constraints version pinning for skill-forge, or when the user mentions skill-forge, agent-skill-*, pixi-skills, or "ship a skill as a conda package".
---
```

### Body sections

1. **Overview** — what skill-forge is, what `pixi-skills` consumes (`share/agent-skills/<name>/SKILL.md`), what this skill produces.
2. **Mode triage table** — first thing Claude sees:

   | User says... | Mode | Reference |
   |---|---|---|
   | "create a skill-forge package for X", topic only | A: author from scratch | `references/authoring-from-scratch.md` |
   | Path to an existing `SKILL.md` or "wrap this skill" | B: wrap existing | `references/wrapping-existing.md` |
   | Git URL, "mirror skill from skills.sh", "package the polars skill from k-dense-ai" | C: mirror external | `references/mirroring-external.md` |

3. **Output path resolution algorithm:**

   ```
   1. Check cwd for `recipes/` directory + `pixi.toml` referencing rattler-build
      or pixi-build-rattler-build.
   2. If detected → propose `recipes/<skill>/`, show resolved path, confirm
      before writing.
   3. If not detected → ask user for output path with default suggestion
      `./recipes/<skill>/`.
   4. Refuse to overwrite an existing non-empty directory without explicit
      confirmation.
   ```

4. **Required artifacts checklist** —
   - `recipe.yaml`
   - `pixi.toml` (`[package.build.backend]` for `pixi-build-rattler-build`)
   - `SKILL.md` (or `fix-skill.patch` for mode C with patches)
   - Optional: `references/`, `PROMPT.md`, `fix-skill.patch`

5. **Hand-off pointers** — table linking each downstream concern to its reference file.

6. **Done-state instructions:**
   - Build: `pixi run rattler-build build -r <output-path>` (or `pixi run build-new` if inside skill-forge clone).
   - Validate: `agentskills validate $CONDA_PREFIX/share/agent-skills/<skill>` (after build + install).
   - Publish: out of scope; pavelzw/skill-forge maintainers handle this via CI.

## Reference files

### `references/authoring-from-scratch.md` (mode A)

Procedure:

1. Resolve target conda-forge package name from topic.
2. Look up version (delegate to `version-pinning.md`).
3. Research the tool — homepage, repo, docs URL, license. Cap research scope at what fits in `SKILL.md` + 2-3 reference files.
4. Draft `SKILL.md` per `skill-md-format.md`. Decide single-file vs. `references/`-augmented (heuristic: >3 sub-areas → use `references/`).
5. Generate `recipe.yaml` (local-source variant from `recipe-templates.md`).
6. Generate `pixi.toml` (one-liner).
7. Optional `PROMPT.md` only when the user gave special update/maintenance instructions. Recipe must not copy it into the package.
8. Pre-write summary: show resolved output path, file list, version pin, SKILL.md description. Confirm. Write.

### `references/wrapping-existing.md` (mode B)

Procedure:

1. Read source `SKILL.md`. Extract frontmatter `name`, `description`, `license`.
2. Detect supporting `references/` directory alongside the file.
3. Infer target package from skill name + description. Confirm with user.
4. Look up version.
5. Decide on source field:
   - Vendor → local-source variant; copy SKILL.md (and `references/`) into output.
   - Remote → git-source variant; user supplies repo + rev.
6. Generate `recipe.yaml` + `pixi.toml`.
7. Pre-write summary, confirm, write.

Edge case: if source frontmatter is missing or malformed, prompt user; never silently fix.

### `references/mirroring-external.md` (mode C)

Procedure:

1. Identify the skill within the repo. Verify the path exists (e.g., `scientific-skills/polars/SKILL.md`).
2. Pin to a full commit SHA. Resolve branches/tags via `gh api repos/<owner>/<repo>/commits/<ref> --jq .sha`. Never write a branch name into the recipe.
3. Decide whether a patch is needed. If yes, generate `fix-skill.patch` (unified diff, paths relative to repo root).
4. Generate `recipe.yaml` (git-source variant).
5. Generate `pixi.toml`.
6. Pre-write summary, confirm, write.
7. If user is contributing to pavelzw/skill-forge, remind them about `.github/workflows/autobump.yml` update strategies (`github-latest-release` or `git-main`). Skill does not edit autobump.yml directly.

### `references/recipe-templates.md`

Three templates side-by-side with concrete examples. See "Templates" section below for full content.

### `references/skill-md-format.md`

- Frontmatter — `name` (defaults to dir name), `description` (required, activation-trigger style), optional `license`, `compatibility`, `metadata.skill-author`.
- Description style: written as activation trigger ("Use when..."), not summary.
- Body conventions: H1 is the skill name; tables and code blocks beat prose.
- `references/` linking: relative paths in `SKILL.md` so Claude loads on demand.
- Things to avoid: adversarial steering toward commercial products, hallucinated package names, instructions that contradict the `run_constraints` pin.

### `references/version-pinning.md`

Heuristic for `run_constraints`:

1. Determine target package name from topic. If unclear, ask.
2. Lookup latest version, in order:
   - `pixi search <pkg> --channel conda-forge --limit 1` if pixi is on PATH.
   - `https://conda.anaconda.org/conda-forge/noarch/repodata.json` (or `linux-64`) — extract latest version.
   - Ask user if both fail.
3. Propose constraint: `>=<latest_minor>,<<next_major>` for semver libraries. For 0.x packages where minor is breaking (typst, polars 0.x), narrow to `>=<minor>,<<next_minor>`.
4. Confirm with user. Allow override.
5. Skip when target is non-singular (e.g., `presentation-design`, `gws-cli`). Document the choice in pre-write summary.

Includes a small table of known 0.x-style packages where minor is breaking.

## Templates

Templates 1, 2, and 3 live in `references/recipe-templates.md`. Template 4 (the `SKILL.md` skeleton) lives in `references/skill-md-format.md` since it's tied to the frontmatter and body conventions described there.

### Template 1: Local source (most common)

`recipe.yaml`:

```yaml
context:
  skill: <SKILL_NAME>

package:
  name: agent-skill-${{ skill }}
  version: "0.0.1"

source:
  url: <UPSTREAM_LICENSE_RAW_URL>
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

Conditionals:

- Omit the `source:` block when no upstream license is being vendored.
- Omit `cp -R $RECIPE_DIR/references` and the `references/*.md` test glob when no `references/` directory exists.
- Omit the `requirements.run_constraints` block when no clear pin applies.

Default behavior: include a source URL for the upstream license file when an upstream repo is identifiable, since this is the prevailing skill-forge pattern.

### Template 2: Git mirror (polars pattern)

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

Conditional: omit the `patches:` field when no patch is needed; never write an empty patch.

### Template 3: `pixi.toml` (all modes, identical)

```toml
[package.build.backend]
name = "pixi-build-rattler-build"
version = "*"
```

### Template 4: `SKILL.md` skeleton (mode A only)

```markdown
---
name: <SKILL_NAME>
description: <ACTIVATION-STYLE DESCRIPTION — "Use when ...">
license: <SPDX_LICENSE>
---

# <Skill Title>

<One-paragraph overview.>

## When to Use This Skill

<Bullets describing trigger situations.>

## <Topic-specific sections>

<Tables, code blocks, decision trees.>

## References

<Optional — only when references/ exists.>
```

## `agentskills validate` test

Always include the validate test block with `skills-ref` as a run dep. No conditional logic — the test is cheap and catches frontmatter regressions across all packages.

```yaml
  - script:
      - agentskills validate $CONDA_PREFIX/share/agent-skills/${{ skill }}
    requirements:
      run:
        - skills-ref
```

## Edge cases & failure modes

### Output path conflicts

- Target directory exists and is non-empty → stop, list contents, ask user to confirm overwrite or pick a new path. Never silently clobber.
- Target directory exists and is empty → write into it without asking.
- Target's parent doesn't exist → ask user before creating intermediate directories.

### Frontmatter problems (mode B)

- No frontmatter → offer to generate from first heading + first paragraph; user confirms before proceeding.
- Malformed YAML → stop, report parse error; do not auto-fix.
- Description not in activation-trigger style → flag and offer to rewrite, but defer to user.

### Version-pinning failures

- `pixi search` returns nothing → fall back to repodata.json fetch.
- Repodata fetch fails → ask user manually.
- Package is `0.0.x` → use `>=<full>,<<next-patch>` rather than the standard heuristic.
- No clear single-package anchor → omit `run_constraints`; document in pre-write summary.

### Git mirror specifics (mode C)

- User gives a branch name → resolve to current HEAD SHA via `gh api repos/<owner>/<repo>/commits/<branch> --jq .sha`. Never write a branch name into the recipe.
- User gives a tag → fine; record the resolved SHA.
- Skill subdirectory missing in repo → stop and ask. Don't fabricate a path.
- Patch generation requested but no concrete diffs → skip the `patches:` field; never write an empty patch.

### License questions

- Upstream license file not at root → adjust `license_file:` path. Common cases: `LICENSE.md`, `COPYING`, `LICENSES/MIT.txt`. Confirm with user if non-standard.
- License unclear or proprietary → ask user; don't guess. Skill-forge requires SPDX-compatible.
- Mode C `license_file:` resolves inside the cloned repo, not from `$RECIPE_DIR`.

### `PROMPT.md` behavior

- User-provided maintenance instructions → write to `PROMPT.md` in recipe dir.
- Recipe must never `cp` `PROMPT.md` into the package (per skill-forge AGENTS.md).
- When updating an existing recipe in modes B/C, read existing `PROMPT.md` if present and follow it.

### `references/` directory handling

- Nested directories under `references/` → recursive `cp -R`; the `references/*.md` test glob may need `references/**/*.md`. Document the choice.
- Non-markdown content (images, scripts) → adjust `package_contents.files` patterns; extend the build script.

### Skill name collisions

- Proposed name already exists as a recipe in target's parent → flag, ask whether update (bump version) or rename.
- Names must be conda-package-safe (lowercase, hyphens, no underscores). Sanitize and confirm if topic name doesn't match.

## Success criteria

### Activation correctness

- Skill activates on phrases like "create a skill-forge package for X", "wrap this SKILL.md as a conda package", "mirror the polars skill from k-dense-ai", "package my skill for pixi-skills".
- Skill does not activate for unrelated phrases like "create a skill" (handled by `superpowers:writing-skills`) or "use the pixi skill" (handled by existing `pixi` plugin).

### Mode selection

- Topic only → mode A.
- Path to an existing `SKILL.md` → mode B.
- Git URL or "mirror" → mode C.
- Ambiguous input → skill asks once before proceeding; never picks blindly.

### Output correctness

- Generated `recipe.yaml` parses as valid YAML and matches one of the three templates exactly with no missing required fields.
- Generated `pixi.toml` is the one-line backend declaration — nothing else.
- Generated `SKILL.md` (mode A) has valid frontmatter with `name` and `description` written in activation-trigger style.
- File layout: `<output>/{recipe.yaml, pixi.toml, SKILL.md, [references/, PROMPT.md, fix-skill.patch]}`.

### Build verification (manual, by user)

- `pixi run rattler-build build -r <output-path>` succeeds inside a skill-forge clone or any pixi env with `rattler-build` + `skills-ref`.
- The built `.conda` package, when installed, passes `agentskills validate $CONDA_PREFIX/share/agent-skills/<skill>` (exit 0).

### Edge cases caught

- Re-running into a non-empty target stops cleanly with a clear message.
- Branch-name `rev` in mode C is resolved to a SHA before write.
- `run_constraints` is omitted (not fabricated) for non-tooling skills.
- Source `SKILL.md` with malformed frontmatter halts mode B with a useful error.

### Doesn't go too far

- Skill never runs `rattler-build build`, `pixi install`, or any network mutation on its own.
- Skill never edits `pavelzw/skill-forge`'s `autobump.yml` — only mentions it.
- Skill never publishes the package.

## Open questions

None blocking. Future enhancements deferred to v2:

- Slash command companions (`/pixi-skill-create`, `/pixi-skill-wrap`, `/pixi-skill-mirror`).
- An `--update` mode that bumps versions in existing recipe directories.
- A small Python helper script for `agentskills validate`-style frontmatter checks at authoring time.
