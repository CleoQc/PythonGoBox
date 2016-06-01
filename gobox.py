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
class KeyPoller():
    def __enter__(self):
        debug ("enter fct")
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        debug ("exit fct")
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        """
           non-blocking method to get one character input from keyb
        """
        dr,dw,de = select.select([sys.stdin], [], [], 0)
        if not dr == []:
            return sys.stdin.read(1)
        return None

    def readKey(self):
        """
           blocking method to get one character input from keyb
        """
        debug ("readKey fct")
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ord(ch) == 3 or ord(ch) == 0x1b: # detect CtrlC or ESC
            raise KeyboardInterrupt
        return ch

#############################################################
# the followin is in a try/except structure because it depends 
# on the date of gopigo.py
#############################################################
try:
    PORTS={"A1":gopigo.analogPort,"D11":gopigo.digitalPort}
except:
    PORTS={"A1":15,"D11":10}

##########################
class Sensor():
    def __init__(self, port, pinmode):
        '''
        port = one of PORTS keys
        pinmode = "INPUT", "OUTPUT"
        '''
        debug ("Sensor init" )
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


##########################
class DigitalSensor(Sensor):
    def __init__(self,pin):
        debug ("DigitalSensor init" )
        self.setPinMode="INPUT"

    def read(self):
        if self.pin == DIGITAL: 
            return gopigo.digitalRead(self.getPortID())

##########################
class AnalogSensor(Sensor):
    def __init__(self,port):
        debug( "AnalogSensor init" )
        self.setPort(port) # "A1"
        self.setPinMode("INPUT")
        self.value = 0
        debug (str(self.getPortID())+", " +str(self.getPinMode()))
        gopigo.pinMode(self.getPortID(),self.getPinMode())

    def read(self):
        return gopigo.analogRead(self.getPortID())
        
    def write(self, power):
        return gopigo.analogWrite(self.getPortID(),power)
    
    def set_value(self,value):
        self.value = value
        return self.value

    def get_value(self):
        return self.value
        
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
        AnalogSensor.__init__(self, port)
 

##########################
class SoundSensor(AnalogSensor):
    """
    Creates a a sound sensor
    """
   
    def __init__(self,port="A1"):
        debug ("Sound Sensor on port "+port)
        AnalogSensor.__init__(self,port)
  
##########################      
class UltraSonicSensor(AnalogSensor):
    def __init__(self,port="A1"):
        debug ("Ultrasonic Sensor on port"+port)
        AnalogSensor.__init__(self,port)
        debug( PORTS[port])
        
    def distance(self):
        return gopigo.us_dist(PORTS[port])

##########################
class Buzzer(AnalogSensor):
    def __init__(self,port="A1"):
        AnalogSensor.__init__(self,port)
        
    def sound(self,power):
        self.set_value(power)
        AnalogSensor.write(self,power)
        
    def soundoff(self):
        AnalogSensor.write(self,0)
##########################
