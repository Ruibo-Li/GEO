import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
a_1 = 0


while (a_1 < 100):
    if a_1 % 2 == 0:
        a_1 = a_1 + 1
        continue
    printl("a = " + str(a_1))
    if (a_1 > 30):
        break
    a_1 = a_1 + 1

