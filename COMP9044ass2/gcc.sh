#!/bin/dash

var=1

# if [ "(" $var -eq 1 ")" && "(" $var ")" ]
# then
#   echo "hello"
# fi

if [ "(" $var -eq 1 -a $var -eq 1 ")" ]
then 
  echo "hello"
fi

# if [ $var -eq 1 ] && [ $var -eq 1 ]
# then 
#   echo "hello"
# fi