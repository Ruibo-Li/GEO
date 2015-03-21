int width := 500
int height := 500
int delta_r := 100
int radius := 250
int x_center := width / 2
int y_center := width / 2
Point center := Point(x_center, y_center)

int max_tries := 20
int tries = 0
int points := 0

board := Window(width, height)

Circle big_circle := Circle(center, radius)

radius := radius - delta_r
Circle medium_circle := Circle(center, radius)

radius := radius - delta_r
Circle small_circle := Circle(center, radius)

render(board, big_circle)
render(board, medium_circle)
render(board, small_circle)

while(tries < max_tries)
	Point click := getMouse()

	if (in(small_circle, click))
		points := points + 10
	ef (in(medium_circle, click))
		points := points+ 5
	ef (in(big_circle, click))
		points := points + 1
		
	tries := tries + 1	
end

float avg := points / tries

print ("Statistics:")
print ("Points: " + points)
print ("Tries: " + tries)
print("Point average: " + avg)

if (avg > 5)
	print ("Great job!")
end
