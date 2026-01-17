# Dependencies Reference

## Conda Version Specs

```toml
[dependencies]
package = "==1.2.3"        # Exact version
package = "~=1.2.3"        # Compatible release (>=1.2.3, <1.3.0)
package = ">1.2,<=1.4"     # Range
package = ">=1.2.3|<1.0"   # Multiple constraints (OR)
package = "*"              # Any version
```

### Version Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Exact match | `==3.11.0` |
| `!=` | Not equal | `!=3.8` |
| `<` | Less than | `<3.12` |
| `<=` | Less than or equal | `<=3.11` |
| `>` | Greater than | `>3.9` |
| `>=` | Greater than or equal | `>=3.9` |
| `~=` | Compatible release | `~=3.11.0` (≥3.11.0, <3.12.0) |
| `*` | Wildcard | `3.11.*` |
| `,` | AND | `">=3.9,<3.12"` |
| \| | OR | `"3.10\|3.11"` |

### MatchSpec Syntax

```toml
package = { version = ">=1.0", channel = "conda-forge" }
package = { version = ">=1.0", build = "py311_0" }
```

### Full MatchSpec TOML Mapping

```toml
[dependencies.pytorch]
version = "2.0.*"
build = "cuda*"
build-number = ">=1"
channel = "https://prefix.dev/my-channel"
md5 = "1234567890abcdef1234567890abcdef"
sha256 = "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
license = "BSD-3-Clause"
file-name = "pytorch-2.0.0-cuda.tar.bz2"
```

### Build Strings

Build strings distinguish package variants (hardware, Python version, compiler). Format: `py311h43a39b2_0`

```bash
pixi add "pytorch=*=cuda*"         # Any CUDA build
pixi add "numpy=*=py311*"          # Python 3.11 builds
pixi add "pytorch [build='cuda*']" # Bracket syntax
pixi add "pytorch [version='2.9.*', build='cuda*']"  # Combined
```

### Build Numbers

```bash
pixi add "python [version='3.11.0', build_number='1']"
pixi add "numpy [build_number='>=5']"
```

```toml
[dependencies.python]
version = "3.11.0"
build-number = ">=1"
```

### Channel Specification

```bash
pixi add "pytorch [channel='pytorch']"
pixi add pytorch::pytorch
pixi add https://prefix.dev/my-channel::custom-package
```

```toml
[dependencies.pytorch]
channel = "pytorch"

[workspace]
channels = ["conda-forge", "pytorch", "nvidia"]
```

### Source Packages (pixi-build preview)

Path-based:
```toml
[dependencies.local-package]
path = "/path/to/package"
```

Git-based:
```toml
[dependencies.git-package]
git = "https://github.com/org/repo"
branch = "main"
subdirectory = "packages/mypackage"

[dependencies.tagged-git-package]
git = "https://github.com/org/repo"
tag = "v1.0.0"

[dependencies.rev-git-package]
git = "https://github.com/org/repo"
rev = "abc123def"
```

## PyPI Version Specs

Follow PEP 440:

```toml
[pypi-dependencies]
pkg = ">=1.0.0"
pkg = "~=1.2.0"            # Compatible (>=1.2.0, <1.3.0)
pkg = "==1.2.*"            # Prefix matching
pkg = "*"                  # Any version (pixi extension)
```

### With extras

```toml
pandas = { version = ">=1.0", extras = ["sql", "excel"] }
```

### Git dependencies

```toml
pkg = { git = "https://github.com/org/repo.git" }
pkg = { git = "https://github.com/org/repo.git", rev = "abc123" }
pkg = { git = "https://github.com/org/repo.git", branch = "main" }
pkg = { git = "https://github.com/org/repo.git", tag = "v1.0.0" }
pkg = { git = "ssh://git@github.com/org/repo.git", subdirectory = "py" }
```

### Local path

```toml
mypackage = { path = "./packages/mypackage", editable = true }
```

### Direct URL

```toml
pkg = { url = "https://example.com/package-1.0.0-py3-none-any.whl" }
```

### Custom index

```toml
torch = { version = ">=2.0", index = "https://download.pytorch.org/whl/cu124" }
```

### Environment markers

```toml
nvidia-nccl-cu12 = { version = "==2.27.3", env-markers = "sys_platform == 'linux'" }
```

## PyPI Options

```toml
[pypi-options]
index-url = "https://pypi.org/simple"
extra-index-urls = ["https://custom.pypi.org/simple"]
find-links = [{ path = "./wheels" }, { url = "https://example.com/wheels" }]
no-build-isolation = ["detectron2"]  # Or true for all
no-build = true                       # No source distributions
no-binary = ["numpy"]                 # Build from source
```

### Index strategy

```toml
[pypi-options]
index-strategy = "first-index"  # Default: stop at first match
# "unsafe-first-match" - search all, prefer first index versions
# "unsafe-best-match" - search all, prefer best version
```

### Prerelease handling

```toml
[pypi-options]
prerelease-mode = "if-necessary-or-explicit"  # Default
# "disallow" - no prereleases
# "allow" - all prereleases ok
# "if-necessary" - only when no stable exists
# "explicit" - only if explicitly requested
```

### Dependency overrides

Override version constraints for transitive PyPI dependencies when direct dependencies specify outdated or overly restrictive versions.

**Warning:** Use with caution. Pixi ignores all version constraints from the dependency and uses your specified version instead.

```toml
# pixi.toml - global override
[pypi-options.dependency-overrides]
numpy = ">=2.0.0"
pandas = ">=2.1.0"

# pyproject.toml - global override
[tool.pixi.pypi-options.dependency-overrides]
numpy = ">=2.0.0"
```

Feature-specific overrides:

```toml
[feature.dev.pypi-options.dependency-overrides]
numpy = ">=2.0.0"

[feature.test.pypi-options.dependency-overrides]
numpy = ">=1.26.0"
```

**Override priority:** When multiple features in an environment override the same dependency, the constraint from the earlier-defined feature is applied (not combined). The default feature always comes last in resolution order.

Use cases:
- Forcing compatible versions when dependencies have conflicting requirements
- Updating to newer library versions when transitive dependencies lag behind
- Resolving version conflicts in complex dependency trees

## Build dependencies

For packages requiring torch during build:

```toml
[dependencies]
pytorch = "2.4.0"

[pypi-options]
no-build-isolation = ["detectron2"]

[pypi-dependencies]
detectron2 = { git = "https://github.com/facebookresearch/detectron2.git" }
```

Conda dependencies are installed before PyPI resolution, making them available for building.

## Conda & PyPI Interoperability

Pixi uses a "conda-first approach" with three-stage dependency resolution:

1. **Conda Resolution**: `resolvo` library (via `rattler`) solves conda dependencies first
2. **Package Mapping**: Conda packages map to PyPI equivalents using `parselmouth`
3. **PyPI Resolution**: `PubGrub` library (via `uv`) resolves remaining PyPI dependencies

### Dual Specification

When both ecosystems specify the same package:

```toml
[dependencies]
python = ">=3.8"
numpy = ">=1.21.0"

[pypi-dependencies]
numpy = ">=1.21.0"
```

Result: Conda version installs since it resolved first; PyPI requirement satisfied by conda package mapping.

### PyPI-Only Dependency

```toml
[dependencies]
python = ">=3.8"

[pypi-dependencies]
numpy = ">=1.21.0"
```

Result: Python from conda; numpy from PyPI.

### Managing Version Conflicts

Conflicts arise when conda resolves differently than PyPI requires:

```toml
# This fails - conda resolves typing_extensions to 4.15.0
[dependencies]
typing_extensions = "*"

[pypi-dependencies]
typing_extensions = "==4.14"
```

**Solution:** Constrain conda dependencies to match PyPI requirements:

```toml
[dependencies]
some-conda-package = "*"
typing_extensions = "<4.15"

[pypi-dependencies]
some-pypi-package = "==0.1.0"
```

## System Requirements

System requirements define what "kind of machines" your environment can run on. They function as virtual packages (`__linux`, `__cuda`, `__glibc`) that communicate system features to the dependency resolver.

### Configuration

```toml
[system-requirements]
linux  = "4.18"
libc   = { family = "glibc", version = "2.28" }
cuda   = "12"
macos  = "13.0"
```

### Defaults

| Platform | Requirement | Default |
|----------|-------------|---------|
| Linux | Kernel | 4.18 |
| Linux | glibc | 2.28 |
| macOS (x64/ARM64) | Version | 13.0 |
| Windows | None | - |

### CUDA Configuration

```toml
[system-requirements]
cuda = "12"
```

**Note:** System requirements cannot enforce specific CUDA runtime versions—they only specify supported versions based on NVIDIA driver APIs.

### Environment-Specific System Requirements

```toml
[feature.cuda.system-requirements]
cuda = "12"

[environments]
cuda = ["cuda"]
```

### Override Environment Variables

For non-standard systems:

```bash
CONDA_OVERRIDE_CUDA=11
CONDA_OVERRIDE_GLIBC=2.28
CONDA_OVERRIDE_OSX=13.0
```
