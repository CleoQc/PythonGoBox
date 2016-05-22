#!/usr/bin/env python 

import gobox
import time
import sys

SPACEBAR = 32
light = gobox.LightSensor()

while True:
    try:
        if (gobox.readKey() == SPACEBAR):
            print( light.read())
            time.sleep(0.5)
    except KeyboardInterrupt:
        sys.exit()
    
