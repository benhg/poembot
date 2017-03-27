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
import textwrap
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
    LED.set_color(YELLOW)
    print_poem()
    LED.set_color(GREEN)


def hold():
    """Called when the button is held down.

    Calls shutdown().
    """
    LED.set_color(YELLOW)
    shutdown()
    LED.set_color(GREEN)


def greet():
    """Called on startup of Poembot, in main().

    Prints a greeting message and then attempts to determine Poembot's network
    address and print it, with instructions to connect to Poembot remotely.
    """

    PRINTER.online()
    PRINTER.setSize('M')
    PRINTER.println("Hello!")
    PRINTER.setSize('S')
    PRINTER.println('Today is ' + time.strftime("%m/%d/%Y"))
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.connect(('8.8.8.8', 0))
        PRINTER.boldOn()
        PRINTER.println('My IP address is ' + my_socket.getsockname()[0])
        PRINTER.boldOff()
        PRINTER.println('Connect with:')
        PRINTER.println('$ ssh pi@poembot')
        PRINTER.feed(3)
        PRINTER.sleep()
    except socket.error:
        PRINTER.boldOn()
        PRINTER.println('Network is unreachable.')
        PRINTER.boldOff()
        PRINTER.feed(3)
        PRINTER.sleep()


def shutdown():
    """Called on a long press of the button, in hold().

    Prints a goodbye message and shuts down Poembot.
    """

    PRINTER.wake()
    PRINTER.println("Goodbye!")
    PRINTER.feed(3)
    PRINTER.offline()
    subprocess.call("sync")
    subprocess.call(["shutdown", "-h", "now"])


def print_poem():
    """Called on a short press of the button, in main().

    Selects a poem based on the day of the month, looks for the corresponding
    file in the poems directory, formats the author and title, and prints it.
    """
    PRINTER.wake()
    day = time.strftime("%m/%d/%Y").split("/")[1]
    poem_path = "poems/" + day + ".txt"
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
        poem += textwrap.fill(line, width=32, subsequent_indent="  ") + "\n"
    PRINTER.boldOn()
    PRINTER.println(title)
    PRINTER.boldOff()
    PRINTER.writeBytes(0x1B, 0x21, 0x1)
    PRINTER.println(poem)
    PRINTER.feed(3)
    PRINTER.sleep()


def main():
    """Main loop. Called when Poembot is powered on.

    Waits a short time for Poembot to boot up, then calls greet() and monitors
    the button for short or long presses, calling tap() or hold() depending on
    the length of the press.
    """

    LED.set_color(RED)
    PRINTER.online()
    LED.set_color(YELLOW)
    greet()
    LED.set_color(GREEN)

    while True:
        if BUTTON.is_pressed():
            LED.set_color(YELLOW)
            print_poem()
            LED.set_color(GREEN)

# Initialization
if __name__ == '__main__':
    main()
