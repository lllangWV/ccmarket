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
pixi global install <pkg>             # Install package globally
pixi exec --spec <pkg> <cmd>          # Run in temporary environment
pixi search <query>                   # Search for packages
```

See [references/cli.md](references/cli.md) for complete CLI documentation including all subcommands and options.

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

## Channel Priority

Channels are searched in order. The solver stops at the first channel containing the package:

```toml
[workspace]
channels = ["conda-forge", "pytorch", "nvidia"]  # conda-forge has highest priority
```

If a package exists in `conda-forge`, the solver won't look in `pytorch` or `nvidia` for it.

### Channel-specific dependencies

Pin a package to a specific channel (excludes all other channels for that package):

```toml
[dependencies]
pytorch = { version = "*", channel = "pytorch" }
cudnn = { version = "*", channel = "nvidia" }
```

### Explicit priority control

Override position-based priority with the `priority` key (higher = more priority):

```toml
[workspace]
channels = ["conda-forge", { channel = "nvidia", priority = 10 }]
```

### Multi-channel example (PyTorch + CUDA)

List from most-specific to most-general:

```toml
[workspace]
channels = ["nvidia/label/cuda-12.1.0", "pytorch", "conda-forge"]

[dependencies]
python = ">=3.11"
pytorch = { version = "*", channel = "pytorch" }
cuda-toolkit = { version = "12.1.*", channel = "nvidia/label/cuda-12.1.0" }
```

Use `pixi info` to verify the resulting channel order.

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

### Parameterized Tasks

Design reusable tasks with arguments like functions:

```toml
[tasks.test]
args = [{ arg = "subset", default = "all" }, { arg = "report", default = "junit.xml" }]
cmd = "pytest {{ subset }} --junit-xml {{ report }}"

[tasks.greet]
args = ["name"]
cmd = "echo Hello, {{ name }}!"
```

```bash
pixi run test                    # Uses defaults
pixi run test unit               # Override subset
pixi run greet World             # Required argument
```

### Task Aliases

Create shortcuts with pre-filled arguments:

```toml
[tasks]
lint-fast = [{ task = "lint", args = ["--fix"] }]
ci = { depends-on = [
  { task = "test", environment = "py311" },
  { task = "test", environment = "py312" }
]}
```

Platform-specific tasks:

```toml
[target.win-64.tasks]
greet = "echo Hello Windows"

[target.unix.tasks]
greet = "echo Hello Unix"
```

See [references/tasks.md](references/tasks.md) for MiniJinja templating, caching, deno_task_shell features, and advanced patterns.

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

## Shebang Scripts

Run standalone scripts with pixi-managed dependencies (Unix/macOS only):

```python
#!/usr/bin/env -S pixi exec --spec python --spec requests -- python
import requests
print(requests.get("https://api.github.com").status_code)
```

```bash
chmod +x script.py
./script.py
```

See [references/shebang.md](references/shebang.md) for more examples and language support.

## GitHub Actions

Use `prefix-dev/setup-pixi` for CI integration:

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    cache: true
- run: pixi run test
```

Multi-environment matrix:

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        environment: [py310, py311, py312]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: prefix-dev/setup-pixi@v0.9.2
        with:
          environments: ${{ matrix.environment }}
          cache: true
      - run: pixi run -e ${{ matrix.environment }} test
```

See [references/github-actions.md](references/github-actions.md) for authentication, caching strategies, and complete examples.

## VS Code Integration

The Python extension automatically detects pixi environments. Manual selection:

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run "Python: Select Interpreter"
3. Choose the pixi environment

For language-agnostic activation, use the Direnv extension with:

```bash
# .envrc
watch_file pixi.lock
eval "$(pixi shell-hook)"
```

See [references/vscode.md](references/vscode.md) for Dev Containers, tasks, debugging, and recommended extensions.

## Authentication

Authenticate with private channels:

```bash
# prefix.dev (Bearer token)
pixi auth login prefix.dev --token <TOKEN>

# anaconda.org (Conda token)
pixi auth login conda.anaconda.org --conda-token <TOKEN>

# Self-hosted (Basic auth)
pixi auth login my-server.example.com --username <USER> --password <PASS>
```

Credentials are stored securely in the system keychain (Windows Credentials Manager, macOS Keychain, or Linux GNOME Keyring).

See [references/authentication.md](references/authentication.md) for PyPI auth, CI/CD setup, and credential management.

## Docker

Official images available at `ghcr.io/prefix-dev/pixi`:

```dockerfile
FROM ghcr.io/prefix-dev/pixi:latest
WORKDIR /app
COPY pixi.toml pixi.lock ./
RUN pixi install --locked
COPY . .
CMD ["pixi", "run", "start"]
```

For optimized production images, use multi-stage builds with `pixi shell-hook` to activate environments without pixi in the final image.

See [references/docker.md](references/docker.md) for multi-stage builds, CUDA images, private channels, and Docker Compose.

## Pixi Pack

Distribute environments as portable archives (no pixi/conda needed on target):

```bash
# Install
pixi global install pixi-pack

# Pack an environment
pixi-pack pack --environment prod --platform linux-64

# On target machine
pixi-unpack environment.tar
source activate.sh
```

See [references/pixi-pack.md](references/pixi-pack.md) for cross-platform packing, self-extracting executables, and CI/CD usage.

## S3 Channels

Use S3-compatible storage as package channels:

```toml
[workspace]
channels = ["s3://my-bucket/my-channel", "conda-forge"]

[workspace.s3-options.my-bucket]
endpoint-url = "https://s3.us-east-1.amazonaws.com"
region = "us-east-1"
```

Authenticate with AWS credentials or `pixi auth login s3://my-bucket --s3-access-key-id <KEY> --s3-secret-access-key <SECRET>`.

See [references/s3.md](references/s3.md) for S3-compatible providers (MinIO, R2, Wasabi), uploading packages, and bucket setup.

## Building Packages

Pixi can build conda packages from source code using the `pixi-build` preview feature.

### Enable Build Feature

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]
preview = ["pixi-build"]
```

### Package Definition

```toml
[package]
name = "my-package"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }

[package.host-dependencies]
hatchling = "*"

[package.run-dependencies]
numpy = ">=1.20"
```

### Build Commands

```bash
pixi build                    # Create .conda package
pixi install                  # Auto-builds path/git dependencies
```

### Available Build Backends

| Backend | Use Case |
|---------|----------|
| `pixi-build-python` | Python packages (PEP 517) |
| `pixi-build-cmake` | C++ packages |
| `pixi-build-ros` | ROS/ROS2 packages |
| `pixi-build-rust` | Rust packages |
| `pixi-build-rattler-build` | Full control with recipes |

### Path Dependencies (Workspaces)

Build local packages as dependencies:

```toml
[dependencies]
my-lib = { path = "./packages/my-lib" }
```

### Development Mode

Install dependencies without building the package:

```toml
[dev]
my-package = { path = "." }
```

See [references/build.md](references/build.md) for Python/C++/ROS building, workspaces, variants, dependency types, and advanced configuration.
