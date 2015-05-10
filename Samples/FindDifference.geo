Window win := createWindow("Find Game", 500, 500)
int i := 2
while(i <= 6)
    Table table := createTable(100, 100, 300/i, 300/i, i, i)
    render(win, table)
    list int rgb 
    listAppend(rgb, randomInt(0,255))
    listAppend(rgb, randomInt(0,255))
    listAppend(rgb, randomInt(0,255))
    setColor(table, RGB2Str(listGet(rgb,0), listGet(rgb,1), listGet(rgb,2)))
    int changeInd := randomInt(0, 2)
    int tmp := listGet(rgb, changeInd) + 60/i
    if(tmp > 255)
        tmp := tmp - 120/i
    end
    listSet(rgb, changeInd, tmp)
    int cellInd := randomInt(0, i*i-1)
    setCellColor(table, cellInd / i, cellInd % i, RGB2Str(listGet(rgb,0), listGet(rgb,1), listGet(rgb,2)))
    Point p := getMouse(win)
    while(getRow(table, getX(p), getY(p))<0 || getCol(table, getX(p), getY(p))<0)
        p := getMouse(win)
    end
    if(getRow(table, getX(p), getY(p)) * i + getCol(table, getX(p), getY(p)) != cellInd)
        Text text := createText(createPoint(250, 450),"You lost (Click to quit)")
        render(win, text)
        break
    end
    remove(table)
    i := i + 1
end
if(i = 7)
    Text text := createText(createPoint(250, 250),"You Win (Click to quit)")
    render(win, text)
end
getMouse(win)
