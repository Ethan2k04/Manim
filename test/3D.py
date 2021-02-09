from manimlib.imports import *

class CurveSurface(SpecialThreeDScene):

    def construct(self):
        self.set_camera_to_default_position()
        axes = self.get_axes()
        w = 1
        surface_01 =ParametricSurface(lambda u,v:v * complex_to_R3(np.exp(1j*w*u)),
                                      u_min=0,u_max=TAU,v_min=1,v_max=3,checkerboard_colors=None,
                                      fill_color=BLUE_B,fill_opacity=0.8,stroke_color=BLUE_A,resolution=(60,10))
                                                                                                        # u  v 方向上的分段数
        surface_02 = ParametricSurface(lambda u, v: v * complex_to_R3(np.exp(1j * w * u)) + OUT * u/PI * 2,
                                       u_min=0, u_max=TAU, v_min=1, v_max=3,
                                       checkerboard_colors=None,fill_color=BLUE_B, fill_opacity=0.8,
                                       stroke_color=BLUE_A, resolution=(60, 10))
        surface_01.set_shade_in_3d(True)
        surface_02.set_shade_in_3d(True)
        self.add(axes,surface_01)
        self.wait()
        self.begin_ambient_camera_rotation()
        self.play(TransformFromCopy(surface_01,surface_02,rate_func=linear),run_time=5)
        self.wait(2)

class Curve1(ThreeDScene):
    CONFIG = {"phi": 60 * DEGREES,
              "theta": 60 * DEGREES,
              "distance": 50}

    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        self.set_camera_orientation(phi=self.phi,theta=self.theta,distance=self.distance)
        curve1 = ParametricFunction(
            lambda u:np.array([
            1.2*np.cos(u),
            1.2*np.sin(u),
            u/2
        ]),color=RED,t_min=-TAU,t_max=TAU
        )

        curve2 = ParametricFunction(
            lambda u: np.array([
            1.2*np.cos(u),
            1.2*np.sin(u),
            u
        ]), color=RED, t_min=-TAU, t_max=TAU
        )

        curve1.set_shade_in_3d(True)
        curve2.set_shade_in_3d(True)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(ShowCreation(curve1))
        self.wait(3)
        self.play(Transform(curve1,curve2),rate_func=there_and_back,run_time=3)
        self.wait(3)

class Cube1(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": WHITE},
              "phi": 60 * DEGREES,
              "theta": 30 * DEGREES,
              "distance": 50
              }
    def construct(self):
        axes = ThreeDAxes()
        label_x = axes.get_x_axis_label("x")
        label_y = axes.get_y_axis_label("y")
        #self.add(axes, label_x, label_y)
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        n = 240
        slide_1 = VGroup()
        for i in range(n):
            d_cube = Cube(fill_color=LIGHT_BROWN).set_width(1).scale([1, 1 / n, 1]).set_opacity(1)
            d_cube.move_to([0, (-2 / n) * i, (2 / n) * i])
            slide_1.add(d_cube)
        slide_2 = slide_1.copy().rotate_about_origin(PI)
        slide = VGroup(slide_1,slide_2)
        slide.move_to([0,0,2])
        #self.add(axes,label_x,label_y)
        #self.begin_ambient_camera_rotation(rate=0.1)
        cube_m_1 = Cube(fill_color=LIGHT_BROWN).set_width(1).scale([1,1,4]).next_to(slide,UP,buff=0).align_to(slide[-1],np.array([0,0,1])).set_opacity(1)
        cube_m_2 = cube_m_1.copy().next_to(slide,DOWN,buff=0).align_to(slide[-1],np.array([0,0,1])).set_opacity(1)
        m = VGroup(slide,cube_m_1,cube_m_2)
        m.move_to(np.array([0,-3,0]))
        cube_l_1 = cube_m_1.copy().scale([1,2,1/4]).move_to([0,3.5,-1.5]).set_color(BLUE).set_opacity(1)
        cube_l_2 = cube_m_1.copy().move_to(np.array([0,2,0])).set_color(BLUE).set_opacity(1)
        self.play(FadeInFrom(cube_m_1,UP),FadeInFrom(cube_m_2,DOWN),FadeInFrom(slide,OUT),FadeInFrom(cube_l_1,LEFT),FadeInFrom(cube_l_2,RIGHT))
        self.wait()
        n = 60
        dt = 1 / n
        phi_0 = self.phi
        theta_0 = self.theta
        phi = 90*DEGREES
        theta = 0 * DEGREES
        delta_phi,delta_theta = (phi - phi_0)/n,(theta-theta_0)/n
        for i in range(n):
            phi_0 += delta_phi
            theta_0 += delta_theta
            self.set_camera_orientation(phi=phi_0,theta=theta_0)
            self.wait(dt)
        l = VGroup(cube_l_1,cube_l_2)
        self.wait()
        self.play(ApplyMethod(m.scale,0.5),
                  ApplyMethod(l.scale,0.5))
        self.play(ApplyMethod(m.move_to,np.array([0,-1,1.25])),
                  ApplyMethod(l.move_to,np.array([0,-1.75,-1.25])))
        text_m = Text("anim",font="DIN Alternate").set_color(BLACK).scale(2).rotate(PI/2).rotate(PI/2,axis=UP).move_to(np.array([0,1.75,1])).align_to(m[-1],IN)
        text_l = Text("aboratory",font="DIN Alternate").set_color(BLACK).scale(2).rotate(PI/2).rotate(PI/2,axis=UP).move_to(np.array([0,1.25,-1])).align_to(l,IN)
        self.play(FadeInFrom(text_m,DOWN),FadeInFrom(text_l,UP))

        #self.set_camera_orientation(phi=90*DEGREES,theta=0*DEGREES,distance=self.distance)
        self.wait(4)
        #self.stop_ambient_camera_rotation()
        #self.begin_ambient_camera_rotation(rate=1)
        #self.stop_ambient_camera_rotation()

class SlideCube(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": BLUE},
              "phi": 60 * DEGREES,
              "theta": 30 * DEGREES,
              "distance": 50
              }
    def construct(self):
        axes = ThreeDAxes()
        label_x = axes.get_x_axis_label("x")
        label_y = axes.get_y_axis_label("y")
        self.add(axes,label_x,label_y)
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        n = 60
        slide_1 = VGroup()
        for i in range(n):
            d_cube = Cube(fill_color=RED).scale([1,1/n,0.6])
            d_cube.move_to([0,(-2/n)*i,(2/n)*i])
            slide_1.add(d_cube)
        slide_2 = slide_1.copy().rotate_about_origin(PI)
        self.play(FadeIn(slide_1),FadeIn(slide_2))
        self.wait()
        self.wait(5)

class Text3D2(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES,theta=-45*DEGREES)
        text3d=TextMobject("This is a 3D text").scale(2).set_shade_in_3d(True)
        text3d.rotate(PI/2,axis=RIGHT)
        self.add(axes,text3d)

# To see the text in the traditional form:
class Text3D3(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES,theta=-45*DEGREES)
        text3d=TextMobject("This is a 3D text")

        self.add_fixed_in_frame_mobjects(text3d) #<----- Add this
        text3d.to_corner(UL)

        self.add(axes)
        self.begin_ambient_camera_rotation()
        self.play(Write(text3d))

        sphere = ParametricSurface(
            lambda u, v: np.array([
                1.5*np.cos(u)*np.cos(v),
                1.5*np.cos(u)*np.sin(v),
                1.5*np.sin(u)
            ]),v_min=0,v_max=TAU,u_min=-PI/2,u_max=PI/2,checkerboard_colors=[RED_D, RED_E],
            resolution=(15, 32)).scale(2)

        self.play(ShowCreation(sphere))
        self.wait(2)

class PrismTest(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": WHITE},
              "phi": 60 * DEGREES,
              "theta": 30 * DEGREES,
              "distance": 50
              }
    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        p = Prism()
        self.play(FadeIn(p))
        self.begin_ambient_camera_rotation(rate=3)
        self.wait(3)

class CurveTest(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 60 * DEGREES,
              "theta": 30 * DEGREES,
              "distance": 50
              }
    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        axes = ThreeDAxes(x_min=0,y_min=0,z_min=0)
        x_lab,y_lab,z_lab = axes.get_x_axis_label("x"),axes.get_y_axis_label("y"),axes.get_z_axis_label("z")
        self.add(axes,x_lab,y_lab,z_lab)
        par_suf_1 = ParametricSurface(lambda u,v: np.array([u,v,np.sin(2 * u)+np.cos(2 * v)]),v_min=0,u_min=0,v_max=PI*2,u_max=PI*2,checkerboard_colors=[RED_D, RED_E])
        all = Group(par_suf_1,axes)
        self.play(ShowCreation(par_suf_1))
        #phi_0, theta_0 = 0, 0
        #dt = 1 / 30
        #for i in range(240):
            #delta_phi = 240 * self.derivative_sigmoid(-6 + i * (12 / 240), dt) * dt * DEGREES
            #delta_theta = 480 * self.derivative_sigmoid(-6 + i * (12 / 240), dt) * dt * DEGREES
            #phi_0 += delta_phi
            #theta_0 += delta_theta
            #self.set_camera_orientation(phi=phi_0, theta=theta_0)
            #self.wait(dt)
        #self.move_camera(20*DEGREES,180*DEGREES,40,run_time=4)

class CubeRotateTest(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
        "phi": 60 * DEGREES,
        "theta": 30 * DEGREES,
        "distance": 100,
        "init_color":RED_A,
     }

    def construct(self):
        self.set_camera_orientation(phi=self.phi,theta=self.theta,distance=self.distance)
        cube_group = VGroup()
        cube_group_sub = VGroup()
        for i in range(10):
            color = interpolate_color(RED_A,RED_E,i/10)
            cube = Cube().set_color(color)
            cube.set_height(1.1**(-i))
            cube_group.add(cube)
        cube_group.arrange(RIGHT)
        cube_group.shift(DOWN * 4)
        for i in range(10):
            cube_group_sub_sub = VGroup()
            for j in range(9):
                color_sub = interpolate_color(cube_group[i].get_color(), PURPLE_E, j / 10)
                cube_sub = Cube().set_height(1.1 ** (- i - j - 1)).set_color(color_sub)
                cube_group_sub_sub.add(cube_sub)
            cube_group_sub_sub.arrange(UP)
            cube_group_sub_sub.next_to(cube_group[i],UP)
            cube_group_sub.add(cube_group_sub_sub)

        self.play(ShowSubmobjectsOneByOne(cube_group))
        self.play(ShowCreation(cube_group))
        factor = 1
        for i in cube_group_sub:
            self.play(ShowSubmobjectsOneByOne(i),run_time=1/factor)
            factor += 1
        self.wait()
        self.play(ShowCreation(cube_group_sub))
        picture = Group(*self.mobjects)
        self.play(ApplyMethod(picture.move_to,ORIGIN))
        self.move_camera(phi=30*DEGREES,theta=360*DEGREES,run_time=8)
        self.wait()


class ColoredSurface(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 60 * DEGREES,
              "theta": 30 * DEGREES,
              "distance": 100
              }
    def construct(self):
        self.set_camera_orientation(self.phi,self.theta,self.distance)
        R = lambda x,y:np.sqrt(x ** 2 + y ** 2) + 1e-8

        surface_origin = ParametricSurface(lambda u,v:np.array([u,v,8 * np.sin(R(u,v))/R(u,v) - 2]),
                                           u_min=-8,u_max=8,v_min=-8,v_max=8,resolution=(50,50)).scale(0.5)
        surface_frame = surface_origin.copy().set_fill(BLUE,opacity=0)

        r = np.linspace(1e-8,8 * np.sqrt(2),1000)
        z = (8 * np.sin(r)/r - 2)/2
        z_1 = max(z) - min(z)
        colors = color_gradient([BLUE_E,YELLOW,RED],100)
        colored_frame = surface_frame.copy()
        colored_surface = surface_origin.copy()
        for ff, fs in zip(colored_frame,colored_surface):
            f_z = ff.get_center()[-1]
            ff.set_color(colors[int((f_z-min(z))/z_1 * 90)])
            fs.set_color(colors[int((f_z-min(z))/z_1 * 90)])
        self.add(surface_origin)
        self.wait()
        self.play(ReplacementTransform(surface_origin,surface_frame),run_time=2)
        self.wait()
        self.play(ReplacementTransform(surface_frame,colored_frame),run_time=2)
        self.wait()
        self.play(ReplacementTransform(colored_frame,colored_surface),run_time=2)
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(5)

class ThreeDLine(ThreeDScene):
    def construct(self):
        l1 = ThreeDVector()