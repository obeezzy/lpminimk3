import sys
import os
from ._parser import GlyphDictionary
from .__init__ import Bitmap


def print_usage():
    print(f'Usage: {os.path.basename(sys.argv[0])} CHARACTER [GLYPH_DICT_JSON]\n')  # noqa


def render(bitmap):
    for index, bit in enumerate(bitmap, start=1):
        if bit:
            print('X', end='')
        else:
            print('.', end='')

        if index % bitmap.max_word_length == 0:
            print('\n', end='')


def main():
    try:
        if len(sys.argv) < 2:
            raise ValueError('Missing character argument.')
        if len(sys.argv) > 3:
            raise ValueError('Too many arguments.')

        character = sys.argv[1]
        DEFAULT_FILENAME = './glyphs/basic_latin.glyph.json'
        filename = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_FILENAME
        glyph_dict = GlyphDictionary(filename,
                                     './schema/glyph.schema.json')
        if character not in glyph_dict:
            raise RuntimeError(f'{character} not found.')

        bitmap = Bitmap(glyph_dict[character])
        render(bitmap)
    except Exception as e:
        print(e, file=sys.stderr)
        print_usage()


if __name__ == '__main__':
    main()
