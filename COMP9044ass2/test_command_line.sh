#!/bin/dash

# command line input testing
# test all cases with single/double quotes

# testing command line arguments
# testing arguments smaller than 10
echo $1 $2 $3 $4 $5 $6 $7 $8 $9 
echo "$1 $2 $3 $4 $5 $6 $7 $8 $9" 
echo '$1 $2 $3 $4 $5 $6 $7 $8 $9'

# testing arguments bigger than or equal to 10
echo ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} 
echo "${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19}"
echo '${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19}' 

# access command line argument list
echo $@
echo "$@"
echo '$@'

# get number of command line argument
echo $#
echo "$#"
echo '$#'
