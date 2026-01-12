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

### Matchspec syntax

```toml
package = { version = ">=1.0", channel = "conda-forge" }
package = { version = ">=1.0", build = "py311_0" }
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
