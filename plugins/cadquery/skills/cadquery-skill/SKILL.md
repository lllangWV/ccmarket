---
name: cadquery
description: Use when creating 3D CAD models, mechanical parts, enclosures, or assemblies in Python. Triggers on parametric modeling, STEP/STL export, bearing blocks, gears, mounting plates.
---

# CadQuery 3D CAD Modeling

Python library for parametric 3D CAD using a fluent API on OpenCascade.

## Core Pattern

```python
import cadquery as cq

# Parameters at top
length, width, height = 80.0, 60.0, 10.0

# Build with fluent chain
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z").workplane()
    .hole(22.0)
    .edges("|Z").fillet(2.0)
)

# Export
cq.exporters.export(result, "model.step")
cq.exporters.export(result, "model.stl")
```

## Selectors Quick Reference

| Selector | Meaning |
|----------|---------|
| `>Z` | Max Z (top) |
| `<Z` | Min Z (bottom) |
| `\|Z` | Parallel to Z |
| `#Z` | Perpendicular to Z |
| `>Z[1]` | Second-highest Z |
| `%Circle` | Circular edges |

**Boolean:** `">Z and |X"`, `">Z or <Z"`, `"not |Z"`

## Key Operations

```python
# 2D
.circle(r), .rect(w, h), .polygon(n, d)
.moveTo(x, y).lineTo(x, y).close()

# 3D
.extrude(d), .hole(d), .cut(solid)
.cboreHole(hole_d, cb_d, cb_depth)
.fillet(r), .chamfer(d), .shell(-t)
.loft(), .sweep(path), .revolve(angle)
.cutThruAll(), .cutBlind(depth)

# Arrays
.rarray(xSp, ySp, xN, yN)
.polarArray(r, start, angle, count)
```

## Common Patterns

**Holes at corners:**
```python
.faces(">Z").workplane()
.rect(60, 40, forConstruction=True)
.vertices()
.hole(5)
```

**Shelled box:**
```python
.box(100, 80, 50)
.faces(">Z").shell(-2.0)
```

**Loft (square to circle):**
```python
cq.Workplane("XY")
.rect(40, 40)
.workplane(offset=50)
.circle(15)
.loft()
```

## Assemblies

```python
part1 = cq.Workplane().box(50, 50, 10)
part2 = cq.Workplane().cylinder(30, 5)

assy = (
    cq.Assembly()
    .add(part1, name="base", color=cq.Color("gray"))
    .add(part2, name="post", loc=cq.Location((0, 0, 20)))
)
assy.save("assembly.step")
```

**Constraint-based:**
```python
.constrain("base@faces@>Z", "post@faces@<Z", "Plane")
.solve()
```

## References

See `references/` for complete API:
- `selectors.md` - Full selector syntax
- `operations.md` - All 2D/3D operations
- `assemblies.md` - Assembly constraints
- `examples.md` - Complete examples
