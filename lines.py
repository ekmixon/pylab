#!/usr/bin/env python

import re

filepath = '/Users/andy/range.txt'
regex = re.compile('fa')
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
