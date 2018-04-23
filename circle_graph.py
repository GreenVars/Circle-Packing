from math import pi
from circle import Circle
from circle_drawer import CircleDrawer
from circle_bounder import from_circle_set

def double_r(c1, c2):
    if not c1.is_placed() or not c2.is_placed():
        return False
    return c1.distance_circ(c2) - c1.r - c2.r <= 1e-5


class CircleGraph():

    def __init__(self, circles, neighbor_func=double_r):
        self.circles = circles
        self.circles.sort(key = lambda c: c.r)
        self.circles = self.circles[::-1]
        self.neighbor_func = neighbor_func
        self.create_adj()

    def empty_adj(self):
        self.adj_m = [[0 for i in self.circles] for j in self.circles]

    def create_adj(self):
        """Create graph from given list of circles and function to determine if neighbors"""
        adj = []
        for c in self.circles:
            adj.append([int(c != c2 and self.neighbor_func(c, c2)) for c2 in self.circles])

        self.adj_m = adj

    def draw(self, neighbor_lines=False, intersect_points=False, bounding_circle=True):
        return CircleDrawer(self).draw(neighbor_lines=neighbor_lines,
                                       intersect_pts=intersect_points,
                                       bounding_circle=bounding_circle
                                       )

    def overlaps(self, circ):
        overlaps = []
        if not circ.is_placed():
            return overlaps
        for c in self.circles:
            if not c.is_placed() or c is circ:
                continue
            if c.overlaps(circ):
                overlaps.append(c)
        return overlaps

    def get_bounding_circle(self):
       return from_circle_set(self.circles)

    def get_percentage_filled(self):
        total_a = sum(pi*(c.r**2) for c in self.circles if c.is_placed())
        bound_area = pi*(self.get_bounding_circle().r ** 2)
        return total_a / bound_area

