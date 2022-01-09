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
from mutagen.mp3 import MP3
from manim import *


YES_YOU_PRINT_HEADER = False
def log_about_to_add_sound(length, path, offset):
    global YES_YOU_PRINT_HEADER
    format = '%s\t%s\t%s'
    if not YES_YOU_PRINT_HEADER:
        print(format % ('length', 'path', 'offset'))
        YES_YOU_PRINT_HEADER = True
    print(format % (length, path, offset))


class Player:
    def __init__(self, scene, lecture):
        self.scene = scene
        self.lecture = lecture

    def play(self):
        offset = 0
        for item in self.lecture:
            if isinstance(item, str):
                if (item.strip() == ""):
                    # because we do not want an empty mp3 file.
                    continue
                _, path = get_audio_bytes(item, get_google_speech_from_text)
                length = MP3(path).info.length
                log_about_to_add_sound(length, path, offset)
                self.scene.add_sound(path, time_offset=offset)
                wait = length + 0.2
                offset += wait
                subtitle = Text(item)
                subtitle.scale(0.5)
                subtitle.to_edge(DOWN)
                self.scene.add(subtitle)
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
    """
config.verbosity
config.disable_caching
frame_rate
upto_animation_number
partial_movie_dir {video_dir}/partial_movie_files/{scene_name}
quality
media_dir
write_all = False #### False?!
log_to_file = False
text_dir (4 subs??
"""
    config.preview = True
    #import ipdb; ipdb.set_trace()
    player = Player(scene, lecture)
    player.play()
    scene.render()
