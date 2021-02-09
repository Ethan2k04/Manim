from manimlib.imports import *

class ParallelCapacitorPlate(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": WHITE},
              "phi": 60 * DEGREES,
              "theta": 30 * DEGREES,
              "distance": 50
              }
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(self.phi,self.theta,self.distance)
        self.add(axes)
        plate_1,plate_2 = Prism().set_color(GREY).set_opacity(1).scale(np.array([1,3,0.8])),Prism().set_color(GREY).set_opacity(1).scale(np.array([1,3,0.8]))
        plate_1.move_to(ORIGIN)
        plate_2.move_to(ORIGIN)
        plate_1.shift(OUT * 2.5)
        plate_2.shift(IN * 2.5)
        vector_0 = Vector(UP*2).set_color(YELLOW).rotate(PI/2,LEFT).move_to(ORIGIN)
        vector_group = VGroup()
        for i in range(3):
            for j in range(4):
                vector = vector_0.copy().shift(LEFT * i).shift(UP * j * 1.5)
                vector_group.add(vector)
        vector_group.move_to(ORIGIN).shift(OUT*2)
        self.add(vector_group)
        self.add(plate_1, plate_2)
        #self.set_camera_orientation(PI/2,PI/2,50)
        for i in range(6):
            self.flash_vector(vector_group,4)
        self.wait(2)

    def flash_vector(self,vector_group,displacement):
        position_init = vector_group.get_center()
        self.play(ApplyMethod(vector_group.shift,IN * displacement),run_time=0.5,rate_func=linear)
        #self.wait(0.5)
        vector_group.move_to(position_init)

class CoulombLaw(ThreeDScene):
    CONFIG = {
        "particle": {
            "color_p": BLUE,
            "color_n": RED,
            "radius": 0.5
        }
    }

    def get_charged_particle(self, mass=1, electricity_quantity=1, position=ORIGIN, velocity=RIGHT, **kwargs):
        para = self.particle
        color = "color_p" if electricity_quantity > 0 else "color_n"
        particle = Sphere(radius=para["radius"], color=para[color])
        particle.electricity_quantity = electricity_quantity
        particle.mass = mass
        particle.move_to(position)
        particle.velocity = velocity

        return particle

    def update_particles_velocity(self, *particles):
        dt = 1e-3
        particle_list = []
        for particle in particles:
            particle_list.append(particle)

        for father_particle in particle_list:
            child_particles = particle_list[:]
            particle_list.pop(0)
            for child_particle in child_particles:
                vect = father_particle.get_center() - child_particle.get_center()
                distance = round(get_norm(vect), 2)
                direction_vect = vect/distance
                acceleration = round(father_particle.electricity_quantity * child_particle.electricity_quantity / (father_particle.mass * distance**2), 2)
                father_particle.velocity += acceleration * direction_vect * dt
            particle_list.append(father_particle)

    def update_particles_postion(self, *particles):
        dt = 1e-3
        self.update_particles_velocity(*particles)
        for particle in particles:
            particle.move_to(particle.get_center() + particle.velocity * dt)

    def start_move(self, particles):
        for particle in particles:
            particle.add_updater(self.update_particles_postion)

class Test1(CoulombLaw):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 60,
              "theta": 60 * DEGREES,
              "distance": 200,
              }

    def construct(self):
        self.set_camera_orientation(phi=self.phi, theta=self.theta, distance=self.distance)
        p1 = self.get_charged_particle(position=LEFT, velocity=UP)
        p2 = self.get_charged_particle(position=RIGHT, velocity=DOWN)
        particles = VGroup(p1, p2)
        self.add(particles)
        self.start_move(particles)
        self.wait(3)