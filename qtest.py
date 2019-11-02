#!/usr/bin/python3

#from queue import Queue
#import queue as Queue
#import queue as Queue
from queue import Queue
import threading

d = Queue()
def consumer():
    print('consumer waiting')
    n = d.get()
    print('consumer got:')
    print(n)

thread = threading.Thread(target=consumer)
thread.start()

print('Producer putting')
d.put([15,'foo.pl'])
print(d)
thread.join()
print('Producer done')
