from manimlib import *

class RandomWalker(Dot):

    def __init__(self, num=314, factor=1.0, **kwargs):
        self.num = num
        self.factor = factor
        self.generate_direction()
        self.direction = None
        self.get_direction()
        super().__init__(**kwargs)

    def generate_direction(self):
        self.dir_list = [self.factor * np.array(
            [np.cos(2 * PI * (t/self.num)),
             np.sin(2 * PI * (t/self.num)),
             0]) for t in range(self.num)]

    def get_direction(self):
        direction = self.dir_list[random.randint(0, self.num-1)]
        #print(direction)
        self.direction = direction

class RandomWalkerScene1(Scene):
    def construct(self):
        plane = NumberPlane()
        #self.add(plane)
        walker = RandomWalker(factor=0.2)
        for i in range(20):
            walker.get_direction()
            self.play(walker.shift, walker.direction, run_time=0.1)

class RandomWalkerScene2(Scene):
    CONFIG = {
        "factor": 0.2,
        "rate_func": smooth,
        "dt": 0.5,
        "run_time": 10
    }

    def construct(self):
        walker_group = RandomWalker(factor=self.factor).get_grid(10, 10, height=4)
        walker_group.set_submobject_colors_by_gradient(BLUE, GREEN)
        for i in range(int(self.run_time/self.dt)):
            for sub in walker_group:
                sub.get_direction()
            self.play(*[ApplyMethod(sub.shift, sub.direction) for sub in walker_group],
                      rate_func=self.rate_func,
                      run_time=self.dt)

class RandomWalkerScene3(RandomWalkerScene2):
    CONFIG = {
        "factor": 0.01,
        "rate_func": linear,
        "dt": 0.1,
        "run_time": 10
    }

class RandomWalkerScene4(RandomWalkerScene2):
    CONFIG = {
        "factor": 2,
        "rate_func": linear,
        "dt": 0.1,
        "run_time": 10
    }