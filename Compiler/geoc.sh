#!/bin/bash


echo compiling $1

out="a.out"

if [ $# -eq 2 ]
then
	out=$2
fi

echo "#!/usr/bin/env python" > $out

echo >> $out
echo >> $out

python compiler.py $1 >> $out

chmod +x $out
