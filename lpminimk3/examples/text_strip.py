"""Scroll the text "Hello, world!" from right to left
across the multiple Launchpad surfaces.
"""

from lpminimk3 import Mode, find_launchpads
from lpminimk3.graphics import TextStrip
import random


def main():
    """Scroll text from right to left across multiple Launchpad surfaces.
    """
    lps = find_launchpads()  # Get all launchpads

    (TextStrip(*lps).set_option(0, "fg_color", random.randint(1, 127))
                    .set_option(1, "fg_color", random.randint(1, 127))
                    .scroll((" "*len(lps)) + "Hello, world"))  # Scroll text once


if __name__ == '__main__':
    main()
