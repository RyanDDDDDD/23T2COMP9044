#!/bin/dash

# Test case: subset 1
# This script covers all commands with different options from subset 1
# to print out all kinds of message of pigs-status

pigs-init
# Initialized empty pigs repository in .pig

echo "this is a" >a
pigs-status
# a - untracked

pigs-add a
pigs-status
# a - added to index

echo "change a" >a
pigs-status
# a - added to index, file changed

rm a
pigs-status
# a - added to index, file deleted

echo "change a" >a

pigs-commit -m "first commit"
# Committed as commit 0

echo "change a again" > a
pigs-status
# a - file changed, changes not staged for commit

pigs-add a
echo "change a again again" > a
pigs-status
# a - file changed, different changes staged for commit

pigs-add a
pigs-status
# a - file changed, changes staged for commit

pigs-commit -a -m "second commit"
# Committed as commit 1

pigs-status
# a - same as repo

rm a
pigs-status
# a - file deleted

echo "change a again again" > a
pigs-rm --cached a
pigs-status
# a - deleted from index

pigs-add a
pigs-rm a
pigs-status
# a - file deleted, deleted from index