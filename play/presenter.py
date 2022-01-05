
from manim import *

class Command:

    def __init__(self, command):
        self.command = command

    def execute(self):
        print("<" + self.command + ">\n\n")

    def disappear(self):
        print("<Now undoing the command or something.>\n\n")

def get_reading_pause(text):
    wpm = 250
    num_words = len(text.split(' '))
    return (num_words / wpm) * 60

"""

    text = Text("People of Earth!!")
    subs.add(text)
    subs.wait(3)
    subs.remove(text)

    text = Text("Look at this!!")
    subs.add(text)
    subs.wait(3)
    subs.remove(text)

    text = Text("(gestures rudely)")
    subs.add(text)
    subs.wait(3)
    subs.remove(text)

    subs.render()
"""


def play_lecture(lecture):
    global subs
    print("---[begin lecture]---\n\n")
    for item in lecture:
        if isinstance(item, str):
            pause = get_reading_pause(item)
            
            text = Text(item)
            subs.add(text)
            subs.wait(pause)
            subs.remove(text)

        elif item.__self__.__class__ == Command:  # yuck
            item()
        else:
            raise ValueError
    print("---[end lecture]---\n\n")

impressive_equation = Command("Showing the impressive equation!")

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
    impressive_equation.execute,
    """Can you still see it? Good. That's the idea.
    """,
    """Now watch me make it disappear.
    """,
    impressive_equation.disappear,
    """All gone? Good. It should be!
    """,
    """Amen!
    """,
]

subs = Scene()

play_lecture(lecture)

subs.render()
