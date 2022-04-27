# lpminimk3
Python API for the [Novation Launchpad Mini MK3](https://novationmusic.com/en/launch/launchpad-mini) with an object-oriented approach.

[![CI](https://github.com/obeezzy/lpminimk3/actions/workflows/main.yml/badge.svg)](https://github.com/obeezzy/lpminimk3/actions/workflows/main.yml)
[![CD](https://github.com/obeezzy/lpminimk3/actions/workflows/deploy.yml/badge.svg?branch=v0.3.0)](https://github.com/obeezzy/lpminimk3/actions/workflows/deploy.yml)

The goals of this project are as follows:
* Intuitive, object-oriented design
* Convenient for use in script and shell
* Access to all (or most) of the Launchpad Mini MK3 MIDI features


## Installation
To install the most stable version of this package, run:
```bash
$ pip install lpminimk3
```
To test the installation, connect your Launchpad to your computer and run:
```bash
$ python -m lpminimk3.examples.hello
```


## Usage example
Make sure your Launchpad is connected to your computer.

### In script
Control LEDs individually:
```python
"""
Display a random array of colors for 5 seconds.
"""

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
    del led.color  # Turn off LED
```
Render text on Launchpad's surface:
```python
"""
Scroll text from right to left across the Launchpad's surface.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text

lp = find_launchpads()[0]  # Get the first available launchpad
lp.open()  # Open device for reading and writing on MIDI interface (by default)

lp.mode = Mode.PROG  # Switch to the programmer mode

print('Watch text scroll across the Launchpad\'s surface.\n'
      'Press Ctrl+C to quit.\n')

lp.grid.render(Text(' Hello, world!').scroll())  # Scroll text indefinitely
```
See more examples [here](https://github.com/obeezzy/lpminimk3/tree/main/examples).

### In shell
Start by finding a connected device and opening the device for reading and writing:
```bash
$ python
>>> import lpminimk3
>>> lp = lpminimk3.find_launchpads()[0]
>>> lp.open()
```
Query the device to ensure we can read and write to it:
```python
>>> lp.device_inquiry()  # Query device
MidiEvent(message=[240, 0, 32, 41, 2, 13, 14, 1, 247], deltatime=150.938086752)
```
Switch to `programmer` mode to start manipulating button LEDs.
```python
>>> lp.mode = 'prog'  # Switch to programmer mode
>>> lp.grid.led('0x0').color = 10  # Set color to yellow (Valid values: 0 - 127)
>>> lp.grid.led(1,0).color = lpminimk3.colors.ColorPalette.Red.SHADE_1  # Set from palette
>>> lp.panel.led('logo').color = 'violet'  # Set logo LED color to violet
>>> lp.panel.led('drums').color = 'green2'  # Set 'Drums' LED color to second shade of green
>>> lp.panel.led('stop').color = 'w1'  # Set 'Stop/Solo/Mute' LED color to first shade of white
>>> lp.panel.led('mute').color = 'o3'  # Set 'Stop/Solo/Mute' LED color to third shade of orange
>>> lp.panel.led('mute').color = 'r0'  # Invalid but okay, will default to 'r1'
>>> lp.panel.led('scene_launch_1').color = '#ff0000'  # Set color to red using hex
>>> lp.panel.led('scene_launch_2').color = (0, 0, 255)  # Set color to blue using rgb
>>> lp.panel.led('mute').color = 0  # Turn off LED
>>> lp.panel.led('logo').reset()  # Another way to turn off LED
>>> del lp.panel.led('stop').color  # Another way to turn off LED
```
Note in the above snippet that `lp.grid` only contains the __*grid*__ buttons
(i.e. the faceless white buttons) and `lp.panel` contains all buttons
(including the __*logo*__ LED at the top right corner).  

Wait for and respond to button presses and releases:
```python
>>> ev = lp.panel.buttons().poll_for_event()  # Block until any button is pressed/released
>>> ev
ButtonEvent(button='7x5', type='press', deltatime=0.0)
```
Or only button releases instead:
```python
>>> ev = lp.panel.buttons().poll_for_event(type='release')  # Block until released
>>> ev
ButtonEvent(button='up', type='release', deltatime=0.0)
```
Pass button names as arguments to wait for specific button events:
```python
>>> lp.panel.buttons('up', '0x0', 'stop').poll_for_event()
```
Render `A` on Launchpad's surface:
```python
>>> lp.grid.render(Text('A'))
```
Print `A` in console:
```python
>>> Text('A').print()
  XX    
 XXXX   
XX  XX  
XX  XX  
XXXXXX  
XX  XX  
XX  XX  
```
Scroll `Hello, world!` on Launchpad's surface once:
```python
>>> lp.grid.render(Text(' Hello, world!').scroll(count=1))
```


## Release History
* [0.4.4](https://github.com/obeezzy/lpminimk3/releases/tag/v0.4.4)
    * Add initial support for Mac
    * Add hex and RGB support
    * Expose examples from root package
    * Refactor port parsing logic
* [0.4.3](https://github.com/obeezzy/lpminimk3/releases/tag/v0.4.3)
    * Add initial support for Windows
* [0.4.2](https://github.com/obeezzy/lpminimk3/releases/tag/v0.4.2)
    * Correct `MANIFEST.in`
* [0.4.1](https://github.com/obeezzy/lpminimk3/releases/tag/v0.4.1)
    * Add `MANIFEST.in`
    * Clean up README
* [0.4.0](https://github.com/obeezzy/lpminimk3/releases/tag/v0.4.0)
    * Add `lpminimk3.graphics` module
    * Introduce text rendering, printing, scrolling and transformations
    * Add `Region`, for representing a group of LEDs
    * Add and update examples
* [0.3.0](https://github.com/obeezzy/lpminimk3/releases/tag/v0.3.0)
    * Change `ButtonEvent.event_type` to `ButtonEvent.type`
* [0.2.1](https://github.com/obeezzy/lpminimk3/releases/tag/v0.2.1)
    * Fix version error
* [0.2.0](https://github.com/obeezzy/lpminimk3/releases/tag/v0.2.0)
    * Add `led_range()` for easy iteration through LEDs
    * Update and add examples
    * Update README for clarity
    * Add `ButtonEvent` and `buttons()`, for handling of button presses and releases
    * Clean up documentation
    * Add logger, for logging MIDI events
    * Move all MIDI messages to `midi_messages` module
    * More robust testing
    * Bug fixes
    * Complete [Project Foundation](https://github.com/obeezzy/lpminimk3/projects/1)
* [0.1.2](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.2)
    * Properly bump up version
* [0.1.1](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.1)
    * Clean up README
* [0.1.0](https://github.com/obeezzy/lpminimk3/releases/tag/v0.1.0)
    * First release ever (Still a work in progress)


## Notes
* Work in progress, so expect things to break!


## License
[MIT](https://choosealicense.com/licenses/mit/)
