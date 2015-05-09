int width := 500
int height := 400

int my_rand(int min, int max) := num
        double rand := randomNum()

        rand := rand * (max - min) + min
        num := rand
end

Window my_window := createWindow("Hello world", width, height)


while (true)
	int x := my_rand(0, width)
	int y := my_rand(0, height)
	Point p1 := createPoint(x, y)

	x := my_rand(0, width)
        y := my_rand(0, height)
        Point p2 := createPoint(x, y)

	x := my_rand(0, width)
        y := my_rand(0, height)
        Point p3 := createPoint(x, y)

	int red := my_rand(0, 255)
	int green := my_rand(0, 255)
	int blue := my_rand(0, 255)

	Shape my_shape
	int rand := my_rand(0, 2)

	print("Rand: " + str(rand))

	if(rand = 0)
		my_shape := createTriangle(p1, p2, p3)
	ef(rand = 1)
		my_shape := createRectangle(p1, p2)
	el
		my_shape := createCircle(p1, my_rand(50, 200))
	end

	setColor(my_shape, red, green, blue)
	render(my_window, my_shape)

	bool clicked := false

	while (!clicked)
		Point click := getMouse(my_window)
		if (inside(click, my_shape))
			clicked := true
		end
	end

	remove(my_shape)
end


getMouse(my_window)
