from manimlib.imports import *


class FibonacciSpiral(MovingCameraScene):

    def fibonacci_number(self,n):
        if n == 1:
            return 1
        if n == 2:
            return 1
        if n > 2:
            return self.fibonacci_number(n-1) + self.fibonacci_number(n-2)


    def fibonacci_series(self,n=10):
        series = []
        for i in range(n):
            series.append(self.fibonacci_number(i+1))
        return series


    def squ_direction(self,n):

        if n % 4 == 1:
            return RIGHT
        if n % 4 == 2:
            return UP
        if n % 4 == 3:
            return LEFT
        if n % 4 == 0:
            return DOWN


    def arc_direction_1(self,n):
        if n % 4 == 1:
            return DL
        if n % 4 == 2:
            return DR
        if n % 4 == 3:
            return UR
        if n % 4 == 0:
            return UL

    def arc_direction_2(self,n):
        if n % 4 == 1:
            return UR
        if n % 4 == 2:
            return UL
        if n % 4 == 3:
            return DL
        if n % 4 == 0:
            return DR


    def construct(self):
        square_length_list = self.fibonacci_series(20)
        squ_group = VGroup()
        arc_group = VGroup()
        squ_1 = Square().set_width(1).move_to(np.array([0.5,0.5,0])).set_fill(GREEN_A,opacity=0.8)
        squ_group.add(squ_1)
        arc_1 = ArcBetweenPoints(squ_1.get_corner(DL),squ_1.get_corner(UR),PI/2)
        arc_group.add(arc_1)
        sec_group = VGroup()
        self.camera_frame.scale(0.4)
        self.play(ShowCreation(arc_1),rate_func=linear)
        scale_factor = 1.5
        sec_color_list = [RED_D,ORANGE,TEAL_D,PURPLE_D,YELLOW_E]
        rec_color_list = [GREEN_E,MAROON_B,YELLOW_D,LIGHT_BROWN,DARK_BROWN]
        for i in range(len(square_length_list)):
            if i == 0:
                pass
            else:
                squ = Square().set_width(square_length_list[i]).set_fill(sec_color_list[(i-1)%5],opacity=0.8)
                squ.next_to(squ_group[i-1])
                squ.next_to(squ_group[i-1],self.squ_direction(i+1),buff=0)
                squ.align_to(squ_group[i-1],self.squ_direction(i))
                arc = ArcBetweenPoints(squ.get_corner(self.arc_direction_1(i+1)),squ.get_corner(self.arc_direction_2(i+1)),PI/2)
                sec = Sector(start_angle=-PI+(PI/2)*i,angle=PI/2).scale(square_length_list[i-1]).move_to(arc_group[i-1].get_center()).set_color(rec_color_list[(i-1)%5])
                self.play(ShowCreation(arc),FadeIn(sec),FadeIn(squ_group[i-1]),self.camera_frame.scale,scale_factor,rate_func=linear)
                squ_group.add(squ)
                arc_group.add(arc)
                sec_group.add(sec)

        self.wait()


class Intro(Scene):
    def copy_machine(self,mobject,n):
        group = VGroup()
        mobject_1 = mobject.copy()
        group.add(mobject_1)
        if n == 1:
            return mobject_1
        else:
            for i in range(n-1):
                mobject_2 = mobject_1.copy()
                mobject_2.next_to(group[i],DOWN*0.2)
                group.add(mobject_2)
            return group


    def construct(self):
        coin = ImageMobject("/Users/ytj/Desktop/ManimInstall/manim_7May/image/coin.png").scale(0.5)
        up_1 = ImageMobject("/Users/ytj/Desktop/ManimInstall/manim_7May/image/aoerjia_1.png")
        up_2 = ImageMobject("/Users/ytj/Desktop/ManimInstall/manim_7May/image/aoerjia_2.png")
        student = ImageMobject("/Users/ytj/Desktop/ManimInstall/manim_7May/image/rideon_1.png")
        text_1 = Text("UP主", font='SetoFont SC').set_color(ORANGE).scale(0.8)
        text_2 = Text("小朋友", font='SetoFont SC').set_color(ORANGE).scale(0.8)
        arrow_1 = Arrow(start=np.array([0,0,0]),end=np.array([0,-1,0])).next_to(text_1,DOWN,buff=0)
        arrow_2 = Arrow(start=np.array([0, 0, 0]), end=np.array([0, -1, 0])).next_to(text_2, DOWN, buff=0)
        text_1_group = VGroup(text_1,arrow_1)
        text_2_group = VGroup(text_2, arrow_2)
        up_1.to_edge(DL,buff=1)
        up_2.to_edge(DL, buff=1)
        student.to_edge(DR,buff=1).align_to(up_1,DOWN)
        text_1_group.next_to(up_1,UP,buff=-0.2)
        text_2_group.next_to(student,UP,buff=-0.5)
        text_day_1 = Text("DAY 1", font='SetoFont SC').set_color(GREEN).scale(0.8).move_to(np.array([-3,3,0]))
        text_day_2 = Text("DAY 2", font='SetoFont SC').set_color(GREEN).scale(0.8).next_to(text_day_1,RIGHT*1.5)
        text_day_3 = Text("DAY 3", font='SetoFont SC').set_color(GREEN).scale(0.8).next_to(text_day_2,RIGHT*1.5)
        text_day_4 = Text("DAY 4", font='SetoFont SC').set_color(GREEN).scale(0.8).next_to(text_day_3, RIGHT * 1.5)
        text_day_5 = Text("DAY 5", font='SetoFont SC').set_color(GREEN).scale(0.8).next_to(text_day_4, RIGHT * 1.5)
        text_day_dot = Text("...", font='SetoFont SC').set_color(GREEN).scale(0.8).next_to(text_day_5,RIGHT*1.5)
        text_day_n = Text("DAY n", font='SetoFont SC').set_color(GREEN).scale(0.8).next_to(text_day_dot, RIGHT*1.5)
        text_question_mark = Text("?", font='SetoFont SC').set_color(ORANGE).scale(2).next_to(text_day_n,DOWN*2)
        fibonacci_list = [1,1,2,3,5,8,13,21]
        coin_day1 = coin.copy().next_to(text_day_1,DOWN)
        coin_day2 = coin.copy().next_to(text_day_2, DOWN)
        coin_day3 = self.copy_machine(coin,2)
        coin_day3[0].next_to(text_day_3,DOWN)
        coin_day3[1].next_to(coin_day3[0], DOWN)
        coin_day4 = self.copy_machine(coin,3)
        coin_day4[0].next_to(text_day_4,DOWN)
        coin_day4[1].next_to(coin_day4[0], DOWN)
        coin_day4[2].next_to(coin_day4[1], DOWN)
        coin_day5 = self.copy_machine(coin, 5)
        coin_day5[0].next_to(text_day_5,DOWN)
        coin_day5[1].next_to(coin_day5[0],DOWN)
        coin_day5[2].next_to(coin_day5[1],DOWN)
        coin_day5[3].next_to(coin_day5[2],DOWN)
        coin_day5[4].next_to(coin_day5[3],DOWN)
        self.add(up_1,text_1_group,student,text_2_group)
        self.wait(2)
        self.play(FadeInFrom(text_day_1,LEFT))
        self.play(FadeInFrom(coin_day1,UP))
        self.wait()
        self.play(FadeInFrom(text_day_2,UP))
        self.play(TransformFromCopy(coin_day1,coin_day2))
        self.wait(0.5)
        self.play(FadeInFrom(text_day_3,UP))
        self.wait()
        self.play(TransformFromCopy(coin_day2,coin_day3[0]))
        self.wait(0.5)
        self.play(FadeInFrom(coin_day3[1],UP))
        self.wait()
        self.play(FadeInFrom(text_day_4,UP))
        self.play(TransformFromCopy(coin_day3[0],coin_day4[0]),TransformFromCopy(coin_day3[1],coin_day4[2]))
        self.wait(0.5)
        self.play(FadeInFrom(coin_day4[1],UP))
        self.wait()
        self.play(FadeInFrom(text_day_5,UP))
        self.play(TransformFromCopy(coin_day4[0],coin_day5[0]),TransformFromCopy(coin_day4[1],coin_day5[2]),TransformFromCopy(coin_day4[2],coin_day5[4]))
        self.wait(0.5)
        self.play(FadeInFrom(coin_day5[1],UP),FadeInFrom(coin_day5[3],DOWN))
        self.wait()
        self.play(FadeInFrom(text_day_dot,UP))
        self.play(FadeInFrom(text_day_n,UP))
        self.play(Transform(up_1,up_2),FadeInFromLarge(text_question_mark),run_time=2)
        self.wait(3)


class FibonacciSeries(Scene):

    def fibonacci_number(self,n):
        if n == 1:
            return 1
        if n == 2:
            return 1
        if n > 2:
            return self.fibonacci_number(n-1) + self.fibonacci_number(n-2)


    def construct(self):

        fibonacci_range = 13
        fibonacci_text = VGroup()
        self.wait()
        for i in range(fibonacci_range+3):
            if i == 0:
                pass
            if i == 1:
                text = Text("1", font='SetoFont SC')
                text.move_to(ORIGIN)
                fibonacci_text.add(text)
                self.add(fibonacci_text)
                self.wait()
            if 1 < i < fibonacci_range:
                text = Text(f",{self.fibonacci_number(i)}", font='SetoFont SC')
                text.next_to(fibonacci_text,RIGHT)
                fibonacci_text.add(text)
                self.play(ApplyMethod(fibonacci_text.move_to,ORIGIN),run_time=0.5)
            if i >= fibonacci_range:
                text = Text(" ... ", font='SetoFont SC')
                text.next_to(fibonacci_text, RIGHT)
                fibonacci_text.add(text)
                self.play(ApplyMethod(fibonacci_text.move_to, ORIGIN), run_time=0.5)
                # self.play(FadeInFromPoint(text,text.get_center()),run_time=0.5)
        self.wait()

class Tezhenggen(Scene):
    def construct(self):
        # coor = NumberPlane()
        # self.add(coor)
        text_1 = Text("递推公式：", font='SetoFont SC')
        tex_1 = TexMobject("x_{n-1}+x_{n}=x_{n+1}").next_to(text_1,RIGHT).set_color(YELLOW)
        text_1_group = VGroup(text_1,tex_1)
        text_1_group_copy = text_1_group.copy()
        text_1_group_copy.scale(0.4).move_to(np.array([-5,3,0]))
        text_2_1 = Text("数列前两项", font='SetoFont SC')
        tex_2 = TexMobject("x_{1}=1",",","x_{2}=1").next_to(text_1,RIGHT)
        text_2_2 = Text("已知", font='SetoFont SC').next_to(tex_2,RIGHT)
        text_2_group = VGroup(text_2_1,text_2_2,tex_2)
        text_2_group_copy = text_2_group.copy()
        text_2_group_copy.scale(0.4).next_to(text_1_group_copy,DOWN).align_to(text_1_group_copy,LEFT)
        text_2_group.next_to(tex_1,DOWN).align_to(text_1,LEFT)
        text_1_2_group = VGroup(text_1_group,text_2_group)
        text_1_2_group.move_to(ORIGIN)
        text_1_2_group_copy = VGroup(text_1_group_copy,text_2_group_copy)
        self.play(FadeInFromPoint(text_1_2_group,text_1_2_group.get_center()))
        self.wait(3)
        self.play(Transform(text_1_2_group,text_1_2_group_copy))
        self.wait(2)
        text_3 = Text("待定系数法,设:", font='SetoFont SC')
        tex_3 = TexMobject("x_{n+1}","-","ax_{n}","=","b(x_{n}-ax_{n-1})").set_color(YELLOW).next_to(text_3,RIGHT)
        text_3_group = VGroup(text_3,tex_3)
        text_3_group.move_to(ORIGIN)
        text_3_group_copy = text_3_group.copy().scale(0.4)
        text_3_group_copy[1].set_color(WHITE)
        text_3_group_copy.next_to(text_2_group_copy,DOWN).align_to(text_2_group_copy,LEFT)
        self.play(FadeInFromPoint(text_3_group[0],text_3_group[0].get_center()))
        self.play(FadeInFrom(text_3_group[1],LEFT))
        self.wait(3)
        text_4 = Text("整理得到", font='SetoFont SC')
        tex_4 = TexMobject("x_{n+1}","=","(a+b)x_{n}","-","abx_{n-1}").set_color(YELLOW).next_to(text_4,RIGHT)
        text_4_group = VGroup(text_4,tex_4)
        self.play(ApplyMethod(text_3_group.shift,UP*0.5))
        text_4_group.next_to(text_3_group,DOWN).align_to(text_3_group,LEFT)
        text_4_group_copy = text_4_group.copy()
        text_4_group_copy.scale(0.4).next_to(text_3_group_copy,DOWN).align_to(text_3_group_copy,LEFT)
        self.play(FadeInFromPoint(text_4,text_4.get_center()))
        self.wait(0.5)
        self.add(tex_3)
        self.play(TransformFromCopy(tex_3,tex_4),ApplyMethod(tex_3.set_color,WHITE))
        self.wait(3)
        self.play(Transform(text_3_group,text_3_group_copy))
        self.play(Transform(text_4_group, text_4_group_copy))
        self.wait()
        text_5 = Text("令", font='SetoFont SC')
        tex_5 = TexMobject(r"\begin{cases}a+b=1\\ab=-1\end{cases}").next_to(text_5,RIGHT)
        text_5_group = VGroup(text_5,tex_5)
        text_6_1 = Text("根据韦达定理,a和b是方程:", font='SetoFont SC')
        tex_6 = TexMobject("x^{2}","-","x","-","1","=","0").next_to(text_6_1,RIGHT).set_color(YELLOW)
        text_6_2 = Text("的实根", font='SetoFont SC').next_to(tex_6,RIGHT)
        text_6_3 = Text("解得", font='SetoFont SC')
        tex_6_1 = TexMobject(r"a=\frac{1+\sqrt{5}}{2}",",",r"b=\frac{1-\sqrt{5}}{2}").set_color(YELLOW).scale(0.8)
        text_6_3.next_to(text_6_1,DOWN).align_to(text_6_1,LEFT)
        tex_6_1.next_to(text_6_3,RIGHT).shift(DOWN*0.2)
        text_6_group = VGroup(text_6_1,tex_6,text_6_2,text_6_3,tex_6_1)
        text_5_group.move_to(ORIGIN)
        self.play(FadeInFromPoint(text_5_group,text_5_group.get_center()))
        self.wait(2)
        self.play(ApplyMethod(text_5_group.shift,UP*0.5))
        text_6_group.next_to(text_5_group, DOWN).align_to(text_5_group,ORIGIN)
        self.play(Write(text_6_group[0]))
        self.play(TransformFromCopy(tex_5,tex_6))
        self.play(Write(text_6_2))
        self.wait()
        self.play(Write(text_6_3))
        self.play(FadeInFrom(tex_6_1,LEFT))
        self.wait(6)
        text_5_group_copy = text_5_group.copy()
        text_5_group_copy.scale(0.4).next_to(text_4_group_copy,DOWN).align_to(text_1_group_copy,LEFT)
        text_6_group_copy = text_6_group.copy()
        text_6_group_copy.scale(0.4).next_to(text_5_group_copy,DOWN).align_to(text_5_group_copy,LEFT)
        self.play(Transform(text_5_group,text_5_group_copy),Transform(text_6_group,text_6_group_copy))
        self.wait(0.5)
        text_7_1 = Text("因此", font='SetoFont SC')
        tex_7_1 = TexMobject("\{ x_{n+1}-ax_{n} \}").set_color(YELLOW)
        text_7_2 = Text("是公比为b的等比数列,", font='SetoFont SC')
        text_7_3 = Text("累乘得:", font='SetoFont SC')
        tex_7_2 = TexMobject("x_{n+1}","-ax_{n}=(x_{2}-ax_{1})\cdot b^{n-1}").set_color(YELLOW)
        tex_7_1.next_to(text_7_1,RIGHT)
        text_7_2.next_to(tex_7_1,RIGHT)
        text_7_3.next_to(text_7_1,DOWN).align_to(text_7_1,LEFT)
        tex_7_2.next_to(text_7_3,RIGHT)
        text_7_group = VGroup(text_7_1,tex_7_1,text_7_2,text_7_3,tex_7_2)
        text_7_group_copy = text_7_group.copy()
        #line_1 = Line(start=np.array([-1.65,3.2,0]),end=np.array([-1.65,0,0]))
        text_7_group.add_background_rectangle(opacity=0.6).move_to(ORIGIN)
        text_7_group_copy.scale(0.4).next_to(text_6_group_copy,DOWN).align_to(text_1_group_copy,LEFT)
        self.play(FadeInFromPoint(text_7_group,text_7_group.get_center()))
        self.wait(4)
        self.play(Transform(text_7_group,text_7_group_copy))
        self.wait()
        text_8_1 = Text("同理", font='SetoFont SC')
        tex_8_1 = TexMobject("\{ x_{n+1}-bx_{n} \}").set_color(YELLOW)
        text_8_2 = Text("是公比为a的等比数列,", font='SetoFont SC')
        text_8_3 = Text("累乘得:", font='SetoFont SC')
        tex_8_2 = TexMobject("x_{n+1}","-bx_{n}=(x_{2}-bx_{1})\cdot a^{n-1}").set_color(YELLOW)
        tex_8_1.next_to(text_8_1, RIGHT)
        text_8_2.next_to(tex_8_1, RIGHT)
        text_8_3.next_to(text_8_1, DOWN).align_to(text_8_1, LEFT)
        tex_8_2.next_to(text_8_3, RIGHT)
        text_8_group = VGroup(text_8_1, tex_8_1, text_8_2, text_8_3, tex_8_2)
        text_8_group_copy = text_8_group.copy()
        text_8_group.add_background_rectangle(opacity=0.6).move_to(ORIGIN)
        text_8_group_copy.scale(0.4).next_to(text_7_group_copy,DOWN).align_to(text_7_group_copy,LEFT)
        self.play(FadeInFromPoint(text_8_group,text_8_group.get_center()))
        self.wait(4)
        self.play(Transform(text_8_group,text_8_group_copy))
        self.wait(0.5)
        tex_9_1 = tex_7_2.copy().scale(2.5).set_color(ORANGE).add_background_rectangle(opacity=0.6)
        tex_9_2 = tex_8_2.copy().scale(2.5).set_color(ORANGE).add_background_rectangle(opacity=0.6)
        tex_9_2.next_to(tex_9_1,DOWN)
        text_9 = VGroup(tex_9_1,tex_9_2).move_to(ORIGIN).shift(RIGHT*2)
        self.play(TransformFromCopy(text_7_group_copy[4],tex_9_1),TransformFromCopy(text_8_group_copy[4],tex_9_2))
        self.wait()
        self.play(FadeOutAndShiftDown(tex_9_1[1]),FadeOutAndShiftDown(tex_9_2[1]))
        self.wait()
        self.play(FadeOut(tex_9_1[2]),FadeOut(tex_9_2[2]))
        text_10 = Text("两式做差，得:", font='SetoFont SC')
        tex_10 = TexMobject(r"x_{n}=\frac{x_{2}-bx_{1}}{a-b}\cdot a^{n-1}+ \frac{x_{2}-ax_{1}}{b-a}\cdot b^{n-1}")
        tex_10.next_to(text_10,DOWN).align_to(text_10,LEFT)
        text_10_group = VGroup(text_10,tex_10).add_background_rectangle(opacity=0.6)
        text_10_group.move_to(ORIGIN)
        self.play(FadeInFromLarge(text_10_group))
        self.wait(3)
        tex_11 = TexMobject(r"x_{n}=\frac{1}{\sqrt{5}} [(\frac{1+\sqrt{5}}{2})^{n}-(\frac{1-\sqrt{5}}{2})^{n}]")
        tex_11.next_to(tex_10,DOWN)
        tex_10_copy = tex_10.copy().scale(0.4).next_to(text_8_group_copy, DOWN).align_to(text_8_group_copy, LEFT)
        self.play(ClockwiseTransform(tex_10,tex_11),FadeIn(tex_10_copy))
        self.play(FadeOut(tex_10),ApplyMethod(tex_11.shift,UP*1.5))
        self.wait(0.5)
        self.play(ApplyWave(tex_11))
        self.play(ApplyMethod(tex_11.set_color,YELLOW))
        self.wait(2)
        text_10_group.remove(tex_10)
        brace = Brace(text_1_group_copy,RIGHT).stretch_to_fit_height(5.5).move_to(ORIGIN).shift(UP*0.3+LEFT*1.5)
        self.play(FadeOut(text_10_group),FadeInFrom(brace,LEFT),ApplyMethod(tex_11.move_to,np.array([3,0.3,0])))
        self.wait(3)