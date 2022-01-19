#!/usr/bin/env python3

from pulpit import *

impressive_equation = MathTex(r"h(u*v)=h(u) \odot h(v)")

lecture = [
    SubChunk(
        """This is the first chunk of text. Let me try to explain the idea here.
    This text appears inside of a Python list. Don't worry, it's just a proof
    of concept!
    """
    ),
    SubChunk(
        """The words that you are seeing now are the next chunk of subtitles
    in the demo. No biggie. Just showing you how to chunk your subs.
    """
    ),
    SubChunk(
        """Now, the next exciting thing is that these subtitles are interleaved
    with "commands". I can tell Manim to display some impressive math equation.
    """
    ),
    SubChunk(
        """Ready?
    """
    ),
    SubChunk(
        """Here goes...
    """
    ),
    SubChunk(
        """Can you see it? Good. That's the idea.
    """,
        actions=[lambda scene: scene.add(impressive_equation)],
    ),
    SubChunk(
        """Now watch me make it disappear.
    """
    ),
    SubChunk(
        """All gone? Good. It should be!
    """,
        actions=[lambda scene: scene.remove(impressive_equation)],
    ),
    SubChunk(
        """Amen!
    """
    ),
]

config.quality = "low_quality"
scene = Scene()
player = Player(scene, lecture, local_tts, baked=True)
player.play()
scene.render()
