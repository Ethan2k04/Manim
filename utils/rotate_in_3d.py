from manimlib.imports import *

#TODO abandoned
class Rotate3D(ThreeDScene):
    CONFIG = {
        "run_time": None,
        "lag_ratio": None,
        "rate_func": linear,
    }
    def __init__(self,**kwargs):
        digest_config(self,kwargs)

    def rotate(self):
        pass