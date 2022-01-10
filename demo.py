from presenter import *

if True:

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
