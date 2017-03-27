#!/usr/bin/python

from __future__ import print_function
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

printer.setSize('S')   # Set type size, accepts 'S', 'M', 'L'
printer.print('test text')

printer.feed(1)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
