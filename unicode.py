#!/usr/bin/env python

import re

filepath = 'README_win32.pod'
regex = re.compile('fa')
with open(filepath, 'r', encoding='ISO8859') as fh:
    n = 0
    while line := fh.readline():
        print(line)
        n += 1
        line = line.rstrip()
        if match := re.search(regex, line):
            print(line)
    fh.close()
