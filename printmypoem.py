#!/usr/bin/python

# Current time and temperature display for Raspberry Pi w/Adafruit Mini
# Thermal Printer.  Retrieves data from DarkSky.net's API, prints current
# conditions and time using large, friendly graphics.
# See forecast.py for a different weather example that's all text-based.
# Written by Adafruit Industries.  MIT license.
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
from Adafruit_Thermal import *
import os, random

# Choose the poem to print
poems = os.listdir("poems")
choice = random.randint(0, len(poems))
poem = poems[choice]

# Get the title and author
with open('poems/LordRandall_Anonymous.txt') as f:
	lines = f.read().splitlines()
title = lines.pop(0)
author = lines.pop(0)

# Open connection to printer and print poem
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer.setSize('M')
printer.println(title)
printer.setSize('M')
printer.println(author+"\n")
printer.setSize('S')
for line in lines:
	printer.println(line)
printer.feed(3)

# Reset everything for next print
printer.sleep()
printer.wake()
printer.setDefault()
