import graphics

class G_triangle:
	def __init__(self, Point1, Point2, Point3):
		vertices = [Point1, Point2, Point3]
		self.geo = Polygon(vertices)
		self.vertices = vertices

def getMouse(board):
	board.getMouse()

def render(board, shape):
	shape.draw(board)

def remove(board, shape):
	

def Window(width, height):
	return GraphWin(width, height)

def Rectangle(Point1, Point2):
	return Rectangle(Point1, Point2)

def G_triangle(Point1, Point2, Point3):
	triangle = G_triangle(Point1, Point2, Point3)
	return triangle

def Circle(Center, Radius):
	return Circle(Center, Radius)

def Point(x, y):
	return Point(x, y)

def Line(Point1, Point2):
	return Line(Point1, Point2)