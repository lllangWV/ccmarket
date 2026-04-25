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
