from circle_intersection import circle_intersection
import math


class Circle():
    def __init__(self, r, x, y):
        self.r = r
        self.x = x
        self.y = y
        self.anchored = False

    def distance(self, x, y):
        """Distance from center of circle to another point"""
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def distance_circ(self, c2):
        """Distance from center of circle to center of another circle"""
        return self.distance(c2.x, c2.y)

    def angle_to_circ(self, c2):
        return self.angle_to(c2.x, c2.y)

    def angle_to(self, x, y):
        """Angle from center of circle to point"""
        return math.atan2(self.y - y, self.x - x)

    def circum_distance(self, x, y):
        """Distance from closest point on circle circumfrance to point"""
        return self.distance(x, y) - self.r

    def circum_distance_circ(self, c2):
        """Distance from closest point on circle circumfrance to closest point on other cirlce circumfrance"""
        return self.distance(c2.x, c2.y) - self.r - c2.r

    def intersect(self, c2):
        """Returns iterable of points other circle intersects this one"""
        return circle_intersection((self.x, self.y, self.r), (c2.x, c2.y, c2.r))

    def overlaps(self, c2):
        d = self.distance_circ(c2)
        if d <= abs(self.r - c2.r):
            return True # One circle inside other
        intersect_pts = self.intersect(c2)
        if len(intersect_pts) < 2:
            return False
        return distance(intersect_pts[0], intersect_pts[1]) > 1e-3 # Intersect points are sufficiently different

    def __repr__(self):
        return "(r={}, ({}, {}))".format(self.r, self.x, self.y)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)