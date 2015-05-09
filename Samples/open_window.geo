bool gameOver(Table table) := won
	won := hasSameColor(table, "00BFFF")
end

int reverseColor(Rectangle cell) := 1
	if (getColor(cell) = "E0EEEE")
		setColor(cell, "00BFFF")
	el
		setColor(cell, "E0EEEE")
	end
end

int setNeighbors(Table table, int x, int y) := 1
	if (x > 100 && x < 400 && y > 100 && y < 400)
		reverseColor(getCell(table, x, y))
		if (x + 50 < 400)
			reverseColor(getCell(table, x + 50, y))
		end
		if (x - 50 > 100)
			reverseColor(getCell(table, x - 50, y))
		end
		if (y + 50 < 400)
			reverseColor(getCell(table, x, y + 50))
		end
		if (y - 50 > 100)
			reverseColor(getCell(table, x, y - 50))
		end
	el
		printl("Click one of the cells please!")	
	end
end

int main() := 1
	Window board := createWindow("Open Window Game", 500, 500)
	Table table := createTable(100, 100, 50, 50, 6, 6)
	setColor(table, "E0EEEE")
	render(board, table)
	bool won := false
	while (!won)
		Point click := getMouse(board)
		setNeighbors(table, getX(click), getY(click))
		won := gameOver(table)
	end
	printl("Congrats! You WON!")
end

main()
