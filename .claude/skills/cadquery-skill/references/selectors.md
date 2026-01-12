# CadQuery Selectors Reference

Selectors filter geometry (faces, edges, vertices) for subsequent operations.

## Selector Methods

```python
.faces(selector)     # Select faces
.edges(selector)     # Select edges
.vertices(selector)  # Select vertices
.wires(selector)     # Select wires
.solids(selector)    # Select solids
```

## Axis Selectors

| Selector | Description |
|----------|-------------|
| `>X` | Maximum X (rightmost) |
| `<X` | Minimum X (leftmost) |
| `>Y` | Maximum Y (back) |
| `<Y` | Minimum Y (front) |
| `>Z` | Maximum Z (top) |
| `<Z` | Minimum Z (bottom) |

## Parallel/Perpendicular

| Selector | Description |
|----------|-------------|
| `\|X` | Parallel to X axis |
| `\|Y` | Parallel to Y axis |
| `\|Z` | Parallel to Z axis |
| `#X` | Perpendicular to X axis |
| `#Y` | Perpendicular to Y axis |
| `#Z` | Perpendicular to Z axis |

## Distance Selectors

| Selector | Description |
|----------|-------------|
| `>XY` | Nearest to XY plane |
| `<XY` | Farthest from XY plane |
| `>XZ` | Nearest to XZ plane |
| `<XZ` | Farthest from XZ plane |
| `>YZ` | Nearest to YZ plane |
| `<YZ` | Farthest from YZ plane |

## Nth Selection

Select the nth item when multiple match:

```python
.faces(">Z[0]")  # First top face
.faces(">Z[1]")  # Second top face
.edges("|Z[-1]") # Last vertical edge
```

## Center of Mass Selectors

Use `>>` for selection by center of mass:

```python
.faces(">>Z")    # Face with center highest in Z
.edges(">>X")    # Edge with center highest in X
```

## Type Selectors

Filter by geometry type:

```python
.edges("%Circle")    # Circular edges
.edges("%Line")      # Linear edges
.faces("%Plane")     # Planar faces
.faces("%Cylinder")  # Cylindrical faces
.faces("%Sphere")    # Spherical faces
```

## Boolean Combinations

Combine selectors with `and`, `or`, `not`:

```python
.edges("|Z and >Y")       # Vertical edges at back
.faces(">Z or <Z")        # Top or bottom face
.edges("not |Z")          # Non-vertical edges
.faces(">Z and #X")       # Top face perpendicular to X
```

## Tagged Selection

Use tags to select from earlier states:

```python
result = (
    cq.Workplane("XY")
    .box(10, 10, 10)
    .tag("box")
    .sphere(8)
    .faces(">Z", tag="box")  # Select from tagged state
    .workplane()
    .hole(2)
)
```

## Selector Examples

```python
# Select top face
.faces(">Z")

# Select all vertical edges for filleting
.edges("|Z").fillet(1.0)

# Select edges on top face
.faces(">Z").edges()

# Select lower-left vertex
.vertices("<X and <Y")

# Select circular edges for chamfer
.edges("%Circle").chamfer(0.5)

# Select front and back faces
.faces("|Y")

# Select second-highest face
.faces(">Z[1]")
```
