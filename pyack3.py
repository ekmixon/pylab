#!/usr/bin/env python3

# pyack.py but with threads.

import os
import sys
import re

from queue import Queue
import threading

search_queue = Queue()
filter_queue = Queue()

global regex
global filter_regex

def findhits():
    while 1:
        filepath, regex = search_queue.get()
        if filepath is None:
            return

        any_printed = False
        with open(filepath, 'r', encoding='ISO8859') as fh:
            n = 0
            line = fh.readline()
            while line:
                n += 1
                match = regex.search(line)
                if match:
                    line = line.rstrip()
                    print(filepath+':'+str(n)+':'+line)
                line = fh.readline()
            fh.close()

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
        if filepath == 'string_cs.t':
            continue
        if filepath == 'POD2HTML.pm':
            continue
        if swapfile_regex.search(filepath):
            continue
        if tilde_regex.search(filepath):
            continue
        if graphic_regex.search(filepath):
            continue
        if garbage_regex.search(filepath):
            continue
        # Put our file in the queue, rather than calling findhits
        with open(filepath, 'r', encoding='ISO8859') as f:
            block = f.read(1000000)
            match = filter_regex.search(block)
            if match:
                search_queue.put([filepath, regex])
            f.close()

search_thread = threading.Thread(target=findhits)
search_thread.start()

filter_thread = threading.Thread(target=filefilter)
filter_thread.start()

# Set the directory you want to start from
text_regex = sys.argv[1]
rootDir = sys.argv[2]
gitpath = rootDir + '/.git'
regex = re.compile(text_regex)
filter_regex = re.compile(text_regex, re.M | re.S)

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
