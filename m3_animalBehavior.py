# import some outside helper libraries
# they contain code that is available for us to use
# and simplify our life
import easygopigo           # gopigo functions
import atexit               # library that will give us a nice exit

# this registers a function that will be called
# each time the code ends, and regardless
# of why it ends (intentional or not)
@atexit.register
def cleanup():
    gopigo.stop()  # we want the gopigo to stop
    print ("Good bye!")

# name the light sensor in our code so we can control it
# you get to name it. Right now its name is my_light
# if you change that, you need to change it when reading it
# REMINDER: the light sensor goes into Port A1
my_light = easygopigo.LightSensor()

# this is the same as a Scratch forever loop
while True:

        # we don't need to broadcast anything before reading the value
        # one of the advantages of Python!
        # we can read the sensor directly

        #  check light sensor value
        lightValue = my_light.read()
        print(lightValue)

        # take decision to go forward or to stop
        if lightValue > 500:
            # print ("Going Forward")
            gopigo.forward()
        else:
            # print ("Stopping") 
            gopigo.stop()

