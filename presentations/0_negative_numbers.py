from presenter import *

pills = MathTex(r"hand.holding(red_pill, blue_pill)")
negative_three = MathTex(r"-3")
animated_numbers = MathTex(r"flashing(1...2...3...)")
flashing_plus = MathTex(r"5 flash(+) 2")
flashing_minus = MathTex(r"8 flash(-) 7")
bare_integral = MathTex(r"\int")

add_apples = MathTex(r"apple + apple")
subtract_apples = MathTex(r"apple - apple")

lecture = [
    """What <emphasis level="strong">are</emphasis> negative numbers?
    """,

    """You likely learned about negative numbers long ago. Maybe they have lost
       their mystery for you.
    """,

    lambda scene: scene.add(pills),

    """But what if I told you there's more here than you think? There are even
       some hints about what professional mathematitions actually do in something
       as mundane as negative numbers.
    """,

    lambda scene: scene.remove(pills),

    lambda scene: scene.add(negative_three),

    """That hoizontal stroke you see to the left of a number is a symbol. It has
       meaning. Just as the symbol you see on the right has meaning: it's a
       number.
    """,
    
    lambda scene: scene.remove(negative_three),

    lambda scene: scene.add(animated_numbers),

    """But maybe you got so used to seeing these symobols that you lost
       your appriciation for their _real_ meaning. What _is_ three? Give it a
       long think sometime. You might find it to be more profound than you gave
       credit in the past.
    """,

    lambda scene: scene.remove(animated_numbers),

    """Likewise, that "dash" that you see to the left of a "negative number" is
       also just a symbol. Why is it a dash? Why not three dots? Why not a
       bunny?
    """,

    """Someone had to invent that symbol, and we ended up with a kind of "dash".
       This same symbol is used as an _operator_.
    """,

    lambda scene: scene.add(flashing_plus),

    """Just as we use the plus symbol as an operator...
    """,

    lambda scene: scene.remove(flashing_plus),

    lambda scene: scene.add(flashing_minus),

    """So can we use the minus symbol as an operator.
    """,

    lambda scene: scene.remove(flashing_minus),

    """But let's dewell on the "symbol" aspect for just a moment.
    """,

    lambda scene: scene.add(bare_integral),

    """Do you know what this symbol means?
    """,

    """You may have no idea, or if you've studied calculus you may get excited
       by this symbol.
    """,

    """Rest assured: It's just a symbol.
    """,

    lambda scene: scene.remove(bare_integral),

    """As with all symbols, the important question is, "What does it _mean_?"
    """,

    """You can think of the minus sign as meaning "has debt" as an approximation.
    """,

    """Likewise, you can think of the plus sign as meaning, "has credit".
    """,

    """Let's use black to represent credit and red to represent debt.
    """,

    """And as is standard with these things, let's an apple to denote "a thing".
    """,

    lambda scene: scene.add(add_apples),

    """I bet you know how many apples we have after having done this!
    """,

    lambda scene: scene.remove(add_apples),

    """But now, if I show you an expression with _debt apples_...
    """,

    lambda scene: scene.add(subtract_apples),

    """
    """,

    """
    """,

    """
    """,

    """
    """,

    """
    """,

    """
    """,

    """
    """,

    """
    """,

    """
    """,

    """
    """,

]

scene = Scene()
player = Player(scene, lecture)
player.play()
scene.render()
