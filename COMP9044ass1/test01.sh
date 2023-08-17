#!/bin/dash

# This script is for testing potential errors for pigs-add and pigs-commit

pigs-init
# Initialized empty pigs repository in .pig

#########################
# testing pigs-add
#########################

### test:when add an non-exisitng file, there should be an error
pigs-add a
# pigs-add: error: can not open 'a'

echo "hello world" >a
pigs-add a
# no error occur, add to index successfully

#########################
# testing pigs-commit
#########################

## test: input validation for pigs-commit
## no arguments provided
pigs-commit
# pigs-commit: error: please only enter 2 or 3 arguments

## 1 arguments provided 
pigs-commit -m
# pigs-commit: error: please only enter 2 or 3 arguments

pigs-commit "first commit"
# pigs-commit: error: please only enter 2 or 3 arguments

## 2 arguments provided
pigs-commit -a ""
# pigs-commit: error: please make sure input -m as argument

pigs-commit -a -m
# pigs-commit: error: please leave commit message

pigs-commit -m -a
# pigs-commit: error: please leave commit message

pigs-commit -b -c
# pigs-commit: error: please make sure input -m as argument

## 3 arguments provided
pigs-commit -a -b "first commit"
# pigs-commit: error: please enter -m as arguments

# Successful commit
pigs-commit -m "first commit"
# Committed as commit 0