#!/bin/dash

# Test case: subset 2
# This script is relative to create,checkout and delete branch,

pigs-init
# Initialized empty pigs repository in .pig

#########################
# testing creating branch
#########################

# can not create branch until the first commit is stored in repo
pigs-branch new_branch
# pigs-branch: error: this command can not be run until after the first commit

# viewing all branches should only be available after the first commit
pigs-branch
# pigs-branch: error: this command can not be run until after the first commit

touch a 
pigs-add a
pigs-commit -m "first comnit"
# Committed as commit 0

pigs-branch
# master

# default branch is master, can not create a branch with same name
pigs-branch master
# pigs-branch: error: not a valid object name: 'master'

# create branch
pigs-branch new_branch

# can not create a duplicate branch
pigs-branch new_branch
# pigs-branch: error: branch '$1' already exists

pigs-branch
# master
# new_branch


#########################
# testing checkout branch
#########################
# can not checkout to current branch
pigs-checkout master
# Already on master

# we can show differemt contents for different branches
pigs-checkout new_branch

touch b
pigs-add b
pigs-commit -m "second commit"

ls
# a b
pigs-checkout master

ls
# a

# can not checkout to an non-existing branch
pigs-checkout non_existing_branch
# pigs-checkout: error: unknown branch 'non_existing_branch'

# we should prevent certain files to be overwritten
echo "hello world" >b
pigs-checkout new_branch
# pigs-checkout: error: Your changes to the following files would be overwritten by checkout:
# b

#########################
# testing delete branch
#########################

rm b

# delete an non-existing branch
pigs-branch -d non_existing_branch
# pigs-branch: error: branch 'non_existing_branch' doesn't exist

pigs-branch -d master
# pigs-branch: error: can not delete branch 'master': default branch

pigs-branch -d new_branch
# pigs-branch: error: branch 'new_branch' has unmerged changes

pigs-merge new_branch -m "merge new branch"
# Fast-forward: no commit created

pigs-branch -d new_branch
# Deleted branch 'new_branch'
