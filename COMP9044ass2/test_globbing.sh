#!/bin/dash

# test globbing in quoted/unquoted cases

# test *
echo *
echo "*"
echo '*'

# test globbing when using it in variable
var=*
echo $var
echo "$var"
echo '$var'

# test glbbing using ? and []
echo ?.c
echo "?.c"
echo '?.c'

echo [ac].c
echo [bc].c
echo [ac].c
echo ???

echo "[ac].c"
echo "[bc].c"
echo "[ac].c"
echo "???"

echo '[ac].c'
echo '[bc].c'
echo '[ac].c'
echo '???'

