#!/bin/dash

# This test script is only for the commands covered in subset 0
# usage of pigs-add and pigs-commit is more complex, compared with test02.sh
# check whether all commands from subset 0 works properly

pigs-init
# Initialized empty pigs repository in .pig

pigs-init
# pigs-init: error: .pig already exists

pigs-add a
# pigs-add: error: can not open 'a'

echo "hello world" >a

pigs-add a
pigs-commit -m 'first commit'
# Committed as commit 0

echo "hello world" >>a
pigs-add a
pigs-commit -m 'second commit'
# Committed as commit 1

echo "hello world" >>a
pigs-add a
pigs-commit -m 'third commit'
# Committed as commit 2

pigs-log
# 2 third commit
# 1 second commit
# 0 first commit

pigs-show 0:a
# hello world

pigs-show 1:a
# hello world
# hello world

pigs-show 2:a
# hello world
# hello world
# hello world

cat a
# hello world
# hello world
# hello world

echo "hello world" >>a
pigs-add a

pigs-show :a
# hello world
# hello world
# hello world
# hello world
