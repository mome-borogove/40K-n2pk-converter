#!/bin/bash

if [ "$@"x == "x" ]
then
  DIRS="."
else
  DIRS=$@
fi

for file in `find $DIRS -name '*.N2PK'`
do
  TARGET_DIR=`echo $file | perl -pe 's/\/[^\/]*\.N2PK//'`
  ./unpack-n2pk.py $file $TARGET_DIR
done
