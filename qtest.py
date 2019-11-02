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
    print('consumer got ' + str(n))

thread = threading.Thread(target=consumer)
thread.start()

print('Producer putting')
d.put(15)
d.put(29)
d.put(44)
print(d)
thread.join()
print('Producer done')
