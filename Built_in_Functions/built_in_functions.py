import graphics
import math

class G_shape(object):
	def __init__(self):

class G_triangle (G_shape):
	def __init__(self, Point1, Point2, Point3):
		super(G_triangle, self).__init__()
		vertices = [Point1.geo, Point2.geo, Point3.geo]
		self.geo = Polygon(vertices)
		self.vertices = [Point1, Point2, Point3]
	def draw(self, board):
		self.geo.draw(board)
	def get_triangle(self):
		return self.geo

class G_rectangle(G_shape):
	def __init__(self, Point1, Point2):
		super(G_rectangle, self).__init__()
		vertices = [Point1.geo, Point2.geo]
		self.geo = Rectangle(Point1, Point2)
		self.vertices = [Point1, Point2]
	def draw(self, board):
		self.geo.draw(board)
	def get_rectangle(self):
		return self.geo

class G_circle(G_shape):
	def __init__(self, Center, Radius):
		super(G_circle, self).__init__()
		self.geo = Circle(Center.geo, Radius)
		self.center = Center
		self.radius = Radius
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
	edges1.append(get_distance(vertices[0],vertices[1]))
	edges1.append(get_distance(vertices[1],vertices[2]))
	edges1.append(get_distance(vertices[0],vertices[2]))
	edges1.sort()
	vertices2 = triangle2.vertices
	edges2 = []
	edges2.append(get_distance(vertices[0],vertices[1]))
	edges2.append(get_distance(vertices[1],vertices[2]))
	edges2.append(get_distance(vertices[0],vertices[2]))
	edges2.sort()
	k0 = float(edge1[0])/edges2[0]
	k1 = float(edge1[1])/edges2[1]
	k2 = float(edge1[2])/edges2[2]
	if abs(k0-k1)<1e-6 and abs(k0-k2)<1e-6:
		return True
	return False

def get_distance(Point1, Point2):
	return math.sqrt((Point1.x - Point2.x) ** 2 + (Point1.y - Point2.y) ** 2)

def is_vertical(line):
	vertices = line.vertices
	if vertices[0].x == vertices[1].x:
		return True
	return False

#compute the cross point of two lines
#returns None if parallel
#point might not be on the line segments
def cross(line1, line2):
	if is_vertical(line1) and is_vertical(line2):
		return None

	vertices1 = line1.vertices
	vertices2 = line2.vertices
	p1 = vertices1[0]
	p2 = vertices1[1]
	q1 = vertices2[0]
	q2 = vertices2[1]

	if is_vertical(line1):
		k2 = (q1.x - q2.x) * 1.0 / (q1.y - q2.y)
		b = q1.y - k2 * q1.x
		c_y = k2 * p1.x + b
		return Point(p1.x, c_y)
	if is_vertical(line2):
		k1 = (p1.x - p2.x) * 1.0 / (p1.y - p2.y)
		b = p1.y - k1 * p1.x
		c_y = k1 * q1.x + b
		return Point(q1.x, c_y) 
   	
	k1 = (p1.x - p2.x) * 1.0 / (p1.y - p2.y)
	k2 = (q1.x - q2.x) * 1.0 / (q1.y - q2.y)
	if abs(k1-k2) < 1e-6
		return None
	b1 = p1.y - k1 * p1.x
	b2 = q1.y - k2 * q1.x
	cross_x = (b2 - b1) * 1.0 / (k1 - k2)
	cross_y = k1 * cross_x + b1
	return G_point(cross_x, cross_y)
	

#compute shortest distance from a point to a line segment
def point_to_line(point, line):
	p1 = line.vertices[0]
	p2 = line.vertices[1]
	if p1.x == p2.x:
		return abs(point.x - p1.x)
	k1 = (p1.x - p2.x) * 1.0 / (p1.y - p2.y)
	if k1 == 0:
		return abs(point.y - p1.y)
	k2 = -1.0 / k1
	b = point.y - k2 * point.x
	cross_point = cross(G_line(point, G_point(0,b)), line)
	if on(cross_point, line):
		return get_distance(point, cross_point)
	else:
		return min(get_distance(point, p1), get_distance(point, p2))

#compute whether two shapes have intersection
def intersect(shape1, shape2):
	
	if isinstance(shape1, G_circle):
		if isinstance(shape2, G_circle):
			return circle_in(shape1, shape2)
		if isinstance(shape2, G_rectangle):
			return circle_oth_in(shape1, shape2)
		if isinstance(shape2, G_triangle):
			return circle_oth_in(shape1, shape2)
	if isinstance(shape1, G_rectangle):
		if isinstance(shape2, G_circle):
			return circle_oth_in(shape2, shape1)
		if isinstance(shape2, G_rectangle):
			return rectangle_in(shape1, shape2)
		if isinstance(shape2, G_triangle):
			return triangle_in(shape2, shape1)
	if isinstance(shape1, G_triangle):
		if isinstance(shape2, G_circle):
			return circle_oth_in(shape2, shape1)
		if isinstance(shape2, G_rectangle):
			return triangle_in(shape1, shape2)
		if isinstance(shape2, G_triangle):
			return triangle_in(shape1, shape2)

#whether two circles intersect
def circle_in(circle1, circle2):
	return get_distance(circle1.center, circle2.center) < (circle1.radius + circle2.radius)

#whether two rectangles intersect
def rectangle_in(rec1, rec2):
	vertices1 = rec1.vertices
	vertices2 = rec2.vertices
	p1 = vertices1[0]
	p2 = vertices1[1]
	q1 = vertices2[0]
	q2 = vertices2[1]
	if min(p1.x, p2.x) > max(q1.x, q2.x) or max(p1.x, p2.x) < min(q1.x, q2.x) 
			or min(p1.y, p2.y) > max(q1.y, q2.y) or max(p1.y, p2.y) < min(q1.y, p2.y):
		return False
	return True


#shape1 must be a triangle, shape2 could be a triangle or a rectangle
def triangle_in(shape1, shape2):
	ver1 = shape1.vertices
	ver2 = shape2.vertices
	if isinstance(shape2, G_rectangle):
		ver2.append(G_point(ver2[0].x, ver2[1].y))
		ver2.append(G_point(ver2[1].x, ver2[0].y))
	lines1 = []
	for i in range(len(ver1)):
		for j in range (i+1, len(ver1):
			l = G_line(ver1[i], ver1[j])
			lines1.append(l)
	lines2 = []
	for i in range(len(ver2)):
		for j in range (i+1, len(ver2)):
			l = G_line(ver2[i], ver2[j])
			lines2.append(l)
	for l1 in lines1:
		for l2 in lines2:
			p = cross(l1, l2)
			vers = l1.vertices
			if p is not None and p.x < max(vers[0].x, vers[1].x) and p.x > min (vers[0].x, vers[1].x):
				return True

	if inside(ver1[0], tri2):
		return True
	if inside(ver2[0], tri1):
		return True
	return False

#c is a circle, shape could be a triangle or rectangle
def circle_oth_in(c, shape):
	ver = shape.vertices
	lines = []
	for i in range(len(ver)):
		for j in range(i+1, len(ver)):
			lines.append(G_line(ver[i], ver[j]))
	for l in lines:
		if point_to_line(c.center, l) < c.radius:
			return True
	return False
	

#determine whether a point p is inside a shape (either triangle or rectangle)
def inside(p, shape):
	vers = shape.vertices
	if isinstance(shape, G_triangle):
		b1 = sign(p, vers[0], vers[1]) < 0
		b2 = sign(p, vers[1], vers[2]) < 0
		b3 = sign(p, vers[2], vers[0]) < 0
		return ((b1 == b2) && (b2 == b3))
	if isinstance(shape, G_rectangle):
		return p.x > min(vers[0].x, vers[1].x) and p.x < max(vers[0].x, vers[1].x)
			and p.y > min(vers[0].y, vers[1].y) and p.y < max(vers[0].y, vers[1].y)
#determine on which side of the line(p1,p2) is the point p
def sign(p, p1, p2):
	return (p.x - p2.x) * (p1.y - p2.y) - (p1.x - p2.x) * (p.y - p2.y)
