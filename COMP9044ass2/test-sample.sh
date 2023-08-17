#!/bin/dash

SOURCE_FILE="`pwd`/sheepy.py"

TARGET_FILE="`pwd`/test-allsamples.sh"

$SOURCE_FILE $TARGET_FILE >temp.py

chmod 755 temp.py
./temp.py 1 2 3 4 5 >a.out 2>&1

$TARGET_FILE 1 2 3 4 5 >b.out 2>&1

if [ $(diff a.out b.out | wc -l) -eq 0 ]
then
  echo "Test passed"
else
  echo "Test not passed"
fi

rm temp.py
# rm a.out b.out