import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
x_1 = 0.0
y_1 = 0.0
m_1 = float(3)
b_1 = float(10)
x_1 = float(0)
printl("x\ty")
while (x_1 < 10):
    y_1 = m_1 * x_1 + b_1
    printl(str(x_1) + "\t" + str(y_1))
    x_1 = x_1 + 1