# import some outside helper libraries
# they contain code that is available for us to use
# and simplify our life

import gobox    # specific library for gobox curriculum
import gopigo   # generic library for gopigo
import atexit   # library that will give us a nice exit

@atexit.register
def cleanup():
    print ("Good bye!")
    gopigo.stop()

# ASCII code for the spacebar
# we define this constant in order to make the code more readable
SPACEBAR=32

# create a light sensor instance
light = gobox.LightSensor()

while True:
        # then check light sensor value
        # take decision to go forward or to stop
        lightValue = light.read()
        print(lightValue)
        if lightValue > 500:
            # print ("Going Forward")
            gopigo.fwd()
        else:
            # print ("Stopping") 
            gopigo.stop()

