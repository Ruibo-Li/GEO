Window initialboard() := window
    window := createWindow("Battle Ship", 900, 500)
    Table userTable := createTable(100, 100, 30, 30, 10, 10)
    drawTable(userTable, window)
    Table computerTable := createTable(500, 100, 30, 30, 10, 10)
    drawTable(computerTable, window)
end

int print_board(s,table) := 1
	string player := "Computer"
	if (s = "u")
		player := "User"
    end

	printl("The " + player + "'s board look like this: \n")

	printf(" ")
    int i := 1
	while(true)
	    printf("  " + str(i+1) + "  ")
	    i := i+1
	    if (i = 11)
	        break
	    end
	end
	printl("\n")

	int i := 0
	while(true)
	    if(i != 9)
            printf(str(i+1) + "  ")
        el
            printf(str(i+1) + " ")
        end   

        int j := 0
        while(true)
            if(getVal(table,i,j) != -1)
                printf(' ')
            ef(s = "u")
                printf(getVal(table,i,j))
            ef(s = "c")
                if(getVal(table,i,j) = 1 || getVal(table,i,j) = 2)
                    printf(getVal(table,i,j))
                el
                    printf(" ")
            end
            if(j!=9)
                printl(" | ")
            end
            if(j=10)
                break
        end
        printl("")
        if(i!=9)
            printl("   ----------------------------------------------------------")
        el
            printl("")
        end
	end
end


int make_move(table,x,y,win,u) := 1
	if(getVal(table,i,j) = -1)
		if(u = 'u')
			set
		el
			cir = Circle(Point(115+y*30,115+x*30),12)
		cir.draw(win)
		return "miss"
	elif board[x][y] == '*' or board[x][y] == '$':
		return "try again"
	else:
		if u == 'u':
			line = Line(Point(530+y*30,100+x*30),Point(500+y*30,130+x*30))
		else:
			line = Line(Point(130+y*30,100+x*30),Point(100+y*30,130+x*30))
		line.draw(win)
		return "hit"