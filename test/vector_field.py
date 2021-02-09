from manimlib.imports import *

class SimpleField(Scene):

    def construct(self):

        plane = NumberPlane(color=RED)
        plane.add(plane.get_axis_labels())
        self.add(plane)

        points = [ x * RIGHT + y * UP
                   for x in np.arange(-5,5,1)
                   for y in np.arange(-3,3,1)
                   ]

        vec_field = []
        for point in points:
            field = 0.5 * RIGHT + 0.5 * UP
            result = Vector(field).shift(point)
            vec_field.append(result)

        draw_field = VGroup(*vec_field)
        self.play(ShowCreation(draw_field),run_time=4)
        self.wait()


class VectorFieldSample(Scene):
    def construct(self):
        func = lambda p: np.array([
            p[0]/2,
            p[1]/2,
            0
        ])

        vector_field_norm = VectorField(func)

        vector_field_not_norm = VectorField(func,length_func=linear)
        self.play(*[GrowArrow(vec) for vec in vector_field_norm])
        self.wait(2)
        self.play(
            ReplacementTransform(
                vector_field_norm,
                vector_field_not_norm
            )
        )

def functioncurlreal(p,velocity=0.05):
    x,y = p[:2]
    result = - y * RIGHT + x * UP
    result *= velocity
    return result

class VectorFieldScene2(Scene):
    def construct(self):
        vector_field = VectorField(functioncurlreal)
        dot1 = Dot([1,1,0],color=RED)
        dot2 = Dot([2,2,0],color=BLUE)
        self.add(vector_field,dot1,dot2)
        self.wait()
        for dot in dot1,dot2:
            move_submobjects_along_vector_field(
                dot,
                lambda p: functioncurlreal(p,0.5)
            )
        self.wait(3)
        for dot in dot1,dot2:
            dot.clear_updaters()
        self.wait()