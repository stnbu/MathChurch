import os
from pulpit import *


def asset(filename):
    return os.path.join(os.path.splitext(__file__)[0] + ".assets", filename)


pills = ImageMobject(asset("pills.jpg"))
pills.scale(0.5)
negative_three = MathTex(r"-3")
animated_numbers = MathTex(r"flashing(1...2...3...)")
flashing_plus = MathTex(r"5 flash(+) 2")
flashing_minus = MathTex(r"8 flash(-) 7")
bare_integral = MathTex(r"\int")

add_apples = MathTex(r"apple + apple")
subtract_apples = MathTex(r"apple - apple")

lecture = [
    SubChunk("""What are negative numbers?"""),

    SubChunk("""You likely learned about negative numbers long ago. Maybe they have lost
       their mystery for you."""),

    SubChunk("""But what if I told you there's more here than you think. There are even
       some hints about what professional mathematitions actually do in something
       as mundane as negative numbers.""",
             actions=[
                 lambda scene: scene.play(FadeIn(pills), run_time=3),
                 lambda scene: scene.play(FadeOut(pills), run_time=3)
             ]),

    SubChunk("""That hoizontal stroke you see to the left of a number is a symbol. It has
       meaning. Just as the symbol you see on the right has meaning: it's a
       number.""",
             actions=[lambda scene: scene.add(negative_three)]),

    SubChunk("""But maybe you got so used to seeing these symobols that you lost
       your appriciation for their real meaning. What is three? Give it a
       long think sometime. You might find it to be more profound than you gave
       credit in the past.""",
             actions=[lambda scene: scene.remove(negative_three),
                      lambda scene: scene.add(animated_numbers)
                      ]),

    # lambda scene: scene.remove(animated_numbers),
    # SubChunk("""Likewise, that "dash" that you see to the left of a "negative number" is
    #    also just a symbol. Why is it a dash? Why not three dots? Why not a
    #    bunny?
    # """),
    # SubChunk("""Someone had to invent that symbol, and we ended up with a kind of "dash".
    #    This same symbol is used as an operator.
    # """),
    # lambda scene: scene.add(flashing_plus),
    # SubChunk("""Just as we use the plus symbol as an operator...
    # """),
    # lambda scene: scene.remove(flashing_plus),
    # lambda scene: scene.add(flashing_minus),
    # SubChunk("""So can we use the minus symbol as an operator.
    # """),
    # lambda scene: scene.remove(flashing_minus),
    # SubChunk("""But let's dewell on the "symbol" aspect for just a moment.
    # """),
    # lambda scene: scene.add(bare_integral),
    # SubChunk("""Do you know what this symbol means?
    # """),
    # SubChunk("""You may have no idea, or if you've studied calculus you may get excited
    #    by this symbol.
    # """),
    # SubChunk("""Rest assured: It's just a symbol.
    # """),
    # lambda scene: scene.remove(bare_integral),
    # SubChunk("""As with all symbols, the important question is, "What does it mean?"
    # """),
    # SubChunk("""You can think of the minus sign as meaning "has debt" as an approximation.
    # """),
    # SubChunk("""Likewise, you can think of the plus sign as meaning, "has credit".
    # """),
    # SubChunk("""Let's use black to represent credit and red to represent debt.
    # """),
    # SubChunk("""And as is standard with these things, let's an apple to denote "a thing".
    # """),
    # lambda scene: scene.add(add_apples),
    # SubChunk("""I bet you know how many apples we have after having done this!
    # """),
    # lambda scene: scene.remove(add_apples),
    # SubChunk("""But now, if I show you an expression with debt apples...
    # """),
    # lambda scene: scene.add(subtract_apples),
]

scene = Scene()
player = Player(scene, lecture, local_tts)
player.play()
scene.render()
