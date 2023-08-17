#!/bin/dash

##### demo using shell features from subset 2
echo 'This program is' $0

lines=$1

echo 'The total number of lines is' ${lines}

if test ${lines} -lt 10
then
  echo "This is good"
else
  echo "This is bad, too many lines"
fi

line=1
while test ${line} != 111
do
  echo "you have to reduce lines"
done
