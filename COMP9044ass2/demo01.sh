#!/bin/dash

##### demo using shell features from subset 1
touch a b

for i in 1 2 3
do
    echo $i
done

for file in  *
do
  echo $file
done

rm a b

cd ..

echo "enter an word"
read var
echo $var

exit 0