import gobox
import gopigo
import atexit

@atexit.register
def cleanup():
    try:
        gopigo.stop()
        buzzer.soundoff()
    except:
        pass

# The following is just a trick to ensure compatibility between Python 2 and 3
try:
    input = raw_input
except NameError:
    pass
    
buzzer = gobox.Buzzer()
while True:
    in_value = input("What would you like to set the buzzer to? ")
    buzzer.sound(in_value)

