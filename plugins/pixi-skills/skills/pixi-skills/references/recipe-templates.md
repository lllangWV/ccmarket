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
