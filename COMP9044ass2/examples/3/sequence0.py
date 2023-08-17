#!/usr/bin/python3 -u

import subprocess
import sys

# print a contiguous integer sequence

start = sys.argv[1]
finish = sys.argv[2]

number = start
while int(number.strip()) <= int(finish):
    print(number.strip())
    number = subprocess.run(['expr', number, '+', '1'], text=True, stdout=subprocess.PIPE).stdout # increment number
