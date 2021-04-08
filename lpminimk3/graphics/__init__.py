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
        self._glyph_dicts = [_GlyphDictionary('./glyphs/basic_latin.glyph.json',  # noqa
                                              './schema/glyph.schema.json')]
        self._characters = self._create_characters(text,
                                                   self._glyph_dicts,
                                                   fg_color,
                                                   bg_color)
        self._string = _String(*self.characters,
                               fg_color=fg_color,
                               bg_color=bg_color)

    def __repr__(self):
        return 'Text(\'{}\')'.format(self._text)

    def __str__(self):
        return self._text

    @Renderable.bits.getter
    def bits(self):
        if len(self.characters) == 1:
            return self._characters[0].bits
        return self._string.bits

    @Renderable.word_count.getter
    def word_count(self):
        if len(self.characters) == 1:
            return self._characters[0].word_count
        return self._string.word_count

    @property
    def characters(self):
        return self._characters

    def render(self, matrix):
        if len(self.characters) == 1:
            self.characters[0].render(matrix)
        else:
            self._string.render(matrix)

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
