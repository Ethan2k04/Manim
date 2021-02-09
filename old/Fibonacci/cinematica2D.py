from manimlib.imports import *
from scipy.misc import derivative

VELOCITY_COLOR = GREEN
TIME_COLOR= YELLOW
DISTANCE_COLOR= BLUE
ACCELERATION_COLOR = RED
TITLE_COLOR = RED



class movimiento2D(GraphScene):
    """
    Anima un movimiento en 2D, mostrando vectores velocidad (show_velocity=True)
    y aceleración (show_acceleration=True)
    """
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "x_axis_label" : "$x$ (m)",
        "x_axis_width": 6,
        "y_min": -5,
        "y_max": 5,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "$y$ (m)",
        "exclude_zero_label": True,
        "y_axis_height": 6,
        "graph_origin": (0,0,0),
        "title": "Movimiento en dos dimensiones",
        "title_position": ORIGIN + 3.725 * UP,
        "title_color": TITLE_COLOR,
        "show_title": True, 
        "show_x_axis": True,
        "show_y_axis": True,
        "show_path": True,
        "show_velocity": True,
        "show_acceleration": True,
        "show_a_centripetal": False,
        "show_a_tangential": False,
        "show_tangent_perp_lines": False,
        "show_tangent_circle": False,
        "vel_scale": 0.2,
        "acc_scale": 0.2,
        "vel_label": "$\\vec{v}$",
        "acc_label": "$\\vec{a}$",
        "label_text_ac": "$\\vec{a}_c$", 
        "label_text_at": "$\\vec{a}_t$", 
        "vel_label_dir": RIGHT,
        "acc_label_dir": LEFT+DOWN,
        "label_dir_ac": 1.5 * DOWN + RIGHT,
        "label_dir_at": 1.0 * UP + 2.0 * RIGHT,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_from": 'pos',
        "label_from_ac": 'pos',
        "label_from_at": 'pos',
        "initial_time": 0.0,
        "run_time": 2.2,
    }
    def X(self, t):
        vx0=5.0
        x0=-5
        x=vx0*t+x0
        return x
    def Y(self,t):
        a=-9.8
        vy0=10.0
        y0=0.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y
    def position(self,t):
        """Position at time t in Scene units

        Args:
            t (float): time

        Returns:
            np.array: position in Scene coordinates
        """
        x=self.X(t)
        y=self.Y(t)
        return self.coords_to_point(x,y)

    def velocity(self,t):
        """Velocity at time t in Scene coordinates

        Args:
            t (float): time

        Returns:
            np.array: Velocity components in Scene coordinates
        """
        vx=derivative(self.X,t,dx=0.001)
        vy=derivative(self.Y,t,dx=0.001)
        # must substract the position on Scene of the origin, because
        # coords_to_point added it.
        return self.coords_to_point(vx,vy) - self.coords_to_point(0,0)

    def acceleration(self,t):
        """Acceleration at time t in Scene coordinates

        Args:
            t (float): time

        Returns:
            np.array: Acceleration cartesian coordiantes in Scene coordiantes
        """
        ax=derivative(self.X,t,dx=0.001,n=2)
        ay=derivative(self.Y,t,dx=0.001,n=2)
        return self.coords_to_point(ax,ay) - self.coords_to_point(0,0)

    def mostrar_titulo(self, color = None, pos = None):
        if color == None:
            color = self.title_color
        if pos == None:
            pos = self.title_position
        titulo_mobj=TextMobject(self.title, color = color).shift(pos)
        self.play(Write(titulo_mobj))
    
    def cinematic_vector(self, t, f=None, color=VELOCITY_COLOR, pos = None, scale=1.0, label_text = None, direction = None, label_from = None):
        """
        Creates velocity or acceleration vector

        Args:
            t (float): current time
            f (function, optional): function to create the vector: velocity or acceleration. Defaults to velocity.
            color (int, optional): color for the vector. Defaults to VELOCITY_COLOR.
            pos (ndarray, optional): position to place the vector. Defaults to self.position(t).
            scale (float): scale for the vector. Default 1.0.
            label_text (str or None): label for the vector. Default None.
            direction (ndarray): direction for the label. Default self.vec_label_dir.
            label_from (str): base position for the label: 'pos' from the position of the particle, 'vel' from the vector

        Returns:
            Vector or VGroup(Vector, TextMobject(label_text))
        """
        if f == None:
            f=self.velocity
        if pos == None:
            pos = self.position(t)
        if type(direction) == type(None):
            direction = self.vel_label_dir
        if type(label_from) == type(None):
            label_from = self.vel_label_from
        vec = Vector(scale*f(t), color = color)
        vec = vec.shift(pos)
        if label_text != None:
            text=TextMobject(label_text, color = color)
            if label_from == 'pos':
                text.next_to(pos, direction = direction)
            elif label_from == 'vec':
                text.next_to(vec, direction = direction)
            else:
                raise Exception('label_from = "%s" should be "pos" or "vec"' % (label_from))
            vec= VGroup(vec,text)
        return vec

    def position_vec(self, t):
        """Position vector in Graph units

        Args:
            t (float): time

        Returns:
            np.array([x,y]): Position in Graph units
        """
        x=self.X(t)
        y=self.Y(t)
        return np.array([x,y])

    def velocity_vec(self,t):
        """Velocity at time t in Graph units

        Args:
            t (float): time

        Returns:
            np.array: Cartesian components of velocity in Graph units
        """
        vx=derivative(self.X,t,dx=0.001)
        vy=derivative(self.Y,t,dx=0.001)
        return np.array([vx,vy])

    def acceleration_vec(self,t):
        """Acceleration at time t in Graph units

        Args:
            t (float): time

        Returns:
            nd.array: Cartesian components of acceleration in Graph units
        """
        ax=derivative(self.X,t,dx=0.001,n=2)
        ay=derivative(self.Y,t,dx=0.001,n=2)
        return np.array([ax, ay])

    def tangent_vec(self,t):
        vx=derivative(self.X,t,dx=0.001)
        vy=derivative(self.Y,t,dx=0.001)
        norm = np.sqrt(vx**2 + vy**2)
        ux = vx / norm
        uy = vy / norm
        return np.array([ux, uy])

    def tangent_unit_vec(self,t, color = GREY):
        [ux, uy] = self.tangent_vec(t)
        return self.coords_to_point(ux, uy) - self.coords_to_point(0,0)

    def perp_vec(self,t):
        [ux, uy] = self.tangent_vec(t)
        perp_vec = np.array([uy, -ux])
        if np.dot(perp_vec, self.acceleration_vec(t)) < 0:
            perp_vec = - perp_vec
        return perp_vec

    def perp_unit_vec(self,t):
        [ux, uy] = self.perp_vec(t)
        return self.coords_to_point(ux, uy) - self.coords_to_point(0,0)

    def acc_components(self, t):
        """Gives the centripetal and tangential components of the acceleration in Graph units

        Args:
            t (float): time

        Returns: (np.array[ax_cen, ay_cen], np.array[ax_tan, ay_tan])
        """
        a = self.acceleration_vec(t)
        t_vec = np.array(self.tangent_vec(t))
        c_vec = np.array(self.perp_vec(t))
        a_t = np.dot(a,t_vec) * t_vec
        a_c = np.dot(a,c_vec) * c_vec
        return (a_c, a_t)

    def acc_component_vecs(
        self, t, 
        label_text_ac = None,
        label_dir_ac = None, 
        label_from_ac = None, 
        label_text_at= None, 
        label_dir_at = None, 
        label_from_at = None, 
        color = ACCELERATION_COLOR):
        """Creates the vector components of the acceleration (centripetal, tangential)

        Args:
            t (float): time
            label_text_ac (str, optional): label for centripetal acceleration. Defaults to "$\vec{a}_c$".
            label_dir_ac (optional): offset for the a_c label. Defaults to 1.5*DOWN.
            label_text_at (str, optional): label for the tangential acceleration. Defaults to "$\vec{a}_t$".
            label_dir_at (optional): offset for the a_t label. Defaults to 4.0*UP+2.0*RIGHT.
            color (optional): color for the vectors and label. Defaults to ACCELERATION_COLOR.

        Returns:
            list: [VGroup(a_centripetal, label), VGroup(a_tangential, label)]
        """
        if label_text_ac == None:
            label_text_ac = self.label_text_ac
        if label_text_at == None:
            label_text_at = self.label_text_at
        if label_dir_ac == None:
            label_dir_ac = self.label_dir_ac
        if label_dir_at == None:
            label_dir_at = self.label_dir_at
        if label_from_ac == None:
            label_from_ac = self.label_from_ac
        if label_from_at == None:
            label_from_at = self.label_from_at

        (a_c, a_t) = self.acc_components(t)
        pos = self.position(t)
        a_c_vec = Vector(
            self.acc_scale*(self.coords_to_point(a_c[0],a_c[1]) - self.coords_to_point(0,0)),
             color = color
            )
        a_c_vec.shift(pos)
        a_t_vec = Vector(
            self.acc_scale*(self.coords_to_point(a_t[0],a_t[1]) - self.coords_to_point(0,0)),
            color = color
            )
        a_t_vec.shift(pos)
        components_list = []
        for vec, label_text, direction, label_from in [
            (a_c_vec, label_text_ac, label_dir_ac, label_from_ac), 
            (a_t_vec, label_text_at, label_dir_at, label_from_at)]:
            if label_text != None:
                text=TextMobject(label_text, color = color)
                if label_from == 'pos':
                    text.next_to(pos, direction = direction)
                if label_from == 'vec':
                    text.next_to(vec, direction = direction)
                vec = VGroup(vec,text)
                components_list.append(vec)
        return components_list

    def get_tangent_circle_center_and_radius_in_graph(self, t):
        """Gets the center of the tangent circle position in Graph units."""
        perp_vec = self.perp_vec(t)
        v2 = np.linalg.norm(self.velocity_vec(t))**2
        [ac, at] = self.acc_components(t)
        ac_norm = np.linalg.norm(ac)
        r = v2 / ac_norm
        center_pos = self.position_vec(t) + r * perp_vec
        return (center_pos, r)

    def get_tangent_circle_center_and_radius_in_scene(self, t):
        """Gets the center of the tangent circle position in Scene units."""
        ([cx, cy], r) = self.get_tangent_circle_center_and_radius_in_graph(t)
        center_pos_in_scene = self.coords_to_point(cx, cy)
        r_in_scene = (self.coords_to_point(r,0)-self.coords_to_point(0,0))[0]
        return (center_pos_in_scene, r_in_scene)

    def tangent_circle(self, t, color = GREY):
        """Constructs the tangent circle to trayectory."""
        # get center and radius in Scene
        (center_pos_in_scene, r_in_scene) = self.get_tangent_circle_center_and_radius_in_scene(t)
        tang_circle = Circle(radius = r_in_scene, color = color).shift(center_pos_in_scene)
        return tang_circle, center_pos_in_scene, r_in_scene
    
    def animate_tangent_circle(self, t, color = GREY):
        """Shows the tangent circle at time t.

        Args:
            t (time): time
        """
        tang_circle, center_pos_in_scene, r_in_scene = self.tangent_circle(t, color = color)
        self.play(ShowCreation(tang_circle))
        return tang_circle, center_pos_in_scene, r_in_scene

    def tangent_perp_lines(self, t, r = None, color = GREY):
        if r == None:
            (center_pos_in_scene, r) = self.get_tangent_circle_center_and_radius_in_scene(t)
        tg = self.tangent_unit_vec(t)
        perp = self.perp_unit_vec(t)
        pos = self.position(t)
        tangent_line = Line(pos - 5.0 * tg, pos + 5.0 * tg , color = color)
        perp_line = Line( pos , center_pos_in_scene, color = color )
        return tangent_line, perp_line

    def animate_tangent_perp_lines(self, t):
        tangent_line, perp_line = self.tangent_perp_lines(t)
        self.play(
            ShowCreation(tangent_line),
            ShowCreation(perp_line)
            )
        return (tangent_line, perp_line)

    def animate_acc_components(self,t):
        """Animation showing the centripetal and tangential components of acceleration."""
        [a_c_vec, a_t_vec] = self.acc_component_vecs(t)
        self.play(
            ShowCreation(a_c_vec),
            ShowCreation(a_t_vec)
            )
        return [a_c_vec, a_t_vec]

    def animate_graph(self):
        point = Dot(self.position(self.initial_time), color = DISTANCE_COLOR, radius=0.2)
        group = VGroup(point)
        if self.show_path:
            path = VMobject(color=DISTANCE_COLOR)
            path.set_points_as_corners([point.get_center(),point.get_center()+UP*0.001])
            group.add(path)
        if self.show_velocity:
            velocity_vector = self.cinematic_vector(self.initial_time, scale=self.vel_scale, label_text=self.vel_label, label_from=self.vel_label_from)
            group.add(velocity_vector)
        if self.show_acceleration:
            acceleration_vector = self.cinematic_vector(
                self.initial_time, 
                f=self.acceleration,color = ACCELERATION_COLOR, 
                scale=self.acc_scale, 
                direction = self.acc_label_dir,
                label_from = self.acc_label_from)
            group.add(acceleration_vector)
        if self.show_a_centripetal or self.show_a_tangential:
            (a_c, a_t ) = self.acc_component_vecs(self.initial_time)
            if self.show_a_centripetal:
                group.add(a_c)
            if self.show_a_tangential:
                group.add(a_t)
        if self.show_tangent_perp_lines:
            tan_line, perp_line = self.tangent_perp_lines(self.initial_time)
            group.add(tan_line, perp_line)
        if self.show_tangent_circle:
            tan_circle, *rest = self.tangent_circle(self.initial_time) 
            group.add(tan_circle)
        current_time=ValueTracker(self.initial_time)
        self.add(group)
        def update_points(group):
            t = current_time.get_value()
            pos = self.position(t)
            # Unpack the group
            # point, path, velocity_vector, acceleration_vector = group
            point, *r = group
            point.move_to(pos)
            if self.show_path:
                path, *r = r
                new_path=path.copy()
                new_path.append_vectorized_mobject(Line(new_path.points[-1],point.get_center()))
                new_path.make_smooth()
                path.become(new_path)
            if self.show_velocity:
                velocity_vector, *r = r 
                velocity_vector.become(self.cinematic_vector(t, scale=self.vel_scale, label_text=self.vel_label, label_from=self.vel_label_from))
            if self.show_acceleration:
                acceleration_vector, *r = r
                acceleration_vector.become(self.cinematic_vector(t,f=self.acceleration,color = ACCELERATION_COLOR,
                                                                scale=self.acc_scale,  label_text=self.acc_label,
                                                                direction = self.acc_label_dir,label_from=self.acc_label_from ))
            if self.show_a_centripetal or self.show_a_tangential:
                a_c_new, a_t_new = self.acc_component_vecs(t)
                if self.show_a_centripetal:
                    a_c, *r = r
                    a_c.become(a_c_new)
                if self.show_a_tangential:
                    a_t, *r = r
                    a_t.become(a_t_new)
            if self.show_tangent_perp_lines:
                tan_line_new, perp_line_new = self.tangent_perp_lines(t)
                tan_line, perp_line, *r = r
                tan_line.become(tan_line_new)
                perp_line.become(perp_line_new)
            if self.show_tangent_circle:
                tan_circle_new, *rest = self.tangent_circle(t)
                tan_circle, *r = r
                tan_circle.become(tan_circle_new)

        group.add_updater(update_points)
        self.play(current_time.set_value, self.initial_time + self.run_time, run_time=self.run_time, rate_func=linear)
        return group

    def run_trayectory_up_to_time(self, t):
        """Runs the trayectory up to time t and pauses there."""
        original_run_time = self.run_time
        original_initial_time = self.initial_time
        self.run_time = t - self.initial_time
        group = self.animate_graph()
        self.run_time = original_run_time 
        self.initial_time = original_initial_time
        return group
    
    def continue_trayectory_from(self, t):
        """Continues to run the trayectory from time t to the end."""
        original_run_time = self.run_time
        original_initial_time = self.initial_time
        self.initial_time = t
        self.run_time = self.run_time - t
        group = self.animate_graph()
        self.run_time = original_run_time 
        self.initial_time = original_initial_time
        return group

    def run_trayectory_from_to(self, t1, t2):
        """Runs the trayectory from time t1 to time t2

        Args:
            t1 (float): initial time
            t2 (float): end time
        
        Returns:
            VGroup(point, [path, velocity, acceleration, ...]) of final
            time t2
        """
        original_run_time = self.run_time
        original_initial_time = self.initial_time
        self.initial_time = t1
        self.run_time = t2 - t1
        group = self.animate_graph()
        self.run_time = original_run_time 
        self.initial_time = original_initial_time
        return group

    def initialize_scene(self):
        if self.show_title:
            self.mostrar_titulo()
        self.setup_axes()
        if not self.show_x_axis:
            self.remove(self.x_axis_label, self.x_axis)
        if not self.show_y_axis:
            self.remove(self.y_axis_label, self.y_axis)

    def construct(self):
        self.initialize_scene()
        self.animate_graph()
        self.wait()
       

class movimiento1D(movimiento2D):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "x_axis_label" : "$x$ (m)",
        "x_axis_width": 9,
        "y_min": -5,
        "y_max": 5,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "$y$ (m)",
        "exclude_zero_label": False,
        "graph_origin": (0,0,0),
        "title": "Movimiento en una dimensión",
        "title_position": ORIGIN + 2.5 * UP,
        "show_title": True, 
        "show_x_axis": True,
        "show_y_axis": False,
        "show_path": True,
        "show_velocity": True,
        "show_acceleration": True,
        "vel_scale": 1.0,
        "acc_scale": 1.0,
        "vel_label": "$\\vec{v}$",
        "acc_label": "$\\vec{a}$",
        "vel_label_dir": 1.5 * UP,
        "acc_label_dir": 2.5 * DOWN,
    }
    def Y(self,t):
        return 0.0
    
class mov_1D_cub(movimiento1D):
    CONFIG = {
        "initial_time": -1.0,
        "run_time": 10.0,
    }
    def X(self,t):
        ts=t*0.55
        return 2*(0.3*ts**3-2.0*ts**2+3.0*ts)
class mov_1D_cub_notraces(mov_1D_cub):
    CONFIG = {
        "show_path": False,
        "show_velocity": False,
        "show_acceleration": False,
    }

class mov_1D_v_const(movimiento1D):
    CONFIG = {
        "title": "Movimiento con velocidad constante",
        "show_path": False,
        "show_acceleration": False,
        "initial_time": 0.0,
        "run_time": 10.0,
        "vel_scale": 2.0,
        "vel_label_dir": UP + RIGHT,
    }
    def X(self,t):
        return 0.8*t-4.5

class mov_1D_a_const(movimiento1D):
    CONFIG = {
        "title": "Movimiento con aceleración constante",
        "show_path": False,
        "acc_scale": 4.0,
        "initial_time": 0.0,
        "run_time": 10.0,
    }
    def X(self,t):
        return 0.14*t**2-0.8*t-1.0

class mov_caida_libre(movimiento2D):
    CONFIG = {
        "title": "Movimiento de caida libre",
        "exclude_zero_label": False,
        "acc_label": "$\\vec{a}=\\vec{g}$",
        "show_path": False,
        "show_x_axis": False,
        "vel_label_dir": 1.5 * RIGHT,
        "acc_label_dir": 2.0 * LEFT + DOWN,
        "initial_time": 0.0,
        "run_time":  2.3,
        "vel_scale": 0.2,
        "acc_scale": 0.2,
    }
    def X(self,t):
        return 0.0
    def Y(self,t):
        a=-9.8
        vy0=10.0
        y0=0.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y

class mov_caida_libre_slow_mo(mov_caida_libre):
    CONFIG = {
        "run_time":  23.0,
        "vel_scale": 0.2*10.0,
        "acc_scale": 0.2*100.0,
    }
    def Y(self,t):
        a=-9.8
        vy0=10.0
        y0=0.0
        t=t/10.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y


class mov_circulos_alternos(movimiento2D):
    CONFIG = {
        "run_time" : 10.0,
        "omega": 1.0,
        "amp_x": 3.5,
        "amp_y": 3.5,
        "vel_scale": 0.5,
        "acc_scale": 0.5,
        # "show_velocity": True,
        # "show_acceleration": True,
        # "show_a_centripetal": True,
        # "show_a_tangential": True,
        # "show_tangent_perp_lines": True,
        # "show_tangent_circle": True,
    }
    def X(self, t):
        x0 = - self.amp_x/2
        if t < PI/self.omega:
            x = x0 - self.amp_x * np.cos(self.omega*t)
        else:
            x =  x0 + 2 * self.amp_x - self.amp_x * np.cos(self.omega*t-PI)
        return x
    def Y(self,t):
        y= self.amp_y*np.sin(self.omega*t)
        return y

class mov_circular_uniforme(movimiento2D):
    """Anima un movimiento circular uniforme con velocidad angular omega."""
    CONFIG = {
        'amplitud': 5.0,
        'omega': 2.0,
        'vueltas': 2.0,
        'phi': 0.0,
        'run_time': None,
        'title': 'Movimiento circular uniforme',
    }

    def construct(self):
        if self.run_time == None:
            """Determina run_time con el numero de vueltas"""
            self.run_time = self.vueltas * TAU / self.omega
        return super().construct()

    def theta(self, t):
        return self.omega*t + self.phi

    def X(self,t):
        return self.amplitud * np.cos(self.theta(t))

    def Y(self,t):
        return self.amplitud * np.sin(self.theta(t))

class mov_circular_uniforme_all_cinematics(mov_circular_uniforme):
    """
    Anima un movimiento circular uniforme con velocidad angular omega.
    Muestra el circulo tangente.
    """
    CONFIG = {
        'amplitud': 5.0,
        'omega': 2.0,
        'vueltas': 2.0,
        'phi': 0.0,
        'run_time': None,
        'title': 'Movimiento circular uniforme',
        "show_velocity": True,
        "show_acceleration": True,
        "show_a_centripetal": False,
        "show_a_tangential": False,
        "show_tangent_perp_lines": True,
        "show_tangent_circle": True,
    }

class mov_circular_no_uniforme(mov_circular_uniforme):
    """Anima un movimiento circular no uniforme, con aceleración angular alpha constante"""
    CONFIG = {
        'amplitud': 5.0,
        'alpha': 0.5,
        'omega': 0.0,
        'phi': 0.0,
        'run_time': 6.0,
        'title': 'Movimiento circular no uniforme'
    }

    def theta(self, t):
        return (self.alpha/2.0) * t**2 + self.omega*t + self.phi

class mov_curvo_acel(mov_circular_no_uniforme):
    CONFIG = {
        'amplitud': 5.0,
        'alpha': -0.035,   #   -0.035
        'omega': -0.35,     #   -0.4
        'phi': PI,
        'run_time': 5.0,
        'time_rescale': 0.7,
        "vel_scale": 1.0,
        "acc_scale": 3.0,
        "vel_label_dir": 2 * UP +  LEFT,
        "acc_label_dir": 8.0 * RIGHT,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_from": 'pos',
        "label_from_ac": 'pos',
        "label_from_at": 'pos',
        'title': '',
        'show_title': False,
        "show_x_axis": False,
        "show_y_axis": False,
        "show_path": True,
        "show_velocity": True,
        "show_acceleration": False,
        "show_a_centripetal": False,
        "show_a_tangential": False,
        "show_tangent_perp_lines": False,
        "show_tangent_circle": False,
        "t": 2.0,  # t =1.5, 2.0 tiempo para mostrar la animación
    }
    def X(self,t):
        xfactor = 2.4
        x0 = 4.0
        return x0 + xfactor * self.amplitud * np.cos(self.theta(self.time_rescale*t))
    def Y(self,t):
        y0 = - 1.5
        return y0 + self.amplitud * np.sin(self.theta(self.time_rescale*t))
        
class mov_curvo_acel_show_a(mov_curvo_acel):
    CONFIG = {
        "show_acceleration": True,
        "acc_label_dir": DOWN + LEFT,
    }

class mov_curvo_acel_show_all_cinematics(mov_curvo_acel):
    CONFIG = {
        "vel_label_dir": UP,
        "acc_label_dir": DOWN + RIGHT,
        "label_dir_ac": DOWN,
        "label_dir_at": RIGHT,
        "show_velocity": True,
        "show_acceleration": True,
        "show_a_centripetal": True,
        "show_a_tangential": True,
        "show_tangent_perp_lines": True,
        "show_tangent_circle": True,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_from": 'vec',
        "label_from_ac": 'vec',
        "label_from_at": 'vec',
    }

class mov_curvo_acel_mas_largo(mov_curvo_acel):
    CONFIG = {
        'run_time': 20.0,  # 30.0,
        'time_rescale': 1.0,
        "show_velocity": True,
        "show_acceleration": False,
        "vel_label_dir": 2 * UP +  LEFT,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
    }
    def X(self,t):
        xfactor = 1.2
        x0 = 0.0
        return x0 + xfactor * self.amplitud * np.cos(self.theta(self.time_rescale*t))
    def Y(self,t):
        y0 =  0.0
        #if t >= 5.0:
        t = 5.0 * np.sqrt(t/5.0)
        return y0 + self.amplitud * np.sin(self.theta(self.time_rescale*t))
        
class mov_curvo_acel_mas_largo_v_y_a(mov_curvo_acel_mas_largo):
    CONFIG = {
        'run_time': 20.0,  # 30.0,
        'time_rescale': 1.0,
        "show_velocity": True,
        "show_acceleration": True,
        "vel_label_dir": 2 * UP +  LEFT,
        "acc_label_dir": UP,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_from": 'vec',
    }
class mov_curvo_acel_mas_largo_show_all_cinematics(mov_curvo_acel_mas_largo):
    CONFIG ={
        "vel_label_dir": ORIGIN,
        "acc_label_dir": ORIGIN,
        "label_dir_ac": ORIGIN,
        "label_dir_at": ORIGIN,
        "show_velocity": True,
        "show_acceleration": True,
        "show_a_centripetal": True,
        "show_a_tangential": True,
        "show_tangent_perp_lines": True,
        "show_tangent_circle": True,
        "vel_label_from": 'vec',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_from": 'vec',
        "label_from_ac": 'vec',
        "label_from_at": 'vec',
    }

class mov_curvo_acel_construction(mov_curvo_acel):
    """ Escena que muestra la construcción gráfica de la aceleración promedio."""
    CONFIG = {
        "dt": 1.0,
        "show_velocity": True,
        "show_acceleration": False,
        "show_a_centripetal": False,
        "show_a_tangential": False,
        "show_path": True,
        "title": "Construcción gráfica de la aceleración promedio",
        "show_title": True,
        "vel_label_from": 'pos',
    }
    def dv(self, t, dt = None):
        if dt == None:
            dt = self.dt
        return self.velocity(t+dt) - self.velocity(t)

    def animate_acceleration_construction(
        self, 
        t = None,    
        dt = None, 
        v_t_label_txt = '$\\vec{v}(t)$',
        v_t_label_dir = None,
        v_t_dt_label_txt = '$\\vec{v}(t+\\Delta t)$',
        v_t_dt_label_dir = 0.5 * DOWN + 1.5 * RIGHT,
        dv_label_txt = '$\\Delta \\vec{v}$',
        dv_label_dir = UP + 0.5 * RIGHT,
        a_label_txt = '$$\\vec{a}_{\\text{med}}=\\frac{\\Delta \\vec{v}}{\\Delta t}$$',
        a_label_dir = 3.0* DOWN + 0.5 * RIGHT,
        a_scale = None,
        continue_path = True):
        """Animates the construction of the average acceleration."""

        if t == None:
            t=self.t
        if dt == None:
            dt = self.dt
        if v_t_label_dir == None:
            v_t_label_dir = self.vel_label_dir
        if a_scale == None:
            a_scale = self.acc_scale

        point, path, v = self.run_trayectory_up_to_time(t)
        v_t, label_t = self.cinematic_vector(t, scale=self.vel_scale, label_text= v_t_label_txt, direction = v_t_label_dir)
        self.remove(v)
        self.play(
            Write(v_t),
            Write(label_t)
            )
        self.wait()
        group = self.run_trayectory_from_to(t,t+dt)
        point, path, v = group
        v_t_dt, label_t_dt = self.cinematic_vector(t+dt , scale=self.vel_scale, label_text=v_t_dt_label_txt, direction = v_t_dt_label_dir)
        self.remove(v)
        self.play(
            Write(v_t_dt),
            Write(label_t_dt)
            )
        self.wait()
        self.play(ApplyMethod(v_t_dt.shift, self.position(t)-self.position(t+dt)))
        self.remove(point, path)
        dv = self.cinematic_vector(
            t, f=self.dv, 
            scale = self.vel_scale, 
            label_text = dv_label_txt, color = ACCELERATION_COLOR,
            direction = dv_label_dir
        )
        dv.shift(self.vel_scale*self.velocity(t))
        self.play(ShowCreation(dv))
        self.wait()
        a = self.cinematic_vector(
            t, f=self.dv, 
            scale = a_scale * self.vel_scale, 
            label_text = a_label_txt,
            color = ACCELERATION_COLOR,
            direction = a_label_dir
        )
        self.play(Transform(dv, a))
        self.wait()
        if continue_path:
            self.remove(v_t_dt, label_t_dt)
            self.continue_trayectory_from(t)
        
    def construct(self):
        self.initialize_scene()
        self.animate_acceleration_construction()
        self.wait()

class mov_curvo_acel_components(mov_curvo_acel):
    """Escena (Scene) de animación de las componentes tangencial y centripeta de la aceleración."""
    CONFIG = {
        "show_velocity": True,
        "show_acceleration": True,
        "show_a_centripetal": False,
        "show_a_tangential": False,
        "show_tangent_perp_lines": False,
        "show_tangent_circle": False,
        "show_path": True,
        "title": "Componentes centripeta y tangencial de la aceleración",
        "show_title": True,
        "label_dir_ac": 1.5 * DOWN,
        "label_dir_at": 4.0 * UP + 2.0 * RIGHT,
    }

    def animate_a_tangent_a_centripetal(
        self, 
        t,   
        a_sum_text = "$\\vec{a} = \\vec{a}_c + \\vec{a}_t$",
        r_label_dir = 6.0 * UP +  7.0 * LEFT,
        continue_path = True):
        """Shows the centripetal and tangent components of acceleration."""

        point, path, v_vec, a_vec, *r = self.run_trayectory_up_to_time(t)
        self.animate_tangent_perp_lines(t)
        (tg_circle, center, r) = self.animate_tangent_circle(t)
        # texto r circulo tangente
        r_text = TextMobject('$r$', color = GREY)
        r_text.next_to(center, direction = r_label_dir)
        self.play(Write(r_text))
        self.wait()

        self.remove(v_vec)
        self.animate_acc_components(t)
        
        # texto a = ac + at
        a_vec, a_txt = a_vec
        a_decomp_txt = TextMobject(a_sum_text, color = ACCELERATION_COLOR)
        pos = self.position(t)
        a_decomp_txt.next_to(pos, direction = self.acc_label_dir)
        self.remove(a_txt)
        self.play(Write(a_decomp_txt))
        self.wait()

        # texto ac = ... at = ...
        ac_txt = TextMobject('$$a_c = \\frac{|\\vec{v}|^2}{r}$$', color = ACCELERATION_COLOR)
        at_txt = TextMobject('$$a_t = \\frac{d|\\vec{v}|}{dt}$$', color =ACCELERATION_COLOR )
        ac_txt.next_to(a_decomp_txt, direction = DOWN)
        at_txt.next_to(ac_txt, direction = DOWN)
        self.play(Write(ac_txt), Write(at_txt))

        if continue_path == True:
            self.acc_label_dir = DOWN + LEFT
            self.continue_trayectory_from(t)

    def construct(self):
        self.initialize_scene()
        t=self.t
        self.animate_a_tangent_a_centripetal(t)
        self.wait()
        
class mov_curvo_frenando(mov_curvo_acel):
    CONFIG = {
        'alpha': -0.35,   #   -0.035
        'omega': 1.35,     
        'phi': PI,
        'run_time': 2.9/0.3,  
        'initial_time' : 0.5/0.3,
        'time_rescale': 0.3,
        "acc_scale": 6.0,
        "vel_scale": 3.0,
        "show_velocity": True,
        "show_acceleration": False,
        "vel_label_dir": 2 * UP +  LEFT,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "y0": 3.0,
    }

    def X(self,t):
        xfactor = 1.2
        x0 = 0.0
        return x0 + xfactor * self.amplitud * np.cos(self.theta(self.time_rescale*t))
    def Y(self,t):
        y0 =  self.y0
        return y0 + self.amplitud * np.sin(self.theta(self.time_rescale*t))        
        
class mov_curvo_frenando_show_a(mov_curvo_frenando):
    CONFIG = {
        "show_velocity": True,
        "show_acceleration": True,
        "vel_label_dir": 2 * DOWN +  RIGHT,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_dir": UP,
        "acc_label_from": 'vec',  # position of the label: 'pos' from position or 'vec' from vector
    }
    
class mov_curvo_frenando_show_all_cinematics(mov_curvo_frenando):
    CONFIG = {
        "show_velocity": True,
        "show_acceleration": True,
        "vel_label_dir": 2 * DOWN +  RIGHT,
        "vel_label_from": 'pos',  # position of the label: 'pos' from position or 'vec' from vector
        "acc_label_dir": 0.25 * UP + 0.4 * LEFT,
        "acc_label_from": 'vec',  # position of the label: 'pos' from position or 'vec' from vector
        "label_dir_ac": 0.5 * RIGHT,
        "label_dir_at": 0.5 * DOWN,
        "show_a_centripetal": True,
        "show_a_tangential": True,
        "show_tangent_perp_lines": True,
        "show_tangent_circle": True,
        "label_from_ac": 'vec',
        "label_from_at": 'vec',
        "y0": 0.0,
    }

class proyectil(movimiento2D):
    CONFIG = {
        "graph_origin": BOTTOM + LEFT_SIDE + 1.2 * (UP + RIGHT),
        "title": "Movimiento de un proyectil",
        "x_min": 0,
        "x_max": 20,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(0, 21, 1)),
        "x_axis_label" : "$x$ (m)",
        "x_axis_width": 12,
        "y_min": 0,
        "y_max": 10,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(0, 11, 1)),
        "y_axis_label" : "$y$ (m)",
        "show_velocity": True,
        "show_acceleration": True,
        "acc_label": "$\\vec{a}=\\vec{g}$",
        "run_time": 2.45,
    }
    def X(self, t):
        vx0=7.5
        x0=0
        x=vx0*t+x0
        return x
    def Y(self,t):
        a=-9.8
        vy0=12.0
        y0=0.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y
    
