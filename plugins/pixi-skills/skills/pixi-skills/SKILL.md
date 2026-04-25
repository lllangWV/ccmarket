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
