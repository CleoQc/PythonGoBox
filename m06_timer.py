import time
import gobox
import gopigo
import atexit

@atexit.register
def cleanup():
    gopigo.stop()
    mybuzzer.soundoff()
    
# The following is just a trick to ensure compatibility between Python 2 and 3
try:
    input = raw_input   #python 2
except NameError:
    pass    # python 3


# let's create a software buzzer so we can control it
mybuzzer = gobox.Buzzer()    

# Ask the user for how many seconds we need to wait
# and confirm back to the user how long we'll be waiting
how_long = int(input("How many seconds before I need to buzz? "))
print("I will alert you in %d seconds" % how_long)

# wait for that many seconds
time.sleep(how_long)

# start buzzing
for i in range(5):
    mybuzzer.sound(254)
    gopigo.left_rot()   # this line will make the robot spin in place
    time.sleep(5)
    mybuzzer.soundoff()
    gopigo.stop()
    time.sleep(1)

