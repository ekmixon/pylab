#!/usr/bin/env python

import os
import sys
import re

def findhits(filepath, regex):
    print('looking in ' + filepath)
    with open(filepath, 'r') as fh:
        n = 0
        line = fh.readline()
        while line:
            n += 1
            line = line.rstrip()
            match = re.search(regex, line)
            if match:
                print(line)
            line = fh.readline()
        fh.close()

# Set the directory you want to start from
rootDir = sys.argv[1]
gitpath = rootDir + '/.git'

regex = re.compile('f9')


for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        findhits(dirpath + fname, regex)

