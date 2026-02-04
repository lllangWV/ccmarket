---
name: rattler-build
description: Use when writing recipe.yaml files, building conda packages, converting conda-build recipes, debugging build failures, or configuring variants for multiple Python/numpy versions
---

# Rattler-Build

Fast cross-platform conda package builder. Creates packages installable via pixi, mamba, or conda.

## Quick Commands

```bash
rattler-build build -r recipe.yaml              # Build package
rattler-build build -r recipe.yaml -c conda-forge  # With channel
rattler-build build --target-platform linux-aarch64  # Cross-compile
rattler-build generate-recipe pypi numpy -w     # Generate from PyPI
rattler-build test -p ./package.conda           # Test package
rattler-build debug -r recipe.yaml && rattler-build debug-shell  # Debug
```

Platforms: `linux-64`, `linux-aarch64`, `osx-64`, `osx-arm64`, `win-64`

## Recipe Structure

```yaml
context:
  version: "1.0.0"

package:
  name: mypackage
  version: ${{ version }}

source:
  url: https://example.com/pkg-${{ version }}.tar.gz
  sha256: abc123...

build:
  noarch: python
  skip:
    - win
  python:
    entry_points:
      - mycli = mypackage.cli:main

requirements:
  build:
    - ${{ compiler('c') }}
  host:
    - python
    - pip
    - numpy
  run:
    - python
    - ${{ pin_compatible('numpy', max_pin='x') }}
  run_exports:
    weak:
      - ${{ pin_subpackage(name, max_pin='x.x') }}

tests:
  - python:
      imports:
        - mypackage
```

## Key Syntax

| Jinja Function | Usage |
|----------------|-------|
| `${{ compiler('c') }}` | C compiler for target platform |
| `${{ pin_subpackage(name, max_pin='x.x') }}` | Pin to recipe output |
| `${{ pin_compatible('numpy', max_pin='x') }}` | Pin to resolved version |

| Selector | Meaning |
|----------|---------|
| `if: win` | Windows |
| `if: unix` | Linux/macOS |
| `if: osx and arm64` | Apple Silicon |

**Conditional dependencies:**
```yaml
requirements:
  run:
    - if: win
      then: pywin32
    - if: unix
      then: pexpect
```

## Multiple Outputs

```yaml
source:
  url: https://example.com/project.tar.gz
  sha256: abc...

outputs:
  - package:
      name: libmylib
    build:
      script: install-lib.sh
    requirements:
      build:
        - ${{ compiler('c') }}
      run_exports:
        weak:
          - ${{ pin_subpackage('libmylib', max_pin='x.x') }}

  - package:
      name: python-mylib
    requirements:
      host:
        - python
        - pip
        - ${{ pin_subpackage('libmylib', exact=True) }}
      run:
        - python
        - ${{ pin_subpackage('libmylib') }}
```

## Variants

```yaml
# variant_config.yaml
python:
  - "3.10"
  - "3.11"
numpy:
  - "1.24"
  - "1.26"

zip_keys:
  - [python, numpy]  # Pair together (2 builds, not 4)

pin_run_as_build:
  numpy:
    max_pin: 'x.x'
```

```bash
rattler-build build -r recipe.yaml -m variant_config.yaml
```

## Debugging

```bash
rattler-build build --keep-build -r recipe.yaml  # Keep env after build
rattler-build debug -r recipe.yaml               # Setup build env
rattler-build debug-shell                        # Enter shell
```

In debug shell:
- `$PREFIX` - host installation
- `$BUILD_PREFIX` - build tools
- `$SRC_DIR` - source directory
- `bash -x conda_build.sh` - run with tracing

## Converting from conda-build

| conda-build | rattler-build |
|-------------|---------------|
| `{% set v = "1.0" %}` | `context: v: "1.0"` |
| `{{ var }}` | `${{ var }}` |
| `# [win]` | `if: win` / `then:` |
| `test:` | `tests:` (plural, list) |
| `build.run_exports` | `requirements.run_exports.weak` |

See [references/](references/) for complete CLI, recipe, variant, and migration docs.
