---
name: manim-voiceover
description: Use when adding narration or voiceovers to manim animations, syncing speech with animations, using text-to-speech services (Azure, gTTS, ElevenLabs, OpenAI), recording microphone audio, or when users mention voiceover, narration, or TTS with manim.
---

# Manim Voiceover

Add voiceovers to Manim animations directly in Python - no video editing needed.

**Extends Manim CE** - inherit from `VoiceoverScene` instead of `Scene`. All Manim features work.

## Quick Start

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MyNarration(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        circle = Circle()

        with self.voiceover(text="This circle appears as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)
```

**Render with caching disabled (required):**
```bash
manim -ql --disable_caching script.py MyNarration
```

## Installation

```bash
# Core + common services
pip install "manim-voiceover[azure,gtts]"

# All services
pip install "manim-voiceover[all]"
```

**System dependencies:**
- **Recording:** `sudo apt install portaudio19-dev && pip install pyaudio`
- **Audio speed:** `sudo apt install sox libsox-fmt-all`

## Speech Services

| Service | Quality | Offline | Cost | Setup |
|---------|---------|---------|------|-------|
| GTTSService | Good | No | Free | None (uses Google Translate) |
| AzureService | Excellent | No | Free 500 min/mo | `AZURE_SUBSCRIPTION_KEY`, `AZURE_SERVICE_REGION` in `.env` |
| ElevenLabsService | Excellent | No | Free 10k chars/mo | `ELEVEN_API_KEY` in `.env` |
| OpenAIService | Excellent | No | Paid | `OPENAI_API_KEY` in `.env` |
| CoquiService | Good | Yes | Free | Requires PyTorch |
| PyTTSX3Service | Basic | Yes | Free | Requires espeak |
| RecorderService | Your voice | Yes | Free | Microphone |

### Service Configuration

```python
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.elevenlabs import ElevenLabsService
from manim_voiceover.services.recorder import RecorderService

# Google TTS (multilingual)
self.set_speech_service(GTTSService(lang="en", tld="com"))

# Azure (high quality, many voices)
self.set_speech_service(AzureService(
    voice="en-US-AriaNeural",
    style="newscast-casual"
))

# ElevenLabs (natural voices)
self.set_speech_service(ElevenLabsService(voice_name="Rachel"))

# Record your own
self.set_speech_service(RecorderService())
```

## Core Patterns

### Basic Sync - Match Animation to Speech

```python
with self.voiceover(text="The square transforms into a circle.") as tracker:
    self.play(Transform(square, circle), run_time=tracker.duration)
```

If animation finishes early, Manim waits for voiceover to complete.

### Bookmarks - Trigger at Specific Words

```python
with self.voiceover(
    text="First <bookmark mark='A'/>the circle, then <bookmark mark='B'/>the square."
) as tracker:
    self.wait_until_bookmark("A")
    self.play(Create(circle))

    self.wait_until_bookmark("B")
    self.play(Create(square))
```

### Time Between Bookmarks

```python
with self.voiceover(
    text="Watch <bookmark mark='start'/>the transformation<bookmark mark='end'/> happen."
) as tracker:
    self.wait_until_bookmark("start")
    self.play(
        Transform(a, b),
        run_time=tracker.time_until_bookmark("end")
    )
```

### Subcaptions - Different Display Text

```python
with self.voiceover(
    text="The equation e to the i pi equals negative one",
    subcaption="e^(iπ) = -1"
) as tracker:
    self.play(Write(equation), run_time=tracker.duration)
```

### Multiple Inheritance

```python
from manim_voiceover import VoiceoverScene
from manim import MovingCameraScene

class NarratedCamera(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        # Both voiceover and camera features available
```

## Common Patterns

### Sequential Narration

```python
def construct(self):
    self.set_speech_service(GTTSService())

    with self.voiceover(text="Let's start with a circle.") as tracker:
        circle = Circle()
        self.play(Create(circle), run_time=tracker.duration)

    with self.voiceover(text="Now we add a square.") as tracker:
        square = Square().next_to(circle, RIGHT)
        self.play(Create(square), run_time=tracker.duration)
```

### Multilingual

```python
# Change language
self.set_speech_service(GTTSService(lang="es"))  # Spanish
self.set_speech_service(GTTSService(lang="fr"))  # French
self.set_speech_service(GTTSService(lang="de"))  # German
```

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Rendering without `--disable_caching` | Always use `manim -ql --disable_caching script.py` |
| Using `Scene` | Use `VoiceoverScene` |
| Missing API keys | Add keys to `.env` file for paid services |
| Animation longer than speech | Use `tracker.duration` for run_time |
| gTTS not working | Requires internet connection |
