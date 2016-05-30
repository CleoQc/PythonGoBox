
# helper libraries
import gobox
import time
import sys



# create a software version of the LightSensor so we can interact with it
light = gobox.LightSensor()


# let's create a loop that will print out the value of the light sensor
# this will loop 100 times
for i in range(0,20): 
    sensorvalue = light.read()
    print( sensorvalue) # get a Light reading and print it
    time.sleep(0.5) # there will be half a second between readings
    
