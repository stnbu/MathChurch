import os
from pulpit import *

pills = ImageMobject(os.path.join(os.path.dirname(__file__), "pills.jpg"))

lecture = [
    SubChunk(
        """This is the first chunk of text. Let me try to explain the idea here.
        This text appears inside of a Python list. Don't worry, it's just a proof
        of concept!
        """,
        actions=[lambda scene: scene.play(FadeIn(pills), run_time=9)],
    )
]

config.quality = "low_quality"
scene = Scene()
player = Player(scene, lecture, local_tts)
player.play()
scene.render()
