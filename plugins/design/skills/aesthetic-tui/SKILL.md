---
name: aesthetic-tui
description: Design beautiful, aesthetic terminal user interfaces (TUIs) and command-line applications using Rich and Click. Use when building CLI tools with styled output, progress bars, tables, panels, syntax highlighting, interactive prompts, command groups, or when integrating Rich with Click for polished help pages.
---

# Aesthetic TUI Design

Build professional terminal applications using **Rich** (styling, formatting) and **Click** (CLI structure).

## Quick Decision Guide

| Need | Solution |
|------|----------|
| Styled text output | `rich.console.Console` + markup |
| Progress tracking | `rich.progress.track()` or `Progress` |
| Tabular data | `rich.table.Table` |
| Boxed content | `rich.panel.Panel` |
| CLI commands/options | `click.command()`, `click.option()` |
| Command groups | `click.group()` |
| Rich + Click integration | `import rich_click as click` |

## Installation

```bash
pip install rich click rich-click --break-system-packages
```

## Core Patterns

### 1. Rich Console - The Foundation

```python
from rich.console import Console

console = Console()

# Styled output
console.print("Hello [bold magenta]World[/bold magenta]!")
console.print("Status: [green]OK[/green] | Errors: [red]3[/red]")

# Logging with timestamps
console.log("Processing started", log_locals=True)

# Dividers
console.rule("[bold blue]Section Header")
```

### 2. Inline Markup

```python
# Colors: red, green, yellow, blue, cyan, magenta, white
"[red]Error[/red]", "[green]Success[/green]", "[yellow]Warning[/yellow]"

# Styles: bold, italic, underline, strike
"[bold red]Critical![/bold red]", "[italic cyan]Note[/italic cyan]"

# Emojis
console.print(":rocket: Launch :white_check_mark: Done!")
```

### 3. Tables

```python
from rich.table import Table

table = Table(title="Report", show_header=True, header_style="bold cyan")
table.add_column("Name", style="cyan")
table.add_column("Status", justify="center")
table.add_row("Alice", "[green]✓ Active[/green]")
table.add_row("Bob", "[red]✗ Inactive[/red]")
console.print(table)
```

### 4. Panels

```python
from rich.panel import Panel

console.print(Panel("Content", title="Title", border_style="blue"))
console.print(Panel.fit("[bold]Compact[/bold]", border_style="green"))
```

### 5. Progress Bars

```python
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn

# Simple
for item in track(range(100), description="Processing..."):
    process(item)

# Multi-task
with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn()) as progress:
    task = progress.add_task("[cyan]Working...", total=100)
    while not progress.finished:
        progress.update(task, advance=1)
```

### 6. Status Spinners

```python
with console.status("[bold green]Working...") as status:
    do_work()
    status.update("[bold blue]Almost done...")
```

### 7. Click CLI

```python
import click

@click.group()
@click.version_option()
def cli():
    """My CLI tool."""

@cli.command()
@click.option("--name", "-n", required=True, help="Your name")
@click.option("--loud/--quiet", default=False)
def greet(name, loud):
    """Greet someone."""
    msg = f"Hello, {name}!" if not loud else f"HELLO, {name.upper()}!"
    click.echo(msg)

if __name__ == "__main__":
    cli()
```

### 8. Rich + Click (rich-click)

```python
import rich_click as click
from rich.console import Console
from rich.panel import Panel

click.rich_click.USE_RICH_MARKUP = True

@click.command()
@click.option("--config", "-c", help="Path to [bold]config[/bold]")
def run(config):
    """Run with [green]style[/green]."""
    Console().print(Panel.fit(f"Config: {config}"))
```

### 9. Prompts

```python
# Click
name = click.prompt("Name", default="User")
password = click.prompt("Password", hide_input=True)
proceed = click.confirm("Continue?")

# Rich (more styling)
from rich.prompt import Prompt, Confirm
name = Prompt.ask("[cyan]Name[/cyan]", default="User")
proceed = Confirm.ask("[yellow]Continue?[/yellow]")
```

## Reference Files

- **[references/rich-components.md](references/rich-components.md)**: Tables, panels, layouts, syntax, trees, columns
- **[references/click-patterns.md](references/click-patterns.md)**: Commands, groups, options, context, callbacks

## Design Principles

1. **Color hierarchy**: cyan=info, green=success, yellow=warn, red=error
2. **Use panels** to group related content
3. **Spinners** for unknown duration, **progress bars** when measurable
4. **Always confirm** user actions with styled feedback
5. **Clear help text** for all options and commands
