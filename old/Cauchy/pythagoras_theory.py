from manimlib.imports import *

class PythagorasTheory(Scene):
    def construct(self):
        # making object
        tri_0 = Polygon(UL,LEFT,RIGHT).set_stroke(WHITE)
        tri_1 = tri_0.copy().set_fill(BLUE,opacity=0.8).set_stroke(WHITE)
        tri_1.shift(LEFT*0.5+DOWN*1.5)
        tri_2 = tri_0.copy().set_fill(BLUE,opacity=0.8).set_stroke(WHITE)
        tri_3 = tri_0.copy().set_fill(BLUE,opacity=0.8).set_stroke(WHITE)
        tri_4 = tri_0.copy().set_fill(ORANGE,opacity=0.8).set_stroke(WHITE)
        square_small = Polygon(np.array([1.5,0.5,0]),
                               np.array([-0.5,1.5,0]),
                               np.array([-1.5,-0.5,0]),
                               np.array([0.5,-1.5,0]))
        square_small.set_fill(GREEN,opacity=0.8).set_stroke(WHITE)

        intro_1 = TextMobject("这是我们小学二年级就学过的勾股弦图").scale(0.8).shift(RIGHT*3+UP*2)
        intro_2 = TextMobject("其中").next_to(intro_1,DOWN).scale(0.8).align_to(intro_1,LEFT)
        formula_1 = TexMobject("a^{2}","+","b^{2}","=","c^{2}").next_to(intro_2,DR).scale(1.5)
        intro_3 = TextMobject("历史上关于勾股定理的证明有很多").scale(0.8).next_to(formula_1, DOWN*4.5).align_to(intro_1,LEFT)
        intro_4 = TextMobject("下面将给出其中的一个").scale(0.8).next_to(intro_3, DOWN ).align_to(intro_3,LEFT)
        formula_1[0].set_color(ORANGE)
        formula_1[2].set_color(BLUE)
        formula_1[4].set_color(YELLOW)


        # animation
        self.play(ShowCreation(tri_0))
        self.play(ApplyMethod(tri_0.set_fill,{"color":BLUE,"opacity":0.8}))
        self.play(Transform(tri_0,tri_1))
        self.play(Transform(tri_1,tri_2.rotate(PI / 2).align_to(tri_1,RIGHT).shift(DR)))
        self.play(Transform(tri_2, tri_3.rotate(PI).align_to(tri_2,RIGHT).shift(UP*0.5)))
        self.play(Transform(tri_3, tri_4.rotate(PI * (3 / 2)).align_to(tri_3, LEFT).shift(LEFT)))
        self.play(GrowFromCenter(square_small))
        big_square = VGroup(tri_0, tri_1, tri_2, tri_3, square_small)
        self.play(ApplyWave(big_square))
        self.play(ApplyMethod(big_square.shift,LEFT*2.5))
        self.play(Write(intro_1))
        self.play(Write(intro_2))
        self.play(Write(formula_1))

        brace_a = Brace(tri_0,LEFT,buff=SMALL_BUFF)
        brace_b = Brace(tri_0,DOWN,buff=SMALL_BUFF)
        value_a = TextMobject("a").add_updater(lambda m:m.next_to(brace_a,LEFT,buff=0.1)).set_color(ORANGE)
        value_b = TextMobject("b").add_updater(lambda m: m.next_to(brace_b, DOWN, buff=0.1)).set_color(BLUE)
        value_c = TextMobject("c").add_updater(lambda m: m.move_to(tri_0.get_center()+RIGHT*0.2)).set_color(YELLOW)
        y_minus_x = ValueTracker(-1)
        def transform_tri_0(mob,dt):
            mob.set_height((3 + y_minus_x.get_value())/2,stretch=True,about_point=VGroup.get_corner(big_square,DL))
            mob.set_width((3 - y_minus_x.get_value()) / 2,stretch=True,about_point=VGroup.get_corner(big_square,DL))
        def transform_tri_1(mob,dt):
            mob.set_width((3 + y_minus_x.get_value())/2,stretch=True,about_point=VGroup.get_corner(big_square,DR))
            mob.set_height((3 - y_minus_x.get_value()) / 2,stretch=True,about_point=VGroup.get_corner(big_square,DR))
        def transform_tri_2(mob,dt):
            mob.set_height((3 + y_minus_x.get_value())/2,stretch=True,about_point=VGroup.get_corner(big_square,UR))
            mob.set_width((3 - y_minus_x.get_value()) / 2,stretch=True,about_point=VGroup.get_corner(big_square,UR))
        def transform_tri_3(mob,dt):
            mob.set_width((3 + y_minus_x.get_value())/2,stretch=True,about_point=VGroup.get_corner(big_square,UL))
            mob.set_height((3 - y_minus_x.get_value()) / 2,stretch=True,about_point=VGroup.get_corner(big_square,UL))
        def update_small_squ(mob,dt):
            mob.set_points_as_corners([tri_0.get_corner(UL),tri_1.get_corner(DL),tri_2.get_corner(DR),tri_3.get_corner(UR)])
        tri_0.add_updater(transform_tri_0)
        tri_1.add_updater(transform_tri_1)
        tri_2.add_updater(transform_tri_2)
        tri_3.add_updater(transform_tri_3)
        square_small.add_updater(update_small_squ)
        brace_a.add_updater(lambda m:m.next_to(tri_0,LEFT,buff=0.1)).add_updater(lambda m:m.set_height(tri_0.get_height(),stretch=True))
        brace_b.add_updater(lambda m: m.next_to(tri_0,DOWN, buff=0.1)).add_updater(lambda m:m.set_width(tri_0.get_width(),stretch=True))
        tri_0_height = DecimalNumber(tri_0.get_height()**2).add_updater(lambda m:m.set_value(tri_0.get_height()**2)).set_color(ORANGE).next_to(formula_1[0],DOWN*1.5)
        tri_0_width = DecimalNumber(tri_0.get_width()**2).add_updater(lambda m:m.set_value(tri_0.get_width()**2)).set_color(BLUE).next_to(formula_1[2],DOWN*1.5)
        tri_0_slide = DecimalNumber(tri_0_height.get_value()+tri_0_width.get_value()).add_updater(
            lambda m: m.set_value(tri_0_height.get_value()+tri_0_width.get_value())).set_color(YELLOW).next_to(formula_1[4], DOWN * 1.5)
        self.play(FadeIn(brace_a),FadeIn(brace_b),FadeIn(value_a),FadeIn(value_b),FadeIn(value_c))
        self.play(FadeInFrom(tri_0_height,UP),FadeInFrom(tri_0_width,UP),FadeInFrom(tri_0_slide,UP))
        self.play(y_minus_x.increment_value,2)
        self.play(y_minus_x.increment_value,-1)
        self.play(y_minus_x.increment_value, 2,Write(intro_3))
        self.play(y_minus_x.increment_value,-3,Write(intro_4))
        self.play(y_minus_x.increment_value,-1)
        self.play(y_minus_x.increment_value, -0.5)
        self.play(y_minus_x.increment_value, +4)
        self.play(y_minus_x.increment_value, -2)

class PythagorasTheoryProof(Scene):
    def construct(self):
        # making object
        tri_1 = Polygon(UL, LEFT, RIGHT).set_fill(BLUE,opacity=0.8).set_stroke(WHITE).shift(LEFT*0.5+DOWN*1.5)
        tri_2 = tri_1.copy()
        tri_3 = tri_1.copy()
        tri_4 = tri_1.copy()
        tri_2.rotate(PI / 2).align_to(tri_1, RIGHT).shift(RIGHT*1+UP*0.5)
        tri_3.rotate(PI).align_to(tri_2, UR).shift(UP)
        tri_4.rotate(PI * (3 / 2)).align_to(tri_3, LEFT).shift(LEFT+UP*1.5)
        square_small = Polygon(np.array([-1.5, -0.5, 0]),
                               np.array([0.5, -1.5, 0]),
                               np.array([1.5, 0.5, 0]),
                               np.array([-0.5, 1.5, 0]))
        square_small.set_fill(GREEN, opacity=0.8).set_stroke(WHITE)
        big_square = VGroup(tri_1, tri_2, tri_3, tri_4, square_small)
        size_square = Polygon(np.array([-1.5, 1.5, 0]),
                               np.array([1.5, 1.5, 0]),
                               np.array([1.5, -1.5, 0]),
                               np.array([-1.5, -1.5, 0])).set_stroke(color=RED,width=10,opacity=1)
        big_square_c = VGroup(big_square.copy(),size_square.copy())
        size_value = TextMobject("面积为:","S")
        size_value[1].set_color(RED).scale(2).shift(RIGHT*0.5)
        size_value.shift(UP*1+RIGHT*3)
        s1 = TexMobject("S_{1}").set_color(WHITE)
        s2 = TexMobject("S_{2}").set_color(WHITE)
        letter_a = TextMobject("a").set_color(ORANGE)
        letter_a_c = letter_a.copy()
        letter_b = TextMobject("b").set_color(BLUE)
        letter_b_c = letter_b.copy()
        equation = TexMobject("a^{2}","+","b^{2}","=","S_{1}","+","S_{2}").align_to(size_value,DL).shift(DOWN)
        # animation
        self.play(FadeInFromDown(big_square))
        self.play(ShowCreation(size_square))

        self.play(Write(size_value[0]))
        size_square_c =size_square.copy()
        self.add(size_square_c)
        self.play(ReplacementTransform(size_square,size_value[1]))
        tri_1_c = tri_1.copy().rotate(-PI/2).align_to(tri_2,RIGHT).align_to(tri_2,UP)
        tri_3_c = tri_3.copy().rotate(-PI/2).align_to(tri_4,LEFT).align_to(tri_4,UP)
        square_small_c1 = Polygon(np.array([-1.5, -0.5, 0]),
                               np.array([-1.5,-1.5,0]),
                               np.array([0.5, -1.5, 0]),
                               np.array([0.5,0.5,0]),
                               np.array([1.5, 0.5, 0]),
                               np.array([-0.5, 1.5, 0])).set_fill(GREEN,opacity=0.8).set_stroke(opacity=0)
        square_small_c2 = Polygon(np.array([-1.5, -0.5, 0]),
                               np.array([-1.5,-1.5,0]),
                               np.array([0.5, -1.5, 0]),
                               np.array([0.5,0.5,0]),
                               np.array([1.5, 0.5, 0]),
                               np.array([1.5,1.5,0]),
                               np.array([-0.5, 1.5, 0]),
                               np.array([-0.5,-0.5,0])).set_fill(GREEN, opacity=0.8).set_stroke(opacity=0)
        square_small_c2_c = square_small_c2.copy()
        self.play(Transform(tri_1, tri_1_c),Transform(square_small,square_small_c1))
        self.remove(square_small)
        self.play(Transform(tri_3, tri_3_c),ApplyMethod(square_small_c1.set_stroke,color=None),Transform(square_small_c1,square_small_c2))
        self.remove(square_small_c1)
        tri_3_4 = VGroup(tri_3,tri_4)
        tri_3_4_c = tri_3_4.copy().rotate(PI/2).align_to(big_square,UL)
        sub_square_a = Polygon(np.array([0.5,1.5,0]),
                               np.array([1.5,1.5,0]),
                               np.array([1.5,0.5,0]),
                               np.array([0.5,0.5,0])).set_fill(GREEN, opacity=0.8).set_stroke(opacity=0)
        sub_square_b = Polygon(np.array([-1.5, 0.5, 0]),
                               np.array([0.5, 0.5, 0]),
                               np.array([0.5, -1.5, 0]),
                               np.array([-1.5, -1.5, 0])).set_fill(GREEN, opacity=0.8).set_stroke(opacity=0)
        self.play(Transform(tri_3_4, tri_3_4_c),Transform(square_small_c2,sub_square_a),Transform(square_small_c2_c,sub_square_b))
        self.add(sub_square_a)
        self.remove(square_small_c2)
        s1.shift(UR)
        s2.shift(DL*0.5)
        letter_a.shift(UP+RIGHT*0.3)
        letter_a_c.shift(UP*0.3+RIGHT)
        letter_b.shift(UP*0.3+LEFT*0.5)
        letter_b_c.shift(RIGHT*0.3+DOWN*0.5)
        self.play(GrowFromCenter(s1),GrowFromCenter(s2),FadeIn(letter_a),FadeIn(letter_b),FadeIn(letter_a_c),FadeIn(letter_b_c))
        self.wait()
        letter_a_copy = letter_a.copy()
        letter_a_c_copy = letter_a_c.copy()
        letter_b_copy = letter_b.copy()
        letter_b_c_copy = letter_b_c.copy()
        s1_copy = s1.copy()
        s2_copy = s2.copy()
        self.add(letter_a_copy,letter_a_c_copy,letter_b_copy,letter_b_c_copy,s1_copy,s2_copy)
        equation[0].set_color(ORANGE)
        equation[2].set_color(BLUE)
        self.play(Transform(letter_a,equation[0]),Transform(letter_a_c,equation[0]),Transform(letter_b,equation[2]),Transform(letter_b_c,equation[2]),Transform(s1,equation[4]),Transform(s2,equation[6]),FadeIn(equation[1]),FadeIn(equation[3]),FadeIn(equation[5]))
        self.remove(tri_3_4_c)
        self.remove(sub_square_b)
        self.remove(tri_1_c)
        self.wait()
        proof = VGroup(tri_1,tri_2,tri_3_4,size_square_c,square_small_c2_c,sub_square_a,s1,s2,letter_a,letter_b,letter_a_c,letter_b_c,size_value,equation,letter_a_copy,letter_a_c_copy,letter_b_copy,letter_b_c_copy,s1_copy,s2_copy)
        self.play(ApplyMethod(proof.shift,LEFT*4))
        self.play(GrowFromCenter(big_square_c.shift(RIGHT*4)))
        letter_c = TextMobject("c").move_to(np.array([3.25,0.5,0])).set_color(YELLOW)
        letter_c_c = letter_c.copy().move_to(np.array([3.5,-0.8,0]))
        s3 = TexMobject("S_{3}").move_to(np.array([4,0,0])).scale(2)
        self.play(FadeIn(letter_c),FadeIn(letter_c_c),GrowFromCenter(s3))
        formula_c = TexMobject("c^{2}","=","S_{3}").next_to(equation,DOWN).align_to(equation,LEFT)
        formula_c[0].set_color(YELLOW)
        letter_c_copy = letter_c.copy()
        letter_c_c_copy = letter_c_c.copy()
        s3_copy = s3.copy()
        self.add(letter_c_copy,letter_c_c_copy,s3_copy)
        self.play(Transform(letter_c,formula_c[0]),Transform(letter_c_c,formula_c[0]))
        self.play(FadeIn(formula_c[1]))
        self.play(Transform(s3,formula_c[2]))
        formula_s = TextMobject("又$\\because S_{1}+S_{2}=S_{3}$").next_to(formula_c,DOWN).align_to(formula_c,LEFT)
        self.wait(2)
        self.play(Write(formula_s))
        self.wait()
        formula_py = TexMobject("a^{2}","+","b^{2}","=","c^{2}").scale(1.5)
        formula_py[0].set_color(ORANGE)
        formula_py[2].set_color(BLUE)
        formula_py[4].set_color(YELLOW)
        self.play(ReplacementTransform(equation,formula_py),ReplacementTransform(formula_c,formula_py),ReplacementTransform(formula_s,formula_py),FadeOut(letter_c),FadeOut(letter_c_c),FadeOut(s3),FadeOut(letter_a),FadeOut(letter_a_c),FadeOut(letter_b),FadeOut(letter_b_c),FadeOut(s1),FadeOut(s2))
        self.wait()
        word_final = TextMobject("证毕")
        word_final.next_to(formula_py,DOWN).align_to(formula_py,LEFT)
        self.play(Write(word_final))