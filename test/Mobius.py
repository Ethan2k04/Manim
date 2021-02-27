from manimlib.imports import *

class Mobius(ThreeDScene):
    CONFIG = {"camera_config": {"background_color": BLACK},
              "phi": 0 * DEGREES,
              "theta": 0 * DEGREES,
              "distance": 50
              }
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)
        mobius = ParametricSurface(lambda u,v:np.array([
                                   (3 + u * np.cos(v/2))*np.cos(v),
                                   (3 + u * np.cos(v/2))*np.sin(v),
                                    u * np.sin(v/2)]),
                                    u_min=-1,u_max=1,v_min=0,v_max=2 * PI,checkerboard_colors=None,
                                      fill_color=BLUE,fill_opacity=1,stroke_color=WHITE,resolution=(100,10))

        self.play(ShowCreation(mobius))
        self.wait(2)
        phi_0,theta_0 = 0,0
        dt = 1/30
        for i in range(240):
            delta_phi = 240 * self.derivative_sigmoid(-6 + i * (12/240) , dt) * dt * DEGREES
            delta_theta = 480 * self.derivative_sigmoid(-6 + i * (12/240) , dt) * dt * DEGREES
            phi_0 += delta_phi
            theta_0 += delta_theta
            self.set_camera_orientation(phi=phi_0,theta=theta_0)
            self.wait(dt)

        self.wait(4)


    def sigmoid(self,t):
        return 1/(1 + np.exp(-t))

    def derivative_sigmoid(self,t,dt):
        return (self.sigmoid(t+dt) - self.sigmoid(t))/dt

