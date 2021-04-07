from abc import ABC
from ..midi_messages import Colorspec,\
                            ColorspecFragment
from ._parser import GlyphDictionary as _GlyphDictionary,\
                     BitmapConfig as _BitmapConfig,\
                     Character as _Character
from ..colors import ColorPalette


class Renderable(ABC):
    def render(self, matrix):
        pass


class BitmapRenderer:
    def __init__(self, bitmap, matrix, *, fg_color, bg_color=None):
        self._bitmap = bitmap
        self._matrix = matrix
        self._fg_color = fg_color
        self._bg_color = bg_color

    def render(self):
        colorspec_fragments = []
        for led, bit in zip(self._matrix.led_range(), self._bitmap):
            bit_config = self._bitmap.config[led.name]
            lighting_type = bit_config.lighting_type
            led_index = led.midi_value
            lighting_data = self._determine_lighting_data(bit_config,
                                                          bit,
                                                          self._fg_color,
                                                          self._bg_color)
            fragment = ColorspecFragment(lighting_type,
                                         led_index,
                                         *lighting_data)
            colorspec_fragments.append(fragment)
        payload = Colorspec(*colorspec_fragments)
        self._matrix.launchpad.send_message(payload)

    def _determine_lighting_data(self, config, bit, fg_color, bg_color):
        lighting_data = []
        if config.lighting_type == 'flash':
            lighting_data = (config.lighting_data.on_state
                             if bit
                             else config.lighting_data.off_state)
        elif config.lighting_type == 'pulse':
            lighting_data = (config.lighting_data.on_state
                             if bit
                             else config.lighting_data.off_state)
        elif config.lighting_type == 'rgb':
            lighting_data = (config.lighting_data.on_state
                             if bit
                             else config.lighting_data.off_state)
        else:
            on_state = (config.lighting_data.fg_color_id
                        if config.lighting_data
                        else [fg_color.color_id])
            off_state = (config.lighting_data.bg_color_id
                         if config.lighting_data
                         else ([0] if not bg_color else [bg_color.color_id]))
            lighting_data = (on_state
                             if bit
                             else off_state)
        return lighting_data


class Bitmap(Renderable):
    MIN_WORD_LENGTH = 8
    MAX_WORD_LENGTH = 9

    def __init__(self, bitmap_data, config_data=None):
        self._data = bitmap_data
        self._config = _BitmapConfig(config_data)
        self._max_word_length = self._determine_max_word_length(self._data)

    def __iter__(self):
        for word in self._data:
            bitmask = 1
            for _ in range(self._max_word_length):
                bit = 1 if (word & bitmask) else 0
                yield bit
                bitmask = bitmask << 1
        yield None

    def __repr__(self):
        return 'Bitmap(\'{}\')'.format(self._data)

    def __str__(self):
        return self._data

    @property
    def data(self):
        return self._data

    @property
    def max_word_length(self):
        return self._max_word_length

    @property
    def config(self):
        return self._config

    def render(self):
        pass

    def _determine_max_word_length(self, data):
        if not data:
            return 0

        word_length = 0
        for word in data:
            digit_count = 1
            while word:
                digit_count += 1
                word = word >> 1
            word_length = max(digit_count, word_length)

        return min(max(Bitmap.MIN_WORD_LENGTH, word_length),
                   Bitmap.MAX_WORD_LENGTH)


class Text(Renderable):
    def __init__(self, text, *,
                 fg_color=ColorPalette.Red.SHADE_4,
                 bg_color=None):
        if not isinstance(text, str):
            raise TypeError('Must be of type str.')

        self._text = text
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._glyph_dicts = [_GlyphDictionary('./glyphs/basic_latin.glyph.json',  # noqa
                                              './schema/glyph.schema.json')]
        self._characters = self._create_characters(text, self._glyph_dicts)

    def __repr__(self):
        return 'Text(\'{}\')'.format(self._text)

    def __str__(self):
        return self._text

    @property
    def characters(self):
        return self._characters

    def render(self, matrix):
        for character in self.characters:
            BitmapRenderer(character.bitmap,
                           matrix,
                           fg_color=self._fg_color,
                           bg_color=self._bg_color).render()

    def _create_characters(self, text, dicts):
        characters = []
        for glyph in text:
            for glyph_dict in dicts:
                if glyph in glyph_dict:
                    characters.append(_Character(glyph, Bitmap(glyph_dict[glyph])))  # noqa
                    break
        return characters
