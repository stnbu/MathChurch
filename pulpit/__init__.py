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

SubChunk = namedtuple("SubChunk", ["text", "actions"], defaults=[[]])

def get_total_waits(actions):
    # FIXME: This is B.A.D.
    # Can we get around it? We need to find actions' total duration
    # before we can know how much wait to add for the audio clip to
    # finish, BUT we must, in order...
    #   1. play audio
    #   1. play animations
    #   1. wait for "audio length MINUS ANIMATIONS LENGTH"
    # I know of no other way to calculate actions' duration. There's
    # a short-circuit, see.
    s = Scene()
    start_time = s.renderer.time
    for action in actions:
        action(s)
    return s.renderer.time - start_time

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
            actions_wait = get_total_waits(chunk.actions)
            path, length = self.tts_engine(chunk.text)
            self.scene.add_sound(path)

            if self.baked:
                subtitle = Text(chunk.text)
                subtitle.scale(0.5)
                subtitle.to_edge(DOWN)
                self.scene.add(subtitle)

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

            for action in chunk.actions:
                action(self.scene)

            if actions_wait < length:
                self.scene.wait(length - actions_wait)


        subrip_file_path = (
            os.path.splitext(self.scene.renderer.file_writer.movie_file_path)[0]
            + ".srt"
        )
        self.subrip_file.write_to(subrip_file_path)
