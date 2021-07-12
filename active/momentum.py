import numpy as np
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
                                  shadow=0.8), f"/Users/ytj/manim-master/my_program/texture/billiard/ball{index+1}_texture.png")
    ball.rotate(angle=PI/2, axis=UP).rotate(angle=PI/2, axis=OUT)
    return ball

class BilliardTable(SGroup):
    CONFIG = {
        "opacity": 1,
        "gloss": 0.5,
        "square_resolution": (2, 2),
        "side_length": 2,
    }

    def init_points(self):
        for vect in [OUT, RIGHT, UP, LEFT, DOWN, IN]:
            face = Square3D(resolution=self.square_resolution)
            face = TexturedSurface(face,
                                   image_file="/Users/ytj/manim-master/my_program/texture/billiard/billiardtable_light.png",
                                   dark_image_file="/Users/ytj/manim-master/my_program/texture/billiard/billiardtable_dark.png")
            face.shift(OUT)
            face.apply_matrix(z_to_vector(vect))
            self.add(face)
        self.set_height(self.side_length)

#TODO squished billiard
class BilliardCollision(ThreeDScene):
    CONFIG = {
        "size_factor": 0.5,
        "kickoff_velocity": [20, 0],
        "fill_rule": [
                    [0, 0, 0],
                    [np.sqrt(3)/2, 1 / 2, 0],
                    [np.sqrt(3)/2, -1 / 2, 0],
                    [np.sqrt(3), 1, 0],
                    [np.sqrt(3), 0, 0],
                    [np.sqrt(3), -1, 0],
                    [3 * np.sqrt(3)/2, 3 / 2, 0],
                    [3 * np.sqrt(3)/2, 1 / 2, 0],
                    [3 * np.sqrt(3)/2, -1 / 2, 0],
                    [3 * np.sqrt(3)/2, -3 / 2, 0]]}

    def construct(self):
        frame = self.camera.frame
        self.space = Space(1 / self.camera.frame_rate, [0, 0])
        self.add(self.space)
        light = self.camera.light_source
        light.move_to(ORIGIN + OUT*3)

        self.add_kickoff()
        self.add_billiard()
        self.add_boundary()
        self.start_simulate()
        self.wait(3)
        self.play(frame.set_euler_angles, {"theta": 30 * DEGREES, "phi": 60 * DEGREES}, run_time=2)

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
            ball = billiard_ball(index=i, radius=radius).move_to(np.array([self.size_factor, self.size_factor, self.size_factor]) * self.fill_rule[i])

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

    def add_boundary(self):
        size_list = [[10, 0.5], [10, 0.5], [0.5, 6.5], [0.5, 6.5]]
        position_list = [np.array([0, 3, 0]), np.array([0, -3, 0]), np.array([-5.25, 0, 0]), np.array([5.25, 0, 0])]
        for i in range(4):
            sample = Cube()
            w, h = 1, 1
            vs = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
            sample.move_to(position_list[i])
            sample.body = self.space.space.static_body
            sample.shape = pymunk.Segment(sample.body, )
            sample.shape.elasticity = 0.99
            sample.shape.friction = 0.8
            self.add(sample)
            self.space.add_body(sample)

##proof
class ReconstructTheQuestion(Scene):
    pass

class ParabolaProof(Scene):
    pass

def calculate_ellipse_para(KE, mass):
    return np.sqrt(2 * (KE / mass))

class EqualEnergyGraphProof(Scene):
    CONFIG = {"init_ela": 1,
              "init_a2b": 5 / 3,
              "m1": 1,
              "m2": 2,
              "KE": 3,
              "MM": 3
              }

    def get_axes(self):
        self.axes = axes = Axes((-5, 5), (-3, 3))
        self.add(axes)

    def calc_ellipse_para(self):
        a = self.a = calculate_ellipse_para(self.KE, self.m1)
        b = self.b = calculate_ellipse_para(self.KE, self.m2)

    def add_para_tracker(self):
        self.ela_factor = ValueTracker(self.init_ela)

    def get_ee_graph(self):
        ee_graph = ParametricCurve(lambda t: self.ela_factor.get_value() *
                                             self.axes.c2p(self.a * np.cos(t), self.b * np.sin(t)),
                                             t_range=(0, 2 * PI))
        return ee_graph

    def get_em_line(self):
        side = np.sqrt(self.m1 **2 + self.m2 **2)
        cosine = self.m2 / side
        sine = -self.m1 / side
        centre = [self.MM/(2 * self.m1), self.MM/(2 * self.m2)]
        em_line = ParametricCurve(lambda t: np.array(
            [centre[0] + t * cosine,
             centre[1] + t * sine,
             0]), t_range=(-4, 4))
        return em_line

class EqualEnergyEllipseProof(EqualEnergyGraphProof):
    CONFIG = {"m1": 2,
              "m2": 2}

    def construct(self):
        self.get_axes()
        self.add_para_tracker()
        self.calc_ellipse_para()
        ee_ellipse = self.get_ee_graph()
        em_line = self.get_em_line()
        self.play(Write(ee_ellipse))
        self.play(Write(em_line))
        ee_ellipse.add_updater(lambda m: m.become(self.get_ee_graph()))
        self.play(ApplyMethod(self.ela_factor.set_value, 0.5))