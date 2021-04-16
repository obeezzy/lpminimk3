"""
Render a typed string on the console.
"""

from lpminimk3.graphics import Text


def main():
    try:
        text_to_render = ''
        while not text_to_render:
            text_to_render = input('Enter text to render '
                                   '(Press Ctrl+C to quit): ')
        text_to_render += ' '
        Text(text_to_render).scroll().print()
    except KeyboardInterrupt:
        print('\n')


if __name__ == '__main__':
    main()
