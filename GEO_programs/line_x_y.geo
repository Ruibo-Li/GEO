/* Apply equation y = m*x + b
	for values of x ranging from 0 to 9 */
double x
double y

// Slope
double m := 3

// y-intercept
double b := 10



x := 0
print("x\ty");
while (x < 10)
	y := m*x + b
print(str(x) + "\t" + str(y))
	x := x + 1
end
