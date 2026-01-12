# Configuration Reference

## Config Locations (Priority Order)

| Priority | Location |
|----------|----------|
| 7 | CLI arguments |
| 6 | `.pixi/config.toml` (workspace) |
| 5 | `$PIXI_HOME/config.toml` |
| 4 | `~/.pixi/config.toml` |
| 3 | `$XDG_CONFIG_HOME/pixi/config.toml` |
| 2 | `~/.config/pixi/config.toml` |
| 1 | `/etc/pixi/config.toml` |

## Shell Settings

```toml
[shell]
change-ps1 = false                  # Disable (pixi) prompt prefix
force-activate = true               # Always re-activate
source-completion-scripts = false   # Disable autocompletion
```

## Network Settings

```toml
tls-no-verify = true  # Disable TLS verification (security risk!)
tls-root-certs = "native"  # Use system certs: "webpki", "native", "all"

[proxy-config]
http = "http://proxy:8080/"
https = "http://proxy:8080/"
non-proxy-hosts = [".internal", "localhost"]
```

## Channel Mirrors

```toml
[mirrors]
"https://conda.anaconda.org/conda-forge" = [
  "https://prefix.dev/conda-forge",
  "oci://ghcr.io/channel-mirrors/conda-forge"
]
```

## PyPI Configuration

```toml
[pypi-config]
index-url = "https://pypi.org/simple"
extra-index-urls = ["https://custom.pypi.org/simple"]
keyring-provider = "subprocess"  # Or "disabled"
allow-insecure-host = ["localhost:8080"]
```

Note: `index-url` and `extra-index-urls` only affect `pixi init`, not global resolution.

## Repodata Settings

```toml
[repodata-config]
disable-bzip2 = true
disable-jlap = true
disable-sharded = true
disable-zstd = true

# Per-channel override
[repodata-config."https://prefix.dev"]
disable-sharded = false
```

## Concurrency

```toml
[concurrency]
downloads = 50  # Max concurrent downloads
solves = 2      # Max concurrent solves
```

## Detached Environments

Store environments outside workspace:

```toml
detached-environments = true  # Use cache dir
detached-environments = "/opt/pixi/envs"  # Custom path
```

## Pinning Strategy

Default for `pixi add`:

```toml
pinning-strategy = "semver"  # Default
# "no-pin" - unconstrained (*)
# "exact-version" - ==1.2.3
# "major" - >=1.2.3,<2
# "minor" - >=1.2.3,<1.3
# "latest-up" - >=1.2.3
```

## Authentication

Override credentials file:

```toml
authentication-override-file = "/path/to/credentials.json"
```

Default lookup: keyring → `~/.rattler/credentials.json` → `.netrc`

## S3 Options

```toml
[s3-options.my-bucket]
endpoint-url = "https://s3.example.com"
force-path-style = true
region = "us-east-1"
```

## Experimental Features

```toml
[experimental]
use-environment-activation-cache = true
```

## CLI Config Commands

```bash
pixi config list                           # Show config
pixi config set <key> <value>              # Set globally
pixi config set --local <key> <value>      # Set for workspace
pixi config unset <key>                    # Remove setting
```

Examples:
```bash
pixi config set default-channels '["conda-forge", "bioconda"]'
pixi config set --local detached-environments true
pixi config set concurrency.downloads 10
```
