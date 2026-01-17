# GitHub Actions Reference

## Setup Action

Use `prefix-dev/setup-pixi` to integrate pixi into GitHub Actions:

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    pixi-version: v0.63.1
    cache: true
- run: pixi run test
```

**Important:** Pin to specific versions (`@v0.9.2`) rather than floating tags. Use Dependabot for automatic updates.

## Basic Workflow

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: prefix-dev/setup-pixi@v0.9.2
        with:
          cache: true
      - run: pixi run test
```

## Caching

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    cache: true                    # Cache project environments (default when pixi.lock exists)
    global-cache: true             # Cache global environments
    cache-key: custom-prefix-      # Custom cache key prefix
```

Restrict cache writes to avoid exceeding GitHub's 10 GB limit:

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    cache: true
    cache-write: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
```

## Multiple Environments

### Matrix strategy (parallel jobs)

```yaml
jobs:
  test:
    strategy:
      matrix:
        environment: [py310, py311, py312]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: prefix-dev/setup-pixi@v0.9.2
        with:
          environments: ${{ matrix.environment }}
      - run: pixi run -e ${{ matrix.environment }} test
```

### Single job (all environments)

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    environments: py311 py312
```

## Environment Activation

Activate environment for all subsequent steps:

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    activate-environment: true     # Activate default environment
    # activate-environment: py311  # Or specify which environment
```

## Custom Shell Wrapper

Run commands directly in pixi environment:

```yaml
- run: |
    python --version
    pip install --no-deps -e .
  shell: pixi run bash -e {0}
```

One-off commands without project manifest:

```yaml
- run: zstd --version
  shell: pixi exec --spec zstd -- bash -e {0}
```

## Authentication

### Token (prefix.dev)

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    auth-host: prefix.dev
    auth-token: ${{ secrets.PREFIX_DEV_TOKEN }}
```

### HTTP Basic Auth (Artifactory, etc.)

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    auth-host: my-artifactory.example.com
    auth-username: ${{ secrets.ARTIFACTORY_USER }}
    auth-password: ${{ secrets.ARTIFACTORY_PASS }}
```

### Conda Token (Anaconda.org)

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    auth-host: conda.anaconda.org
    auth-conda-token: ${{ secrets.ANACONDA_TOKEN }}
```

### S3 Credentials

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    auth-host: s3://my-bucket
    auth-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    auth-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## Global Environments

Install tools needed for setup:

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    global-environments: |
      google-cloud-sdk
      keyring --with keyrings.google-artifactregistry-auth
```

## Installation Control

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    locked: true           # Use --locked flag
    frozen: true           # Use --frozen flag
    run-install: false     # Skip install, only set up pixi
    manifest-path: pyproject.toml  # Explicit manifest path
```

## Debugging

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    log-level: vvv         # Options: q, default, v, vv, vvv
```

Or re-run workflow in debug mode via GitHub UI.

## Self-Hosted Runners

Clean up after job to prevent secret leakage:

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    post-cleanup: true
    pixi-bin-path: ${{ runner.temp }}/bin/pixi
```

## Multi-Platform Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: prefix-dev/setup-pixi@v0.9.2
        with:
          cache: true
      - run: pixi run test
```

## Complete Example

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        environment: [py310, py311, py312]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - uses: prefix-dev/setup-pixi@v0.9.2
        with:
          environments: ${{ matrix.environment }}
          cache: true
          cache-write: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}

      - name: Run tests
        run: pixi run -e ${{ matrix.environment }} test

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: prefix-dev/setup-pixi@v0.9.2
        with:
          environments: lint
          cache: true
      - run: pixi run -e lint check
```

## Action Inputs Reference

| Input | Description |
|-------|-------------|
| `pixi-version` | Pixi version to install |
| `cache` | Enable project environment caching |
| `global-cache` | Enable global environment caching |
| `cache-key` | Custom cache key prefix |
| `cache-write` | Condition for writing cache |
| `environments` | Space-separated environments to install |
| `global-environments` | Global packages to install |
| `activate-environment` | Activate environment for subsequent steps |
| `locked` | Use --locked flag |
| `frozen` | Use --frozen flag |
| `run-install` | Run pixi install (default: true) |
| `manifest-path` | Path to manifest file |
| `log-level` | Logging verbosity |
| `auth-host` | Authentication host |
| `auth-token` | Bearer token |
| `auth-username` | HTTP basic auth username |
| `auth-password` | HTTP basic auth password |
| `auth-conda-token` | Conda token |
| `post-cleanup` | Clean up after job |
| `pixi-bin-path` | Custom pixi binary path |
