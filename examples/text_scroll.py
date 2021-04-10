"""
Scroll text from left to right along the Launchpad's surface.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text
import time


def ascending_range():
    counter = 1
    while True:
        yield counter
        counter += 1


def scroll_text(text, lp):
    while True:
        for shift_count in ascending_range():
            lp.grid.render(Text(text).shift_left(shift_count))
            time.sleep(.2)


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Watch text scroll across the Launchpad\'s surface.\n'  # noqa
          'Press Ctrl+C to quit.\n')
    scroll_text('a', lp)


if __name__ == '__main__':
    main()
