from manimlib.imports import *

#utils
def get_charged_particles(color, sign, radius=0.1):
    result = Circle(
        stroke_color=WHITE,
        stroke_width=0.5,
        fill_color=color,
        fill_opacity=0.8,
        radius=radius
    )
    sign = TexMobject(sign)
    sign.set_stroke(WHITE, 1)
    sign.set_width(0.5 * result.get_width())
    sign.move_to(result)
    result.add(sign)
    return result

def coulomb_func(point, sources):  #由于代码书写规则，这里的kQ写成了kq
    k = 10
    x, y = point[:2]
    result = np.array([0., 0., 0.])
    for source in sources:
        kq = k * source[0]
        r = np.sqrt((x - source[1][0]) ** 2 + (y - source[1][1]) ** 2)
        r_min = max(0.01, r)
        norm = kq / (r_min ** 2)
        e = np.array([norm * ((x - source[1][0]) / r), norm * ((y - source[1][1]) / r), 0])
        result += e
    return result

def rate_func(decrease_factor=1):
    return lambda t: (1 / decrease_factor) * t ** 2

def opacity_func(decrease_factor=1, increase_factor=1):
    return lambda t: increase_factor * 1500 * (1 - abs(decrease_factor * t) ** 0.0001)

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
        text_mobject_kwargs = {
            "alignment": "",
            "arg_separator": self.quote_arg_separator,
        }
        if isinstance(self.quote, str):
            if self.use_quotation_marks:
                quote = TextMobject("``%s''" %
                                    self.quote.strip(), **text_mobject_kwargs)
            else:
                quote = TextMobject("%s" %
                                    self.quote.strip(), **text_mobject_kwargs)
        else:
            if self.use_quotation_marks:
                words = [self.text_size + " ``"] + list(self.quote) + ["''"]
            else:
                words = [self.text_size] + list(self.quote)
            quote = TextMobject(*words, **text_mobject_kwargs)
            # TODO, make less hacky
            if self.quote_arg_separator == " ":
                quote[0].shift(0.2 * RIGHT)
                quote[-1].shift(0.2 * LEFT)
        for term, color in self.highlighted_quote_terms.items():
            quote.set_color_by_tex(term, color)
        quote.to_edge(UP, buff=self.top_buff)
        if quote.get_width() > max_width:
            quote.set_width(max_width)
        return quote

    def get_author(self, quote):
        author = TextMobject(self.text_size + " --" + self.author)
        #author.next_to(quote, DOWN, buff=self.author_buff)
        author.to_edge(RIGHT, buff=LARGE_BUFF)
        author.to_edge(DOWN, buff=LARGE_BUFF)
        author.set_color(YELLOW)
        return author


#mobjects
class JigglingSubmobjects(VGroup):
    CONFIG = {
        "amplitude": 0.05,
        "jiggles_per_second": 1,
    }

    def __init__(self, group, **kwargs):
        VGroup.__init__(self, **kwargs)
        for submob in group.submobjects:
            submob.jiggling_direction = rotate_vector(
                RIGHT, np.random.random() * TAU,
            )
            submob.jiggling_phase = np.random.random() * TAU
            self.add(submob)
        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        for submob in self.submobjects:
            submob.jiggling_phase += dt * self.jiggles_per_second * TAU
            submob.shift(
                self.amplitude *
                submob.jiggling_direction *
                np.sin(submob.jiggling_phase) * dt
            )

class ChargedParticle(VGroup):
    CONFIG = {
        'radius': 4,
        "layer_radius": 2,
        'layer_num': 80,
        'opacity_func': lambda t: 1500 * (1 - abs(t - 0.009) ** 0.0001),
        'rate_func': lambda t: t ** 2,
        "sign": "+",
        "glow": True
    }

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.color_list = color_gradient(self.colors, self.layer_num)
        particle = get_charged_particles(color=self.color, sign=self.sign, radius=0.015 * self.radius)
        #self.add(Dot(color=average_color(self.colors[0], WHITE), plot_depth=4).set_height(0.015 * self.radius))
        self.add(particle)
        if self.glow:
            num_boundary = int(self.layer_num * (0.015 * self.radius/self.layer_radius) ** 0.5)
            for i in range(num_boundary, self.layer_num):
                self.add(Arc(radius=self.layer_radius * self.rate_func((0.5 + i) / self.layer_num), angle=TAU,
                             color=self.color_list[i],
                             stroke_width=101 * (self.rate_func((i + 1) / self.layer_num) - self.rate_func(
                                 i / self.layer_num)) * self.layer_radius,
                             stroke_opacity=self.opacity_func(self.rate_func(i / self.layer_num)), plot_depth=5))

class Trail(VGroup):
    CONFIG = {
        'max_width': 5,
        'nums': 500,
        'trail_color': BLUE_B,
        'rate_func': lambda t: t ** 1.25,
    }

    def __init__(self, mob, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.add(mob)
        self.trail = VGroup()
        self.path_xyz = []
        self.add(self.trail)
        self.pos_old = self[0].get_center()
        if type(self.trail_color) != str:
            self.colors = color_gradient(self.trail_color, self.nums)

    def get_path_xyz(self, err=1e-6):
        pos_new = self[0].get_center()
        pos_old = self.pos_old
        if sum(abs(pos_new - pos_old)) > err:
            self.path_xyz.append(pos_new)
        self.pos_old = pos_new
        while len(self.path_xyz) > self.nums:
            self.path_xyz.remove(self.path_xyz[0])

    def create_path(self):
        path = VGroup()
        self.get_path_xyz()
        if len(self.path_xyz) > 1:
            for i in range(len(self.path_xyz) - 1):
                if type(self.trail_color) == str:
                    path.add(Line(self.path_xyz[i], self.path_xyz[i + 1], stroke_color=self.trail_color,
                                  stroke_opacity=self.rate_func(i / len(self.path_xyz)),
                                  plot_depth=self.rate_func(2 - i / len(self.path_xyz)),
                                  stroke_width=self.max_width * self.rate_func(i / len(self.path_xyz))))
                else:
                    path.add(Line(self.path_xyz[i], self.path_xyz[i + 1], stroke_color=self.colors[i],
                                  stroke_opacity=self.rate_func(i / len(self.path_xyz)),
                                  plot_depth=self.rate_func(2 - i / len(self.path_xyz)),
                                  stroke_width=self.max_width * self.rate_func(i / len(self.path_xyz))))

        return path

    def update_path(self, trail):
        trail.become(self.create_path())

    def start_trace(self):
        # self.trail.add_updater(self.update_trail)
        self.trail.add_updater(self.update_path)

    def stop_trace(self):
        self.trial.remove_updater(self.update_path)

    def decrease_trail_num(self, trail, dt):
        if self.nums > max(self.min_num, 2):
            if self.nums <= 2:
                trail.become(VGroup())
            else:
                self.nums -= self.rate
                if self.nums < 2:
                    self.nums = 2
                trail.become(self.create_path())

    def retrieve_trail(self, rate=2, min_num=0):
        # self.stop_trace()
        self.nums = len(self.trail)
        self.min_num = min_num
        self.rate = rate
        self.trail.add_updater(self.decrease_trail_num)

class ParticleInField(VGroup):
    CONFIG = {
        'cmr': -3.0,
        'pos': np.array([0.5, 0.5, 0.0]),
        'velocity': np.array([-3.0, -4.0, 0.0]),
        'plot_depth': 5,
        'func': None,
        "sources": [[10, [0, 0, 0]]]
    }

    def __init__(self, mob, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.particle = mob.move_to(self.pos)
        self.add(self.particle)

    def get_acceleration(self, func, cmr, pos):
        E = func(pos, self.sources)
        a = cmr * E
        return a

    def update_xyz(self, delta_t=2.5e-3):
        cmr = self.cmr
        pos = self.pos
        func = self.func
        a = self.get_acceleration(func, cmr, pos)

        self.velocity += a * delta_t
        self.pos += self.velocity * delta_t

    def reset_velocity(self):
        v = self.velocity

    def update_particle(self, mob, dt):
        self.update_xyz()
        mob.move_to(self.pos)

    def start_move(self):
        self.add_updater(self.update_particle)

#scenes
class Intro(OpeningQuote):
    CONFIG = {
        "quote": ["Don't try to understand it.", "Feel it."],
        "author": "TENET",
        "fade_in_kwargs": {
            "lag_ratio": 0.2,
            "rate_func": linear,
            "run_time": 1,
        },
        "top_buff": 1.0,
        "author_buff": 3.0,
    }

    def construct(self):
        self.quote = self.get_quote()
        self.author = self.get_author(self.quote)

        self.play(FadeIn(self.quote[0:2], **self.fade_in_kwargs))
        self.wait(0.5)
        self.play(FadeIn(self.quote[2:4], **self.fade_in_kwargs))
        self.wait()
        self.play(Write(self.author, run_time=2))
        self.wait()

class StaticSourceScene(ThreeDScene):
    CONFIG = {
        "graph_x_min": -FRAME_X_RADIUS * 4,
        "graph_x_max": FRAME_X_RADIUS * 4,
        "graph_y_min": -FRAME_Y_RADIUS * 4,
        "graph_y_max": FRAME_Y_RADIUS * 4,
        "phi": 60 * DEGREES,
        "theta": 60 * DEGREES,
        "distance": 200,
        "surface_resolution": (40, 40),
                 # [cmr荷质比, pos位置]
        "sources": [[10, [0, 0, 0]]],
        "particles": [[30, [-6, 3, 0], [50, 0, 0]]],
        "source_radius": 15,
        "particle_radius": 5,
        "source_group": VGroup(),
        "particle_group": VGroup(),
        "vector_group": VGroup(),
        "trail": True,  #轨迹
        "free_moving": True,  #在电场中自由移动
        "jiggling": True,  #粒子抖动
        "lagged_start": True,  #入场动画
        "source_glow": True
    }

    def construct(self):
        self.get_source()
        self.play_moving_particle()
        self.wait(10)
        #self.get_plane()
        #self.get_potential_surface()
        #self.begin_ambient_camera_rotation()
        #self.wait(2)

    def get_source(self):
        source_group = self.source_group
        for source in self.sources:
            particle = ChargedParticle(color=RED if source[0] > 0 else BLUE, colors=[RED_D, RED_A] if source[0] > 0
                             else [BLUE_B, BLUE_A], radius=self.source_radius, plot_depth=5, opacity_func=opacity_func(1,
                             increase_factor=2), rate_func=rate_func(1), sign="+" if source[0] > 0 else "-", glow=self.source_glow).move_to(source[1])
            source_group.add(particle)
        if self.lagged_start:
            self.play(LaggedStart(*[FadeInFromLarge(source, 0.3) for source in source_group], lag_ratio=0.2))
        else:
            self.add(source_group)
        if self.jiggling:
            source_group = JigglingSubmobjects(source_group)
        self.add(source_group)

    def get_vectors(self):
        def single_vector(sources, particle):
            force = -coulomb_func(particle.get_center(), sources)
            norm = abs(np.sqrt(sum(p ** 2 for p in force)))
            unit = force / norm
            result = Vector().set_color(ORANGE)
            result.put_start_and_end_on(particle.get_center(), particle.get_center() +
                                        unit * 0.3 * (norm ** 0.25))
            return result

        pairs = VGroup()
        for i in self.particle_group:
            vector = single_vector(self.sources, i)
            pairs.add(VGroup(vector, i))
            self.vector_group.add(vector)

        self.play(LaggedStart(*[FadeInFromPoint(mob[0], mob[1].get_center()) for mob in pairs], lag_ratio=0.1))

    def add_static_particle(self, start=0, end=-1):
        count = start
        particle_group = self.particle_group
        for p in self.particles[start:end]:
            particle_group.add(ChargedParticle(color=BLUE if p[0] < 0 else RED,
                                                    colors=[BLUE_B, BLUE_A] if p[0] < 0 else [RED_D, RED_A],
                                                    radius=self.particle_radius, plot_depth=5,
                                                    opacity_func=opacity_func(decrease_factor=2),
                                                    rate_func=rate_func(decrease_factor=2), sign="-" if p[0] < 0 else "+").move_to(self.particles[count][1]))
            count += 1
        if self.lagged_start:
            self.play(LaggedStart(*[FadeInFromLarge(par, 0.3) for par in particle_group[start:end]], lag_ratio=0.1))
        else:
            self.add(particle_group)

    def play_moving_particle(self, start=0, end=-1):
        count = start
        for p in self.particles[start:end]:
            trail = Trail(self.particle_group[count], trail_color=BLUE_B if self.particles[count][0] < 0 else RED_D, max_width=4, rate_func=lambda t: t ** 4)
            if self.trail:
                self.add(trail.trail)
                trail.start_trace()
            count += 1

        count = start
        if self.free_moving:
            for p in self.particles[start:end]:
                moving_particle = ParticleInField(self.particle_group[count], cmr=p[0], pos=p[1], velocity=p[2], func=coulomb_func, sources=self.sources)
                self.add(moving_particle)
                moving_particle.start_move()
                count += 1

    def get_plane(self):
        surface_config = {
            "u_min": self.graph_x_min,
            "u_max": self.graph_x_max,
            "v_min": self.graph_y_min,
            "v_max": self.graph_y_max,
            "resolution": self.surface_resolution,
            "checkerboard_colors": [GREY, LIGHT_GREY]
        }
        plane = ParametricSurface(
            lambda x, y: np.array([
                x, y, 0.05
            ]),
            **surface_config,
        )
        plane.set_style(
            fill_opacity=0.2,
            stroke_width=0.5,
            stroke_color=WHITE,
        )

        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, distance=200, added_anims=[
            Write(plane)
        ])

    def get_func(self, r, theta):
        output = 0
        k = 1
        for source in self.sources:
            output += r * complex_to_R3(np.exp(1j * theta)) + (k * source[0])/(r**2) * OUT
        return output

    def get_potential_surface(self):
        surface_config = {
            "u_min": 0.5,
            "u_max": FRAME_Y_RADIUS * 4,
            "v_min": 0,
            "v_max": PI * 2,
            "resolution": (50, 50),
        }
        surface = ParametricSurface(self.get_func, **surface_config)
        surface.set_style(
            fill_opacity=0.5,
            fill_color=BLUE_B,
            stroke_width=0.5,
            stroke_color=WHITE,
            stroke_opacity=1
        )
        self.surface = surface
        self.play(Write(surface), run_time=2)

    def reverse_camera(self):
        self.move_camera(phi=self.phi + PI, theta=self.theta, distance=self.distance, added_anims=[])

class ShowElectricForce(StaticSourceScene):
    CONFIG = {
        "graph_x_min": -FRAME_X_RADIUS * 4,
        "graph_x_max": FRAME_X_RADIUS * 4,
        "graph_y_min": -FRAME_Y_RADIUS * 4,
        "graph_y_max": FRAME_Y_RADIUS * 4,
        "surface_resolution": (40, 40),
        "sources": [[30/4, [0, 0, 0]]],
        "source_radius": 15,
        "source_group": VGroup(),
        "particle_group": VGroup(),
        "vector_group": VGroup(),
        "particles": [[-15/4, [1, 3/4, 0], [0, 0, 0]],
                      [-15/4, [-1, 3/4, 0], [0, 0, 0]],
                      [-15/4, [-1, -3/4, 0], [0, 0, 0]],
                      [-15/4, [1, -3/4, 0], [0, 0, 0]]],
        "particle_radius": 5,
        "trail": True
    }

    def construct(self):
        self.get_source()
        self.add_static_particle(start=0, end=4)
        self.get_vectors()
        factor = ValueTracker(1)
        for i in range(4):
            self.radial_changing_force(i, factor)
        self.dashed_circle(factor)
        self.play(ApplyMethod(factor.increment_value, 1), rate_func=linear, run_time=3)
        #self.play(ApplyMethod(factor.increment_value, 1), rate_func=linear)
        self.get_formula(formula="F=\\frac{1}{4\pi \\varepsilon _{0}} \\frac{q_{1}q_{2}}{r^2}", factor=factor)
        self.play(ApplyMethod(factor.increment_value, -2), rate_func=linear, run_time=6)
        self.wait(4)

    def radial_changing_force(self, index, factor):
        particle = self.particle_group[index]
        self.vector_group[index].add_updater(lambda m: m.become(self.get_single_vector(self.sources, particle)))
        array = self.particle_group[index].get_center()
        particle.add_updater(lambda m: m.move_to(array * factor.get_value()))

    def dashed_circle(self, factor):
        pos = self.particles[0][1]
        r = np.sqrt(sum(p**2 for p in pos))
        circle = Circle(radius=r).set_color(LIGHT_GREY)
        line = DashedLine().put_start_and_end_on(ORIGIN, RIGHT*r).set_color(LIGHT_GREY)
        r_letter = TexMobject("r").set_color(WHITE).move_to(line.get_center() + UP*0.25).scale(0.5)
        circle.move_to(ORIGIN)
        dashed_circle = DashedVMobject(circle, num_dashes=20)
        self.play(ShowCreation(dashed_circle), ShowCreation(line), Write(r_letter))
        line.add_updater(lambda m: m.put_start_and_end_on(ORIGIN, RIGHT * r * factor.get_value()))
        r_letter.add_updater(lambda m: m.move_to(line.get_center() + UP * 0.25))
        dashed_circle.add_updater(lambda m: m.set_width(2 * r * factor.get_value()))

    def get_formula(self, formula, factor):
        text = TexMobject(formula)
        text.scale(2)
        text.to_edge(UP)
        text.add_background_rectangle()
        frame = SurroundingRectangle(text,
                                     stroke_width=0, fill_color=BLACK, fill_opacity=1, height=6)
        text = VGroup(text, frame)
        text.scale(0.6)
        text.to_edge(UR)
        animated_frame = AnimatedBoundary(frame)
        self.play(FadeInFromLarge(frame, 0.3), ApplyMethod(factor.increment_value, 1/3), rate_func=linear)
        self.add(animated_frame)
        self.play(Write(text[0]), ApplyMethod(factor.increment_value, 2/3), run_time=2, rate_func=linear)

class VortexParticles(StaticSourceScene):
    CONFIG = {
        "sources": [[10, [0., .0, .0]]],
        "particles": [[-40., [.0, FRAME_X_RADIUS/2, .0], [20.0, -20.0, 0.0]],
                      [-40., [.0, -FRAME_X_RADIUS/2, .0], [-20.0, 20.0, 0.0]],
                      [-40., [FRAME_X_RADIUS/2, .0, .0], [-20.0, -20.0, 0.0]],
                      [-40., [-FRAME_X_RADIUS/2, .0, .0], [20.0, 20.0, 0.0]]],
        "jiggling": False,
        "lagged_start": True
    }

    def construct(self):
        self.get_source()
        self.add_static_particle(start=0, end=5)
        self.wait()
        self.play_moving_particle(start=0, end=5)
        self.wait(6)

class ElectrodesAndParticle(StaticSourceScene):
    CONFIG = {
        "source_radius": 10,
        "sources": [
                    [10, [0., FRAME_X_RADIUS / 4, .0]],
                    [10, [0.525 * 1, FRAME_X_RADIUS / 4, .0]],
                    [10, [0.525 * 2, FRAME_X_RADIUS / 4, .0]],
                    [10, [0.525 * 3, FRAME_X_RADIUS / 4, .0]],
                    [10, [0.525 * 4, FRAME_X_RADIUS / 4, .0]],
                    [10, [0.525 * 5, FRAME_X_RADIUS / 4, .0]],
                    [10, [0.525 * 6, FRAME_X_RADIUS / 4, .0]],
                    [10, [-0.525 * 1, FRAME_X_RADIUS / 4, .0]],
                    [10, [-0.525 * 2, FRAME_X_RADIUS / 4, .0]],
                    [10, [-0.525 * 3, FRAME_X_RADIUS / 4, .0]],
                    [10, [-0.525 * 4, FRAME_X_RADIUS / 4, .0]],
                    [10, [-0.525 * 5, FRAME_X_RADIUS / 4, .0]],
                    [10, [-0.525 * 6, FRAME_X_RADIUS / 4, .0]],
                    [-10, [0., -FRAME_X_RADIUS / 4, .0]],
                    [-10, [0.525 * 1, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [0.525 * 2, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [0.525 * 3, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [0.525 * 4, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [0.525 * 5, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [0.525 * 6, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [-0.525 * 1, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [-0.525 * 2, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [-0.525 * 3, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [-0.525 * 4, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [-0.525 * 5, -FRAME_X_RADIUS / 4, .0]],
                    [-10, [-0.525 * 6, -FRAME_X_RADIUS / 4, .0]],
        ],
        "particles": [[0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [30.0, 0.0, 0.0]],
                      [0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [40.0, 0.0, 0.0]],
                      [0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [50.0, 0.0, 0.0]],
                      [0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [60.0, 0.0, 0.0]],
                      [-0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [30.0, 0.0, 0.0]],
                      [-0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [40.0, 0.0, 0.0]],
                      [-0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [50.0, 0.0, 0.0]],
                      [-0.125, [-FRAME_X_RADIUS - 1.0, .0, .0], [60.0, 0.0, 0.0]]],
        "jiggling": True,
        "lagged_start": False,
        "source_glow": False
    }

    def construct(self):
        rec_1 = Polygon(np.array([3.45, FRAME_X_RADIUS / 4 + 0.3, .0]), np.array([-3.45, FRAME_X_RADIUS / 4 + 0.3, .0]),
                        np.array([-3.45, FRAME_X_RADIUS / 4 - 0.2, .0]), np.array([3.45, FRAME_X_RADIUS / 4 - 0.2, .0]))
        rec_2 = Polygon(np.array([3.45, -FRAME_X_RADIUS / 4 + 0.2, .0]), np.array([-3.45, -FRAME_X_RADIUS / 4 + 0.2, .0]),
                        np.array([-3.45, -FRAME_X_RADIUS / 4 - 0.3, .0]), np.array([3.45, -FRAME_X_RADIUS / 4 - 0.3, .0]))
        rec_1.set_fill(color=Portrait, opacity=0.8).set_stroke(opacity=0)
        rec_2.set_fill(color=Portrait, opacity=0.8).set_stroke(opacity=0)
        self.add(rec_1, rec_2)
        self.get_source()
        self.wait()
        self.add_static_particle(start=0, end=4)
        self.play_moving_particle(start=0, end=4)
        self.wait(5)
        self.add_static_particle(start=4, end=8)
        self.play_moving_particle(start=4, end=8)
        self.wait(6)

class DipoleField(StaticSourceScene):
    CONFIG = {
        "sources": [[10, [-2, 0, 0]], [10, [2, 0, 0]]],
        "particles": [[-48., [2.0, 1.5, 0.0], [-61.0, 0.0, 0.0]], [-48., [-2.0, -1.5, 0.0], [60.0, 0.0, 0.0]]],
        "jiggling": False,
        "lagged_start": False
    }

    def construct(self):
        self.get_source()
        self.add_static_particle()
        self.wait()
        self.play_moving_particle()
        self.wait(10)

class FlowerOrbit(StaticSourceScene):
    CONFIG = {
        "graph_x_min": -FRAME_X_RADIUS * 4,
        "graph_x_max": FRAME_X_RADIUS * 4,
        "graph_y_min": -FRAME_Y_RADIUS * 4,
        "graph_y_max": FRAME_Y_RADIUS * 4,
        "surface_resolution": (40, 40),
        "sources": [[30, [0, 0, 0]]],
        "source_radius": 15,
        "source_group": VGroup(),
        "particle_group": VGroup(),
        "vector_group": VGroup(),
        "particles": [[-15, [-5 / 2, 0, 0], [0, -15 * np.sqrt(2), 0]],
                      [-15, [-3 / 2, -2, 0], [12 * np.sqrt(2), -9 * np.sqrt(2), 0]],
                      [-15, [0, -5 / 2, 0], [15 * np.sqrt(2), 0, 0]],
                      [-15, [3 / 2, -2, 0], [12 * np.sqrt(2), 9 * np.sqrt(2), 0]],
                      [-15, [5 / 2, 0, 0], [0, 15 * np.sqrt(2), 0]],
                      [-15, [3 / 2, 2, 0], [-12 * np.sqrt(2), 9 * np.sqrt(2), 0]],
                      [-15, [0, 5 / 2, 0], [-15 * np.sqrt(2), 0, 0]],
                      [-15, [-3 / 2, 2, 0], [-12 * np.sqrt(2), -9 * np.sqrt(2), 0]]],
        "particle_radius": 5,
        "trail": True,
    }

    def construct(self):
        self.get_source()
        self.add_static_particle(start=0, end=9)
        self.play_moving_particle(start=0, end=9)
        self.wait(12)

#abandoned
def generate_source_position(num):
    source_position_group = []
    init = (num - 1)/2
    for i in range(num):
        for j in range(num):
            pos = [10, [-4 * init + 4 * i, -4 * init + 4 * j, 0]]
            source_position_group.append(pos)
    return source_position_group

def generate_particle_position(num):
    source_position_group = generate_source_position(num)
    particle_position_group = []
    for pos in source_position_group:
        x, y = pos[1][0], pos[1][1]
        particle_position_group.append([-10, [x + 1.5, y, 0]])
        print(pos)
    return particle_position_group

class MoleculeOrbit(StaticSourceScene, MovingCameraScene):
    CONFIG = {"surface_resolution": (40, 40),
              "sources": generate_source_position(8),
              "particles": generate_particle_position(8),
              "source_radius": 15,
              "particle_radius": 5,
              "source_group": VGroup(),
              "particle_group": VGroup(),
              "vector_group": VGroup(),
              "trail": True,
              "free_moving": False,
              "jiggling": False,
              "lagged_start": False
              }

    def construct(self):
        t = ValueTracker(0)
        self.camera_frame.scale(0.3)
        self.get_source()
        self.add_static_particle(end=256)
        self.play_moving_particle(end=256)
        self.arrange_particles(t)
        self.play(ApplyMethod(t.increment_value, PI * 4/3), run_time=6, rate_func=linear)
        self.play(ApplyMethod(t.increment_value, PI * 4), self.camera_frame.scale, 18, run_time=18, rate_func=linear)

    def move_along_source(self, particle, source, theta):
        center = source.get_center()
        particle.add_updater(lambda m: m.move_to(center + 1.5 * UP * np.sin(3 * theta.get_value())
                                                 + 1.5 * RIGHT * np.cos(3 * theta.get_value())))
    def arrange_particles(self, theta):
        index = 0
        for particle in self.particle_group:
            self.move_along_source(particle, self.source_group[index], theta)
            index += 1

class TwoSourceChargesAndPotentialSurface(ThreeDScene):
    CONFIG = {
        "graph_x_min": -FRAME_X_RADIUS * 4,
        "graph_x_max": FRAME_X_RADIUS * 4,
        "graph_y_min": -FRAME_Y_RADIUS * 4,
        "graph_y_max": FRAME_Y_RADIUS * 4,
        "surface_resolution": (40, 40)
    }

    def construct(self):
        opacity_func_source = opacity_func(1, increase_factor=2)
        rate_func_source = rate_func(1)
        opacity_func_particle = opacity_func(1)
        rate_func_particle = rate_func(1)
        p1 = ChargedParticle(color=BLUE, colors=[BLUE_B, BLUE_A], radius=5, plot_depth=5, opacity_func=opacity_func_particle,
                             rate_func=rate_func_particle, sign="-")
        p2 = ChargedParticle(color=BLUE, colors=[BLUE_B, BLUE_A], radius=5, plot_depth=5, opacity_func=opacity_func_particle,
                             rate_func=rate_func_particle, sign="-")
        c1 = ChargedParticle(color=RED, colors=[RED_D, RED_A], radius=15, plot_depth=5, layer_num=300,
                             opacity_func=opacity_func_source, rate_func=rate_func_source, sign="+")
        c2 = ChargedParticle(color=RED, colors=[RED_D, RED_A], radius=15, plot_depth=5, layer_num=300,
                             opacity_func=opacity_func_source, rate_func=rate_func_source, sign="+")
        t1 = Trail(p1, trail_color=BLUE_B, max_width=4)
        t2 = Trail(p2, trail_color=BLUE_B, max_width=4)
        self.plane = self.get_plane()

        c1.move_to(np.array([-2, 0, 0]))
        c2.move_to(np.array([2, 0, 0]))

        sources_group = [[10, [2, 0, 0]], [10, [-2, 0, 0]]]
        moving_particle_p1 = ParticleInField(p1, cmr=-3.0, pos=np.array([2.0, 1.5, 0.0]),
                                             velocity=np.array([-15.0, 0.0, 0.0]), func=coulomb_func, sources=sources_group)
        moving_particle_p2 = ParticleInField(p2, cmr=-3.0, pos=np.array([-2.0, -1.5, 0.0]),
                                             velocity=np.array([15.0, 0.0, 0.0]), func=coulomb_func, sources=sources_group)
        moving_particle_p1.reset_velocity()
        moving_particle_p2.reset_velocity()

        self.add(moving_particle_p1, moving_particle_p2, t1.trail, t2.trail, c1, c2)
        t1.start_trace()
        t2.start_trace()
        moving_particle_p1.start_move()
        moving_particle_p2.start_move()
        self.wait(8)
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, distance=200, added_anims=[
                Write(self.plane)
            ])
        self.wait(5)

    def get_plane(self):
        surface_config = {
            "u_min": self.graph_x_min,
            "u_max": self.graph_x_max,
            "v_min": self.graph_y_min,
            "v_max": self.graph_y_max,
            "resolution": self.surface_resolution,
            "checkerboard_colors": [GREY, LIGHT_GREY]
        }
        plane = ParametricSurface(
            lambda x, y: np.array([
                x, y, 0.05
            ]),
            **surface_config,
        )
        plane.set_style(
            fill_opacity=0.2,
            stroke_width=0.5,
            stroke_color=WHITE,
        )
        return plane

    def get_potential_surface(self):
        surface = ParametricSurface(
            lambda x, y: np.array([

            ]))
