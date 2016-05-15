#!/usr/bin/env python 

# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios
import gopigo
import time

old_settings=''
fd=''

##########################
def readKey():
    """
       blocking method to get one character input from keyb
    """
    global old_settings
    global fd
    fd = sys.stdin.fileno()

    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ord(ch) == 3 or ord(ch) == 0x1b:  # detect Ctrl C or ESC
        raise KeyboardInterrupt
    return ord(ch)



class Sensor():
    def __init__(self, pin):
        self.pin=0
        if pin == "A1":
            self.pin=0
#            print ("Setting port to A1")
            gopigo.pinMode(gopigo.analogPort,"INPUT")
        if pin == "D11":
            self.pin=1
#            print ("Setting port to D11")
            gopigo.pinMode(dgopigo.igitalPort,"INPUT")

    def read(self):
        if self.pin == 0: 
            return gopigo.analogRead(gopigo.analogPort)
        if self.pin == 1: 
            return gopigo.digitalRead(gopigo.digitalPort)

class LightSensor(Sensor):
    """
    Creates a light sensor from which we can read.
    Light sensor is by default on pin A1(A-one)
    self.pin takes a value of 0 when on analog pin (default value)
	     takes a value of 1 when on digital pin
             D11 is used here to match what is written on the board
    """
    def __init__(self, pin="A1"):
        Sensor.__init__(self,pin)


   
