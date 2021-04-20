"""
Scroll text from left to right along the Launchpad's surface,
lighting specific regions.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text
from lpminimk3.regions import Labeled
import random


def cycle_func(period_fraction, lp):
    position = int(period_fraction * 17)
    for index, led in enumerate(lp.panel.led_range(region=Labeled())):
        if position == index:
            led.color = 'green4'
        else:
            led.color = 0


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Watch text scroll across the Launchpad\'s surface.\n'  # noqa
          'Press Ctrl+C to quit.\n')

    while True:
        try:
            lp.grid.render(Text(' Watch the region light up.')
                           .scroll(count=1,
                                   cycle_func=cycle_func)
                           .rotate(-90)
                           .fg_color.set(random.randint(1, 127)))
        except KeyboardInterrupt:
            print('\n')
            break


if __name__ == '__main__':
    main()
