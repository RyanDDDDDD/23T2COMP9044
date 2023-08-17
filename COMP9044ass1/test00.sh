#!/bin/dash

# This test is for checking whether all commands except pigs-init is accessible
# before the .pig is created
# By default, no any commands should be accessable until the current directory
# is initialized as a repository

# This script is only for testing all commands
# to see whether all commands covered in subset0/1/2 is available before
# the repository is created

# we also check whether we can initialize repository twice after create .pig

pigs-add
# pigs-add: error: pigs repository directory .pig not found

pigs-commit
# pigs-add: error: pigs repository directory .pig not found

pigs-log
# pigs-add: error: pigs repository directory .pig not found

pigs-show
# pigs-add: error: pigs repository directory .pig not found

pigs-rm
# pigs-add: error: pigs repository directory .pig not found

pigs-status
# pigs-add: error: pigs repository directory .pig not found

pigs-branch
# pigs-add: error: pigs repository directory .pig not found

pigs-checkout
# pigs-add: error: pigs repository directory .pig not found

pigs-merge
# pigs-add: error: pigs repository directory .pig not found

pigs-init
# Initialized empty pigs repository in .pig

pigs-init
# pigs-init: error: .pig already exists