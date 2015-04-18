from graphics import *
import math
from built_in_classes import *


def createWindow(width, height):
    return GraphWin(width, height)


def createTriangle(point1, point2, point3):
    return GTriangle(point1, point2, point3)


def createCircle(center, radius):
    return GCircle(center, radius)


def createPoint(x, y):
    return GPoint(x, y)


def createLine(point1, point2):
    return GLine(point1, point2)


def render(board, shape):
    shape.geo.draw(board)


def remove(shape, window):
    shape.geo.undraw(window)


def areAimilar(triangle1, triangle2):
    vertices1 = triangle1.vertices
    edges1 = list()
    edges1.append(getDistance(vertices1[0], vertices1[1]))
    edges1.append(getDistance(vertices1[1], vertices1[2]))
    edges1.append(getDistance(vertices1[0], vertices1[2]))
    edges1.sort()
    vertices2 = triangle2.vertices
    edges2 = list()
    edges2.append(getDistance(vertices2[0], vertices2[1]))
    edges2.append(getDistance(vertices2[1], vertices2[2]))
    edges2.append(getDistance(vertices2[0], vertices2[2]))
    edges2.sort()
    k0 = float(edges1[0]) / edges2[0]
    k1 = float(edges1[1]) / edges2[1]
    k2 = float(edges1[2]) / edges2[2]
    if abs(k0 - k1) < 1e-6 and abs(k0 - k2) < 1e-6:
        return True
    return False


def getDistance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def isVertical(line):
    vertices = line.vertices
    if vertices[0].x == vertices[1].x:
        return True
    return False


# compute the cross point of two lines
# returns None if parallel
# point might not be on the line segments
def cross(line1, line2):
    if isVertical(line1) and isVertical(line2):
        return None

    vertices1 = line1.vertices
    vertices2 = line2.vertices
    p1 = vertices1[0]
    p2 = vertices1[1]
    q1 = vertices2[0]
    q2 = vertices2[1]

    if isVertical(line1):
        k2 = (q1.x - q2.x) * 1.0 / (q1.y - q2.y)
        b = q1.y - k2 * q1.x
        c_y = k2 * p1.x + b
        return G_point(p1.x, c_y)
    if isVertical(line2):
        k1 = (p1.x - p2.x) * 1.0 / (p1.y - p2.y)
        b = p1.y - k1 * p1.x
        c_y = k1 * q1.x + b
        return G_point(q1.x, c_y)

    k1 = (p1.x - p2.x) * 1.0 / (p1.y - p2.y)
    k2 = (q1.x - q2.x) * 1.0 / (q1.y - q2.y)
    if abs(k1 - k2) < 1e-6:
        return None
    b1 = p1.y - k1 * p1.x
    b2 = q1.y - k2 * q1.x
    cross_x = (b2 - b1) * 1.0 / (k1 - k2)
    cross_y = k1 * cross_x + b1
    return G_point(cross_x, cross_y)


# compute shortest distance from a point to a line segment
def pointToLine(point, line):
    p1 = line.vertices[0]
    p2 = line.vertices[1]
    if p1.x == p2.x:
        return abs(point.x - p1.x)
    k1 = (p1.x - p2.x) * 1.0 / (p1.y - p2.y)
    if k1 == 0:
        return abs(point.y - p1.y)
    k2 = -1.0 / k1
    b = point.y - k2 * point.x
    cross_point = cross(G_line(point, G_point(0, b)), line)
    if (cross_point.x < max(p1.x, p2.x)) and cross_point.x > min(p1.x, p2.x):
        return getDistance(point, cross_point)
    else:
        return min(getDistance(point, p1), getDistance(point, p2))


# compute whether two shapes have intersection
def intersect(shape1, shape2):
    if isinstance(shape1, G_circle):
        if isinstance(shape2, G_circle):
            return circleIn(shape1, shape2)
        if isinstance(shape2, G_rectangle):
            return circleOthIn(shape1, shape2)
        if isinstance(shape2, G_triangle):
            return circleOthIn(shape1, shape2)
    if isinstance(shape1, G_rectangle):
        if isinstance(shape2, G_circle):
            return circleOthIn(shape2, shape1)
        if isinstance(shape2, G_rectangle):
            return rectangleIn(shape1, shape2)
        if isinstance(shape2, G_triangle):
            return triangleIn(shape2, shape1)
    if isinstance(shape1, G_triangle):
        if isinstance(shape2, G_circle):
            return circleOthIn(shape2, shape1)
        if isinstance(shape2, G_rectangle):
            return triangleIn(shape1, shape2)
        if isinstance(shape2, G_triangle):
            return triangleIn(shape1, shape2)


# whether two circles intersect
def circleIn(circle1, circle2):
    return getDistance(circle1.center, circle2.center) < (circle1.radius + circle2.radius)


# whether two rectangles intersect
def rectangleIn(rec1, rec2):
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
def triangleIn(tri1, tri2):
    ver1 = tri1.vertices
    ver2 = tri2.vertices
    if isinstance(tri2, G_rectangle):
        ver2.append(G_point(ver2[0].x, ver2[1].y))
        ver2.append(G_point(ver2[1].x, ver2[0].y))
    lines1 = []
    for i in range(len(ver1)):
        for j in range(i + 1, len(ver1)):
            l = G_line(ver1[i], ver1[j])
            lines1.append(l)
    lines2 = []
    for i in range(len(ver2)):
        for j in range(i + 1, len(ver2)):
            l = G_line(ver2[i], ver2[j])
            lines2.append(l)
    for l1 in lines1:
        for l2 in lines2:
            p = cross(l1, l2)
            vers = l1.vertices
            if p is not None and (p.x < max(vers[0].x, vers[1].x)) and p.x > min(vers[0].x, vers[1].x):
                return True

    if inside(ver1[0], tri2):
        return True
    if inside(ver2[0], tri1):
        return True
    return False


# c is a circle, shape could be a triangle or rectangle
def circleOthIn(c, shape):
    ver = shape.vertices
    lines = []
    for i in range(len(ver)):
        for j in range(i + 1, len(ver)):
            lines.append(G_line(ver[i], ver[j]))
    for l in lines:
        if pointToLine(c.center, l) < c.radius:
            return True
    return False


# determine whether a point p is inside a shape (either triangle or rectangle)
def inside(p, shape):
    vers = shape.vertices
    if isinstance(shape, G_triangle):
        b1 = sign(p, vers[0], vers[1]) < 0
        b2 = sign(p, vers[1], vers[2]) < 0
        b3 = sign(p, vers[2], vers[0]) < 0
        return (b1 == b2) and (b2 == b3)
    if isinstance(shape, G_rectangle):
        return p.x > min(vers[0].x, vers[1].x) and (p.x < max(vers[0].x, vers[1].x)) and (p.y > min(vers[0].y, vers[
            1].y)) and p.y < max(vers[0].y, vers[1].y)


# determine on which side of the line(p1,p2) is the point p
def sign(p, p1, p2):
    return (p.x - p2.x) * (p1.y - p2.y) - (p1.x - p2.x) * (p.y - p2.y)
