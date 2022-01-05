#!/usr/bin/env python3

"""Demo of a concept:

Let the _subtitles_ drive the video/presentation. Then you can text-to-speech the
output, *or* you can have someone read the subs and merge that with the video.

A separation of powers: Math people write the presentations, voice people voice
the presentation (or whoever wants to).
"""

from manim import *

def get_reading_pause(text):
    wpm = 250
    num_words = len(text.split(' '))
    return (num_words / wpm) * 60


def play_lecture(lecture):
    global scene
    global impressive_equation
    for item in lecture:
        if isinstance(item, str):
            pause = get_reading_pause(item)
            
            text = Text(item)
            text.scale(0.5)
            text.to_edge(DOWN)
            scene.add(text)
            scene.wait(pause)
            scene.remove(text)

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
    ['add', impressive_equation],
    """Can you still see it? Good. That's the idea.
    """,
    """Now watch me make it disappear.
    """,
    ['remove', impressive_equation],
    """All gone? Good. It should be!
    """,
    """Amen!
    """,
]

scene = Scene()
play_lecture(lecture)
scene.render()
