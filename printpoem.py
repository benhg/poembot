#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Main script for Watzek PoemBot.  Monitors button
for taps/holds and prints a poem selected for the day of the month.

Required software includes Adafruit_Thermal and Monk Makes Squid/Button
libraries. Other libraries used are part of stock Python install.

Resources:
https://github.com/evanwill/poemBot Evan Will's PoemBot
http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
https://github.com/simonmonk/squid Simon Monk's Squid & Libraries
"""

import textwrap
from button import *
from squid import *
from Adafruit_Thermal import *

LED = Squid(18, 23, 24)
BUTTON = Button(25, debounce=0.1)
PRINTER = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)


def print_poem(number):
    """ Called on a short press of the button, in main().

    Selects a poem based on the day of the month, looks for the corresponding
    file in the poems directory, formats the author and title, and prints it.
    """
    PRINTER.wake()
    poem_path = "poems/" + number + ".txt"
    try:
        with open(poem_path) as poem_file:
            poem_lines = poem_file.read().splitlines()
    except IOError as error:
        PRINTER.println(error)
        PRINTER.feed(3)
    title = textwrap.fill(poem_lines.pop(0), width=32)
    author = textwrap.fill(poem_lines.pop(0), width=32)
    poem = ""
    for line in poem_lines:
        poem += textwrap.fill(line, width=42, subsequent_indent="  ") + "\n"
    PRINTER.boldOn()
    PRINTER.println(title)
    PRINTER.boldOff()
    PRINTER.println(author)
    PRINTER.writeBytes(0x1B, 0x21, 0x1)
    PRINTER.println(poem)
    PRINTER.feed(3)
    PRINTER.sleep()

print_poem('15')
