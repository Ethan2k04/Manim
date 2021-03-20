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
    def construct(self):
        walker_group = RandomWalker(factor=0.2).get_grid(10, 10, height=4)
        walker_group.set_submobject_colors_by_gradient(BLUE, GREEN)
        for i in range(20):
            for sub in walker_group:
                sub.get_direction()
            self.play(*[ApplyMethod(sub.shift, sub.direction) for sub in walker_group], run_time=0.5)