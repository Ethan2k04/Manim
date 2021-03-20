from manimlib import *
from my_program.utils.ThreeDVector import ThreeDVector
# old version
def tuplify(obj):
    if isinstance(obj, str):
        return (obj,)
    try:
        return tuple(obj)
    except TypeError:
        return (obj,)

class ThreeDVMobject(VMobject):
    CONFIG = {
        "shade_in_3d": True,
    }

class ParametricSurfaceOLD(VGroup):
    CONFIG = {
        "u_min": -5,
        "u_max": 5,
        "v_min": -5,
        "v_max": 5,
        "resolution": (50, 50),
        "surface_piece_config": {},
        "fill_color": BLUE_D,
        "fill_opacity": 1.0,
        "checkerboard_colors": [BLUE_D, BLUE_E],
        "stroke_color": GREY_A,
        "stroke_width": 0.6,
        "should_make_jagged": False,
        "pre_function_handle_to_anchor_scale_factor": 0.00001,
    }

    def __init__(self, func, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.func = func
        self.setup_in_uv_space()
        self.apply_function(lambda p: func(p[0], p[1]))
        if self.should_make_jagged:
            self.make_jagged()

    def get_u_values_and_v_values(self):
        res = tuplify(self.resolution)
        if len(res) == 1:
            u_res = v_res = res[0]
        else:
            u_res, v_res = res
        u_min = self.u_min
        u_max = self.u_max
        v_min = self.v_min
        v_max = self.v_max

        u_values = np.linspace(u_min, u_max, u_res + 1)
        v_values = np.linspace(v_min, v_max, v_res + 1)

        return u_values, v_values

    def setup_in_uv_space(self):
        u_values, v_values = self.get_u_values_and_v_values()
        faces = VGroup()
        for i in range(len(u_values) - 1):
            for j in range(len(v_values) - 1):
                u1, u2 = u_values[i:i + 2]
                v1, v2 = v_values[j:j + 2]
                face = ThreeDVMobject()
                face.set_points_as_corners([
                    [u1, v1, 0],
                    [u2, v1, 0],
                    [u2, v2, 0],
                    [u1, v2, 0],
                    [u1, v1, 0],
                ])
                faces.add(face)
                face.u_index = i
                face.v_index = j
                face.u1 = u1
                face.u2 = u2
                face.v1 = v1
                face.v2 = v2
        faces.set_fill(
            color=self.fill_color,
            opacity=self.fill_opacity
        )
        faces.set_stroke(
            color=self.stroke_color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
        )
        self.add(*faces)
        if self.checkerboard_colors:
            self.set_fill_by_checkerboard(*self.checkerboard_colors)

    def set_fill_by_checkerboard(self, *colors, opacity=None):
        n_colors = len(colors)
        for face in self:
            c_index = (face.u_index + face.v_index) % n_colors
            face.set_fill(colors[c_index], opacity=opacity)

#utils
def get_charged_particle(color, sign, radius=0.1):
    result = Circle(
        stroke_color=WHITE,
        stroke_width=0.5,
        fill_color=color,
        fill_opacity=0.8,
        radius=radius
    )
    sign = Tex(sign)
    sign.set_stroke(WHITE, 1)
    sign.set_width(0.5 * result.get_width())
    sign.move_to(result)
    result.add(sign)
    return result

def get_charged_particle_3d(sign, radius=0.1, opacity=0.8):
    positive_texture = "my_program/texture/positive_charge.png"
    dark_positive_charge = "my_program/texture/dark_positive_charge.png"
    negative_texture = "my_program/texture/negative_charge.png"
    dark_negative_charge = "my_program/texture/dark_negative_charge.png"

    result = TexturedSurface(Sphere(radius=radius), positive_texture, dark_positive_charge) if sign == "+"\
        else TexturedSurface(Sphere(radius=radius), negative_texture, dark_negative_charge)
    result.set_opacity(opacity)

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
        self.add_updater(lambda m, dt: m.update_position(dt))

    def update_position(self, dt):
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
        particle = get_charged_particle(color=self.color, sign=self.sign, radius=0.015 * self.radius)
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

    def get_path_xyz(self, err=1e-2):  #err=1e-6
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
        "quote": ["'Don't try to understand it.", "Feel it.'"],
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

        self.play(FadeIn(self.quote[0], **self.fade_in_kwargs))
        self.wait(0.5)
        self.play(FadeIn(self.quote[1], **self.fade_in_kwargs))
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
            self.play(LaggedStart(*[FadeIn(source, scale=3) for source in source_group], lag_ratio=0.2))
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
            self.play(LaggedStart(*[FadeIn(par, scale=3) for par in particle_group[start:end]], lag_ratio=0.1))
        else:
            self.add(particle_group)

    def play_moving_particle(self, start=0, end=-1):
        count = start
        if self.trail:
            for p in self.particles[start:end]:
                trail = Trail(self.particle_group[count], trail_color=BLUE_B if self.particles[count][0] < 0 else RED_D, max_width=4, rate_func=lambda t: t ** 4)
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

class DipoleField(StaticSourceScene):
    CONFIG = {
        "sources": [[10, [-2, 0, 0]], [10, [2, 0, 0]]],
        "particles": [[-48., [2.0, 1.5, 0.0], [-61.0, 0.0, 0.0]], [-48., [-2.0, -1.5, 0.0], [60.0, 0.0, 0.0]]],
        "jiggling": False,
        "lagged_start": False,
        "trail": True
    }

    def construct(self):
        self.get_source()
        self.add_static_particle()
        self.wait()
        self.play_moving_particle()
        frame = self.camera.frame
        self.play(
            # 在过渡期间移动相机帧
            frame.increment_phi, -60 * DEGREES,
            frame.increment_theta, -30 * DEGREES,
            run_time=3
        )
        self.wait(10)

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
        rec_1.set_fill(color=[GREY_A, GREY_E], opacity=0.8)
        rec_1.set_stroke(opacity=0)
        rec_2.set_fill(color=[GREY_A, GREY_E], opacity=0.8)
        rec_2.set_stroke(opacity=0)
        self.add(rec_1, rec_2)
        self.get_source()
        self.wait()
        self.add_static_particle(start=0, end=4)
        self.play_moving_particle(start=0, end=4)
        self.wait(5)
        self.add_static_particle(start=4, end=8)
        self.play_moving_particle(start=4, end=8)
        self.wait(6)

class IntroduceElectricFieldScene2(Scene):
    CONFIG = {
        "screen_height": 3,
        "camera_config": {"background_color": "#464646"}
    }
    def construct(self):
        screen_dipole = ScreenRectangle(height=self.screen_height).set_fill("#000000")
        screen_electrodes = ScreenRectangle(height=self.screen_height).set_fill("#000000")
        screens = VGroup(screen_dipole, screen_electrodes)
        screens.arrange(RIGHT, buff=MED_LARGE_BUFF, aligned_edge=UP)
        titles = self.get_title("The graph of \phi(x)")#self.get_title("Electric Field")
        screen_dipole = AnimatedBoundary(screen_dipole)
        screen_electrodes = AnimatedBoundary(screen_electrodes)
        self.add(titles, screen_dipole)
        self.wait(2)
        self.add(screen_electrodes)
        self.wait(20)

    def get_title(self, word):
        title = Tex(word)
        title.scale(2)
        title.to_edge(UP)
        title.add_background_rectangle()
        return title

class ShowElectricForce(ThreeDScene):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.8,
    }

    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=60 * DEGREES,
        )
        light = self.camera.light_source
        light.move_to(np.array([2 * np.sqrt(3), -6, 4]))

        # axes = ThreeDAxes()
        # labels = axes.get_axis_labels()
        # self.add(axes, labels)

        source = self.source = get_charged_particle_3d("+", radius=self.source_radius, opacity=0.999)
        particle = self.particle = get_charged_particle_3d("-", radius=self.particle_radius, opacity=0.999)
        pos_source = np.array([-2, 0, 0])
        pos_particle = np.array([2, 0, 0])
        source.move_to(pos_source)
        particle.move_to(pos_particle)

        dashed_line = self.dashed_line = self.get_dashed_line()
        self.distance_init = get_norm(self.source.get_center() - self.particle.get_center())
        self.vector_source = vector_source = self.get_3d_vector("source")
        self.vector_particle = vector_particle = self.get_3d_vector("particle")
        bracket = self.bracket = self.get_labels()
        text = self.get_formula("Coulomb's Law:",
                                r"F_{1 } = \frac {1 }{4\pi \epsilon _{0 } } \frac{q_{1}q_{2} }{r^{2} } e_{12 } = -F_{2 }")

        self.r = ValueTracker(4)
        self.theta = ValueTracker(0)

        self.add(source, particle, dashed_line, bracket)
        self.add_updater_to_related_mobjects()
        # 添加自旋效果
        always_rotate(self.source, rate=20 * DEGREES)
        always_rotate(self.particle, rate=-20 * DEGREES)
        self.wait(2)

        indicator = ThreeDVector().set_direction([0, 0, -1]).set_color(RED)
        indicator.next_to(source, OUT, buff=0.30)
        self.play(FadeIn(indicator))
        for i in range(3):
            self.play(ApplyMethod(indicator.shift, IN*0.25), run_time=0.5, rate_func=there_and_back)
        self.play(FadeOut(indicator))

        self.play(FadeInFromPoint(vector_source, source.get_center() + RIGHT * self.source_radius),
                  FadeInFromPoint(vector_particle, particle.get_center() + LEFT * self.particle_radius))
        self.wait()

        self.play(Write(text))
        self.play(*self.move_particle_to(3, 0))
        self.wait()
        self.play(*self.move_particle_to(8, 0), func=linear, run_time=4)
        self.wait()
        self.r.set_value(3), self.theta.set_value(0)
        self.play(*self.move_particle_to(8, 0), func=linear, run_time=4)
        self.wait(2)
        self.r.set_value(4), self.theta.set_value(-PI/3)
        self.wait(0.5)

        dashed_orbit = self.dashed_orbit = self.get_dashed_orbit()
        self.play(Write(dashed_orbit))
        self.play(*self.move_particle_to(4, PI/3), func=linear, run_time=4)
        self.wait()
        self.r.set_value(4), self.theta.set_value(-PI / 3)
        self.play(*self.move_particle_to(4, PI/3), func=linear, run_time=4)
        self.wait(5)

    def get_distance(self):
        return get_norm(self.particle.get_center() - self.source.get_center())

    def get_unit_vector(self):
        return (self.particle.get_center() - self.source.get_center())/self.get_distance()

    def get_dashed_line(self):
        vector = self.particle.get_center() - self.source.get_center()
        unit_vector = vector/get_norm(vector)
        start = self.source.get_center() + unit_vector * self.source_radius
        end = self.particle.get_center() - unit_vector * self.particle_radius
        line = DashedLine(start=start, end=end, num_dashes=10)
        return line

    def get_dashed_orbit(self):
        distance = self.get_distance()
        orbit = Arc(radius=distance, arc_center=self.source.get_center(), start_angle=-PI/3, angle=2*PI/3, n_components=30)
        orbit = DashedVMobject(orbit, num_dashes=10, positive_space_ratio=0.8)
        return orbit

    def get_3d_vector(self, which):
        colors = color_gradient(["#FF0000", "#FFF200", "#1E9600"], 50)
        result = ThreeDVector(
            position=self.particle.get_center(),
            vector=self.source.get_center() - self.particle.get_center(),
            max_bottom_radius=0.1,
            top_radius_to_bottom_radius=1
        )
        distance = self.get_distance()
        unit_vector = (self.particle.get_center() - self.source.get_center())/distance
        index = int(50 * (distance-1)/8)
        length = self.vector_length_init * (distance / self.distance_init) ** (-0.5)
        result.set_vector_length(length).set_color(colors[index])

        force_source = result.copy()
        force_particle = result.copy()

        force_source.set_direction(self.particle.get_center() - self.source.get_center())
        force_source.set_position(self.source.get_center() + unit_vector * self.source_radius)
        force_particle.set_position(self.particle.get_center() - unit_vector * self.particle_radius)
        unit_vector = self.get_unit_vector()
        ppd = np.cross(OUT, unit_vector)
        arc = np.arccos(np.dot(RIGHT, unit_vector))
        self.force_particle_label = force_particle_label = Tex("E", font_size=24)
        self.force_source_label = force_source_label = Tex("F_{2}", font_size=24)
        force_source_label.rotate(arc if unit_vector[1] > 0 else -arc)
        force_particle_label.rotate(arc if unit_vector[1] > 0 else -arc)
        force_source_label.move_to(force_source.get_center() - 2 * ppd * SMALL_BUFF)
        force_particle_label.move_to(force_particle.get_center() - 2 * ppd * SMALL_BUFF)
        if which == "source":
            return VGroup(force_source, force_source_label)
        if which == "particle":
            return VGroup(force_particle, force_particle_label)
        else:
            raise AssertionError

    def get_labels(self):
        radius = Text("r", font="Arial", font_size=24)
        q_particle = Tex("q_{1}")
        q_source = Tex("q_{2}")
        unit_vector = self.get_unit_vector()
        ppd = np.cross(OUT, unit_vector)

        line_1 = Line(
            self.dashed_line.get_start() + ppd * MED_SMALL_BUFF,
            self.dashed_line.get_start() + ppd * MED_LARGE_BUFF
        )
        line_2 = Line(
            self.dashed_line.get_end() + ppd * MED_SMALL_BUFF,
            self.dashed_line.get_end() + ppd * MED_LARGE_BUFF
        )
        line_3 = Line(
            self.dashed_line.get_start() + ppd * MED_LARGE_BUFF,
            self.dashed_line.get_end() + ppd * MED_LARGE_BUFF
        )

        arc = np.arccos(np.dot(RIGHT, unit_vector))
        radius.rotate(arc if unit_vector[1] > 0 else -arc)
        radius.move_to(line_3.get_center() + 2 * ppd * SMALL_BUFF)
        q_source.rotate(PI/2, RIGHT).rotate(PI/6)
        q_particle.rotate(PI/2, RIGHT).rotate(PI/6)
        q_source.move_to(self.source.get_center() + IN * (self.source_radius + MED_SMALL_BUFF))
        q_particle.move_to(self.particle.get_center() + IN * (self.particle_radius + MED_SMALL_BUFF))
        bracket = VGroup(line_1, line_2, line_3, radius, q_source, q_particle)
        return bracket

    def add_updater_to_related_mobjects(self):
        self.dashed_line.add_updater(lambda m: m.become(self.get_dashed_line()))
        self.vector_source.add_updater(lambda m: m.become(self.get_3d_vector("source")))
        self.vector_particle.add_updater(lambda m: m.become(self.get_3d_vector("particle")))
        self.bracket.add_updater(lambda m: m.become(self.get_labels()))
        self.particle.add_updater(
            lambda m: m.move_to(self.source.get_center() +
                                self.r.get_value() *
                                complex_to_R3(np.exp(1j * self.theta.get_value())))
        )

    def move_particle_to(self, radius, angle):
        return [ApplyMethod(self.r.set_value, radius), ApplyMethod(self.theta.set_value, angle)]

    def get_formula(self, words, formula, index=0):
        text = VGroup(Text(words, font="Arial", font_size=36), Tex(formula))
        text.arrange(RIGHT)
        text.fix_in_frame()
        text.move_to(ORIGIN)
        text.to_edge(UP)
        text.shift(1.5 * DOWN * index)

        return text


# 2D potential
class ShowElectricPotential(ShowElectricForce):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.6,
        "d_theta": PI/24,
        "dr": 1,
        "has_particle": True,
        "has_labels": True,
        "dashed_line_group": VGroup(),
        "path_group": VGroup()
    }

    def construct(self):
        self.init_the_scene()

        formula_1 = VGroup(Tex("W = -\int_{a}^{b} F\cdot ds"), Tex("W(unit) = -\int_{a}^{b} E\cdot ds"))
        formula_1.arrange(RIGHT, buff=MED_LARGE_BUFF)
        formula_1.to_edge(DOWN, buff=LARGE_BUFF)
        formula_2 = Tex(r"-\int_{a}^{b} E\cdot ds = -\frac{q }{4\pi\epsilon _{0} } \int_{a}^{b} \frac{dr }{r^{2} } = -\frac{q }{4\pi\epsilon _{0} } (\frac{1 }{r_{a} }- \frac{1 }{r_{b} }) ")
        formula_2.move_to(formula_1.get_center())


        self.particle.add_updater(
            lambda m: m.move_to(self.source.get_center() +
                                self.r.get_value() *
                                complex_to_R3(np.exp(1j * self.theta.get_value())))
        )

        self.force_particle_label.add_updater(lambda m: m.set_color(self.vector_particle.get_color()))
        self.add(self.vector_particle)
        self.vector_particle.add_updater(lambda m: m.become(self.get_3d_vector("particle")))

        self.add(formula_1)
        self.play(self.get_assistant_line())
        self.show_path(5, speed_factor=5)
        self.play(
                  FadeOut(formula_1),
                  *list(map(GrowFromCenter, formula_2))
                )
        self.wait(2)

    def init_the_scene(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=0 * DEGREES,
            phi=0 * DEGREES,
        )

        source = self.source = get_charged_particle_3d("-", radius=self.source_radius, opacity=0.999)
        source.rotate(PI / 2, axis=RIGHT)
        particle = self.particle = get_charged_particle_3d("+", radius=self.particle_radius, opacity=0.999)
        particle.rotate(PI / 2, axis=RIGHT)
        pos_source = np.array([-3, 0, 0])
        pos_particle = np.array([5, 0, 0])
        source.move_to(pos_source)
        particle.move_to(pos_particle)

        self.r = ValueTracker(8)
        self.theta = ValueTracker(0)
        self.distance_init = get_norm(self.source.get_center() - self.particle.get_center())

        self.vector_particle = self.get_3d_vector("particle")

        light = self.camera.light_source
        light.add_updater(lambda m: m.next_to(particle, OUT * 4))

        self.add(source)

        if self.has_particle:
            self.add(particle)

    def get_path(self,
                 which,
                 target,
                 text="NaN",
                 has_label=True):

        unit_vector = self.get_unit_vector()
        text = Tex(text)
        if which == "linear":
            trail = Line(self.particle.get_center(), self.source.get_center() + unit_vector * target).set_color(YELLOW)
            self.path_group.add(trail)
            return ShowCreation(trail)
        if which == "circular":
            start_angle = np.arccos(np.dot(unit_vector, RIGHT))
            start_angle = start_angle if unit_vector[1] >= 0 else -start_angle
            distance = self.get_distance()
            trail = Arc(start_angle=start_angle, angle=target, radius=distance, arc_center=self.source.get_center()).set_color(WHITE)
            text.move_to(trail.get_start())
            self.path_group.add(trail)
            if has_label:
                return [ShowCreation(trail), Write(text)]
            else:
                return [ShowCreation(trail)]

    def get_assistant_line(self):
        unit_vector = self.get_unit_vector()
        origin = self.source.get_center()
        dashed_line = DashedLine(start=origin + unit_vector * self.source_radius,
                                 end=origin + FRAME_WIDTH * complex_to_R3(np.exp(1j * self.theta.get_value())))
        dashed_line.set_color(WHITE).set_opacity(0.5)
        self.dashed_line_group.add(dashed_line)

        return FadeIn(dashed_line)

    def show_path(self, num, speed_factor=1.):
        d_theta = self.d_theta
        dr = self.dr
        text_list = []
        run_time = 1/speed_factor
        for j in range(num):
            text_list.append("a" + "'" * j)
        text_list.append("b")

        r_init = self.r.get_value()
        for i in range(num):
            delta_r = dr * i

            # circular movement
            if i == 0:
                self.play(*self.move_particle_to(r_init - delta_r, (i + 1) * d_theta),
                          *self.get_path("circular", d_theta, text_list[i]), run_time=run_time)
            if i != 0 and self.has_labels:
                self.play(*self.move_particle_to(r_init - delta_r, (i + 1) * d_theta),
                          *self.get_path("circular", d_theta, text_list[i]), run_time=run_time)
            if i != 0 and not self.has_labels:
                self.play(*self.move_particle_to(r_init - delta_r, (i + 1) * d_theta),
                          *self.get_path("circular", d_theta, text_list[i], has_label=False), run_time=run_time)

            # assistant_line
            self.play(self.get_assistant_line(), run_time=run_time)

            # radial movement
            if i != num - 1:
                self.play(*self.move_particle_to(r_init - dr - delta_r, (i + 1) * d_theta),
                          self.get_path("linear", r_init - dr - delta_r), run_time=run_time)
                self.wait(run_time)
            if i == num - 1:
                self.play(*self.move_particle_to(r_init - dr - delta_r, (i + 1) * d_theta),
                          self.get_path("linear", r_init - dr - delta_r), run_time=run_time)
                text = Tex(text_list[-1]).move_to(
                    self.source.get_center() + self.get_distance() * complex_to_R3(np.exp(1j * (i + 1) * d_theta)))
                self.play(Write(text), run_time=run_time)

class ShowWorkDoneInElectricField(ShowElectricPotential):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.6,
        "d_theta": PI / 6,
        "dr": 6,
        "has_particle": True,
        "has_labels": True,
        "dashed_line_group": VGroup(),
        "path_group": VGroup()
    }

    def construct(self):
        self.init_the_scene()

        formula_1 = VGroup(Tex("W = -\int_{a}^{b} F\cdot ds"), Tex("W(unit) = -\int_{a}^{b} E\cdot ds"))
        formula_1.arrange(RIGHT, buff=MED_LARGE_BUFF)
        formula_1.to_edge(DOWN, buff=LARGE_BUFF)

        self.particle.add_updater(
            lambda m: m.move_to(self.source.get_center() +
                                self.r.get_value() *
                                complex_to_R3(np.exp(1j * self.theta.get_value())))
        )


        self.play(FadeInFromPoint(self.vector_particle, self.particle.get_center() + LEFT * self.particle_radius))
        self.vector_particle.add_updater(lambda m: m.become(self.get_3d_vector("particle")))

        self.play(Write(formula_1))
        self.play(self.get_assistant_line())
        self.show_path(1, speed_factor=0.6)

        text_circular = Text("circular").set_color(WHITE)
        text_radial = Text("radial").set_color(WHITE)
        text_circular.move_to(self.path_group[0].get_center())
        text_radial.rotate(PI/6).move_to(self.path_group[1].get_center())

        self.play(GrowFromCenter(text_radial), GrowFromCenter(text_circular))
        self.wait()
        self.play(FadeToColor(self.path_group[1], YELLOW), FadeToColor(text_radial, YELLOW))
        self.play(ApplyWave(text_radial), ApplyWave(self.path_group[1]))
        self.wait(3)

class ShowElectricPotentialFaster(ShowElectricPotential):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.6,
        "d_theta": PI / 48,
        "dr": 0.5,
        "has_labels": False
    }
    def construct(self):
        self.init_the_scene()

        formula_1 = Tex(
            r"-\int_{a}^{b} E\cdot ds = -\frac{q }{4\pi\epsilon _{0} } \int_{a}^{b} \frac{dr }{r^{2} } = -\frac{q }{4\pi\epsilon _{0} } (\frac{1 }{r_{a} }- \frac{1 }{r_{b} }) ")
        formula_1.to_edge(DOWN, buff=LARGE_BUFF)

        self.particle.add_updater(
            lambda m: m.move_to(self.source.get_center() +
                                self.r.get_value() *
                                complex_to_R3(np.exp(1j * self.theta.get_value())))
        )

        self.force_particle_label.add_updater(lambda m: m.set_color(self.vector_particle.get_color()))
        self.vector_particle.add_updater(lambda m: m.become(self.get_3d_vector("particle")))

        self.add(formula_1, self.vector_particle)
        self.play(self.get_assistant_line())
        self.show_path(10, speed_factor=10)
        self.wait(2)

class ShowElectricPotentialFasterFaster(ShowElectricPotential):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.6,
        "d_theta": PI / 96,
        "dr": 0.25,
        "has_labels": False
    }

    def construct(self):
        self.init_the_scene()

        formula_1 = Tex(
            r"-\int_{a}^{b} E\cdot ds = -\frac{q }{4\pi\epsilon _{0} } \int_{a}^{b} \frac{dr }{r^{2} } = -\frac{q }{4\pi\epsilon _{0} } (\frac{1 }{r_{a} }- \frac{1 }{r_{b} }) ")
        formula_1.to_edge(DOWN, buff=LARGE_BUFF)

        self.particle.add_updater(
            lambda m: m.move_to(self.source.get_center() +
                                self.r.get_value() *
                                complex_to_R3(np.exp(1j * self.theta.get_value())))
        )

        line_a = DashedLine(start=self.source.get_center(), end=self.particle.get_center()).set_color(YELLOW)
        label_ra = Tex("r_{a}").next_to(line_a, DOWN, buff=SMALL_BUFF)
        line_a.add(label_ra)

        self.force_particle_label.add_updater(lambda m: m.set_color(self.vector_particle.get_color()))
        self.vector_particle.add_updater(lambda m: m.become(self.get_3d_vector("particle")))

        self.add(formula_1, self.vector_particle)
        self.play(self.get_assistant_line())
        self.show_path(20, speed_factor=20)

        self.wait(2)

class ShowElectricPotentialRandomly(ShowElectricPotential):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.6,
        "has_particle": False
    }

    def construct(self):
        self.init_the_scene()

        formula_1 = Tex(
            r"-\int_{a}^{b} E\cdot ds = -\frac{q }{4\pi\epsilon _{0} } \int_{a}^{b} \frac{dr }{r^{2} } = -\frac{q }{4\pi\epsilon _{0} } (\frac{1 }{r_{a} }- \frac{1 }{r_{b} }) ")
        formula_1.to_edge(DOWN, buff=LARGE_BUFF)
        formula_2 = Tex(
            r" W(unit) = -\int_ {\underset{\underset{path}{any} }{a} }^{ \underset{}{b} }E\cdot ds"
        )
        formula_2.to_edge(DOWN, buff=LARGE_BUFF)

        dot_a = Sphere(radius=0.1, color=WHITE)
        dot_b = Sphere(radius=0.1, color=WHITE)
        dot_a.move_to(np.array([5, 0, 0]))
        dot_b.move_to(np.array([-3 + 3 * np.cos(5/24 * PI), 3 * np.sin(5/24 * PI), 0]))
        label_a = Tex("a").next_to(dot_a, RIGHT, buff=SMALL_BUFF)
        label_b = Tex("b").next_to(dot_b, LEFT, buff=SMALL_BUFF)
        line_a = DashedLine(start=self.source.get_center(), end=dot_a.get_center()).set_color(WHITE)
        line_b = DashedLine(start=self.source.get_center(), end=dot_b.get_center()).set_color(WHITE)
        label_ra = Tex("r_{a}").move_to(line_a.get_center())
        label_rb = Tex("r_{b}").move_to(line_b.get_center())

        self.add(formula_1, dot_a, dot_b, label_a, label_b, line_a, line_b, label_ra, label_rb)
        p = dot_a.get_center()
        q = dot_b.get_center()

        solid_path_a = VMobject().set_points_smoothly([
            p,
            q + DOWN * 1.5 + RIGHT * 2,
            q
        ]).set_color(YELLOW)

        solid_path_b = VMobject().set_points_smoothly([
            p,
            p + LEFT * 1 + UP * 0.5,
            p + LEFT * 2 + UP * 2,
            p + LEFT * 1 + UP * 3,
            p + LEFT * 1 + UP * 1,
            p + LEFT * 3 + UP * 2,
            p + LEFT * 4 + UP * 3,
            p + LEFT * 5.5 + UP * 3,
            q
        ]).set_color(YELLOW)

        self.play(
            ShowCreation(
                solid_path_a,
                rate_func=bezier([0, 0, 1, 1]),
                run_time=3,
            )
        )
        self.wait()
        self.remove(solid_path_a)
        self.play(
            ShowCreation(
                solid_path_b,
                rate_func=bezier([0, 0, 1, 1]),
                run_time=3,
            )
        )

        self.play(FadeOut(solid_path_b))
        self.play(CircleIndicate(label_ra), CircleIndicate(label_rb), run_time=2)
        self.play(Transform(formula_1, formula_2))
        self.wait(4)

class ShowDefinePotential(ShowElectricPotential):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "vector_length_init": 0.6,
        "has_particle": False
    }

    def construct(self):
        self.init_the_scene()
        frame = self.camera.frame
        p = Sphere(radius=0.2).move_to(np.array([3, -2, 0]))
        tex_p = Tex("p").next_to(p, UP)
        p.add(tex_p)
        self.add(p)
        self.play(ApplyMethod(frame.shift, OUT*100 + RIGHT*40))
        orbit = Arc(radius=80, arc_center=self.source.get_center(), start_angle=-PI / 3, angle=2 * PI / 3,
                    n_components=30)
        p_zero = Sphere(radius=1).set_color(WHITE).move_to(self.source.get_center() + RIGHT * 80)
        tex_p0 = Tex("P_{0}").scale(10)
        tex_p0.next_to(p_zero, UP, buff=LARGE_BUFF)
        self.play(FadeIn(tex_p0), FadeIn(p_zero))
        tex_phi0 = Tex("\phi=0 V")
        tex_phi0.scale(10)
        tex_phi0.move_to(np.array([self.source.get_center() + RIGHT * 80 + DOWN * 20]))
        orbit = DashedVMobject(orbit, num_dashes=10, positive_space_ratio=0.8)
        self.play(Write(orbit), FadeIn(tex_phi0))
        self.wait(3)
        self.play(ApplyMethod(frame.shift, IN * 100 + LEFT * 40))

        formula_1 = self.get_formula("", " \phi(p)=- \int_{p_{0 } }^{p } E \cdot ds")
        self.play(Write(formula_1))
        formula_2 = self.get_formula("", r"\phi (x,y)=\frac{Q }{4\pi\epsilon _{0 } }\frac{1 }{r } ,r=\sqrt{x^2+y^2}", index=1)
        radius = DashedLine(self.source.get_center(), np.array([3, -2, 0])).set_color(WHITE)
        r = Tex("r").move_to(radius.get_center())
        radius.add(r)
        self.wait(2)
        self.play(Write(formula_2), FadeIn(radius))
        self.wait(5)


# 3D part
class PotentialFunction(ThreeDScene):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "axes_config": {
            # "x_range": np.array([-6, 6, 1]),
            # "y_range": np.array([-5, 5, 1]),
            # "z_range": np.array([-4, 4, 1]),
            "x_axis_config": {
                "tick_frequency": TAU / 8,
                "include_tip": False,
            },
            "num_axis_pieces": 1,
        },
        "sources": [[3, [0, 0, 0]]],
        "source_group": VGroup(),
        "tex_group": VGroup(),
        "monopole": False
    }
    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=60 * DEGREES,
        )
        light = self.camera.light_source
        light.move_to(np.array([2 * np.sqrt(3), -6, 4]))

        x = self.x = ValueTracker(1)
        y = self.y = ValueTracker(0)

        plane = self.get_plane()
        surface = self.get_surface()
        axes = self.get_3d_axes(surface)
        contour_curve_100 = self.get_contour_curve(1)
        contour_curve_50 = self.get_contour_curve(2)
        contour_curve_25 = self.get_contour_curve(4)

        self.add(plane, axes)
        source = self.get_source_charge()
        always_rotate(self.source_group[0])

        tc = get_charged_particle_3d("+", radius=0.1)
        tc.move_to(np.array([1.25, 0, 0]))
        tc_copy = tc.copy()
        tex_a = Tex("a").next_to(tc_copy, DOWN)
        self.play(GrowFromCenter(tc), FadeIn(tex_a))
        self.add(tc_copy)
        self.play(ApplyMethod(tc.move_to, np.array([3.75, 0, 0])))
        tex_b = Tex("b").next_to(tc, DOWN)
        vector = ThreeDVector(RIGHT*2, RIGHT * 1.5,
                              max_bottom_radius=0.1,
                              top_radius_to_bottom_radius=1
                              ).set_color(YELLOW)
        self.play(GrowFromCenter(vector), FadeIn(tex_b))
        tex_ep = Tex("\Delta E_{p}=?").set_color(YELLOW)
        tex_ep.add_background_rectangle(color=BLACK)
        tex_ep.fix_in_frame()
        tex_ep.scale(2)
        tex_ep.to_edge(UP)
        self.play(FadeIn(tex_ep))
        self.wait(5)
        self.play(FadeOut(tc), FadeOut(tc_copy), FadeOut(vector), FadeOut(tex_ep), FadeOut(tex_a), FadeOut(tex_b))

        self.play(FadeIn(surface))
        self.play(frame.set_euler_angles, {"theta": 0 * DEGREES, "phi": 80 * DEGREES},
                  frame.move_to, np.array([0, -4, 3]),
                  run_time=3, rate_func=smooth)

        self.play(*self.get_test_charge("+"))#, ApplyMethod(surface.set_opacity, 0.2))
        self.play(FadeIn(contour_curve_100))
        self.wait()
        self.play(ApplyMethod(x.set_value, 2), FadeIn(contour_curve_50), run_time=3)
        self.wait()
        self.play(ApplyMethod(x.set_value, 4), FadeIn(contour_curve_25), run_time=3)
        tex_ep = Tex("\phi \downarrow \Rightarrow E_{p} \downarrow ").set_color(YELLOW)
        tex_ep.add_background_rectangle(color=BLACK)
        tex_ep.fix_in_frame()
        tex_ep.scale(2)
        tex_ep.to_edge(UR)
        self.play(FadeIn(tex_ep))
        self.wait(5)
        self.play(FadeOut(self.test_charge), FadeOut(self.rod), FadeOut(tex_ep))

        self.x.set_value(1)

        self.play(ApplyMethod(surface.set_opacity, 0.4), *self.get_test_charge("-"))
        self.wait()
        self.play(ApplyMethod(x.set_value, 2), run_time=3)
        self.wait()
        self.play(ApplyMethod(x.set_value, 4), run_time=3)

        tex_ep = Tex(r"\phi \downarrow \Rightarrow E_{p} \uparrow  ").set_color(YELLOW)
        tex_ep.add_background_rectangle(color=BLACK)
        tex_ep.fix_in_frame()
        tex_ep.scale(2)
        tex_ep.to_edge(UR)
        self.play(FadeIn(tex_ep))

        self.wait(5)


    def potential_fun(self, x, y):
        k = 1
        result = np.array([x, y, 0.])
        for source in self.sources:
            kq = k * source[0]
            r = np.sqrt((x - source[1][0]) ** 2 + (y - source[1][1]) ** 2)
            r_min = max(0.01, r)
            norm = kq / r_min
            result += np.array([0, 0, norm])
        return result

    def get_source_charge(self):
        for info in self.sources:
            source = get_charged_particle_3d(sign="+" if info[0] > 0 else "-",
                                             radius=0.5,
                                             opacity=1)
            source.move_to(np.array(info[1]) + UP * 0.5)
            self.add(source)
            self.source_group.add(source)

    def get_surface(self,
                    gloss=0.6,
                    opacity=0.8,
                    shadow=0.6,
                    **kwargs):
        return ParametricSurface(
            uv_func=self.potential_fun if not self.monopole else
            lambda r, theta: r * complex_to_R3(np.exp(1j * theta)) + 5/r * OUT,
            u_range=(-10, 10) if not self.monopole else (0.01, 10),
            v_range=(-10, 10) if not self.monopole else (0, TAU),
            color=RED if self.sources[0][0] > 0 else BLUE_E,
            gloss=gloss,
            opacity=opacity,
            shadow=shadow,
        )

    def get_mesh_surface(self, surface):
        return SurfaceMesh(surface,
                           stroke_width=2,
                           resolution=(10, 10))

    def get_contour_curve(self, r):
        contour_curve = ParametricCurve(
            t_func=lambda t: np.array([r * np.cos(t), r * np.sin(t), self.sources[0][0]/r]),
            t_range=[0, TAU, 0.1],
            color=YELLOW
        )
        tex = Tex(f"\phi = {int(100/r)} V") if self.sources[0][0] > 0 else Tex(f"\phi = {-int(100/r)} V")
        tex.set_color(YELLOW)
        tex.rotate(PI/2, RIGHT)
        tex.move_to(np.array([r, 0, self.sources[0][0]/r]))
        self.tex_group.add(tex)
        contour_curve.add(tex)
        return contour_curve

    def get_plane(self, u_min=-10, u_max=10, v_min=-10, v_max=10):
        surface_config = {
            "u_min": u_min,
            "u_max": u_max,
            "v_min": v_min,
            "v_max": v_max,
            "resolution": (20, 20),
            "checkerboard_colors": [GREY_BROWN, GREY_B]
        }
        plane = ParametricSurfaceOLD(
            lambda x, y: np.array([
                x, y, 0.
            ]),
            **surface_config,
        )
        plane.set_style(
            fill_opacity=0.2,
            stroke_width=0.5,
            stroke_color=WHITE,
        )
        return plane

    def get_3d_axes(self, surface, height=20, width=20):
        axes = ThreeDAxes(x_range=np.array([0, 20, 2]),
                            y_range=np.array([0, 20, 2]),
                            z_range=np.array([-5, 5, 1]),
                            height=height,
                            width=width)
        axes.rotate(-PI/2)
        axes.move_to(np.array([0, 0, 0]))
        function_tex = Tex(r"\phi (x,y)= \frac{kQ_{+} }{r_{+ } } + \frac{kQ_{-} }{r_{-} } ").set_color_by_gradient([BLUE_E, RED_E])
        function_tex.rotate(PI/2, RIGHT)
        function_tex.next_to(axes.get_edge_center(OUT), RIGHT, buff=LARGE_BUFF).shift(IN*2)
        axes.add(function_tex)
        self.tex_group.add(function_tex)
        return axes

    def get_test_charge(self, sign):
        test_charge = self.test_charge = self.test_charge = get_charged_particle_3d(sign, radius=0.2, opacity=0.999)
        if sign == "+":
            test_charge.add_updater(lambda m: m.move_to(np.array([self.x.get_value(),
                                                              self.y.get_value(),
                                                              self.potential_fun(self.x.get_value(), self.y.get_value())[2] + MED_SMALL_BUFF])
                                                        ))
        else:
            test_charge.add_updater(lambda m: m.move_to(np.array([self.x.get_value(),
                                                                  self.y.get_value(),
                                                                  self.potential_fun(self.x.get_value(),
                                                                                     self.y.get_value())[2] - MED_SMALL_BUFF])
                                                        ))
        if sign == "+":
            rod = self.rod = Line3D(start=np.array([self.x.get_value(), self.y.get_value(), 0]),
                        end=test_charge.get_center() - OUT * MED_LARGE_BUFF)
            rod.add_updater(
                lambda m: m.become(Line3D(
                        start=np.array([self.x.get_value(), self.y.get_value(), 0]),
                        end=test_charge.get_center() - OUT * MED_LARGE_BUFF,
                        width=0.2),

                            ))
        else:
            rod = self.rod = Line3D(start=np.array([self.x.get_value(), self.y.get_value(), 0]),
                                    end=test_charge.get_center() + OUT * MED_LARGE_BUFF)
            rod.add_updater(
                lambda m: m.become(Line3D(
                    start=np.array([self.x.get_value(), self.y.get_value(), 0]),
                    end=test_charge.get_center() + OUT * MED_LARGE_BUFF,
                    width=0.2),
                ))

        return [FadeIn(test_charge), FadeIn(rod)]

class PotentialForNegative(PotentialFunction):
    CONFIG = {
        "camera_class": ThreeDCamera,
        "source_radius": 0.8,
        "particle_radius": 0.1,
        "axes_config": {
            # "x_range": np.array([-6, 6, 1]),
            # "y_range": np.array([-5, 5, 1]),
            # "z_range": np.array([-4, 4, 1]),
            "x_axis_config": {
                "tick_frequency": TAU / 8,
                "include_tip": False,
            },
            "num_axis_pieces": 1,
        },
        "sources": [[-3, [0, 0, 0]]],
        "source_group": VGroup(),
        "tex_group": VGroup(),
        "monopole": False
    }

    def construct(self):
        frame = self.camera.frame

        light = self.camera.light_source
        light.move_to(np.array([0, 0, 3]))

        x = self.x = ValueTracker(-4)
        y = self.y = ValueTracker(0)

        plane = self.get_plane()
        surface = self.get_surface(opacity=1)
        axes = self.get_3d_axes(surface)
        contour_curve_100 = self.get_contour_curve(1)
        contour_curve_50 = self.get_contour_curve(2)
        contour_curve_25 = self.get_contour_curve(4)

        self.add(plane, axes, surface)
        source = self.get_source_charge()

        frame.set_euler_angles(theta=0 * DEGREES, phi=70 * DEGREES)
        frame.move_to, np.array([0, -4, 3])

        always_rotate(self.source_group[0])
        tex_ep = Tex("Q < 0 \Rightarrow \phi < 0 ").set_color(YELLOW)
        tex_ep.add_background_rectangle(color=BLACK)
        tex_ep.fix_in_frame()
        tex_ep.scale(2)
        tex_ep.to_edge(UR)

        self.play(LaggedStartMap(FadeIn, VGroup(contour_curve_25, contour_curve_50, contour_curve_100), lag_ratio=0.6))
        self.play(FadeIn(tex_ep))
        self.wait()
        self.play(ApplyMethod(light.move_to, np.array([0, -2, -3])),
        frame.set_euler_angles, {"theta": 0 * DEGREES, "phi": 120 * DEGREES}, run_time=4)
        self.wait(3)

class PotentialForDipole(PotentialFunction):
    CONFIG = {
        "sources": [[1, [-2, 0, 0]], [-1, [2, 0, 0]]],
        "monopole": False
    }

    def construct(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=60 * DEGREES,
        )
        light = self.camera.light_source
        light.move_to(np.array([2 * np.sqrt(3), -6, 4]))


        plane = self.get_plane(u_min=-5, u_max=5, v_min=-5, v_max=5)
        surface = ParametricSurfaceOLD(
            func=self.potential_fun,
        )

        source_pos = get_charged_particle_3d("+", radius=0.5)
        source_pos.move_to(np.array([-2, 0, 0]))
        source_neg = get_charged_particle_3d("-", radius=0.5)
        source_neg.move_to(np.array([2, 0, 0]))

        z_max = 1
        colors = color_gradient([BLUE_E, RED_E], 101)

        for ff in surface:
            f_z = ff.get_center()[-1]
            ff.set_fill(colors[50 + int(50 * max(-1, min(1, f_z/z_max)))])

        axes = self.get_3d_axes(surface, height=10, width=10)

        self.add(axes, plane, source_pos, source_neg)
        always_rotate(source_pos)
        always_rotate(source_neg)
        self.wait(3)
        self.play(FadeIn(surface))
        self.play(frame.set_euler_angles, {
            "theta": -30 * DEGREES,
            "phi": 60 * DEGREES}, run_time=5
        )
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=60 * DEGREES,
        )

        self.y = ValueTracker(-0.2)

        sliced_curve = self.get_sliced_graph()
        slices_plane = Square3D(u_range=(-5, 5), v_range=(-2, 2), opacity=0.4)
        slices_plane.rotate(PI/2, RIGHT)
        slices_plane.move_to(np.array([0, self.y.get_value(), 0]))
        self.play(FadeIn(sliced_curve), FadeIn(slices_plane))
        self.remove(source_pos, source_neg)
        self.wait(3)
        sliced_curve.add_updater(lambda m: m.become(self.get_sliced_graph()))
        slices_plane.add_updater(lambda m: m.move_to(np.array([0, self.y.get_value(), 0])))
        self.play(ApplyMethod(self.y.set_value, -3), run_time=6)
        self.play(ApplyMethod(self.y.set_value, -0.2), run_time=6)
        self.wait()
        self.y.set_value(0.2)
        self.play(ApplyMethod(self.y.set_value, 3), run_time=6)
        self.play(ApplyMethod(self.y.set_value, 0.2), run_time=6)
        self.wait()

    def get_sliced_graph(self):
        y = self.y
        return ParametricCurve(
            t_func=lambda t: np.array([t, y.get_value(), self.potential_fun(t, y.get_value())[2]]),
            t_range=(-5, 5),
            stroke_width=3,
            color=YELLOW
        )

class DipolePotential2D(Scene):
    CONFIG = {
        "sources": [[1, [-2, 0, 0]], [-1, [2, 0, 0]]]
    }
    def construct(self):
        y = self.y = ValueTracker(-0.2)
        grpah = FunctionGraph(
            self.potential_func,
            x_range=[-8, 8, 0.25]
        )
        axes = Axes(width=14, height=8)
        axes.add(axes.get_y_axis_label("\phi(x, y)"))
        axes.add(axes.get_x_axis_label("x"))
        self.add(grpah, axes)
        self.wait(3)
        grpah.add_updater(lambda m: m.become(FunctionGraph(self.potential_func, x_range=[-8, 8, 0.25])))
        self.play(ApplyMethod(self.y.set_value, -3), run_time=6)
        self.play(ApplyMethod(self.y.set_value, -0.2), run_time=6)
        self.wait()
        self.y.set_value(0.2)
        self.play(ApplyMethod(self.y.set_value, 3), run_time=6)
        self.play(ApplyMethod(self.y.set_value, 0.2), run_time=6)
        self.wait()

    def potential_func(self, x):
        k = 1
        y = self.y.get_value()
        result = np.array([x, y, 0.])
        for source in self.sources:
            kq = k * source[0]
            r = np.sqrt((x - source[1][0]) ** 2 + (y - source[1][1]) ** 2)
            r_min = max(0.01, r)
            norm = kq / r_min
            result += np.array([0, 0, norm])
        return result[2]

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
    return particle_position_group

class MoleculeOrbit(StaticSourceScene):
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
