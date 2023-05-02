"""Run slideshow of logos.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import Bitmap
from lpminimk3.graphics.art import Bitmaps
import time
import os


SLIDES = [
        "APPLE",
        "APPLE_OLD",
        "FACEBOOK",
        "GMAIL",
        "GOOGLE",
        "ITUNES",
        "WINDOWS",
        "XBOX",
        "YOUTUBE"
        ]


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Watch logos appear on your Launchpad.\n'  # noqa
          'Press Ctrl+C to quit.\n')

    while True:
        try:
            for k, v in Bitmaps.__dict__.items():
                if k in SLIDES and isinstance(v, str) and os.path.isfile(v):
                    lp.grid.render(Bitmap(v))
                    time.sleep(2)
        except KeyboardInterrupt:
            print('\n')
            break


if __name__ == '__main__':
    main()
