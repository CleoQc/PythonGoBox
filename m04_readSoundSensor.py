import easygopigo
import atexit
import time

@atexit.register
def cleanuo():
   print("Good bye!")
   gopigo.stop()

mySoundSensor=easygopigo.SoundSensor()

while True:
    soundValue = mySoundSensor.read()
    print(soundValue)
    time.sleep(1)
