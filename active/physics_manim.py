from manimlib import *
import pymunk


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


def step(space, dt):
    space.space.step(dt)


def simulate(b):
    x, y = b.body.position
    b.move_to(x * RIGHT + y * UP)
    b.rotate(b.body.angle - b.angle)
    b.angle = b.body.angle


class PhysicTest(Scene):
    def construct(self):
        space = Space(1 / self.camera.frame_rate)
        self.add(space)

        circle = Circle().shift(UP)
        circle.set_fill(RED, 1)
        circle.shift(DOWN + RIGHT)

        circle.body = pymunk.Body()
        circle.body.position = \
            circle.get_center()[0], \
            circle.get_center()[1]
        circle.shape = pymunk.Circle(
            circle.body,
            circle.get_width() / 2)
        circle.shape.elasticity = 0.8
        circle.shape.density = 1
        circle.angle = 0

        rect = Square().shift(UP)
        rect.rotate(PI/4)
        rect.set_fill(YELLOW_A, 1)
        rect.shift(UP*2)
        rect.scale(0.5)

        rect.body = pymunk.Body()
        rect.body.position = \
            rect.get_center()[0], \
            rect.get_center()[1]
        rect.body.angle = PI / 4
        rect.shape = pymunk.Poly.create_box(rect.body, (1, 1))
        rect.shape.elasticity = 0.4
        rect.shape.density = 2
        rect.shape.friction = 0.8
        rect.angle = PI / 4

        ground = Rectangle(20, 0.1)
        ground.shift(3*DOWN)
        ground.body = space.space.static_body
        ground.shape = pymunk.Segment(ground.body, (-10, -3), (10, -3), 0.1)
        ground.shape.elasticity = 0.99
        ground.shape.friction = 0.8
        self.add(ground)

        wall1 = Rectangle(0.1, 10)
        wall1.shift(4*LEFT)
        wall1.body = space.space.static_body
        wall1.shape = pymunk.Segment(wall1.body, (-4, -5), (-4, 5), 0.1)
        wall1.shape.elasticity = 0.99
        self.add(wall1)

        wall2 = Rectangle(0.1, 10)
        wall2.shift(4*RIGHT)
        wall2.body = space.space.static_body
        wall2.shape = pymunk.Segment(wall2.body, (4, -5), (4, 5), 0.1)
        wall2.shape.elasticity = 0.99
        self.add(wall2)

        self.play(
            DrawBorderThenFill(circle),
            DrawBorderThenFill(rect))
        self.wait()

        space.add_body(circle)
        space.add_body(rect)
        space.add_body(ground)
        space.add_body(wall1)
        space.add_body(wall2)
        space.add_updater(step)
        circle.add_updater(simulate)
        rect.add_updater(simulate)
        self.wait(10)


class TextTest(Scene):
    def construct(self):
        space = Space(1 / self.camera.frame_rate)
        self.add(space)
        space.add_updater(step)

        ground = Line(5*LEFT + 3 * DOWN, 5*RIGHT+3*DOWN)
        self.play(ShowCreation(ground))
        ground.body = space.space.static_body
        ground.shape = pymunk.Segment(ground.body, (-5, -3), (5, -3), 0.05)
        ground.shape.elasticity = 0.9
        ground.shape.friction = 0.8
        space.add_body(ground)

        def add_physic(text):
            parts = text.family_members_with_points()
            for p in parts:
                self.add(p)
                p.body = pymunk.Body()
                p.body.position = \
                    p.get_center()[0], \
                    p.get_center()[1]
                p.shape = pymunk.Poly.create_box(
                    p.body, (p.get_width(), p.get_height()))
                p.shape.elasticity = 0.4
                p.shape.density = 1
                p.shape.friction = 0.8

                p.angle = 0
                space.add_body(p)
                p.add_updater(simulate)

        forms = [
            r"a^2-b^2=(a+b)(a-b)",
            r"x_{1,2}=\frac{-b\pm \sqrt{b^2-4ac}}{2a}",
            r"e^{i\pi}+1=0",
            r"\cos(x+y)=\cos x \cos y - \sin x \sin y",
            r"e^x=\sum_{i=0}^\infty \frac{x^i}{i!}"
        ]

        for f in forms:
            text = Tex(f)
            self.play(Write(text))
            self.remove(text)
            add_physic(text)

            self.wait(5)

class ThreeBalls(Scene):
    def construct(self):
        space = Space(1 / self.camera.frame_rate)
        self.add(space)

        circle_1 = Circle()
        circle_1.set_fill(RED, 1)
        circle_1.shift(DOWN + RIGHT)

        circle_1.body = pymunk.Body()
        circle_1.body.position = \
            circle_1.get_center()[0], \
            circle_1.get_center()[1]
        circle_1.body.velocity = [-3., 3.]
        circle_1.shape = pymunk.Circle(
            circle_1.body,
            circle_1.get_width() / 2)
        circle_1.shape.elasticity = 0.8
        circle_1.shape.density = 1
        circle_1.angle = 0

        circle_2 = Circle()
        circle_2.set_fill(RED, 1)
        circle_2.shift(DOWN + LEFT)

        circle_2.body = pymunk.Body()
        circle_2.body.position = \
            circle_2.get_center()[0], \
            circle_2.get_center()[1]
        circle_2.body.velocity = [3., 3.]
        circle_2.shape = pymunk.Circle(
            circle_2.body,
            circle_2.get_width() / 2)
        circle_2.shape.elasticity = 0.8
        circle_2.shape.density = 1
        circle_2.angle = 0

        circle_3 = Circle()
        circle_3.set_fill(RED, 1)
        circle_3.shift(UP)

        circle_3.body = pymunk.Body()
        circle_3.body.position = \
            circle_3.get_center()[0], \
            circle_3.get_center()[1]
        circle_3.shape = pymunk.Circle(
            circle_3.body,
            circle_3.get_width() / 2)
        circle_3.shape.elasticity = 0.8
        circle_3.shape.density = 1
        circle_3.angle = 0

        ground = Rectangle(20, 0.1)
        ground.shift(3 * DOWN)
        ground.body = space.space.static_body
        ground.shape = pymunk.Segment(ground.body, (-10, -3), (10, -3), 0.1)
        ground.shape.elasticity = 0.99
        ground.shape.friction = 0.8
        self.add(ground)

        wall1 = Rectangle(0.1, 10)
        wall1.shift(4 * LEFT)
        wall1.body = space.space.static_body
        wall1.shape = pymunk.Segment(wall1.body, (-4, -5), (-4, 5), 0.1)
        wall1.shape.elasticity = 0.99
        self.add(wall1)

        wall2 = Rectangle(0.1, 10)
        wall2.shift(4 * RIGHT)
        wall2.body = space.space.static_body
        wall2.shape = pymunk.Segment(wall2.body, (4, -5), (4, 5), 0.1)
        wall2.shape.elasticity = 0.99
        self.add(wall2)

        self.play(
            DrawBorderThenFill(circle_1),
            DrawBorderThenFill(circle_2),
            DrawBorderThenFill(circle_3))
        self.wait()

        space.add_body(circle_1)
        space.add_body(circle_2)
        space.add_body(circle_3)
        space.add_body(ground)
        space.add_body(wall1)
        space.add_body(wall2)
        space.add_updater(step)
        circle_1.add_updater(simulate)
        circle_2.add_updater(simulate)
        circle_3.add_updater(simulate)
        self.wait(10)