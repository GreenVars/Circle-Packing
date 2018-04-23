from math import pi

from circle_graph import CircleGraph
from circle import Circle


class CircleSolver:
    def __init__(self, circles):
        self.cg = CircleGraph(circles)
        self.tangent_to = self.cg.circles[0]

    def solve(self):
        self.clear_circle_coords()
        self.place_first_two_circles()
        for i in range(2, len(self.cg.circles)):
            try:
                self.place_circle(i)
            except Exception as e:
                raise Exception("ALGORITHM FAILED, COULD NOT FIND PLACE TO PUT NEXT CIRCLE")

    def clear_circle_coords(self):
        for c in self.cg.circles:
            c.x, c.y = None, None

    def place_first_two_circles(self):
        self.cg.empty_adj()
        self.cg.circles[0].x = 0
        self.cg.circles[0].y = 0
        self.cg.circles[1].x = 0
        self.cg.circles[1].y = self.cg.circles[0].r + self.cg.circles[1].r

    def place_circle(self, i):
        tangent_r = self.tangent_to.r
        curr = self.cg.circles[i]
        prev = self.cg.circles[i-1]

        from_tangent = Circle(tangent_r + curr.r, self.tangent_to.x, self.tangent_to.y)
        from_prev = Circle(prev.r + curr.r, prev.x, prev.y)

        intersect_pts = from_tangent.intersect(from_prev)
        overlaps = [self.cg.overlaps(Circle(curr.r, pt[0], pt[1])) for pt in intersect_pts]
        for index, overs in enumerate(overlaps):
            if len(overs) == 0:
                curr.x, curr.y = intersect_pts[index]
                return None

        flattened_overlaps = [item for items in overlaps for item in items]
        self.tangent_to = max(flattened_overlaps, key=lambda c: c.r)
        self.place_circle(i)