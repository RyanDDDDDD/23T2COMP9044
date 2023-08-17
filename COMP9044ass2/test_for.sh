#!/bin/dash

# test for-loop in quote/unquoted cases
for char in a b c
do
  echo $char
done

for char in "a b c"
do
  echo $char
done

for char in 'a b c'
do
  echo $char
done

# looping list contain variable
var=1
var2=2

for char in $var $var2 a b c
do
  echo $char
done

for char in "$var $var2 a b c"
do
  echo $char
done

for char in '$var $var2 a b c'
do
  echo $char
done

# looping list contain globbing
for char in *
do
  echo $char
done

for char in "*"
do
  echo $char
done

# for char in '*'
do
  echo $char
done

# looping list can be mixed of quote/unquoted arguments
for char in "$var" '$var2' $var 'a b c'
do
  echo $char
done

# nested for-loop
for char in a b c
do
  for char2 in d e f
  do
    echo $char $char2
  done
done

