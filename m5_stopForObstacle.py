import gobox
import gopigo
import time
import atexit

@atexit.register
# this will be called if the program is killed via 
# a Ctrl-C on the keyboard or any other reason
def cleanup():
	gopigo.stop()
	
	
# Let's start the GoPiGo. 
# this command only needs to be given once 
# GoPiGo will keep going forward until told to stop
gopigo.fwd()

# Note the absence of Wait code, or time.sleep in Python
# As GoPiGo is not using broadcast events in Python
# there's no need to space the queries out
# It's possible to loop as quickly as possible
# and get precise behavior.
while True:
	dist = gopigo.us_dist(gopigo.analogPort)
	# in case of error the above function can return a value of -1
	# there's a danger here if we simply check for less than 40
	if dist > 0 and dist < 40:
		gopigo.stop()
		break  # this break forces the while loop to quit

