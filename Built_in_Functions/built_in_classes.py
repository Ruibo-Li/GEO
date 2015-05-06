from graphics import *


class GShape(object):
    def __init__(self):
        self.geo = None


class GTriangle(GShape):
    def __init__(self, point1, point2, point3):
        super(GTriangle, self).__init__()
        vertices = [point1.geo, point2.geo, point3.geo]
        self.geo = Polygon(vertices)
        self.vertices = [point1, point2, point3]

    def get_triangle(self):
        return self.geo


class GRectangle(GShape):
    def __init__(self, point1, point2):
        super(GRectangle, self).__init__()
        vertices = [point1.geo, point2.geo]
        self.geo = Rectangle(point1, point2)
        self.vertices = [point1, point2]

    def get_rectangle(self):
        return self.geo


class GCircle(GShape):
    def __init__(self, center, radius):
        super(GCircle, self).__init__()
        self.geo = Circle(center.geo, radius)
        self.center = center
        self.radius = radius

    def get_circle(self):
        return self.geo


class GText(GShape):
    def __init__(self, point, text):
        super(GPoint, self).__init__()
        self.geo = Text(point.geo, text)

    def get_text(self):
        return self.geo


class GPoint(GShape):
    def __init__(self, x, y):
        super(GPoint, self).__init__()
        self.geo = Point(x, y)
        self.x = x
        self.y = y

    def get_point(self):
        return self.geo


class GLine(GShape):
    def __init__(self, point1, point2):
        super(GLine, self).__init__()
        vertices = [point1.geo, point2.geo]
        self.geo = Line(point1.geo, point2.geo)
        self.vertices = [point1, point2]

    def get_line(self):
        return self.geo


class Table:
    def __init__(self, px, py, l, h, m, n):
        self.px = px
        self.py = py
        self.cellLength = l
        self.cellHeight = h
        self.rowNum = m
        self.colNum = n

    def drawTable(self, window):
        tablelength = self.cellLength * self.colNum
        tableheight = self.cellHeight * self.rowNum
        for i in xrange(self.rowNum+1):
            Line(Point(self.px, self.py + i * self.cellHeight), Point(self.px + tablelength, self.py + i * self.cellHeight)).draw(window)
        for i in xrange(self.colNum+1):
            Line(Point(self.px + i * self.cellLength, self.py), Point(self.px + i * self.cellLength, self.py + tableheight)).draw(window)

    def getRowNum(self, x, y):
        return (y - self.py) / self.cellHeight

    def getColNum(self, x, y):
        return (x - self.px) / self.cellLength