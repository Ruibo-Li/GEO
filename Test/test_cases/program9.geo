//This test checks different string builtin functions

string a := "this is"
string b := " a"
string c := a + b + " test  "

printf(c)
printl(c)

list string l1 := split(c, " ")

string d := strip(c, " ")

printl(d)

string e := replaceString(c, "test", "Test")

printl(e)


int f := findSubstring(c, "test")

printl("Substring: " + str(f))


string g := "12344"

bool h := isDigit(g)

bool i := isUpper(c)

bool j := isLower(c)

string k := lower(d)

printl(k)

string l := upper(c)

printl(l)


list string m    

listAppend(m, "hello")
listAppend(m, "world!")

string n := joinString(" ", m)

printl(n)
