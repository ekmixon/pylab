#!/usr/bin/env python3

# pyack.py but with threads.

import os
import sys
import re

swapfile_regex = re.compile('\\.swp$')
tilde_regex = re.compile('~$')
graphic_regex = re.compile('\\.(png|ico|gif)$')
garbage_regex = re.compile('\\.(pbc|gz)$')

def findhits(filepath):
    print(filepath)

def filefilter(filepath):
    if filepath == 'string_cs.t':
        return
    if filepath == 'POD2HTML.pm':
        return
    if swapfile_regex.search(filepath):
        return
    if tilde_regex.search(filepath):
        return
    if graphic_regex.search(filepath):
        return
    if garbage_regex.search(filepath):
        return
    findhits(filepath)

# Set the directory you want to start from
rootDir = sys.argv[1]
gitpath = rootDir + '/.git'

for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for i in filenames:
        filefilter(dirpath + '/' + i)
