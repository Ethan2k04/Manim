from manimlib.imports import *
import math

class Tutorial(Scene):
    def construct(self):
        mobs = VGroup(*[
            mob.set_height(3)
            for mob in [Square(),Circle(),Triangle()]
        ])
        mobs.set_fill(opacity=1)
        for i in range(1,3):
            mobs[i].next_to(mobs[i-1].get_left(),RIGHT,buff=1)
        mobs.move_to(ORIGIN)

        self.add(*mobs)
        self.wait()

        for mob in mobs[::-1]:
            self.remove(mob)
            self.wait(0.5)

        self.wait()
class LHopital(GraphScene):

    CONFIG = {
        "graph_origin": 0.5 * DOWN + 4 * LEFT,
        "x_min":0,
        "x_max":9,
        "y_min":-3,
        "y_max":5,
        "axes_color":WHITE,}

    def construct(self):
        wood_bar = ImageMobject("/Users/ytj/Desktop/ManimInstall/manim_7May/image/wood.jpeg").set_height(0.5,stretch=True).set_width(15,stretch=True).to_edge(DOWN,buff=0)
        self.add(wood_bar)
        self.setup_axes(animate=False)
        graph_1 = self.get_graph(self.func_1,YELLOW)
        dl = VGroup(*[mob.set_color(ORANGE)
                                for mob in [Dot(),Line()]])
        moving_x = ValueTracker(2)
        dl[0].add_updater(lambda m:m.move_to(self.coords_to_point(moving_x.get_value(),self.func_1(moving_x.get_value()))))
        dl[1].add_updater(lambda m:m.put_start_and_end_on(self.graph_origin,dl[0].get_center()))
        self.play(ShowCreation(graph_1))
        self.play(FadeIn(dl))
        self.play(ApplyMethod(moving_x.increment_value,4),rate_func=smooth,run_time=4)
        self.wait()
        self.play(ApplyMethod(moving_x.increment_value, -3),rate_func=smooth,run_time=3)

    def func_1(self,x):
        return 1.5 ** (np.log2(x)) * np.sin(x)