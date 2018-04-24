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
descending_5 = [Circle(5 + 5 * r, 0, 0) for r in range(20)]
# g = CircleGraph(circles, double_r)
# cs = CircleSolver(random_circles(35))
def get_density(circles, file_name="ex.png"):
    cs = CircleSolver(circles)
    cs.solve()
    cs.cg.create_adj()
    cs.cg.draw(neighbor_lines=True, intersect_points=True, bounding_circle=True, file_name=file_name)
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
    """
    /home/admin/Programs/anaconda3/bin/python /home/admin/Dev/circles/circle_pack.py
max_r= 20 circle_count = 20 avg_density 0.6830343654371949
max_r= 40 circle_count = 20 avg_density 0.6821697765657849
max_r= 60 circle_count = 20 avg_density 0.6874599516992347
max_r= 80 circle_count = 20 avg_density 0.676180359926015
max_r= 20 circle_count = 40 avg_density 0.6992188858115557
max_r= 40 circle_count = 40 avg_density 0.6954109958255275
max_r= 60 circle_count = 40 avg_density 0.7008481309787218
max_r= 80 circle_count = 40 avg_density 0.6984942369944757
max_r= 20 circle_count = 60 avg_density 0.720750393626036
max_r= 40 circle_count = 60 avg_density 0.7120921259825378
max_r= 60 circle_count = 60 avg_density 0.717020028857957
max_r= 80 circle_count = 60 avg_density 0.7133454496289922
max_r= 20 circle_count = 80 avg_density 0.7276226049056339
max_r= 40 circle_count = 80 avg_density 0.7278964763228614
max_r= 60 circle_count = 80 avg_density 0.7247804441006381
max_r= 80 circle_count = 80 avg_density 0.7218198204706388

Process finished with exit code 0


    :return:
    """
    for x in range(20, 100, 20):
        for r in range(20, 100, 20):
            print("max_r=", r, "circle_count =", str(x),"avg_density", sample(30, x, 1, r))

#print(get_density(random_circles(200, 5, 20), file_name="200random5to20.png"))
print(get_density(descending_5, file_name="radius5to100.png"))
#make_table()

# uniform 37 radius 25 .755102
# 100random5to50 0.7465
# 200random5to20 .7370995
# 40random10to100 0.721147
# 20random10to250 0.683337
# radius5to100 0.6786
