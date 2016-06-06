import gobox
import gopigo
import atexit
import time
import pprint  # this is called pretty print, and allows for better printing
@atexit.register
def cleanup():
    gopigo.stop()
    
# let's create an empty data list
earthquakeData = []

myMotionSensor = gobox.MotionSensor()

for i in range(100):  # loop 100 times
    current_earthwake = myMotionSensor.read()
    earthquakeData.append(current_earthwake)
    time.sleep(0.25)


# compare these two methods of printing a list
print(earthquakeData)
#pprint.pprint(earthquakeData)
    

# write to a file
# the file will be on your Desktop
f = open('/home/pi/Desktop/earthquakedata.txt', 'w')
for i in range(len(earthquakeData)):
	f.write(earthquakeData[i])
	f.write("\n")  # this means a new line, or Enter key in a word processor
f.close()  # this saves the file, same as File/Save in a word processor
