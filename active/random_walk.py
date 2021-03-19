from manimlib import *

class RandomWalker(Mobject):
    def __init__(self):
        shape = Dot()
        self.add(shape)

class Test(Scene):
    def construct(self):
        a = Dot()
        self.play(a.shift, UP)