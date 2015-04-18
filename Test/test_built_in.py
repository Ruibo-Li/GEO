import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in_functions import *


def main():
    # test Window
    Window(100, 100)

    # test render
    Board board = createBoard()
    Shape shape = createShape()
    render(board, shape)
