#!/usr/bin/env bash

rm -fr *_actual.py

for i in {1..10}
    do
        program="program$i.geo"
        benchmark="program$i.py"
        actual="program""$i""_actual.py"
        python ../lex_yacc.py $program > $actual
        if cmp -s $benchmark $actual
        then
	        echo "test$i passes"
	        rm -rf actual
        else
	        echo "test$i fails"

	        echo "Reason:"
	        diff $benchmark $actual
        fi
        echo "-----------------------------------------"
    done
