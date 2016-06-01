import gobox
import gopigo
import atexit
import time

@atexit.register
def cleanup():
    print("Good bye!")

# check an ASCII table
# https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/ASCII-Table-wide.svg/2000px-ASCII-Table-wide.svg.png
b=98
while gobox.readKey() != b:
	print ("Hello")
print("Thank you for letting me stop!")

