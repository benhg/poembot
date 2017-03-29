# PoemBot

PoemBot is a [WatzekDigitalInitiatives](https://github.com/WatzekDigitalInitiatives) project based on [evanwill](github.com/evanwill)'s own [poemBot](https://github.com/evanwill/poemBot). It prints selected poems on receipts to commemorate National Poetry Month.

Members of the PoemBot Working Group:

-   [sophiahorigan](github.com/sophiahorigan)
-   [thatbudakguy](github.com/thatbudakguy)
-   [jeremymcwilliams](github.com/jeremymcwilliams)
-   [DanOswalt](github.com/DanOswalt)
-   Erica Jensen
-   Jen Jacobs
-   Parvaneh Abbaspour
-   Chel Pennock

## Construction

PoemBot runs on a Raspberry Pi connected to a [thermal receipt printer](http://www.adafruit.com/products/597). It has a [Raspberry Squid LED](https://github.com/simonmonk/squid) as a status indicator and a pushbutton to trigger the printing of a poem. It lives inside a 3d printed enclosure designed using SketchUp (`boxfinal.skp`).

## Usage

The Raspberry Pi is configured to run `start.sh` as a `cron` job at startup, which runs the main Python script `poembot.py`. When the button is pressed, a poem is selected based on the day of the month from the `poems` folder and printed. The `printpoem.py` script can be run at will over `ssh` to test printing of individual poems from the `poems` folder. See `poembot.py` for more details.

## License

PoemBot is offered under an MIT license. You are free to use the code for any purpose you choose.
