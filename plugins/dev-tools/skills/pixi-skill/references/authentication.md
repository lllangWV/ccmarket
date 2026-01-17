# Authentication Reference

## Authentication Methods

| Method | Use Case | Header/Format |
|--------|----------|---------------|
| Bearer Token | prefix.dev, modern APIs | `Authorization: Bearer <TOKEN>` |
| Conda Token | anaconda.org, Quetz | URL embedded: `/t/<TOKEN>/...` |
| Basic HTTP | Self-hosted, Artifactory | `Authorization: Basic <base64>` |

## Login Commands

### Bearer token (prefix.dev)

```bash
pixi auth login prefix.dev --token <TOKEN>
```

### Conda token (anaconda.org)

```bash
pixi auth login conda.anaconda.org --conda-token <TOKEN>
```

### Basic authentication

```bash
pixi auth login my-server.example.com --username <USER> --password <PASS>
```

### S3 credentials

```bash
pixi auth login s3://my-bucket \
  --s3-access-key-id <KEY_ID> \
  --s3-secret-access-key <SECRET> \
  --s3-session-token <TOKEN>  # Optional
```

## Logout

```bash
pixi auth logout prefix.dev
pixi auth logout conda.anaconda.org
```

## Credential Storage

### Platform-specific secure storage

| Platform | Storage | Search Term |
|----------|---------|-------------|
| Windows | Credentials Manager | "rattler" |
| macOS | Keychain | "rattler" |
| Linux | GNOME Keyring (libsecret) | "rattler" |

### Fallback storage

If no secure keychain is available, credentials are stored (insecurely) in:

```
~/.rattler/credentials.json
```

## Custom Credentials File

Override storage location with environment variable:

```bash
export RATTLER_AUTH_FILE=/path/to/credentials.json
```

This takes precedence over CLI arguments and keychain storage.

### credentials.json format

```json
{
  "*.prefix.dev": {
    "BearerToken": "your-token-here"
  },
  "conda.anaconda.org": {
    "CondaToken": "your-conda-token"
  },
  "my-server.example.com": {
    "BasicHTTP": {
      "username": "user",
      "password": "pass"
    }
  }
}
```

**Note:** Wildcard hosts (e.g., `*.prefix.dev`) match all subdomains.

## PyPI Authentication

### Keyring

Install keyring for PyPI authentication:

```bash
pixi global install keyring
```

Configure in `pixi.toml`:

```toml
[pypi-options]
keyring-provider = "subprocess"
```

#### Backend packages for cloud registries

```bash
# Google Artifact Registry
pixi global install keyring keyrings.google-artifactregistry-auth

# Azure DevOps
pixi global install keyring artifacts-keyring

# AWS CodeArtifact
pixi global install keyring keyrings.codeartifact
```

### .netrc file

Standard authentication file for PyPI:

**Unix:** `~/.netrc`
**Windows:** `%HOME%\_netrc`

```
machine pypi.example.com
  login your-username
  password your-password

machine upload.pypi.org
  login __token__
  password pypi-your-api-token
```

Secure the file:

```bash
chmod 600 ~/.netrc
```

## Environment Variables

For CI/CD and automation:

```bash
# Custom credentials file
export RATTLER_AUTH_FILE=/path/to/credentials.json

# Direct token (some integrations)
export PREFIX_DEV_TOKEN=your-token
export ANACONDA_TOKEN=your-token
```

## CI/CD Integration

### GitHub Actions

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    auth-host: prefix.dev
    auth-token: ${{ secrets.PREFIX_DEV_TOKEN }}
```

### GitLab CI

```yaml
before_script:
  - pixi auth login prefix.dev --token $PREFIX_DEV_TOKEN
```

### Docker

```dockerfile
ARG PREFIX_DEV_TOKEN
RUN pixi auth login prefix.dev --token $PREFIX_DEV_TOKEN
```

Build with:

```bash
docker build --build-arg PREFIX_DEV_TOKEN=$PREFIX_DEV_TOKEN .
```

## Private Channel Configuration

After authentication, use private channels in your manifest:

```toml
[workspace]
channels = ["https://repo.prefix.dev/my-private-channel", "conda-forge"]
```

Or with conda.anaconda.org:

```toml
[workspace]
channels = ["conda.anaconda.org/my-org/label/main", "conda-forge"]
```

## Troubleshooting

### Check stored credentials

```bash
# macOS
security find-generic-password -s rattler

# Linux (if using secret-tool)
secret-tool search service rattler
```

### Verify authentication

```bash
pixi search my-private-package --channel https://repo.prefix.dev/my-channel
```

### Clear credentials

```bash
pixi auth logout <host>

# Or manually remove from keychain/credentials file
```

### Debug authentication issues

```bash
pixi install -vvv  # Verbose output shows auth attempts
```
