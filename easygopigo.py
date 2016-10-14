#!/usr/bin/env python 

# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios
import select
import gopigo

old_settings=''
fd=''
gpg_debug = False

##########################
def debug(in_str):
    if gpg_debug:
        print(in_str)

##########################
# Ensure compatibility with Python 2 and 3
##########################
try:
    input = raw_input
except NameError:
    pass

#############################################################
# the following is in a try/except structure because it depends 
# on the date of gopigo.py
#############################################################
try:
    PORTS={"A1":gopigo.analogPort,"D11":gopigo.digitalPort}
except:
    PORTS={"A1":15,"D11":10}

ANALOG = 1
DIGITAL = 0

##########################
class Sensor():
    def __init__(self, port, pinmode):
        '''
        port = one of PORTS keys
        pinmode = "INPUT", "OUTPUT"
        '''
        debug ("Sensor init" )
        debug(pinmode)
        self.setPort(port)
        self.setPinMode(pinmode)
        gopigo.pinMode(self.getPortID(),self.getPinMode())
 
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


##########################
class DigitalSensor(Sensor):
    def __init__(self,port,pinmode):
        debug ("DigitalSensor init" )
        self.pin = DIGITAL
        Sensor.__init__(self,port,pinmode)

    def read(self):
        return str(gopigo.digitalRead(self.getPortID()))

##########################
class AnalogSensor(Sensor):
    def __init__(self,port,pinmode):
        debug( "AnalogSensor init" )
        self.value = 0
        self.pin = ANALOG
        Sensor.__init__(self,port,pinmode)

    def read(self):
        self.value = gopigo.analogRead(self.getPortID())
        return self.value
        
    def write(self, power):
        self.value = power
        return gopigo.analogWrite(self.getPortID(),power)
    
        
##########################
class LightSensor(AnalogSensor):
    """
    Creates a light sensor from which we can read.
    Light sensor is by default on pin A1(A-one)
    self.pin takes a value of 0 when on analog pin (default value)
        takes a value of 1 when on digital pin
    D11 is used here to match what is written on the board
    """
    def __init__(self, port="A1"):
        debug ("LightSensor init" )
        AnalogSensor.__init__(self, port,"INPUT")
 

##########################
class SoundSensor(AnalogSensor):
    """
    Creates a a sound sensor
    """
   
    def __init__(self,port="A1"):
        debug ("Sound Sensor on port "+port)
        AnalogSensor.__init__(self,port,"INPUT")
  
##########################      
class UltraSonicSensor(AnalogSensor):
    def __init__(self,port="A1"):
        debug ("Ultrasonic Sensor on port "+port)
        AnalogSensor.__init__(self,port,"INPUT")
        debug( PORTS[port])
        
    def read(self):
        return gopigo.us_dist(PORTS[self.port])

##########################
class Buzzer(AnalogSensor):
    def __init__(self,port="D11"):
        AnalogSensor.__init__(self,port,"OUTPUT")
        
    def sound(self,power):
        # sound will accept either a string or a numeric value
        # if power can't be cast to an int, then turn buzzer off
        debug(type(power))
        try:
            power = int(power)
        except:
            power = 0
        debug(type(power))
        AnalogSensor.write(self,power)
        
    def soundoff(self):
        AnalogSensor.write(self,0)
        
        
##########################
class Led(AnalogSensor):
    def __init__(self,port="D11"):
        AnalogSensor.__init__(self,port,"OUTPUT")
        self.power = 0  # current power level being fed 
        
    def lighton(self,power):
        AnalogSensor.write(self,power)
        self.value = power
        
    def lightoff(self):
        AnalogSensor.write(self,0)
        
    def ison(self):
        return (self.value>0)
    
    def isoff(self):
        return (self.value==0)
        

##########################
class MotionSensor(DigitalSensor):
    def __init__(self,port="D11"):
        DigitalSensor.__init__(self,port,"INPUT")

    def read(self):
	value = DigitalSensor.read(self)
	return int(value)
        



