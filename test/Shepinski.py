from manimlib.imports import *

class ShepinskiAssembly(Scene):
    def Taowa(self,n,t,tri,Vgroup):
        if n == 1:
            tri_0 = Triangle().set_width(n)
            Vgroup.add(tri_0)
            return tri_0
        if n == 2 :
            tri_1 = Triangle().set_width(n/2).rotate(PI)
            Vgroup.add(tri_1)
            return tri_1
        if n > 2:
            tri_n_a = Triangle().set_width(n/(2**(t-1)))
            tri_n_b = Triangle().set_width(n / (2 ** (t - 1)))
            tri_n_c = Triangle().set_width(n / (2 ** (t - 1)))
            tri_n_a.next_to(self.Taowa(n,t-2,tri_n_a),UP,buff=0)
            tri_n_b.move_to(self.Taowa())
            Vgroup.add(tri_n)

    def construct(self):
        self.play(ShowCreation(tri_0))

class Test(Scene):
    def construct(self):
        a = Triangle()
        b = Triangle().rotate(PI).next_to(a,UR,buff=0)
        self.play(ShowCreation(a),ShowCreation(b))