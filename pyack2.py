#!/usr/bin/env python3

# pyack.py but with threads.

import os
import sys
import re

from queue import Queue
import threading

q = Queue()

def findhits():
    while 1:
        filepath, regex = q.get()
        if filepath is None:
            return

        any_printed = False
        with open(filepath, 'r', encoding='ISO8859') as fh:
            n = 0
            while line := fh.readline():
                n += 1
                if match := regex.search(line):
                    if not any_printed:
                        print(filepath)
                        any_printed = True
                    line = line.rstrip()
                    print(f'{n}: {line}')
            fh.close()

thread = threading.Thread(target=findhits)
thread.start()

# Set the directory you want to start from
text_regex = sys.argv[1]
rootDir = sys.argv[2]
gitpath = f'{rootDir}/.git'
regex = re.compile(text_regex)


swapfile_regex = re.compile('\\.swp$')
tilde_regex = re.compile('~$')
graphic_regex = re.compile('\\.(png|ico|gif)$')
garbage_regex = re.compile('\\.(pbc|gz)$')
for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        if fname == 'string_cs.t':
            continue
        if fname == 'POD2HTML.pm':
            continue
        if swapfile_regex.search(fname):
            continue
        if tilde_regex.search(fname):
            continue
        if graphic_regex.search(fname):
            continue
        if garbage_regex.search(fname):
            continue
        # Put our file in the queue, rather than calling findhits
        q.put([f'{dirpath}/{fname}', regex])

# Tell the findhits to stop
q.put([None,None])
thread.join()
