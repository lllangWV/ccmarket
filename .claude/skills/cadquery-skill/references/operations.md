# CadQuery Operations Reference

## 2D Drawing Operations

### Basic Shapes

```python
.circle(radius)
.rect(width, height)
.polygon(nSides, diameter)
.ellipse(xRadius, yRadius)
.slot2D(length, diameter, angle=0)
```

### Lines and Arcs

```python
.moveTo(x, y)                    # Move without drawing
.lineTo(x, y)                    # Line to absolute position
.line(dx, dy)                    # Line by offset
.hLine(distance)                 # Horizontal line
.vLine(distance)                 # Vertical line
.hLineTo(x)                      # Horizontal to X coordinate
.vLineTo(y)                      # Vertical to Y coordinate
.threePointArc((x1,y1), (x2,y2)) # Arc through 3 points
.tangentArcPoint((x, y))         # Tangent arc to point
.radiusArc((x, y), radius)       # Arc with given radius
.close()                         # Close the path
```

### Splines and Polylines

```python
.spline(points, includeCurrent=False)
.polyline(points)
```

### Construction Geometry

```python
.rect(w, h, forConstruction=True)  # Reference rectangle
.circle(r, forConstruction=True)   # Reference circle
```

### Positioning

```python
.center(x, y)          # Shift workplane center
.pushPoints([(x,y)...]) # Add points to stack
```

### Arrays

```python
.rarray(xSpacing, ySpacing, xCount, yCount)  # Rectangular array
.polarArray(radius, startAngle, angle, count) # Circular array
```

## 3D Operations

### Extrusion

```python
.extrude(distance)                    # Basic extrude
.extrude(distance, combine=True)      # Combine with context
.extrude(distance, taper=10)          # Tapered extrude
.extrude("next")                      # Extrude to next face
.extrude("last")                      # Extrude to last face
```

### Holes

```python
.hole(diameter)                       # Through hole
.hole(diameter, depth)                # Blind hole
.cboreHole(holeDia, cboreDia, cboreDepth)  # Counterbore
.cskHole(holeDia, cskDia, cskAngle)   # Countersink
```

### Cutting

```python
.cutThruAll()                         # Cut through entire part
.cutBlind(depth)                      # Cut to depth
.cutBlind("next")                     # Cut to next face
.cut(otherSolid)                      # Boolean subtract
```

### Boolean Operations

```python
.union(otherSolid)                    # Boolean add
.intersect(otherSolid)                # Boolean intersect
.cut(otherSolid)                      # Boolean subtract
```

### Edge/Face Modifications

```python
.fillet(radius)                       # Round edges
.chamfer(distance)                    # Bevel edges
.chamfer(length, angle)               # Angled chamfer
.shell(thickness)                     # Hollow solid
.shell(-thickness)                    # Shell inward
.faces(">Z").shell(thickness)         # Shell with open face
```

### Sweep Operations

```python
.sweep(path)                          # Sweep along path
.sweep(path, multisection=True)       # Multi-section sweep
.twistExtrude(distance, angle)        # Twisted extrude
```

### Loft

```python
# Loft between profiles
result = (
    cq.Workplane("XY")
    .rect(10, 10)
    .workplane(offset=10)
    .circle(5)
    .loft()
)
```

### Revolve

```python
.revolve(angleDegrees)                       # Full/partial revolve
.revolve(angleDegrees, axisStart, axisEnd)   # Custom axis
```

### Primitives

```python
.box(length, width, height)           # Rectangular box
.sphere(radius)                       # Sphere at origin
.cylinder(height, radius)             # Cylinder
.cone(height, radius1, radius2)       # Cone/frustum
```

### Transformations

```python
.translate((dx, dy, dz))              # Move
.rotate((0,0,0), (0,0,1), angle)      # Rotate around axis
.rotateAboutCenter((1,0,0), angle)    # Rotate about center
.mirror("XY")                         # Mirror about plane
.mirrorX()                            # Mirror about YZ plane
.mirrorY()                            # Mirror about XZ plane
```

### Splitting

```python
.split(keepTop=True, keepBottom=False)  # Split solid
```

### Offset

```python
.offset2D(distance)                   # Offset 2D wire
.offset2D(distance, "arc")            # Arc-style corners
.offset2D(distance, "intersection")   # Sharp corners
```

## Workplane Operations

```python
.workplane()                          # New workplane on selection
.workplane(offset=5.0)                # Offset workplane
.workplane(centerOption="CenterOfMass") # Center on mass
.transformed(rotate=(45, 0, 0))       # Rotated workplane
.copyWorkplane(otherWorkplane)        # Copy from another
```

## Stack Operations

```python
.first()                              # Select first item
.last()                               # Select last item
.item(n)                              # Select nth item
.end()                                # Go back in chain
.all()                                # Return all solids as list
.val()                                # Get single underlying shape
.vals()                               # Get all underlying shapes
```
