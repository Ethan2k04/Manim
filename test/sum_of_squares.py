from manimlib.imports import *

class Equation(Scene):

    def construct(self):
        eq_01 = TexMobject("{1}^{2}","+{2}^{2}","+{3}^{2}","+{4}^{2}","+{5}^{2}","+\dots","=","\quad?")
        item01 = eq_01[0].copy().scale(3).move_to(np.array([0,0,0]))
        eq_01_1 = eq_01.move_to(LEFT)
        self.play(FadeIn(item01))
        self.wait()
        self.play(ReplacementTransform(item01,eq_01_1[0]))
        self.wait()
        self.play(Write(eq_01[1:7]))
        self.wait(0.5)
        self.play(FadeInFromDown(eq_01_1[7].copy().scale(3).set_color(RED)))