from manimlib.imports import *
import numpy as np

def cross_product(v1, v2):
    return np.array([
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ])

class ThreeDLine(VMobject):
    CONFIG = {
        'color': BLUE,
        'fill_opacity': 1,
        'radius': 0.05,
        'circle_side_width': 2,
        'circle_side_color': None,
        'delta_radian': np.sqrt(3) / 60
    }
    def __init__(self, vector=RIGHT, position=ORIGIN, **kwargs):
        VMobject.__init__(self,**kwargs)
        self.__vector_position_dot = Dot(ORIGIN, radius=0.01, fill_opacity=0)
        self.__vector_end_dot = Dot([0, 0, get_norm(vector)], radius=0.01, fill_opacity=0)
        self.add(self.__vector_position_dot, self.__vector_end_dot)
        if get_norm(vector) > 0.:
            self.__get_some_parameters()
            self.__add_cylinder()
            self.__delete_some_useless_parameters()
            self.set_direction(vector)
        self.shift(position)

    def __get_some_parameters(self):
        self.vector_length = self.get_vector_length()
        self.delta_theta = self.delta_radian / self.radius

    def __add_cylinder(self):

        thetas = np.c_[0:2 * np.pi:self.delta_theta]

        bc_points = np.c_[
            self.radius * np.cos(thetas),
            self.radius * np.sin(thetas),
            np.zeros_like(thetas)].tolist()

        tc_points = np.c_[
            self.radius * np.cos(thetas),
            self.radius * np.sin(thetas),
            np.full_like(thetas, self.vector_length)].tolist()

        for i in range(-1, len(bc_points) - 1):
            self.add(Polygon(
                *[*bc_points[i:i + 2], tc_points[i + 1], tc_points[i]],
                color=self.color,
                stroke_width=1,
                stroke_color=self.color,
                fill_opacity=self.fill_opacity,
                shade_in_3d=True)
            )

        self.add(Polygon(
            *tc_points,
            color=self.color,
            stroke_width=self.circle_side_width,
            stroke_color=self.circle_side_color,
            fill_opacity=self.fill_opacity,
            shade_in_3d=True)
        )

        self.add(Polygon(
            *bc_points,
            color=self.color,
            stroke_width=self.circle_side_width,
            stroke_color=self.circle_side_color,
            fill_opacity=self.fill_opacity,
            shade_in_3d=True)
        )

    def __delete_some_useless_parameters(self):

        del self.vector_length
        del self.radius
        del self.delta_radian

    def get_position(self):
        # This method is used to get the position of vector
        # In this class, the position of the vector all means the position of beginning point of the vector
        return self.__vector_position_dot.get_center()

    def get_end(self):
        # This method is used to get the position of end point of the vector
        return self.__vector_end_dot.get_center()

    def get_vector(self):
        # This method is used to get the array of the vector
        return self.get_end() - self.get_position()

    def get_start_and_end(self):
        return self.get_position(), self.get_end()

    def get_vector_length(self):
        # This method is used to get the length of the vector
        return get_norm(self.get_vector())

    def get_unit_vector(self):
        # This method is used to get the unit vector of the vector
        return self.get_vector() / self.get_vector_length()

    def set_direction(self, new_direction):
        # This method is used to change the direction of vector into a new direction
        # It only changes the direction but not changes the length of the vector
        norm = np.array(new_direction, dtype=np.float64) / get_norm(new_direction)
        cosine = self.get_unit_vector().dot(norm)
        if cosine > 1.:
            cosine = 1
        elif cosine < -1.:
            cosine = -1
        return self.rotate(
            np.arccos(cosine),
            axis=cross_product(self.get_vector(), norm),
            about_point=self.get_position())

    def set_position(self, new_position):
        # This method is used to change the position of vector into a new position
        return self.shift(np.array(new_position, dtype=np.float64) - self.get_position())

    def set_vector_length(self, new_length):
        # This method is used to change the length of the vector into a new length
        # It achieves the aim through scaling the vector(self.scale(...)), so the vector will be made larger of smaller
        # Scaling the vector will also change the position of the vector
        # So this method also sets the position to the original position
        original_position = self.get_position()
        self.scale(new_length / self.get_vector_length())
        return self.set_position(original_position)

    def set_vector(self, new_vector, new_position=None):
        # This method does the three things below:
        # The first one is changing the direction of the vector into the direction of a new vector
        # The second one is changing the length of  the vector into the length of the new vector
        # The last one is changing the position of the vector into the position of the new vector
        # If you don't give the paramter 'new_position', the last one won't be done
        if new_position:
            self.set_position(new_position)
        self.set_direction(new_vector)
        return self.set_vector_length(get_norm(new_vector))

    def move_along_curve(self, func, t, dt):
        # The form of this parameter 'func' is 'lambda t:np.array([x(t),y(t),z(t)])'
        # This method will move the vector to a point on the curve of 'func'
        # And change the direction of the vector into the direction of the tangent vector at this point
        self.set_direction(func(t + dt) - func(t))
        return self.set_position(func(t))

    def put_start_and_end_on(self, start, end):
        curr_start, curr_end = self.get_start_and_end()
        curr_vect = curr_end - curr_start
        if np.all(curr_vect == 0):
            return self
            #raise Exception("Cannot position endpoints of closed loop")
        target_vect = end - start
        self.scale(
            get_norm(target_vect) / get_norm(curr_vect),
            about_point=curr_start,
        )
        self.rotate(
            angle_of_vector(target_vect) -
            angle_of_vector(curr_vect),
            about_point=curr_start
        )
        self.shift(start - curr_start)
        return self
