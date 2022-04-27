import os
from abc import ABC
import time
import math
from functools import reduce
from ..colors._colors import ColorShade, ColorShadeStore, RgbColor
from ..midi_messages import Colorspec,\
                            ColorspecFragment,\
                            Constants
from ._parser import GlyphDictionary,\
                     BitmapDocument,\
                     BitmapConfig


class Renderable(ABC):
    @property
    def bits(self):
        pass

    @property
    def word_count(self):
        return 0

    def render(self, matrix):
        pass


class BitmapRenderer:
    def __init__(self,
                 raw_bitmap,
                 matrix, *,
                 fg_color,
                 bg_color):
        self._raw_bitmap = raw_bitmap
        self._matrix = matrix
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._angle = 0
        self._flip_axis = 'x'

    def render(self):
        colorspec_fragments = []
        for led, bit in zip(self._matrix.led_range(rotation=self._angle,
                                                   flip_axis=self._flip_axis),
                            self._raw_bitmap):
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
        if config.lighting_type == Constants.LightingType.FLASH:
            lighting_data = ([config.lighting_data.on_state.color.id]
                             if bit
                             else [config.lighting_data.off_state.color.id])
        elif config.lighting_type == Constants.LightingType.PULSE:
            lighting_data = ([config.lighting_data.on_state.color.id]
                             if bit
                             else [config.lighting_data.off_state.color.id])
        elif config.lighting_type == Constants.LightingType.RGB:
            lighting_data = (config.lighting_data.on_state.color.rgb
                             if bit
                             else config.lighting_data.off_state.color.rgb)
        else:
            on_state = ([config.lighting_data.on_state.color.id]
                        if config.lighting_data
                        else [fg_color.color_id])
            off_state = ([config.lighting_data.off_state.color.id]
                         if config.lighting_data
                         else ([0]
                               if not bg_color
                               else [bg_color.color_id]))
            lighting_data = (on_state
                             if bit
                             else off_state)
        return lighting_data


class RawBitmapMatrix:
    def __init__(self, raw_bitmap):
        self._raw_bitmap = raw_bitmap
        self._raw_matrix = self._load(raw_bitmap)

    def __repr__(self):
        return ('RawBitmapMatrix('
                f'bit={self._raw_matrix})')

    def bit(self, x, y):
        return self._raw_matrix[y][x]

    def rotated_range(self, angle, *, flip_axis=''):
        assert angle, 'Angle cannot be zero.'
        angle = self._normalize_angle(angle)
        angle = self._flip_angle(angle)
        angle_rad = math.radians(angle)
        for index, bit in enumerate(self._raw_bitmap):
            x = int(index / self._raw_bitmap.word_count)
            y = int(index % self._raw_bitmap.word_count)
            max_x = max_y = self._raw_bitmap.word_count - 1
            rotated_x = round((y * math.sin(angle_rad)) + (x * math.cos(angle_rad)))  # noqa
            rotated_y = round((y * math.cos(angle_rad)) - (x * math.sin(angle_rad)))  # noqa
            x_flip_required = y_flip_required = False
            if angle == 90:
                rotated_y = min(max_y + rotated_y, max_y)
                x_flip_required = (FlipAxis.X in flip_axis)
                y_flip_required = (FlipAxis.Y in flip_axis)
            elif angle == 180:
                rotated_y = min(max_y + rotated_y, max_y)
                rotated_x = min(max_x + rotated_x, max_x)
                x_flip_required = FlipAxis.Y in flip_axis
                y_flip_required = FlipAxis.X in flip_axis
            elif angle == 270:
                rotated_x = min(max_x + rotated_x, max_x)
                x_flip_required = (FlipAxis.X in flip_axis)
                y_flip_required = (FlipAxis.Y in flip_axis)
            if flip_axis:
                flipped_x = (self._flip_axis(rotated_x)
                             if x_flip_required
                             else rotated_x)
                flipped_y = (self._flip_axis(rotated_y)
                             if y_flip_required
                             else rotated_y)
                yield self.bit(flipped_x, flipped_y)
            else:
                yield self.bit(rotated_x, rotated_y)

    def flipped_range(self, axis):
        for index, bit in enumerate(self._raw_bitmap):
            x = int(index / self._raw_bitmap.word_count)
            y = int(index % self._raw_bitmap.word_count)
            flipped_x = (self._flip_axis(x)
                         if FlipAxis.Y in axis
                         else x)
            flipped_y = (self._flip_axis(y)
                         if FlipAxis.X in axis
                         else y)
            yield self.bit(flipped_x, flipped_y)

    def _blank_matrix(self):
        matrix = []
        for _ in range(self._raw_bitmap.word_count):
            matrix.append([])
            for _ in range(self._raw_bitmap.word_count):
                matrix[-1].append(0)
        return matrix

    def _load(self, raw_bitmap):
        matrix = self._blank_matrix()
        for index, bit in enumerate(raw_bitmap):
            x = int(index % raw_bitmap.word_count)
            y = int(index / raw_bitmap.word_count)
            matrix[x][y] = bit

        return matrix

    def _normalize_angle(self, angle):
        if angle and (angle % 90) == 0 and abs(angle) > 270:
            return angle % 360
        assert (round(abs(angle)) in (0, 90, 180, 270)), \
               'Angle must be a multiple of 90.'
        return angle

    def _flip_axis(self, value):
        max_value = self._raw_bitmap.word_count - 1
        return max_value - value

    def _flip_angle(self, angle):
        if angle == -90 or angle == 270:
            return 90
        elif angle == -180:
            return 180
        elif angle == 90 or angle == -270:
            return 270
        return angle


class RawBitmap:
    def __init__(self, bitmap_data, config_data=None):
        assert isinstance(bitmap_data, list)
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


class RenderableColor:
    def __init__(self, renderable, value):
        self._renderable = renderable
        self._value = value
        self._validate(value)

    def __repr__(self):
        return f'RenderableColor({self._value})'

    @property
    def color_id(self):
        return self._color_id

    def set(self, value):
        self._validate(value)
        return self._renderable

    def _validate(self, value):
        if not value:
            self._color_id = 0
        elif (not isinstance(value, ColorShade)
                and not isinstance(value, str)
                and not isinstance(value, int)
                and not isinstance(value, (tuple, list))):
            raise TypeError('Must be of type ColorShade '
                            'or str or int or tuple or list.')
        elif ((isinstance(value, str)
                and not ColorShadeStore().contains(value)
                and not RgbColor.is_valid(value))
                or (isinstance(value, (tuple, list))
                    and not RgbColor.is_valid(value))):
            raise ValueError('Invalid color.')
        elif RgbColor.is_valid(value):
            self._rgb_color = RgbColor(value)
        else:
            self._color_id = self._determine_color_id(value)

    def _determine_color_id(self, value):
        color_id = (value
                    if ColorShade.is_valid_id(value)
                    else -1)
        if color_id < 0:
            color_shade = ColorShadeStore().find(value)
            color_id = (color_shade.color_id
                        if color_shade
                        else color_id)
        if color_id < 0:
            raise ValueError(f'Color ID values must be between '
                             f'{ColorShade.MIN_COLOR_ID} and '
                             f'{ColorShade.MAX_COLOR_ID}.')
        return color_id


class TextScroll:
    def __init__(self,
                 text,
                 period,
                 direction,
                 *,
                 cycle_func,
                 timeout,
                 count):
        if timeout:
            assert period < timeout
        if cycle_func:
            assert callable(cycle_func)

        self._text = text
        self._period = period
        self._direction = direction
        self._cycle_func = cycle_func
        self._timeout = -1 if not timeout else timeout
        self._count = -1 if not count else count

    def render(self, string, matrix):
        time_left = self._timeout
        rotations_left = self._count
        text_width = len(self._text) * matrix.width
        while time_left and rotations_left:
            for _ in range(text_width):
                if self._direction == ScrollDirection.RIGHT:
                    string.shift_right()
                else:
                    string.shift_left()
                CharacterRenderer(string.character_to_render,
                                  matrix,
                                  angle=string.angle,
                                  flip_axis=string.flip_axis).render()
                if self._cycle_func:
                    self._cycle_func(_/text_width, matrix.launchpad)
                time.sleep(self._period)
                time_left = (max(time_left - self._period, 0)
                             if time_left != -1
                             else time_left)
            rotations_left = (max(rotations_left - 1, 0)
                              if rotations_left != -1
                              else rotations_left)

    def print(self, *,
              string,
              one,
              zero):
        time_left = self._timeout
        rotations_left = self._count
        while time_left and rotations_left:
            for _ in range(len(self._text) * string.character_to_render.word_count):  # noqa
                if self._direction == ScrollDirection.RIGHT:
                    string.shift_right()
                else:
                    string.shift_left()
                for index, bit in enumerate(string.character_to_render.raw_bitmap,  # noqa
                                            start=1):
                    if bit:
                        print(one, end='')
                    else:
                        print(zero, end='')
                    if index % string.character_to_render.word_count == 0:
                        print('\n', end='')
                time.sleep(self._period)
                time_left = (max(time_left - self._period, 0)
                             if time_left != -1
                             else time_left)
                os.system('clear')
                print('\r', end='')
            rotations_left = (max(rotations_left - 1, 0)
                              if rotations_left != -1
                              else rotations_left)


class ScrollDirection:
    LEFT = 'left'
    RIGHT = 'right'


class FlipAxis:
    X = 'x'
    Y = 'y'
    XY = 'xy'


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
            for index, word in enumerate(character.raw_bitmap.data):
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
                    temp_bitmap_data.append(word | (((new_carry & (1 << index))
                                                     >> index << msb_address)))
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
            for index, word in enumerate(character.raw_bitmap.data):
                if carry:
                    temp_bitmap_data.append((word << 1) | ((carry & (1 << (msb_address - index)))  # noqa
                                                            >> (msb_address - index)))  # noqa
                else:
                    temp_bitmap_data.append(word << 1)
                new_carry |= (word & (1 << msb_address)) >> index
            transformed_bitmap_data = temp_bitmap_data
            if circular and new_carry:
                temp_bitmap_data = []
                for index, word in enumerate(transformed_bitmap_data):
                    temp_bitmap_data.append(word | ((new_carry & (1 << index))  # noqa
                                                    >> index))
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
    def __init__(self,
                 character,
                 matrix, *,
                 angle=0,
                 flip_axis=''):
        self._raw_bitmap = character.raw_bitmap
        self._matrix = matrix
        self._fg_color = character.fg_color
        self._bg_color = character.bg_color
        self._angle = angle
        self._flip_axis = flip_axis

    def render(self):
        colorspec_fragments = []
        for led, bit in zip(self._matrix.led_range(rotation=self._angle,
                                                   flip_axis=self._flip_axis),
                            self._raw_bitmap):
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
        if config.lighting_type == Constants.LightingType.FLASH:
            lighting_data = (config.lighting_data.on_state
                             if bit
                             else config.lighting_data.off_state)
        elif config.lighting_type == Constants.LightingType.PULSE:
            lighting_data = (config.lighting_data.on_state
                             if bit
                             else config.lighting_data.off_state)
        elif config.lighting_type == Constants.LightingType.RGB:
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
                 bg_color,
                 *,
                 carry=None,
                 transformed_bitmap_data=None,
                 offset=None):
        assert isinstance(fg_color, RenderableColor)
        assert isinstance(bg_color, RenderableColor)

        self._glyph = glyph
        self._raw_bitmap = RawBitmap(bitmap_data)
        self._fg_color = fg_color
        self._bg_color = bg_color
        self._carry = carry
        self._raw_bitmap_transformed = (RawBitmap(transformed_bitmap_data)
                                        if transformed_bitmap_data
                                        else None)
        self._offset = (Offset(*offset)
                        if offset
                        else Offset())
        self._angle = 0
        self._flip_axis = ''

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

    @fg_color.setter
    def fg_color(self, color):
        assert isinstance(color, RenderableColor)
        self._fg_color = color

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        assert isinstance(color, RenderableColor)
        self._bg_color = color

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
        CharacterRenderer(self,
                          matrix,
                          angle=self._angle,
                          flip_axis=self._flip_axis).render()

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

    def rotate(self, angle):
        self._angle = angle


class String(Renderable):
    def __init__(self, text, *, fg_color, bg_color):
        assert isinstance(fg_color, RenderableColor)
        assert isinstance(bg_color, RenderableColor)

        if text and not isinstance(text, str):
            raise TypeError("text must be of type 'str'.")

        glyph_dicts = self._create_glyph_dicts()
        characters = self._create_characters(text,
                                             glyph_dicts,
                                             fg_color,
                                             bg_color)
        self._text = text
        self._characters = list(characters)
        self._angle = 0
        self._text_scroll = None
        self._flip_axis = ''

    def __repr__(self):
        return (f"String('{self}')")

    def __str__(self):
        char_list = list(reduce(lambda literal, char: literal + str(char),
                                self._characters, ''))
        return f"{''.join(char_list)}"

    @Renderable.bits.getter
    def bits(self):
        if self.angle:
            matrix = RawBitmapMatrix(self.character_to_render.raw_bitmap)
            for bit in matrix.rotated_range(self.angle,
                                            flip_axis=self.flip_axis):
                yield bit
        elif self.flip_axis:
            matrix = RawBitmapMatrix(self.character_to_render.raw_bitmap)
            for bit in matrix.flipped_range(self._flip_axis):
                yield bit
        else:
            for bit in self.character_to_render.raw_bitmap:
                yield bit

    @Renderable.word_count.getter
    def word_count(self):
        return self.character_to_render.word_count

    @property
    def fg_color(self):
        return self.character_to_render.fg_color

    @fg_color.setter
    def fg_color(self, color):
        assert isinstance(color, RenderableColor)
        self.character_to_render.fg_color = color

    @property
    def bg_color(self):
        return self.character_to_render.bg_color

    @bg_color.setter
    def bg_color(self, color):
        assert isinstance(color, RenderableColor)
        self.character_to_render.bg_color = color

    @property
    def characters(self):
        return self._characters

    @property
    def character_to_render(self):
        return self._characters[0]

    @property
    def angle(self):
        return self._angle

    @property
    def flip_axis(self):
        return self._flip_axis

    @flip_axis.setter
    def flip_axis(self, flip_axis):
        assert isinstance(flip_axis, str)
        assert flip_axis in FlipAxis.XY
        self._flip_axis = flip_axis

    @property
    def text_scroll(self):
        return self._text_scroll

    @text_scroll.setter
    def text_scroll(self, text_scroll):
        if not isinstance(text_scroll, TextScroll):
            raise ValueError("Must be of type 'TextScroll'.")
        self._text_scroll = text_scroll

    def render(self, matrix):
        if self._text_scroll:
            self._text_scroll.render(self, matrix)
        else:
            CharacterRenderer(self.character_to_render,
                              matrix,
                              angle=self.angle,
                              flip_axis=self.flip_axis).render()

    def print(self, *,
              one='X',
              zero=' '):
        if self._text_scroll:
            self._text_scroll.print(string=self,
                                    one=one,
                                    zero=zero)
        else:
            self._print_in_console(one=one, zero=zero)

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
                    shifted_first_character = self._characters[0].shift_left()
                    carry = shifted_first_character.carry
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
                    shifted_last_character = self._characters[-1].shift_right()
                    carry = shifted_last_character.carry
                for character in self._characters:
                    new_character = character.shift_right(carry=carry)
                    carry = new_character.carry
                    shifted_characters.append(new_character)
                self._characters = shifted_characters

    def rotate(self, angle):
        self._angle = angle

    def _create_characters(self, text, dicts, fg_color, bg_color):
        characters = []
        text = '\u0000' if not text else text
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
                glyph_dicts.append(GlyphDictionary(os.path.join(glyph_dict_dir, filename)))  # noqa
        return glyph_dicts

    def _print_in_console(self, one='X', zero=' '):
        matrix = RawBitmapMatrix(self.character_to_render.raw_bitmap)
        if self.flip_axis and not self.angle:
            for index, bit in enumerate(matrix.flipped_range(self.flip_axis),   # noqa
                                        start=1):  # noqa
                self._print_bit(bit, index, one=one, zero=zero)
        elif self.angle:
            for index, bit in enumerate(matrix.rotated_range(self._angle,
                                                             flip_axis=self.flip_axis),  # noqa
                                        start=1):
                self._print_bit(bit, index, one=one, zero=zero)
        else:
            for index, bit in enumerate(self.character_to_render.raw_bitmap,
                                        start=1):
                self._print_bit(bit, index, one=one, zero=zero)

    def _print_bit(self, bit, index, *, one, zero):
        if bit:
            print(one[0], end='')
        elif 'LOGLEVEL' in os.environ:
            print('.', end='')
        else:
            print(zero[0], end='')
        if index % self.character_to_render.word_count == 0:
            print('\n', end='')


class BitmapPrivate(Renderable):
    def __init__(self,
                 filename, *,
                 fg_color,
                 bg_color):
        assert isinstance(filename, str)
        assert isinstance(fg_color, RenderableColor)
        assert isinstance(bg_color, RenderableColor)
        self._bitmap_document = BitmapDocument(filename)
        self._raw_bitmap = RawBitmap(self._bitmap_document.bitmap_data,
                                     self._bitmap_document.bitmap_config)
        self._fg_color = fg_color
        self._bg_color = bg_color

    def __repr__(self):
        return (f"BitmapPrivate('{self}')")

    def __str__(self):
        return repr(self)

    @Renderable.bits.getter
    def bits(self):
        for bit in self.raw_bitmap:
            yield bit

    @Renderable.word_count.getter
    def word_count(self):
        return self._raw_bitmap.word_count

    @property
    def filename(self):
        return self._bitmap_document.filename

    @property
    def raw_bitmap(self):
        return self._raw_bitmap

    @property
    def fg_color(self):
        return self._fg_color

    @fg_color.setter
    def fg_color(self, color):
        assert isinstance(color, RenderableColor)
        self._fg_color = color

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        assert isinstance(color, RenderableColor)
        self._bg_color = color

    def render(self, matrix):
        BitmapRenderer(self.raw_bitmap,
                       matrix,
                       fg_color=self.fg_color,
                       bg_color=self.bg_color).render()

    def print(self, *,
              one='X',
              zero=' '):
        for index, bit in enumerate(self.raw_bitmap,
                                    start=1):
            self._print_bit(bit, index, one=one, zero=zero)

    def _print_bit(self, bit, index, *, one, zero):
        if bit:
            print(one[0], end='')
        elif 'LOGLEVEL' in os.environ:
            print('.', end='')
        else:
            print(zero[0], end='')
        if index % self.raw_bitmap.word_count == 0:
            print('\n', end='')
