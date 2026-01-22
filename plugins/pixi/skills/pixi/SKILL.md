---
name: pixi
description: Use when working with pixi.toml or pyproject.toml manifests, adding conda or PyPI dependencies, configuring environments, defining tasks, or troubleshooting dependency resolution. Also use for CUDA/PyTorch setup, channel priority issues, or cross-platform builds.
---

# Pixi Package Manager

Cross-platform package and environment manager supporting conda and PyPI packages.

## When to Use

- Setting up a new project with `pixi init`
- Adding/removing conda or PyPI dependencies
- Defining runnable tasks
- Configuring multiple environments (dev, test, prod)
- Setting up CUDA/GPU dependencies
- Troubleshooting channel priority or dependency conflicts

## Quick Reference

| Action | Command |
|--------|---------|
| Initialize | `pixi init` or `pixi init --pyproject` |
| Add conda | `pixi add python numpy` |
| Add PyPI | `pixi add --pypi requests` |
| Add from channel | `pixi add pytorch --channel pytorch` |
| Run task | `pixi run <task>` |
| Enter shell | `pixi shell` |
| Install/update | `pixi install` |
| Show info | `pixi info` |

Run `pixi --help` or `pixi <cmd> --help` for details. See [references/cli.md](references/cli.md) for complete CLI reference.

## Manifest (pixi.toml)

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

For `pyproject.toml`, prefix with `tool.pixi.` (e.g., `[tool.pixi.workspace]`).

| Table | Purpose |
|-------|---------|
| `[workspace]` | Channels, platforms, name |
| `[dependencies]` | Conda packages |
| `[pypi-dependencies]` | PyPI packages |
| `[tasks]` | Runnable commands |
| `[feature.<name>]` | Feature-specific config |
| `[environments]` | Environment definitions |
| `[system-requirements]` | CUDA, libc specs |
| `[target.<platform>]` | Platform overrides |

## Channel Priority

Channels searched in order; first match wins:

```toml
channels = ["conda-forge", "pytorch", "nvidia"]
```

Pin package to channel: `pytorch = { version = "*", channel = "pytorch" }`

See [references/dependencies.md](references/dependencies.md) for version specs and PyPI options.

## Environments

```toml
[feature.test.dependencies]
pytest = "*"

[environments]
default = { features = ["dev"], solve-group = "main" }
test = { features = ["test", "dev"], solve-group = "main" }
```

Use `solve-group` to share versions across environments. See [references/environments.md](references/environments.md).

## Tasks

```toml
[tasks]
hello = "echo Hello"
build = { cmd = "npm build", cwd = "frontend" }
test = { cmd = "pytest", depends-on = ["build"] }
```

Parameterized: `cmd = "pytest {{ subset }}"` with `args = ["subset"]`. See [references/tasks.md](references/tasks.md).

## Common Scenarios

**CUDA/PyTorch:**
```toml
[system-requirements]
cuda = "12.0"

[dependencies]
pytorch-gpu = "*"
```
See [references/pytorch.md](references/pytorch.md).

**CI/CD:** Use `prefix-dev/setup-pixi@v0.9.2`. See [references/github-actions.md](references/github-actions.md).

**Docker:** Use `ghcr.io/prefix-dev/pixi`. See [references/docker.md](references/docker.md).

**Building packages:** Enable `preview = ["pixi-build"]`. See [references/build.md](references/build.md).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrong package from wrong channel | Pin channel: `{ version = "*", channel = "pytorch" }` |
| Environments have conflicting versions | Use `solve-group` to sync |
| PyPI package not found | Use `--pypi` flag or `[pypi-dependencies]` |
| CUDA not detected | Add `[system-requirements] cuda = "12"` |

## Reference Files

- [cli.md](references/cli.md) - All commands and options
- [dependencies.md](references/dependencies.md) - Version specs, git deps
- [environments.md](references/environments.md) - Features, solve-groups
- [tasks.md](references/tasks.md) - Parameterized tasks, caching
- [configuration.md](references/configuration.md) - Global config
- [authentication.md](references/authentication.md) - Private channels
- [pytorch.md](references/pytorch.md) - GPU setup
- [docker.md](references/docker.md) - Container builds
- [github-actions.md](references/github-actions.md) - CI setup
- [build.md](references/build.md) - Package building
- [pixi-pack.md](references/pixi-pack.md) - Portable archives
- [s3.md](references/s3.md) - S3 channels
- [vscode.md](references/vscode.md) - Editor integration
