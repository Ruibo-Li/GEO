// Test of program that appears in final report

/* Apply equation y = m * x + b
for values of x ranging from 0 t0 9 */

double x
double y

double m := 3

double b := 10

x:= 0

printl("x\ty")

while (x < 10)
        y := m * x + b
        printl(str(x) + "\t" + str(y))
        x := x + 1
end
