import gopigo # this has all the functions related to GoPiGo; not sensors
import time # Python library that allows us to deal with time

print ("Going Forward")
gopigo.fwd()
time.sleep(1)
print ("Going Backward")
gopigo.bwd()
time.sleep(1)
print ("Turning to the left")
gopigo.left()
time.sleep(0.5)
print ("Spinning left")
gopigo.left_rot()
time.sleep(0.5)
print ("Stopping")
gopigo.stop()
