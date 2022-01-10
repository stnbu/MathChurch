#!/usr/bin/env python3
"""Demo of a concept:

Let the _subtitles_ drive the video/presentation. Then you can text-to-speech
the output, *or* you can have someone read the subs and merge that with the
video.

A separation of powers: Math people write the presentations, voice people voice
the presentation (or whoever wants to).
"""

from types import FunctionType
from tts import *
from manim import *


class Player:
    def __init__(self, scene, lecture, tts_engine):
        self.scene = scene
        self.lecture = lecture
        self.tts_engine = tts_engine

    def play(self):
        for item in self.lecture:
            if isinstance(item, str):
                if item.strip() == "":
                    # because we do not want an empty mp3 file.
                    continue
                path, length = self.tts_engine(item)
                logger.info(
                    "File %s has play time %s and corresponds to input "
                    "text of length %s characters." % (path, length, len(item))
                )
                self.scene.add_sound(path)
                wait = length + 0.2
                subtitle = Text(item)
                subtitle.scale(0.5)
                subtitle.to_edge(DOWN)
                self.scene.add(subtitle)
                logger.info(
                    "We will be adding a pause to the video of %s seconds" % wait
                )
                self.scene.wait(wait)
                self.scene.remove(subtitle)
            elif isinstance(item, FunctionType):
                item(self.scene)
            else:
                raise ValueError


if __name__ == "__main__":

    impressive_equation = MathTex(r"h(u*v)=h(u) \odot h(v)")

    lecture = [
        """This is the first chunk of text. Let me try to explain the idea here.
        This text appears inside of a Python list. Don't worry, it's just a proof
        of concept!
        """,
        """The words that you are seeing now are the next chunk of subtitles
        in the demo. No biggie. Just showing you how to chunk your subs.
        """,
        """Now, the next exciting thing is that these subtitles are interleaved
        with "commands". I can tell Manim to display some impressive math equation.
        """,
        """Ready?
        """,
        """Here goes...
        """,
        lambda scene: scene.add(impressive_equation),
        """Can you see it? Good. That's the idea.
        """,
        """Now watch me make it disappear.
        """,
        lambda scene: scene.remove(impressive_equation),
        """All gone? Good. It should be!
        """,
        """Amen!
        """,
    ]

    scene = Scene()
    player = Player(scene, lecture, local_tts)
    player.play()
    scene.render()
