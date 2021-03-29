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

for led_id in range(81):  # Loop through all 81 LEDs
    lp.panel.led(led_id).color = random.randint(1, 127)  # Set LED to a random color

time.sleep(5)  # Keep LEDs on for a while

for led_id in range(81):
    lp.panel.led(led_id).reset()  # Turn off LED

```
View example file [here](examples/flash.py).

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
>>> lp.grid.led('0x0').color = 10  # Set color to yellow
>>> lp.grid.led(1,0).color = 10  # Set color of next LED to yellow
>>> lp.panel.led('logo').color = 1  # Set logo LED color to white
```


## Release History
* [0.1.1](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.1)
    * Cleanup README
* [0.1.0](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.0)
    * First release ever (Still a work in progress)


## Notes
* Work in progress, so expect things to break!


## License
[MIT](https://choosealicense.com/licenses/mit/)
