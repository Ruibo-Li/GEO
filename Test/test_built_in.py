import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in_functions import *


def main():
    # test Window
    board = GraphWin("test", 1000, 1000)

    # test Point
    point = createPoint(5, 5)
    render(board, point)

    # test Triangle
    p21 = createPoint(5, 10)
    p22 = createPoint(10, 10)
    p23 = createPoint(8, 15)
    tr1 = createTriangle(p21, p22, p23)
    render(board, tr1)

    # test Circle
    p31 = createPoint(5, 10)
    circle = createCircle(p31, 20)
    render(board, circle)

    # test Line
    p41 = createPoint(6, 7)
    p42 = createPoint(10, 12)
    line = createLine(p41, p42)
    render(board, line)

    # test render
    p51 = createPoint(50, 50)
    render(board, p51)

    # test remove
    remove(p51)

    # areSimilar
    tr2 = createTriangle(p21, p22, p23)
    assert(areSimilar(tr1, tr2))

    # areSimilar
    assert(intersect(tr1, tr2))

    board.getMouse()


main()