import graphics
import math

class G_triangle:
	def __init__(self, Point1, Point2, Point3):
		vertices = [Point1.geo, Point2.geo, Point3.geo]
		self.geo = Polygon(vertices)
		self.vertices = [Point1, Point2, Point3]

class G_rectangle:
	def __init__(self, Point1, Point2):
		vertices = [Point1.geo, Point2.geo]
		self.geo = Rectangle(Point1, Point2)
		self.vertices = [Point1, Point2]

class G_circle:
	def __init__(self, Center, Radius):
		self.geo = Circle(Center.geo, Radius)
		self.center = Center
		self.radius = Radius

class G_point:
	def __init__(self, x, y):
		self.geo = Point(x, y)
		self.x = x
		self.y = y

class G_line:
	def __init__(self, Point1, Point2):
		vertices = [Point1.geo, Point2.geo]
		self.geo = Line(Point1.geo, Point2.geo)
		self.vertices = [Point1, Point2]

def getMouse(board):
	board.getMouse()

def render(board, shape):
	shape.draw(board)

def remove(board, shape):
	

def Window(width, height):
	return GraphWin(width, height)

def AreSimilar(triangle1, triangle2):
	vertices1 = triangle1.vertices
	edges1 = []
	edges1.append(getDistance(vertices[0],vertices[1]))
	edges1.append(getDistance(vertices[1],vertices[2]))
	edges1.append(getDistance(vertices[0],vertices[2]))
	edges1.sort()
	vertices2 = triangle2.vertices
	edges2 = []
	edges2.append(getDistance(vertices[0],vertices[1]))
	edges2.append(getDistance(vertices[1],vertices[2]))
	edges2.append(getDistance(vertices[0],vertices[2]))
	edges2.sort()
	k0 = float(edge1[0])/edges2[0]
	k1 = float(edge1[1])/edges2[1]
	k2 = float(edge1[2])/edges2[2]
	if abs(k0-k1)<1e-6 and abs(k0-k2)<1e-6:
		return True
	return False

def getDistance(Point1, Point2):
	return math.sqrt((Point1.x - Point2.x) ** 2 + (Point1.y - Point2.y) ** 2)
