from easygopigo import *
from gopigo import *
from time import sleep


import ir_receiver

import atexit               # library that will give us a nice exit

# this registers a function that will be called
# each time the code ends, and regardless
# of why it ends (intentional or not)
@atexit.register
def cleanup():
    stop()  # we want the gopigo to stop
    print ("Good bye!")


# this is a variable that holds our security distance
# you may want to change it to get it more sensitive, or less
distance_to_stop=20


def safe_in_front():
    '''
    We create our own function to check the distance sensor
    It will return either True or False after
        checking for an object in front.
    '''
    if us_dist(15) <= distance_to_stop:
    # oh oh, danger! danger! Stop
        return False
    else:
        return True



print "Press any button on the remote to control the GoPiGo"
print "Use the * or the # to end the program"

# infinite loop
while True:

    # check if there's something in front
    # if there is, stop, even if GoPiGo is going backward
    # the GoPiGo will stop if the cat walks in front of it while
    #   it's going backward
    # your chosen behavior may be different
    if not safe_in_front():
        stop()

    code = ir_receiver.nextcode()

    # if  we didn't receive a code, loop right away
    if len(code) != 0:

        if code == 'KEY_UP':
            # check if it's safe to go forward first.
            if safe_in_front():
                forward()
        elif code == 'KEY_DOWN':
            backward()
        elif code == 'KEY_OK':
            stop()
        elif code=="KEY_LEFT":
            left()
        elif code=="KEY_RIGHT":
            right()
        elif code == 'KEY_H' or code == 'KEY_S':
            exit(0)

    sleep(0.1)

