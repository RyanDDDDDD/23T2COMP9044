#!/bin/dash

echo hello world
echo 42 is the meaning of life, the universe, and everything
echo To be or not to be: that is the question

# ==================
x=1
y=2
foo=hello
bar=world
course_code=COMP2041
AssignmentName=Sheepy

# ==================
theAnswer=42
echo The meaning of life, the universe, and everything is $theAnswer

name=COMP2041
echo I hope you are enjoying $name this semester

H=Hello
W=World
echo $H, $W

P1=race
P2=car
palindrome=$P1$P2
echo $palindrome

# ==================

echo *

C_files=*.[ch]
echo $C_files

echo all of the single letter Python files are: ?.py

# ===================

for i in 1 2 3
do
    echo $i
done

for word in this is a string
do
    echo $word
done

for file in *.c *.c
do
    echo $file
done

# ===================
# echo hello world
# exit
# echo this will not be printed
# exit 0
# echo this will double not be printed
# exit 3

# ===================
# echo *
# cd /tmp
# echo *
# cd ..
# echo *

# ===================
# echo What is your name:
# read name

# echo What is your quest:
# read quest

# echo What is your favourite colour:
# read colour

# echo What is the airspeed velocity of an unladen swallow:
# read velocity

# echo Hello $name, my favourite colour is $colour too.
# ===================
touch test_file.txt
ls -l test_file.txt

for course in COMP1511 COMP1521 COMP2511 COMP2521 # keyword
do                                                # keyword
    echo $course                                  # builtin
    mkdir $course                                 # external command
    chmod 700 $course                             # external command
done 
# ===================

# echo This program is: $0

file_name=$2
number_of_lines=$5

echo going to print the first $number_of_lines lines of $file_name
# ===================
string=BAR
echo FOO${string}BAZ
# ===================

if test -w /dev/null
then
    echo /dev/null is writeable
fi

# ===================
row=1
while test $row != 11111111111
do
    echo $row
    row=1$row
done
# ===================

echo 'hello    world'

echo 'This is not a $variable'

echo 'This is not a glob *.sh'
# ===================
echo "hello    world"

echo "This is sill a $variable"

echo "This is not a glob *.sh"
# ===================
date=`date +%Y-%m-%d`

echo Hello `whoami`, today is $date

echo "command substitution still works in double quotes: `hostname`"

echo 'command substitution does not work in single quotes: `not a command`'
# ===================
# echo -n "How many? "
# read n
# ===================
echo I have $# arguments
# ===================
echo "My arguments are $@"
# ===================
i='!'
while test $i != '!!!!!!'
do
    j='!'
    while test $j != '!!!!!!'
    do
        echo -n ". "
        j="!$j"
    done
    echo
    i="!$i"
done

for file in *.txt
do
    if test -f "$file"
    then
        dos2unix "$file"
    fi
done
#  ===================
case $# in
    0)
        echo no arguments
        ;;
    1)
        echo one argument
        ;;
    2|3|4)
        echo some arguments
        ;;
    *)
        echo many arguments
        ;;
esac
# ===================
date=$(date +%Y-%m-%d)

echo Hello $(whoami), today is $date

echo "command substitution still works in double quotes: $(hostname)"

echo 'command substitution does not work in single quotes: $(not a command)'

echo "The groups I am part of are $(groups $(whoami))"
# ===================
x=6
y=7
echo $((x  + y))
# ===================
echo hello >file
echo world >> file
cat <file
# ===================
test -w /dev/null && echo /dev/null is writeable
test -x /dev/null || echo /dev/null is not executable

# ===================
if test -w /dev/null && test -r /dev/null
then
    echo /dev/null is writeable and readable
fi

if grep -Eq $(whoami) enrolments.tsv
then
    echo I am enrolled in COMP2041/9044
fi
