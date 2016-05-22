# import some outside helper libraries
# they contain code that is available for us to use
# and simplify our life

import gobox    # specific library for gobox curriculum
import gopigo   # generic library for gopigo

# ASCII code for the spacebar
# we define this constant in order to make the code more readable
SPACEBAR=32

# this is just in case we run into an issue. At least the GoPiGo will stop
gopigo.stop()

# create a light sensor instance
light = gobox.LightSensor()

try:
    # ask for a keypress and display it
    keypressed = gobox.readKey()
    print (keypressed)

    # if SPACEBAR has been pressed, launch the animal
    if (keypressed == SPACEBAR):
        # start a forever loop
        while True:
                # then check light sensor value
                # take decision to go forward or to stop
                lightValue = light.read()
                if lightValue > 500:
                    # print ("Going Forward")
                    gopigo.fwd()
                else:
                    # print ("Stopping") 
                    gopigo.stop()
except:
    pass
finally:
    print("ending" )
    gopigo.stop()

