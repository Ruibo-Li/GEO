from built_in_classes import *
import math


def get_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def is_vertical(line):
    vertices = line.vertices
    if vertices[0].x == vertices[1].x:
        return True
    return False


# compute the cross point of two lines
# returns None if parallel
# point might not be on the line segments
def compute_cross(line1, line2):
    if is_vertical(line1) and is_vertical(line2):
        return None

    vertices1 = line1.vertices
    vertices2 = line2.vertices
    p1 = vertices1[0]
    p2 = vertices1[1]
    q1 = vertices2[0]
    q2 = vertices2[1]

    if is_vertical(line1):
        k2 = (q1.y - q2.y) * 1.0 / (q1.x - q2.x)
        b = q1.y - k2 * q1.x
        c_y = k2 * p1.x + b
        return GPoint(p1.x, c_y)
    if is_vertical(line2):
        k1 = (p1.y - p2.y) * 1.0 / (p1.x - p2.x)
        b = p1.y - k1 * p1.x
        c_y = k1 * q1.x + b
        return GPoint(q1.x, c_y)

    k1 = (p1.y - p2.y) * 1.0 / (p1.x - p2.x)
    k2 = (q1.y - q2.y) * 1.0 / (q1.x - q2.x)
    if abs(k1 - k2) < 1e-6:
        return None
    b1 = p1.y - k1 * p1.x
    b2 = q1.y - k2 * q1.x
    cross_x = (b2 - b1) * 1.0 / (k1 - k2)
    cross_y = k1 * cross_x + b1
    return GPoint(cross_x, cross_y)


# whether two circles intersect
def circle_in(circle1, circle2):
    return get_distance(circle1.center, circle2.center) < (circle1.radius + circle2.radius)


# whether two rectangles intersect
def rectangle_in(rec1, rec2):
    vertices1 = rec1.vertices
    vertices2 = rec2.vertices
    p1 = vertices1[0]
    p2 = vertices1[1]
    q1 = vertices2[0]
    q2 = vertices2[1]
    if min(p1.x, p2.x) > max(q1.x, q2.x) or max(p1.x, p2.x) < min(q1.x, q2.x) or min(p1.y, p2.y) > max(q1.y,
                                                                                                       q2.y) or max(
            p1.y, p2.y) < min(q1.y, p2.y):
        return False
    return True


# shape1 must be a triangle, shape2 could be a triangle or a rectangle
def triangle_in(tri1, tri2):
    ver1 = tri1.vertices
    ver2 = tri2.vertices
    if isinstance(tri2, GRectangle):
        ver2.append(GPoint(ver2[0].x, ver2[1].y))
        ver2.append(GPoint(ver2[1].x, ver2[0].y))
    lines1 = []
    for i in range(len(ver1)):
        for j in range(i + 1, len(ver1)):
            l = GLine(ver1[i], ver1[j])
            lines1.append(l)
    lines2 = []
    for i in range(len(ver2)):
        for j in range(i + 1, len(ver2)):
            l = GLine(ver2[i], ver2[j])
            lines2.append(l)
    for l1 in lines1:
        for l2 in lines2:
            p = compute_cross(l1, l2)
            vers = l1.vertices
            if p is not None and (p.x < max(vers[0].x, vers[1].x)) and p.x > min(vers[0].x, vers[1].x):
                return True

    if is_inside(ver1[0], tri2):
        return True
    if is_inside(ver2[0], tri1):
        return True
    return False


# c is a circle, shape could be a triangle or rectangle
def circle_oth_in(c, shape):
    ver = shape.vertices
    lines = []
    for i in range(len(ver)):
        for j in range(i + 1, len(ver)):
            lines.append(GLine(ver[i], ver[j]))
    for l in lines:
        if point_to_line(c.center, l) < c.radius:
            return True
    return False


def is_inside(p, shape):
    vers = shape.vertices
    if isinstance(shape, GTriangle):
        b1 = sign(p, vers[0], vers[1]) < 0
        b2 = sign(p, vers[1], vers[2]) < 0
        b3 = sign(p, vers[2], vers[0]) < 0
        return (b1 == b2) and (b2 == b3)
    if isinstance(shape, GRectangle):
        return p.x > min(vers[0].x, vers[1].x) and (p.x < max(vers[0].x, vers[1].x)) and (p.y > min(vers[0].y, vers[
            1].y)) and p.y < max(vers[0].y, vers[1].y)
    if isinstance(shape, GCircle):
        if get_distance(p, shape.center)<= shape.radius:
            return True
        else:
            return False


# determine on which side of the line(p1,p2) is the point p
def sign(p, p1, p2):
    return (p.x - p2.x) * (p1.y - p2.y) - (p1.x - p2.x) * (p.y - p2.y)


# compute shortest distance from a point to a line segment
def point_to_line(point, line):
    p1 = line.vertices[0]
    p2 = line.vertices[1]
    if p1.x == p2.x:
        return abs(point.x - p1.x)
    k1 = (p1.y - p2.y) * 1.0 / (p1.x - p2.x)
    if k1 == 0:
        return abs(point.y - p1.y)
    k2 = -1.0 / k1
    b = point.y - k2 * point.x
    cross_point = compute_cross(GLine(point, GPoint(0, b)), line)
    if cross_point.x < max(p1.x, p2.x) and cross_point.x > min(p1.x, p2.x):
        return get_distance(point, cross_point)
    else:
        return min(get_distance(point, p1), get_distance(point, p2))
