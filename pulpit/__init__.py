#!/usr/bin/env python3
"""Demo of a concept:

Let the _subtitles_ drive the video/presentation. Then you can text-to-speech
the output, *or* you can have someone read the subs and merge that with the
video.

A separation of powers: Math people write the presentations, voice people voice
the presentation (or whoever wants to).
"""

from types import FunctionType
from .tts import *
from manim import *


class Player:
    def __init__(self, scene, lecture, tts_engine):
        self.scene = scene
        self.lecture = lecture
        self.tts_engine = tts_engine

    def play(self, count=None):
        for index, item in enumerate(self.lecture):
            if count is not None and index + 1 == count:
                break
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
