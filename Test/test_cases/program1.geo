int sum(int a, int b) := c
        c := a + b
end

int sub(int a, int b) := c
        c := a - b
end

int hello(int b) := a
        a := 10 
end

int main() := k
        int a := 10
        int b := 20
        printl(str(a) + " + " + str(b) + " = " + str(sum(a, b)))
        printl(str(a) + " - " + str(b) + " = " + str(sub(a, b)))
end

main()