Table table


Window initializeGameBoard(int length, int width) := board
	board := createWindow("Open Window Game", length, width)
	table := createTable(100, 100, 50, 50, 6, 6)
	setColor(table, 255, 255, 0)
	render(board, table)
end


bool gameOver(Table table) := won
	won := hasSameColor(table, 0, 0, 255)
end

int main() := 1
	Window board := initializeGameBoard(500, 500)
	while (!gameOver(table))
		Point click := getMouse(board)
		setColor(getCell(table, getX(click), getY(click)), 0, 0, 255)
	end
end

main()
