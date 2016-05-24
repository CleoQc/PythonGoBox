import gobox
import gopigo
import time

with gobox.KeyPoller() as keyPoller:
    while True:
        print "non blocking"
        while True:
            print ".",
            c = keyPoller.poll()
            if not c is None:
                if c == "c":
                    break
                print c
        print "blocking"
        while True:
            print "!"
            c = keyPoller.readKey()
            if not c is None:
                if c == "c":
                    break
                print str(c)
