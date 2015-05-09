//This test is for built in functions of lists

list int list1
list int list2
listAppend(list1, 10)
listAppend(list1, 20)
listAppend(list2, 30)

listExtend(list1, list2)

listInsert(list1, 1, 10)

listRemove(list1, 1)

int n := listIndex(list1, 10)

int count := listCount(list1, 10)

listSort(list1)

listReverse(list1)

int x := listPop(list1)

//These are errors
//x := listPop(list3)
//listInsert(list1, 1, "error")
