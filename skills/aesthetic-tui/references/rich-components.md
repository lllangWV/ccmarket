# Rich Components Reference

Detailed API patterns for Rich library components.

## Console

```python
from rich.console import Console

console = Console()

# Output methods
console.print("Text", style="bold red")           # Styled print
console.log("Message", log_locals=True)           # With timestamp + locals
console.out("Raw output", highlight=False)        # No formatting
console.rule("Section", style="blue")             # Horizontal rule
console.clear()                                    # Clear screen

# Export
console.save_html("output.html")
console.save_svg("output.svg", title="My Output")
console.save_text("output.txt")
```

## Tables

```python
from rich.table import Table
from rich import box

table = Table(
    title="Title",
    caption="Caption",
    show_header=True,
    header_style="bold magenta",
    show_lines=False,          # Row separators
    expand=False,              # Fill width
    box=box.ROUNDED,           # Border style: MINIMAL, SIMPLE, DOUBLE, etc.
    padding=(0, 1),            # (top/bottom, left/right)
)

table.add_column("Col1", 
    style="cyan",
    justify="left",            # left, center, right
    no_wrap=True,
    width=20,
    ratio=1,                   # Relative width
)

table.add_row("Cell1", "Cell2", style="dim")  # Row style
table.add_row("Cell3", "Cell4", end_section=True)  # Add line after
```

### Box Styles
```python
from rich import box
# box.ASCII, box.SQUARE, box.ROUNDED, box.MINIMAL, box.SIMPLE
# box.HEAVY, box.DOUBLE, box.MARKDOWN
```

## Panels

```python
from rich.panel import Panel

Panel(
    "Content",
    title="Title",
    subtitle="Subtitle",
    title_align="left",        # left, center, right
    border_style="blue",
    box=box.ROUNDED,
    padding=(1, 2),            # (vertical, horizontal)
    expand=True,
)

Panel.fit("Content")           # Shrink to content
```

## Progress

```python
from rich.progress import (
    Progress, track,
    SpinnerColumn, BarColumn, TextColumn,
    TimeElapsedColumn, TimeRemainingColumn,
    MofNCompleteColumn, TaskProgressColumn,
    FileSizeColumn, TransferSpeedColumn,
)

# Simple iteration
for item in track(items, description="Working..."):
    process(item)

# Advanced
with Progress(
    SpinnerColumn(spinner_name="dots"),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(bar_width=40),
    TaskProgressColumn(),
    TimeRemainingColumn(),
    transient=True,            # Clear on exit
) as progress:
    task = progress.add_task("[cyan]Task", total=100, start=True)
    progress.update(task, advance=10, description="New desc")
    progress.remove_task(task)
```

### Spinner Names
`dots`, `line`, `pipe`, `simpleDots`, `star`, `growVertical`, `bounce`, `arc`, `circle`, `moon`

## Syntax Highlighting

```python
from rich.syntax import Syntax

code = '''
def hello(name):
    print(f"Hello, {name}!")
'''

syntax = Syntax(
    code, 
    "python",
    theme="monokai",           # dracula, github-dark, one-dark, etc.
    line_numbers=True,
    start_line=1,
    highlight_lines={2},       # Highlight specific lines
    word_wrap=True,
)
console.print(syntax)

# From file
syntax = Syntax.from_path("script.py", theme="monokai")
```

## Markdown

```python
from rich.markdown import Markdown

md = Markdown("""
# Header
Some **bold** and *italic* text.
- List item 1
- List item 2

```python
print("code block")
```
""")
console.print(md)
```

## Tree

```python
from rich.tree import Tree

tree = Tree("[bold]Root")
branch = tree.add("[green]Branch 1")
branch.add("Leaf 1")
branch.add("Leaf 2")
tree.add("[blue]Branch 2").add("Leaf 3")

console.print(tree)
```

## Columns

```python
from rich.columns import Columns
from rich.panel import Panel

items = [Panel(f"Item {i}", expand=True) for i in range(6)]
console.print(Columns(items, equal=True, expand=True))
```

## Layout

```python
from rich.layout import Layout

layout = Layout()
layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="footer", size=3),
)
layout["body"].split_row(
    Layout(name="left"),
    Layout(name="right", ratio=2),
)
layout["header"].update(Panel("Header"))
layout["left"].update(Panel("Sidebar"))
layout["right"].update(Panel("Content"))

console.print(layout)
```

## Live Display

```python
from rich.live import Live
from rich.table import Table
import time

def generate_table() -> Table:
    table = Table()
    table.add_column("Time")
    table.add_row(str(time.time()))
    return table

with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(10):
        time.sleep(0.4)
        live.update(generate_table())
```

## JSON

```python
from rich.json import JSON

console.print(JSON('{"name": "Alice", "age": 30}'))
# Or from dict
console.print_json(data={"name": "Alice"})
```

## Padding

```python
from rich.padding import Padding

padded = Padding("Content", (2, 4))  # (top/bottom, left/right)
padded = Padding("Content", (1, 2, 3, 4))  # (top, right, bottom, left)
```

## Text

```python
from rich.text import Text

text = Text()
text.append("Hello ", style="bold")
text.append("World", style="red")
text.highlight_words(["World"], style="underline")
console.print(text)
```

## Styled Tracebacks

```python
from rich.traceback import install

install(show_locals=True)  # Call at program start

# Or manually
from rich.console import Console
console = Console()
try:
    1/0
except:
    console.print_exception(show_locals=True)
```

## Logging Integration

```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")
log.info("This is [bold]formatted[/bold]", extra={"markup": True})
```

## Color Reference

### Named Colors
`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
Bright: `bright_red`, `bright_green`, etc.

### Custom Colors
```python
"[#ff5733]Hex color[/#ff5733]"
"[rgb(255,87,51)]RGB color[/rgb(255,87,51)]"
"[color(208)]256-color[/color(208)]"
```

### Background
```python
"[on red]Red background[/on red]"
"[white on blue]White text, blue bg[/white on blue]"
```
