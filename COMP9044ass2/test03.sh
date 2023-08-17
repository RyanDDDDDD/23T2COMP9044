#!/bin/dash

SOURCE_FILE="`pwd`/sheepy.py"

TARGET_FILE="`pwd`/test_for.sh"

$SOURCE_FILE $TARGET_FILE | python3 >a.out 2>&1
$TARGET_FILE >b.out

if [ $(diff a.out b.out | wc -l) -eq 0 ]
then
  echo "Test passed"
else
  echo "Test not passed"
fi

rm a.out b.out
