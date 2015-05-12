
string circleColor := "FF0000"
string rectColor := "00FF00"
string triColor := "0000FF"

Text instr

int main() := 0
	Window window := createWindow("Demo", 600, 600)
	Table table := createTable(2, 0, 200, 200, 3, 1)


	Circle drawCircle := createCircle(createPoint(100,100), 50)
	setColor(drawCircle, circleColor)
	render(window, drawCircle)

	Rectangle drawRect := createRectangle(createPoint(25, 270), createPoint(180, 340))
	setColor(drawRect, rectColor)
	render(window, drawRect)

	Triangle drawTrig := createTriangle(createPoint(100, 420), createPoint(20, 560), createPoint(180, 560))
	setColor(drawTrig, triColor)
	render(window, drawTrig)

	render(window, table)

	instr := createText(createPoint(300, 5), "Pick a figure to draw")
	render(window, instr)

	while (true)
		displayMsg("Pick a figure to draw", window)
		Point click := getMouse(window)

		if (!inside(click, table))
			displayMsg("Please select a figure first", window)
			continue
		end

		Shape toDraw

		if (inside(click, drawTrig))
			toDraw := drawTriangle(window)
		ef (inside(click, drawCircle))
			toDraw := drawCirc(window)
		ef (inside(click, drawRect))
			toDraw := drawRectangle(window)
		el
			displayMsg("Please select a figure first", window)
                        continue
		end

		render(window, toDraw)
	end


	getMouse(window)
end


int displayMsg(string msg, Window window) := 0
	remove(instr)
	instr := createText(createPoint(300, 10), msg)
	render(window, instr)
end



Triangle drawTriangle(Window window) := triangle
	displayMsg("Click one vertext for the triangle", window)

	Point p1 := getMouse(window)

	displayMsg("Click the second vertext for the triangle", window)

	Point p2 := getMouse(window)

	displayMsg("Click the third for the triangle", window)

	Point p3 := getMouse(window)

	triangle := createTriangle(p1, p2, p3)

	setColor(triangle, triColor)
end

Circle drawCirc(Window window) := circle
	displayMsg("Click the center of the circle", window)
	Point p1 := getMouse(window)

	displayMsg("Click where the circle should pass by", window)
	Point p2 := getMouse(window)

	int radius := getDistance(p1, p2)

	circle := createCircle(p1, radius)

	setColor(circle, circleColor)
end

Rectangle drawRectangle(Window window) := rectangle
	displayMsg("Click one vertext of the rectangle", window)
	Point p1 := getMouse(window)

	displayMsg("Click the other vertext of the rectangle", window)
	Point p2 := getMouse(window)

	rectangle := createRectangle(p1, p2)

	setColor(rectangle, rectColor)
end

main()
