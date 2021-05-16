import random

import numpy as np
from manimlib import *


def boltzmann_function(v_range, temperature):
    v_map = dict()
    ##TODO some coefficient should be add
    for v in range(v_range):
        possibility = 100 * np.power(temperature, -3 / 2) * v ** 2 * np.exp(-1 * v ** 2 / temperature)
        v_map[str(v)] = possibility
    if not v_map:
        v_map = {"0": 0}
    return v_map


class RandomWalker(Dot):

    ##TODO a rigid container should be add

    def __init__(self, v_range=15, **kwargs):
        self.num = 314
        self.temperature = 1
        self.v_range = v_range
        self.v_map = boltzmann_function(v_range, self.temperature)
        self.v_list = []
        self.transform_list_to_map()
        self.dir_list = []
        self.generate_direction()
        self.velocity = np.array([0, 0, 0])
        self.get_velocity()
        super().__init__(**kwargs)

    def transform_list_to_map(self):
        for key, value in self.v_map.items():
            for i in range(round(value)):
                self.v_list.append(int(key))

    def update_v_list(self):
        self.v_map = boltzmann_function(self.v_range, self.temperature)
        self.v_list = []
        for key, value in self.v_map.items():
            for i in range(round(value)):
                self.v_list.append(int(key))

    def generate_direction(self):
        self.dir_list = [complex_to_R3(np.exp(1j * 2 * PI * (t / self.num)))
                         for t in range(self.num)]

    def get_velocity(self):
        print(self.v_list)
        velocity = 0.01 * self.v_list[random.randint(0, len(self.v_list) - 1)] * self.dir_list[
            random.randint(0, self.num - 1)]
        self.velocity = velocity

    def update_color(self):
        pass

class DistributionGraphScene(Scene):
    CONFIG = {
        "x_range": [-1, 50],
        "y_range": [-1, 3],
    }
    def construct(self):
        self.temperature = ValueTracker(273)
        self.digest_data()
        self.axes = Axes(x_range=self.x_range, y_range=self.y_range)
        self.add(self.axes)
        self.graph = self.get_riemann_rectangles(x_range=[0, self.x_range[-1]], data_map=self.data_map_init)
        self.play(ShowCreation(self.graph))
        self.wait()
        self.add_graph_updater()
        self.play(ApplyMethod(self.temperature.set_value, 600, run_time=3))
        self.play(ApplyMethod(self.temperature.set_value, 100, run_time=3))

    def digest_data(self):
        self.data_map_init = boltzmann_function(v_range=self.x_range[-1], temperature=self.temperature.get_value())

    def add_graph_updater(self):
        self.graph.add_updater(lambda m: m.become(self.get_riemann_rectangles(x_range=[0, self.x_range[-1]],
                                                                              data_map=boltzmann_function(
                                                                              v_range=self.x_range[-1],
                                                                              temperature=self.temperature.get_value()
                                                                              ))))

    def get_riemann_rectangles(self,
                               x_range=None,
                               data_map=None,
                               input_sample_type="right",
                               stroke_width=1,
                               stroke_color=BLACK,
                               fill_opacity=1,
                               colors=(BLUE, GREEN)):

        rects = []
        xs = np.arange(*x_range)
        for x0, x1 in zip(xs, xs[1:]):
            if input_sample_type == "left":
                sample = x0
            elif input_sample_type == "right":
                sample = x1
            elif input_sample_type == "center":
                sample = 0.5 * x0 + 0.5 * x1
            else:
                raise Exception("Invalid input sample type")
            height = 2 * data_map[str(round(sample))]
            rect_width = self.axes.x_axis.get_unit_size() * (x1 - x0)
            rect = Rectangle(width=rect_width, height=height)
            rect.move_to(self.axes.c2p(x0, 0), DL)
            rects.append(rect)
        result = VGroup(*rects)
        result.set_submobject_colors_by_gradient(*colors)
        result.set_style(
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            fill_opacity=fill_opacity,
        )
        return result

class RandomWalkerScene(Scene):
    CONFIG = {
        "factor": 0.0,
        "rate_func": linear,
        "dt": 0.1,
        "run_time": 5,
        "box_ratio_to_screen": 0.3
    }

    def construct(self):
        walker_group = RandomWalker(v_range=150).get_grid(10, 10, height=4)
        colors = color_gradient([BLUE, RED], 120)
        for i in range(int(self.run_time / self.dt)):
            for sub in walker_group:
                sub.update_v_list()
                sub.get_velocity()
                index = int(500 * (100 * get_norm(sub.velocity) / sub.v_range))
                print(index)
                sub.set_color(colors[index])
                sub.temperature += 5
            self.play(*[ApplyMethod(sub.shift, sub.velocity) for sub in walker_group],
                      rate_func=self.rate_func,
                      run_time=self.dt)


class RandomWalkerSceneWithContainer(Scene):
    CONFIG = {
        "factor": 0.0,
        "rate_func": linear,
        "dt": 0.1,
        "run_time": 10,
        "box_ratio_to_screen": 0.3
    }

    def construct(self):
        walker_group = RandomWalker().get_grid(10, 10, height=4)
        walker_group.set_color(BLUE)
        walker_group.set_submobject_colors_by_gradient(BLUE, RED)
        colors = color_gradient([BLUE, ORANGE, RED], 101)
        back_ground_colors = color_gradient([BLUE_A, BLUE_E], 101)
        back_ground = self.container_box()
        back_ground.set_fill(opacity=0.4)
        self.add(back_ground)
        self.wait()
        # for i in range(int(self.run_time/self.dt)):
        #     for sub in walker_group:
        #         sub.factor += 0.005
        #         sub.get_direction()
        #         sub.set_color(colors[int(200 * sub.factor)])
        #         back_ground.set_fill(back_ground_colors[int(200 * sub.factor)])
        #     self.play(*[ApplyMethod(sub.shift, sub.direction) for sub in walker_group],
        #               rate_func=self.rate_func,
        #               run_time=self.dt)
        #
        # for i in range(int(self.run_time/self.dt)):
        #     for sub in walker_group:
        #         sub.factor -= 0.005
        #         sub.get_direction()
        #         sub.set_color(colors[int(200 * sub.factor)])
        #         back_ground.set_fill(back_ground_colors[int(200 * sub.factor)])
        #     self.play(*[ApplyMethod(sub.shift, sub.direction) for sub in walker_group],
        #               rate_func=self.rate_func,
        #               run_time=self.dt)

    def container_box(self):
        width = FRAME_X_RADIUS * self.box_ratio_to_screen
        height = FRAME_Y_RADIUS * self.box_ratio_to_screen
        in_wall = Polygon(np.array([width, height, 0.0]),
                          np.array([width, -height, 0.0]),
                          np.array([-width, -height, 0.0]),
                          np.array([-width, height, 0.0]))
        vertices = in_wall.get_vertices()
        right_wall = None
        # TODO 黄金分割比的容器且自动生成
        width = self.camera.get_frame_width() / 2
        height = self.camera.get_frame_height() / 2
        rightside = Polygon(np.array([4.0, 2.0, 0.0]), np.array([2.0, -1.0, 0.0]), RIGHT * width + DOWN * height,
                            RIGHT * width + UP * height)
        downside = Polygon(np.array([4.0, -2.0, 0.0]), np.array([-2.0, -1.0, 0.0]), LEFT * width + DOWN * height,
                           RIGHT * width + DOWN * height)
        leftside = Polygon(np.array([-4.0, -2.0, 0.0]), np.array([-2.0, 1.0, 0.0]), LEFT * width + UP * height,
                           LEFT * width + DOWN * height)
        upside = Polygon(np.array([-4.0, 2.0, 0.0]), np.array([2.0, 1.0, 0.0]), RIGHT * width + UP * height,
                         LEFT * width + UP * height)
        return VGroup(upside, rightside, downside, leftside)


class RandomWalkerScene3(RandomWalkerScene):
    CONFIG = {
        "factor": 0.01,
        "rate_func": linear,
        "dt": 0.1,
        "run_time": 10
    }


class RandomWalkerScene4(RandomWalkerScene):
    CONFIG = {
        "factor": 2,
        "rate_func": linear,
        "dt": 0.1,
        "run_time": 10
    }
