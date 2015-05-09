Window window := createWindow("Window test", 500, 400)

Point p1 := createPoint(30, 100)
Point p2 := createPoint(100, 150)
Point p3 := createPoint(150, 130)
Point p4 := createPoint(400, 230)
Point p5 := createPoint(350, 330)
Point p6 := createPoint(10, 30)

Triangle triangle1 := createTriangle(p1, p2, p3)
Triangle triangle2 := createTriangle(p4, p5, p6)

Rectangle rect1 := createRectangle(p1, p3)
Rectangle rect2 := createRectangle(p5, p2)

Circle circ1 := createCircle(p3, 100)
Circle circ2 := createCircle(p1, 10)

Line line1 := createLine(p1, p5)
Line line2 := createLine(p3, p2)

Table table := createTable(10, 10, 10, 10, 10, 10)

Text text := createText(p3, "Hello world!")

render(window, triangle1)
getMouse(window)
render(window, triangle2)
getMouse(window)
render(window, rect1)
getMouse(window)
render(window, rect2)
getMouse(window)
render(window, circ1)
getMouse(window)
render(window, circ2)
getMouse(window)
render(window, line1)
getMouse(window)
render(window, line2)
getMouse(window)

render(window, table)
getMouse(window)

remove(table)
getMouse(window)
remove(line2)
getMouse(window)
remove(line1)
getMouse(window)



