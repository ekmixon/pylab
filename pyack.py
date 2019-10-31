#!/usr/bin/env python

import os
import sys
import re

def findhits(filepath, regex):
    any_printed = False
    with open(filepath, 'r') as fh:
        n = 0
        line = ''
        try:
            line = fh.readline()
        except (UnicodeDecodeError):
            print("Got a unicode error: " + filepath)
            pass
        while line:
            n += 1
            line = line.rstrip()
            match = re.search(regex, line)
            if match:
                if not any_printed:
                    print(filepath)
                    any_printed = True
                print(str(n) + ': ' + line)
            line = fh.readline()
        fh.close()

# Set the directory you want to start from
text_regex = sys.argv[1]
rootDir = sys.argv[2]
gitpath = rootDir + '/.git'
regex = re.compile(text_regex)


swapfile_regex = re.compile('\.swp$')
tilde_regex = re.compile('~$')
for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        if re.search(swapfile_regex, fname):
            continue
        if re.search(tilde_regex, fname):
            continue
        findhits(dirpath + '/' + fname, regex)

