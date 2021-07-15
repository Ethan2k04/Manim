import numpy as np
import sympy as sy
import pymunk


from manimlib import *


class Space(Mobject):
    def __init__(self, dt, gravity, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.dt = dt

    def add_body(self, body):
        if body.body != self.space.static_body:
            self.space.add(body.body)
        self.space.add(body.shape)


class OpeningQuote(Scene):
    CONFIG = {
        "quote": [],
        "quote_arg_separator": " ",
        "highlighted_quote_terms": {},
        "author": "",
        "fade_in_kwargs": {
            "lag_ratio": 0.5,
            "rate_func": linear,
            "run_time": 5,
        },
        "text_size": "\\Large",
        "use_quotation_marks": True,
        "top_buff": 1.0,
        "author_buff": 1.0,
    }

    def construct(self):
        self.quote = self.get_quote()
        self.author = self.get_author(self.quote)

        self.play(FadeIn(self.quote, **self.fade_in_kwargs))
        self.wait(2)
        self.play(Write(self.author, run_time=3))
        self.wait()

    def get_quote(self, max_width=FRAME_WIDTH - 1):
        words = self.quote
        quote = VGroup()
        for word in words:
            quote.add(Text(word, font="Arial"))
        quote.arrange(RIGHT, aligned_edge=UP)
        # TODO, make less hacky
        # if self.quote_arg_separator == " ":
        #     quote[0].shift(0.2 * RIGHT)
        #     quote[-1].shift(0.2 * LEFT)
        for term, color in self.highlighted_quote_terms.items():
            quote.set_color_by_tex(term, color)
        quote.move_to(ORIGIN)
        if quote.get_width() > max_width:
            quote.set_width(max_width)
        return quote

    def get_author(self, quote):
        author = TexText(self.text_size + " --" + self.author)
        author.next_to(quote, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        author.set_color(YELLOW)
        return author


def step(space, dt):
    space.space.step(dt)


def simulate(b):
    x, y = b.body.position
    b.move_to(x * RIGHT + y * UP)
    b.rotate(b.body.angle - b.angle)
    b.angle = b.body.angle


##quote
class Quote(OpeningQuote):
    pass


##introduction
def billiard_ball(index, radius=0.5):
    ball = TexturedSurface(Sphere(radius=radius,
                                  opacity=1,
                                  gloss=0.8,
                                  shadow=0.8),
                           f"/Users/ytj/manim-master/my_program/texture/billiard/ball{index + 1}_texture.png")
    ball.rotate(angle=PI / 2, axis=UP).rotate(angle=PI / 2, axis=OUT)
    return ball

# TODO squished billiard
class BilliardCollision(ThreeDScene):
    CONFIG = {
        "size_factor": 0.5,
        "kickoff_velocity": [20, 0],
        "fill_rule": [
            [0, 0, 0],
            [np.sqrt(3) / 2, 1 / 2, 0],
            [np.sqrt(3) / 2, -1 / 2, 0],
            [np.sqrt(3), 1, 0],
            [np.sqrt(3), 0, 0],
            [np.sqrt(3), -1, 0],
            [3 * np.sqrt(3) / 2, 3 / 2, 0],
            [3 * np.sqrt(3) / 2, 1 / 2, 0],
            [3 * np.sqrt(3) / 2, -1 / 2, 0],
            [3 * np.sqrt(3) / 2, -3 / 2, 0]]}

    def construct(self):
        frame = self.camera.frame
        self.space = Space(1 / self.camera.frame_rate, [0, 0])
        self.add(self.space)
        table = ImageMobject("/Users/ytj/manim-master/my_program/texture/billiard/billiard_table.png")
        table.scale(1.5)
        self.add(table)
        light = self.camera.light_source
        light.move_to(ORIGIN + OUT)

        self.add_kickoff()
        self.add_billiard()
        self.start_simulate()
        self.wait(3)

    def start_simulate(self):
        self.space.add_updater(step)

    def add_kickoff(self):
        kickoff_ball = Sphere(radius=self.size_factor * 0.5,
                              fill_color=WHITE,
                              gloss=0.8,
                              shadow=0.8).shift(LEFT * 3)

        kickoff_ball.body = pymunk.Body()
        kickoff_ball.body.position = \
            kickoff_ball.get_center()[0], \
            kickoff_ball.get_center()[1]
        kickoff_ball.body.velocity = self.kickoff_velocity
        kickoff_ball.shape = pymunk.Circle(
            kickoff_ball.body,
            kickoff_ball.get_width() / 2)
        kickoff_ball.shape.elasticity = 0.8
        kickoff_ball.shape.density = 1
        kickoff_ball.shape.friction = 1
        kickoff_ball.angle = 0

        self.space.add_body(kickoff_ball)
        kickoff_ball.add_updater(simulate)
        self.add(kickoff_ball)

    def add_billiard(self):
        self.billiard = VGroup()
        radius = 0.5 * self.size_factor
        for i in range(10):
            ball = billiard_ball(index=i, radius=radius).move_to(
                np.array([self.size_factor, self.size_factor, self.size_factor]) * self.fill_rule[i])

            ball.body = pymunk.Body()
            ball.body.position = \
                ball.get_center()[0], \
                ball.get_center()[1]
            ball.shape = pymunk.Circle(
                ball.body,
                ball.get_width() / 2)
            ball.shape.elasticity = 0.3
            ball.shape.density = 1
            ball.shape.friction = 1
            ball.angle = 0

            self.space.add_body(ball)
            ball.add_updater(simulate)
            self.billiard.add(ball)

        for i in range(len(self.billiard)):
            self.add(self.billiard[i])

##proof
class ReconstructTheQuestion(Scene):
    pass


class ParabolaProof(Scene):
    pass


def calculate_ellipse_para(KE, mass):
    return np.sqrt(2 * (KE / mass))


class EqualEnergyGraphProof(Scene):
    CONFIG = {"m1": 1,
              "m2": 2,
              "kinetic_energy": 3,
              "momentum": 3,
              "axes_config": {
                  "x_range": (-7, 7),
                  "y_range": (-4, 4)
              }
              }

    def get_axes(self, shape):
        self.axes = axes = NumberPlane(axis_config={
            "stroke_color": WHITE,
            "stroke_width": 1,
            "include_ticks": True,
            "include_tip": True
        },
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            x_range=self.axes_config["x_range"], y_range=self.axes_config["y_range"])
        self.add(axes)
        if shape == "ellipse":
            self.add(axes.get_axis_labels("v_{a}", "v_{b}"))
        if shape == "circle":
            self.add(axes.get_axis_labels("\sqrt{m_{a} } v_{a}", "\sqrt{m_{b} } v_{b}"))

    def add_para_tracker(self):
        self.KE = ValueTracker(self.kinetic_energy)
        self.MM = ValueTracker(self.momentum)

    def get_ee_graph(self, shape):
        if shape == "ellipse":
            a = self.a = calculate_ellipse_para(self.KE.get_value(), self.m1)
            b = self.b = calculate_ellipse_para(self.KE.get_value(), self.m2)
        if shape == "circle":
            a = self.a = b = self.b = np.sqrt(2 * self.KE.get_value())
        ee_graph = ParametricCurve(lambda t: self.axes.c2p(a * np.cos(t), b * np.sin(t)),
                                   t_range=(0, 2 * PI))
        return ee_graph

    def get_em_line(self, shape):
        if shape == "ellipse":
            side = np.sqrt(self.m1 ** 2 + self.m2 ** 2)
            cosine = self.m2 / side
            sine = -self.m1 / side
            centre = [self.momentum / (2 * self.m1), self.momentum / (2 * self.m2)]
            em_line = ParametricCurve(lambda t: np.array(
                [centre[0] + t * cosine,
                 centre[1] + t * sine,
                 0]), t_range=(-4, 4))
        if shape == "circle":
            side = self.m1 + self.m2
            cosine = np.sqrt(self.m2) / side
            sine = -np.sqrt(self.m1) / side
            centre = [self.momentum / (2 * np.sqrt(self.m1)), self.momentum / (2 * np.sqrt(self.m2))]
            em_line = ParametricCurve(lambda t: np.array(
                [centre[0] + t * cosine,
                 centre[1] + t * sine,
                 0]), t_range=(-8, 8))
        return em_line

    def get_colored_shape(self, shape):
        colored_shape = Circle()
        shape_outline = self.get_ee_graph(shape=shape)
        colored_shape.stretch_to_fit_width(2 * self.axes.c2p(self.a, 0)[0])
        colored_shape.stretch_to_fit_height(2 * self.axes.c2p(0, self.b)[1])
        colors_map = color_gradient([BLUE_A, BLUE], 50)
        index = int(50 * (self.a + self.b) / (self.axes_config["x_range"][1] + self.axes_config["y_range"][1]))
        colored_shape.set_style(fill_color=colors_map[index],
                                fill_opacity=0.5,
                                stroke_width=0)
        return VGroup(shape_outline, colored_shape)

    def cal_point_coordinate(self, shape):
        v1, v2 = sy.symbols("v1 v2")
        eq = [self.m1 * v1 ** 2 + self.m2 * v2 ** 2 - 2 * self.KE.get_value(),
              self.m1 * v1 + self.m2 * v2 - self.MM.get_value()]
        result = list(sy.nonlinsolve(eq, [v1, v2]))
        if len(result) == 1:
            result_only = result[0]
            point_only = np.array([result_only[0], result_only[1], 0])
            if shape == "ellipse":
                point_only = np.array([result_only[0], result_only[1], 0])
            if shape == "circle":
                point_only = np.array([result_only[0] * np.sqrt(self.m1), result_only[1] * np.sqrt(self.m2), 0])
            return [point_only, point_only]
        else:
            result_a, result_b = result[0], result[1]
            if shape == "ellipse":
                point_a = np.array([result_a[0], result_a[1], 0])
                point_b = np.array([result_b[0], result_b[1], 0])
            if shape == "circle":
                point_a = np.array([result_a[0] * np.sqrt(self.m1), result_a[1] * np.sqrt(self.m2), 0])
                point_b = np.array([result_b[0] * np.sqrt(self.m1), result_b[1] * np.sqrt(self.m2), 0])
            return [point_a, point_b]

    def get_intersection(self, shape):
        points = self.cal_point_coordinate(shape)
        point_a = Dot(points[0]).set_color(WHITE)
        point_b = Dot(points[1]).set_color(WHITE)
        return VGroup(point_a, point_b)

    def get_dashed_line(self, dot):
        centre = dot.get_center()
        l1 = DashedLine(centre, np.array([centre[0], 0, 0]))
        l2 = DashedLine(centre, np.array([0, centre[1], 0]))
        for l in [l1, l2]:
            l.set_style(stroke_opacity=0.8)
        return VGroup(l1, l2)

    def get_assistance(self, dots):
        lines = VGroup()
        for i in range(2):
            x_t = RegularPolygon(n=3, start_angle=TAU / 4)
            y_t = RegularPolygon(n=3, start_angle=TAU / 2) if i == 0 else RegularPolygon(n=3, start_angle=0)
            for j in [x_t, y_t]:
                j.set_style(fill_color=WHITE, fill_opacity=0.8, stroke_opacity=0).scale(0.1)
            x_t.move_to(np.array([dots[i].get_center()[0], -0.1, 0]))
            y_t.move_to(np.array([0.1, dots[i].get_center()[1], 0]) if i == 0 else np.array([-0.1, dots[i].get_center()[1], 0]))
            line = VGroup(self.get_dashed_line(dots[i]), x_t, y_t)
            lines.add(line)
        return lines

class EqualEnergyEllipseProof(EqualEnergyGraphProof):
    CONFIG = {"m1": 2,
              "m2": 4,
              "kinetic_energy": 6,
              "momentum": 6
              }

    def construct(self):
        self.get_axes("ellipse")
        self.add_para_tracker()
        ee_ellipse = self.get_colored_shape("ellipse")
        em_line = self.get_em_line("ellipse")
        points = self.get_intersection("ellipse")
        lines = self.get_assistance(points)

        self.play(Write(ee_ellipse))
        self.play(Write(em_line))
        self.play(FadeIn(points), FadeIn(lines))
        points.add_updater(lambda m: m.become(self.get_intersection("ellipse")))
        lines.add_updater(lambda m: m.become(self.get_assistance(points)))
        ee_ellipse.add_updater(lambda m: m.become(self.get_colored_shape("ellipse")))
        self.play(ApplyMethod(self.KE.set_value, 3))
        self.play(ApplyMethod(self.KE.set_value, 9), run_time=2)


# transformation: v_ = sqrt(m) * v
class EqualEnergyCircleProof(EqualEnergyGraphProof):
    CONFIG = {"m1": 1,
              "m2": 2,
              "kinetic_energy": 3,
              "momentum": 3
              }

    def construct(self):
        self.get_axes("circle")
        self.add_para_tracker()
        ee_circle = self.get_colored_shape("circle")
        em_line = self.get_em_line("circle")
        points = self.get_intersection("circle")

        self.play(Write(ee_circle))
        self.play(Write(em_line))
        self.play(FadeIn(points))
        points.add_updater(lambda m: m.become(self.get_intersection("circle")))
        ee_circle.add_updater(lambda m: m.become(self.get_colored_shape("circle")))
        self.play(ApplyMethod(self.KE.set_value, 1.5))
