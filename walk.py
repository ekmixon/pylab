#!/usr/bin/env python

import os
import sys

# Set the directory you want to start from
rootDir = sys.argv[1]
gitpath = rootDir + '/.git'
for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        print('%s/%s' % (dirpath, fname))
