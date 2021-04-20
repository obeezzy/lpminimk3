"""
Display characters typed with a QWERTY keyboard on the Launchpad's surface.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Text
import sys
import termios
import tty


def getchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def render_character(lp):
    while True:
        c = getchar()
        if ord(c) == 0x03:
            sys.exit()
        else:
            lp.grid.render(Text(c))


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Press a key on your keyboard to display a character on your Launchpad.\n'  # noqa
          'Press Ctrl+C to quit.\n')
    render_character(lp)  # Render character on Launchpad's surface


if __name__ == '__main__':
    main()
