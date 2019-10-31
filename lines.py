#!/usr/bin/env python


filepath = '/Users/andy/range.txt'
with open( filepath, 'r' ) as fh:
    n = 0
    line = fh.readline()
    while line:
        n += 1
        print( line )
        line = fh.readline()
    fh.close()
