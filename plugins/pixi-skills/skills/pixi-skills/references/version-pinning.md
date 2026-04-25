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
