import gobox
import gopigo
import time

with gobox.KeyPoller() as keyPoller:
    while True:
        print "non blocking"
        while True:
            print ".",   # this is to verify this code is non blocking
            c = keyPoller.poll()
            if not c is None:
                if c == "c":
                    break
                print c
        print "blocking"
        while True:
            print "!"  # this print is to verify this code is indeed blocking
            c = keyPoller.readKey()
            if not c is None:
                if c == "c":
                    break
                print str(c)
