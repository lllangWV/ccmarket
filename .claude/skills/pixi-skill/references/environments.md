# Environments and Features Reference

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

## Solve Groups

Environments in the same solve-group share identical dependency versions:

```toml
[environments]
default = { features = [], solve-group = "main" }
test = { features = ["test"], solve-group = "main" }
lint = { features = ["lint"], solve-group = "main" }
```

This ensures test and lint environments have the same base dependencies as default.

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
minimal = { features = ["core"], no-default-feature = true }
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

## CPU/GPU Pattern

```toml
[feature.gpu.system-requirements]
cuda = "12"

[feature.gpu.dependencies]
pytorch-gpu = "*"

[feature.cpu.dependencies]
pytorch-cpu = "*"

[environments]
default = ["gpu"]
cpu = ["cpu"]
```

Run with: `pixi run -e cpu python script.py`

## Activation

```toml
[activation]
scripts = ["setup.sh"]  # Run on activation
env = { MY_VAR = "value" }

[target.win-64.activation]
scripts = ["setup.bat"]

[target.unix.activation.env]
PATH_EXTRA = "$HOME/bin"

[target.win.activation.env]
PATH_EXTRA = "%USERPROFILE%\\bin"
```

Note: Scripts run via system shell (bash on Unix, cmd on Windows) before environment is active.
