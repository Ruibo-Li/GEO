int start(Window win) := 1
    int i := 2
    while(i <= 6)
        Table table := createTable(100, 100, 300/i, 300/i, i, i)
        render(win, table)
  
        list int rgb 
        listAppend(rgb, randomInt(0,255))
        listAppend(rgb, randomInt(0,255))
        listAppend(rgb, randomInt(0,255))
        setColor(table, listGet(rgb,0), listGet(rgb,1), listGet(rgb,2))
        int changeInd := randomInt(0, 2)
        int tmp := listGet(rgb, changeInd) + 60/i
        if(tmp > 255)
            tmp := tmp - 120/i
        end
        listSet(rgb, changeInd, tmp)

        int cellInd := randomInt(0, i*i-1)
        setCellColor(table, cellInd / i, cellInd % i, listGet(rgb,0), listGet(rgb,1), listGet(rgb,2))

        Point p := getMouse(win)
        if(getRow(table, getX(p), getY(p)) * i + getCol(table, getX(p), getY(p)) != cellInd)
            printl("You lost")
            done
        end
        remove(table)
        i := i + 1
    end
    printl("You Win")
end

int main() := 1
    Window win := createWindow("Find Game", 500, 500)
    start(win)
end

main()
