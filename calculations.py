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
    points = []

    # x = -10
    if b != 0:
        y = (c - a * (-10)) / b
        if -10 <= y <= 10:
            points.append([-10, y])

    # x = 10
    if b != 0:
        y = (c - a * (10)) / b
        if -10 <= y <= 10:
            points.append([10, y])

    # y = -10
    if a != 0:
        x = (c - b * (-10)) / a
        if -10 <= x <= 10:
            points.append([x, -10])

    # y = 10
    if a != 0:
        x = (c - b * (10)) / a
        if -10 <= x <= 10:
            points.append([x, 10])

    # якщо лінія повністю поза межами — повертаємо щось базове
    if len(points) < 2:
        return [[0, 0], [0, 0]]

    # беремо лише 2 точки (будь-які 2 достатньо)
    return points[:2]



def transform_values(points):
    transformed = []
    for x, y in points:
        if -10 <= x <= 10:
            x = 300 + x * 25
        else:
            x = 300

        if -10 <= y <= 10:
            y = 300 - y * 25
        else:
            y = 300

        transformed.append([x, y])
    return transformed

