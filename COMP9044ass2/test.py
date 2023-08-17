#!/usr/bin/python3 -u
import sys
import subprocess
import os
start = '13' 
if (int(str(len(sys.argv) - 1).strip()) > int(str('0').strip())): 
    start = f'{sys.argv[1]}' 
i = '0' 
number = f'{start}' 
file = './tmp.numbers' 
subprocess.run(['rm', '-f', file]) 
while (True): 
    if (os.access('{file}',os.R_OK)): 
        if (not subprocess.run(['fgrep', '-x', '-q', number, file]).returncode): 
            print('Terminating: series is repeating') 
            sys.exit(0)
    openFile = open(f'{file}','a')
    print(f'{number}', file = openFile) 
    openFile.close()
    print(f'{i} {number}') 
    k = f'{subprocess.run(["expr", number, "%", "2"], text=True, stdout=subprocess.PIPE).stdout.rstrip()}' 
    if (int(str(k).strip()) == int(str('1').strip())): 
        number = f'{subprocess.run(["expr", "7", "*", number, "+", "3"], text=True, stdout=subprocess.PIPE).stdout.rstrip()}' 
    else:  
        number = f'{subprocess.run(["expr", number, "/", "2"], text=True, stdout=subprocess.PIPE).stdout.rstrip()}' 
    i = f'{subprocess.run(["expr", i, "+", "1"], text=True, stdout=subprocess.PIPE).stdout.rstrip()}' 
    if (int(str(number).strip()) > int(str('100000000').strip()) or int(str(number).strip()) < int(str('-100000000').strip())): 
        print('Terminating: too large') 
        sys.exit(0)
subprocess.run(['rm', '-f', file]) 
