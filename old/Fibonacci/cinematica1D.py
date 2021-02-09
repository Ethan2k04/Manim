from manimlib.imports import *

VELOCITY_COLOR = GREEN
TIME_COLOR= YELLOW
DISTANCE_COLOR= BLUE

class Plot2(Scene):
    def construct(self):
        c1 = FunctionGraph(lambda x: 2*np.exp(-2*(x-1)**2))
        c2 = FunctionGraph(lambda x: x**2)
        axes1=Axes(y_min=-3,y_max=3)
        axes2=Axes(y_min=0,y_max=10)
        self.play(ShowCreation(axes1),ShowCreation(c1))
        self.wait()
        self.play(
            ReplacementTransform(axes1,axes2),
            ReplacementTransform(c1,c2)
        )
        self.wait()

class IncrementNumber(Succession):
    CONFIG = {
        "start_num" : 0,
        "changes_per_second" : 1,
        "run_time" : 11,
    }
    def __init__(self, num_mob, **kwargs):
        digest_config(self, kwargs)
        n_iterations = int(self.run_time * self.changes_per_second)
        new_num_mobs = [
            TexMobject(str(num)).move_to(num_mob, LEFT)
            for num in range(self.start_num, self.start_num+n_iterations)
        ]
        transforms = [
            Transform(
                num_mob, new_num_mob, 
                run_time = 1.0/self.changes_per_second,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )
            for new_num_mob in new_num_mobs
        ]
        Succession.__init__(
            self, *transforms, **{
                "rate_func" : None,
                "run_time" : self.run_time,
            }
        )

class IncrementTest(Scene):
    def construct(self):
        num = TexMobject("0")
        num.shift(UP)
        self.play(IncrementNumber(num))
        self.wait()

class movimiento1D(GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-10, 11, 1)),
        "x_axis_label" : "Posición $x$ (m)",
        "x_axis_width": 6,
        "y_min": 0,
        "y_max": 1,
        "y_axis_height": 0,
        "y_axis_label": "",
        "exclude_zero_label": False,
        "graph_origin": (0,0,0),
        "run_time_def": 10,
        "type": "horizontal",
        "title": "Movimiento en una dimensión",
        "show_title": True, 
    }
    def X(self, t):
        #ts=t*self.run_time_def
        ts=t*1.8
        return 5*(-2.0*ts**2+3.0*ts)
    
    def parametric_fnct_X(self,t):
        x=self.X(t)
        y=0
        if self.type == "horizontal":
            return self.coords_to_point(x,y)
        elif self.type == "vertical":
            return self.coords_to_point(y,x)
        else:
            raise Exception("type=%s. Movement type should be horizontal or vertical" % (self.type))

    def mostrar_titulo(self, color = RED, pos=ORIGIN + 2.5 * UP):
        titulo_mobj=TextMobject(self.title, color = color).shift(pos)
        self.play(Write(titulo_mobj))

    def construct(self):
        if self.show_title:
            self.mostrar_titulo()
        self.setup_axes()
        if self.type == "horizontal":
            self.remove(self.y_axis_label, self.y_axis)
        if self.type == "vertical":
            self.remove(self.x_axis_label, self.x_axis)
        dotX = Dot(self.parametric_fnct_X(0), color=BLUE, radius=0.2)
        pathX = ParametricFunction(self.parametric_fnct_X)
        self.play(ShowCreation(dotX))
        self.play(MoveAlongPath(dotX, pathX, rate_func=linear),
            run_time=self.run_time_def)
def Xcub(t):
    ts=(t-0.10)*5.5
    # ts=t*5
    return 2*(0.3*ts**3-2.0*ts**2+3.0*ts)

class movimiento1D_cubico(movimiento1D):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_labeled_nums" : list(range(-5, 6, 1)),
    }
    def X(self, t):
        return Xcub(t)

class movimiento1D_cubico_vert(movimiento1D):
    CONFIG = {
        "y_min": -5,
        "y_max": 5,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        "y_axis_height": 6,
        "x_min": 0,
        "x_max": 1,
        "x_axis_width": 0,
        "x_axis_label": "",
        "type": "vertical",
        "show_title": False,
    }
    def X(self, t):
        return Xcub(t)
    
def X_v_const(t):
    ts = t * 10
    return 0.8*ts-4.5

class movimiento1D_v_const(movimiento1D):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "title": "Movimiento con velocidad constante",
    }
    def X(self, t):
        return X_v_const(t)

class movimiento1D_v_const_vert(movimiento1D_v_const):
    CONFIG = {
        "y_min": -5,
        "y_max": 5,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        "y_axis_height": 6,
        "x_min": 0,
        "x_max": 1,
        "x_axis_width": 0,
        "x_axis_label": "",
        "type": "vertical",
        "show_title": False,
    }

def X_a_const(t):
    ts = t * 10
    return 0.14*ts**2-0.8*ts-1.0

class movimiento1D_a_const(movimiento1D):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "title": "Movimiento con aceleración constante",
    }
    def X(self, t):
        return X_a_const(t)

class movimiento1D_a_const_vert(movimiento1D_a_const):
    CONFIG = {
        "y_min": -5,
        "y_max": 5,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        "y_axis_height": 6,
        "x_min": 0,
        "x_max": 1,
        "x_axis_width": 0,
        "x_axis_label": "",
        "type": "vertical",
        "show_title": False,
    }


class point_and_shadow(Dot):
    CONFIG = {
        "fill_color": DISTANCE_COLOR,
        "fill_opacity": 0, 
        'radius': 0.2,
        }

    def __init__(self, point=ORIGIN, graph_scene=None, **kwargs):
        super().__init__(point=point, **kwargs)
        self.graph_scene=graph_scene

    def get_shadows(self):
        x,y = self.graph_scene.point_to_coords((self.get_x(), self.get_y(),0))
        x_0=self.graph_scene.coords_to_point(x,0)
        y_0=self.graph_scene.coords_to_point(0,y)
        x_y=self.graph_scene.coords_to_point(x,y)
        x_p =  Dot(x_0, name='x_shadow', color=DISTANCE_COLOR, radius=0.2) 
        y_p = Dot(y_0, name='y_shadow', color=DISTANCE_COLOR, radius=0.2)
        return (
                x_p,
                Line(x_0, x_y, name='x_line', color=GREY),
                y_p,
                Line(y_0,x_y,name='y_line', color=GREY),
                )
    
class XvsT(GraphScene):
    CONFIG = {
        "x_axis_label": "$t$",
        "x_min": 0,
        "x_max": 10,
        "y_axis_label": "$x$",
        'y_min': -10,
        'y_max': 10,
        "graph_origin": ORIGIN + 6 * LEFT,
        "exclude_zero_label": False,
        'show_objects_list': [
        #    'x_shadow', 
            'x_line',
        #    'x_vector',
            'y_shadow',
            'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'run_time': 10,
    }
    def X(self, t):
        # time scale reduced to [0,1]
        #ts=t*self.run_time_def
        ts=t*1.8
        return 5*(-2.0*ts**2+3.0*ts)

    def Xsc(self, t):
        # Position rescaled to run_time
        return self.X(t/self.run_time)
    
    def Vsc(self,t, dt=0.001):
        return (self.Xsc(t+dt)-self.Xsc(t))/dt

    def show_linea_tangente(self, t, dt=0.001, dt_left=-1.0, dt_right=1.0):
        v=self.Vsc(t, dt)
        punto_left = self.coords_to_point(t+dt_left,self.Xsc(t)+v*dt_left)
        punto_right = self.coords_to_point(t+dt_right,self.Xsc(t)+v*dt_right)
        linea = Line(punto_left, punto_right, color=VELOCITY_COLOR)
        self.play(ShowCreation(linea))


    def parametric_fnct(self,t):
        tsc=self.run_time*t
        x=self.X(t)
        return self.coords_to_point(tsc,x)

    def show_label_x0(self, t0=0, text='$x_0$', text_shift=RIGHT + 0.02 * DOWN):
        text_x0=TextMobject(text)
        label_coord = self.input_to_graph_point(t0, self.fun_graph)
        text_x0.next_to(label_coord, text_shift )
        line = Line(label_coord + 0.2 * LEFT, label_coord + 0.2 * RIGHT)
        self.play(Write(text_x0), ShowCreation(line))

    def show_ecuacion_mov(self,titulo='Movimiento con velocidad constante $v$', text='$x(t) = v t + x_0$'):
        titulo_mobj=TextMobject(titulo, color = RED).shift(ORIGIN + 2.5 * UP)
        ecuacion_mobj=TextMobject(text, color = DISTANCE_COLOR ).shift(ORIGIN + 1.9 * UP)
        self.play(Write(titulo_mobj))
        self.play(Write(ecuacion_mobj))

    def show_label_pendiente(self, text='pendiente $v$', t=4,
                            text_shift=2.4 * RIGHT + 0.7 * DOWN,
                            arrow_start=RIGHT + 0.8 * DOWN, arrow_end=0.1 * UP):
        label_coord = self.input_to_graph_point(t, self.fun_graph)
        text_mobj=TextMobject(text, color = VELOCITY_COLOR)
        text_mobj.shift(label_coord + text_shift)
        arrow = Arrow(label_coord + arrow_start, label_coord + arrow_end, color = VELOCITY_COLOR)
        self.play(Write(text_mobj), ShowCreation(arrow))

    def animate_graph(self):
        point = point_and_shadow(self.parametric_fnct(0),self)
        path = VMobject(color=DISTANCE_COLOR)
        path.set_points_as_corners([point.get_center(),point.get_center()+UP*0.001])
        shadows = point.get_shadows()
        for s in shadows:
            s.fade(darkness=1.0)
        group=VGroup(point, path, *shadows)
        r=get_norm(point.get_center())
        spiral=ParametricFunction(self.parametric_fnct)
        phi=ValueTracker(0)
        self.add(group)
        show_objects_list=self.show_objects_list
        def update_points(group):
            point, path, *shadows = group
            point.move_to(spiral.point_from_proportion(phi.get_value()))
            new_objects = point.get_shadows()
            for obj, new_obj in zip(shadows,new_objects): 
                if obj.name in show_objects_list:
                    obj.become(new_obj)
            new_path=path.copy()
            new_path.append_vectorized_mobject(Line(new_path.points[-1],point.get_center()))
            new_path.make_smooth()
            path.become(new_path)
        group.add_updater(update_points)
        self.play(phi.increment_value, 1, run_time=self.run_time , rate_func=linear)
        self.play(*[FadeOut(s) for s in shadows])
        self.wait(0.5)

    def construct(self):
        self.setup_axes()
        self.fun_graph=self.get_graph(self.Xsc)
        self.animate_graph()
        

class XvsT_cubico(XvsT):
    CONFIG = {
        "x_axis_label": "$t$",
        "x_min": 0,
        "x_max": 10,
        "x_labeled_nums" : list(range(1, 11)),
        "x_axis_label" : "Tiempo $t$ (s)",
        "y_axis_label": "$x$",
        'y_min': -5,
        'y_max': 5,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        "graph_origin": 5 * LEFT,
        'show_objects_list': [
        #    'x_shadow', 
            'x_line',
        #    'x_vector',
            'y_shadow',
            'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'run_time': 10,
    }
    def X(self, t):
        return Xcub(t)

class XvsT_v_const(XvsT):
    CONFIG = {
        "x_axis_label": "$t$",
        "x_min": 0,
        "x_max": 10,
        "x_labeled_nums" : list(range(1, 11)),
        "x_axis_label" : "Tiempo $t$ (s)",
        "y_axis_label": "$x$",
        'y_min': -5,
        'y_max': 5,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        "graph_origin": 5 * LEFT,
        'show_objects_list': [
        #    'x_shadow', 
            'x_line',
        #    'x_vector',
            'y_shadow',
            'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'run_time': 10,
    }
    def X(self, t):
        return X_v_const(t)
    
    def construct(self):
        super().construct()
        self.show_ecuacion_mov()
        self.show_label_x0()
        self.show_label_pendiente()
        




class XvsT_a_const(XvsT):
    CONFIG = {
        "x_axis_label": "$t$",
        "x_min": 0,
        "x_max": 10,
        "x_labeled_nums" : list(range(1, 11)),
        "x_axis_label" : "Tiempo $t$ (s)",
        "y_axis_label": "$x$",
        'y_min': -5,
        'y_max': 5,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        "graph_origin": 5 * LEFT,
        'show_objects_list': [
        #    'x_shadow', 
            'x_line',
        #    'x_vector',
            'y_shadow',
            'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'run_time': 10,
    }
    def X(self, t):
        return X_a_const(t)
    
    def construct(self):
        super().construct()
        self.show_ecuacion_mov(titulo='Movimiento con aceleración constante $a$',
                                text='$x(t)=\\frac{1}{2} a t^2 + v_0 t + x_0$')
        self.fun_graph=self.get_graph(lambda t: self.X(t/10.0))
        self.show_label_x0(text_shift=1.01 * RIGHT+ 0.0 * UP)
        self.show_linea_tangente(t=0, dt_left=-0.5, dt_right=3.0)
        self.show_label_pendiente(text='pendiente inicial $v_0$', t=0, 
                                  text_shift = 3 * RIGHT + 2 * DOWN,
                                  arrow_start = 1.0 * RIGHT + 2.0 * DOWN,
                                  arrow_end = 0.0 * DOWN)
        

        


class SecantLineToTangentLine(GraphScene):
    CONFIG = {
        "x_min" : 0,
        "x_max" : 10,
        "x_labeled_nums" : list(range(1, 11)),
        "x_axis_label" : "Tiempo $t$ (s)",
        # "y_min" : -10,
        # "y_max" : 110,
        # "y_tick_frequency" : 10,
        # "y_labeled_nums" : list(range(10, 110, 10)),
        "y_min" : -5,
        "y_max" : 5,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Posición $x$ (m)",
        #"x_axis_width": 0.8*FRAME_WIDTH,
        #"y_axis_height": 0.8*FRAME_HEIGHT,
        # "graph_origin" : 2.5*DOWN + 5*LEFT,
        "graph_origin" : 5*LEFT,
        "default_graph_colors" : [DISTANCE_COLOR, VELOCITY_COLOR],
        "default_derivative_color" : VELOCITY_COLOR,
        "time_of_journey" : 10,
        "care_movement_rate_func" : smooth,
        # "start_time" : 6,
        "start_time" : 1.4,
        # "end_time" : 2,
        "end_time" : 8,
        "alt_end_time" : 10,
        "start_dt" : 1.5,
        "end_dt" : 0.01,
        "secant_line_length" : 10,

    }
    def construct(self):
        self.setup_axes(animate = False)
        # self.remove(self.y_axis_label_mob, self.x_axis_label_mob)
        self.add_graph()
        self.draw_axes()
        self.show_tangent_line()
        

    def get_ds_dt_group(self, dt, animate = False):
        points = [
            self.input_to_graph_point(time, self.graph)
            for time in (self.curr_time, self.curr_time+dt)
        ]
        dots = list(map(Dot, points))
        for dot in dots:
            dot.scale_in_place(0.5)
        secant_line = Line(*points)
        secant_line.set_color(VELOCITY_COLOR)
        secant_line.scale_in_place(
            self.secant_line_length/secant_line.get_length()
        )

        interim_point = points[1][0]*RIGHT + points[0][1]*UP
        dt_line = Line(points[0], interim_point, color = TIME_COLOR)
        ds_line = Line(interim_point, points[1], color = DISTANCE_COLOR)
        dt = TexMobject("dt")
        dt.set_color(TIME_COLOR)
        if dt.get_width() > dt_line.get_width():
            dt.scale(
                dt_line.get_width()/dt.get_width(),
                about_point = dt.get_top()
            )
        dt.next_to(dt_line, DOWN, buff = SMALL_BUFF)
        ds = TexMobject("dx")
        ds.set_color(DISTANCE_COLOR)
        if ds.get_height() > ds_line.get_height():
            ds.scale(
                ds_line.get_height()/ds.get_height(),
                about_point = ds.get_left()
            )
        ds.next_to(ds_line, RIGHT, buff = SMALL_BUFF)

        group = VGroup(
            secant_line, 
            ds_line, dt_line,
            ds, dt,
            *dots
        )
        if animate:
            self.play(
                ShowCreation(dt_line),
                Write(dt),
                ShowCreation(dots[0]),                
            )
            self.play(
                ShowCreation(ds_line),
                Write(ds),
                ShowCreation(dots[1]),                
            )
            self.play(
                ShowCreation(secant_line),
                Animation(VGroup(*dots))
            )
        return group

    def add_graph(self):
        def double_smooth_graph_function(t):
            if t < 5:
                return 50*smooth(t/5.)
            else:
                return 50*(1+smooth((t-5)/5.))
        # self.graph = self.get_graph(double_smooth_graph_function)
        self.graph = self.get_graph(lambda t: Xcub(t/10.0))
        self.graph_label = self.get_graph_label(
            self.graph, "x(t)", 
            x_val = self.x_max, 
            direction = DOWN+RIGHT, 
            buff = SMALL_BUFF,
        )

    def draw_axes(self):
        # self.x_axis.remove(self.x_axis_label_mob)
        # self.y_axis.remove(self.y_axis_label_mob)
        self.play(Write(
            VGroup(
                self.x_axis, self.y_axis,
                self.graph, self.graph_label
            ),
            run_time = 4
        ))
        self.wait()

    def show_tangent_line(self):
        self.curr_time = self.start_time

        ds_dt_group = self.get_ds_dt_group(self.start_dt, animate = True)
        self.wait()
        def update_ds_dt_group(ds_dt_group, alpha):
            new_dt = interpolate(self.start_dt, self.end_dt, alpha)
            new_group = self.get_ds_dt_group(new_dt)
            # Transform(ds_dt_group, new_group).update(1)
            ds_dt_group.become(new_group)
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_ds_dt_group),
            run_time = 15
        )
        self.wait()
        def update_as_tangent_line(ds_dt_group, alpha):
            self.curr_time = interpolate(self.start_time, self.end_time, alpha)
            new_group = self.get_ds_dt_group(self.end_dt)
            # Transform(ds_dt_group, new_group).update(1)
            ds_dt_group.become(new_group)
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_as_tangent_line),
            run_time = 8,
            rate_func = there_and_back
        )
        self.wait()
        
        self.play(
            UpdateFromAlphaFunc(ds_dt_group, update_ds_dt_group),
            run_time = 8,
            rate_func = lambda t : 1-there_and_back(t)
        )
        self.wait()

        v_line = self.get_vertical_line_to_graph(
            self.curr_time,
            self.graph,
            line_class = Line,
            line_kwargs = {
                "color" : MAROON_B,
                "stroke_width" : 3
            }
        )
        def v_line_update(v_line):
            v_line.put_start_and_end_on(
                self.coords_to_point(self.curr_time, 0),
                self.input_to_graph_point(self.curr_time, self.graph),
            )
            return v_line
        self.play(ShowCreation(v_line))
        self.wait()

        original_end_time = self.end_time
        for end_time in self.alt_end_time, original_end_time, self.start_time:
            self.end_time = end_time
            self.play(
                UpdateFromAlphaFunc(ds_dt_group, update_as_tangent_line),
                UpdateFromFunc(v_line, v_line_update),
                run_time = abs(self.curr_time-self.end_time),
            )
            self.start_time = end_time
        self.play(FadeOut(v_line))

    