"""The classic snake game.
"""
from lpminimk3 import find_launchpads, Mode
import random
import time


SNAKE_COLOR = 16     # green-ish
APPLE_COLOR = 5      # red-ish
HEAD_COLOR = 100     # bright color for head
TICK = 0.18          # movement speed (seconds per step)

# Side buttons for movement
BTN_UP = ("up",    (0, -1))
BTN_DOWN = ("down",  (0, 1))
BTN_LEFT = ("left",  (-1, 0))
BTN_RIGHT = ("right", (1, 0))
CONTROLS = [BTN_UP, BTN_DOWN, BTN_LEFT, BTN_RIGHT]
BUTTON_NAMES = list(map(lambda direction: direction[0], CONTROLS))


# Side button map
def read_direction(lp):
    """Returns new direction if a control button is pressed.

    Parameters
    ----------
    lp : object
        Launchpad instance

    Returns
    -------
    tuple
        XY coordinates of new direction or None if no direction set.
    """
    ev = lp.panel.buttons(*BUTTON_NAMES).poll_for_event(type="press", timeout=.2)

    if ev is not None:
        pressed_buttons = list(filter(lambda direction: direction[0] == ev.button.name, CONTROLS))
        return pressed_buttons[0][1] if len(pressed_buttons) else None

    return None


def spawn_apple(snake):
    """Places an apple somewhere not on the snake.

    Parameters
    ----------
    snake : tuple
        XY coordinates of the snake
    """
    while True:
        pos = (random.randint(0, 7), random.randint(0, 7))
        if pos not in snake:
            return pos


def draw_board(lp, snake, apple):
    """Draws everything onto the Launchpad.

    Parameters
    ----------
    lp : object
        Launchpad instance
    snake : tuple
        XY coordinates of the snake
    apple : tuple
        XY coordinates of the apple
    """
    lp.grid.reset()

    # Draw apple
    ax, ay = apple
    lp.grid.led(ax, ay).color = APPLE_COLOR

    # Draw snake head
    hx, hy = snake[0]
    lp.grid.led(hx, hy).color = HEAD_COLOR

    # Draw snake body
    for x, y in snake[1:]:
        lp.grid.led(x, y).color = SNAKE_COLOR


def game_over_animation(lp):
    """Flashes the board red for game over.

    Parameters
    ----------
    lp : object
        Launchpad instance
    """
    for _ in range(3):
        for led in lp.grid.led_range():
            led.color = 5
        time.sleep(.2)
        lp.grid.reset()
        time.sleep(.2)
    bid_farewell()


def run_snake(lp):
    """Runs the snake game.

    Parameters
    ----------
    lp : object
        Launchpad instance
    """
    snake = [(4, 4), (4, 5), (4, 6)]   # start snake
    direction = (0, -1)               # moving up
    apple = spawn_apple(snake)

    illuminate_controls(lp)

    while True:
        # Read input
        new_dir = read_direction(lp)
        if new_dir:
            # Prevent reversing directly into yourself
            if (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                direction = new_dir

        # Move snake
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = ((head_x + dx) % 8, (head_y + dy) % 8)  # wrap-around

        # Collision with self
        if new_head in snake:
            game_over_animation(lp)
            return  # reset game

        snake.insert(0, new_head)

        # Eating apple?
        if new_head == apple:
            apple = spawn_apple(snake)
        else:
            snake.pop()  # remove tail segment

        # Draw board
        draw_board(lp, snake, apple)

        time.sleep(TICK)


def greet():
    """Greets players with an intro message.
    """
    print("Welcome to Snake")
    print("----------------")
    print("Use the arrow keys at the top left corner of your Launchpad to control the snake's position.")


def bid_farewell():
    """Bids farewell to players.
    """
    print("Game over! Try again")
    print()
    greet()


def illuminate_controls(lp):
    """Illuminates the controls used to play the snake game.

    Parameters
    ----------
    lp : object
        Launchpad instance
    """
    new_color = random.randint(0, 127)
    lp.panel.led(BTN_UP[0]).color = new_color
    lp.panel.led(BTN_DOWN[0]).color = new_color
    lp.panel.led(BTN_LEFT[0]).color = new_color
    lp.panel.led(BTN_RIGHT[0]).color = new_color


def main():
    lp = find_launchpads()[0]
    lp.open()
    lp.mode = Mode.PROG
    lp.panel.reset()

    greet()
    while True:
        run_snake(lp)


if __name__ == "__main__":
    main()
