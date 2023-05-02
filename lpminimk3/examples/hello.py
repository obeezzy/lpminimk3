"""Scroll the text "Hello, world!" from right to left
across the Launchpad's surface once.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text


def main():
    """Scroll text from right to left across the Launchpad's surface.
    """
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    lp.grid.render(Text(' Hello, world!').scroll())  # Scroll text once  # noqa


if __name__ == '__main__':
    main()
