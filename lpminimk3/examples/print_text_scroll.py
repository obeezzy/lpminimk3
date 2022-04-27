"""
Print a typed string on the console.
"""

from lpminimk3.graphics import Text


def main():
    try:
        text_to_print = ''
        while not text_to_print:
            text_to_print = input('Enter text to print '
                                  '(Press Ctrl+C to quit): ')
        text_to_print += ' '
        Text(text_to_print).scroll().print()
    except KeyboardInterrupt:
        print('\n')


if __name__ == '__main__':
    main()
