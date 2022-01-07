#!/usr/bin/env python3

"""Demo of a concept:

Let the _subtitles_ drive the video/presentation. Then you can text-to-speech
the output, *or* you can have someone read the subs and merge that with the
video.

A separation of powers: Math people write the presentations, voice people voice
the presentation (or whoever wants to).
"""

if __name__ == "__main__":
    import sys, os

    sys.path.append(os.path.dirname(__file__))  # only grownups are allowed to do this.


from gtts import *
from mutagen.mp3 import MP3
from manim import *


def get_reading_pause(text):
    wpm = 250
    num_words = len(text.split(" "))
    return (num_words / wpm) * 60


current_offset = 0


def play_lecture(lecture):
    global scene
    global impressive_equation
    global current_offset
    for item in lecture:
        if isinstance(item, str):
            _, path = get_audio_bytes(item, get_google_speech_from_text)
            length = MP3(path).info.length
            scene.add_sound(path, time_offset=current_offset)
            subtitle = Text(item)
            subtitle.scale(0.5)
            subtitle.to_edge(DOWN)
            scene.add(subtitle)
            scene.wait(length)
            scene.remove(subtitle)
        elif isinstance(item, list):
            command, mobject = item
            if command == "add":
                scene.add(mobject)
            elif command == "remove":
                scene.remove(mobject)
            else:
                raise ValueError
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
        ["add", impressive_equation],
        """Can you see it? Good. That's the idea.
        """,
        """Now watch me make it disappear.
        """,
        ["remove", impressive_equation],
        """All gone? Good. It should be!
        """,
        """Amen!
        """,
    ]

    scene = Scene()
    play_lecture(lecture)
    scene.render()
