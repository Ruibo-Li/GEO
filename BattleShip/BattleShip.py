import copy, random
from graphics import *

def initialboard():
    window = GraphWin("Battle Ship", 900, 500)
    for i in xrange(11):
        Line(Point(100 + 30 * i, 100), Point(100 + 30 * i, 400)).draw(window)
        Line(Point(500 + 30 * i, 100), Point(500 + 30 * i, 400)).draw(window)
        Line(Point(100, 100 + 30 * i), Point(400, 100 + 30 * i)).draw(window)
        Line(Point(500, 100 + 30 * i), Point(800, 100 + 30 * i)).draw(window)
    return window

def print_board(s,board):

	# WARNING: This function was crafted with a lot of attention. Please be aware that any
	#          modifications to this function will result in a poor output of the board 
	#          layout. You have been warn. 

	#find out if you are printing the computer or user board
	player = "Computer"
	if s == "u":
		player = "User"
	
	print "The " + player + "'s board look like this: \n"

	#print the horizontal numbers
	print " ",
	for i in range(10):
		print "  " + str(i+1) + "  ",
	print "\n"

	for i in range(10):
	
		#print the vertical line number
		if i != 9: 
			print str(i+1) + "  ",
		else:
			print str(i+1) + " ",

		#print the board values, and cell dividers
		for j in range(10):
			if board[i][j] == -1:
				print ' ',	
			elif s == "u":
				print board[i][j],
			elif s == "c":
				if board[i][j] == "*" or board[i][j] == "$":
					print board[i][j],
				else:
					print " ",
			
			if j != 9:
				print " | ",
		print
		
		#print a horizontal line
		if i != 9:
			print "   ----------------------------------------------------------"
		else: 
			print 

def user_place_ships(board,ships,win):

	for ship in ships.keys():

		#get coordinates from user and vlidate the postion
		valid = False
		while(not valid):
			print_board("u",board)
			print "Placing a/an " + ship
			x,y = get_coor(win,'l')
			ori = v_or_h()
			valid = validate(board,ships[ship],x,y,ori)
			if not valid:
				print "Cannot place a ship there.\nPlease take a look at the board and try again."

		#place the ship
		board = place_ship(board,ships[ship],ship[0],ori,x,y,win,'u')
		print_board("u",board)

	return board


def computer_place_ships(board,ships,win):

	for ship in ships.keys():
	
		#genreate random coordinates and vlidate the postion
		valid = False
		while(not valid):

			x = random.randint(1,10)-1
			y = random.randint(1,10)-1
			o = random.randint(0,1)
			if o == 0: 
				ori = "v"
			else:
				ori = "h"
			valid = validate(board,ships[ship],x,y,ori)

		#place the ship
		print "Computer placing a/an " + ship
		board = place_ship(board,ships[ship],ship[0],ori,x,y,win,'c')
	
	return board


def place_ship(board,ship,s,ori,x,y,win,u):

	#place ship based on orientation
	if ori == "v":
		x0 = 100+30*y
		y0 = 100+30*x
		for i in range(ship):
			board[x+i][y] = s
			if u == 'u':
				line = Line(Point(x0,y0+i*30),Point(x0+30,y0+i*30+30))
				line.draw(win)

	elif ori == "h":
		x0 = 100+30*y
		y0 = 100+30*x		
		for i in range(ship):
			board[x][y+i] = s
			if u == 'u':
				line = Line(Point(x0+i*30,y0),Point(x0+i*30+30,y0+30))
				line.draw(win)

	return board
	
def validate(board,ship,x,y,ori):

	#validate the ship can be placed at given coordinates
	if ori == "v" and x+ship > 10:
		return False
	elif ori == "h" and y+ship > 10:
		return False
	else:
		if ori == "v":
			for i in range(ship):
				if board[x+i][y] != -1:
					return False
		elif ori == "h":
			for i in range(ship):
				if board[x][y+i] != -1:
					return False
		
	return True

def v_or_h():
    user_input = None
    direction = GraphWin("Horizontal or Vertical", 350, 100)
    Rectangle(Point(50, 25), Point(150, 75)).draw(direction)
    Rectangle(Point(200, 25), Point(300, 75)).draw(direction)
    Text(Point(100, 50), 'Horizontal').draw(direction)
    Text(Point(250, 50), 'Vertical').draw(direction)
    while not user_input:
        click = direction.getMouse()
        x, y = click.getX(), click.getY()
        if 25 < y < 75:
            if 50 < x < 150:
                user_input = 'h'
            elif 200 < x < 300:
                user_input = 'v'
    direction.close()
    return user_input

def get_coor(window,flag):

    while True:
        click = window.getMouse()
        try:
            #see that user entered 2 values seprated by comma
            coor = [-1, -1]

            #check that 2 values are integers
            x = click.getX()
            y = click.getY()

            count = 0
            for i in xrange(100, 400, 30):
                if (flag == 'l' and i < x < i + 30) or (flag == 'r' and i + 400 < x < i + 430):
                    coor[1] = count
                    break
                count = count + 1

            count = 0
            for i in xrange(100, 400, 30):
                if i < y < i + 30:
                    coor[0] = count
                    break
                count = count + 1

            #check that values of integers are between 1 and 10 for both coordinates
            if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
                raise Exception("Invalid entry. Please use values between 1 to 10 only.")

            #if everything is ok, return coordinates
            return coor
        
        except ValueError:
            print "Invalid entry. Please enter only numeric values for coordinates"
        except Exception as e:
            print e

def make_move(board,x,y,win,u):
	
	#make a move on the board and return the result, hit, miss or try again for repeat hit
	if board[x][y] == -1:
		if u == 'u':
			cir = Circle(Point(515+y*30,115+x*30),12)
		else:
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

def user_move(board,win):
	
	#get coordinates from the user and try to make move
	#if move is a hit, check ship sunk and win condition
	while(True):
		x,y = get_coor(win,'r')
		res = make_move(board,x,y,win,'u')
		if res == "hit":
			print "Hit at " + str(x+1) + "," + str(y+1)
			check_sink(board,x,y)
			board[x][y] = '$'
			if check_win(board):
				return "WIN"
		elif res == "miss":
			print "Sorry, " + str(x+1) + "," + str(y+1) + " is a miss."
			board[x][y] = "*"
		elif res == "try again":
			print "Sorry, that coordinate was already hit. Please try again"	

		if res != "try again":
			return board

def computer_move(board,win):
	
	#generate user coordinates from the user and try to make move
	#if move is a hit, check ship sunk and win condition
	while(True):
		x = random.randint(1,10)-1
		y = random.randint(1,10)-1
		res = make_move(board,x,y,win,'c')
		if res == "hit":
			print "Hit at " + str(x+1) + "," + str(y+1)
			check_sink(board,x,y)
			board[x][y] = '$'
			if check_win(board):
				return "WIN"
		elif res == "miss":
			print "Sorry, " + str(x+1) + "," + str(y+1) + " is a miss."
			board[x][y] = "*"

		if res != "try again":
			
			return board
	
def check_sink(board,x,y):

	#figure out what ship was hit
	if board[x][y] == "A":
		ship = "Aircraft Carrier"
	elif board[x][y] == "B":
		ship = "Battleship"
	elif board[x][y] == "S":
		ship = "Submarine" 
	elif board[x][y] == "D":
		ship = "Destroyer"
	elif board[x][y] == "P": 
		ship = "Patrol Boat"
	
	#mark cell as hit and check if sunk
	board[-1][ship] -= 1
	if board[-1][ship] == 0:
		print ship + " Sunk"
		

def check_win(board):
	
	#simple for loop to check all cells in 2d board
	#if any cell contains a char that is not a hit or a miss return false
	for i in range(10):
		for j in range(10):
			if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
				return False
	return True

def start_game():
    start_window = GraphWin('Start Game', 100, 50)
    Rectangle(Point(20, 15), Point(80, 35)).draw(start_window)
    Text(Point(50, 25), 'Start').draw(start_window)
    click = start_window.getMouse()
    x, y = click.getX(), click.getY()
    while not (20 < x < 80 and 15 < y < 35):
        click = start_window.getMouse()
        x, y = click.getX(), click.getY()
    start_window.close()
    print 'Game started. Good luck!'

def main():
	win = initialboard()
	#types of ships
	ships = {"Aircraft Carrier":5,
		     "Battleship":4,
 		     "Submarine":3,
		     "Destroyer":3,
		     "Patrol Boat":2}

	#setup blank 10x10 board
	board = []
	for i in range(10):
		board_row = []
		for j in range(10):
			board_row.append(-1)
		board.append(board_row)

	#setup user and computer boards
	user_board = copy.deepcopy(board)
	comp_board = copy.deepcopy(board)

	#add ships as last element in the array
	user_board.append(copy.deepcopy(ships))
	comp_board.append(copy.deepcopy(ships))

	#ship placement
	user_board = user_place_ships(user_board,ships,win)
	comp_board = computer_place_ships(comp_board,ships,win)
	start_game()

	#game main loop
	while(1):
		#user move
		print_board("c",comp_board)
		comp_board = user_move(comp_board,win)

		#check if user won
		if comp_board == "WIN":
			print "User WON! :)"
			quit()
			
		#display current computer board
		print_board("c",comp_board)

		#computer move
		user_board = computer_move(user_board,win)
		
		#check if computer move
		if user_board == "WIN":
			print "Computer WON! :("
			quit()
			
		#display user board
		print_board("u",user_board)
	
if __name__=="__main__":
	main()
