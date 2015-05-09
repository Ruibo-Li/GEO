//This test is to test simple lists
list int list1
list int list2

listAppend(list1, 10)
listAppend(list1, 20)
listAppend(list2, 30)

listExtend(list1, list2)

int i := 0

while (i < 3)
        int b := listGet(list1, i)
        printl("list1[" + str(i) + "] = " + str(b))
        i := i + 1
end
