from graphics import *


class GShape(object):
    def __init__(self):
        self.geo = None
        self.value = 0


class GTriangle(GShape):
    def __init__(self, point1, point2, point3):
        super(GTriangle, self).__init__()
        vertices = [point1.geo, point2.geo, point3.geo]
        self.geo = Polygon(vertices)
        self.vertices = [point1, point2, point3]
        self.color = None

    def get_triangle(self):
        return self.geo


class GRectangle(GShape):
    def __init__(self, point1, point2):
        super(GRectangle, self).__init__()
        vertices = [point1.geo, point2.geo]
        self.geo = Rectangle(point1, point2)
        self.vertices = [point1, point2]
        self.color = None

    def get_rectangle(self):
        return self.geo


class GCircle(GShape):
    def __init__(self, center, radius):
        super(GCircle, self).__init__()
        self.geo = Circle(center.geo, radius)
        self.center = center
        self.radius = radius
        self.color = None

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


class GColor():
    def __init__(self, r, g, b):
        self.geo = color_rgb(r, g, b)
        self.r = r
        self.g = g
        self.b = b

    def get_color(self):
        return self.r, self.g, self.b


class Table(GShape):
    def __init__(self, px, py, l, h, m, n):
        self.px = px
        self.py = py
        self.cellLength = l
        self.cellHeight = h
        self.rowNum = m
        self.colNum = n
        self.cells = []
        for i in xrange(m):
            for j in xrange(n):
                lux = px + j * l
                luy = py + i * h
                newcell = GRectangle(GPoint(lux, luy), GPoint(lux + l, luy + h))
                self.cells.append(newcell)

    def drawTable(self, window):
        for cell in self.cells:
            cell.geo.draw(window)

    def getRow(self, x, y):
        return (x - self.px) / self.cellLength

    def getCol(self, x, y):
        return (y - self.py) / self.cellHeight

    def getCell(self, x, y):
        row = self.getRow(x, y)
        col = self.getCol(x, y)
        self.cells[row*self.colNum + col]
        return (y - self.py) / self.cellHeight

    def getVal(self, i, j):
        return (y - self.py) / self.cellHeight