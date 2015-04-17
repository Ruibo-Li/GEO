// This test is for function

// Invoke built-in readTriangle() function to read points from command line
Triangle t1 := readTriangle()
Triangle t2 := readTriangle()

// Define function demo1() that returns a boolean value res
bool demo1(Triangle t1, Triangle t2) := res
	res := areSimilar(t1, t2)
end