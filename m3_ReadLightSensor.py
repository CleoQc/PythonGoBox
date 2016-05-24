#!/usr/bin/env python 

# helper libraries
import gobox
import time
import sys
import atexit

@atexit.register
def cleaup():
    print("Good bye")

# this 32 comes from the ASCII table. It represents the spacebar
SPACEBAR = 32

# create a software version of the LightSensor so we can interact with it
light = gobox.LightSensor()

# create a software version of the keyboard so we can check for key inputs
keyb = gobox.KeyPoller()
while True: # forever loop
    if (keyb.readKey() == SPACEBAR):  # wait for spacebar to be pressed
        print( light.read()) # get a Light reading and print it
    
