# Pixi Build

Pixi's build feature enables creating conda packages from source code. This is useful for:
- Building and uploading packages to conda channels
- Allowing users to build dependencies from source automatically
- Managing multiple packages in workspaces (monorepos)

> **Note:** `pixi-build` is a preview feature. Enable it with `preview = ["pixi-build"]` in the workspace table.

## Getting Started

### Basic Configuration

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["win-64", "linux-64", "osx-arm64", "osx-64"]
preview = ["pixi-build"]

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

### CLI Commands

```bash
pixi build                    # Create a .conda package file
pixi install                  # Auto-builds path/git/URL dependencies
pixi run <task>               # Auto-builds if needed before running
```

## Build Backends

Build backends are executables that handle the actual package building. They decouple package building from pixi itself.

### Available Backends

| Backend | Use Case |
|---------|----------|
| `pixi-build-python` | Python packages using PEP 517 build systems |
| `pixi-build-cmake` | C++ packages with CMake |
| `pixi-build-ros` | ROS/ROS2 packages |
| `pixi-build-rust` | Rust packages |
| `pixi-build-rattler-build` | Full control with rattler-build recipes |

### Backend Configuration

```toml
[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }
channels = [
  "https://prefix.dev/pixi-build-backends",
  "https://prefix.dev/conda-forge",
]

# Backend-specific configuration
[package.build.config]
extra-args = ["-DCMAKE_BUILD_TYPE=Release"]
```

### Overriding Backends (Development)

```bash
# Override specific backend
PIXI_BUILD_BACKEND_OVERRIDE="pixi-build-cmake=/path/to/bin" pixi install

# Use all backends from PATH
PIXI_BUILD_BACKEND_OVERRIDE_ALL=1 pixi install
```

## Dependency Types

Packages have three dependency categories:

### Build Dependencies

Dependencies needed on the **build machine** during compilation. Used for cross-compilation.

```toml
[package.build-dependencies]
cxx-compiler = "*"
cmake = "*"
```

### Host Dependencies

Dependencies for the **target machine** needed during build/link time.

```toml
[package.host-dependencies]
python = "3.12.*"
hatchling = "*"      # Python build backend
nanobind = "*"       # For C++ bindings
openssl = "*"        # Libraries to link against
```

### Run Dependencies

Dependencies required when **running** the package.

```toml
[package.run-dependencies]
numpy = ">=1.20"
requests = "*"
```

### Cross-Compilation Example

When building on linux-64 for linux-aarch64:
- **Build dependencies**: Use linux-64 binaries (compilers run on build machine)
- **Host dependencies**: Use linux-aarch64 binaries (linked into final package)

## Building Python Packages

### Project Structure

```
my-package/
├── src/
│   └── my_package/
│       └── __init__.py
├── pyproject.toml
└── pixi.toml
```

### pyproject.toml

```toml
[project]
name = "my-package"
version = "0.1.0"
requires-python = ">= 3.11"
dependencies = ["rich"]

[project.scripts]
my-cli = "my_package:main"

[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]
```

### pixi.toml

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["win-64", "linux-64", "osx-arm64", "osx-64"]
preview = ["pixi-build"]

[dependencies]
my-package = { path = "." }

[tasks]
start = "my-cli"

[package]
name = "my-package"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }

[package.host-dependencies]
hatchling = "==1.26.3"

[package.run-dependencies]
rich = "13.9.*"
```

### Initialize and Run

```bash
pixi init --format pixi       # Create pixi.toml (not extending pyproject.toml)
pixi run start                # Build and run
```

## Building C++ Packages

### With pixi-build-cmake

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["osx-arm64", "linux-64", "osx-64", "win-64"]
preview = ["pixi-build"]

[dependencies]
cpp_math = { path = "." }
python = "*"

[tasks]
start = "python -c 'import cpp_math as b; print(b.add(1, 2))'"

[package]
name = "cpp_math"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-cmake", version = "0.3.*" }

[package.build.config]
extra-args = ["-DCMAKE_BUILD_TYPE=Release"]

[package.host-dependencies]
cmake = "3.20.*"
nanobind = "2.4.*"
python = "3.12.*"
```

### CMakeLists.txt for Python Bindings

```cmake
cmake_minimum_required(VERSION 3.20)
project(cpp_math)

find_package(Python 3.8 COMPONENTS Interpreter Development.Module REQUIRED)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(cpp_math src/math.cpp)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -c "import sysconfig; print(sysconfig.get_path('purelib'))"
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE PYTHON_SITE_PACKAGES)

install(TARGETS cpp_math LIBRARY DESTINATION "${PYTHON_SITE_PACKAGES}")
```

### With rattler-build (Advanced)

For more control, use `pixi-build-rattler-build` with a `recipe.yaml`:

```toml
[package.build]
backend = { name = "pixi-build-rattler-build", version = "0.3.*" }
```

**recipe.yaml:**

```yaml
package:
  name: cpp_math
  version: 0.1.0

source:
  path: .
  use_gitignore: true

build:
  number: 0
  script: |
    cmake $CMAKE_ARGS \
      -GNinja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=$PREFIX \
      -B $SRC_DIR/../build \
      -S .
    cmake --build $SRC_DIR/../build --target install

requirements:
  build:
    - ${{ compiler('cxx') }}
    - cmake
    - ninja
  host:
    - python 3.12.*
    - nanobind
```

## Building ROS Packages

### Workspace Setup

```bash
pixi init ros_ws --channel https://prefix.dev/robostack-jazzy \
  --channel https://prefix.dev/conda-forge
cd ros_ws
pixi add ros-jazzy-ros2run
```

### Enable Build Preview

```toml
[workspace]
channels = [
  "https://prefix.dev/robostack-jazzy",
  "https://prefix.dev/conda-forge",
]
platforms = ["linux-64"]
preview = ["pixi-build"]

[dependencies]
ros-jazzy-ros2run = ">=0.32.4,<0.33"
```

### Create ROS Package

```bash
# Python package
pixi run ros2 pkg create --build-type ament_python \
  --destination-directory src --node-name my_node my_ros_pkg

# C++ package
pixi run ros2 pkg create --build-type ament_cmake \
  --destination-directory src --node-name my_node my_ros_pkg
```

### Package Configuration (src/my_ros_pkg/pixi.toml)

```toml
[package.build.backend]
channels = [
  "https://prefix.dev/pixi-build-backends",
  "https://prefix.dev/conda-forge",
]
name = "pixi-build-ros"
version = "*"

[package.build.config]
distro = "jazzy"
```

### Add to Workspace

```toml
[dependencies]
ros-jazzy-my-ros-pkg = { path = "src/my_ros_pkg" }
```

### Build and Run

```bash
pixi build                              # Build the package
pixi run ros2 run my_ros_pkg my_node    # Run the node
```

**Key Features:**
- Metadata automatically read from `package.xml`
- Package names prefixed with `ros-<distro>-<name>`
- ROS dependencies auto-mapped (e.g., `std_msgs` → `ros-jazzy-std-msgs`)

## Workspaces (Monorepos)

Develop multiple interdependent packages in a single workspace.

### Directory Structure

```
my-workspace/
├── pixi.toml                 # Root workspace manifest
├── pyproject.toml            # Optional: Python package at root
├── src/
│   └── python_pkg/
│       └── __init__.py
└── packages/
    └── cpp_math/
        ├── pixi.toml         # Subpackage manifest
        ├── CMakeLists.txt
        └── src/
            └── math.cpp
```

### Root Manifest

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["win-64", "linux-64", "osx-arm64", "osx-64"]
preview = ["pixi-build"]

[dependencies]
python_pkg = { path = "." }

[package]
name = "python_pkg"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }

[package.run-dependencies]
cpp_math = { path = "packages/cpp_math" }
rich = "13.9.*"
```

### Subpackage Manifest (packages/cpp_math/pixi.toml)

Remove workspace table from subpackages—they inherit from root:

```toml
[package]
name = "cpp_math"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-cmake", version = "0.3.*" }

[package.host-dependencies]
cmake = "3.20.*"
nanobind = "2.4.*"
python = "3.12.*"
```

**Best Practices:**
- Define workspace settings only in root manifest
- Use `path` dependencies for local packages
- Subpackages resolved from source, not conda channels

## Build Variants

Build packages against different dependency versions (build matrices).

### Configuration

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["linux-64", "osx-arm64"]
preview = ["pixi-build"]

# Define variants
[workspace.build-variants]
python = ["3.11.*", "3.12.*"]
```

### Testing Variants with Environments

```toml
[feature.py311.dependencies]
python = "3.11.*"

[feature.py312.dependencies]
python = "3.12.*"

[environments]
py311 = ["py311"]
py312 = ["py312"]
```

### Flexible Dependencies

Change package dependencies to accept variants:

```toml
[package.host-dependencies]
python = "*"          # Accept any version from variants

[package.run-dependencies]
numpy = ">=1.20"
```

### Verify Builds

```bash
pixi list --environment py311    # Check py311 variant build
pixi list --environment py312    # Check py312 variant build
```

Different variants produce packages with distinct build strings.

## Package Source Configuration

By default, source code is expected in the manifest directory. Override this for non-standard layouts:

```toml
[package.build.source]
path = "source"       # Relative path to source directory
```

**Use Cases:**
- Source in subdirectory
- Git submodules
- Shared source between packages

### Example Structure

```
my-package/
├── pixi.toml
└── source/
    ├── src/
    │   └── main.cpp
    └── include/
        └── main.h
```

## Development Builds

The `[dev]` table installs package dependencies without building the package itself. Useful for development workflows.

### Configuration

```toml
[workspace]
channels = ["https://prefix.dev/conda-forge"]
platforms = ["linux-64", "win-64", "osx-64", "osx-arm64"]
preview = ["pixi-build"]

[package]
name = "my-rust-pkg"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-rust", version = "0.4.*" }

[package.build-dependencies]
cmake = "*"

[package.host-dependencies]
python = "3.12.*"

[package.run-dependencies]
bat = "*"

# Development mode: install deps only, don't build package
[dev]
my-rust-pkg = { path = "." }

[dependencies]
cargo-insta = "*"     # Additional dev tools

[tasks]
build = "cargo build"
test = "cargo test"
start = "cargo run"
```

### Usage

```bash
pixi install          # Installs all dependencies (cmake, python, bat, cargo-insta)
pixi run cargo build  # Use installed tools directly
pixi run start        # Run development build
```

**Key Difference from `[dependencies]`:**
- `[dependencies]`: Builds package in isolated environment, installs result
- `[dev]`: Installs build/host/run dependencies directly, skips package build

## Current Limitations

- Limited backend options (Python, CMake, ROS, Rust, rattler-build)
- Some parameters missing in backends
- Recursive source dependencies not supported
- Workspace dependencies not inherited by subpackages
