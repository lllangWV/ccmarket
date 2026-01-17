# Environments and Features Reference

## Overview

Pixi manages environments as isolated sets of files in `.pixi/envs` directories, mimicking a global system install while keeping workspaces isolated and easily removable.

## Activation Methods

Three primary ways to activate environments:

1. **`pixi shell`** - Launches a new shell with the environment activated
2. **`pixi shell-hook`** - Outputs activation commands for your current shell
3. **`pixi run`** - Executes commands or tasks in the environment

### Shell-Specific Setup

**Bash/Zsh:**
```bash
eval "$(pixi shell-hook)"
```

**Fish:**
```fish
pixi shell-hook | source
```

Activation sets variables: `PATH`, `CONDA_PREFIX`, `PIXI_PROJECT_NAME`, `PIXI_PROJECT_ROOT`, plus package-specific activation scripts.

### Specifying Environments

```bash
# Default environment
pixi run python
pixi shell

# Specific environment
pixi run -e test pytest
pixi run --environment cuda python
pixi shell -e cuda
```

Interactive selection when task exists in multiple environments:
```
pixi run ambiguous-task
? Select an environment:
❯ default
  test
  dev
```

## Environment Structure

Each environment in `.pixi/envs/<name>/` contains:
- `bin/` - Executable binaries
- `conda-meta/` - Metadata including manifest path, env name, Pixi version, lock file hash
- `etc/`, `include/`, `lib/` - Standard conda directories

## Activation Configuration

```toml
[activation]
scripts = ["setup.sh"]
env = { MY_VAR = "value" }

[activation.env]
PYTHONIOENCODING = "utf-8"
PYTHONNOUSERSITE = "1"

[target.unix.activation]
scripts = ["install/setup.sh", "activation.sh"]

[target.unix.activation.env]
PATH_EXTRA = "$HOME/bin"

[target.win-64.activation]
scripts = ["setup.bat"]

[target.win.activation.env]
PATH_EXTRA = "%USERPROFILE%\\bin"
```

Note: Scripts run via system shell (bash on Unix, cmd on Windows) before environment is active.

## Feature Definition

Features group related configuration that can be combined into environments.

```toml
[feature.cuda]
activation = { scripts = ["cuda_setup.sh"] }
channels = ["nvidia", "conda-forge"]
dependencies = { cuda = "12.0", cudnn = "*" }
platforms = ["linux-64", "win-64"]
system-requirements = { cuda = "12" }

[feature.cuda.pypi-dependencies]
torch = { version = "*", index = "https://download.pytorch.org/whl/cu124" }

[feature.cuda.tasks]
train = "python train.py"

[feature.cuda.target.linux-64.dependencies]
nccl = "*"
```

### Feature fields

All workspace-level fields are available per feature:
- `dependencies`, `pypi-dependencies`
- `pypi-options`
- `activation`
- `tasks`
- `platforms`
- `channels`
- `channel-priority`
- `system-requirements`
- `target.<platform>.*`

## Environment Definition

Environments combine features:

```toml
[environments]
# Simple: just list features
dev = ["test", "lint"]

# Explicit: with options
prod = { features = ["core"], no-default-feature = false }
test = { features = ["test"], solve-group = "default" }
ci = { features = ["test", "lint"], solve-group = "default" }
```

### Environment options

- `features` - List of features to include
- `no-default-feature` - Exclude default feature (default: false)
- `solve-group` - Share dependency versions across environments

## Default Feature

Configuration outside any `[feature.*]` block belongs to the "default" feature:

```toml
# These belong to the default feature
[dependencies]
python = ">=3.11"

[tasks]
start = "python main.py"
```

Use `no-default-feature = true` to exclude it:

```toml
[environments]
lint = { features = ["lint"], no-default-feature = true }
```

## Solve Groups

Environments in the same solve-group share identical dependency versions:

```toml
[environments]
default = { features = [], solve-group = "main" }
test = { features = ["test"], solve-group = "main" }
lint = { features = ["lint"], solve-group = "main" }
```

This ensures test and lint environments have the same base dependencies as default.

### Production + Testing Pattern

Ensures test environment uses identical dependency versions as production:

```toml
[feature.test.dependencies]
pytest = "*"

[environments]
default = { features = ["test"], solve-group = "prod-group" }
prod = { features = [], solve-group = "prod-group" }
```

## Feature Merging Rules

When environments combine multiple features:

| Field | Merge behavior |
|-------|---------------|
| `dependencies` | Union (conflicts error) |
| `pypi-dependencies` | Union (conflicts error) |
| `tasks` | Union (last wins on conflict) |
| `activation` | Union |
| `channels` | Union (ordered by priority) |
| `platforms` | Intersection |
| `system-requirements` | Highest version wins |

## Channel Priority

Channels in features use priority ordering (higher = first):

```toml
channels = ["nvidia", {channel = "pytorch", priority = -1}]
# Results in: ["nvidia", "conda-forge", "pytorch"]
```

## Multi-Python Testing

Testing across Python versions:

```toml
[feature.py39.dependencies]
python = "~=3.9.0"

[feature.py310.dependencies]
python = "~=3.10.0"

[feature.py311.dependencies]
python = "~=3.11.0"

[feature.py312.dependencies]
python = "~=3.12.0"

[feature.test.dependencies]
pytest = "*"

[environments]
py39 = ["py39", "test"]
py310 = ["py310", "test"]
py311 = ["py311", "test"]
py312 = ["py312", "test"]
```

GitHub Actions integration:
```yaml
strategy:
  matrix:
    environment: [py39, py310, py311, py312]
steps:
  - run: pixi run --environment ${{ matrix.environment }} test
```

## Platform-specific Environments

```toml
[feature.macos]
platforms = ["osx-arm64", "osx-64"]

[feature.macos.dependencies]
tensorflow-macos = "*"

[feature.linux]
platforms = ["linux-64"]

[feature.linux.dependencies]
tensorflow = "*"

[environments]
ml-macos = ["macos", "ml-core"]
ml-linux = ["linux", "ml-core"]
```

## Hardware-Specific Configurations (CPU/GPU/MLX)

```toml
[feature.cuda]
platforms = ["win-64", "linux-64"]
system-requirements = { cuda = "12" }

[feature.cuda.dependencies]
pytorch-cuda = "12.1.*"

[feature.cuda.tasks]
train = "python train.py --cuda"

[feature.mlx]
platforms = ["osx-arm64"]

[feature.mlx.dependencies]
mlx = ">=0.16.0"

[feature.mlx.tasks]
train = "python train.py --mlx"

[feature.cpu.dependencies]
pytorch-cpu = "*"

[feature.cpu.tasks]
train = "python train.py --cpu"

[environments]
cuda = ["cuda"]
mlx = ["mlx"]
default = ["cpu"]
```

Run with: `pixi run -e cuda train` or `pixi run -e mlx train`

## Environment Maintenance

**Checking sync status:** Pixi compares the lock file hash against stored metadata. Mismatches trigger automatic environment updates.

**Cleanup:**
```bash
# Remove all environments
rm -rf .pixi/envs

# Selective cleanup
pixi clean
```

## Lock File Structure

Packages in `pixi.lock` include an `environments` field listing which environments include that package:

```yaml
- platform: linux-64
  name: python
  version: 3.9.3
  environments:
    - dev
    - test
    - py39
```

## Package Caching

Pixi maintains a shared cache (customizable via `PIXI_CACHE_DIR`) containing:
- `pkgs/` - Downloaded conda packages
- `repodata/` - Metadata cache
- `uv-cache/` - PyPI wheels and archives
- `http-cache/` - Conda-PyPI mappings
