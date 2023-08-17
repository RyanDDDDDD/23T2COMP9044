#!/bin/dash

# A very simple test to ensure pigs-add and pigs-commit works properly

pigs-init
# Initialized empty pigs repository in .pig

touch a b c
pigs-add a b c

pigs-commit -m "first commit"
# Committed as commit 0

pigs-commit -m "second commit"
# nothing to commit