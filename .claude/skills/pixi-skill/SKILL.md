---
name: pixi
description: Package and environment management with Pixi. Use when working with pixi.toml or pyproject.toml manifests, managing conda/pypi dependencies, creating environments, running tasks, or configuring Pixi workspaces. Triggers include pixi commands, conda package management, environment setup, dependency resolution, and workspace configuration.
---

# Pixi Package Manager

Pixi is a cross-platform package and environment manager supporting conda and PyPI packages.

## Quick Reference

### Initialize a workspace

```bash
pixi init my-project
pixi init --pyproject  # Use pyproject.toml instead
```

### Manage dependencies

```bash
pixi add python numpy pandas          # Add conda packages
pixi add --pypi requests flask        # Add PyPI packages
pixi add pytorch --channel pytorch    # From specific channel
pixi remove <package>                 # Remove a dependency
```

### Run tasks and environments

```bash
pixi run <task>                       # Run a task
pixi run -e <env> <task>              # Run in specific environment
pixi shell                            # Enter environment shell
pixi install                          # Install/update environment
```

### Other common commands

```bash
pixi list                             # List installed packages
pixi update                           # Update lockfile
pixi tree                             # Show dependency tree
pixi info                             # Show system/workspace info
```

## Manifest Structure (pixi.toml)

Minimal workspace:

```toml
[workspace]
channels = ["conda-forge"]
name = "my-project"
platforms = ["linux-64", "osx-arm64", "win-64"]

[dependencies]
python = ">=3.11"

[tasks]
start = "python main.py"
```

### Key Tables

| Table | Purpose |
|-------|---------|
| `[workspace]` | Channels, platforms, name, version |
| `[dependencies]` | Conda package dependencies |
| `[pypi-dependencies]` | PyPI package dependencies |
| `[tasks]` | Runnable commands |
| `[feature.<name>]` | Feature-specific config |
| `[environments]` | Environment definitions |
| `[system-requirements]` | System specs (cuda, libc) |
| `[activation]` | Scripts/env vars on activation |
| `[target.<platform>]` | Platform-specific overrides |

For pyproject.toml, prefix tables with `tool.pixi.` (e.g., `[tool.pixi.workspace]`).

## Dependencies

### Conda packages

```toml
[dependencies]
python = ">=3.11,<3.13"
numpy = "~=1.26"
pytorch = { version = "*", channel = "pytorch" }
```

### PyPI packages

```toml
[pypi-dependencies]
requests = ">=2.28"
flask = { version = "*", extras = ["async"] }
mypackage = { path = "./local-pkg", editable = true }
torch = { version = "*", index = "https://download.pytorch.org/whl/cu124" }
```

See [references/dependencies.md](references/dependencies.md) for version specs, git dependencies, and PyPI options.

## Environments and Features

Features group dependencies for reuse across environments:

```toml
[feature.test.dependencies]
pytest = "*"
pytest-cov = "*"

[feature.dev.dependencies]
ruff = "*"
mypy = "*"

[environments]
default = { features = ["dev"], solve-group = "main" }
test = { features = ["test", "dev"], solve-group = "main" }
prod = { features = [], no-default-feature = false }
```

Use `solve-group` to share dependency versions across environments.

See [references/environments.md](references/environments.md) for advanced patterns.

## Tasks

```toml
[tasks]
# Simple command
hello = "echo Hello"

# With working directory and environment variables
build = { cmd = "npm build", cwd = "frontend", env = { NODE_ENV = "production" } }

# With dependencies (runs after other tasks)
test = { cmd = "pytest", depends-on = ["build"] }

# With inputs/outputs for caching
compile = { cmd = "gcc -o main main.c", inputs = ["main.c"], outputs = ["main"] }
```

Platform-specific tasks:

```toml
[target.win-64.tasks]
greet = "echo Hello Windows"

[target.unix.tasks]
greet = "echo Hello Unix"
```

## System Requirements

For CUDA or specific system libraries:

```toml
[system-requirements]
cuda = "12"
libc = { family = "glibc", version = "2.28" }
```

## Platform Targets

Override configuration per platform:

```toml
[target.osx-arm64.dependencies]
tensorflow-macos = "*"

[target.linux-64.dependencies]
tensorflow = "*"
```

Valid targets: `win-64`, `win-arm64`, `linux-64`, `osx-64`, `osx-arm64`, `unix`, `win`, `linux`, `osx`

## Configuration

Global config location: `~/.pixi/config.toml`

```toml
[shell]
change-ps1 = false

[mirrors]
"https://conda.anaconda.org/conda-forge" = ["https://prefix.dev/conda-forge"]

[pypi-config]
index-url = "https://pypi.org/simple"
keyring-provider = "subprocess"
```

See [references/configuration.md](references/configuration.md) for all options.

## PyTorch Installation

For CUDA support with conda-forge:

```toml
[system-requirements]
cuda = "12.0"

[dependencies]
pytorch-gpu = "*"
cuda-version = "12.6.*"
```

For PyPI with specific CUDA index:

```toml
[pypi-dependencies]
torch = { version = ">=2.5", index = "https://download.pytorch.org/whl/cu124" }
```

See [references/pytorch.md](references/pytorch.md) for CPU/GPU environments and troubleshooting.

## Environment Variables

Pixi sets these variables in activated environments:

- `PIXI_PROJECT_ROOT` - Project root directory
- `PIXI_ENVIRONMENT_NAME` - Current environment name
- `CONDA_PREFIX` - Environment path
- `INIT_CWD` - Directory where `pixi run` was invoked

Priority: `task.env` > `activation.env` > `activation.scripts` > dependency scripts > outside env
