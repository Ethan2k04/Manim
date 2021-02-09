from manimlib.imports import *
from math import *

class Introduction(Scene):
    pass

class CoordinateGradScene(ThreeDScene):
    CONFIG = {
        "axes_config": {
            "x_min": 0,
            "x_max": 6.5,
            "y_min": 0,
            "y_max": 6.5,
            "z_min": 0,
            "z_max": 3.5,
            "dash_line_config": {
                "dash_opacity": 0.3
            }
        },
        "default_surface_config": {
            "u_min": 0,
            "u_max": 6,
            "v_min": 0,
            "v_max": 6,
            "fill_opacity": 0.8,
            "checkerboard_colors": [BLUE_D,BLUE_E],
            "stroke_width": 0.5,
            "stroke_color": WHITE,
            "stroke_opacity": 0.5,
            "length_of_output": 100
              },
        "default_graph_style": {
            "stroke_width": 4,
            "stroke_color": ORANGE
        },
        "dot_and_height": {
            "radius": 0.3,
            "color": PURPLE,
            "width": 3
        }
    }

    def get_3d_axes(self, include_labels=True, include_numbers=False, **kwargs):
        config = dict(self.axes_config)
        config.update(kwargs)
        axes = ThreeDAxes(**config)
        axes.set_stroke(width=2)

        if include_numbers:
            self.add_axes_numbers(axes)

        if include_labels:
            self.add_axes_labels(axes)

        dash_surface_xy = self.get_dash_surface(axes, "xy")
        dash_surface_yz = self.get_dash_surface(axes, "yz")
        dash_surface_xz = self.get_dash_surface(axes, "xz")
        dash_surface = VGroup(dash_surface_xy, dash_surface_yz, dash_surface_xz)
        axes.add(dash_surface)

        return axes

    def get_dash_surface(self, axes, direction):
        dash_surface = VGroup()
        dash_opacity = 0.3
        if direction == "xy":
            end_a = ceil(self.axes_config["x_max"])
            end_b = ceil(self.axes_config["y_max"])
            for i in range(1, end_a):
                dash = DashedLine(start=axes.c2p(i, 0, 0),
                                  end=axes.c2p(i, end_b-1, 0)).set_opacity(dash_opacity)
                dash_surface.add(dash)
            for i in range(1, end_b):
                dash = DashedLine(start=axes.c2p(0, i, 0),
                                  end=axes.c2p(end_a-1, i, 0)).set_opacity(dash_opacity)
                dash_surface.add(dash)
        if direction == "yz":
            end_a = ceil(self.axes_config["y_max"])
            end_b = ceil(self.axes_config["z_max"])
            for i in range(1, end_a):
                dash = DashedLine(start=axes.c2p(0, i, 0),
                                  end=axes.c2p(0, i, end_b-1)).set_opacity(dash_opacity)
                dash_surface.add(dash)
            for i in range(1, end_b):
                dash = DashedLine(start=axes.c2p(0, 0, i),
                                  end=axes.c2p(0, end_a-1, i)).set_opacity(dash_opacity)
                dash_surface.add(dash)
        if direction == "xz":
            end_a = ceil(self.axes_config["x_max"])
            end_b = ceil(self.axes_config["z_max"])
            for i in range(1, end_a):
                dash = DashedLine(start=axes.c2p(i, 0, 0),
                                  end=axes.c2p(i, 0, end_b-1)).set_opacity(dash_opacity)
                dash_surface.add(dash)
            for i in range(1, end_b):
                dash = DashedLine(start=axes.c2p(0, 0, i),
                                  end=axes.c2p(end_a-1, 0, i)).set_opacity(dash_opacity)
                dash_surface.add(dash)

        return dash_surface

    def add_axes_labels(self, axes):
        x_label = TexMobject("x")
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        axes.x_axis.label = x_label

        y_label = TextMobject("y")
        y_label.rotate(90 * DEGREES, OUT)
        y_label.next_to(axes.y_axis.get_end(), UP)
        axes.y_axis.label = y_label

        z_label = TextMobject("z")
        z_label.rotate(-90 * DEGREES, RIGHT)
        z_label.next_to(axes.z_axis.get_zenith(), RIGHT)
        axes.z_axis.label = z_label
        for axis in axes:
            axis.add(axis.label)
        return axes

    @staticmethod
    def add_axes_numbers(axes):
        x_axis = axes.x_axis
        y_axis = axes.y_axis

        x_axis.add_numbers()
        y_axis.add_numbers()
        #for number in y_axis.numbers:
            #number.rotate(90 * DEGREES)
        return axes

    def get_time_slice_graph(self, axes, func, b, **kwargs):
        config = dict()
        config.update(self.default_graph_style)
        config.update({
            "t_max": 0 if b <= self.default_surface_config["u_max"] else b - self.default_surface_config["u_max"],
            "t_min": b if b <= self.default_surface_config["u_max"] else self.default_surface_config["u_max"],
        })
        config.update(kwargs)
        return ParametricFunction(
            lambda x: axes.c2p(
                x, -x+b, func(x, -x+b)
            ),
            **config,
        )

    def get_initial_state_graph(self, axes, func, **kwargs):
        return self.get_time_slice_graph(
            axes,
            func,
            b= 7,
            **kwargs
        )

    def get_surface(self, axes, func, **kwargs):
        config = {
            "resolution": (50, 50),
        }
        config.update(self.default_surface_config)
        config.update(kwargs)
        return ParametricSurface(
            lambda x, y: axes.c2p(
                x, y, func(x, y)
            ),
            **config
        )

    def get_colored_surface(self, surface, func, axes, **kwargs):
        x, y = np.linspace(axes.x_min, axes.x_max, 50), np.linspace(axes.y_min, axes.y_max, 50)
        z = func(x, y)
        z_1 = max(z) - min(z)
        colors = color_gradient([PURPLE_E, RED, ORANGE, YELLOW, GREEN], 100)
        corlored_surface = surface.copy()
        for ff in corlored_surface:
            f_z = axes.p2c(ff.get_center())[-1]
            ff.set_color(colors[int(((f_z - min(z)) / z_1) * 100)])
        return corlored_surface

    def get_height(self, func, axes, x_value, y_value, **kwargs):
        config = dict()
        config.update(self.default_graph_style)
        config.update({
            "t_min": 0,
            "t_max": func(x_value, y_value),
            "stroke_color": ORANGE
        })
        config.update(kwargs)
        #label = TexMobject("f(x,y)", "=", "0").set_color(YELLOW)
        #label.rotate(PI/2).rotate(PI/2, UP).rotate(PI/4).move_to(height.get_center()).shift(UL*0.5)
        return ParametricFunction(
            lambda t: axes.c2p(
                x_value, y_value, t
            ), **config
        )

    def get_assist_xy_line(self, axes, point, color, **kwargs):
        p = np.array([point.get_x(), point.get_y(), 0])
        x_value, y_value = axes.p2c(p)[0], axes.p2c(p)[1]
        l_x = DashedLine(start=axes.c2p(
                x_value, 0, 0), end=axes.c2p(x_value, y_value, 0)).set_color(color)

        l_y = DashedLine(start=axes.c2p(
                0, y_value, 0), end=axes.c2p(x_value, y_value, 0)).set_color(color)

        return VGroup(l_x, l_y)

    def get_point(self, func, axes, x, y):
        point = Sphere(radius=0.1).set_color(ORANGE)
        point.add_updater(
            lambda m: m.move_to(axes.c2p(x.get_value(), y.get_value(),
                                         func(x.get_value(), y.get_value())))
        )
        return point

    def get_indicate_vetor(self, point):
        vector = ThreeDVector().set_direction([0, 0, -1]).set_color(ORANGE)
        vector.next_to(point, OUT, buff=0.25)
        return vector

    def get_input_triangle(self, axes, x_value, y_value, color):
        x_triangle = RegularPolygon(n=3, start_angle=TAU / 4).set_fill(color, 1).set_stroke(width=0).scale(0.1)
        y_triangle = RegularPolygon(n=3, start_angle=0).set_fill(color, 1).set_stroke(width=0).scale(0.1)
        x_triangle.move_to(axes.c2p(x_value, 0, 0))
        y_triangle.move_to(axes.c2p(0, y_value, 0))
        return VGroup(x_triangle, y_triangle)

    def get_2d_input_point(self, axes, x, y, color):
        dot = Dot(axes.c2p(x.get_value(), y.get_value(), 0))
        dot.set_color(color)
        dot.add_updater(
            lambda m: m.move_to(axes.c2p(x.get_value(), y.get_value()))
        )
        return dot

    def get_output_decimal(self, height, func, x_value, y_value):
        maximum = func(3, 3)
        value = DecimalNumber(func(x_value, y_value))
        value.rotate(PI/2).rotate(PI/2, UP).rotate(- PI/4)
        value.set_color(ORANGE)
        value.add_background_rectangle(stroke_color=ORANGE)
        value.next_to(height, OUT)

        return value

class SceneOneText1(Scene):
    def construct(self):
        text = Text("约束条件:", font="Source Han Sans CN").set_color(WHITE)
        tex = TexMobject("g(x,y)", "=", "0").set_color(YELLOW)
        word = VGroup(text, tex).arrange(RIGHT)
        word.move_to(ORIGIN)
        self.play(Write(word))
        self.wait(15)

class SceneOneText2(Scene):
    def construct(self):
        text_1 = Text("在约束条件下是一条", font="Source Han Sans CN").set_color(WHITE)
        text_2 = Text("曲线", font="Source Han Sans CN").set_color(ORANGE)
        tex = TexMobject("f(x,y)").set_color(ORANGE)
        word = VGroup(tex, text_1, text_2).arrange(RIGHT)
        word.move_to(ORIGIN)
        self.play(Write(word))
        self.wait(15)

class ShowTwoVariablesFunction(CoordinateGradScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 60,
              "theta": 60 * DEGREES,
              "distance": 200,
              }

    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        axes = self.get_3d_axes(include_numbers=True).move_to(ORIGIN)
        func = self.func()
        original_surface = self.get_surface(axes, func)
        y_lable = axes.y_axis.label
        y_lable.rotate(-PI/2)

        x = ValueTracker(3)
        y = ValueTracker(3)

        colored_surface = self.get_colored_surface(original_surface, func, axes)
        output_point = self.get_point(func, axes, x, y)
        assist_line = self.get_assist_xy_line(axes, output_point, GREEN)
        input_tri = self.get_input_triangle(axes, x.get_value(), y.get_value(), GREEN)
        dot = self.get_2d_input_point(axes, x, y, ORANGE)

        x_decimal = DecimalNumber(0).add_updater(
            lambda m: m.set_value(x.get_value())
        ).set_color(GREEN)
        y_decimal = DecimalNumber(0).add_updater(
            lambda m: m.set_value(y.get_value())
        ).set_color(GREEN)
        #font = "Hannotate SC"
        left_bracket = TexMobject("(").set_color(GREEN)
        comma = TexMobject(",").set_color(GREEN)
        right_bracket = TexMobject(")").set_color(GREEN)
        decimal_input = VGroup(left_bracket, x_decimal, comma, y_decimal, right_bracket).arrange(RIGHT)

        left_bracket.shift(RIGHT*0.25)
        x_decimal.shift(RIGHT*0.125)
        comma.shift(DOWN*0.25)
        y_decimal.shift(LEFT*0.125)
        right_bracket.shift(LEFT*0.25)

        decimal_input.add_background_rectangle(stroke_color=GREEN)
        decimal_input.add_updater(lambda m: m.next_to(dot, UR, buff=0.125))

        self.play(FadeInFromLarge(axes, 0.3))
        output_line = self.get_height(func, axes, x.get_value(), y.get_value())
        self.play(FadeIn(dot), FadeIn(input_tri), FadeIn(assist_line), FadeIn(output_line), FadeInFromLarge(output_point, 0.3))
        assist_line.add_updater(
            lambda m: m.become(self.get_assist_xy_line(
                axes, dot, GREEN
            ))
        )
        input_tri.add_updater(
            lambda m: m.become(self.get_input_triangle(
                axes, x.get_value(), y.get_value(), GREEN
            ))
        )
        output_line.add_updater(
            lambda m: m.become(self.get_height(
                func, axes, x.get_value(), y.get_value()
            ))
        )
        #value = self.get_output_decimal(output_line, func, x.get_value(), y.get_value())
        #self.play(Write(decimal_input), run_time=0.5)
        self.wait()
        self.play(ApplyMethod(x.set_value, 1), ApplyMethod(y.set_value, 5))
        self.wait()
        self.play(ApplyMethod(x.set_value, 2), ApplyMethod(y.set_value, 1))
        self.wait()
        self.play(ApplyMethod(x.set_value, 5), ApplyMethod(y.set_value, 4))
        self.wait(3)
        #self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES)

        # value.add_updater(
        #     lambda m: m.become(self.get_output_decimal(output_line, func, x.get_value(), y.get_value()))
        # )

        point_group = VGroup()

        x_fake, y_fake = np.linspace(axes.x_min, axes.x_max, 50), np.linspace(axes.y_min, axes.y_max, 50)
        z_fake = func(x_fake, y_fake)
        z_1 = max(z_fake) - min(z_fake)
        colors = color_gradient([PURPLE_E, RED, ORANGE, YELLOW, GREEN], 100)

        self.play(FadeOut(value), FadeOut(decimal_input))
        self.begin_ambient_camera_rotation(-0.04)

        for i in range(13):
            for j in range(13):
                self.play(ApplyMethod(x.set_value, 0.5 * (i)), ApplyMethod(y.set_value, 0.5 * (j)), run_time=0.05, rate_func=linear)
                point_ = output_point.copy().clear_updaters()
                f_z = axes.p2c(point_.get_center())[-1]
                point_.set_color(colors[int(((f_z - min(z_fake)) / z_1) * 99)])
                point_group.add(point_)
                self.add(point_)
        
        self.wait()
        self.play(FadeOut(point_group), FadeOut(output_point), FadeOut(output_line), FadeOut(assist_line), FadeOut(dot),
                  FadeOut(input_tri), FadeIn(colored_surface))
        self.wait(2)
        self.stop_ambient_camera_rotation()
        # self.play(ApplyMethod(colored_surface.set_opacity, 0.4))
        # self.move_camera(phi=0, theta=-PI/2)

    @staticmethod
    def func():
        return lambda u, v: 3.5 * np.exp(-(((u-3)/2)**2+0.25*((u-3)/2)*((v-3)/2)+((v-3)/2)**2))

class ShowGraphAndConditionSurface_2D(CoordinateGradScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 60 * DEGREES,
              "theta": 60 * DEGREES,
              "distance": 200,
              }

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-PI/2, distance=self.distance)
        axes = self.get_3d_axes(include_numbers=True).move_to(ORIGIN)
        func = self.func()

        # text = Text("约束条件:", font="Source Han Sans CN").set_color(WHITE)
        # tex = TexMobject("g(x,y)", "=", "0").set_color(YELLOW)
        # word = VGroup(text, tex).arrange(RIGHT)
        # tex.next_to(axes, DOWN, buff=0.5)

        b = ValueTracker(7)
        x = ValueTracker(1)
        y = ValueTracker(6)

        original_surface = self.get_surface(axes, func)
        colored_surface = self.get_colored_surface(original_surface, func, axes)
        colored_surface.set_opacity(0.2)
        condition_line_1 = ParametricFunction(lambda t: axes.c2p(t, -t + b.get_value(), 0), t_min=6, t_max=1).set_color(YELLOW)
        condition_line_2 = ParametricFunction(lambda t: axes.c2p(t, 6/t, 0), t_min=1, t_max=6).set_color(YELLOW)
        condition_line_3 = ParametricFunction(lambda t: axes.c2p(4 + 2 * np.cos(t), 4 + 2 * np.sin(t), 0), t_min=0, t_max=PI*2).set_color(YELLOW)

        y_label = axes.y_axis.label
        y_label.rotate(-PI / 2)

        point = self.get_point(func, axes, x, y)
        dot = self.get_2d_input_point(axes, x, y, GREEN)
        height = self.get_height(func, axes, x.get_value(), y.get_value())
        assist_line = self.get_assist_xy_line(axes, dot, color=GREEN)
        input_label = self.get_input_triangle(axes, x.get_value(), y.get_value(), GREEN)
        x_decimal = DecimalNumber(0).add_updater(
            lambda m: m.set_value(x.get_value())
        ).set_color(GREEN)
        y_decimal = DecimalNumber(0).add_updater(
            lambda m: m.set_value(y.get_value())
        ).set_color(GREEN)
        # font = "Hannotate SC"
        left_bracket = TexMobject("(").set_color(GREEN)
        comma = TexMobject(",").set_color(GREEN)
        right_bracket = TexMobject(")").set_color(GREEN)
        decimal_input = VGroup(left_bracket, x_decimal, comma, y_decimal, right_bracket).arrange(RIGHT)

        left_bracket.shift(RIGHT * 0.25)
        x_decimal.shift(RIGHT * 0.125)
        comma.shift(DOWN * 0.25)
        y_decimal.shift(LEFT * 0.125)
        right_bracket.shift(LEFT * 0.25)
        decimal_input.add_background_rectangle(stroke_color=GREEN)

        self.add(axes)
        self.add(colored_surface)
        self.add(dot, input_label, assist_line, decimal_input)
        #self.play(FadeIn(height), FadeIn(point))
        self.add(condition_line_1)

        height.add_updater(
            lambda m: m.become(self.get_height(
                func, axes, x.get_value(), y.get_value()
            ))
        )
        assist_line.add_updater(
            lambda m: m.become(self.get_assist_xy_line(
                axes, dot, GREEN
            ))
        )
        input_label.add_updater(
            lambda m: m.become(self.get_input_triangle(
                axes, x.get_value(), y.get_value(), GREEN
            ))
        )
        decimal_input.add_updater(lambda m: m.next_to(dot, UR, buff=0.125))

        self.play(ApplyMethod(x.set_value, 6), ApplyMethod(y.set_value, 1), rate_func=there_and_back, run_time=4)
        self.wait(3)
        self.play(ApplyMethod(x.set_value, 6), ApplyMethod(y.set_value, 1), rate_func=linear, run_time=4)
        # condition_plane.add_updater(
        #     lambda m: m.move_to(axes.c2p(b.get_value() / 2, b.get_value() / 2, self.axes_config["z_max"] / 2))
        # )

        condition_line_1_c = condition_line_1.copy()

        self.wait()
        self.play(ReplacementTransform(condition_line_1, condition_line_2), ApplyMethod(x.set_value, np.sqrt(6)), ApplyMethod(y.set_value, np.sqrt(6)))
        self.wait(2)
        self.play(ReplacementTransform(condition_line_2, condition_line_3), ApplyMethod(x.set_value, 4 - np.sqrt(2)), ApplyMethod(y.set_value, 4 - np.sqrt(2)))
        self.wait(2)
        self.play(ReplacementTransform(condition_line_3, condition_line_1_c), ApplyMethod(x.set_value, 1), ApplyMethod(y.set_value, 6))
        self.wait(3)
        # condition_curve.add_updater(
        #     lambda m: m.become(self.get_time_slice_graph(
        #         axes,
        #         func, b.get_value()))
        # )
        self.play(ApplyMethod(x.set_value, 6), ApplyMethod(y.set_value, 1), rate_func=linear, run_time=4)
        self.wait()
        self.play(ApplyMethod(x.set_value, 3.5), ApplyMethod(y.set_value, 3.5), rate_func=smooth, run_time=1)
        self.wait()
        self.play(Flash(decimal_input.get_center()))
        self.wait(6)
        # vector = Vector(np.array([-1, -1, 0])).set_color(ORANGE)
        # vector.next_to(dot, UR)
        # self.play(FadeIn(vector))
        # for i in range(3):
        #     vector.shift(0.5 * DL, run_time=0.5)
        # self.wait(2)
        #self.begin_ambient_camera_rotation(rate=PI / 12)

    @staticmethod
    def func():
        return lambda u, v: 3.5 * np.exp(-(((u-3)/2)**2+0.25*((u-3)/2)*((v-3)/2)+((v-3)/2)**2))

class ShowGraphAndConditionSurface_3D(CoordinateGradScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 60 * DEGREES,
              "theta": 60 * DEGREES,
              "distance": 200,
              }

    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        axes = self.get_3d_axes(include_numbers=True).move_to(ORIGIN)
        func = self.func()

        # text_1 = Text("在约束条件下的", font="Source Han Sans CN").set_color(WHITE)
        # text_2 = Text("极值", font="Source Han Sans CN").set_color(ORANGE)
        # tex = TexMobject("f(x,y)").set_color(YELLOW)
        # word = VGroup(tex, text_1, text_2).arrange(RIGHT)
        # self.add_fixed_in_frame_mobjects(word)
        # word.to_edge(DOWN, buff=0.5)

        b = ValueTracker(7)
        x = ValueTracker(1)
        y = ValueTracker(6)

        original_surface = self.get_surface(axes, func)
        colored_surface = self.get_colored_surface(original_surface, func, axes)
        colored_surface.set_opacity(0.2)
        condition_curve_1 = self.get_initial_state_graph(axes, func)
        condition_curve_2 = ParametricFunction(lambda t: axes.c2p(t, 6 / t, func(t, 6 / t)), t_min=1, t_max=6).set_color(ORANGE)
        condition_curve_3 = ParametricFunction(lambda t: axes.c2p(4 + 2 * np.cos(t), 4 + 2 * np.sin(t), func(4 + 2 * np.cos(t), 4 + 2 * np.sin(t))), t_min=0,
                                               t_max=PI * 2).set_color(ORANGE)
        condition_line_1 = ParametricFunction(lambda t: axes.c2p(t, -t + b.get_value(), 0), t_min=6, t_max=1).set_color(YELLOW)
        condition_line_2 = ParametricFunction(lambda t: axes.c2p(t, 6 / t, 0), t_min=1, t_max=6).set_color(YELLOW)
        condition_line_3 = ParametricFunction(lambda t: axes.c2p(4 + 2 * np.cos(t), 4 + 2 * np.sin(t), 0), t_min=0,
                                              t_max=PI * 2).set_color(YELLOW)
        condition_plane = Rectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2,
        ).set_width(self.axes_config["x_max"] * sqrt(2)).set_height(self.axes_config["z_max"] + 0.5, stretch=True)
        condition_text = TexMobject("g(x,y)=", "0").set_color(YELLOW)
        condition_text.align_to(condition_plane, UP).align_to(condition_plane, RIGHT)
        condition_plane = VGroup(condition_plane, condition_text)
        condition_plane.rotate(90 * DEGREES, RIGHT).rotate(135 * DEGREES, OUT)
        condition_plane.move_to(axes.c2p(b.get_value()/2, b.get_value()/2, self.axes_config["z_max"]/2))

        point = self.get_point(func, axes, x, y)
        dot = self.get_2d_input_point(axes, x, y, GREEN)
        height = self.get_height(func, axes, x.get_value(), y.get_value())
        assist_line = self.get_assist_xy_line(axes, dot, color=GREEN)
        input_label = self.get_input_triangle(axes, x.get_value(), y.get_value(), GREEN)

        self.play(FadeIn(axes), FadeIn(colored_surface), FadeIn(condition_line_1), FadeIn(dot), FadeIn(input_label), FadeIn(assist_line))
        self.play(FadeInFromLarge(point, 0.3), ShowCreation(height))
        self.wait()
        #self.play(FadeIn(height), FadeIn(point))

        height.add_updater(
            lambda m: m.become(self.get_height(
                func, axes, x.get_value(), y.get_value()
            ))
        )
        assist_line.add_updater(
            lambda m: m.become(self.get_assist_xy_line(
                axes, dot, GREEN
            ))
        )
        input_label.add_updater(
            lambda m: m.become(self.get_input_triangle(
                axes, x.get_value(), y.get_value(), GREEN
            ))
        )

        condition_curve_1_c = condition_curve_1.copy()
        condition_line_1_c = condition_line_1.copy()

        self.play(ApplyMethod(x.set_value, 6), ApplyMethod(y.set_value, 1), ShowCreation(condition_curve_1), rate_func=linear, run_time=4)

        self.wait()
        self.play(ReplacementTransform(condition_line_1, condition_line_2), ReplacementTransform(condition_curve_1, condition_curve_2),
                  ApplyMethod(x.set_value, np.sqrt(6)), ApplyMethod(y.set_value, np.sqrt(6)))
        self.wait(2)
        self.play(ReplacementTransform(condition_line_2, condition_line_3),
                  ReplacementTransform(condition_curve_2, condition_curve_3),
                  ApplyMethod(x.set_value, 4 - np.sqrt(2)), ApplyMethod(y.set_value, 4 - np.sqrt(2)))
        self.wait(2)
        self.play(ReplacementTransform(condition_line_3, condition_line_1_c),
                  ReplacementTransform(condition_curve_3, condition_curve_1_c),
                  ApplyMethod(x.set_value, 6), ApplyMethod(y.set_value, 1))
        self.wait()
        self.play(FadeIn(condition_plane))
        # condition_plane.add_updater(
        #     lambda m: m.move_to(axes.c2p(b.get_value() / 2, b.get_value() / 2, self.axes_config["z_max"] / 2))
        # )
        self.play(ApplyMethod(x.set_value, 1), ApplyMethod(y.set_value, 6), rate_func=linear, run_time=4)
        self.wait()
        condition_curve_1.add_updater(
            lambda m: m.become(self.get_time_slice_graph(
                axes,
                func, b.get_value()))
        )

        self.play(ApplyMethod(x.set_value, 3.5), ApplyMethod(y.set_value, 3.5), rate_func=smooth, run_time=1)
        vector = self.get_indicate_vetor(point)
        self.play(FadeInFrom(vector, OUT))
        for i in range(3):
            self.play(ApplyMethod(vector.shift, IN*0.25), run_time=0.5, rate_func=there_and_back)

        vector.add_updater(
            lambda m: m.next_to(point, OUT, buff=0.25)
        )
        max_tex = TexMobject("f(x,y)_{max}").set_color(ORANGE). \
            rotate(90 * DEGREES, RIGHT).rotate(135 * DEGREES, OUT)
        max_tex.add_updater(
            lambda m: m.next_to(vector, OUT, buff=0.25)
        )

        self.play(Write(max_tex))
        self.wait(2)
        #self.begin_ambient_camera_rotation(rate=PI / 12)

    @staticmethod
    def func():
        return lambda u, v: 3.5 * np.exp(-(((u-3)/2)**2+0.25*((u-3)/2)*((v-3)/2)+((v-3)/2)**2))