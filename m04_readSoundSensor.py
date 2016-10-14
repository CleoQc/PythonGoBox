from easygopigo import *
from time import sleep
import atexit

@atexit.register
def cleanuo():
   print("Good bye!")
   stop()

mySoundSensor=SoundSensor()

while True:
    soundValue = mySoundSensor.read()
    print(soundValue)
    sleep(1)
