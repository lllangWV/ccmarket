#!/usr/bin/env python3
"""
Example: Aesthetic TUI Application
Demonstrates combining Rich and Click for a beautiful CLI.
"""

import rich_click as click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Confirm
from rich import box
import time

# Configure rich-click
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_ARGUMENT = "bold yellow"

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="mytool")
@click.option("--verbose", "-v", is_flag=True, help="Enable [bold]verbose[/bold] output")
@click.pass_context
def cli(ctx, verbose):
    """
    [bold cyan]MyTool[/bold cyan] - An aesthetic CLI application.
    
    Build beautiful terminal interfaces with [green]Rich[/green] and [blue]Click[/blue].
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
@click.argument("name")
@click.option("--style", "-s", type=click.Choice(["minimal", "fancy", "compact"]), default="fancy")
@click.pass_context
def greet(ctx, name, style):
    """Greet someone with [green]style[/green]."""
    if style == "fancy":
        console.print(Panel.fit(
            f"[bold cyan]Hello, {name}![/bold cyan]\n[dim]Welcome to the aesthetic TUI[/dim]",
            title="[bold green]✨ Greeting ✨[/bold green]",
            border_style="cyan",
            padding=(1, 4),
        ))
    elif style == "compact":
        console.print(f"[bold green]→[/bold green] Hello, [cyan]{name}[/cyan]!")
    else:
        console.print(f"Hello, {name}!")
    
    if ctx.obj["verbose"]:
        console.print("[dim]Verbose: Greeting completed successfully[/dim]")


@cli.command()
@click.option("--format", "-f", type=click.Choice(["table", "list"]), default="table")
def status(format):
    """Show system [yellow]status[/yellow] information."""
    data = [
        ("Database", "Connected", "green"),
        ("Cache", "Active", "green"),
        ("API", "Healthy", "green"),
        ("Queue", "3 pending", "yellow"),
        ("Storage", "87% used", "yellow"),
    ]
    
    if format == "table":
        table = Table(
            title="[bold]System Status[/bold]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center")
        table.add_column("Health", justify="center")
        
        for service, status, color in data:
            icon = "●" if color == "green" else "◐" if color == "yellow" else "○"
            table.add_row(
                service,
                status,
                f"[{color}]{icon}[/{color}]"
            )
        console.print(table)
    else:
        for service, status, color in data:
            icon = "✓" if color == "green" else "!" if color == "yellow" else "✗"
            console.print(f"[{color}]{icon}[/{color}] [bold]{service}:[/bold] {status}")


@cli.command()
@click.argument("task_name")
@click.option("--steps", "-n", default=10, help="Number of [bold]steps[/bold] to simulate")
def run(task_name, steps):
    """Run a simulated [magenta]task[/magenta] with progress."""
    
    console.print(Panel.fit(
        f"[bold]Starting:[/bold] {task_name}",
        border_style="blue"
    ))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]{task_name}[/cyan]", total=steps)
        
        for i in range(steps):
            time.sleep(0.2)
            progress.update(task, advance=1)
    
    console.print(f"\n[bold green]✓[/bold green] Task [cyan]{task_name}[/cyan] completed!")


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
def reset(force):
    """[red]Reset[/red] all settings to defaults."""
    
    if not force:
        console.print(Panel(
            "[bold red]⚠ Warning[/bold red]\n\n"
            "This will reset all settings to their defaults.\n"
            "This action cannot be undone.",
            title="[bold]Confirmation Required[/bold]",
            border_style="red",
        ))
        
        if not Confirm.ask("[yellow]Are you sure you want to continue?[/yellow]"):
            console.print("[dim]Operation cancelled.[/dim]")
            return
    
    with console.status("[bold red]Resetting...[/bold red]"):
        time.sleep(1)
    
    console.print("[bold green]✓[/bold green] Settings have been reset to defaults.")


@cli.group()
def config():
    """Manage [blue]configuration[/blue] settings."""
    pass


@config.command("show")
def config_show():
    """Display current configuration."""
    table = Table(
        title="[bold]Configuration[/bold]",
        box=box.SIMPLE,
        show_header=True,
        header_style="bold blue",
    )
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Source", style="dim")
    
    settings = [
        ("debug", "false", "default"),
        ("log_level", "INFO", "config.yaml"),
        ("api_url", "https://api.example.com", "environment"),
        ("timeout", "30", "default"),
    ]
    
    for key, value, source in settings:
        table.add_row(key, value, source)
    
    console.print(table)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a configuration value."""
    console.print(f"[bold green]✓[/bold green] Set [cyan]{key}[/cyan] = [green]{value}[/green]")


if __name__ == "__main__":
    cli()
