import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
def maximum(x_2, y_2):
    z_2 = 0
    if (x_2 >= y_2):
        z_2 = x_2
    else:
        x_2 = y_2
    return z_2