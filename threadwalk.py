#!/usr/bin/env python3

# pyack.py but with threads.

import os
import sys
import re

from queue import Queue
import threading

search_queue = Queue()
filter_queue = Queue()

def findhits():
    while 1:
        filepath, regex = search_queue.get()
        if filepath is None:
            return
        print(filepath)

def filefilter():
    swapfile_regex = re.compile('\\.swp$')
    tilde_regex = re.compile('~$')
    graphic_regex = re.compile('\\.(png|ico|gif)$')
    garbage_regex = re.compile('\\.(pbc|gz)$')
    while 1:
        filepath, regex = filter_queue.get()
        if filepath is None:
            search_queue.put([None,None])
            return
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
        search_queue.put([filepath, regex])

search_thread = threading.Thread(target=findhits)
search_thread.start()

filter_thread = threading.Thread(target=filefilter)
filter_thread.start()

# Set the directory you want to start from
rootDir = sys.argv[1]
gitpath = rootDir + '/.git'
regex = re.compile('x')

for dirpath, dirnames, filenames in os.walk(rootDir):
    if dirpath == gitpath:
        dirnames[:] = []
        continue
    dirnames.sort()
    filenames.sort()
    for fname in filenames:
        filter_queue.put([dirpath + '/' + fname, regex])

# Tell the findhits to stop
filter_queue.put([None,None])
search_thread.join()
filter_thread.join()
