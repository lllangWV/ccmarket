# Tasks Reference

## Task Basics

Tasks automate common workflows like formatting, linting, testing, and building. Define tasks in the `[tasks]` section.

```toml
[tasks]
hello = "echo Hello"                              # Simple string
build = { cmd = "npm build", cwd = "frontend" }   # With options
```

## Task Arguments (Parameterization)

Design tasks like functions with parameters and defaults for reusability.

### Defining arguments

```toml
[tasks.greet]
args = ["name"]
cmd = "echo Hello, {{ name }}!"

[tasks.test]
args = [
  { arg = "subset", default = "all" },
  { arg = "report", default = "reports/junit.xml" }
]
cmd = "pytest {{ subset }} --junit-xml {{ report }} -q"
```

### Running parameterized tasks

```bash
pixi run test                          # Uses both defaults
pixi run test integration              # Overrides subset only
pixi run test unit tmp/out.xml         # Overrides both
```

### Passing arguments to dependencies

```toml
[tasks.install-release]
depends-on = [{ task = "install", args = ["/path/to/manifest", "--debug"] }]
```

## MiniJinja Templating

Task commands support MiniJinja templating with filters and conditionals.

### Placeholders and filters

```toml
[tasks]
uppercase = { cmd = "echo {{ text | upper }}", args = ["text"] }
join-list = { cmd = "echo {{ items | join(',') }}", args = ["items"] }
```

### Conditionals

```toml
[tasks.test]
args = [{ arg = "coverage", default = "" }]
cmd = "pytest {% if coverage %}--cov{% endif %}"
```

### Pixi context variables

Pixi provides automatic context variables:

| Variable | Description |
|----------|-------------|
| `pixi.platform` | Current platform (linux-64, osx-arm64, win-64) |
| `pixi.environment.name` | Environment name |
| `pixi.manifest_path` | Absolute path to pixi.toml |
| `pixi.version` | Pixi version |
| `pixi.is_win` | True if Windows |
| `pixi.is_unix` | True if Unix (Linux/macOS) |
| `pixi.is_linux` | True if Linux |
| `pixi.is_osx` | True if macOS |

```toml
[tasks.platform-cmd]
cmd = """echo {% if pixi.is_win %}windows{% else %}unix{% endif %}"""
```

## Task Dependencies

Tasks can depend on other tasks, creating execution pipelines.

```toml
[tasks]
configure = "cmake -G Ninja -S . -B .build"
build = { cmd = "ninja -C .build", depends-on = ["configure"] }
test = { cmd = "ctest", depends-on = ["build"] }
```

### Shorthand for task-only dependencies

```toml
[tasks]
style = [{ task = "fmt" }, { task = "lint" }]
```

### Environment-specific dependencies

Run tasks in different conda environments:

```toml
[tasks.test-all]
depends-on = [
  { task = "test", environment = "py311" },
  { task = "test", environment = "py312" }
]
```

### Task aliases with arguments

Create shortcuts with pre-filled arguments:

```toml
[tasks]
lint-fast   = [{ task = "lint", args = ["--fix"] }]
lint-strict = [{ task = "lint", args = ["--select", "I001"] }]
```

## Caching with Inputs/Outputs

Pixi caches task results when the environment, inputs, outputs, and command remain unchanged.

```toml
[tasks.build]
cmd = "make"
inputs = ["src/*.cpp", "include/*.hpp"]
outputs = ["build/app.exe"]
```

### With parameterized paths

```toml
[tasks.process-file]
args = ["filename"]
cmd = "python process.py inputs/{{ filename }}.txt --output outputs/{{ filename }}.processed"
inputs = ["inputs/{{ filename }}.txt"]
outputs = ["outputs/{{ filename }}.processed"]
```

## Working Directory

Execute tasks in a specific directory relative to pixi.toml:

```toml
[tasks]
frontend-build = { cmd = "npm run build", cwd = "frontend" }
backend-test = { cmd = "pytest", cwd = "backend" }
```

## Environment Variables

Set task-specific environment variables:

```toml
[tasks]
dev = { cmd = "python main.py", env = { LOG_LEVEL = "DEBUG", ENV = "development" } }
prod = { cmd = "python main.py", env = { LOG_LEVEL = "WARN", ENV = "production" } }
```

Variables support shell-style expansions and work uniformly across platforms.

## Clean Environment

Restrict tasks to only Pixi-provided environment variables:

```toml
[tasks]
isolated = { cmd = "python script.py", clean-env = true }
```

**Note:** Not supported on Windows due to compiler and dependency requirements.

## Hidden Tasks

Prefix with underscore to hide from `pixi task list`:

```toml
[tasks]
_internal-helper = "echo helper"
build = { cmd = "make", depends-on = ["_internal-helper"] }
```

## Platform-Specific Tasks

Define tasks for specific platforms:

```toml
[target.win-64.tasks]
greet = "echo Hello Windows"
open = "start ."

[target.unix.tasks]
greet = "echo Hello Unix"
open = "xdg-open ."

[target.osx.tasks]
open = "open ."
```

Valid targets: `win-64`, `win-arm64`, `linux-64`, `osx-64`, `osx-arm64`, `unix`, `win`, `linux`, `osx`

## deno_task_shell Features

Pixi uses deno_task_shell for cross-platform execution.

### Built-in commands

`cp`, `mv`, `rm`, `mkdir`, `pwd`, `sleep`, `echo`, `cat`, `exit`, `unset`, `xargs`

### Shell syntax

```toml
[tasks]
# Boolean lists
both = "cmd1 && cmd2"              # Continue on success
either = "cmd1 || cmd2"            # Continue on failure

# Sequential
all = "cmd1 ; cmd2 ; cmd3"

# Pipelines
filter = "cat file.txt | grep pattern"

# Command substitution
version = "echo $(python --version)"

# Redirects
save = "echo output > file.txt"
append = "echo more >> file.txt"

# Globs
clean = "rm *.tmp"
find = "ls **/*.py"
```

## Complete Example

```toml
[tasks]
# Development
dev = { cmd = "python -m uvicorn main:app --reload", env = { ENV = "dev" } }

# Testing with parameters
test = { cmd = "pytest {{ path }} -v", args = [{ arg = "path", default = "tests/" }] }
test-cov = [{ task = "test", args = ["--cov=src"] }]

# Build pipeline
_compile = { cmd = "gcc -c src/*.c -Iinclude", inputs = ["src/*.c"], outputs = ["*.o"] }
_link = { cmd = "gcc -o app *.o", depends-on = ["_compile"], outputs = ["app"] }
build = { depends-on = ["_link"] }

# Multi-environment CI
ci = { depends-on = [
  { task = "test", environment = "py310" },
  { task = "test", environment = "py311" },
  { task = "test", environment = "py312" }
]}

# Platform-specific
[target.unix.tasks]
serve = "python -m http.server"

[target.win-64.tasks]
serve = "python -m http.server"
```
