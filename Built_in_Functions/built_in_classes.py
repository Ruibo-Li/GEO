class G_shape(object):
    def __init__(self):


class G_triangle(G_shape):
    def __init__(self, point1, point2, point3):
        super(G_triangle, self).__init__()
        vertices = [point1.geo, point2.geo, point3.geo]
        self.geo = Polygon(vertices)
	self.vertices = [point1, point2, point3]

    def draw(self, board):
        self.geo.draw(board)

    def get_triangle(self):
        return self.geo


class G_rectangle(G_shape):
    def __init__(self, point1, point2)
        super(G_rectangle, self).__init__()
        vertices = [point1.geo, point2.geo]
        self.geo = Rectangle(point1, point2)
	self.vertices = [point1, point2]

    def draw(self, board):
        self.geo.draw(board)

    def get_rectangle(self):
        return self.geo


class G_circle(G_shape):
    def __init__(self, center, radius):
        super(G_circle, self).__init__()
        self.geo = Circle(center.geo, radius)
	self.center = center
	self.radius = radius

    def draw(self, board):
        self.geo.draw(board)

    def get_circle(self):
        return self.geo


class G_point:
    def __init__(self, x, y):
        self.geo = Point(x, y)
        self.x = x
        self.y = y

    def draw(self, board):
        self.geo.draw(board)

    def get_point(self):
        return self.geo


class G_line:
    def __init__(self, Point1, Point2):
        vertices = [Point1.geo, Point2.geo]
        self.geo = Line(Point1.geo, Point2.geo)
        self.vertices = [Point1, Point2]

    def draw(self, board):
        self.geo.draw(board)

    def get_line(self):
        return self.geo

