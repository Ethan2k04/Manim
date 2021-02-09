from manimlib.imports import *

class Func(GraphScene):
    CONFIG = dict(x_min=-10, x_max=10, y_min=-5, y_max=5,x_tick_frequency=2, y_tick_frequency=1,graph_origin=ORIGIN, function_color=RED,
                  axes_color=GREEN, x_labeled_nums=range(-10, 10, 4))

    def construct(self):
        self.setup_axes(animate=True)
        func_graph1=self.get_graph(self.func_to_graph1)
        self.play(ShowCreation(func_graph1))
        self.wait()
    def func_to_graph1(self,x):
        return -(x - 3) ** 2 + 2