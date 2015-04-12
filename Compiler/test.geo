int factorial(int n) := x
        if(n = 0 || n = 1)
                x := 1
        el
                x := n * factorial(n - 1)
        end
end

int main() := y
        int n := 5

        print("Factorial of " + str(n) + ": " + str(factorial(n)))
end

main()
