# Multi-Platform Configuration Reference

## Platform Definition

The `workspace.platforms` field specifies which platforms your project supports. When multiple platforms are defined, Pixi determines which dependencies to install for each platform individually.

```toml
[workspace]
platforms = ["win-64", "linux-64", "osx-64", "osx-arm64"]
```

## Supported Platforms

| Platform | Description |
|----------|-------------|
| `win-64` | Windows 64-bit |
| `linux-64` | Linux 64-bit |
| `osx-64` | macOS Intel |
| `osx-arm64` | macOS Apple Silicon |

When installing on an unsupported platform, users receive a warning message.

## Target Specifier

The target specifier syntax allows platform-specific configuration overrides using `[target.PLATFORM]` sections.

### pixi.toml syntax
```toml
[target.win-64.dependencies]
package = "*"
```

### pyproject.toml syntax
```toml
[tool.pixi.target.win-64.dependencies]
package = "*"
```

## Platform-Specific Dependencies

Specify different dependencies per platform:

```toml
[dependencies]
python = ">=3.8"

[target.win-64.dependencies]
msmpi = "*"
python = "3.8"

[target.linux-64.dependencies]
openmpi = "*"

[target.osx-arm64.dependencies]
libomp = "*"
```

This enables:
- Installing packages exclusively on certain platforms
- Using different package versions across platforms
- Platform-specific implementations of the same functionality

### CLI Commands

```bash
# Add dependency for specific platform
pixi add --platform win-64 package-name

# Add host dependency for specific platform
pixi add --host --platform win-64 package-name

# Add build dependency for specific platform
pixi add --build --platform osx-64 package-name

# Add to multiple platforms
pixi add --platform linux-64 --platform osx-64 package-name
```

## Platform-Specific Activation

Handle differences in shell requirements across platforms:

```toml
[activation]
scripts = ["setup.sh", "local_setup.bash"]

[target.win-64.activation]
scripts = ["setup.bat", "local_setup.bat"]

[target.osx-arm64.activation]
scripts = ["setup.sh", "macos_setup.sh"]
```

When targeting a specific platform, only that target's activation scripts execute, overriding the default configuration.

### Platform-Specific Environment Variables

```toml
[activation.env]
COMMON_VAR = "shared"

[target.unix.activation.env]
PATH_SEP = ":"
HOME_VAR = "$HOME"

[target.win-64.activation.env]
PATH_SEP = ";"
HOME_VAR = "%USERPROFILE%"
```

## Platform Groups

Use `unix` and `win` as shorthand for multiple platforms:

```toml
# Applies to linux-64, osx-64, osx-arm64
[target.unix.dependencies]
readline = "*"

# Applies to win-64
[target.win.dependencies]
pyreadline3 = "*"
```

## Platform-Specific Tasks

```toml
[tasks]
build = "make build"

[target.win-64.tasks]
build = "nmake build"

[target.osx-arm64.tasks]
build = "make build ARCH=arm64"
```

## Feature Platform Restrictions

Restrict features to specific platforms:

```toml
[feature.cuda]
platforms = ["linux-64", "win-64"]

[feature.cuda.dependencies]
cuda = "12.0"

[feature.mlx]
platforms = ["osx-arm64"]

[feature.mlx.dependencies]
mlx = "*"
```

## Complete Example

```toml
[workspace]
name = "cross-platform-app"
channels = ["conda-forge"]
platforms = ["win-64", "linux-64", "osx-64", "osx-arm64"]

[dependencies]
python = ">=3.10"
numpy = "*"

# Windows-specific
[target.win-64.dependencies]
pywin32 = "*"

[target.win-64.activation]
scripts = ["scripts/setup.bat"]

# Linux-specific
[target.linux-64.dependencies]
libgomp = "*"

# macOS Intel
[target.osx-64.dependencies]
libomp = "*"

# macOS Apple Silicon
[target.osx-arm64.dependencies]
libomp = "*"

# Unix common (Linux + macOS)
[target.unix.activation]
scripts = ["scripts/setup.sh"]

[target.unix.activation.env]
LD_LIBRARY_PATH = "$CONDA_PREFIX/lib"

[tasks]
start = "python main.py"

[target.win-64.tasks]
start = "python main.py --windows"
```
