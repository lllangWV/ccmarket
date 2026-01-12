---
name: cadquery
description: Create parametric 3D CAD models using CadQuery, a Python-based scripting CAD library. Use when creating 3D models, mechanical parts, enclosures, assemblies, or exporting to STL/STEP/DXF. Triggers on requests for 3D modeling, CAD design, bearing blocks, gears, enclosures, mechanical assemblies, or parametric parts.
---

# CadQuery 3D CAD Modeling

CadQuery is a Python library for building parametric 3D CAD models using a fluent API built on OpenCascade.

## Installation

```bash
pip install cadquery --break-system-packages
```

## Core Workflow

1. Create a Workplane on a reference plane (XY, XZ, YZ)
2. Draw 2D geometry (circles, rectangles, polygons)
3. Transform to 3D (extrude, revolve, sweep, loft)
4. Select features (faces, edges, vertices)
5. Add more features or modify (holes, fillets, chamfers)
6. Export result (STL, STEP, DXF)

## Quick Start Pattern

```python
import cadquery as cq

# Parametric dimensions
length, width, height = 80.0, 60.0, 10.0
hole_diameter = 22.0
padding = 12.0

# Build the model
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z").workplane()
    .hole(hole_diameter)
    .faces(">Z").workplane()
    .rect(length - padding, width - padding, forConstruction=True)
    .vertices()
    .cboreHole(2.4, 4.4, 2.1)
    .edges("|Z").fillet(2.0)
)

# Export
cq.exporters.export(result, "output.step")
cq.exporters.export(result, "output.stl")
```

## Workplanes

Workplanes define the 2D reference for drawing. Methods create new Workplanes in a chain.

```python
cq.Workplane("XY")  # Front plane (default)
cq.Workplane("XZ")  # Top plane
cq.Workplane("YZ")  # Side plane

# Create workplane on a face
.faces(">Z").workplane()           # On top face
.faces(">Z").workplane(offset=5.0) # Offset from face
```

## Selectors (Quick Reference)

Select geometry for operations. See [references/selectors.md](references/selectors.md) for complete guide.

| Selector | Description |
|----------|-------------|
| `>Z` | Farthest in +Z direction |
| `<Z` | Farthest in -Z direction |
| `\|Z` | Parallel to Z axis |
| `#Z` | Perpendicular to Z axis |
| `>XY` | Nearest to XY plane |

```python
.faces(">Z")      # Top face
.edges("|Z")      # Vertical edges
.vertices("<XY")  # Lower-left vertex
```

## Essential 2D Operations

```python
.circle(radius)
.rect(width, height)
.polygon(n_sides, diameter)
.slot2D(length, diameter)
.ellipse(x_radius, y_radius)
.polyline([(x1,y1), (x2,y2), ...])
.spline([(x1,y1), (x2,y2), ...])
.moveTo(x, y).lineTo(x2, y2).close()
```

## Essential 3D Operations

```python
.extrude(distance)              # Extrude 2D profile
.cut(other_solid)               # Boolean subtract
.union(other_solid)             # Boolean add
.intersect(other_solid)         # Boolean intersect
.hole(diameter, depth=None)     # Through or blind hole
.cboreHole(hole_d, cb_d, cb_h)  # Counterbore hole
.cskHole(hole_d, csk_d, angle)  # Countersink hole
.fillet(radius)                 # Round edges
.chamfer(distance)              # Bevel edges
.shell(thickness)               # Hollow out (-thickness for inward)
.loft()                         # Blend between profiles
.sweep(path)                    # Sweep along path
.revolve(angle)                 # Revolve around axis
```

## Common Patterns

### Holes at Rectangle Corners
```python
.faces(">Z").workplane()
.rect(60, 40, forConstruction=True)
.vertices()
.hole(5)
```

### Circular Pattern
```python
.faces(">Z").workplane()
.polarArray(radius=20, startAngle=0, angle=360, count=6)
.hole(3)
```

### Rectangular Array
```python
.faces(">Z").workplane()
.rarray(xSpacing=10, ySpacing=10, xCount=3, yCount=3)
.hole(2)
```

### Shell with Open Face
```python
.faces(">Z").shell(-2.0)  # Hollow, keeping top open
```

### Profile Extrusion
```python
(cq.Workplane("XY")
 .moveTo(0, 0)
 .lineTo(10, 0)
 .lineTo(10, 5)
 .threePointArc((5, 7), (0, 5))
 .close()
 .extrude(20))
```

## Exporting

```python
import cadquery as cq

# Export to various formats
cq.exporters.export(result, "model.step")  # CAD interchange
cq.exporters.export(result, "model.stl")   # 3D printing
cq.exporters.export(result.section(), "model.dxf")  # 2D drawing
```

## Context Solid Behavior

CadQuery automatically combines new features with the "context solid" (first solid created):
- `extrude()` adds to context solid by default
- `hole()`, `cutThruAll()` subtract from context solid
- Use `combine=False` to create separate solids

## Tagging for Complex Models

```python
result = (
    cq.Workplane("XY")
    .box(10, 10, 10)
    .faces(">Z").workplane().tag("top_plane")
    .circle(2).extrude(5)
    .workplaneFromTagged("top_plane")
    .center(3, 0).circle(1).extrude(3)
)
```

## Additional References

- **Selectors**: See [references/selectors.md](references/selectors.md) for complete selector syntax
- **Operations**: See [references/operations.md](references/operations.md) for all 2D/3D operations
- **Assemblies**: See [references/assemblies.md](references/assemblies.md) for multi-part assemblies
- **Examples**: See [references/examples.md](references/examples.md) for complete examples

## Script Template

Use this template when creating CadQuery models:

```python
import cadquery as cq

# === Parameters ===
# Define all dimensions as variables for parametric control

# === Build Model ===
result = (
    cq.Workplane("XY")
    # ... build geometry
)

# === Export ===
cq.exporters.export(result, "/mnt/user-data/outputs/model.step")
cq.exporters.export(result, "/mnt/user-data/outputs/model.stl")
```
