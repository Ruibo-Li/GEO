import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
def main():
    k_2 = 0
    a_2 = 10
    b_2 = 20
    while (b_2 > 0):
        a_3 = 20
        print("a = " + str(a_3))
        b_2 = b_2 - 1
        a_3 = a_3 + 1
        if b_2 % 2 == 1:
            b_4 = 100
            a_4 = 5000
            printl("b = " + str(b_4))
            printl("a = " + str(a_4))
    printl("a = " + str(a_2))
    return k_2
main()