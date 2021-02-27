from manimlib.imports import *

class ListColorGradient(Scene):
    CONFIG = {"reference_color": [Flare, Summer_Dog, Rainbow_Blue],
              "color_name": ["Flare", "Summer Dog", "Rainbow Blue"]}
    def construct(self):
        frame_height = self.camera.get_frame_height()
        frame_width = self.camera.get_frame_width()
        group = VGroup()
        i = 0
        for color in self.reference_color:
            group.add(self.add_sample(i))
            i += 1
        group.arrange(RIGHT)
        group.move_to(ORIGIN)
        self.play(LaggedStart(*[FadeInFromLarge(box, 0.3) for box in group], lag_ratio=0.2))
        self.play(ApplyMethod(group.arrange, LEFT))
        self.play(ApplyMethod(group.arrange, UP))
        self.play(ApplyMethod(group.arrange, UR))

    def add_sample(self, index):
        box = Square(stroke_opacity=0, fill_opacity=1).set_sheen(0.5, RIGHT)
        box.set_fill(self.reference_color[index])
        title = TextMobject(self.color_name[index])
        title.add_updater(lambda m: m.next_to(box, DOWN * 0.5))
        return VGroup(box, title)

class Test(Scene):
    CONFIG = {"camera_config": {"background_color": BLACK}}

    def construct(self):
        box = Square(stroke_opacity=0, fill_opacity=1).set_sheen(0.5, RIGHT)
        box.set_fill(Solid_Vault)
        self.play(FadeIn(box))
        self.wait()