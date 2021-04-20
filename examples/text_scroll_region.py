"""
Scroll text from left to right along the Launchpad's surface,
lighting a specified region.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text
from lpminimk3.region import Labeled as LabeledRegion
import random


def cycle_func(fraction, lp):
    labeled_region = LabeledRegion()  # Region of labeled buttons
    scroll_index = int(fraction * len(labeled_region))  # position in scroll
    for index, led in enumerate(lp.panel.led_range(region=labeled_region)):  # Loop through all labeled buttons  # noqa
        if scroll_index == index:
            led.color = 'green4'  # Light up LED to green
        else:
            del led.color  # Turn off all other LEDs


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Watch text scroll across the Launchpad\'s surface.\n'  # noqa
          'Press Ctrl+C to quit.\n')

    while True:
        try:
            lp.grid.render(Text(' The entrance of your word giveth light...')
                           .scroll(count=1,
                                   cycle_func=cycle_func)
                           .rotate(-90)
                           .fg_color.set(random.randint(1, 127)))
        except KeyboardInterrupt:
            print('\n')
            break


if __name__ == '__main__':
    main()
