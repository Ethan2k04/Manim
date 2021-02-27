from manimlib import *

#utils
def rate_func(decrease_factor=1):
    return lambda t: (1 / decrease_factor) * t ** 2

def opacity_func(decrease_factor=1, increase_factor=1):
    return lambda t: increase_factor * 1500 * (1 - abs(decrease_factor * t) ** 0.0001)

def get_ball(color, sign, radius=0.3):
    result = Circle(
        stroke_color=WHITE,
        stroke_width=0,
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

def discrete_points_on_circle(num=10, radius=1):
    delta_t = TAU/num
    point_group = []
    for p in range(num):
        theta = delta_t*p
        point = radius * np.array([np.cos(theta), np.sin(theta), 0])
        point_group.append(point)
    return point_group

#mobjects
class Ball(VGroup):
    CONFIG = {
        'radius': 4,
        "layer_radius": 2,
        'layer_num': 80,
        'opacity_func': lambda t: 1500 * (1 - abs(t - 0.009) ** 0.0001),
        'rate_func': lambda t: t ** 2,
        "sign": "A"
    }

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.color_list = color_gradient(self.colors, self.layer_num)
        particle = get_ball(color=self.color, sign=self.sign, radius=0.015 * self.radius)
        #self.add(Dot(color=average_color(self.colors[0], WHITE), plot_depth=4).set_height(0.015 * self.radius))
        self.add(particle)
        num_boundary = int(self.layer_num * (0.015 * self.radius/self.layer_radius) ** 0.5)
        for i in range(num_boundary, self.layer_num):
            self.add(Arc(radius=self.layer_radius * self.rate_func((0.5 + i) / self.layer_num), angle=TAU,
                         color=self.color_list[i],
                         stroke_width=101 * (self.rate_func((i + 1) / self.layer_num) - self.rate_func(
                             i / self.layer_num)) * self.layer_radius,
                         stroke_opacity=self.opacity_func(self.rate_func(i / self.layer_num)), plot_depth=5))

class ChasingBalls(VGroup):
    CONFIG = {
        "balls": VGroup(),
        "pos": [np.array([0., 4., 0.]), np.array([-2 * np.sqrt(3), -2, 0]), np.array([2 * np.sqrt(3), -2, 0])],
        "factor": 4
    }

    def __init__(self, *mobjects, **kwargs):
        VGroup.__init__(self, **kwargs)
        index = 0
        for mob in mobjects:
            self.balls.add(mob.move_to(self.pos[index]))
            index += 1
        for ball in self.balls:
            self.add(ball)

    def update_xy(self, dt):
        index = 0
        for pos in self.pos:
            velocity = self.pos[index-1] - self.pos[index]
            norm = abs(np.sqrt(sum(p ** 2 for p in velocity)))
            result = velocity * self.factor / norm
            self.pos[index] += result * dt
            index -= 1

    def update_balls(self, balls, dt=1/60):
        self.update_xy(dt)
        index = 0
        for ball in balls:
            ball.move_to(self.pos[index])
            index += 1

    def start_move(self):
        self.add_updater(self.update_balls)

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
#scene
class ChasingBallsScene(Scene):
    CONFIG = {
        "balls": VGroup(),
        "traces": VGroup(),
        "ball_radius": 0.1,
        "num": 16,
        "pos": discrete_points_on_circle(num=16, radius=2),
        "circle_radius": 2,
        "circle": True,
        "balls_color": ["#00b09b", "#96c93d"],
        "boundary_color": ORANGE,
        "factor": 2
    }

    def construct(self):
        self.get_balls()
        self.wait(10)

    def get_balls(self):
        colors = color_gradient(self.balls_color, self.num)
        index = 0
        for pos in self.pos:
            self.balls.add(get_ball(colors[index], f"{index}", radius=self.ball_radius))
            #self.traces.add(Trail(self.balls[index], trail_color=[colors[index-1], colors[index]]))
            index += 1
        chasing_balls = ChasingBalls(*self.balls, factor=self.factor, pos=self.pos)
        self.add(chasing_balls)
        for p in self.traces:
            self.add(p.trail)
        chasing_balls.start_move()
    

    def play_animated_boundary(self):
        if self.circle:
            boundary = Circle(radius=self.circle_radius)
            boundary.move_to(ORIGIN)
        else:
            boundary = Polygon(*self.pos)
        animated_boundary = AnimatedBoundary(boundary, colors=self.boundary_color)
        self.add(animated_boundary)

class ChasingBallsInCircuit(ChasingBallsScene):
    CONFIG = {
        "balls": VGroup(),
        "traces": VGroup(),
        "ball_radius": 0.01,
        "num": 16,
        "pos": discrete_points_on_circle(num=16, radius=3),
        "circle_radius": 2,
        "circle": True,
        "balls_color": [RED_D, ORANGE, YELLOW_D, WHITE],
        "boundary_color": [RED_D, ORANGE, YELLOW_D, WHITE],
        "factor": 3
    }

    def construct(self):
        self.get_balls()
        self.wait(5)
