from random import uniform


def monte_carlo_area(n):
    s0 = 4 * 4
    s_t = 6.57343

    cnt = 0
    for _ in range(n):
        x = uniform(-2, 2)
        y = uniform(-2, 2)
        if area_condition(x, y):
            cnt += 1

    result = (cnt / n) * s0
    relative_error = abs(result - s_t) / s_t
    return (result, relative_error)


def area_condition(x, y):
    return -(x**3) + y**5 < 2 and x - y < 1


def monte_carlo_integral(n):
    a = 0
    b = 2
    analytic_result = int_f(b) - int_f(a)

    integral_sum = 0
    for _ in range(n):
        x = uniform(a, b)
        integral_sum += f(x)

    result = (integral_sum / n) * (b - a)
    relative_error = abs(result - analytic_result) / analytic_result
    return (result, relative_error)


def f(x):
    return x**3


def int_f(x):
    return x**4 / 4
