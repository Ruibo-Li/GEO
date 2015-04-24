from built_in_resource import *


def createWindow(title, width, height):
    return GraphWin(title, width, height)


def createTriangle(point1, point2, point3):
    return GTriangle(point1, point2, point3)


def createCircle(center, radius):
    return GCircle(center, radius)


def createPoint(x, y):
    return GPoint(x, y)


def createLine(point1, point2):
    return GLine(point1, point2)


def render(window, shape):
    shape.geo.draw(window)


def remove(shape):
    shape.geo.undraw()


def areSimilar(triangle1, triangle2):
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
    return is_vertical(line)


# compute the cross point of two lines
# returns None if parallel
# point might not be on the line segments
def cross(line1, line2):
    return compute_cross(line1, line2)


# compute shortest distance from a point to a line segment
def pointToLine(point, line):
    return point_to_line(point, line)


# compute whether two shapes have intersection
def intersect(shape1, shape2):
    if isinstance(shape1, GCircle):
        if isinstance(shape2, GCircle):
            return circle_in(shape1, shape2)
        if isinstance(shape2, GRectangle):
            return circle_oth_in(shape1, shape2)
        if isinstance(shape2, GTriangle):
            return circle_oth_in(shape1, shape2)
    if isinstance(shape1, GRectangle):
        if isinstance(shape2, GCircle):
            return circle_oth_in(shape2, shape1)
        if isinstance(shape2, GRectangle):
            return rectangle_in(shape1, shape2)
        if isinstance(shape2, GTriangle):
            return triangle_in(shape2, shape1)
    if isinstance(shape1, GTriangle):
        if isinstance(shape2, GCircle):
            return circle_oth_in(shape2, shape1)
        if isinstance(shape2, GRectangle):
            return triangle_in(shape1, shape2)
        if isinstance(shape2, GTriangle):
            return triangle_in(shape1, shape2)


# determine whether a point p is inside a shape (either triangle or rectangle)
def inside(p, shape):
    return is_inside(p, shape)


# cast shape to triangle
def shape_to_triangle(shape):
    if isinstance(shape, GCircle):
        return GTriangle(shape)
