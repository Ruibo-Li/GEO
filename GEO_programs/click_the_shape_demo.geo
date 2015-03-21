/* This demo2 function renders a random figure of random size upon 
   receiving a mouse click and returns the current board. */

// Define function demo2() that returns a board
Window demo2() := board
    // Init and set board size in pixels
    board := Window(500, 500)
    while (true)
        int i := random(1, 4)
        int x := random(0, 600)
        int y := random(0, 100)
        int width := random(100, 300)
        int length := random(100, 300)
        Shape shape := null

        if (i = 1)
            shape := Rectangle(Point(x, y), Point(x + width, y + length))
        ef (i = 2)
            shape := Circle(Point(x, y), length)
        el
            shape := Triangle(Point(x, y), Point(x + width, y + length), 
                Point(x, y + length))
        end

        // Render the random figure and pause for user input
        render(board, shape)
        list coords := getMouse()
        // Prompt user input until a valid mouse click
        while (!in(shape, coords))
            coords := getMouse()
        end
        remove(board, shape)

    end
end
