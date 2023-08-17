#!/bin/dash

##### demo using shell features from subset 4
check=0

if [ $check -eq 0 ]
then
  var=1
  var2=2
  case $var in
    0)
      echo no arguments
      ;;
    1)
      case $var2 in
        2)
          echo two
          ;;
        *)
          echo other
          ;;
      esac
      echo one argument
      ;;
    2|3|4)
      echo some arguments
      ;;
    *)
      echo many arguments
      ;;
  esac
fi

# from assignment spec
date=$(date +%Y-%m-%d)

echo "The groups I am part of are $(groups $(whoami))"

x=6
y=7
echo $((x  + y)) >file
echo $((x  + y)) >>file

cat <file

test -w /dev/null && echo /dev/null is writeable
test -x /dev/null || echo /dev/null is not executable

if test -w /dev/null && test -x /dev/null
then
    echo /dev/null is writeable and executable
fi

if grep -Eq $(whoami) enrolments.tsv
then
    echo I am enrolled in COMP2041/9044
fi

