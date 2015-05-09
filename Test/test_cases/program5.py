import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
a_1 = 10
while (a_1 < 500):
    if (a_1 < 100):
        printl("Less than 100")
    elif (a_1 < 200):
        printl("less than 200")
    elif (a_1 < 300):
        printl("less than 300")
    else:
        printl("more than 300")
    a_1 = a_1 + 1