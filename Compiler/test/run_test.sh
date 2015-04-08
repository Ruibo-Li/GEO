#!/usr/bin/env bash


for i in {1..3}
    do
        program="program$i.geo"
        benchmark="program$i.py"
        actual="program""$i""_actual.py"
	echo $actual
        python ../lex_yacc.py $program > $actual
        if cmp -s benchmark actual
        then
	        echo "test$i passes"
	        rm -rf actual
        else
	        echo "test$i fails"
        fi
    done
