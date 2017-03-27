#!/usr/bin/python
# Selects a poem based on the date and print it.

from __future__ import print_function
from Adafruit_Thermal import *
import time

# Choose the poem to print, by date
mm, dd, yyyy = time.strftime("%m/%d/%Y").split("/")
poem_path = "allpoems/poems/" + dd + ".txt"

# Read the poem file
with open(poem_path) as poem_file:
    poem_lines = poem_file.read().splitlines()

# Get the title and author (first and second lines)
title = poem_lines.pop(0)
author = poem_lines.pop(1)

# Open connection to printer and print poem
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer.setSize('M')
printer.println(title)
printer.setSize('M')
printer.println(author + "\n")
printer.setSize('S')
for line in lines:
    printer.println(line)
printer.feed(3)

# Reset everything for next print
printer.sleep()
printer.wake()
printer.setDefault()
