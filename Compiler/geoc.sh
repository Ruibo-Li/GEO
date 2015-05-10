#!/bin/bash



base_dir=$(dirname "$(readlink  "$0")")

echo compiling $1

out="a.out"

if [ $# -eq 2 ]
then
	out=$2
fi

echo "#!/usr/bin/env python" > $out

echo >> $out
echo >> $out

python "$base_dir/compiler.py" $1 >> $out

chmod +x $out
