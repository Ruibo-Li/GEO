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
listInsert(list1_1, 1, 10)
listRemove(list1_1, 1)
n_1 = listIndex(list1_1, 10)
count_1 = listCount(list1_1, 10)
listSort(list1_1)
listReverse(list1_1)
x_1 = listPop(list1_1)