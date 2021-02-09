from manimlib.imports import *


class Graph():

    def __init__(self,x_row,y_row,start,end,barrier=None):
        self.x_row = x_row
        self.y_row = y_row
        self.start = start
        self.end = end
        self.barrier = barrier
        self.position = self.start

    def update(self,increment):
        self.position += increment


class AStar(Scene):

    def built_in_algorithm(self):
        x = np.array([10,0,0])
        y = np.array([0,10,0])
        start = np.array([2,2,0])
        end = np.array([8,8,0])
        graph = Graph(x,y,start,end)
        movement_map = []

        while graph.position != graph.end:
            dis_map = {}
            for i in [UP,RIGHT,DOWN,LEFT]:
                act = graph.position + i
                movement = act - graph.start
                to_end = end - act
                value = abs(movement[0]) + abs(movement[1]) + abs(to_end[0]) + abs(to_end[1])
                dis_map[i] = value
            for key,value in dis_map.items():
                if value == min(dis_map.values()):
                    movement_map.append(key)
                    break
          #  graph.position += movement_map[]

    def construct(self):
        pass

