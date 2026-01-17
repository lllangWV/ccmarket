# Rust with Pixi Reference

## Project Setup

Initialize a Pixi workspace for Rust:

```bash
pixi init my_rust_project
cd my_rust_project
```

Add the Rust toolchain:

```bash
pixi add rust
```

Initialize a Cargo project:

```bash
pixi run cargo init
```

## Configuration

### Basic pixi.toml

```toml
[workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]

[dependencies]
rust = "*"

[tasks]
build = "cargo build"
start = "cargo run"
test = "cargo test"
```

### With System Dependencies

```toml
[dependencies]
rust = "*"
openssl = "*"
pkg-config = "*"
compilers = "*"

[tasks]
build = "cargo build"
release = "cargo build --release"
```

## Building and Running

```bash
# Direct execution
pixi run cargo build
pixi run cargo run

# Using tasks
pixi run build
pixi run start

# Interactive shell
pixi shell
cargo build
cargo run
```

## Task Management

### Define Tasks

```bash
pixi task add build "cargo build"
pixi task add start "cargo run"
pixi task add test "cargo test"
pixi task add fmt "cargo fmt"
pixi task add lint "cargo clippy"
```

### Advanced Task Configuration

```toml
[tasks]
build = "cargo build"
release = "cargo build --release"
test = "cargo test"
fmt = "cargo fmt"

[tasks.lint]
cmd = "cargo clippy"
depends-on = ["fmt"]

[tasks.check]
cmd = "cargo check"
inputs = ["src/**/*.rs", "Cargo.toml"]
```

## System Dependencies

Pixi manages C/system libraries alongside Rust, preventing build failures:

```bash
# Common system dependencies
pixi add openssl pkg-config compilers

# For specific libraries
pixi add zlib libssl-dev cmake
```

### Common Dependencies by Use Case

**Web/Network projects:**
```toml
[dependencies]
rust = "*"
openssl = "*"
pkg-config = "*"
```

**Database projects:**
```toml
[dependencies]
rust = "*"
postgresql = "*"
sqlite = "*"
pkg-config = "*"
```

**Graphics/GUI projects:**
```toml
[dependencies]
rust = "*"
compilers = "*"
cmake = "*"
pkg-config = "*"
```

## Key Benefits Over rustup

- **System dependencies included:** No separate installation of OpenSSL, libssl, etc.
- **Cross-platform reproducibility:** Same environment on any system with Pixi
- **Unified tooling:** Manage Rust, system libraries, and build tools together
- **No global state:** Each project has isolated dependencies

## Troubleshooting

### Missing System Library

```
error: failed to run custom build command for `openssl-sys`
```

Solution:
```bash
pixi add openssl pkg-config
```

### Linker Errors

```bash
pixi add compilers
```

### pkg-config Not Found

```bash
pixi add pkg-config
```
