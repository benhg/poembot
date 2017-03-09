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
import Image, ImageDraw, time, urllib, json

# Open connection to printer and print image
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer.print('hello world')
printer.feed(3)
