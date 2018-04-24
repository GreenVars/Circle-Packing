from math import pi

from circle_graph import CircleGraph
from circle import Circle

import sys

STANDARD_LIMIT = sys.getrecursionlimit()

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

    def place_circle(self, i): # ISSUE IN THIS WHERE IT WON'T PICK CORRECT NEXT TANGENT CAUSING INFINITE LOOP
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
        #flattened_overlaps.remove(self.tangent_to)
        #flattened_overlaps.remove(prev)
        try:
            self.tangent_to = max(flattened_overlaps, key=lambda c: c.r) # pick furthest circle
            self.place_circle(i)
        except RecursionError as e: # clause to try all possible overlaps and picking valid config
            sys.setrecursionlimit(100)  # work around for tangent brute force, bad practice but will speed up runs
            # TODO REWRITE THIS TO CLEVERLY FIND PROPER NEXT TANGENT, NO BRUTE FORCE
            flattened_overlaps.remove(self.tangent_to)
            while len(flattened_overlaps) > 0:
                try:
                    self.tangent_to = flattened_overlaps[0]
                    self.place_circle(i)
                    sys.setrecursionlimit(STANDARD_LIMIT)
                    return
                except:
                    flattened_overlaps.remove(self.tangent_to)

            raise Exception("RAN OUT OF POSSIBILITIES") # no overlaps work as a tangent
