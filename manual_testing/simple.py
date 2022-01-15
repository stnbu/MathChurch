
from pulpit import *

pills = ImageMobject("pills.jpg")

lecture = [
    SubChunk(
        """This is the first chunk of text. Let me try to explain the idea here.
        This text appears inside of a Python list. Don't worry, it's just a proof
        of concept!
        """,
        [lambda scene: scene.play(FadeIn(pills), run_time=9)])
]

config.quality = "low_quality"
scene = Scene()
player = Player(scene, lecture, local_tts)
player.play()
scene.render()

# ~/git/MathChurch/media/videos/480p15/Scene.mp4
# ~/git/MathChurch/media/videos/480p15/Scene.srt