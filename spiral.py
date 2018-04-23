from math import log, pi, exp, sqrt, cos, sin

phi = (1 + sqrt(5)) / 2
b = 2 * log(phi) / pi


def polar_to_cart(r, theta):
    return r * cos(theta), r * sin(theta)


def cart_to_polar_on_spiral(x, y, a, b=b):
    r = sqrt(x ** 2 + y ** 2)
    return (r, solve_for_theta(r, a, b))


def arc_length(theta, a, b=b):
    return (a * sqrt(1 + b ** 2) * exp(b * theta)) / b


def spiral(theta, a, b=b):
    return a * exp(b * theta)


def calculate_a(max_r):
    return max_r / 1 / phi ** 4


def solve_for_theta(r, a, b=b):
    return log(r / a) / b


def calculate_spiral_lower_bound(radii, a, b=b):
    k_prime = 2 * b * sum(radii) / (a * sqrt(1 + b ** 2))
    return log(k_prime) / b


def calc_theta_upper_bound(origin_to_prev_center, prev_r, curr_r, a, b=b, lower_bound=None):
    if lower_bound: # Something to compare to to check acuteness
        r_hat = sqrt((curr_r + prev_r) ** 2 + (origin_to_prev_center) ** 2)
        theta_1 = solve_for_theta(r_hat, a, b=b)
        if theta_1 > lower_bound: # Acute, can use better upper bound
            return theta_1

    # Not acute, must use general triangle inequality
    r_hat = origin_to_prev_center + prev_r + curr_r
    return solve_for_theta(r_hat, a, b=b)


def calc_theta_lower_bound(prev_theta, prev_r, curr_r, a, b=b):
    return log((b / (a * sqrt(1 + b ** 2))) * (prev_r + curr_r + arc_length(prev_theta, a, b))) / b

def rotate_point(pivot, point, angle):
    return (cos(angle) * (point[0] - pivot[0]) - sin(angle) * (point[1] - pivot[1]) + pivot[0],
            sin(angle) * (point[0] - pivot[0]) + cos(angle) * (point[1] - pivot[1]) + pivot[1])