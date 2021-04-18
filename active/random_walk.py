import random

import numpy as np
from manimlib import *


def boltzmann_function(v_range, temperature):
    v_list = []
    ##TODO some coefficient should be add
    for v in range(v_range):
        possibility = 100 * np.power(temperature, -3 / 2) * v ** 2 * np.exp(-1 * v ** 2 / temperature)
        for p in range(round(possibility)):
            v_list.append(v)
    if not v_list:
        v_list = [0]
    return v_list


class RandomWalker(Dot):

    ##TODO a rigid container should be add

    def __init__(self, v_range=15, **kwargs):
        self.num = 314
        self.temperature = 1
        self.v_range = v_range
        self.v_list = boltzmann_function(v_range, self.temperature)
        self.dir_list = []
        self.generate_direction()
        self.velocity = np.array([0, 0, 0])
        self.get_velocity()
        super().__init__(**kwargs)

    def update_v_list(self):
        self.v_list = boltzmann_function(self.v_range, self.temperature)

    def generate_direction(self):
        self.dir_list = [complex_to_R3(np.exp(1j * 2 * PI * (t / self.num)))
                         for t in range(self.num)]

    def get_velocity(self):
        velocity = 0.1 * self.v_list[random.randint(0, len(self.v_list) - 1)] * self.dir_list[
            random.randint(0, self.num - 1)]
        self.velocity = velocity

    def update_color(self):
        pass


class BoltzmannLaw(Axes):

    ##TODO should be integrate to RandomWalker class

    def __init__(self, mass=1, temperature=273, **kwargs):
        k = 0.001
        self.c1 = mass / (2 * k * temperature)
        self.c2 = np.sqrt(self.c1 / PI)
        self.function = lambda u: self.c2 * np.exp(- self.c1 * u ** 2)
        self.x_range = [-4, 4, 0.25]
        super().__init__(self.x_range, **kwargs)
        self.graph = self.get_graph(self.function)
        self.add(self.graph)


class Test(Scene):
    def construct(self):
        a = BoltzmannLaw()
        t = ValueTracker(273)
        a.add_updater(lambda m: m.become(BoltzmannLaw(temperature=t.get_value())))
        self.play(FadeIn(a))
        self.play(ApplyMethod(t.set_value, 100))


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
        colors = color_gradient([BLUE, RED], 200)
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

        for i in range(int(self.run_time / self.dt)):
            for sub in walker_group:
                sub.update_v_list()
                sub.get_velocity()
                index = int(500 * (100 * get_norm(sub.velocity) / sub.v_range))
                print(index)
                sub.set_color(colors[index])
            self.play(*[ApplyMethod(sub.shift, sub.velocity) for sub in walker_group],
                      rate_func=self.rate_func,
                      run_time=self.dt)

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
