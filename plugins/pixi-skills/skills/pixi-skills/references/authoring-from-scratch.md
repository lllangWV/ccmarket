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
