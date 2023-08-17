#!/bin/dash

# Test case: subset 1
# This script is for exploring different errors when using pigs-rm
# try to use pigs-rm with different options to remove files in differrent situation

pigs-init
# Initialized empty pigs repository in .pig

########################
# testing pigs-rm no options
#########################

## try to rm an non-existing file
pigs-rm a
# pigs-rm: error: 'a' is not in the pigs repository

touch a
pigs-add a

pigs-commit -m "first commit"
# Committed as commit 0

## try to rm a after staged change (not commit)
echo "hello world" >a
pigs-add a

pigs-rm a
# pigs-rm: error: 'a' has staged changes in the index

## file in index/working directory and local repo are not the same
echo "hello world" >>a
pigs-rm a
# pigs-rm: error: 'a' in the repository is different to the working file and the repository

# reset directory
rm -rf .pig
rm -rf ./*

###########################################################
###########################################################

########################
# testing pigs-rm 1 option (--cached / --force)
#########################

pigs-init
# Initialized empty pigs repository in .pig

touch a
pigs-add a

pigs-commit -m "first commit"

### test: --cached is used
pigs-rm --cached
# pigs-rm: error: please specify a file to delete

# try to delete an non-existing file
pigs-rm --cached b
# pigs-rm: error: 'b' is not in the pigs repository

### test: --force is used
pigs-rm --force
# pigs-rm: error: please specify a file to delete

# try to delete an non-existing file
pigs-rm --force b
# pigs-rm: error: 'b' is not in the pigs repository

# reset directory
rm -rf .pig
rm -rf ./*

###########################################################
###########################################################

########################
# testing pigs-rm 2 options
#########################

pigs-init
# Initialized empty pigs repository in .pig

touch a
pigs-add a

pigs-commit -m "first commit"

pigs-rm --cached --force
# pigs-rm: error: please specify a file to delete

pigs-rm --force --cached
# pigs-rm: error: please specify a file to delete

pigs-rm --cached --force b
# pigs-rm: error: 'b' is not in the pigs repository

