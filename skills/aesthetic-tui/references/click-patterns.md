# Click Patterns Reference

Detailed API patterns for the Click CLI library.

## Basic Command

```python
import click

@click.command()
def hello():
    """Command docstring becomes help text."""
    click.echo("Hello!")

if __name__ == "__main__":
    hello()
```

## Options

```python
@click.command()
@click.option("--name", "-n", default="World", help="Name to greet")
@click.option("--count", "-c", type=int, default=1, help="Repeat count")
@click.option("--verbose/--quiet", "-v/-q", default=False)
@click.option("--format", type=click.Choice(["json", "yaml", "text"]))
@click.option("--config", type=click.Path(exists=True))
@click.option("--output", type=click.File("w"), default="-")  # "-" = stdout
def cmd(name, count, verbose, format, config, output):
    pass
```

### Option Parameters

```python
@click.option(
    "--name", "-n",           # Long and short form
    default="value",          # Default value
    required=True,            # Must be provided
    type=str,                 # str, int, float, bool, click.Choice, etc.
    help="Description",       # Help text
    show_default=True,        # Show default in help
    envvar="MY_NAME",         # Read from env var
    prompt="Enter name",      # Prompt if not provided
    hide_input=True,          # For passwords
    confirmation_prompt=True, # Confirm password
    multiple=True,            # Allow multiple values (becomes tuple)
    nargs=2,                  # Exact number of values
    is_flag=True,             # Boolean flag
    flag_value="yes",         # Value when flag is set
    count=True,               # Count occurrences (-vvv = 3)
    hidden=True,              # Hide from help
    callback=validate_fn,     # Validation/transformation
)
```

### Types

```python
click.STRING                  # Default
click.INT                     
click.FLOAT
click.BOOL
click.UUID
click.Choice(["a", "b"])      # Limited choices
click.Path(exists=True, dir_okay=False, resolve_path=True)
click.File("r")               # Opens file handle
click.IntRange(0, 100)        # Bounded integer
click.FloatRange(0.0, 1.0)
click.DateTime(formats=["%Y-%m-%d"])
```

## Arguments

```python
@click.command()
@click.argument("filename")                          # Required positional
@click.argument("files", nargs=-1)                   # Variable number
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path())
def cmd(filename, files, src, dst):
    pass
```

## Command Groups

```python
@click.group()
@click.version_option(version="1.0.0", prog_name="mytool")
def cli():
    """Main CLI application."""
    pass

@cli.command()
def init():
    """Initialize project."""
    click.echo("Initialized!")

@cli.command("run")  # Custom command name
def run_cmd():
    """Run the application."""
    click.echo("Running...")

# Nested groups
@cli.group()
def db():
    """Database commands."""
    pass

@db.command()
def migrate():
    """Run migrations."""
    pass

if __name__ == "__main__":
    cli()
# Usage: mycli db migrate
```

## Context & State

```python
@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug

@cli.command()
@click.pass_context
def status(ctx):
    if ctx.obj["DEBUG"]:
        click.echo("Debug mode is on")

# Using pass_obj for simpler access
@cli.command()
@click.pass_obj
def status(obj):
    click.echo(f"Debug: {obj['DEBUG']}")
```

### Custom Object

```python
class Config:
    def __init__(self):
        self.verbose = False
        self.home = "."

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option("--verbose", is_flag=True)
@pass_config
def cli(config, verbose):
    config.verbose = verbose

@cli.command()
@pass_config
def show(config):
    click.echo(f"Verbose: {config.verbose}")
```

## Prompts & Confirmation

```python
# Basic prompt
name = click.prompt("Your name", default="Anonymous")

# Password
password = click.prompt("Password", hide_input=True, confirmation_prompt=True)

# Confirmation
if click.confirm("Do you want to continue?"):
    click.echo("Continuing...")

# Abort on no
if click.confirm("Delete everything?", abort=True):
    click.echo("Deleted!")
```

## Styled Output

```python
# Basic
click.echo("Plain text")

# Styled
click.secho("Error!", fg="red", bold=True)
click.secho("Success!", fg="green")
click.secho("Warning!", fg="yellow")
click.secho("Info!", fg="blue")
click.secho("Highlight", bg="cyan", fg="black")

# Style separately
styled = click.style("styled text", fg="red", bold=True)
click.echo(f"Some {styled} here")

# Colors: black, red, green, yellow, blue, magenta, cyan, white, reset
# Bright: bright_red, bright_green, etc.
# Attributes: bold, dim, underline, blink, reverse, reset
```

## Progress Bar

```python
with click.progressbar(items, label="Processing") as bar:
    for item in bar:
        process(item)

# With length
with click.progressbar(length=100, label="Downloading") as bar:
    for chunk in download():
        bar.update(len(chunk))

# Custom format
with click.progressbar(
    items,
    label="Working",
    show_eta=True,
    show_percent=True,
    show_pos=True,
    fill_char="█",
    empty_char="░",
) as bar:
    for item in bar:
        process(item)
```

## Utilities

```python
# Clear screen
click.clear()

# Pager for long output
click.echo_via_pager(long_text)

# Edit in external editor
message = click.edit("Initial content")

# Launch URL or file
click.launch("https://example.com")
click.launch("document.pdf")

# Get single character
char = click.getchar()

# Pause
click.pause("Press any key...")
```

## Callbacks & Validation

```python
def validate_positive(ctx, param, value):
    if value is not None and value < 0:
        raise click.BadParameter("Must be positive")
    return value

@click.command()
@click.option("--count", callback=validate_positive)
def cmd(count):
    pass

# Eager options (process before others)
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 1.0.0")
    ctx.exit()

@click.command()
@click.option("--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    pass
```

## Error Handling

```python
# Abort with error
raise click.Abort()

# Exit with message
raise click.ClickException("Something went wrong")

# Bad parameter
raise click.BadParameter("Invalid value", param_hint="--name")

# Usage error
raise click.UsageError("Missing required options")

# Exit codes
ctx.exit(1)  # Exit with code
```

## Entry Points (setup.py / pyproject.toml)

```python
# pyproject.toml
[project.scripts]
mytool = "mypackage.cli:cli"

# Or setup.py
entry_points={
    "console_scripts": [
        "mytool=mypackage.cli:cli",
    ],
}
```

## Testing

```python
from click.testing import CliRunner

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["--name", "Test"])
    assert result.exit_code == 0
    assert "Test" in result.output

# With input
result = runner.invoke(cli, input="yes\n")

# With environment
result = runner.invoke(cli, env={"MY_VAR": "value"})

# Isolated filesystem
with runner.isolated_filesystem():
    with open("test.txt", "w") as f:
        f.write("test")
    result = runner.invoke(cli, ["test.txt"])
```

## Command Chaining

```python
@click.group(chain=True)
def cli():
    pass

@cli.command()
def step1():
    click.echo("Step 1")

@cli.command()
def step2():
    click.echo("Step 2")

# Usage: mycli step1 step2
```

## Result Callbacks

```python
@click.group(chain=True, result_callback=process_pipeline)
def cli():
    pass

def process_pipeline(results):
    """Called after all chained commands complete."""
    for r in results:
        click.echo(f"Result: {r}")

@cli.command()
def cmd1():
    return "cmd1_result"
```
