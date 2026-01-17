# VS Code Integration

## Python Extension

The [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) automatically detects pixi environments.

### Automatic detection

When opening a Python file, VS Code typically detects and selects the pixi default environment automatically.

### Manual selection

If automatic detection fails or you need a different environment:

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Run "Python: Select Interpreter"
3. Choose the pixi environment from the list

### Settings

Configure the Python extension to use pixi environments:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.pixi/envs/default/bin/python"
}
```

For a specific environment:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.pixi/envs/dev/bin/python"
}
```

## Direnv Extension

For language-agnostic environment activation, use the [Direnv extension](https://marketplace.visualstudio.com/items?itemName=mkhl.direnv).

### Setup

1. Install direnv on your system
2. Install the VS Code Direnv extension
3. Create `.envrc` in your project root:

```bash
watch_file pixi.lock
eval "$(pixi shell-hook)"
```

4. Allow direnv: `direnv allow`

The terminal and all extensions will now use the pixi environment.

## Dev Containers

Use VS Code Dev Containers for consistent, reproducible environments.

### Directory structure

```
.devcontainer/
├── Dockerfile
└── devcontainer.json
```

### Dockerfile

```dockerfile
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install pixi
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/root/.pixi/bin:$PATH"

# Optional: pre-install project dependencies
WORKDIR /workspace
COPY pixi.toml pixi.lock ./
RUN pixi install
```

### devcontainer.json

```json
{
  "name": "Pixi Dev Container",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "mounts": [
    "source=${localWorkspaceFolderBasename}-pixi,target=${containerWorkspaceFolder}/.pixi,type=volume"
  ],
  "postCreateCommand": "pixi install",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python"
      ]
    }
  }
}
```

**Important:** Mount `.pixi` as a volume (not local storage) to avoid case-sensitivity issues with conda packages on macOS and Windows.

### With authentication

For private channels, pass secrets during build:

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "args": {
      "PREFIX_DEV_TOKEN": "${localEnv:PREFIX_DEV_TOKEN}"
    }
  }
}
```

In Dockerfile:

```dockerfile
ARG PREFIX_DEV_TOKEN
RUN pixi auth login --token $PREFIX_DEV_TOKEN prefix.dev
```

For GitHub Codespaces, configure secrets in repository settings.

## Tasks Integration

Add pixi tasks to VS Code's task runner:

### .vscode/tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "pixi: test",
      "type": "shell",
      "command": "pixi run test",
      "group": "test",
      "problemMatcher": []
    },
    {
      "label": "pixi: build",
      "type": "shell",
      "command": "pixi run build",
      "group": "build",
      "problemMatcher": []
    },
    {
      "label": "pixi: lint",
      "type": "shell",
      "command": "pixi run lint",
      "group": "none",
      "problemMatcher": []
    }
  ]
}
```

Run tasks via Command Palette: "Tasks: Run Task"

## Debugging

### Python debugging

Create a launch configuration using the pixi environment:

### .vscode/launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File (Pixi)",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "python": "${workspaceFolder}/.pixi/envs/default/bin/python"
    },
    {
      "name": "Python: Run Task",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["tests/"],
      "console": "integratedTerminal",
      "python": "${workspaceFolder}/.pixi/envs/default/bin/python"
    }
  ]
}
```

## Recommended Extensions

| Extension | Purpose |
|-----------|---------|
| Python | Python language support, environment detection |
| Pylance | Python language server |
| Direnv | Language-agnostic environment activation |
| Even Better TOML | Syntax highlighting for pixi.toml |
| Remote - Containers | Dev container support |

## Tips

- Reload VS Code window after `pixi install` if the environment isn't detected
- Use `pixi shell` in the integrated terminal for full environment access
- The `.pixi` directory can be added to `.gitignore`
- For monorepos, set `python.defaultInterpreterPath` per workspace folder
