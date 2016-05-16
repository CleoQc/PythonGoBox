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


PORTS={"A1":gopigo.analogPort,"D11":gopigo.digitalPort}

class Sensor():
    def __init__(self, port, pinmode):
        '''
        port = one of PORTS keys
        pinmode = "INPUT", "OUTPUT"
        '''
        print "Sensor init" 
        self.port=port
        self.portID=PORTS[self.port]
        self.pinmode=pinmode
 
    def setPort(self,port):
        self.port=port
        self.portID =PORTS[self.port]
    def getPort(self):
        return (self.port)
    def getPortID(self):
        return (self.portID)
    def setPinMode(self,pinmode):
        self.pinmode=pinmode
    def getPinMode(self):
        return (self.pinmode)
    def isAnalog(self):
        return (self.pin == ANALOG)
    def isDigital(self):
        return (self.pin == DIGITAL)


class DigitalSensor(Sensor):
    def __init__(self,pin):
        print "DigitalSensor init" 
        self.setPinMode="INPUT"

    def read(self):
        if self.pin == DIGITAL: 
            return gopigo.digitalRead(self.getPortID())

class AnalogSensor(Sensor):
    def __init__(self,port):
        print "AnalogSensor init" 
        self.setPort(port) # "A1"
        self.setPinMode("INPUT")
        print (self.getPortID(), self.getPinMode())
        gopigo.pinMode(self.getPortID(),self.getPinMode())

    def read(self):
        return gopigo.analogRead(self.getPortID())
        
class LightSensor(AnalogSensor):
    """
    Creates a light sensor from which we can read.
    Light sensor is by default on pin A1(A-one)
    self.pin takes a value of 0 when on analog pin (default value)
	     takes a value of 1 when on digital pin
             D11 is used here to match what is written on the board
    """
    def __init__(self, port="A1"):
        print "LightSensor init" 
        AnalogSensor.__init__(self, port)
 


   