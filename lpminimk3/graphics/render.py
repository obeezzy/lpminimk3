import sys
import os
from .__init__ import Text


def print_usage():
    print(f'Usage: {os.path.basename(sys.argv[0])} CHARACTER\n')  # noqa


def main(letter=None):
    try:
        if len(sys.argv) != 2 and not isinstance(letter, str):
            raise ValueError('Missing character argument.')

        input_string = sys.argv[1] if not letter else letter
        Text(input_string).print()
    except Exception as e:
        print(e, file=sys.stderr)
        print_usage()


if __name__ == '__main__':
    main()
