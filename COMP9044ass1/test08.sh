#!/bin/dash

# Test case: subset 2
# This script is for exploring potential error with pigs-merge

pigs-init
# Initialized empty pigs repository in .pig

#########################
# testing merge error checking
#########################

touch a
pigs-add a

pigs-commit -m "first commit"
# Committed as commit 0

pigs-branch new_branch

pigs-checkout new_branch
# Switched to branch 'new_branch'

touch b
pigs-add b

pigs-commit -m "second commit"
# Committed as commit 1

pigs-checkout master
# Switched to branch 'master'

# input checking
pigs-merge
# pigs-merge: error: invalid aruguments for pigs-merge

pigs-merge new_branch
# pigs-merge: error: empty commit message

pigs-merge new_branch -m
# pigs-merge: error: invalid aruguments for pigs-merge

pigs-merge new_branch -a "merge new branch"
# pigs-merge: error: the second argument should be -m

pigs-merge non_existing_branch -m "merge an non existing branch"
# pigs-merge: error: unknown branch 'merge an non existing branch'

# when two branches change same file, prevent merging by showing error
echo "hello" >a
pigs-commit -a -m "change a at master"
# Committed as commit 2

pigs-checkout new_branch
echo "world" >a
pigs-commit -a -m "change a at new branch"
# Committed as commit 3

pigs-checkout master
pigs-merge new_branch -m "merge new branch"
# pigs-merge: error: These files can not be merged:
# a

touch c
pigs-add c
pigs-merge new_branch -m "merge new branch"
# pigs-merge: error: index is not clean, commit before merge
