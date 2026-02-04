# CadQuery Operations

## 2D Drawing

### Basic Shapes
```python
.circle(radius)
.rect(width, height)
.polygon(nSides, diameter)
.ellipse(xRadius, yRadius)
.slot2D(length, diameter, angle=0)
```

### Lines/Arcs
```python
.moveTo(x, y)                     # Move without drawing
.lineTo(x, y)                     # Line to absolute
.line(dx, dy)                     # Line by offset
.hLine(d), .vLine(d)              # Horizontal/vertical
.hLineTo(x), .vLineTo(y)          # To coordinate
.threePointArc((x1,y1), (x2,y2))  # Arc through 3 points
.tangentArcPoint((x, y))          # Tangent arc
.radiusArc((x, y), radius)        # Arc with radius
.close()                          # Close path
```

### Splines
```python
.spline(points, includeCurrent=False)
.polyline(points)
```

### Construction
```python
.rect(w, h, forConstruction=True)   # Reference rect
.circle(r, forConstruction=True)    # Reference circle
```

### Positioning
```python
.center(x, y)             # Shift workplane center
.pushPoints([(x,y)...])   # Add points to stack
```

### Arrays
```python
.rarray(xSpacing, ySpacing, xCount, yCount)
.polarArray(radius, startAngle, angle, count)
```

## 3D Operations

### Extrusion
```python
.extrude(distance)
.extrude(distance, taper=10)       # Tapered
.extrude("next")                   # To next face
.extrude("last")                   # To last face
```

### Holes
```python
.hole(diameter)                           # Through hole
.hole(diameter, depth)                    # Blind hole
.cboreHole(holeDia, cboreDia, cboreDepth) # Counterbore
.cskHole(holeDia, cskDia, cskAngle)       # Countersink
```

### Cutting
```python
.cutThruAll()              # Cut through part
.cutBlind(depth)           # Cut to depth
.cutBlind("next")          # Cut to next face
.cut(otherSolid)           # Boolean subtract
```

### Boolean
```python
.union(otherSolid)
.intersect(otherSolid)
.cut(otherSolid)
```

### Edge/Face Mods
```python
.fillet(radius)               # Round edges
.chamfer(distance)            # Bevel edges
.chamfer(length, angle)       # Angled chamfer
.shell(thickness)             # Hollow solid
.shell(-thickness)            # Shell inward
.faces(">Z").shell(t)         # Shell with open face
```

### Sweep/Loft
```python
.sweep(path)
.sweep(path, multisection=True)
.twistExtrude(distance, angle)
.loft()
```

### Revolve
```python
.revolve(angleDegrees)
.revolve(angleDegrees, axisStart, axisEnd)
```

### Primitives
```python
.box(length, width, height)
.sphere(radius)
.cylinder(height, radius)
.cone(height, radius1, radius2)
```

### Transform
```python
.translate((dx, dy, dz))
.rotate((0,0,0), (0,0,1), angle)
.rotateAboutCenter((1,0,0), angle)
.mirror("XY")
.mirrorX(), .mirrorY()
```

### Split
```python
.split(keepTop=True, keepBottom=False)
```

### Offset
```python
.offset2D(distance)
.offset2D(distance, "arc")           # Arc corners
.offset2D(distance, "intersection")  # Sharp corners
```

## Workplane

```python
.workplane()                           # On selection
.workplane(offset=5.0)                 # Offset
.workplane(centerOption="CenterOfMass")
.transformed(rotate=(45, 0, 0))        # Rotated
```

## Stack

```python
.first(), .last(), .item(n)
.end()     # Go back in chain
.all()     # All solids as list
.val()     # Single underlying shape
.vals()    # All underlying shapes
```
