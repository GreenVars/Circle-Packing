from circle import Circle
from circle_drawer import CircleDrawer

def double_r(c1, c2):
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

    def draw(self, neighbor_lines=False, intersect_points=False, draw_golden_spiral=True):
        return CircleDrawer(self).draw(neighbor_lines=neighbor_lines,
                                       intersect_pts=intersect_points,
                                       spiral=draw_golden_spiral)

    def overlaps(self, i):
        circ = self.circles[i]
        for c in self.circles:
            if c is circ:
                continue
            if c.overlaps(circ):
                print(c, circ)
                print(4972974)
                return True
        return False

if __name__ == "__main__":
    from circle_solver import CircleSolver

    circles = [
        Circle(10, 100, 200),
        Circle(30, 150, 200),
        Circle(90, -300, 115),
        Circle(130, 100, 30),
        Circle(115, 100, 150),
        Circle(60, -350, -30),
        Circle(30, 110, 175),
        Circle(5, -200, 65)
    ]

    circles2 = [
        Circle(10, 50, 50),
        Circle(40, 60, 50),
        Circle(50, 60, 50),
        Circle(15, 50, 50),
        Circle(20, 60, 50),
        Circle(18, 50, 50),
        Circle(24, 60, 50),
        Circle(10, 50, 50),
        Circle(20, 60, 50),
        Circle(10, 50, 50),
        Circle(20, 60, 50),
        Circle(10, 60, 50),
        Circle(10, 60, 50),
        Circle(10, 60, 50),
        Circle(10, 60, 50),
        Circle(15, 60, 50),
        Circle(14, 60, 50),
        Circle(13, 60, 50),
        Circle(12, 60, 50),
        Circle(11, 60, 50),

    ]

    # g = CircleGraph(circles, double_r)
    cs = CircleSolver([Circle(5 + 5*r, 0 , 0 ) for r in range(15)])
    cs.solve(None)
    cs.cg.create_adj()
    cs.cg.draw(neighbor_lines=True, intersect_points=True, draw_golden_spiral=True)
