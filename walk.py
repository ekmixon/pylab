#!/usr/bin/env python

import os
import sys

# Set the directory you want to start from
rootDir = sys.argv[1]
gitpath = f'{rootDir}/.git'


# https://docs.python.org/3.3/library/os.html?highlight=os.walk#os.walk
for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        print(f'{dirpath}/{fname}')
