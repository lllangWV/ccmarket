# Shebang Scripts Reference

Run scripts with pixi-managed dependencies without explicit environment setup.

**Note:** Only available on Unix-like systems (Linux and macOS). Windows does not support shebang lines.

## Basic Syntax

```
#!/usr/bin/env -S pixi exec --spec <package> -- <interpreter>
```

Components:
- `#!/usr/bin/env -S` - Locates pixi in PATH; `-S` treats remaining args as command
- `--spec <package>` - Declares inline dependencies (repeatable)
- `--` - Separates pixi options from the interpreter command

## Python Scripts

### Simple script

```python
#!/usr/bin/env -S pixi exec --spec python -- python
print("Hello from pixi!")
```

### With dependencies

```python
#!/usr/bin/env -S pixi exec --spec python --spec requests -- python
import requests
response = requests.get("https://api.github.com")
print(response.status_code)
```

### With version constraints

```python
#!/usr/bin/env -S pixi exec --spec python>=3.11 --spec numpy>=1.26,<2.0 -- python
import numpy as np
print(np.__version__)
```

### Multiple packages

```python
#!/usr/bin/env -S pixi exec --spec py-rattler>=0.10.0,<0.11 --spec typer>=0.15.0,<0.16 -- python
import rattler
import typer

app = typer.Typer()

@app.command()
def main():
    print("Running with pixi shebang!")

if __name__ == "__main__":
    app()
```

## Bash Scripts

### With tools

```bash
#!/usr/bin/env -S pixi exec --spec bat -- bash -e
bat my-file.json
```

### With multiple tools

```bash
#!/usr/bin/env -S pixi exec --spec ripgrep --spec fd-find -- bash -e
fd "\.py$" | xargs rg "import"
```

## R Scripts

```r
#!/usr/bin/env -S pixi exec --spec r-base --spec r-ggplot2 -- Rscript
library(ggplot2)
print("R with ggplot2!")
```

## Usage

1. Create the script with shebang header
2. Make it executable:
   ```bash
   chmod +x myscript.py
   ```
3. Run directly:
   ```bash
   ./myscript.py
   ```

## How It Works

When you execute `./script.py`:

1. System reads the shebang line
2. Invokes `pixi exec` with specified packages
3. Pixi creates a temporary environment with dependencies
4. Runs the interpreter with your script in that environment
5. Environment is cached for faster subsequent runs

## Channel Specification

Use `--channel` to specify package sources:

```python
#!/usr/bin/env -S pixi exec --channel conda-forge --spec python --spec pandas -- python
import pandas as pd
print(pd.__version__)
```

## Tips

- Keep shebang lines readable by limiting dependencies
- For complex dependency sets, consider a full pixi project instead
- Version constraints help ensure reproducibility
- The temporary environment is cached, so repeated runs are fast
- Use `pixi exec` directly for one-off commands without creating scripts
