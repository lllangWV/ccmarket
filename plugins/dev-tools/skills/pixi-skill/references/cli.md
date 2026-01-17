# CLI Reference

## Command Overview

| Command | Purpose |
|---------|---------|
| `add` | Add dependencies to the workspace |
| `auth` | Authenticate with prefix.dev or anaconda.org |
| `build` | Create conda packages from pixi specs |
| `clean` | Remove environments and caches |
| `completion` | Generate shell completion scripts |
| `config` | Manage configuration settings |
| `exec` | Execute commands in temporary environments |
| `global` | Manage globally installed packages |
| `info` | Display system and workspace details |
| `init` | Create a new workspace |
| `install` | Install environments and update lockfile |
| `list` | Show installed packages |
| `lock` | Resolve dependencies without installing |
| `reinstall` | Reset and reinstall environments |
| `remove` | Remove dependencies from workspace |
| `run` | Execute tasks in pixi environments |
| `search` | Search for conda packages |
| `self-update` | Update pixi to latest version |
| `shell` | Launch interactive environment shell |
| `shell-hook` | Output shell activation scripts |
| `task` | Manage workspace tasks |
| `tree` | Show dependency tree |
| `update` | Update dependencies in lockfile |
| `upgrade` | Upgrade dependencies in manifest and lockfile |
| `upload` | Publish packages to channels |
| `workspace` | Configure workspace settings |

## Global Options

```bash
-v, --verbose      # Increase verbosity (-v, -vv, -vvv, -vvvv)
-q, --quiet        # Suppress output
--color <MODE>     # always, never, auto (default: auto)
--no-progress      # Disable progress bars
--manifest-path    # Path to pixi.toml or pyproject.toml
```

## Dependency Management

### pixi add

```bash
pixi add python numpy                    # Add conda packages
pixi add --pypi requests flask           # Add PyPI packages
pixi add pytorch --channel pytorch       # From specific channel
pixi add --feature test pytest           # Add to feature
pixi add -e dev ruff mypy                # Add to environment
pixi add --platform linux-64 pkg         # Platform-specific
pixi add --build cmake                   # Build dependency
pixi add --host openssl                  # Host dependency
```

### pixi remove

```bash
pixi remove numpy                        # Remove conda package
pixi remove --pypi requests              # Remove PyPI package
pixi remove --feature test pytest        # Remove from feature
```

### pixi update

```bash
pixi update                              # Update all packages
pixi update numpy pandas                 # Update specific packages
pixi update --dry-run                    # Preview changes
pixi update --json                       # Output as JSON
```

### pixi upgrade

```bash
pixi upgrade                             # Upgrade all in manifest
pixi upgrade numpy                       # Upgrade specific package
pixi upgrade --exclude pandas            # Exclude packages
pixi upgrade --dry-run                   # Preview changes
```

## Environment Management

### pixi install

```bash
pixi install                             # Install default environment
pixi install -e dev                      # Install specific environment
pixi install --frozen                    # Don't update lockfile
pixi install --locked                    # Require up-to-date lockfile
```

### pixi shell

```bash
pixi shell                               # Enter default environment
pixi shell -e dev                        # Enter specific environment
pixi shell --change-ps1                  # Modify shell prompt
exit                                     # Exit the shell
```

### pixi clean

```bash
pixi clean                               # Remove .pixi directory
pixi clean --cache                       # Clear package cache
pixi clean -e dev                        # Remove specific environment
```

### pixi reinstall

```bash
pixi reinstall                           # Reinstall all environments
pixi reinstall -e dev                    # Reinstall specific environment
```

## Task Management

### pixi run

```bash
pixi run <task>                          # Run a task
pixi run -e dev <task>                   # Run in specific environment
pixi run python script.py                # Run command directly
pixi run --frozen <task>                 # Don't update lockfile
```

### pixi task

```bash
pixi task list                           # List all tasks
pixi task add <name> <command>           # Add a task
pixi task add build "make" --depends-on configure
pixi task add test "pytest" --cwd tests
pixi task add dev "npm start" --env NODE_ENV=development
pixi task remove <name>                  # Remove a task
pixi task alias <name> <tasks...>        # Create task alias
```

## Information Commands

### pixi info

Debug and overview command for your machine and workspace.

```bash
pixi info                                # Show workspace info
pixi info --json                         # Output as JSON
pixi info --extended                     # Detailed system info (includes cache size)
```

**Global information** (always shown):

| Field | Description |
|-------|-------------|
| Platform | Current OS as recognized by pixi |
| Virtual packages | System packages (`__cuda`, `__glibc`, etc.) used in dependency resolution |
| Cache dir | Where pixi stores cached packages |
| Auth storage | Credential storage location |
| Cache size | Cache directory size in MiB (with `--extended`) |

**Workspace information** (when manifest exists):

| Field | Description |
|-------|-------------|
| Manifest file | Path to pixi.toml or pyproject.toml |
| Last updated | Timestamp of last lockfile update |

**Environment information** (per environment):

| Field | Description |
|-------|-------------|
| Features | Enabled features for the environment |
| Channels | Package sources used |
| Dependency count | Number of defined dependencies |
| Dependencies | List of required packages |
| Target platforms | Supported operating systems |
| Tasks | Available tasks in the environment |

### pixi list

```bash
pixi list                                # List installed packages
pixi list -e dev                         # List for environment
pixi list --json                         # Output as JSON
pixi list --explicit                     # Show explicit deps only
pixi list --sort-by name                 # Sort by name/size/kind
```

### pixi tree

```bash
pixi tree                                # Show dependency tree
pixi tree -e dev                         # For specific environment
pixi tree numpy                          # Show tree for package
pixi tree --invert pandas                # Show reverse dependencies
```

### pixi search

```bash
pixi search numpy                        # Search for package
pixi search "py*"                        # Wildcard search
pixi search numpy --channel conda-forge  # Search specific channel
pixi search --limit 10 numpy             # Limit results
```

## Global Package Management

### pixi global

```bash
pixi global install ruff                 # Install globally
pixi global install ruff mypy            # Multiple packages
pixi global install --channel conda-forge bat
pixi global remove ruff                  # Remove global package
pixi global list                         # List global packages
pixi global update                       # Update global packages
pixi global sync                         # Sync with manifest
```

Global packages are installed to `~/.pixi/` and exposed on PATH.

## Project Initialization

### pixi init

```bash
pixi init                                # Init in current directory
pixi init my-project                     # Create new directory
pixi init --pyproject                    # Use pyproject.toml
pixi init --channel pytorch              # Add channel
pixi init --platform linux-64            # Set platforms
pixi init --import environment.yml       # Import from conda env
```

## Temporary Environments

### pixi exec

```bash
pixi exec python                         # Run in temp environment
pixi exec --spec numpy python            # With specific package
pixi exec --spec "python>=3.11" python   # Version constraint
```

Creates isolated temporary environments for one-off commands.

## Authentication

### pixi auth

```bash
pixi auth login prefix.dev               # Login to prefix.dev
pixi auth login anaconda.org             # Login to anaconda.org
pixi auth logout prefix.dev              # Logout
```

## Shell Completion

### pixi completion

```bash
pixi completion --shell bash >> ~/.bashrc
pixi completion --shell zsh >> ~/.zshrc
pixi completion --shell fish >> ~/.config/fish/completions/pixi.fish
pixi completion --shell powershell >> $PROFILE
```

## Configuration

### pixi config

```bash
pixi config list                         # Show all config
pixi config list --json                  # Output as JSON
pixi config set default-channels '["conda-forge"]'
pixi config unset default-channels
pixi config edit                         # Open config in editor
pixi config edit --system                # Edit system config
```

## Self Management

### pixi self-update

```bash
pixi self-update                         # Update to latest
pixi self-update --version 0.30.0        # Specific version
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `PIXI_HOME` | Override default pixi home (~/.pixi) |
| `PIXI_CACHE_DIR` | Override cache directory |
| `PIXI_COLOR` | Control colored output |
| `PIXI_NO_PROGRESS` | Disable progress bars |
| `PIXI_FROZEN` | Equivalent to --frozen flag |
| `PIXI_LOCKED` | Equivalent to --locked flag |
