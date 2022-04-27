"""
Scroll text from right to left across the Launchpad's surface.
"""

import sys
from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Watch text scroll across the Launchpad\'s surface.\n'  # noqa
          'Press Ctrl+C to quit.\n')

    try:
        lp.grid.render(Text(' Hello, world!').scroll())
    except KeyboardInterrupt:
        return 1


if __name__ == '__main__':
    sys.exit(main())
