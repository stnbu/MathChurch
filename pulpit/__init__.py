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
from .subrip import *
from manim import *


class Player:
    def __init__(self, scene, lecture, tts_engine, baked=False, ripped=True):
        self.scene = scene
        self.lecture = lecture
        self.tts_engine = tts_engine
        self.baked = baked
        self.ripped = ripped
        self.subrip_file = SubRipFile()
        self.offset = 0.0

    def play(self, count=None):
        for index, item in enumerate(self.lecture):
            if count is not None and index + 1 == count:
                break
            if isinstance(item, str):
                if item.strip() == "":
                    # because we do not want an empty mp3 file.
                    continue
                path, length = self.tts_engine(item)
                self.scene.add_sound(path)

                if self.baked:
                    subtitle = Text(item)
                    subtitle.scale(0.5)
                    subtitle.to_edge(DOWN)
                    self.scene.add(subtitle)

                self.scene.wait(length)

                if self.baked:
                    self.scene.remove(subtitle)

                if self.ripped:
                    self.subrip_file.add(
                        SubRipChunk(appear=self.offset, disappear=self.offset+length, text=item)
                    )

                self.offset = self.offset + length

            elif isinstance(item, FunctionType):
                item(self.scene)
            else:
                raise ValueError
        subrip_file_path = (
            os.path.splitext(self.scene.renderer.file_writer.movie_file_path)[0]
            + ".srt"
        )
        self.subrip_file.write_to(subrip_file_path)
