import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
def factorial(n_2):
    x_2 = 0
    if n_2 == 0 or n_2 == 1:
        x_2 = 1
    else:
        x_2 = n_2 * factorial(n_2 - 1)
    return x_2
def main():
    y_2 = 0
    n_2 = 5
    printl("Factorial of " + str(n_2) + ": " + str(factorial(n_2)))
    return y_2
main()