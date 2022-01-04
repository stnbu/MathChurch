

from manim import *

class SomeEquasion(Scene):
    def construct(self):
        ds_m = MathTex(r"E = mc^2", fill_color="#343434").scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        logo = VGroup(ds_m)
        logo.move_to(ORIGIN)
        self.add(logo)
