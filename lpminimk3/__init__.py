"""Python API for the Launchpad Mini MK3.

This module exposes API to discover connected Launchpads
on your computer and control them.

Examples
--------

Find a connected device and open the device for reading and writing:
    >>> import lpminimk3
    >>> lp = lpminimk3.find_launchpads()[0]
    >>> lp.open()

Query the device to ensure reading and writing works:
    >>> lp.device_inquiry()
    MidiEvent(message=[240, 0, 32, 41, 2, 13, 14, 1, 247], deltatime=0.0)

Switch to the programmer mode:
    >>> lp.mode = Mode.PROG

After a Launchpad is initialized, its `Grid` and `Panel` can be manipulated.

Set color of LED at "0x0" to yellow (Valid values: 0 - 127):
    >>> lp.grid.led('0x0').color = 10

Set color of LED at "1x0" to the first shade of palette color "red":
    >>> import lpminimk3
    >>> from lpminimk3.colors import ColorPalette
    >>> lp.grid.led('1x0').color = ColorPalette.Red.SHADE_1

Set color of LED at "logo" (in panel) to violet:
    >>> lp.panel.led('logo').color = 'violet'

Set color of LED at "Drums" to second shade of "green":
    >>> lp.panel.led('drums').color = 'green2'

Set color of LED at "Stop/Solo/Mute" to first shade of "white":
    >>> lp.panel.led('stop').color = 'w1'

Set color of LED at "Stop/Solo/Mute" to third shade of "orange":
    >>> lp.panel.led('mute').color = 'o3'

Set color of LED at "Stop/Solo/Mute" to first shade of "red" (Invalid, but okay):  # noqa
    >>> lp.panel.led('solo').color = 'r0'

Set color of LED at "Scene Launch 1" to "red" using hex:
    >>> lp.panel.led('scene_launch_1').color = '#ff0000'

Set color of LED at "Scene Launch 2" to "blue" using RGB:
    >>> lp.panel.led('scene_launch_2').color = (0, 0, 255)

Set color of LED at "Scene Launch 2" to "magenta" using web colors:
    >>> from lpminimk3.colors import WebColor
    >>> lp.panel.led('scene_launch_3').color = WebColor("magenta")

Turn off "Stop/Solo/Mute" LED:
    >>> lp.panel.led('mute').color = 0

Another way to turn off LED:
    >>> lp.panel.led('mute').reset()

Another way to turn off LED:
    >>> del lp.panel.led('mute').color

Wait for and respond to button presses and releases:
    >>> lp.panel.buttons().poll_for_event()
    ButtonEvent(button='4x1', type='press', deltatime=4.202155996)

Wait for button releases:
    >>> lp.panel.buttons().poll_for_event(type='release')
    ButtonEvent(button='4x1', type='release', deltatime=0.171533228)

Wait for "Up", "0x0" or "Stop/Solo/Mute" button to be pressed or released:
    >>> lp.panel.buttons('up', '0x0', 'stop').poll_for_event()
    ButtonEvent(button='4x1', type='release', deltatime=0.040492674)
"""

from .__version__ import __version__, VERSION  # noqa
from .components import Grid, Panel, Led, ButtonFace  # noqa
from .utils import Interface, Mode, Layout, ButtonEvent  # noqa
from .device import LaunchpadMiniMk3, find_launchpads  # noqa

if __name__ == "__main__":
    import doctest
    doctest.testmod()
