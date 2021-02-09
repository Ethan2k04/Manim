from manimlib.imports import *
class EllipseSample(Scene):
    def construct(self):
        coor = NumberPlane()
        self.add(coor)
        cir_1 = Circle(radius = 2,color=YELLOW)
        self.add(cir_1)
        self.wait()
        ell_1 = Ellipse(width=6,height=4).set_stroke(color=ORANGE)
        self.play(Transform(cir_1,ell_1))
        ecc_a = Dot(np.array([-np.sqrt(5),0,0]))
        ecc_b = Dot(np.array([np.sqrt(5),0,0]))
        self.play(FadeIn(ecc_a),FadeIn(ecc_b))


