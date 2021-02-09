from manimlib.imports import *

class TwoDBallFalling(Scene):
    CONFIG = {"g" : 9.8,"kp" : 0.2,"v" : 3}
    def construct(self):
        ball_1 = Circle().set_stroke(color=WHITE).scale(0.25)
        ball_1.to_edge(UP)
        ball_2 = ball_1.copy()
        ball_2.to_edge(UP)
        dt = 1/30
        position_init = ball_1.get_center()

        for i in range(180):
            position_now_1 = position_init + np.array([0,-self.gravity_displacement(i/30),0])
            position_now_2 = position_init + np.array([self.v * self.kp * (i/30),-self.gravity_displacement(i/30),0])
            self.play(ApplyMethod(ball_1.move_to,position_now_1),ApplyMethod(ball_2.move_to,position_now_2),run_time=dt)
        self.wait()

    def gravity_displacement(self,t):
        return self.kp * 0.5 * self.g * (t ** 2)