Window initialboard() := window
    window := createWindow("Battle Ship", 900, 500)
    Table table1 := createTable(100, 100, 30, 30, 10, 10)
    drawTable(table1, window)
    Table table2 := createTable(100, 100, 30, 30, 10, 10)
    drawTable(table2, window)    
