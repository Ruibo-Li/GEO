import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
def sum(a_2, b_2):
    c_2 = 0
    c_2 = a_2 + b_2
    return c_2
def sub(a_2, b_2):
    c_2 = 0
    c_2 = a_2 - b_2
    return c_2
def hello(b_2):
    a_2 = 0
    a_2 = 10
    return a_2
def main():
    k_2 = 0
    a_2 = 10
    b_2 = 20
    printl(str(a_2) + " + " + str(b_2) + " = " + str(sum(a_2, b_2)))
    printl(str(a_2) + " - " + str(b_2) + " = " + str(sub(a_2, b_2)))
    return k_2
main()