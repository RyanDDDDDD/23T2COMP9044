#!/bin/dash

# variable comparision
var=0
while test $var -ne 3
do
  echo $var
  var=$((var + 1))
done

# condition is True
var=0
while true
do
  echo $var
  break
done

# using [] for condition test in while loop
var=0
while [ $var -ne 5 ]
do
  echo $var
  var=$((var + 1))
done

# nested while loop
var=0
while test $var -ne 3
do
  echo $var
  var=$((var + 1))
  var1=0
  while test $var1 -ne 3
  do
    echo $var1
    var1=$((var1 + 1))
  done
done