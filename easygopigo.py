#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from builtins import input

import sys
import tty
import select
import gopigo
import ir_receiver


old_settings = ''
fd = ''
gpg_debug = False

##########################


def debug(in_str):
    '''
    '''
    if gpg_debug:
        print(in_str)

#############################################################
# the following is in a try/except structure because it depends
# on the date of gopigo.py
#############################################################
try:
    PORTS = {"A1": gopigo.analogPort, "D11": gopigo.digitalPort, "SERIAL": -1}
except:
    PORTS = {"A1": 15, "D11": 10, "SERIAL": -1}


ANALOG = 1
DIGITAL = 0
SERIAL = -1

##########################


class Sensor():
    '''
    Base class for all sensors
    Class Attributes:
        port : string - user-readable port identification
        portID : integer - actual port id
        pinmode : "INPUT" or "OUTPUT"
        pin : 1 for ANALOG, 0 for DIGITAL
        descriptor = string to describe the sensor for printing purposes
    Class methods:
        setPort / getPort
        setPinMode / getPinMode
        isAnalog
        isDigital
    '''
    def __init__(self, port, pinmode):
        '''
        port = one of PORTS keys
        pinmode = "INPUT", "OUTPUT", "SERIAL" (which gets ignored)
        '''
        debug("Sensor init")
        debug(pinmode)
        self.setPort(port)
        self.setPinMode(pinmode)
        if pinmode == "INPUT" or pinmode == "OUTPUT":
            gopigo.pinMode(self.getPortID(), self.getPinMode())

    def __str__(self):
        return ("{} on port {}".format(self.descriptor, self.getPort()))

    def setPort(self, port):
        self.port = port
        self.portID = PORTS[self.port]

    def getPort(self):
        return (self.port)

    def getPortID(self):
        return (self.portID)

    def setPinMode(self, pinmode):
        self.pinmode = pinmode

    def getPinMode(self):
        return (self.pinmode)

    def isAnalog(self):
        return (self.pin == ANALOG)

    def isDigital(self):
        return (self.pin == DIGITAL)

    def set_descriptor(self, descriptor):
        self.descriptor = descriptor
##########################


class DigitalSensor(Sensor):
    '''
    Implements read and write methods
    '''
    def __init__(self, port, pinmode):
        debug("DigitalSensor init")
        self.pin = DIGITAL
        Sensor.__init__(self, port, pinmode)

    def read(self):
        '''
        tries to get a value up to 10 times.
        As soon as a valid value is read, it returns either 0 or 1
        returns -1 after 10 unsuccessful tries
        '''
        okay = False
        error_count = 0
        while not okay and error_count < 10:
            try:
                rtn = int(gopigo.digitalRead(self.getPortID()))
                okay = True
            except:
                error_count += 1
        if error_count > 10:
            return -1
        else:
            return rtn

    def write(self, power):
        self.value = power
        return gopigo.digitalWrite(self.getPortID(), power)
##########################


class AnalogSensor(Sensor):
    '''
    implements read and write methods
    '''
    def __init__(self, port, pinmode):
        debug("AnalogSensor init")
        self.value = 0
        self.pin = ANALOG
        Sensor.__init__(self, port, pinmode)

    def read(self):
        self.value = gopigo.analogRead(self.getPortID())
        return self.value

    def write(self, power):
        self.value = power
        return gopigo.analogWrite(self.getPortID(), power)
##########################


class LightSensor(AnalogSensor):
    """
    Creates a light sensor from which we can read.
    Light sensor is by default on pin A1(A-one)
    self.pin takes a value of 0 when on analog pin (default value)
        takes a value of 1 when on digital pin
    """
    def __init__(self, port="A1"):
        debug("LightSensor init")
        AnalogSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Light sensor")
##########################


class SoundSensor(AnalogSensor):
    """
    Creates a sound sensor
    """
    def __init__(self, port="A1"):
        debug("Sound Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Sound sensor")

##########################


class UltraSonicSensor(AnalogSensor):

    def __init__(self, port="A1"):
        debug("Ultrasonic Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT")
        self.safe_distance = 500
        self.set_descriptor("Ultrasonic sensor")

    def is_too_close(self):
        if gopigo.us_dist(PORTS[self.port]) < self.get_safe_distance():
            return True
        return False

    def set_safe_distance(self,dist):
        self.safe_distance = int(dist)

    def get_safe_distance(self):
        return self.safe_distance

    def read(self):
        return gopigo.us_dist(PORTS[self.port])
##########################


class Buzzer(AnalogSensor):
    '''
    The Buzzer class is a digital Sensor with power modulation (PWM).
    Default port is D11
    Note that it inherits from AnalogSensor in order to support PWM
    It has three methods:
    sound(power)
    soundoff() -> which is the same as sound(0)
    soundon() -> which is the same as sound(254), max value
    '''
    def __init__(self, port="D11"):
        AnalogSensor.__init__(self, port, "OUTPUT")
        self.set_descriptor("Buzzer")

    def sound(self, power):
        '''
        sound takes a power argument (from 0 to 254)
        the power argument will accept either a string or a numeric value
        if power can't be cast to an int, then turn buzzer off
        '''
        try:
            power = int(power)
        except:
            power = 0
        debug(type(power))
        AnalogSensor.write(self, power)

    def sound_off(self):
        '''
        Makes buzzer silent
        '''
        AnalogSensor.write(self, 0)

    def sound_on(self):
        '''
        Maximum buzzer sound
        '''
        AnalogSensor.write(self, 254)
##########################


class Led(AnalogSensor):
    def __init__(self, port="D11"):
        AnalogSensor.__init__(self, port, "OUTPUT")
        self.set_descriptor("LED")

    def light_on(self, power):
        AnalogSensor.write(self, power)
        self.value = power

    def light_off(self):
        AnalogSensor.write(self, 0)

    def is_on(self):
        return (self.value > 0)

    def is_off(self):
        return (self.value == 0)
##########################


class MotionSensor(DigitalSensor):
    def __init__(self, port="D11"):
        DigitalSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Motion Sensor")
##########################


class ButtonSensor(DigitalSensor):

    def __init__(self, port="D11"):
        DigitalSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Button sensor")
##########################

class Remote(Sensor):

    def __init__(self, port):
        Sensor.__init__(self, port, "SERIAL")
        self.set_descriptor("Remote Control")


    def get_remote_code(self):
        '''
        Returns the keycode from the remote control
        No preprocessing
        You have to check that length > 0
            before handling the code value
        '''
        return ir_receiver.nextcode()



if __name__ == '__main__':
    import time
    b = Buzzer()
    print (b)
    print ("Sounding buzzer")
    b.sound_on()
    time.sleep(1)
    print ("buzzer off")
    b.sound_off()
