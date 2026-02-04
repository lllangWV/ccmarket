# CadQuery Assemblies

Combine multiple parts with positioning and constraints.

## Basic Assembly

```python
import cadquery as cq

part1 = cq.Workplane().box(10, 10, 5)
part2 = cq.Workplane().cylinder(10, 3)

assy = (
    cq.Assembly()
    .add(part1, name="base", color=cq.Color("gray"))
    .add(part2, name="cylinder",
         loc=cq.Location((0, 0, 7.5)),
         color=cq.Color("red"))
)

assy.save("assembly.step")
```

## Location

```python
# Translation only
loc = cq.Location((x, y, z))

# Rotation (axis, angle degrees)
loc = cq.Location((0, 0, 0), (0, 0, 1), 45)

# Combined
loc = cq.Location(cq.Vector(x, y, z), cq.Vector(0, 0, 1), angle)
```

## Colors

```python
cq.Color("red")
cq.Color("blue")
cq.Color("gray")
cq.Color(0, 0, 1, 0.5)  # RGBA (0-1)
```

## Constraint-Based

```python
part1 = (cq.Workplane().box(20, 20, 5)
         .faces(">Z").tag("top"))

part2 = (cq.Workplane().box(10, 10, 10)
         .faces("<Z").tag("bottom"))

assy = (
    cq.Assembly()
    .add(part1, name="base")
    .add(part2, name="block")
    .constrain("base?top", "block?bottom", "Plane")
    .solve()
)
```

## Constraint Types

### Point
```python
.constrain("part1@vertices@>Z", "part2@vertices@<Z", "Point")
.constrain("part1", "part2", "Point", param=5.0)  # 5mm offset
```

### Axis
```python
.constrain("part1@faces@>Z", "part2@faces@<Z", "Axis")
.constrain("p1@faces@>Z", "p2@faces@>Z", "Axis", param=0)  # Same dir
```

### Plane
Combines Point and Axis (faces touch):
```python
.constrain("part1@faces@>Z", "part2@faces@<Z", "Plane")
```

### PointInPlane
```python
.constrain("part1@vertices@>Z", "part2@faces@>Y", "PointInPlane")
```

### PointOnLine
```python
.constrain("sphere", "box@edges@>Z", "PointOnLine")
```

### Fixed
```python
.constrain("base", "Fixed")
.constrain("part", "FixedPoint", (0, 0, 0))
.constrain("part", "FixedRotation", (0, 0, 45))
.constrain("part@faces@>Z", "FixedAxis", (0, 0, 1))
```

## Constraint Syntax

```python
"partName@faces@>Z"       # Top face
"partName@edges@|Z"       # Vertical edges
"partName@vertices@<XY"   # Lower-left vertex
"partName?tagName"        # Tagged geometry
```

## Example

```python
import cadquery as cq

def make_base():
    return (cq.Workplane().box(50, 50, 10)
            .faces(">Z").workplane()
            .rect(30, 30, forConstruction=True)
            .vertices().hole(5))

def make_post():
    return cq.Workplane().cylinder(30, 4)

base = make_base()
post = make_post()

base.faces(">Z").tag("top")
post.faces("<Z").tag("bottom")

assy = (
    cq.Assembly()
    .add(base, name="base", color=cq.Color("gray"))
    .add(post, name="post1", color=cq.Color("red"))
    .add(post, name="post2", color=cq.Color("red"))
    .constrain("base?top", "post1?bottom", "Plane")
    .constrain("base@vertices@>X and >Y", "post1", "Point")
    .constrain("base?top", "post2?bottom", "Plane")
    .constrain("base@vertices@<X and >Y", "post2", "Point")
    .solve()
)

assy.save("posts.step")
```

## Export

```python
assy.save("output.step")
assy.save("output.xml")  # OCCT XML
```
