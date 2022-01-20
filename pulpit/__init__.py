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

class SubChunk:

    def __init__(self, *lines, actions=None):
        if len(lines) == 0:
            raise ValueError
        if len(lines) == 1:
            self.text, = lines
        else:
            stripped_lines = [l.strip() for l in lines[1:-1]]
            stripped_lines.insert(0, lines[0].rstrip())
            try:
                stripped_lines.append(lines[-1].lstrip())
            except:
                import ipdb; ipdb.set_trace()
            self.text = ' '.join(stripped_lines)
        if actions is None:
            self.actions = []
        else:
            self.actions = actions

class Player:
    def __init__(self, scene, lecture, tts_engine, baked=False, ripped=True):
        self.scene = scene
        self.lecture = lecture
        self.tts_engine = tts_engine
        self.baked = baked
        self.ripped = ripped
        self.subrip_file = SubRipFile()

    def play(self):
        sound_track_offset = 0.0
        waiting_until = 0.0
        for chunk in self.lecture:
            path, length = self.tts_engine(chunk.text)
            self.scene.add_sound(path)

            if self.baked:
                subtitle = Text(chunk.text)
                subtitle.scale(0.5)
                subtitle.to_edge(DOWN)
                self.scene.add(subtitle)

            start_time = self.scene.renderer.time
            for action in chunk.actions:
                action(self.scene)
            actions_wait = self.scene.renderer.time - start_time

            if actions_wait < length:
                self.scene.wait(length - actions_wait)

            if self.baked:
                self.scene.remove(subtitle)
            if self.ripped:
                self.subrip_file.add(
                    SubRipChunk(
                        appear=sound_track_offset,
                        disappear=sound_track_offset + length,
                        text=chunk.text,
                    )
                )

            sound_track_offset = sound_track_offset + length

        subrip_file_path = (
            os.path.splitext(self.scene.renderer.file_writer.movie_file_path)[0]
            + ".srt"
        )
        self.subrip_file.write_to(subrip_file_path)
