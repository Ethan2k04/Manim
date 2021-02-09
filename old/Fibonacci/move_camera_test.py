from manimlib.imports import *

class Test(MovingCameraScene):
    def construct(self):
        rec_1 = Rectangle().set_color(ORANGE).set_fill(ORANGE).shift(RIGHT*3)
        rec_2 = Rectangle().set_color(BLUE).set_fill(BLUE).shift(LEFT*3)
        tri_1 = Triangle().set_color(YELLOW).set_fill(YELLOW)
        self.add(rec_1,rec_2,tri_1)
        self.play(self.camera_frame.scale,2)
        self.wait()