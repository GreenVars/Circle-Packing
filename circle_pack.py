from circle_solver import CircleSolver
from circle import Circle

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


def random_circles(n, min_r=1, max_r=100):
    from random import randint, uniform
    return [Circle(randint(min_r, max_r), 0, 0) for _ in range(n)]


all_the_same = [Circle(21, 0, 0) for r in range(19)]  # breaks when r = 20
descending_5 = [Circle(5 + 5 * r, 0, 0) for r in range(35)]
# g = CircleGraph(circles, double_r)
# cs = CircleSolver(random_circles(35))
def get_density(circles):
    cs = CircleSolver(circles)
    cs.solve()
    cs.cg.create_adj()
    cs.cg.draw(neighbor_lines=True, intersect_points=True, bounding_circle=True)
    return cs.cg.get_percentage_filled()

def sample(n, circ_count, min_r, max_r):
    densities = []
    while len(densities) < n:
        try:
            densities.append(get_density(random_circles(circ_count, min_r, max_r)))
        except: # algorithm has bug where will fail but we can still gather results where it works correctly
            pass

    return sum(densities)/len(densities)

def make_table():
    for x in range(20, 100, 20):
        for r in range(20, 100, 20):
            print("max_r=", r, "circle_count =", str(x),"avg_density", sample(30, x, 1, r))

print(get_density(random_circles(120, 10, 25)))