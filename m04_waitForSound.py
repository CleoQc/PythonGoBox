import easygopigo
import atexit

@atexit.register
def cleanup():
    gopigo.stop()
    print("good bye!")


# Create a Sound Sensor variable
mySoundSensor = easygopigo.SoundSensor()

# Set desired threshold
myThreshold=50

# start a Forever loop
while True:
    # read the sensor
    mySoundLevel = mySoundSensor.read()

    # if above threshold, then go on attack mode !
    if mySoundLevel > myThreshold:
        gopigo.fwd()
    else:
        gopido.stop()

