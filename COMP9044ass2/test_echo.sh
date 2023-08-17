# This script is for testing every possible usage of echo
# in quoted/unquoted cases

# no variable, only unquoted and quoted string 
echo hello world
echo "hello world"
echo 'hello world'

# access variable in echo 
var1=hello
var2=world
echo $var1 $var2
echo "$var1 $var2"
echo '$var1 $var2'

echo ${var1} ${var2}
echo "${var1} ${var2}"
echo '${var1} ${var2}'

# also, use python builtIn and keyword to deinf variable
print=hello
pass=world
echo $print $pass
echo "$print $pass"
echo '$print $pass'

echo ${print} ${pass}
echo "${print} ${pass}"
echo '${print} ${pass}'

# access non-existing variables
echo $not_exist
echo "$not_exist"
echo '$not_exist'

# contain backticks 
echo `pwd`
echo "`pwd`"
echo '`pwd`'

# using $() and $(())
echo $(pwd)
echo "$(pwd)"
echo '$(pwd)'

echo $((1 + 2))
echo "$((1 + 2))"
echo '$((1 + 2))'

# using -n option
echo -n hello world
echo -n "hello world"
echo -n 'hello world'

# combine different scenarios
echo -n "the first variable is $print" 'the second variable is $pass' $pass
