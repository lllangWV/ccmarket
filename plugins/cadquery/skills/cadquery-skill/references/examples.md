# CadQuery Examples

## Bearing Pillow Block

```python
import cadquery as cq

height, width, thickness = 60.0, 80.0, 10.0
diameter, padding = 22.0, 12.0

result = (
    cq.Workplane("XY")
    .box(height, width, thickness)
    .faces(">Z").workplane().hole(diameter)
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

outer_w, outer_l, outer_h = 100.0, 150.0, 50.0
wall_t, corner_r = 3.0, 10.0
screw_inset, screw_od, screw_id = 12.0, 10.0, 4.0

shell = (
    cq.Workplane("XY")
    .rect(outer_w, outer_l).extrude(outer_h)
    .edges("|Z").fillet(corner_r)
    .edges("#Z").fillet(2.0)
)

inner = (
    shell.faces("<Z").workplane(wall_t)
    .rect(outer_w - 2*wall_t, outer_l - 2*wall_t)
    .extrude(outer_h - 2*wall_t, combine=False)
    .edges("|Z").fillet(corner_r - wall_t)
)

box = shell.cut(inner)

result = (
    box.faces(">Z").workplane(-wall_t)
    .rect(outer_w - 2*screw_inset, outer_l - 2*screw_inset, forConstruction=True)
    .vertices()
    .circle(screw_od/2).circle(screw_id/2)
    .extrude(-(outer_h - wall_t))
)

cq.exporters.export(result, "enclosure.step")
```

## Lego Brick

```python
import cadquery as cq

lbumps, wbumps = 4, 2
pitch, clearance = 8.0, 0.1
bump_d, bump_h, height = 4.8, 1.8, 9.6
wall_t = (pitch - bump_d) / 2

total_l = lbumps * pitch - 2 * clearance
total_w = wbumps * pitch - 2 * clearance

s = cq.Workplane("XY").box(total_l, total_w, height)
s = s.faces("<Z").shell(-wall_t)

s = (s.faces(">Z").workplane()
     .rarray(pitch, pitch, lbumps, wbumps, True)
     .circle(bump_d/2).extrude(bump_h))

if lbumps > 1 and wbumps > 1:
    post_d = pitch - wall_t
    s = (s.faces("<Z").workplane(invert=True)
         .rarray(pitch, pitch, lbumps-1, wbumps-1, True)
         .circle(post_d/2).circle(bump_d/2)
         .extrude(height - wall_t))

cq.exporters.export(s, "lego_brick.step")
```

## I-Beam

```python
import cadquery as cq

L, H, W, t = 100.0, 20.0, 20.0, 2.0

pts = [
    (0, H/2), (W/2, H/2), (W/2, H/2 - t),
    (t/2, H/2 - t), (t/2, t - H/2),
    (W/2, t - H/2), (W/2, -H/2), (0, -H/2),
]

result = (
    cq.Workplane("front")
    .polyline(pts).mirrorY()
    .extrude(L)
)

cq.exporters.export(result, "i_beam.step")
```

## Helical Spring

```python
import cadquery as cq

helix = cq.Wire.makeHelix(pitch=5, height=30, radius=10)

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

w, l, h, wall, lip = 60, 80, 40, 2, 3

bottom = (
    cq.Workplane("XY")
    .box(w, l, h)
    .edges("|Z").fillet(3)
    .faces(">Z").shell(-wall)
)

lid = (
    cq.Workplane("XY")
    .box(w, l, wall + lip)
    .edges("|Z").fillet(3)
    .translate((0, 0, h + 5))
)

lip_insert = (
    cq.Workplane("XY")
    .box(w - 2*wall - 0.5, l - 2*wall - 0.5, lip)
    .translate((0, 0, h + 5 - lip))
)

result = bottom.union(lid.union(lip_insert))

cq.exporters.export(result, "box_with_lid.step")
```

## Rounded Box with Holes

```python
import cadquery as cq

length, width, height = 60, 40, 15
corner_r, hole_inset, hole_d = 5, 8, 4

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z").fillet(corner_r)
    .edges("#Z").fillet(2)
    .faces(">Z").workplane()
    .rect(length - 2*hole_inset, width - 2*hole_inset, forConstruction=True)
    .vertices()
    .hole(hole_d)
)

cq.exporters.export(result, "mounting_box.step")
```
