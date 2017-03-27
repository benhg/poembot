#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Main script for Watzek PoemBot.  Monitors button
for taps/holds and prints a poem selected for the day of the month.

MUST BE RUN AS ROOT (due to GPIO access)

Required software includes Adafruit_Thermal and PySerial
libraries. Other libraries used are part of stock Python install.

Resources:
https://github.com/evanwill/poemBot Evan Will's PoemBot
http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
"""

from __future__ import print_function
import subprocess
import time
import socket
#import textwrap
from button import *
from squid import *
from Adafruit_Thermal import *

LED = Squid(18, 23, 24)
BUTTON = Button(25, debounce=0.1)
PRINTER = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)


def tap():
    """Called when button is briefly tapped.

    Calls print_poem().
    """
    LED.set_color(GREEN)
    print_poem()
    LED.set_color(BLUE)


def hold():
    """Called when the button is held down.

    Calls shutdown().
    """
    LED.set_color(GREEN)
    shutdown()
    LED.set_color(BLUE)


def greet():
    """Called on startup of Poembot, in main().

    Prints a greeting message and then attempts to determine Poembot's network
    address and print it, with instructions to connect to Poembot remotely.
    """

    PRINTER.println("Hello!")
    PRINTER.feed(3)
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.connect(('8.8.8.8', 0))
        PRINTER.boldOn()
        PRINTER.println('My IP address is ' + my_socket.getsockname()[0])
        PRINTER.boldOff()
        PRINTER.println('Connect with:')
        PRINTER.println('$ ssh pi@poembot')
        PRINTER.feed(3)
    except socket.error:
        PRINTER.boldOn()
        PRINTER.println('Network is unreachable.')
        PRINTER.boldOff()
        PRINTER.println(
            'Connect display and keyboard for network troubleshooting.')
        PRINTER.feed(3)


def shutdown():
    """Called on a long press of the button, in hold().

    Prints a goodbye message and shuts down Poembot.
    """

    PRINTER.println("Goodbye!")
    PRINTER.feed(3)
    subprocess.call("sync")
    subprocess.call(["shutdown", "-h", "now"])


def print_poem():
    """Called on a short press of the button, in main().

    Selects a poem based on the day of the month, looks for the corresponding
    file in the poems directory, formats the author and title, and prints it.
    """

    day = time.strftime("%m/%d/%Y").split("/")[1]
    poem_path = "allpoems/poems/" + day + ".txt"
    with open(poem_path) as poem_file:
        poem_lines = poem_file.read().splitlines()
    title = poem_lines.pop(0)
    author = poem_lines.pop(1)
    PRINTER.setSize('M')
    PRINTER.println(title)
    PRINTER.setSize('M')
    PRINTER.println(author + "\n")
    PRINTER.setSize('S')
    for line in poem_lines:
        PRINTER.println(line)
    PRINTER.feed(3)


def main():
    """Main loop. Called when Poembot is powered on.

    Waits a short time for Poembot to startup, then calls greet() and monitors
    the button for short or long presses, calling tap() or hold() depending on
    the length of the press.
    """

    # GPIO setup
    LED.set_color(GREEN)
    time.sleep(30)
    greet()
    LED.set_color(BLUE)

    # Main loop
    while True:
        if BUTTON.is_pressed():
            print_poem()


# Initialization
if __name__ == '__main__':
    main()
