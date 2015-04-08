
int sum(int a, int b) := c
	c := a + b
end

int sub(int a, int b) := c
	c := a - b
end

int hello(int b) := hello(a)
	int a := 10
end

int main() := k
	int a := 10
	int b := 20
	print(str(a) + " + " + str(b) + " = " + str(sum(a, b)))
	print(str(a) + " - " + str(b) + " = " + str(sub(a, b)))
end


main()
