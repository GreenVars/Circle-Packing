from math import pi

from circle_graph import CircleGraph
from circle import Circle

import scipy.optimize
import spiral


class CircleSolver:
    def __init__(self, circles):
        self.cg = CircleGraph(circles)
        self.a = spiral.calculate_a(self.cg.circles[0].r)
        self.c_0 = self.cg.circles[0]
        self.r_0 = self.cg.circles[0].r

    def solve(self, file_name):
        self.place_in_spiral()

    def place_in_spiral(self, inside=True):
        self.place_first_two_circles()
        for index, c in enumerate(self.cg.circles[2:], start=2):
            self.place_circle(index)
        # anchor first two
        self.cg.circles[0].anchored = True
        self.cg.circles[1].anchored = True

        if inside:
            self.turn_inside()
            pass

    def place_first_two_circles(self):
        self.cg.empty_adj()
        self.cg.circles[0].x = 0
        self.cg.circles[0].y = 0
        r_prime = self.cg.circles[1].r
        theta_prime = spiral.solve_for_theta(self.r_0 + r_prime, a=self.a)
        self.cg.circles[1].x, self.cg.circles[1].y = spiral.polar_to_cart(self.r_0 + r_prime, theta_prime)

    def place_circle(self, i, add_bounding_circles=False):
        prev_circ = self.cg.circles[i - 1]
        curr_circ = self.cg.circles[i]
        prev_r = prev_circ.r
        curr_r = curr_circ.r

        origin_to_prev_center, prev_theta = spiral.cart_to_polar_on_spiral(prev_circ.x, prev_circ.y, self.a)

        theta_min = spiral.calc_theta_lower_bound(prev_theta, prev_r, curr_r, a=self.a)
        theta_max = spiral.calc_theta_upper_bound(origin_to_prev_center, prev_r, curr_r, a=self.a,
                                                  lower_bound=theta_min)

        if add_bounding_circles:  # for debugging and graphics
            r_min = spiral.spiral(theta_min, self.a)
            r_max = spiral.spiral(theta_max, self.a)

            x_min, y_min = spiral.polar_to_cart(r_min, theta_min)
            x_max, y_max = spiral.polar_to_cart(r_max, theta_max)

            self.cg.circles.append(Circle(4, x_min, y_min))
            self.cg.circles.append(Circle(6, x_max, y_max))

        def difference_from_r_sum(theta):
            r = spiral.spiral(theta, a=self.a)
            x, y = spiral.polar_to_cart(r, theta)
            return prev_circ.distance(x, y) - curr_r - prev_r

        theta_hat = scipy.optimize.brentq(difference_from_r_sum, theta_min, theta_max)

        r_hat = spiral.spiral(theta_hat, a=self.a)

        curr_circ.x, curr_circ.y = spiral.polar_to_cart(r_hat, theta_hat)

    def turn_inside(self):
        for index, c in enumerate(self.cg.circles[2:], start=2):
            if self.rotate_circle_and_co(index) == False:  # Rotation caused an overlap of original circle
                print(index)
                break
        else:  # no overlaps
            return True

        # Rotated such that first tier is filled
        self.twist_rotate(index)
        # self.rotate_with_respect_to_circ(index-1, index, -2.517059278918)
        # self.rotate_with_respect_to_circ(index, index+1, -1.1)
        # self.rotate_until_tangent_with(index, index-2)

    # -0.3419075978427143 2.4070359278918034


    def twist_rotate(self, starting_index):
        tangent_to = starting_index - 2
        for c_index, circ in enumerate(self.cg.circles[starting_index:], start=starting_index):
            try:
                intersects = self.rotate_until_tangent_with(c_index, tangent_to)
            except:
                return
            print(intersects)
            while intersects == False:
                print(55)
                tangent_to -= 1
                try:
                    intersects = self.rotate_until_tangent_with(c_index, tangent_to)
                except Exception as e:
                    print(e)
                    return
            print("did circ successcully " + str(c_index) + " " + str(circ))

    def rotate_with_respect_to_circ(self, pivot_index, circ_index, angle):
        pivot = self.cg.circles[pivot_index]
        circ = self.cg.circles[circ_index]
        circ.x, circ.y = spiral.rotate_point((pivot.x, pivot.y), (circ.x, circ.y), angle)

    def rotate_until_tangent_with(self, circ_index, tangent_index):
        pivot = self.cg.circles[circ_index - 1]
        circ = self.cg.circles[circ_index]
        tangent = self.cg.circles[tangent_index]

        # determine bounds
        def dist_to_tangent(theta):
            x, y = spiral.rotate_point((pivot.x, pivot.y), (circ.x, circ.y), theta)
            return tangent.distance(x, y) - tangent.r - circ.r

        pivot_angle_to_circ = pivot.angle_to_circ(circ)
        pivot_angle_to_tan = pivot.angle_to_circ(tangent)
        print()



        print("Circ to rotate " + str(circ))
        print("pivot " + str(pivot))
        print("tangent " + str(tangent))

        lower = -.5  # min(pivot_angle_to_circ, pivot_angle_to_tan)
        upper = -pi - .5  # max(pivot_angle_to_circ, pivot_angle_to_tan)
        print(lower, upper)
        print(dist_to_tangent(lower), dist_to_tangent(upper))
        theta_hat = scipy.optimize.brentq(dist_to_tangent, lower, upper)  # CHECK BOUNDS
        print(theta_hat)

        for index, c in enumerate(self.cg.circles[circ_index:], start=circ_index):
            self.rotate_with_respect_to_circ(circ_index - 1, index, theta_hat)

        return not self.cg.overlaps(circ_index)

    def rotate_circle_and_co(self, i):  # Clockwise bc of inverted y
        pivot = self.cg.circles[i - 1]
        circ = self.cg.circles[i]

        # determine bounds
        def dist_to_c(theta):
            x, y = spiral.rotate_point((pivot.x, pivot.y), (circ.x, circ.y), theta)
            return self.c_0.distance(x, y) - self.r_0 - circ.r

        theta_hat = scipy.optimize.brentq(dist_to_c, 0, pi / 4)  # CHECK BOUNDS
        for index, c in enumerate(self.cg.circles[i:], start=i):
            self.rotate_with_respect_to_circ(i - 1, index, theta_hat)

        return not self.cg.overlaps(i)
