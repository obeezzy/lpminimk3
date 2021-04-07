from abc import ABC
from ..midi_messages import Colorspec,\
                            ColorspecFragment
from ._parser import GlyphDictionary as _GlyphDictionary,\
                     BitmapConfig as _BitmapConfig,\
                     Character as _Character


class Renderable(ABC):
    def render(self, matrix):
        pass


class Bitmap(Renderable):
    def __init__(self, bitmap_data, config_data=None):
        self._data = bitmap_data
        self._config = _BitmapConfig(config_data)

    def __iter__(self):
        for word in self._data:
            bitmask = 1 << len(self._data)
            while bitmask:
                bit = 1 if (word & bitmask) else 0
                yield bit
                bitmask = bitmask >> 1
        yield None

    @property
    def data(self):
        return self._data

    @property
    def config(self):
        return self._config

    def render(self):
        pass

    def __repr__(self):
        return 'Bitmap(\'{}\')'.format(self._data)

    def __str__(self):
        return self._data


class Text(Renderable):
    def __init__(self, text):
        if not isinstance(text, str):
            raise TypeError('Must be of type str.')

        self._text = text
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
        colorspec_fragments = []
        for character in self.characters:
            for led, bit in zip(matrix.led_range(), character.bitmap):
                bit_config = character.bitmap.config[led.name]
                lighting_type = bit_config.lighting_type
                led_index = led.midi_value
                lighting_data = self._determine_lighting_data(bit_config, bit)
                fragment = ColorspecFragment(lighting_type, led_index, *lighting_data)  # noqa
                colorspec_fragments.append(fragment)
        payload = Colorspec(*colorspec_fragments)
        matrix.launchpad.send_message(payload)

    def _create_characters(self, text, dicts):
        characters = []
        for glyph in text:
            for glyph_dict in dicts:
                if glyph in glyph_dict:
                    characters.append(_Character(glyph, Bitmap(glyph_dict[glyph])))  # noqa
                    break
        return characters

    def _determine_lighting_data(self, config, bit):
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
            lighting_data = (config.lighting_data.on_state
                             if bit
                             else config.lighting_data.off_state)
        return lighting_data
