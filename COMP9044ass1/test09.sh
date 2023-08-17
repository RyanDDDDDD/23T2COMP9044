#!/bin/dash

# Test case: subset 2
# This script is for testing merging by branch name 
# and commit number (latest and intermediate commit of another branch)

#########################
# testing merge branch using branch name 
#########################

pigs-init
# Initialized empty pigs repository in .pig

touch a
pigs-add a

pigs-commit -m "first commit"
# Committed as commit 0

### fast-forward merge
pigs-branch new_branch

pigs-checkout new_branch
# Switched to branch 'new_branch'

touch b
pigs-add b

pigs-commit -m "second commit"
# Committed as commit 1

pigs-checkout master
# Switched to branch 'master'

pigs-merge new_branch -m "merge new branch"
# Fast-forward: no commit created

### three-way merge
touch c
pigs-add c

pigs-commit -m "third commit"
# Committed as commit 2

pigs-checkout new_branch
# Switched to branch 'new_branch'

touch d
pigs-add d

pigs-commit -m "fourth commit"
# Committed as commit 3

pigs-checkout master
# Switched to branch 'master'

pigs-merge new_branch -m "merge new branch again"
# Committed as commit 4

# reset directory
rm -rf .pig
rm -rf ./*

#########################
# testing merge branch using commit number (latest commit of another branch)
#########################

pigs-init
# Initialized empty pigs repository in .pig

touch a
pigs-add a

pigs-commit -m "first commit"
# Committed as commit 0

### fast-forward merge
pigs-branch new_branch

pigs-checkout new_branch
# Switched to branch 'new_branch'

touch b
pigs-add b

pigs-commit -m "second commit"
# Committed as commit 1

pigs-checkout master
# Switched to branch 'master'

pigs-merge 1 -m "merge new branch"
# Fast-forward: no commit created

ls
# a b

### three-way merge
touch c
pigs-add c

pigs-commit -m "third commit"
# Committed as commit 2

pigs-checkout new_branch
# Switched to branch 'new_branch'

touch d
pigs-add d

pigs-commit -m "fourth commit"
# Committed as commit 3

pigs-checkout master
# Switched to branch 'master'

ls
# a b c

pigs-merge 3 -m "merge new branch again"
# Committed as commit 4

ls
# a b c d

# reset directory
rm -rf .pig
rm -rf ./*

#########################
# testing merge branch using commit number (intermediate commit of another branch)
#########################

pigs-init
# Initialized empty pigs repository in .pig

touch a
pigs-add a

pigs-commit -m "first commit"
# Committed as commit 0

### fast-forward merge
pigs-branch new_branch

pigs-checkout new_branch
# Switched to branch 'new_branch'

touch b
pigs-add b

pigs-commit -m "second commit"
# Committed as commit 1

touch c
pigs-add c

pigs-commit -m "third commit"
# Committed as commit 2

# files of new branch
ls
# a b c

pigs-checkout master
# Switched to branch 'master'

# files of master
ls 
# a

pigs-merge 1 -m "merge new branch"
# Fast-forward: no commit created

# files of master
ls
# a b

### three-way merge
touch d
pigs-add d

pigs-commit -m "fourth commit"
# Committed as commit 3

# files of master
ls
# a b d

pigs-checkout new_branch
# Switched to branch 'new_branch'

# files of new branch
ls
# a b c

touch e
pigs-add e

pigs-commit -m "fifth commit"
# Committed as commit 4

pigs-checkout master
# Switched to branch 'master'

# files of master
ls
# a b d

pigs-merge 2 -m "merge new branch again"
# Committed as commit 5

# files of master
ls
# a b c d
