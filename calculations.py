#ax+by=c
def calculate_axes_intersections(a, b, c):
    points = []
    if b != 0:
        points.append([0, c/b])
    if a != 0:
        points.append([c/a, 0])
    if not points:
        points = [[0,0]]
    return points

def calculate_limits(a, b, c):
    xmin = [-10, (c - a*(-10)) / b] if b != 0 else None
    xmax = [10, (c - a*(10)) / b] if b != 0 else None
    ymin = [(c - b*(-10)) / a, -10] if a != 0 else None
    ymax = [(c - b*(10)) / a, 10] if a != 0 else None

    return [p for p in [xmin, xmax, ymin, ymax] if p is not None]


def transform_values(l):
    x, y = l

    if -10 <= x <= 10:
        x = 300 + x * 25
    else:
        x = 300

    if -10 <= y <= 10:
        y = 300 - y * 25
    else:
        y = 300

    return [x, y]
