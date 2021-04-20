"""
Wait for button presses and log events.
"""

from lpminimk3 import ButtonEvent, Mode, find_launchpads
import random
import sys


def handle_event(button_event):
    if button_event and button_event.type == ButtonEvent.PRESS:
        button_event.button.led.color = random.randint(1, 127)  # Set LED to random color while button is pressed  # noqa
        print(f"Button '{button_event.button.name}' pressed.")
    elif button_event and button_event.type == ButtonEvent.RELEASE:
        button_event.button.led.color = 0  # Turn LED off once button is released  # noqa
        print(f"Button '{button_event.button.name}' released.")
    else:
        sys.exit()  # Exit on KeyboardInterrupt


def main():
    lp = find_launchpads()[0]  # Get the first available launchpad
    lp.open()  # Open device for reading and writing on MIDI interface (by default)  # noqa

    lp.mode = Mode.PROG  # Switch to the programmer mode

    print('Push any button on your Launchpad to see it light up!\n'
          'Press Ctrl+C to quit.\n')
    while True:
        handle_event(lp.panel.buttons().poll_for_event())  # Wait for a button press/release  # noqa


if __name__ == '__main__':
    main()
