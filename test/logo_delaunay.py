from manimlib.imports import *

class Delaunay(Scene):
    def construct(self):
        # Create a random set of points
        d_1 = self.delaunay_construct()
        d_2 = self.delaunay_construct()
        d_3 = self.delaunay_construct()
        self.play(ShowCreation(d_1))
        self.play(ReplacementTransform(d_1,d_2))
        self.play(ReplacementTransform(d_2, d_3))
        # Create Delaunay Triangulation and insert points one by one
    def delaunay_construct(self):
        seeds = np.random.random((30, 2))
        dt = Delaunay2D()
        for s in seeds:
            dt.addPoint(s)

        dot_info = dt.exportDT()
        line_info = dt.exportTriangles()
        dot_group = VGroup()
        line_group = VGroup()
        for i in dot_info[0]:
            dot = Dot()
            pos_0 = i * 5
            pos = np.array([round(pos_0[0], 2), round(pos_0[1], 2), 0])
            dot.move_to(pos)
            dot_group.add(dot)

        for i in line_info:
            tri_dot = VGroup()
            tri_line = VGroup()
            for j in i:
                tri_dot.add(dot_group[j])
            line_1 = Line(tri_dot[0],tri_dot[1])
            line_2 = Line(tri_dot[1], tri_dot[2])
            line_3 = Line(tri_dot[2], tri_dot[0])
            line_group.add(line_1,line_2,line_3)
        print(line_info)
        delaunay = VGroup(line_group,dot_group)
        delaunay.move_to(ORIGIN)
        return delaunay



        # Dump points and triangles to console
        #print("Input points:\n", seeds)
        #print ("Delaunay triangles:\n", dt.exportDT())