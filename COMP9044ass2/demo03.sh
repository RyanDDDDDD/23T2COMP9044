#!/bin/dash

##### demo using shell features from subset 3
echo "we have $# command line arguments"

echo "all arguments are $@"

echo "the current directory is `pwd`"

echo -n "How many lines in this program ? "
read lines

for n in 1 2 3
do
  for i in 4 5 6
  do
    echo "outer is $n, inner is $i"
  done
done