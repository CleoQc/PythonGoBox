import gobox
import gopigo
import time
import atexit

@atexit.register
def cleanup():
    gopigo.stop()
    giveAnswer()   # on exit, we want to give the answer via the LED
    
    
# we create this function here that will output the answer
# it will blink the led based on how many times the lights
# were switched on
def giveAnswer():
    print ("giving the answer")
    for x in range(count):
        myled.lighton(255)
        time.sleep(0.5)
        myled.lightoff()
        time.sleep(0.5)

# this is our variable that keeps count of how many times the lights were turned on
count = 0  

# Keep track of the state. 1 = lights are on, 0 = lights are off
state = 1

# this is our threshold. You may want to modify this
threshold = 400

# let's create a software light sensor
mylightsensor = gobox.LightSensor()

# and a software LED
myled = gobox.Led()

# loop forever
# possible modification: loop for a certain number of times
#                        and call giveanswer() afterwards
while True:
    # wait a second before each loop
    # only real reason for this is so we can read the messages
    # that get printed to the screen
    time.sleep(1) 
    
    # query the light sensor
    current_light_value = mylightsensor.read()
    
    # our STATE MACHINE in action!
    if state == 0:   # lights are currently off
        if current_light_value < threshold:  # and they're still off
            print ("It was dark and it is still dark")
        else:  # but they've been turned on! Keep track!
            print ("It was dark but now it is light, lights were turned on, adding to count")
            state = 1
            count += 1
    else:  # lights are currently on
        if current_light_value < threshold:  # but we're not in the dark!
            print("it was light but now it is dark")
            state = 0
        else: # and they're still on
            print("it was light and it is still light")


