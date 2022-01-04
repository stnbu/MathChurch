

from manim import *

class SomeEquasion(Scene):
    def construct(self):
        ds_m = MathTex(r"E = mc^2", fill_color="#343434").scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        logo = VGroup(ds_m)
        logo.move_to(ORIGIN)
        self.add(logo)

class BraceAnnotation(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        self.add(line, dot, dot2, b1, b2, b1text, b2text)
