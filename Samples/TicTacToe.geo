string player1 := "FF0000"
string player2 := "00FF00"
string initColor := "FFFFFF"

int main() := 0
	Window window := createWindow("Tic Tac Toe", 350, 350)
	Table board := createTable(25, 25, 100, 100, 3, 3)	
	setColor(board, "FFFFFF")
	render(window, board)

	bool winner := false
	string currentPlayer := player1

	while (!winner)
		Point click := getMouse(window)

		if (!inside(click, board))
			printl("Click a cell please")
			continue
		end

		Rectangle cell := getCell(board, getX(click), getY(click))

		if (!canClick(click, cell))
			printl("Please click a cell that hasn't been clicked")
			continue
		end

		makeMove(cell, currentPlayer)
		
		if (checkWin(board))
			if (currentPlayer = player1)
				displayMessage("Player 1 wins!", window)
			el
				displayMessage("Player 2 wins!", window)
			end
			break
		end	
	
		if (currentPlayer = player1)
			currentPlayer := player2
		el
			currentPlayer := player1
		end

		if (!movesLeft(board))
			displayMessage("No moves left. Both are losers!", window)
			break
		end
	end
	getMouse(window)
end

bool checkWin(Table table) := win
	int row1 := 0
	int row2 := 1
	int row3 := 2

	int col1 := 0
	int col2 := 1
	int col3 := 2

	Rectangle cell1 := getACell(table, row1, col1)
	Rectangle cell2 := getACell(table, row1, col2)	
	Rectangle cell3 := getACell(table, row1, col3)

	if (checkCellsWin(cell1, cell2, cell3))
		win := true
		done
	end

	cell1 := getACell(table, row2, col1)	
	cell2 := getACell(table, row2, col2)	
	cell3 := getACell(table, row2, col3)	

	if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end


	cell1 := getACell(table, row3, col1)
        cell2 := getACell(table, row3, col2)
        cell3 := getACell(table, row3, col3)

	if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end


	//Cells
	cell1 := getACell(table, row1, col1)
        cell2 := getACell(table, row2, col1)
        cell3 := getACell(table, row3, col1)

        if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end


	cell1 := getACell(table, row1, col2)
        cell2 := getACell(table, row2, col2)
        cell3 := getACell(table, row3, col2)

        if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end



	cell1 := getACell(table, row1, col3)
        cell2 := getACell(table, row2, col3)
        cell3 := getACell(table, row3, col3)

        if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end


	//Diagonals
	cell1 := getACell(table, row1, col1)
        cell2 := getACell(table, row2, col2)
        cell3 := getACell(table, row3, col3)

        if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end


	cell1 := getACell(table, row1, col3)
        cell2 := getACell(table, row2, col2)
        cell3 := getACell(table, row3, col1)

        if (checkCellsWin(cell1, cell2, cell3))
                win := true
                done
        end
end


bool checkCellsWin(Rectangle cell1, Rectangle cell2, Rectangle cell3) := win
	if (initColor != getColor(cell1) && getColor(cell1) = getColor(cell2) && getColor(cell2) = getColor(cell3))
		win := true
	end
end


int makeMove(Rectangle cell, string player) := 0
	setColor(cell, player)
end


bool canClick(Point click, Rectangle cell) := valid
	if (getColor(cell) = "FFFFFF")
		valid := true
	el
		valid := false
	end
end


bool movesLeft(Table board) := left
	int i := 0
        int j := 0

        while (i < 3)
                j := 0
                while (j < 3)
                        Rectangle cell := getACell(board, i, j)
			if (getColor(cell) = initColor)
				left := true
				break
			end
                        j := j + 1
                end
                i := i + 1
        end
end

int displayMessage(string message, Window window) := 0
	Point p := createPoint(200, 10)
	Text msg := createText(p, message)
	render(window, msg)
end

main()
