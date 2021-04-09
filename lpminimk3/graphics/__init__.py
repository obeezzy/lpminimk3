import os
from ._parser import GlyphDictionary as _GlyphDictionary,\
                     Character as _Character,\
                     String as _String,\
                     Renderable
from ..colors import ColorPalette as _ColorPalette


class Text(Renderable):
    def __init__(self, text, *,
                 fg_color=_ColorPalette.Red.SHADE_4,
                 bg_color=None):
        if not isinstance(text, str):
            raise TypeError('Must be of type str.')

        self._text = text
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._glyph_dicts = self._create_glyph_dicts()
        self._characters = self._create_characters(text,
                                                   self._glyph_dicts,
                                                   fg_color,
                                                   bg_color)
        self._string = _String(*self._characters)

    def __repr__(self):
        return 'Text(\'{}\')'.format(self._text)

    def __str__(self):
        return self._text

    @Renderable.bits.getter
    def bits(self):
        if len(self._characters) == 1:
            return self._characters[0].bits
        return self._string.bits

    @Renderable.word_count.getter
    def word_count(self):
        if len(self._characters) == 1:
            return self._characters[0].word_count
        return self._string.word_count

    def render(self, matrix):
        if len(self._characters) == 1:
            self._characters[0].render(matrix)
        else:
            self._string.render(matrix)

    def shift_left(self, count=1):
        if len(self._characters) == 1:
            self._characters[0] = self._characters[0].shift_left(count=count)
            return self._characters[0]
        return self._string.shift_left(count=count)

    def shift_right(self, count=1):
        if len(self._characters) == 1:
            self._characters[0] = self._characters[0].shift_right(count=count)
            return self._characters[0]
        return self._string.shift_right(count=count)

    def _create_characters(self, text, dicts, fg_color, bg_color):
        characters = []
        for glyph in text:
            for glyph_dict in dicts:
                if glyph in glyph_dict:
                    characters.append(_Character(glyph,
                                                 glyph_dict[glyph],
                                                 fg_color,
                                                 bg_color))
                    break
        return characters

    def _create_glyph_dicts(self):
        glyph_dicts = []
        current_dir = os.path.dirname(__file__)
        glyph_dict_dir = os.path.join(current_dir, 'glyphs')
        for filename in os.listdir(glyph_dict_dir):
            if filename.endswith('.glyph.json'):
                glyph_dicts.append(_GlyphDictionary(os.path.join(glyph_dict_dir, filename),  # noqa
                                   './schema/glyph.schema.json'))
        return glyph_dicts
