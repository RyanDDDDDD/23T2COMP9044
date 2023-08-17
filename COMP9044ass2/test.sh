#!/bin/dash

var=12
var2=1

if [ $var > $var2 ]
then
  echo ">"
fi

#!/bin/dash

echo "hello world" > "test0. txt"
echo "hello world" > "test1. txt"
echo "hello world" > test2.txt
echo "hello world" > 'test3.txt'
echo "hello world" >'test4.txt'
echo "hello world">'test5.txt'

echo "hello world 2" >> "test0. txt"
echo "hello world" >> "test1. txt"
echo "hello world" >> test2.txt
echo "hello world" >> 'test3.txt'
echo "hello world" >>'test4.txt'
echo "hello world">>'test5.txt'

a=123
if test "$a" -eq "$a"
then
    echo It is a number
fi

#!/bin/dash

var=aaaa
case $var in
    a)
        echo no arguments
        ;;
    [10]|w)
        echo one argument
        ;;
    2|3|4)
        echo some arguments
        ;;
    *)
        echo many arguments
        ;;
esac

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

#!/bin/dash
file=test.txt
number=1

echo $number >>$file
echo $number >file

echo $undefined # prints nothing
echo ${print} # same result

a='1a 2b'

for item in $a
do
    echo $item
done

x=6
y=7
echo $((x + y))
date=$(date +%Y-%m-%d)
echo $date
echo "The groups I am part of are $(groups $(whoami))"
echo "The groups I am part of are $(groups $(whoami) $(whoami))"
echo "The groups $(groups $(whoami)) I am part of are $(groups $(whoami))"
echo "The groups $(groups $(whoami)) I am part of are $(groups $(whoami) $(whoami))"

zid=z5351656
echo "The groups I am part of are $(groups $(whoami) $zid)"
echo "The groups I am part of are $(groups $(whoami) "$zid")"
echo "The groups I am part of are $(groups $(whoami) $(whoami) $zid)"
echo "The groups $(groups $(whoami) $zid) I am part of are $(groups $(whoami) $zid)"
echo "The groups $(groups $(whoami)) I am part of are $(groups $(whoami) $(whoami) $zid)"


if [ -d /dev/full ]
then
    echo "-d success"
fi
if [ -n /dev/full ]
then
    echo "-n success"
fi
if [ -z /dev/full ]
then
    echo "-z success"
fi
if [ -w /dev/full ]
then
    echo "-w success"
fi

if [ -r /dev/full ]
then
    echo "-r success"
fi

if [ -x /dev/full ]
then
    echo "-x success"
fi

if [ -d /dev/full ]
then
    echo "-d success"
fi

if [ -f /dev/full ]
then
    echo "-f success"
fi

if [ -e /dev/full ]
then
    echo "-e success"
fi

if [ -h /dev/full ]
then
    echo "-h success"
fi

if [ -L /dev/full ]
then
    echo "-L success"
fi

if [ -k /dev/full ]
then
    echo "-k success"
fi

if [ -s /dev/full ]
then
    echo "-s success"
fi

if [ -g /dev/full ]
then
    echo "-g success"
fi

if [ -u /dev/full ]
then
    echo "-u success"
fi

if [ -G /dev/full ]
then
    echo "-G success"
fi

if [ -O /dev/full ]
then
    echo "-O success"
fi

if [ -b /dev/full ]
then
    echo "-b success"
fi

if [ -c /dev/full ]
then
    echo "-c success"
fi

if [ -p /dev/full ]
then
    echo "-p success"
fi

if [ -S /dev/full ]
then
    echo "-S success"
fi

