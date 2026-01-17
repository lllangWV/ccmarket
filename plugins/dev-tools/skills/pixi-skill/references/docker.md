# Docker / Container Reference

## Official Images

Pixi provides official Docker images at `ghcr.io/prefix-dev/pixi`.

### Available tags

| Tag | Base |
|-----|------|
| `latest` | Ubuntu Jammy |
| `jammy` | Ubuntu 22.04 |
| `focal` | Ubuntu 20.04 |
| `bullseye` | Debian Bullseye |
| `noble-cuda-12.9.1` | Ubuntu Noble + CUDA 12.9.1 |
| `noble-cuda-13.0.0` | Ubuntu Noble + CUDA 13.0.0 |

## Basic Dockerfile

Simple single-stage build:

```dockerfile
FROM ghcr.io/prefix-dev/pixi:latest

WORKDIR /app
COPY . .

RUN pixi install --locked

CMD ["pixi", "run", "start"]
```

## Multi-Stage Build (Recommended)

Optimized production image without pixi in final stage:

```dockerfile
# Build stage
FROM ghcr.io/prefix-dev/pixi:latest AS build

WORKDIR /app

# Copy manifest files first for better caching
COPY pixi.toml pixi.lock ./
RUN pixi install --locked -e prod

# Copy application code
COPY . .

# Generate activation script
RUN pixi shell-hook -e prod > /shell-hook.sh

# Create entrypoint that activates environment
RUN echo '#!/bin/bash\nsource /shell-hook.sh\nexec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Production stage
FROM ubuntu:24.04 AS production

WORKDIR /app

# Copy environment from build stage (preserve path structure)
COPY --from=build /app/.pixi/envs/prod /app/.pixi/envs/prod
COPY --from=build /shell-hook.sh /shell-hook.sh
COPY --from=build /entrypoint.sh /entrypoint.sh

# Copy application code
COPY --from=build /app/src ./src

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "src/main.py"]
```

## Environment Activation

Use `pixi shell-hook` to generate activation scripts that work without pixi installed:

```dockerfile
# Generate shell hook for environment activation
RUN pixi shell-hook -e prod > /activate.sh

# In entrypoint or CMD
RUN echo '#!/bin/bash\nsource /activate.sh\nexec "$@"' > /entrypoint.sh
```

## Layer Caching

Optimize Docker layer caching by copying manifest files before source code:

```dockerfile
# Copy only manifest files first
COPY pixi.toml pixi.lock ./
RUN pixi install --locked

# Then copy source code (changes more frequently)
COPY src/ ./src/
```

## Multiple Environments

Build different images for different environments:

```dockerfile
# Development image
FROM ghcr.io/prefix-dev/pixi:latest AS dev
WORKDIR /app
COPY . .
RUN pixi install --locked -e dev
CMD ["pixi", "run", "-e", "dev", "serve"]

# Production image
FROM ghcr.io/prefix-dev/pixi:latest AS prod
WORKDIR /app
COPY . .
RUN pixi install --locked -e prod
CMD ["pixi", "run", "-e", "prod", "start"]
```

Build specific target:

```bash
docker build --target prod -t myapp:prod .
docker build --target dev -t myapp:dev .
```

## With Private Channels

### Build argument

```dockerfile
FROM ghcr.io/prefix-dev/pixi:latest

ARG PREFIX_DEV_TOKEN
RUN pixi auth login prefix.dev --token $PREFIX_DEV_TOKEN

WORKDIR /app
COPY . .
RUN pixi install --locked
```

Build with:

```bash
docker build --build-arg PREFIX_DEV_TOKEN=$PREFIX_DEV_TOKEN -t myapp .
```

### Secret mount (Docker BuildKit)

More secure approach that doesn't store token in layer:

```dockerfile
# syntax=docker/dockerfile:1
FROM ghcr.io/prefix-dev/pixi:latest

WORKDIR /app
COPY pixi.toml pixi.lock ./

RUN --mount=type=secret,id=prefix_token \
    pixi auth login prefix.dev --token $(cat /run/secrets/prefix_token) && \
    pixi install --locked

COPY . .
```

Build with:

```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=prefix_token,env=PREFIX_DEV_TOKEN \
  -t myapp .
```

## CUDA Images

For GPU workloads:

```dockerfile
FROM ghcr.io/prefix-dev/pixi:noble-cuda-12.9.1

WORKDIR /app
COPY . .

RUN pixi install --locked

CMD ["pixi", "run", "train"]
```

Run with GPU access:

```bash
docker run --gpus all myapp
```

## Docker Compose

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    command: pixi run serve

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: pixi run worker
    depends_on:
      - app
```

## .dockerignore

Exclude unnecessary files:

```
.pixi/
.git/
*.pyc
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.egg-info/
dist/
build/
.env
```

## Tips

- **Use `--locked`**: Ensures reproducible builds from `pixi.lock`
- **Multi-stage builds**: Keep production images small by not including pixi
- **Layer caching**: Copy `pixi.toml` and `pixi.lock` before source code
- **Shell hook**: Use `pixi shell-hook` for activation without pixi binary
- **Secrets**: Use BuildKit secret mounts for private channel tokens
- **.dockerignore**: Exclude `.pixi/` directory to avoid copying local environment

## Resources

- [pixi-docker](https://github.com/prefix-dev/pixi-docker) - Official Docker images
- [pixi-docker-example](https://github.com/pavelzw/pixi-docker-example) - Example repository
