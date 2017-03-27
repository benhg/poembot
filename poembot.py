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
import RPi.GPIO as GPIO
import subprocess
import time
import socket
#import textwrap
from Adafruit_Thermal import *

LED_PIN = 18
BUTTON_PIN = 23
HOLD_TIME = 2     # Duration for button hold (shutdown)
TAP_TIME = 0.01  # Debounce time for button taps
PRINTER = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

def tap():
    """Called when button is briefly tapped.

    Calls print_poem().
    """
    GPIO.output(LED_PIN, GPIO.HIGH)  # LED on while working
    print_poem()
    GPIO.output(LED_PIN, GPIO.LOW)


def hold():
    """Called when the button is held down.

    Calls shutdown().
    """
    GPIO.output(LED_PIN, GPIO.HIGH)
    shutdown()
    GPIO.output(LED_PIN, GPIO.LOW)


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
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(30)
    greet()
    GPIO.output(LED_PIN, GPIO.LOW)

    # Poll initial button state and time
    prev_button_state = GPIO.input(BUTTON_PIN)
    prev_time = time.time()
    tap_enable = False
    hold_enable = False

    # Main loop
    while True:

        # Poll current button state and time
        button_state = GPIO.input(BUTTON_PIN)
        current_time = time.time()

        # Has button state changed?
        if button_state != prev_button_state:
            prev_button_state = button_state   # Yes, save new state/time
            prev_time = current_time
        else:                             # Button state unchanged
            if (current_time - prev_time) >= HOLD_TIME:  # Button held more than 'HOLD_TIME'?
                # Yes it has.  Is the hold action as-yet untriggered?
                if hold_enable is True:        # Yep!
                    hold()                      # Perform hold action (usu. shutdown)
                    hold_enable = False          # 1 shot...don't repeat hold action
                    tap_enable = False          # Don't do tap action on release
            elif (current_time - prev_time) >= TAP_TIME:  # Not HOLD_TIME.  TAP_TIME elapsed?
                # Yes.  Debounced press or release...
                if button_state is True:       # Button released?
                    if tap_enable is True:       # Ignore if prior hold()
                        tap()                     # Tap triggered (button released)
                        tap_enable = False        # Disable tap and hold
                        hold_enable = False
                else:                         # Button pressed
                    tap_enable = True           # Enable tap and hold actions
                    hold_enable = True

        # LED blinks while idle, for a brief interval every 2 seconds.
        if ((int(current_time) & 1) == 0) and ((current_time - int(current_time)) < 0.15):
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)


# Initialization
if __name__ == '__main__':
    main()
