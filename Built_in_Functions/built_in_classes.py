from graphics import *
from built_in_functions_basic import *


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
        self.geo = Rectangle(point1.geo, point2.geo)
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
        super(GText, self).__init__()
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


class GTable(GShape):
    def __init__(self, px, py, l, h, m, n):
        super(GTable, self).__init__()
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

    def undrawTable(self):
        for cell in self.cells:
            cell.geo.undraw()

    def getRow(self, x, y):
        if x < self.px or x > self.px + self.colNum*self.cellLength or y < self.py or y > self.py \
                + self.rowNum*self.cellHeight:
            return -1
        return (y - self.py) / self.cellHeight

    def getCol(self, x, y):
        if x < self.px or x > self.px + self.colNum*self.cellLength or y < self.py or y > self.py \
                + self.rowNum*self.cellHeight:
            return -1
        return (x - self.px) / self.cellLength

    def getCell(self, x, y):
        row = self.getRow(x, y)
        col = self.getCol(x, y)
        if row != -1 and col != -1:
            return self.cells[row*self.colNum + col]
        return None

    def getVal(self, i, j):
        return self.cells[i*self.colNum + j].value

    def getColor(self, i, j):
        return self.cells[i*self.colNum + j].color

    def setColor(self, st):
        color = GColor(getR(st), getG(st), getB(st))
        for cell in self.cells:
            cell.color = color
            cell.geo.setFill(color.geo)

    def setCellColor(self, i, j, st):
        color = GColor(getR(st), getG(st), getB(st))
        self.cells[i*self.colNum + j].color = color
        self.cells[i*self.colNum + j].geo.setFill(color.geo)

    def hasSameColor(self, st):
        color = GColor(getR(st), getG(st), getB(st))
        for cell in self.cells:
            if cell.color != color:
                return False
        return True