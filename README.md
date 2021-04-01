# lpminimk3
Python API for the [Novation Launchpad Mini MK3](https://novationmusic.com/en/launch/launchpad-mini) with an object-oriented approach.

[![CI](https://github.com/obeezzy/lpminimk3/actions/workflows/main.yml/badge.svg)](https://github.com/obeezzy/lpminimk3/actions/workflows/main.yml)

The goals of this project are as follows:
* Intuitive, object-oriented design
* Convenient for use in script or in shell
* Access to all (or most) of the Launchpad Mini MK3 MIDI features


## Installation
To install the most stable version of this package, run:
```bash
$ pip install lpminimk3
```


## Usage example
Make sure your Launchpad is connected to your computer.

### In script
```python
"""Displays a random array of colors for 5 seconds."""

from lpminimk3 import Mode, find_launchpads
import random
import time

lp = find_launchpads()[0]  # Get the first available launchpad
lp.open()  # Open device for reading and writing on MIDI interface (by default)

lp.mode = Mode.PROG  # Switch to the programmer mode

for led in lp.panel.led_range():  # Loop through all LEDs
    led.color = random.randint(1, 127)  # Set LED to a random color

time.sleep(5)  # Keep LEDs on for a while

for led in lp.panel.led_range():
    led.reset()  # Turn off LED

```
View example file [here](https://github.com/obeezzy/lpminimk3/examples/flash.py).

### In shell
```bash
$ python
>>> import lpminimk3
>>> lp = lpminimk3.find_launchpads()[0]
>>> lp.open()
>>> lp.device_inquiry()  # Query device
MidiEvent(message=[240, 0, 32, 41, 2, 13, 14, 1, 247], deltatime=150.938086752)
>>>
>>> lp.mode = 'prog'  # Switch to programmer mode
>>> lp.grid.led('0x0').color = 10  # Set color to yellow (Valid values: 0 - 127)
>>> lp.grid.led(1,0).color = lpminimk3.colors.ColorPalette.Red.SHADE_1  # Set from palette
>>> lp.panel.led('logo').color = 'violet'  # Set logo LED color to violet
>>> lp.panel.led('drums').color = 'green2'  # Set 'Drums' LED color to second shade of green
>>> lp.panel.led('stop').color = 'w1'  # Set 'Stop/Solo/Mute' LED color to first shade of white
>>> lp.panel.led('mute').color = 'o3'  # Set 'Stop/Solo/Mute' LED color to third shade of orange
>>> lp.panel.led('mute').color = 'r0'  # Invalid but okay, will default to 'r1'
```


## Release History
* [0.1.2](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.2)
    * Properly bump up version
* [0.1.1](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.1)
    * Cleanup README
* [0.1.0](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.0)
    * First release ever (Still a work in progress)


## Notes
* Work in progress, so expect things to break!


## License
[MIT](https://choosealicense.com/licenses/mit/)
