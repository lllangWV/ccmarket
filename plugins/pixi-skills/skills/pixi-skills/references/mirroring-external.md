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
