# CadQuery Examples

## Bearing Pillow Block

```python
import cadquery as cq

# Parameters
height = 60.0
width = 80.0
thickness = 10.0
diameter = 22.0  # Bearing diameter
padding = 12.0   # Distance from edge to holes

result = (
    cq.Workplane("XY")
    .box(height, width, thickness)
    .faces(">Z").workplane()
    .hole(diameter)
    .faces(">Z").workplane()
    .rect(height - padding, width - padding, forConstruction=True)
    .vertices()
    .cboreHole(2.4, 4.4, 2.1)
    .edges("|Z").fillet(2.0)
)

cq.exporters.export(result, "pillow_block.step")
```

## Parametric Enclosure

```python
import cadquery as cq

# Parameters
outer_w, outer_l, outer_h = 100.0, 150.0, 50.0
wall_t = 3.0
corner_r = 10.0
screw_inset = 12.0
screw_od, screw_id = 10.0, 4.0

# Outer shell
shell = (
    cq.Workplane("XY")
    .rect(outer_w, outer_l)
    .extrude(outer_h)
    .edges("|Z").fillet(corner_r)
    .edges("#Z").fillet(2.0)
)

# Inner cavity
inner = (
    shell.faces("<Z")
    .workplane(wall_t)
    .rect(outer_w - 2*wall_t, outer_l - 2*wall_t)
    .extrude(outer_h - 2*wall_t, combine=False)
    .edges("|Z").fillet(corner_r - wall_t)
)

# Cut cavity
box = shell.cut(inner)

# Add screw posts
result = (
    box.faces(">Z")
    .workplane(-wall_t)
    .rect(outer_w - 2*screw_inset, outer_l - 2*screw_inset, forConstruction=True)
    .vertices()
    .circle(screw_od/2)
    .circle(screw_id/2)
    .extrude(-(outer_h - wall_t))
)

cq.exporters.export(result, "enclosure.step")
```

## Lego Brick

```python
import cadquery as cq

# Parameters
lbumps = 4  # bumps long
wbumps = 2  # bumps wide
pitch = 8.0
clearance = 0.1
bump_d = 4.8
bump_h = 1.8
height = 9.6
wall_t = (pitch - bump_d) / 2

total_l = lbumps * pitch - 2 * clearance
total_w = wbumps * pitch - 2 * clearance

# Base
s = cq.Workplane("XY").box(total_l, total_w, height)
s = s.faces("<Z").shell(-wall_t)

# Top bumps
s = (s.faces(">Z").workplane()
     .rarray(pitch, pitch, lbumps, wbumps, True)
     .circle(bump_d/2)
     .extrude(bump_h))

# Bottom posts (for multi-bump bricks)
if lbumps > 1 and wbumps > 1:
    post_d = pitch - wall_t
    s = (s.faces("<Z").workplane(invert=True)
         .rarray(pitch, pitch, lbumps-1, wbumps-1, True)
         .circle(post_d/2)
         .circle(bump_d/2)
         .extrude(height - wall_t))

cq.exporters.export(s, "lego_brick.step")
```

## I-Beam Profile

```python
import cadquery as cq

L, H, W, t = 100.0, 20.0, 20.0, 2.0

pts = [
    (0, H/2),
    (W/2, H/2),
    (W/2, H/2 - t),
    (t/2, H/2 - t),
    (t/2, t - H/2),
    (W/2, t - H/2),
    (W/2, -H/2),
    (0, -H/2),
]

result = (
    cq.Workplane("front")
    .polyline(pts)
    .mirrorY()
    .extrude(L)
)

cq.exporters.export(result, "i_beam.step")
```

## Bottle (Classic OCC Example)

```python
import cadquery as cq

L, w, t = 20.0, 6.0, 3.0

# Body profile
p = (
    cq.Workplane("XY")
    .center(-L/2, 0)
    .vLine(w/2)
    .threePointArc((L/2, w/2 + t), (L, w/2))
    .vLine(-w/2)
    .mirrorX()
    .extrude(30.0)
)

# Neck
p = (p.faces(">Z")
     .workplane(centerOption="CenterOfMass")
     .circle(3.0)
     .extrude(2.0))

# Shell
result = p.faces(">Z").shell(0.3)

cq.exporters.export(result, "bottle.step")
```

## Cycloidal Gear

```python
import cadquery as cq
from math import sin, cos, pi, floor

def hypocycloid(t, r1, r2):
    return (
        (r1-r2)*cos(t) + r2*cos(r1/r2*t - t),
        (r1-r2)*sin(t) + r2*sin(-(r1/r2*t - t))
    )

def epicycloid(t, r1, r2):
    return (
        (r1+r2)*cos(t) - r2*cos(r1/r2*t + t),
        (r1+r2)*sin(t) - r2*sin(r1/r2*t + t)
    )

def gear(t, r1=6, r2=1):
    if (-1)**(1 + floor(t/2/pi*(r1/r2))) < 0:
        return epicycloid(t, r1, r2)
    else:
        return hypocycloid(t, r1, r2)

result = (
    cq.Workplane("XY")
    .parametricCurve(lambda t: gear(t * 2 * pi, 6, 1))
    .twistExtrude(15, 90)
    .faces(">Z").workplane()
    .circle(2)
    .cutThruAll()
)

cq.exporters.export(result, "gear.step")
```

## Rounded Box with Mounting Holes

```python
import cadquery as cq

# Parameters
length, width, height = 60, 40, 15
corner_radius = 5
hole_inset = 8
hole_diameter = 4

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z").fillet(corner_radius)
    .edges("#Z").fillet(2)
    .faces(">Z").workplane()
    .rect(length - 2*hole_inset, width - 2*hole_inset, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

cq.exporters.export(result, "mounting_box.step")
```

## Sweep Along Path

```python
import cadquery as cq

# Create a helical path
helix = cq.Wire.makeHelix(pitch=5, height=30, radius=10)

# Sweep a circle along the helix
result = (
    cq.Workplane("XY")
    .center(10, 0)
    .circle(1)
    .sweep(helix)
)

cq.exporters.export(result, "spring.step")
```

## Box with Lid

```python
import cadquery as cq

# Parameters
w, l, h = 60, 80, 40
wall = 2
lip = 3

# Bottom
bottom = (
    cq.Workplane("XY")
    .box(w, l, h)
    .edges("|Z").fillet(3)
    .faces(">Z").shell(-wall)
)

# Lid
lid = (
    cq.Workplane("XY")
    .box(w, l, wall + lip)
    .edges("|Z").fillet(3)
    .translate((0, 0, h + 5))  # Position above box
)

# Inner lip
lip_insert = (
    cq.Workplane("XY")
    .box(w - 2*wall - 0.5, l - 2*wall - 0.5, lip)
    .translate((0, 0, h + 5 - lip))
)

lid = lid.union(lip_insert)

# Combine for export
result = bottom.union(lid)

cq.exporters.export(result, "box_with_lid.step")
```
