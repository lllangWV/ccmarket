# PyTorch Installation Reference

## Method 1: Conda-Forge (Recommended)

### GPU with CUDA

```toml
[workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "win-64"]

[system-requirements]
cuda = "12.0"

[dependencies]
pytorch-gpu = "*"
cuda-version = "12.6.*"  # Pin CUDA version
```

### CPU Only

```toml
[dependencies]
pytorch-cpu = "*"
```

### Dual CPU/GPU Environments

```toml
[workspace]
channels = ["conda-forge"]
platforms = ["linux-64"]

[feature.gpu.system-requirements]
cuda = "12.0"

[feature.gpu.dependencies]
pytorch-gpu = "*"
cuda-version = "12.6.*"

[feature.cpu.dependencies]
pytorch-cpu = "*"

[environments]
default = ["gpu"]
cpu = ["cpu"]
```

Run: `pixi run -e cpu python script.py`

## Method 2: PyPI

### PyTorch Indexes

- CPU: `https://download.pytorch.org/whl/cpu`
- CUDA 11.8: `https://download.pytorch.org/whl/cu118`
- CUDA 12.1: `https://download.pytorch.org/whl/cu121`
- CUDA 12.4: `https://download.pytorch.org/whl/cu124`
- ROCm 6: `https://download.pytorch.org/whl/rocm6.2`

### GPU Installation

```toml
[workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "win-64"]

[dependencies]
python = ">=3.11,<3.13"

[pypi-dependencies]
torch = { version = ">=2.5.1", index = "https://download.pytorch.org/whl/cu124" }
torchvision = { version = ">=0.20.1", index = "https://download.pytorch.org/whl/cu124" }
```

### Cross-Platform with CPU Fallback

```toml
[pypi-dependencies]
torch = { version = ">=2.5.1", index = "https://download.pytorch.org/whl/cu124" }

[target.osx.pypi-dependencies]
torch = { version = ">=2.5.1", index = "https://download.pytorch.org/whl/cpu" }
```

### Multi-Environment PyPI

```toml
[feature.gpu.system-requirements]
cuda = "12.0"

[feature.gpu.pypi-dependencies]
torch = { version = ">=2.5.1", index = "https://download.pytorch.org/whl/cu124" }

[feature.cpu.pypi-dependencies]
torch = { version = ">=2.5.1", index = "https://download.pytorch.org/whl/cpu" }

[environments]
default = ["cpu"]
gpu = ["gpu"]
```

## Verification

```bash
pixi run python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

Check detected CUDA:
```bash
pixi info  # Look for __cuda in virtual packages
nvidia-smi  # System CUDA
pixi run nvcc --version  # Environment CUDA toolkit
```

## Troubleshooting

### GPU version not installing

**Conda-forge:**
- Ensure `system-requirements.cuda` is set
- Use `cuda-version` package to pin version

**PyPI:**
- Use correct index URL for your CUDA version
- Verify Python version compatibility (PyTorch doesn't support 3.13 yet)

### ABI tag mismatch

```
torch==2.5.1 has no wheels with a matching Python ABI tag
```

Solution: Use Python 3.12 or earlier.

### Platform tag mismatch

```
torch>=2.5.1 has no wheels with a matching platform tag
```

Solution: Use CPU index for macOS, CUDA index only for Linux/Windows.

### Mixed channel conflicts

Don't mix:
- conda-forge + pytorch channel
- conda + pypi for torch and its dependents

Pick one source and use consistently.

### Cross-platform resolution on macOS

PyPI CUDA packages can't resolve on macOS (no CUDA support). Run resolution on a Linux/Windows machine for CUDA environments.

## Legacy: PyTorch Channel

Not recommended (discontinued updates):

```toml
[workspace]
channels = ["main", "nvidia", "pytorch"]

[dependencies]
pytorch = "*"
```
