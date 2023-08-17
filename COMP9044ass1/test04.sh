#!/bin/dash

# Test case: subset 1
# Simple use of all commands covered in subset 0 and 1
# Commit files using -a -m option
# Then remove files using pigs-rm with --cached --forced optionaly
# and use pigs-status to check filt status

pigs-init
# Initialized empty pigs repository in .pig

touch a b
pigs-add a b

# Successful commit
pigs-commit -m "first commit"
# Committed as commit 0

########################
# testing pigs-commit -a -m
#########################

# try to commit with -a -m, it fails
pigs-commit -a -m "second commit"
# nothing to commit

# update content of a and commit again
echo "hello world" >a
pigs-commit -a -m "second commit"
# Committed as commit 1

########################
# testing pigs-rm [--cached] [--force]
#########################

# remove file from index
pigs-rm --cached a

ls
# a b

pigs-commit -m "third commit"
# Committed as commit 2

ls 
# a b

# remove b from local repo/working directory/index
pigs-rm --force b

ls
# a

pigs-status
# a - untracked