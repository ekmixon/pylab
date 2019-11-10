#!/usr/bin/env python


n = 0

def thing():
    global n
    n += 1
    return n

def main():
    while (x = thing()) is not None:
        print(x)

main()
