

int a := 10

a := a + 1


int increment_a(int by) := 0
	a := a + by
end


int print_a() := 0
	print("a = " + str(a))
end

print_a()

a := a - 1

print_a()


increment_a(10)

print_a()

increment_a(-2)

print_a()

