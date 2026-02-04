---
name: manim
description: Use when creating mathematical animations, visualizing equations, animating graphs, making educational math or science videos, or when users mention manim. Triggers include LaTeX animations, geometric visualizations, 3D math scenes, function plotting, or animated proofs.
---

# Manim Community Edition

Create mathematical animations for educational videos using Manim Community Edition (docs.manim.community).

**Not ManimGL or 3b1b's original manim** - APIs differ significantly.

## Quick Start

```python
from manim import *

class MyScene(Scene):
    def construct(self):  # Must be exactly "construct"
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        self.wait()
```

**Render:** `manim -pql script.py SceneName`

Flags: `-p` preview, `-q[l/m/h/k]` quality (low/med/high/4k), `-s` save last frame, `-t` transparent

## Core Patterns

### The .animate Syntax (Most Flexible)

```python
self.play(obj.animate.shift(RIGHT).scale(2).set_color(RED))
```

### MathTex with Isolatable Parts

**Method 1: Double braces** (simple equations only)
```python
eq = MathTex(r"{{ a^2 }} + {{ b^2 }} = {{ c^2 }}")
eq[0].set_color(RED)  # a^2
eq[2].set_color(BLUE) # b^2
```

**Method 2: Separate arguments** (works with `\frac`, complex structures)
```python
eq = MathTex(r"E", r"=", r"mc^2")
eq[0].set_color(RED)  # E
eq[2].set_color(BLUE) # mc^2
```

**Note:** Double braces inside `\frac{}{}` cause LaTeX errors. Use separate args instead.

**Always use raw strings** (`r'...'`) for LaTeX.

### Graphs and Updaters

```python
axes = Axes(x_range=[-3, 3], y_range=[-2, 5])
graph = axes.plot(lambda x: x**2, color=YELLOW)

# ValueTracker for animatable values
t = ValueTracker(0)
dot = Dot()
dot.add_updater(lambda m: m.move_to(axes.c2p(t.get_value(), t.get_value()**2)))
self.play(t.animate.set_value(2), run_time=3)
dot.clear_updaters()  # Remove when done
```

### Positioning

```python
obj.move_to(ORIGIN)           # Absolute
obj.shift(UP * 2 + RIGHT)     # Relative
obj.next_to(other, RIGHT, buff=0.5)  # Adjacent
VGroup(a, b, c).arrange(RIGHT, buff=0.3)  # Line up
```

Directions: `UP, DOWN, LEFT, RIGHT, ORIGIN, UL, UR, DL, DR, IN, OUT`

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Blank output | Check `construct()` spelling |
| LaTeX errors | Use raw strings `r"\frac{1}{2}"` |
| `{{ }}` in `\frac` | Use separate MathTex args instead |
| Transform confusion | `Transform` mutates source; `ReplacementTransform` replaces |
| Updater persists | Call `obj.clear_updaters()` when done |

## Scene Dimensions

- Height: 8 units, Width: ~14.22 units (16:9)
- Origin (0,0,0) at center

## Reference Documentation

Detailed API guides in `references/`:
- **mobjects.md** - All mobject types, methods, styling
- **animations.md** - Animation types, rate functions, updaters
- **3d-scenes.md** - ThreeDScene, camera, 3D objects
- **examples.md** - Common patterns and complete examples
