# CadQuery Selectors

Select geometry (faces, edges, vertices) for operations.

## Methods

```python
.faces(sel)      # Select faces
.edges(sel)      # Select edges
.vertices(sel)   # Select vertices
.wires(sel)      # Select wires
.solids(sel)     # Select solids
```

## Axis Direction

| Selector | Description |
|----------|-------------|
| `>X` | Max X (rightmost) |
| `<X` | Min X (leftmost) |
| `>Y` | Max Y (back) |
| `<Y` | Min Y (front) |
| `>Z` | Max Z (top) |
| `<Z` | Min Z (bottom) |

## Parallel/Perpendicular

| Selector | Description |
|----------|-------------|
| `\|X` | Parallel to X |
| `\|Y` | Parallel to Y |
| `\|Z` | Parallel to Z |
| `#X` | Perpendicular to X |
| `#Y` | Perpendicular to Y |
| `#Z` | Perpendicular to Z |

## Plane Distance

| Selector | Description |
|----------|-------------|
| `>XY` | Nearest to XY plane |
| `<XY` | Farthest from XY |
| `>XZ` | Nearest to XZ plane |
| `>YZ` | Nearest to YZ plane |

## Nth Selection

```python
.faces(">Z[0]")   # First top face
.faces(">Z[1]")   # Second top face
.edges("|Z[-1]")  # Last vertical edge
```

## Center of Mass

```python
.faces(">>Z")  # Face with center highest in Z
.edges(">>X")  # Edge with center highest in X
```

## Type Filters

```python
.edges("%Circle")    # Circular edges
.edges("%Line")      # Linear edges
.faces("%Plane")     # Planar faces
.faces("%Cylinder")  # Cylindrical faces
```

## Boolean

```python
.edges("|Z and >Y")    # Vertical edges at back
.faces(">Z or <Z")     # Top or bottom
.edges("not |Z")       # Non-vertical edges
```

## Tagged Selection

```python
result = (
    cq.Workplane("XY")
    .box(10, 10, 10)
    .tag("box")
    .sphere(8)
    .faces(">Z", tag="box")  # From tagged state
    .workplane()
    .hole(2)
)
```

## Examples

```python
.faces(">Z")                    # Top face
.edges("|Z").fillet(1.0)        # Round vertical edges
.faces(">Z").edges()            # Edges on top face
.vertices("<X and <Y")          # Lower-left vertex
.edges("%Circle").chamfer(0.5)  # Chamfer circular edges
.faces(">Z[1]")                 # Second-highest face
```
