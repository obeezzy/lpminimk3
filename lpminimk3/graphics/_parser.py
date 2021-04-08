import os
from abc import ABC
import json
import jsonschema
from ..midi_messages import Constants,\
                            Colorspec,\
                            ColorspecFragment


class Renderable(ABC):
    @property
    def bits(self):
        yield None

    @property
    def word_count(self):
        return 0

    def render(self, matrix):
        pass


class GlyphDictionary:
    def __init__(self, json_filename, schema_filename):
        self._filename = self._determine_abspath(json_filename)
        self._data = self._load(json_filename)
        schema = self._load(schema_filename)
        self._validate(self._data, schema)

    def __iter__(self):
        for glyph, bitmap_data in self._data.items():
            yield glyph, bitmap_data

    def __contains__(self, unicode):
        return unicode in self._data['glyphs']

    def __getitem__(self, unicode):
        return self._data['glyphs'][unicode]

    def __repr__(self):
        return 'GlyphDictionary(filename=\'{}\')'.format(self.filename)

    def __str__(self):
        return (str(self._data['glyphs'])
                if self._data
                else '')

    @property
    def filename(self):
        return self._filename

    def _load(self, filename):
        data = None
        filename = self._determine_abspath(filename)
        with open(filename) as f:
            data = json.load(f)
        return data

    def _validate(self, data, schema):
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError:
            raise ValueError('Invalid JSON file format.')

    def _determine_abspath(self, filename):
        if not os.path.isabs(filename):
            current_dir = os.path.dirname(__file__)
            return os.path.join(current_dir, filename)
        return filename


class RawBitmap:
    def __init__(self, bitmap_data, config_data=None):
        self._data = bitmap_data
        self._config = BitmapConfig(config_data)

    def __iter__(self):
        for word in self._data:
            bitmask = 1
            for _ in range(self.word_count):
                bit = 1 if (word & bitmask) else 0
                yield bit
                bitmask = bitmask << 1
        yield None

    def __repr__(self):
        return 'RawBitmap(\'{}\')'.format(self._data)

    def __str__(self):
        return self._data

    @property
    def data(self):
        return self._data

    @property
    def word_count(self):
        return len(self._data)

    @property
    def config(self):
        return self._config

    def render(self):
        pass


class Offset:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __repr__(self):
        return 'Offset({}, {})'.format(self.x, self.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class LightingConfig:
    DEFAULT_ON_STATE = 1
    DEFAULT_OFF_STATE = 0

    def __init__(self, lighting_type, *, on_state=None, off_state=None):
        self._lighting_type = lighting_type
        self._on_state = on_state
        self._off_state = off_state

    def __repr__(self):
        return 'LightingConfig(\'{}\')'.format(self._name)

    def __str__(self):
        return self._data

    @property
    def on_state(self):
        return (self._on_state
                if self._on_state
                else [LightingConfig.DEFAULT_ON_STATE])

    @property
    def off_state(self):
        return (self._off_state
                if self._off_state
                else [LightingConfig.DEFAULT_OFF_STATE])


class BitConfig:
    def __init__(self, name=None, config_data=None):
        self._name = name
        self._data = config_data

    def __repr__(self):
        return 'BitConfig(\'{}\')'.format(self._name)

    def __str__(self):
        return self._data

    @property
    def lighting_type(self):
        return (self._data['lighting_type']
                if self._data and 'lighting_type' in self._data
                else Constants.LightingType.STATIC)

    @property
    def name(self):
        return (self._name
                if self._name
                else 'default')

    @property
    def lighting_data(self):
        if self._data:
            return LightingConfig(self.lighting_type,
                                  **self._data.get('lighting_data'))
        return None


class BitmapConfig:
    def __init__(self, config_data):
        self._data = config_data

    def __getitem__(self, name):
        if self._data and name in self._data:
            return self._data[name]
        return BitConfig()


class CharacterRenderer:
    def __init__(self, character, matrix, *, raw_bitmap=None):
        self._raw_bitmap = (raw_bitmap
                            if raw_bitmap
                            else character._raw_bitmap)
        self._matrix = matrix
        self._fg_color = character.fg_color
        self._bg_color = character.bg_color

    def render(self):
        colorspec_fragments = []
        for led, bit in zip(self._matrix.led_range(), self._raw_bitmap):
            bit_config = self._raw_bitmap.config[led.name]
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


class Character(Renderable):
    def __init__(self,
                 glyph,
                 bitmap_data,
                 fg_color,
                 bg_color=None,
                 *,
                 carry=None,
                 transformed_bitmap_data=None,
                 offset=None):
        self._glyph = glyph
        self._raw_bitmap = RawBitmap(bitmap_data)
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._carry = carry
        self._raw_bitmap_transformed = (RawBitmap(transformed_bitmap_data)
                                        if transformed_bitmap_data
                                        else None)
        self._offset = Offset(*offset) if offset else Offset()

    def __repr__(self):
        return 'Character(glyph=\'{}\', offset={})'.format(self._glyph,
                                                           repr(self._offset))

    def __str__(self):
        return self._glyph

    def __iter__(self):
        return self.bits

    @Renderable.bits.getter
    def bits(self):
        for bit in self._raw_bitmap:
            yield bit

    @Renderable.word_count.getter
    def word_count(self):
        return self._raw_bitmap.word_count

    @property
    def glyph(self):
        return self._glyph

    @property
    def fg_color(self):
        return self._fg_color

    @property
    def bg_color(self):
        return self._bg_color

    @property
    def carry(self):
        return self._carry

    @property
    def raw_bitmap(self):
        return self._raw_bitmap

    @property
    def raw_bitmap_transformed(self):
        return self._raw_bitmap_transformed

    @property
    def offset(self):
        return self._offset

    def render(self, matrix):
        CharacterRenderer(self,
                          matrix,
                          raw_bitmap=(self.raw_bitmap_transformed
                                      if self.raw_bitmap_transformed
                                      else self.raw_bitmap)).render()

    def shift_left(self, *, carry=None, count=1):
        bitmap_data = []
        shift_count = count + self.offset.x
        new_carry = 0
        for index, word in enumerate(self._raw_bitmap.data, start=1):
            if carry:
                bitmap_data.append((word >> shift_count) | (carry << (self.word_count - index)))  # noqa
            else:
                bitmap_data.append(word >> shift_count)
            new_carry |= ((word << (self.word_count - index)) >> (index - 1))
        return Character(self.glyph,
                         self._raw_bitmap.data,
                         self._fg_color,
                         self._bg_color,
                         carry=new_carry,
                         transformed_bitmap_data=bitmap_data,
                         offset=(self.offset.x + 1, self.offset.y))

    def shift_right(self, *, carry=None, count=1):
        bitmap_data = []
        shift_count = count + self.offset.x
        new_carry = 0
        for index, word in enumerate(self._raw_bitmap.data, start=1):
            if carry:
                bitmap_data.append((word << shift_count) | (carry >> (self.word_count - index)))  # noqa
            else:
                bitmap_data.append(word << shift_count)
            new_carry |= ((word >> (self.word_count - index)) << (index - 1))
        return Character(self.glyph,
                         self._raw_bitmap.data,
                         self._fg_color,
                         self._bg_color,
                         carry=new_carry,
                         transformed_bitmap_data=bitmap_data,
                         offset=(self.offset.x - 1, self.offset.y))


class String(Renderable):
    def __init__(self, *characters):
        self._characters = list(characters)
        self._character_to_render = self._characters[0]

    def __iter__(self):
        return self.bits

    @Renderable.bits.getter
    def bits(self):
        for bit in self._character_to_render:
            yield bit

    @Renderable.word_count.getter
    def word_count(self):
        return self._character_to_render.word_count

    def render(self, matrix):
        CharacterRenderer(self._character_to_render,
                          matrix).render()

    def shift_left(self):
        carry = None
        self._character_to_render = self._character_to_render.shift_left(carry)

    def shift_right(self):
        carry = None
        self._character_to_render = self._character_to_render.shift_right(carry)  # noqa

    def __repr__(self):
        return 'String(\'{}\')'.format(self._rendered_character.glyph)

    def __str__(self):
        return self._glyph
