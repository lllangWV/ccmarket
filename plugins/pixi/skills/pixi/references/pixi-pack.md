# Pixi Pack Reference

Compress and distribute pixi environments as portable archives.

## Installation

```bash
# Global installation
pixi global install pixi-pack

# Or run directly
pixi exec pixi-pack --help
```

Pre-built binaries available at [github.com/Quantco/pixi-pack/releases](https://github.com/Quantco/pixi-pack/releases).

## Packing Environments

### Basic usage

```bash
pixi-pack pack
```

Creates `environment.tar` from the default environment.

### Specify environment and platform

```bash
pixi-pack pack --environment prod --platform linux-64
```

### Custom output file

```bash
pixi-pack pack --output my-environment.tar
```

### Cross-platform packing

Pack for a different platform than the current machine:

```bash
# Pack for Linux from macOS
pixi-pack pack --platform linux-64

# Pack for Windows
pixi-pack pack --platform win-64
```

### Self-extracting executable

Bundle the unpacker with the environment:

```bash
pixi-pack pack --create-executable
```

Creates a single executable that extracts and sets up the environment.

## Unpacking Environments

### Basic usage

```bash
pixi-unpack environment.tar
```

Creates:
- `./env/` - The unpacked environment
- `activate.sh` - Unix activation script
- `activate.bat` - Windows activation script

### Custom output directory

```bash
pixi-unpack environment.tar --output /path/to/env
```

### Using the environment

```bash
# Unix
source activate.sh
python --version

# Windows
activate.bat
python --version
```

## Advanced Options

### Inject additional packages

Add packages not in `pixi.lock`:

```bash
pixi-pack pack --inject my-custom-package-1.0.0.conda
```

### PyPI wheels

Include wheel packages:

```bash
pixi-pack pack --ignore-pypi-non-wheel
```

### Caching

Speed up repeated operations:

```bash
pixi-pack pack --use-cache ~/.pixi-pack/cache
```

### Manifest path

Specify custom manifest location:

```bash
pixi-pack pack --manifest-path /path/to/pixi.toml
```

## Configuration File

Create a config file for advanced settings:

```toml
# pixi-pack.toml

[cache]
path = "~/.pixi-pack/cache"

[download]
parallel = 8

[mirrors]
"https://conda.anaconda.org/conda-forge" = ["https://prefix.dev/conda-forge"]
```

Use with:

```bash
pixi-pack pack --config pixi-pack.toml
```

## CI/CD Usage

### GitHub Actions

```yaml
- name: Install pixi-pack
  run: pixi global install pixi-pack

- name: Pack environment
  run: pixi-pack pack --environment prod --platform linux-64

- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: environment
    path: environment.tar
```

### Deploy to server

```bash
# On build machine
pixi-pack pack --environment prod --platform linux-64
scp environment.tar server:/app/

# On target server (no conda/pixi needed)
pixi-unpack environment.tar
source activate.sh
python app.py
```

## Compatibility

The archive includes fallback files for manual installation:

- `environment.yml` - Conda environment file
- `repodata.json` - Package metadata

Install without `pixi-unpack`:

```bash
tar -xf environment.tar
conda env create -f environment.yml
# or
micromamba create -f environment.yml
```

## Command Reference

### pixi-pack pack

```
pixi-pack pack [OPTIONS]

Options:
  -e, --environment <ENV>    Environment to pack
  -p, --platform <PLATFORM>  Target platform
  -o, --output <FILE>        Output file path
  -m, --manifest-path <PATH> Path to pixi.toml
  --create-executable        Create self-extracting executable
  --inject <PACKAGE>         Inject additional packages
  --use-cache <PATH>         Cache directory
  --config <PATH>            Configuration file
  --ignore-pypi-non-wheel    Ignore non-wheel PyPI packages
```

### pixi-unpack

```
pixi-unpack [OPTIONS] <ARCHIVE>

Options:
  -o, --output <DIR>  Output directory (default: ./env)
```

## Use Cases

- **Air-gapped deployments**: Ship environments to machines without internet
- **Reproducible deployments**: Exact environment reproduction on target machines
- **Cross-platform builds**: Create Linux packages on macOS/Windows
- **CI/CD acceleration**: Cache packed environments between runs
- **Custom package bundling**: Include in-house packages with dependencies
