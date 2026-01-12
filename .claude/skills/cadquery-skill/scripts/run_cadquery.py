#!/usr/bin/env python3
"""
CadQuery model runner and exporter.

Usage:
    python run_cadquery.py <model_script.py> [output_dir]

This script:
1. Runs the CadQuery model script
2. Exports the result to STEP and STL formats
3. Reports any errors

The model script should define a variable named 'result' containing the final model.
"""

import sys
import os
from pathlib import Path


def run_model(script_path: str, output_dir: str = None):
    """Run a CadQuery model script and export results."""
    try:
        import cadquery as cq
    except ImportError:
        print("Error: cadquery not installed. Run: pip install cadquery-ocp --break-system-packages")
        sys.exit(1)

    script_path = Path(script_path)
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Set output directory
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = Path("/mnt/user-data/outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Read and execute the script
    script_content = script_path.read_text()
    
    # Create execution namespace with cadquery imported
    namespace = {"cq": cq, "__name__": "__main__"}
    
    try:
        exec(script_content, namespace)
    except Exception as e:
        print(f"Error executing script: {e}")
        sys.exit(1)

    # Find the result
    result = namespace.get("result")
    if result is None:
        print("Error: Script must define a 'result' variable with the CadQuery model")
        sys.exit(1)

    # Export
    base_name = script_path.stem
    
    step_path = out_dir / f"{base_name}.step"
    stl_path = out_dir / f"{base_name}.stl"
    
    try:
        cq.exporters.export(result, str(step_path))
        print(f"Exported: {step_path}")
    except Exception as e:
        print(f"Warning: Could not export STEP: {e}")

    try:
        cq.exporters.export(result, str(stl_path))
        print(f"Exported: {stl_path}")
    except Exception as e:
        print(f"Warning: Could not export STL: {e}")

    print("Done!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    script = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    run_model(script, output)
