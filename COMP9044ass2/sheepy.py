#!/usr/bin/python3 -u

import sys
import re

def getSpaces(line):
  """
  get leading spaces of each line
  """
  leadingSpaces = re.match(r"(\s*)",line)
  if (leadingSpaces.group(1) == None):
    return ""
  
  return leadingSpaces.group(1)

def getComments(line):
  # get comments from each end of line
  trailingComment = re.match(r"(.*[^$])(#.*[^\"'])$",line)
  if (trailingComment == None):
    # no comments at the end of line
    return ""
  else:
    return trailingComment.group(2)

def backtickCommand(inputStr):
  """
    if $(()) or $() exist in arguments, put them into backticks to
    avoid being accidentally split into two arguments
  """
  numberOfDollar = 0
  firstQuote = 0
  lastQuote = 0
  
  checkList = set(["$","(",")"])

  ret = ""
  for i in range(len(inputStr)):
    c = inputStr[i]

    if (c not in checkList):
      ret += c
      continue
    
    if (c == "$"):
      if (inputStr[i + 1] == "("):
      # find $() and $(())
        if (not numberOfDollar):
          # start of $() and $(())
          ret += '`' + c
          numberOfDollar += 1
        else:
          ret += c
          numberOfDollar += 1
      else:
        # normal $ to access variable
        ret += c
      continue
    
    if (c == "("):
      if (numberOfDollar > 0):
        # the current char is in $() or $(())
        firstQuote += 1
        ret += c
      else:
        # normal ()
        ret += c
      continue
    
    if (c == ")"):
      if (numberOfDollar > 0):
        # the current char is in $() or $(())
        if (firstQuote - lastQuote == 1):
          # end of $() or $(())
          lastQuote = 0
          firstQuote = 0
          numberOfDollar = 0
          ret += c + "`"
        else:
          lastQuote += 1
          ret += c
      else:
        # normal ()
        ret += c
      continue
  
  return ret

def getArgs(inputStr):
  """
  split arguments by single/double quote, backticks, and a single space
  """
  # quote $() and $(())
  inputStr = backtickCommand(inputStr)
  
  # if current line is for defining new variable,dont need to process argument
  if (re.match(r"[^ =]+=[^ =]+",inputStr)):
    return inputStr

  # external command line tool, with no arguments
  if (" " not in inputStr):
    return []

  ret = []
  
  args = re.split(" ",inputStr,1)[1]
  while (len(args)):
    if (args[0] == "\""):
      nextArg = re.match(r"\"[^\"]+\"[^\"'` ]*",args).group()
      args = args.removeprefix(nextArg)
      ret.append(nextArg)
    elif (args[0] == "'"):
      nextArg = re.match(r"'[^']+'[^\"'` ]*",args).group()
      args = args.removeprefix(nextArg)
      ret.append(nextArg)
    elif (args[0] == "`"):
      nextArg = re.match(r"`[^`]+`[^\"'` ]*",args).group()
      args = args.removeprefix(nextArg)
      ret.append(nextArg)
    else:
      splitArgs = re.split(r" +",args,1)
      nextArg =  splitArgs[0] 
      ret.append(nextArg)
      if (len(splitArgs) == 1):
        # last element
        break
      args = splitArgs[1].lstrip()
      
  return [ arg for arg in ret if arg != '' ]

def getRedirect(line):
  """
  extract redirection from current line
  """
  ret = []

  redirect = re.search(r"[^<>](<[^< ][a-zA-Z1-9 _-{}\[\].]*|>{1,2}[^<>][a-zA-Z1-9 _-{}\[\].]+)$",line)

  if redirect:
    redirect = redirect.group()

    # remove redirection from the end of line
    lineRemoveRedirect = line.removesuffix(redirect)

    ret.append(lineRemoveRedirect)
  else:
    ret.append(line)

  if redirect :
    if (re.search(r"[^>](>{1,2}[^>].*)$",redirect) and re.search(r"[^<](<[^<].*)$",redirect)):
      redirect = redirect.strip()
      # split direction arguments if they are both used
      firstArg = re.match(r"(>{1,2}|<)(.*)",redirect).groups()[0].strip()
      
      redirect = redirect.lstrip(firstArg)
      argumentList = re.split(r"(>{1,2}|<)",redirect)

      firstFile = argumentList[0].strip()
      secondArg = argumentList[1].strip()
      secondFile = argumentList[2].strip()

      firstRedirection = firstArg + firstFile
      secondRedirection = secondArg + secondFile

      ret.append(firstRedirection)
      ret.append(secondRedirection)
  
    else:
      redirect = redirect.strip()
      # only one redirection
      firstArg = re.match(r"(>{1,2}|<)(.*)",redirect).groups()[0]

      redirect = redirect.lstrip(firstArg)
      argumentList = re.split(r"(>{1,2}|<)",redirect)
      firstFile = argumentList[0].strip()
      firstRedirection = firstArg + firstFile

      ret.append(firstRedirection)
    
  return ret

def transformedArgs(args):
  """
  process each argument to get a correct syntax in python
  for example: if argument is quoted by $1, transfromed to sys.argv[1]
  """
  newArgs = []
 
  for arg in args:
    # replace all `$()` and `$(())` to $() and $(())
    arg = re.sub(r"`(\$\([^`]*\))`",r"\1",arg)

    # argument is not quoted by single quote
    if (not re.fullmatch(r"'.*'",arg)):
      checkStartSingleQuote = ""
      if (re.match(r"'[^']+'",arg)):
        target = re.match(r"'[^']+'",arg).group()
        checkStartSingleQuote = '"' + target[1:-1] + '"'

        # only check the part outside of single quote
        arg = arg.removeprefix(target)

      # check globbing for the provided arguments

      if((arg[0] != '"' and arg[0] != "'" and arg[0] != "`") and re.search(r"[^ ]*[?*]+[^ ]*|\[.*?\]",arg)):
        modules.add("glob")
        # when globbing doesn't find a matching, return raw string

        arg = r"{' '.join(sorted(glob.glob(" + rf"'{arg}'" + "))) if ' '.join(sorted(glob.glob("+ rf"'{arg}'" + "))) != '' else " + rf"'{arg}'" + "}"

        if (re.search(r"glob\.glob\('.*?\$.*?'\)",arg)):
          arg = re.sub(r"glob\.glob\(('.*?\$.*?')\)",r"glob.glob(f\1)",arg)
        if (re.search(r"else ('.*\$.*')}$",arg)):
          arg = re.sub(r"else ('.*\$.*')}$",r"else f\1",arg)

      # transform command line argument
      if (re.search(r"\$[0-9]",arg)):
        # command line arguments smaller than 10
        modules.add("sys")
        arg = re.sub(r"(\$[0-9])",lambda str: "{sys.argv[" + str.group()[1:] + "]}",arg)

      if(re.search(r"\${[1-9][0-9]+}",arg)):
        # command line arguments bigger than 10
        modules.add("sys")
        arg = re.sub(r"(\${[1-9][0-9]+})",lambda str: "{sys.argv[" + str.group()[2:-1] + "]}",arg)

      # replace any variables accessed by $var with ${var}
      def func0(str):
        variable = str.group()[1:]
        return "${" + variable + "}"

      arg = re.sub(r"(\$\w+)",func0,arg)
      
      if(re.search(r"\${[^}]+}",arg)):
        # access variable using ${}
        def func1(inputStr):
          variable = inputStr.group()[2:-1]
          
          if (variable in variables):
            return "{" + variables[variable] + "}"
          else: 
            # we are in looping or trying to print an undefined variable
            if (variable in loopingCounters):
              # this is a looping counter
              return "{" + variable + "}"
            else:
              # trying to print an undefined variable, define a variable with empty string
              if (variable in validKeywords):
                variable = variable + "_alternative"

              lines.append(f"{spaces}{variable} = '' {trailingComment}")
              return "{" + variable + "}"

        arg = re.sub(r"\$({[^}]+})",func1,arg)

      # replace $(())
      if(re.search(r"\$\(\([^)]+\)\)",arg)):
        def func2(inputStr):
          arithmeticOperation = inputStr.group()[3:-2]
          arithmeticOperation = re.sub(r"(\w+)",r"int(\1)",arithmeticOperation)
          # variable expansion
          arithmeticOperation = re.sub(r"\${([^}]+)}",r"\1",arithmeticOperation)
          arithmeticOperation = re.sub(r"\$([^ ]+)",r"\1",arithmeticOperation)

          return "{" + arithmeticOperation + "}"

        arg = re.sub(r"\$\(\([^)]+\)\)",func2,arg)

      # process $() recursively 
      if(re.search(r"\$\(.*\)",arg)):

        # find all occurences of $(()), then replace each of them in original string
        modules.add("subprocess")
    
        def func3(inputStr):
          argList = inputStr.group()[1:-1].split(" ")
          argList[0] = argList[0][1:]
          ret = "{subprocess.run(" + repr(argList) + ", text=True, stdout=subprocess.PIPE).stdout.rstrip()}"
          ret = re.sub(r"'(tmp_[0-9]+)'",r"\1",ret)
          return ret
        
        global number
       
        while (re.search(r"\$\([^$)]+\)",arg)):
          # the innermost command
          command = re.search(r"\$\([^$)]+\)",arg).group()

          convertCommand = re.sub(r"\$\(([^)]*)\)",func3,command)
          
          # variable expansion
          convertCommand = re.sub(r"'{(.*?)}'",r"\1",convertCommand)

          # define an new variable for the innermost command
          lines.append(f"{spaces}tmp_{number} = f\"{convertCommand}\"")
          variables[f"tmp_{number}"] = f"tmp_{number}"
          
          arg = re.sub(r"\$\([^$)]+\)",rf"tmp_{number}",arg,1)
          
          number += 1
        
        # wrap all temp commands into {} to access its value
        arg = re.sub(r"(tmp_[0-9]+)",r"{\1}",arg)
       
        # if one of the argument is quoted by single/double quote,it will be quoted again after running repr
        # to solve this, remove the outer quotes
        arg = re.sub(r"\"([^\"]+)\"",r"\1",arg)

        arg = re.sub(r"\$\((.*)\)",func3,arg)

        # variable replacement
        arg = re.sub(r"'([^']*)\$([^{][^']*[^}]?)'",r"str(\1) + str(\2)",arg)
        arg = re.sub(r"'([^']*)\${([^}]+)}'",r"str(\1) + str(\2)",arg)
        arg = re.sub(r"'\$([^']+)'",r"\1",arg)
      
      # check backticks
      if(re.search(r"`.*`",arg)):

        # find all occurences of backticks, then replace each of them in original string
        modules.add("subprocess")
        def func4(inputStr):
          return "`{subprocess.run(" + repr(inputStr.group()[1:-1].split(" ")) + ", text=True, stdout=subprocess.PIPE).stdout.rstrip()}`"
        
        # if one of the argument is quoted by single/double quote,it will be quoted again after running repr
        # to solve this, remove the outer quotes
        arg = re.sub(r"\"([^\"]+)\"",r"\1",arg)

        arg = re.sub(r"`.*?`",func4,arg)

        # variable access
        arg = re.sub(r"'{(.*?)}'",r"\1",arg)

        # ????
        arg = re.sub(r"'([^']*)\$([^{][^']*[^}]?)'",r"str(\1) + str(\2)",arg)
        arg = re.sub(r"'([^']*)\${([^}]+)}'",r"str(\1) + str(\2)",arg)

      if(re.search(r"\$@",arg)):
        # command line argument lists
        modules.add("sys")
        arg = re.sub(r"\$@",r"{' '.join(sys.argv[1:])}",arg)
      
      if(re.search(r"\$#",arg)):
        # command line number
        modules.add("sys")
        arg = re.sub(r"\$#",r"{len(sys.argv) - 1}",arg) 

      newArgs.append(checkStartSingleQuote + arg)
    else:
      # argument quoted by single quote, treated as raw string
      newArgs.append(arg)

  return newArgs

def separateStatement(args):
  """
  reaplace -a -o options from test
  """
  combinedStatement = " ".join(args)
  if (combinedStatement[:4] == "test"):
    combinedStatement = re.sub(r"(-a |-o )",r"\1 test ",combinedStatement)
  else:
    combinedStatement = re.sub(r"(-a |-o )",r" ] \1 [ ",combinedStatement)

  ret = re.split(r"(-a |-o )",combinedStatement)
  
  return [ segment.strip() for segment in ret ]

def isTest(segment):
  if (re.match(r"test ",segment)):
    return True

  if (re.fullmatch(r"\[.*?\]",segment)):
    return True

  return False

def getSegmentArgs(segment,segmentType):
  """
  get arguments of each semgment
  """
  # the $() and $(()) has been put into ``, needs to remove `` to run getArgs again
  segment = re.sub(r"`(\$\([^`]+\))`",r"\1",segment)
  
  if (segmentType == "test"):
    firstArg = segment.split(" ")[0]

    segementList = getArgs(segment)
    if (firstArg != "test"):      
      # test using []
      segementList = segementList[:-1]

    return segementList
  else:
    firstArg = segment.split(" ")[0]
    # true/false condition
    if (firstArg == "true" or firstArg == "false" ):
      ret = []
      ret.append("True" if firstArg == "true" else "False")
      return ret
    
    # external command
    segementList = getArgs(segment)

    segementList.insert(0,firstArg)
    
    return segementList

def splitCondition(args):
  """
  split all conditions and external commands by && and ||
  """
  ret = []

  temp = []
  for arg in args:
    if (arg == "&&" or arg == "||"):
      ret.append([x for x in temp])
      temp.clear()
      temp.append(arg)
      ret.append([x for x in temp])
      temp.clear()
      continue

    temp.append(arg) 
  
  # add last condition
  ret.append([x for x in temp])

  return [x for x in ret if x != []]

def parseArgs(args):
  """
  parsing arguments in if/while statement 
  1) split arguments into multiple segment if multiple test/external commands exists (seperate by && and ||)
  2) for each segment, determine if it is external command or test
  3) check syntax of test: 
      1: test -option ... 
      2: [ -option ... ]
  """

  ret = ""
  pre = ""

  conditions = splitCondition(args)

  for i in range(len(conditions)):
    condition = conditions[i]

    if (condition[0] == "&&" or condition[0] == "||"):
      if (condition[0] == "&&"):
        pre = pre + " and "
        ret += pre
        pre = ""
      else:
        pre = "not " + pre + " or "
        ret += pre
        pre = ""

      continue

    segments = separateStatement(condition)
    # print(segments)
    for segment in segments:
      if (segment == "-o"):
        pre += " or "
        continue

      if (segment == "-a"):
        pre += " and "
        continue
      
      if (isTest(segment)):
        args = getSegmentArgs(segment,"test")
        args = transformedArgs(args)

        checkNot = ""
        if (args[0] == "!"):
          checkNot = "not "
          args = args[1:]

        if (len(args) == 1):
          transformedSegment = f"len({args[0]}) != 0"
          pre += checkNot + transformedSegment
          continue

        elif (len(args) == 2):

          option = args[0]
          path = args[1]
          # remove single/double quote when there is no variable expansion
          if (re.fullmatch(r"(['\"])[^{].*[^}]\1",path)):
            path = path[1:-1]

          # options for check file existence
          if (option == "-n"):
            transformedSegment = f"len('{path}') != 0"
            pre += checkNot +  transformedSegment
            continue
          if (option == "-z"):
            transformedSegment = f"len('{path}') == 0"
            pre += checkNot +  transformedSegment
            continue
          if (option == "-w"):
            modules.add("os")
            transformedSegment = f"os.access('{path}',os.W_OK)"
            pre += checkNot +  transformedSegment
            continue
          if (option == "-r"):
            modules.add("os")
            transformedSegment = f"os.access('{path}',os.R_OK)"
            pre += checkNot + transformedSegment
            continue
          if (option == "-x"):
            modules.add("os")
            transformedSegment = f"os.access('{path}',os.X_OK)"
            pre += checkNot + transformedSegment
            continue
          if (option == "-d"):
            modules.add("os")
            transformedSegment = f"os.path.isdir('{path}')"
            pre += checkNot + transformedSegment
            continue
          if (option == "-f"):
            modules.add("os")
            transformedSegment = f"os.path.isfile('{path}')"
            pre += checkNot + transformedSegment
            continue
          if (option == "-e"):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}')"
            pre += checkNot + transformedSegment
            continue
          if (option == "-h" or option == "-L" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.path.islink('{path}')"
            pre += checkNot + transformedSegment
            continue
          if (option == "-s" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.stat('{path}').st_size > 0"
            pre += checkNot + transformedSegment
            continue
          if (option == "-k" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.stat('{path}').st_mode & 0o1000 == 0o1000"
            pre += checkNot + transformedSegment
            continue
          if (option == "-g" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.stat('{path}').st_mode & 0o2000 == 0o2000"
            pre += checkNot + transformedSegment
            continue
          if (option == "-u" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.stat('{path}').st_mode & 0o4000 == 0o4000"
            pre += checkNot + transformedSegment
            continue
          if (option == "-G" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.getegid() == os.stat('{path}').st_gid"
            pre += checkNot + transformedSegment
            continue
          if (option == "-O" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and os.geteuid() == os.stat('{path}').st_uid"
            pre += checkNot + transformedSegment
            continue
          if (option == "-b" ):
            modules.add("os")
            transformedSegment = f"os.path.exists('{path}') and stat.S_ISBLK(os.stat('{path}').st_mode)"
            pre += checkNot + transformedSegment
            continue
          if (option == "-c" ):
            modules.add("os")
            modules.add("stat")
            transformedSegment = f"os.path.exists('{path}') and stat.S_ISCHR(os.stat('{path}').st_mode)"
            pre += checkNot + transformedSegment
            continue
          if (option == "-p" ):
            modules.add("os")
            modules.add("stat")
            transformedSegment = f"os.path.exists('{path}') and stat.S_ISFIFO(os.stat('{path}').st_mode)"
            pre += checkNot + transformedSegment
            continue
          if (option == "-S" ):
            modules.add("os")
            modules.add("stat")
            transformedSegment = f"os.path.exists('{path}') and stat.S_ISSOCK(os.stat('{path}').st_mode)"
            pre += checkNot + transformedSegment
            continue
        elif (len(args) == 3):
          if (args[1] == "-nt" ):
          # FILE1 -nt FILE2: FILE1 is newer (modification date) than FILE2
            modules.add("os")
            transformedSegment = f"os.path.exists('{args[0]}') and os.path.exists('{args[2]}') and os.stat('{args[0]}').st_mtime > os.stat('{args[2]}').st_mtime"
            pre += checkNot + transformedSegment
            continue
          if (args[1] == "-ot" ):
            # FILE1 -ot FILE2: FILE1 is older than FILE2
            modules.add("os")
            transformedSegment = f"os.path.exists('{args[0]}') and os.path.exists('{args[2]}') and os.stat('{args[0]}').st_mtime < os.stat('{args[2]}').st_mtime"
            pre += checkNot + transformedSegment
            continue

          # options for variable comparision
          # convert operands
          for i in [0, 2]:
            if (re.fullmatch(r"{([^}]+)}",args[i])):
              # variable needs to be replace
              args[i] = re.sub(r"{([^}]+)}",r"\1",args[i])
            elif(re.fullmatch(r"\"{([^}]+)}\"",args[i])):
              args[i] = re.sub(r"\"{([^}]+)}\"",r"\1",args[i])
            else:
              if (not re.fullmatch(r"'[^']+'",args[i]) and not re.fullmatch(r"\"[^\"]+\"",args[i])):
                # raw string not quoted, put single quote around the string
                args[i] = "'" + args[i] + "'"

          option = args[1]
          # string comparison
          if (option == "="):          
            args[1] = "=="
            pre += checkNot + " ".join(args)
            continue
          if (option == "!="):          
            pre += checkNot + " ".join(args)
            continue

          # number comparison
          args[0] = f"int(str({args[0]}).strip())"
          args[2] = f"int(str({args[2]}).strip())"

          if (option == "-eq"): 
            args[1] = "=="          
          elif (option == "-ne"):           
            args[1] = "!="          
          elif (option == "-gt"):           
            args[1] = ">"          
          elif (option == "-ge"):           
            args[1] = ">="          
          elif (option == "-le"):           
            args[1] = "<="          
          elif (option == "-lt"):           
            args[1] = "<"

          pre += checkNot + " ".join(args)
      else:
        args = getSegmentArgs(segment,"command")
        args = transformedArgs(args)

        # only solve true/false condition
        if (len(args) == 1 and (args[0] == "True" or args[0] == "False")):
          pre += args[0]
        else:
          strArgs = repr(args)
          strArgs = "not subprocess.run(" + strArgs + ").returncode"
          
          # replace variable expansion
          strArgs = re.sub(r"'{([^']+)}'",r"\1",strArgs)

          pre += strArgs

  ret += pre
  ret = ret.removesuffix(" and ")
  ret = ret.removesuffix(" or ")

  return ret

def isExpand(args):
  """
  determine whether we would expand variables or globbing using f-string
  """
  expand = False

  # determine if there is variables or characters need to be expand in args list
  for arg in args:
    if (arg[0] != "'" and arg[0] != '"'):
      # argument not included by single/double quote, try search character for globbing
      if(re.fullmatch(r"[^ ]*[?*]+[^ ]*|\[.*?\]",arg)):
        # find characters for globbing
        expand = True
        break
    
    # if current string is '.*'str, need to check str
    if (re.match(r"'[^']+'.+",arg)):
      target = re.match(r"'[^']+'",arg).group()
      # only check the part outside of single quote
      arg = arg.removeprefix(target)

    if (arg[0] != "'"):
      # argument not included by single quote, try check if backticks exists or using ${} to access variable
      if(re.fullmatch(r".*\${[^}]+}.*",arg)):
        # check if ${} exist to access variable
        expand = True
        break
      
      # check if there is shell syntax variable access
      if (re.search("\$\w+",removeSpacesline)):
        expand = True
        break

      if(re.search(r"`[^`]+`",arg)):
        # check if backticks exists
        expand = True
        break
        
      if(re.search(r"\$#",arg)):
        # check if $# exist
        expand = True
        break

      if(re.search(r"\$@",arg)):
        # check if $@ exist
        expand = True
        break
  
  # get the whole string removed from single quote, to check $() and $(())
  lines = re.sub(r"'[^']+'",'',' '.join(args))

  # check $(())
  if (re.search(r"\$\(\([^)]+\)\)",lines)):
    expand = True

  # check $()
  if (re.search(r"\$\(.*\)",lines)):
    expand = True

  return expand  
  
def stringArgs(args):
  # return f-string for echo and variable

  retArgs = ""
  for arg in args:
    # single quote argument, remove single quote before transformed to string
    if (re.fullmatch(r"(['])(.*)\1",arg)):
      arg = arg[1:-1]
      retArgs += arg + " "
      continue

    # double quote argument, remove double quote before transformed to string
    arg = re.sub(r"\"([^\"]+)\"",r"\1",arg)  

    # remove backticks
    arg = re.sub(r"`([^`]+)`",r"\1",arg)  
    
    retArgs += arg + " "

  # whole string would be quoted by single quote using output f-string, need to replace all single quote with double quotes
  # to avoid python syntax error
  retArgs = re.sub(r"'",r'"',retArgs)

  # only remove the last added space and preverse other existing spaces at the end
  return retArgs[:-1]

def getLastCommand(args):
  """
  extract the last external commands from arguments and remove the extracted arguments 
  """

  conditions = splitCondition(args)

  lastCommand = conditions[-1]

  # remove the last two elements, which are &&/|| and external commands 
  conditions.pop()

  args = []

  for condition in conditions:
    args += [ arg for arg in condition ]

  return lastCommand,args

def externalCommand(args,firstArg):
  # external command tool

  modules.add("subprocess")

  args.insert(0,firstArg)

  # split line to get the redirection option
  redirectionList = getRedirect(" ".join(args))

  # first element is external command and options
  redirectionList.pop(0)

  # remove the rediction option from arguments
  for _ in range(len(redirectionList)):
    args.pop()

  # check if we have redirection, if so, extract redirection and remove it from the original line
  isRedirected = True if len(redirectionList) else False

  redirectType = ""
  redirectFile = []

  for i in range(len(redirectionList)):
    checkRedirection = re.match(r"(>{1,2}|<)(.*)",redirectionList[i]).group(1)
    
    if (checkRedirection == ">>"):
      redirectType += "a"
    elif (checkRedirection == ">"):
      redirectType += "w"
    else:
      redirectType += "r"

    redirectFile.append(redirectionList[i].lstrip(checkRedirection))

  args = transformedArgs(args)

  args = repr(args)

  # replace globbing to f-string
  args = re.sub(r"\"{' '\.join\((sorted\(glob\.glob\('[^']+'\)\))\) if ' '\.join\(\1\) != '' else '[^']+'}\"",r"*(\1)",args)

  args = re.sub(r"\*\(sorted\(glob\.glob\('([^']+)'\)\)\)",r"*(sorted(glob.glob('\1')) if sorted(glob.glob('\1')) != [] else ['\1'])",args)

  # replace $@ if exist
  args = re.sub(r"'\"{\\' \\'\.join\(sys\.argv\[1:\]\)}\"'","*sys.argv[1:]",args)

  # replace variable accessed by $var
  args = re.sub(r"'{(.*)}'",r"\1",args)

  # replace variable accessed by "$var"
  args = re.sub(r"'\"{([^}]+)}\"'",r"\1",args)
  
  # open file for redirection
  if(isRedirected):
    for i in range(len(redirectType)):
      lines.append(f"{spaces}openFile_{redirectFile[i]} = open('{redirectFile[i]}','{redirectType[i]}')")
      # process args string to add option
      if (redirectType[i] == "a" or redirectType[i] == "w"):
        args += f",stdout = openFile_{redirectFile[i]}"
      else:
        args += f",stdin = openFile_{redirectFile[i]}"

  lines.append(f"{spaces}subprocess.run({args}) {trailingComment}")

  # close file
  if(isRedirected):
    for i in range(len(redirectType)):
      lines.append(f"{spaces}openFile_{redirectFile[i]}.close()")

def builtInExit(args):
  status = args[0] if (len(args)) else ""
    
  modules.add("sys")
  lines.append(f"{spaces}sys.exit({status}){trailingComment}")
  
def builtInCd(args):
  path = args[0] if (len(args)) else ""

  modules.add("os")
  lines.append(f"{spaces}os.chdir('{path}'){trailingComment}")

def builtInRead(args):
  global spaces
  global spaceLength

  lines.append(f"{spaces}tempRead = input() {trailingComment}")

  # read may have multipal arguments to define multiple variables
  for i in range(len(args)):
    variable = args[i]
    variable = variable.strip("\"'")
    # variable naming validation
    if (variable in validKeywords):
      variables[variable] = variable + "_alternative"
      variable = variable + "_alternative"
    else:
      variables[variable] = variable 

    lines.append(f"{spaces}{variables[variable]} = tempRead.split(' ',maxsplit={len(args) - 1})[{i}]")

def builtInEcho(args):
  # check option -n existence
  optionProvided = False

  if (len(args) and args[0] == "-n"):
    optionProvided = True
    args = args[1:]
  
  formatArgs = transformedArgs(args)
  # convert list of arguments to string format
  formatArgs = stringArgs(formatArgs)
  # print(formatArgs)
  # split line to the redirection character 
  redirectionList = getRedirect(formatArgs)
  
  # remove the line without the rediction option
  formatArgs = redirectionList[0]

  redirectionList.remove(formatArgs)

  # check if we have redirection
  isRedirected = True if len(redirectionList) else False

  redirectType = ""
  redirectFile = ""

  if (len(redirectionList) == 1):
    checkRedirection = re.match(r"(>{1,2}|<)(.*)",redirectionList[0]).group(1)

    if (checkRedirection == ">>"):
      redirectType = "a"
    elif (checkRedirection == ">"):
      redirectType = "w"
    redirectFile = redirectionList[0].lstrip(checkRedirection)
  elif (len(redirectionList) == 2):
    # both redirection are used
    numberArgs = 0
    checkRedirection = re.match(r"(>{1,2}|<)(.*)",redirectionList[numberArgs]).group(1)
    if (checkRedirection == "<"):
      # check second rediection
      numberArgs = 1
      checkRedirection = re.match(r"(>{1,2}|<)(.*)",redirectionList[numberArgs]).group(1)

    if (checkRedirection == ">>"):
      redirectType = "a"
    elif (checkRedirection == ">"):
      redirectType = "w"

    redirectFile = redirectionList[numberArgs].lstrip(checkRedirection)

  if(isRedirected):
    if (expand):
      lines.append(f"{spaces}openFile = open(f'{redirectFile}','{redirectType}')")
    else:
      lines.append(f"{spaces}openFile = open('{redirectFile}','{redirectType}')")
  
  formatString = ""

  if (expand):
    # output f-string since we expanded variables
    formatString = f"{spaces}print(f'{formatArgs}', end='') {trailingComment}" if optionProvided else f"{spaces}print(f'{formatArgs}') {trailingComment}"
  else:
    # output raw string
    formatString = f"{spaces}print('{formatArgs}', end='') {trailingComment}" if optionProvided else f"{spaces}print('{formatArgs}') {trailingComment}"

  if(isRedirected):
    # add file attribute to print method, so that we can output content to file
    if (expand):
      formatString = re.sub(r"(print\(f'.*')(\))",r"\1, file = openFile\2",formatString)
    else:
      formatString = re.sub(r"(print\('.*')(\))",r"\1, file = openFile\2",formatString)

  lines.append(formatString)

  if(isRedirected):
    lines.append(f"{spaces}openFile.close()")

if (len(sys.argv) != 2):
  print("Please provide only 1 argument")
  exit(1)
  
file = open(sys.argv[1],'r')

# set for storing all necessary modules to be imported in the translated python file 
modules = set()

# all variables with their transfromed name, if the defined variable is python keyword or builtIn, transfrom to var_alternative
variables = {}

# all builtIns needs to transform
builtIns = set(["echo","exit","cd","read","test","[","]"])

# all shell syntax keyword needs to transform
keyword = set(["for","while","if","fi","elif","do","done","else","then","case","esac","continue","break",";;"])

# all keyword and builtIn for variable validation
# from https://www.w3schools.com/python/python_ref_keywords.asp
# and https://www.w3schools.com/python/python_ref_functions.asp
validKeywords = set(["and","as","assert","break","class","continue","def","del","elif","else","except","False","finally",
                "for","from","global","if","import","in","is","lambda","None","nonlocal","not","or","pass","raise",
                "return","True","try","while","with","yield","abs","all","any","ascii","bin","bool","bytearry",
                "bytes","callable","chr","classmethod","compile","complex","delattr","dict","dir","divmod","enumerate",
                "eval","exec","filter","float","format","frozenset","getattr","globals","hasattr","hash","help","hex",
                "id","input","int","isinstance","issubclass","iter","len","list","locals","map","max","memoryview",
                "min","next","object","oct","open","ord","pow","print","property","range","repr","reversed","round",
                "set","setattr","slice","sorted","staticmethod","str","sum","super","tuple","type","vars","zip"])

# there may be nested case statement, we need to record the level of case statement to 
inCase = 0

# there may be multiple options in case statement, we need to record the number of matching options for each nested case statement
caseLength = {}

# a single space length, used for remove the space of line in case statement
spaceLength =""

# store all looping counter in for-loop
loopingCounters = []

# all tranfromed lines from the target shell script
lines = []

# global number to record the number of intermediate command we need to execute when parsing $() recursively
number = 0

for line in file:
  # remove trailing space
  line = line.rstrip()
  # script #!  
  if (line == "#!/bin/dash"):
    lines.append("#!/usr/bin/python3 -u")
    continue 

  # current line is empty
  if (line == ""):
    lines.append("")
    continue

  # remove spaces at the beginning of line
  removeSpacesline = line.strip()

  # get leading spaces at the start of each line
  spaces = getSpaces(line)

  # initialize space length
  if (spaceLength == "" and spaces != "" ):
    spaceLength = spaces

  # in case the shell script is not space aligned, adjust alignment
  if (spaceLength != ""):
    spaces = spaceLength * int((len(spaces)/len(spaceLength)))

  # if we are in case statement, adjust space alignment
  if (inCase and removeSpacesline[:4] != "esac"):
    spaces = spaceLength * int((len(spaces) - inCase * len(spaceLength))/len(spaceLength))
  
  # check if current line is comment
  if (removeSpacesline[0] == "#"):
    lines.append((f"{spaces}{removeSpacesline}"))
    continue

  # check and extract comments from the end of each line
  trailingComment = getComments(removeSpacesline)

  if (trailingComment != ""):
    # comment exists, remove it from the end for later parsing
    removeSpacesline = re.sub(f"^(.*){trailingComment}$",r"\1",removeSpacesline)

  # now the current line must be either an external command line tool or shell syntax line

  # process line to get seperate arguments
  args = getArgs(removeSpacesline)

  # put argument of variable assignment into args list
  if (re.match(r"[^ =]+=[^ =]+",removeSpacesline)):
    args = re.split(r"=",removeSpacesline,1)[1:]

  # determine whether we would expand variables or globbing using f-string
  expand = isExpand(args)

  # check if the current line is defining an new variable
  if (re.match(r"[^ =]+=[^ =]+",removeSpacesline)):
    variable = re.split(r"=",removeSpacesline,1)[0]
    value = re.split(r"=",removeSpacesline,1)[1]
    
    # check if variable naming is valid (i.e not using python keyword or builtIn)
    if (variable in validKeywords):
      variables[variable] = variable + "_alternative"
      variable = variable + "_alternative"
    else:
      variables[variable] = variable 

    valueList = []
    valueList.append(value)
    value = transformedArgs(valueList)

    value = stringArgs(value).strip()

    if (expand):
      lines.append(f"{spaces}{variable} = f'{value}' {trailingComment}")
    else:
      lines.append(f"{spaces}{variable} = '{value}' {trailingComment}")

    continue

  # need to determine if the current line is an external command or shell syntax
  firstArg = re.split(r"\s+",removeSpacesline,1)[0]
  if (firstArg in builtIns):
    # current line is builtIn 
    if (firstArg == "exit"):
      builtInExit(args)
      continue
    
    if (firstArg == "cd"):
      builtInCd(args)
      continue

    if (firstArg == "echo"):
      builtInEcho(args)
      continue

    if (firstArg == "read"):
      # print(args)
      builtInRead(args)
      continue
    
    if (firstArg == "test"):
      args.insert(0,firstArg)

      # print(args)
      lastCommand,conditions = getLastCommand(args)

      line = parseArgs(conditions)

      line = re.sub(r"'\"{([^}]+)}\"'",r"\1",line)
      lines.append(f"{spaces}if ({line}): {trailingComment}")

      # comment has been add, clear it to prevent adding it again
      trailingComment = ""

      # adjust spaces to put the external command or buildin under if statement
      if (len(spaceLength) == 0):
        # if the unit of spaceLenght haven't get set, set it by default
        spaceLength = "    " 
      spaces = spaceLength * int(((len(spaces) / len(spaceLength))+ 1))

      if (lastCommand[0] in builtIns):
        if (lastCommand[0] == "exit"):
          builtInExit(lastCommand[1:])
        elif (lastCommand[0] == "cd"):
          builtInCd(lastCommand[1:])
        elif (lastCommand[0] == "echo"):
          builtInEcho(lastCommand[1:])
        elif (lastCommand[0] == "read"):
          builtInRead(lastCommand[1:])
      else:
        externalCommand(lastCommand[1:],lastCommand[0])

      continue

  if (firstArg in keyword):
    if (firstArg == "for"):
      loopingCounter = args[0]

      loopingCounters.append(loopingCounter)
      elements = args[2:]

       
      elements = transformedArgs(elements) 
      # canonical represenation of elements
      elements = repr(elements)

      # replace variable
      elements = re.sub(r"'{([^}]+)}'",r"\1",elements)

      elements = re.sub(r"\"{' '\.join\((sorted\(glob\.glob\('[^']+'\)\))\) if ' '\.join\(\1\) != '' else '[^']+'}\"",r"*(\1)",elements)

      elements = re.sub(r"\*\(sorted\(glob\.glob\('([^']+)'\)\)\)",r"*(sorted(glob.glob('\1')) if sorted(glob.glob('\1')) != [] else ['\1'])",elements)

      outputStr = f"{spaces}for {loopingCounter} in {elements}: {trailingComment}"

      lines.append(outputStr)
      continue

    if (firstArg == "do"):
      if (trailingComment != ""):
        lines.append(f"{spaces}{trailingComment}")
      continue

    if (firstArg == "done"):
      # remove looping counter in for-loop
      if (len(loopingCounters)):
        loopingCounters.pop()

      if (trailingComment != ""):
        lines.append(f"{spaces}{trailingComment}")
      continue

    if (firstArg == "while"):
      line = parseArgs(args)
      line = re.sub(r"'\"{([^}]+)}\"'",r"\1",line)
      lines.append(f"{spaces}while ({line}): {trailingComment}")
      continue

    if (firstArg == "if" or firstArg == "elif" ):
      line = parseArgs(args)
      line = re.sub(r"'\"{([^}]+)}\"'",r"\1",line)
      lines.append(f"{spaces}if ({line}): {trailingComment}")
      continue

    if (firstArg == "fi" or firstArg == "then" or firstArg == ";;"):
      if(trailingComment != ""):
        lines.append(f"{spaces}  {trailingComment}")
      continue
    
    if (firstArg == "else"):
      lines.append(f"{spaces}else:  {trailingComment}")
      continue

    if (firstArg == "continue"):
      lines.append(f"{spaces}continue  {trailingComment}")
      continue

    if (firstArg == "break"):
      lines.append(f"{spaces}break  {trailingComment}")
      continue

    if (firstArg == "case"):
      inCase += 1

      matchingObject = args[0]

      tempList = []
      tempList.append(matchingObject)
    
      matchingObject = transformedArgs(tempList)[0]

      # case pattern matching is globbing 
      modules.add("fnmatch")
      if (expand):
        lines.append(f"{spaces}object_{inCase} = f'{matchingObject}' {trailingComment}")
      else:
        lines.append(f"{spaces}object_{inCase} = '{matchingObject}' {trailingComment}")

      # record number of matching options for current case
      caseLength[inCase] = 0

      continue

    if (firstArg == "esac"):
      inCase -= 1
      if(trailingComment != ""):
        lines.append(f"{spaces}  {trailingComment}")
      continue
  
  # check if current line is case pattern matching option
  if (re.fullmatch(r".*\)",firstArg)):
    patterns = firstArg[:-1]

    # split patterns by |
    patterns = patterns.split("|")

    matchingStrs = ""

    caseLength[inCase] += 1
    
    for i in range(len(patterns)):
      pattern = patterns[i]
      if (i == 0):
        if (len(patterns) == 1):
          matchingStr = f"fnmatch.fnmatchcase(object_{inCase},'{pattern}')"
        else:
          matchingStr = f"(fnmatch.fnmatchcase(object_{inCase},'{pattern}'))"
      else:
        matchingStr = f" or (fnmatch.fnmatchcase(object_{inCase},'{pattern}'))"

      matchingStrs += matchingStr

    # the first matching option in case statement
    if (caseLength[inCase] == 1):
      lines.append(f"{spaces}if({matchingStrs}): {trailingComment}")
    else:
      lines.append(f"{spaces}elif({matchingStrs}): {trailingComment}")

    continue

  # current line is external command
  externalCommand(args,firstArg)

file.close()

"""
output transformed file
"""

print("#!/usr/bin/python3 -u")
lines.remove("#!/usr/bin/python3 -u")

# import all necessary modules for the transformed python file
for module in modules:
  print(f"import {module}")

# output all lines
for line in lines:
  print(line)