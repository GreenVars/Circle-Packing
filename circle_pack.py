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


def random_circles(n):
    from random import randint
    return [Circle(randint(5, 100), 0, 0) for i in range(n)]


all_the_same = [Circle(21, 0, 0) for r in range(19)]  # breaks when r = 20
descending_5 = [Circle(5 + 5 * r, 0, 0) for r in range(25)]
# g = CircleGraph(circles, double_r)
cs = CircleSolver(random_circles(40))
cs.solve()
cs.cg.create_adj()
cs.cg.draw(neighbor_lines=True, intersect_points=True, bounding_circle=True)
print(cs.cg.get_percentage_filled())