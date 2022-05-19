"""
Random party mode with some interactivity

Author: Matthew Wachter
"""

from lpminimk3 import Mode, find_launchpads, colors
import random
import math


def main():  # noqa
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    for led in lp.panel.led_range():
        del led.color  # Turn off LED

    try:
        while True:
            order = [i for i in range(0, 64)]
            for i in range(0, len(order)):

                random.shuffle(order)
                led_n = order[i]
                led = lp.grid.led(led_n % 8, math.floor(led_n / 8))
                r = random.randint(-6, 6)
                if r > 4:
                    led.color = colors.ColorPalette.Red.SHADE_2
                elif r > 0:
                    led.color = colors.ColorPalette.Red.SHADE_9
                elif r == 0:
                    led.color = colors.ColorPalette.Yellow.SHADE_3
                else:
                    led.color = 0

                l_time = random.randint(1, 8)
                ev = lp.panel.buttons().poll_for_event(type='press',
                                                       timeout=l_time / 16)
                if ev and ev.button:
                    if r > 0:
                        ev.button.led.color = colors.ColorPalette.Green.SHADE_7
                    else:
                        ev.button.led.color = colors.ColorPalette.Green.SHADE_10  # noqa
    except KeyboardInterrupt:
        print('stopping')


if __name__ == '__main__':
    main()
