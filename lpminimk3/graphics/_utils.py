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
        pass

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
        return f"GlyphDictionary(filename='{self.filename}')"

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
        if not isinstance(bitmap_data, list):
            raise TypeError("bitmap_data must be of type 'list'.")
        self._data = bitmap_data
        self._config = BitmapConfig(config_data)

    def __iter__(self):
        for word in self._data:
            bitmask = 1
            for _ in range(self.word_count):
                bit = 1 if (word & bitmask) else 0
                yield bit
                bitmask = bitmask << 1

    def __repr__(self):
        return f"RawBitmap('{self._data}')"

    def __str__(self):
        bit_string = ''
        for index, bit in enumerate(self, start=1):
            bit_string += str(bit)
            bit_string += ('\n'
                           if index % self.word_count == 0
                           else ' ')
        return bit_string

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
        return f'Offset({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

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
        return f"LightingConfig('{self._name}')"

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
        return f"BitConfig(name='{self._name}')"

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


class CharacterTransform:
    def __init__(self, character, bitmap_data):
        self._character = character
        self._character_raw_bitmap = RawBitmap(bitmap_data)

    def __repr__(self):
        return ("CharacterTransform("
                f"character='{self._character}')")

    def shift_left(self, *, carry=None, count=1, circular=False):
        count = max(0, count)
        count = count % self._character.word_count
        character = self._character
        for _ in range(count):
            transformed_bitmap_data = []
            temp_bitmap_data = []
            new_carry = 0
            msb_address = self._character.word_count - 1
            for index, word in enumerate(character.raw_bitmap.data):  # noqa
                if carry:
                    temp_bitmap_data.append((word >> 1) | ((carry & (1 << index))  # noqa
                                                            << (msb_address - index)))  # noqa
                else:
                    temp_bitmap_data.append(word >> 1)
                new_carry |= (word & 1) << index
            transformed_bitmap_data = temp_bitmap_data
            if circular and new_carry:
                temp_bitmap_data = []
                for index, word in enumerate(transformed_bitmap_data):  # noqa
                    temp_bitmap_data.append(word | (((new_carry & (1 << index))  # noqa
                                                     >> index << msb_address)))  # noqa
            transformed_bitmap_data = temp_bitmap_data
            character = Character(self._character.glyph,
                                  self._character_raw_bitmap.data,
                                  self._character.fg_color,
                                  self._character.bg_color,
                                  carry=new_carry,
                                  transformed_bitmap_data=transformed_bitmap_data,  # noqa
                                  offset=(self._character.offset.x + count,
                                          self._character.offset.y))
        return character

    def shift_right(self, *, carry=None, count=1, circular=False):
        count = max(0, count)
        count = count % self._character.word_count
        character = self._character
        for _ in range(count):
            transformed_bitmap_data = []
            temp_bitmap_data = []
            new_carry = 0
            msb_address = self._character.word_count - 1
            for index, word in enumerate(character.raw_bitmap.data):  # noqa
                if carry:
                    temp_bitmap_data.append((word << 1) | ((carry & (1 >> index))  # noqa
                                                            >> (msb_address - index)))  # noqa
                else:
                    temp_bitmap_data.append(word << 1)
                new_carry |= (word & (1 << msb_address)) >> (msb_address - index)  # noqa
            transformed_bitmap_data = temp_bitmap_data
            if circular and new_carry:
                temp_bitmap_data = []
                for index, word in enumerate(transformed_bitmap_data):  # noqa
                    temp_bitmap_data.append(word | ((new_carry & (1 << index))  # noqa
                                                     >> index))  # noqa
            transformed_bitmap_data = temp_bitmap_data
            character = Character(self._character.glyph,
                                  self._character_raw_bitmap.data,
                                  self._character.fg_color,
                                  self._character.bg_color,
                                  carry=new_carry,
                                  transformed_bitmap_data=transformed_bitmap_data,  # noqa
                                  offset=(self._character.offset.x - count,
                                          self._character.offset.y))
        return character


class CharacterRenderer:
    def __init__(self, character, matrix):
        self._raw_bitmap = character.raw_bitmap
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
        return ("Character("
                f"glyph='{self._glyph}', "
                f"offset={self._offset}, "
                f"carry={self.carry})")

    def __str__(self):
        return f'{self._glyph}'

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
        return (self._raw_bitmap_transformed
                if self._raw_bitmap_transformed
                else self._raw_bitmap)

    @property
    def offset(self):
        return self._offset

    def render(self, matrix):
        CharacterRenderer(self, matrix).render()

    def print(self):
        print(self.raw_bitmap)

    def shift_left(self, *, carry=None, count=1, circular=False):
        return CharacterTransform(self,
                                  self._raw_bitmap.data)\
                                          .shift_left(carry=carry,
                                                      count=count,
                                                      circular=circular)

    def shift_right(self, *, carry=None, count=1, circular=False):
        return CharacterTransform(self,
                                  self._raw_bitmap.data)\
                                          .shift_right(carry=carry,
                                                       count=count,
                                                       circular=circular)


class String(Renderable):
    def __init__(self, text, *, fg_color, bg_color=None):
        if not isinstance(text, str):
            raise TypeError("text must be of type 'str'.")
        if not len(text):
            raise ValueError("text cannot be empty.")
        self._glyph_dicts = self._create_glyph_dicts()
        characters = self._create_characters(text,
                                             self._glyph_dicts,
                                             fg_color,
                                             bg_color)
        self._characters = list(characters)

    def __repr__(self):
        return ("String("
                f"'{repr(self.character_to_render)}')")

    def __iter__(self):
        return self.bits

    def __str__(self):
        return ''

    @Renderable.bits.getter
    def bits(self):
        for bit in self.character_to_render.raw_bitmap:
            yield bit

    @Renderable.word_count.getter
    def word_count(self):
        return self.character_to_render.word_count

    @property
    def characters(self):
        return self._characters

    @property
    def character_to_render(self):
        return self._characters[0]

    def render(self, matrix):
        CharacterRenderer(self.character_to_render,
                          matrix).render()

    def print(self):
        print(self.character_to_render.raw_bitmap)

    def shift_left(self, *, count=1, circular=True):
        count = 0 if not isinstance(count, int) or count < 0 else count
        if len(self._characters) == 1:
            self._characters[0] = self._characters[0].shift_left(count=count,
                                                                 circular=circular)  # noqa
        else:
            for _ in range(count):
                shifted_characters = []
                carry = 0
                if circular:
                    first_character = self._characters[0].shift_left()
                    carry = first_character.carry
                for character in reversed(self._characters):
                    new_character = character.shift_left(carry=carry)
                    carry = new_character.carry
                    shifted_characters.append(new_character)
                shifted_characters.reverse()
                self._characters = shifted_characters

    def shift_right(self, *, count=1, circular=True):
        count = 0 if not isinstance(count, int) or count < 0 else count
        if len(self._characters) == 1:
            self._characters[0] = self._characters[0].shift_right(count=count,
                                                                  circular=circular)  # noqa
        else:
            for _ in range(count):
                shifted_characters = []
                carry = 0
                if circular:
                    last_character = self._characters[-1].shift_right()
                    carry = last_character.carry
                for character in self._characters:
                    new_character = character.shift_right(carry=carry)
                    carry = new_character.carry
                    shifted_characters.append(new_character)
                self._characters = shifted_characters

    def _create_characters(self, text, dicts, fg_color, bg_color):
        characters = []
        for glyph in text:
            for glyph_dict in dicts:
                if glyph in glyph_dict:
                    characters.append(Character(glyph,
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
                glyph_dicts.append(GlyphDictionary(os.path.join(glyph_dict_dir, filename),  # noqa
                                   './schema/glyph.schema.json'))
        return glyph_dicts