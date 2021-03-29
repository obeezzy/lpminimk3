"""Displays a random array of colors for 5 seconds."""

from lpminimk3 import Mode, find_launchpads
import random
import time

lp = find_launchpads()[0]  # Get the first available launchpad
lp.open()  # Open device for reading and writing on MIDI interface (by default)

lp.mode = Mode.PROG  # Switch to the programmer mode

for led_id in range(81):  # Loop through all 81 LEDs
    lp.panel.led(led_id).color = random.randint(1, 127)  # Set LED to a random color  # noqa

time.sleep(5)  # Keep LEDs on for a while

for led_id in range(81):
    lp.panel.led(led_id).reset()  # Turn off LED
