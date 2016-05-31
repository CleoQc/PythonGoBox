import gobox
import gopigo
import atexit

@atexit.register
def cleanup():
    try:
        gopigo.stop()
        buzzer.soundof()
    except:
        pass
        
try:
    input = raw_input
except NameError:
    pass

buzzer = gobox.Buzzer()
in_value = input("What would you like to set the buzzer to? ")
print (type(in_value))
