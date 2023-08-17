#!/bin/dash

SOURCE_FILE="`pwd`/sheepy.py"

TARGET_FILE="`pwd`/test_command_line.sh"

$SOURCE_FILE $TARGET_FILE >tmp.py
chmod 755 tmp.py
./tmp.py 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 >a.out 2>&1
$TARGET_FILE 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 >b.out

if [ $(diff a.out b.out | wc -l) -eq 0 ]
then
  echo "Test passed"
else
  echo "Test not passed"
fi

rm tmp.py
rm a.out b.out
