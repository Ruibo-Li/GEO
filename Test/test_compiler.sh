#!/usr/bin/env bash

rm -fr test_cases/*_actual.py

echo "-----------------------------------------"
for i in {1..10}
    do
        program="test_cases/program$i.geo"
        benchmark="test_cases/program$i.py"
        actual="test_cases/program""$i""_actual.py"
        python ../Compiler/compiler.py $program > $actual
        if cmp -s $benchmark $actual
        then
	        echo "test$i passes"
	        rm -fr $actual
        else
	        echo "test$i fails"

	        echo "Reason:"
	        diff $benchmark $actual
        fi
        echo "-----------------------------------------"
    done
