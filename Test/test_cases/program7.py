import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Built_in_Functions.built_in import *
list1_1 = []
list2_1 = []
listAppend(list1_1, 10)
listAppend(list1_1, 20)
listAppend(list2_1, 30)
listExtend(list1_1, list2_1)
i_1 = 0
while (i_1 < 3):
    b_2 = listGet(list1_1, i_1)
    printl("list1[" + str(i_1) + "] = " + str(b_2))
    i_1 = i_1 + 1