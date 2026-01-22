---
name: manim-slides
description: Use when creating interactive presentations with manim, making slide-based animations, or when users want presentation controls like pause, loop, or transitions. Triggers include presentation mode, slides, next_slide, presenter notes, or converting animations to HTML/PDF/PPTX.
---

# Manim Slides

Create interactive presentations from Manim animations with pause points, loops, and transitions.

**Extends Manim CE** - inherits from `Slide` instead of `Scene`. All Manim features work.

## Quick Start

```python
from manim import *
from manim_slides import Slide

class MyPresentation(Slide):
    def construct(self):
        title = Text("Hello")
        self.play(Write(title))
        self.next_slide()  # Pause point - press space to continue

        self.next_slide(loop=True)  # Loop until user advances
        self.play(title.animate.scale(1.2))
        self.play(title.animate.scale(1/1.2))
        self.next_slide()  # End loop
```

**Two-step workflow:**
```bash
manim -ql script.py MyPresentation  # Render with manim
manim-slides MyPresentation         # Present interactively
```

## Core Methods

### next_slide() - Create Pause Points

```python
self.next_slide()                    # Basic pause
self.next_slide(loop=True)           # Loop until advance
self.next_slide(auto_next=True)      # Auto-advance when done
self.next_slide(notes="Explain X")   # Presenter notes (Markdown)
self.next_slide(skip_animations=True) # Skip during render (dev mode)
```

### Transitions

```python
# Wipe: slide objects off while sliding new ones on
self.wipe(old_mobjects, new_mobjects, direction=LEFT)

# Zoom: scale+fade transition
self.zoom(old_mobjects, new_mobjects, scale=1.5, out=True)
```

### Canvas - Persistent Objects

Objects on canvas persist across slides without re-adding:

```python
self.add_to_canvas(header=title, sidebar=menu)  # Named refs
self.next_slide()  # header and sidebar still visible
self.remove_from_canvas("header")  # Remove by name
# Access: self.canvas["sidebar"], self.canvas_mobjects
```

## 3D Presentations

```python
from manim_slides import ThreeDSlide

class My3D(ThreeDSlide):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)
        axes = ThreeDAxes()
        self.play(Create(axes))
        self.next_slide()
```

## Performance Optimization

```python
class FastRender(Slide):
    skip_reversing = True  # Don't generate reverse animations

    def construct(self):
        self.next_slide(skip_animations=True)  # Skip section in dev
        # ... animations to skip
        self.next_slide()  # Resume normal
```

## Modular Organization

Break long presentations into helper methods:

```python
class Modular(Slide):
    def construct(self):
        self.intro_section()
        self.main_content()
        self.conclusion()

    def intro_section(self):
        title = Text("Intro")
        self.play(Write(title))
        self.next_slide()
        self.play(FadeOut(title))
```

## Export Formats

```bash
manim-slides convert MyPresentation output.html  # Interactive HTML
manim-slides convert MyPresentation output.pdf   # PDF slides
manim-slides convert MyPresentation output.pptx  # PowerPoint
manim-slides convert --one-file MyPresentation out.html  # Self-contained
```

## Presentation Controls

| Key | Action |
|-----|--------|
| Space/Right | Next slide |
| Left | Previous slide |
| R | Reverse playback |
| F | Fullscreen |
| Q/Esc | Quit |

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using `Scene` | Use `Slide` or `ThreeDSlide` |
| `manim-slides render` for CE | Just use `manim` to render, then `manim-slides` to present |
| Manual FadeOut/FadeIn | Use `wipe()` or `zoom()` transitions |
| Giant construct() | Break into modular helper methods |
| No loop end marker | Add `self.next_slide()` after loop content |
