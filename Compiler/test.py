import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
width_1 = 500
height_1 = 400
def my_rand(min_2, max_2):
    num_2 = 0
    rand_2 = randomNum()
    rand_2 = rand_2 * (max_2 - min_2) + min_2
    num_2 = int(rand_2)
    return num_2
my_window_1 = createWindow("Hello world", width_1, height_1)
while True:
    x_2 = my_rand(0, width_1)
    y_2 = my_rand(0, height_1)
    p1_2 = createPoint(x_2, y_2)
    x_2 = my_rand(0, width_1)
    y_2 = my_rand(0, height_1)
    p2_2 = createPoint(x_2, y_2)
    x_2 = my_rand(0, width_1)
    y_2 = my_rand(0, height_1)
    p3_2 = createPoint(x_2, y_2)
    red_2 = my_rand(0, 255)
    green_2 = my_rand(0, 255)
    blue_2 = my_rand(0, 255)
    my_shape_2 = None
    rand_2 = my_rand(0, 2)
    print("Rand: " + str(rand_2))
    if rand_2 == 0:
        my_shape_2 = createTriangle(p1_2, p2_2, p3_2)
    elif rand_2 == 1:
        my_shape_2 = createRectangle(p1_2, p2_2)
    else:
        my_shape_2 = createCircle(p1_2, my_rand(50, 200))
    setColor(my_shape_2, red_2, green_2, blue_2)
    render(my_window_1, my_shape_2)
    clicked_2 = False
    while  not clicked_2:
        click_3 = getMouse(my_window_1)
        if inside(click_3, my_shape_2):
            clicked_2 = True
    remove(my_shape_2)
getMouse(my_window_1)