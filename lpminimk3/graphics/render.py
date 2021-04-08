import sys
import os
from .__init__ import Text


def print_usage():
    print(f'Usage: {os.path.basename(sys.argv[0])} CHARACTER\n')  # noqa


def render(text):
    for index, bit in enumerate(text.bits, start=1):
        if bit:
            print('X', end='')
        elif 'LOGLEVEL' in os.environ:
            print('.', end='')
        else:
            print(' ', end='')

        if index % text.word_count == 0:
            print('\n', end='')


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('Missing character argument.')

        input_string = sys.argv[1]
        text = Text(input_string[0])
        render(text)
    except Exception as e:
        print(e, file=sys.stderr)
        print_usage()


if __name__ == '__main__':
    main()
