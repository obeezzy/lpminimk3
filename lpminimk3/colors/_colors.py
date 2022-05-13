"""
Colors for the Launchpad Mini MK3.
"""

import re


class RgbColor:
    """
    An RGB color.
    """
    _RGB_LENGTH = 3
    _MIN_HEX_LENGTH = 4
    _MAX_HEX_LENGTH = 7
    _MIN_COLOR_VALUE = 0
    _MAX_COLOR_VALUE = 255

    def __init__(self, value):
        if (not isinstance(value, str)
                and not isinstance(value, (tuple, list))):
            raise TypeError('RGB color must be str or tuple or list.')
        if (isinstance(value, str)
            and len(value) != RgbColor._MIN_HEX_LENGTH
                and len(value) != RgbColor._MAX_HEX_LENGTH):
            raise ValueError('Only hex values in the '
                             '#rgb and #rrggbb formats are accepted.')
        self._parse(value)

    def __repr__(self):
        return f'RgbColor(r={self.r}, g={self.g}, b={self.b})'

    @staticmethod
    def is_valid(value):
        """
        Returns `True` if `value` is a valid (r,g,b) or hex value,
        otherwise returns `False`.
        """
        if isinstance(value, str):
            match = re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', value)
            return True if match else False
        elif isinstance(value, (tuple, list)):
            valid_values = list(filter(lambda rgb_value: min(RgbColor._MAX_COLOR_VALUE,  # noqa
                                                             max(rgb_value, RgbColor._MIN_COLOR_VALUE)) == rgb_value,  # noqa
                                       value))
            return (len(valid_values) == len(value)
                    and len(value) == RgbColor._RGB_LENGTH)
        return False

    @property
    def value(self):
        """
        RGB value, as string.
        """
        return self._value

    @property
    def r(self):
        """
        Red value
        """
        return self._r >> 1

    @property
    def g(self):
        """
        Green value
        """
        return self._g >> 1

    @property
    def b(self):
        """
        Blue value
        """
        return self._b >> 1

    def _parse(self, value):
        if (isinstance(value, str)
                and len(value) == RgbColor._MIN_HEX_LENGTH):
            self._r = int(value[1], 16)
            self._g = int(value[2], 16)
            self._b = int(value[3], 16)
            self._value = value
        elif (isinstance(value, str)
                and len(value) == RgbColor._MAX_HEX_LENGTH):
            self._r = int(value[1:3], 16)
            self._g = int(value[3:5], 16)
            self._b = int(value[5:7], 16)
            self._value = value
        elif (isinstance(value, (tuple, list))
                and len(value) == RgbColor._RGB_LENGTH):
            self._r = value[0]
            self._g = value[1]
            self._b = value[2]
            self._value = value


class ColorShade:
    """
    A color shade.

    A color shade is color from the Launchpad's color palette.
    There are 128 valid color shades, ranging from ID 0 to 127
    (with ID 0 used for OFF).
    """

    MIN_COLOR_ID = 0
    MAX_COLOR_ID = 127
    HEX_VALUES = [
            '#616161',
            '#b3b3b3',
            '#ffffff',
            '#ffb3b3',
            '#ff6161',  # 5
            '#dd6161',
            '#b36161',
            '#fff3d5',
            '#ffb361',
            '#dd8c61',  # 10
            '#b37661',
            '#ffeea1',
            '#ffff61',
            '#dddd61',
            '#b3b361',  # 15
            '#ddffa1',
            '#a1dd61',
            '#81b361',
            '#c2ffb3',
            '#c2ffb3',  # 20
            '#61ff61',
            '#61dd61',
            '#61b361',
            '#c2ffc2',
            '#61ff8c',  # 25
            '#61dd76',
            '#61b36b',
            '#c2ffcc',
            '#61ffcc',
            '#61dda1',  # 30
    ]

    def __init__(self, color_id, color_group):
        self._color_id = color_id
        self._color_group = color_group

    def __repr__(self):
        return ('ColorShade('
                f'group={self.color_group}, '
                f'id={self.color_id})')

    @staticmethod
    def is_valid_id(value):
        """
        Returns `True` if `value` is a valid color ID,
        otherwise returns `False`.
        """
        return (True
                if isinstance(value, int)
                and value >= ColorShade.MIN_COLOR_ID
                and value <= ColorShade.MAX_COLOR_ID
                else False)

    @property
    def hex(self):
        """Hex color code."""
        return ColorShade.HEX_VALUES[self._color_id]

    @property
    def color_id(self):
        """Unique color ID."""
        return self._color_id

    @property
    def color_group(self):
        """Color group."""
        return self._color_group


class ColorPalette:
    """
    Color palette of Launchpad.

    The color palette contains 127 predefined color shades.
    """
    class Red:
        SHADE_1 = ColorShade(0x04, 'red')
        SHADE_2 = ColorShade(0x05, 'red')
        SHADE_3 = ColorShade(0x06, 'red')
        SHADE_4 = ColorShade(0x07, 'red')
        SHADE_5 = ColorShade(0x48, 'red')
        SHADE_6 = ColorShade(0x6a, 'red')
        SHADE_7 = ColorShade(0x6b, 'red')
        SHADE_8 = ColorShade(0x78, 'red')
        SHADE_9 = ColorShade(0x79, 'red')

    class Orange:
        SHADE_1 = ColorShade(0x09, 'orange')
        SHADE_2 = ColorShade(0x0a, 'orange')
        SHADE_3 = ColorShade(0x0b, 'orange')
        SHADE_4 = ColorShade(0x3c, 'orange')
        SHADE_5 = ColorShade(0x53, 'orange')
        SHADE_6 = ColorShade(0x54, 'orange')
        SHADE_7 = ColorShade(0x60, 'orange')
        SHADE_8 = ColorShade(0x6c, 'orange')
        SHADE_9 = ColorShade(0x7e, 'orange')
        SHADE_10 = ColorShade(0x7f, 'orange')

    class Yellow:
        SHADE_1 = ColorShade(0x08, 'yellow')
        SHADE_2 = ColorShade(0x0c, 'yellow')
        SHADE_3 = ColorShade(0x3d, 'yellow')
        SHADE_4 = ColorShade(0x3e, 'yellow')
        SHADE_5 = ColorShade(0x49, 'yellow')
        SHADE_6 = ColorShade(0x4a, 'yellow')
        SHADE_7 = ColorShade(0x61, 'yellow')
        SHADE_8 = ColorShade(0x63, 'yellow')
        SHADE_9 = ColorShade(0x64, 'yellow')
        SHADE_10 = ColorShade(0x69, 'yellow')
        SHADE_11 = ColorShade(0x6d, 'yellow')
        SHADE_12 = ColorShade(0x71, 'yellow')
        SHADE_13 = ColorShade(0x7c, 'yellow')
        SHADE_14 = ColorShade(0x7d, 'yellow')

    class Blue:
        SHADE_1 = ColorShade(0x24, 'blue')
        SHADE_2 = ColorShade(0x25, 'blue')
        SHADE_3 = ColorShade(0x26, 'blue')
        SHADE_4 = ColorShade(0x27, 'blue')
        SHADE_5 = ColorShade(0x28, 'blue')
        SHADE_6 = ColorShade(0x29, 'blue')
        SHADE_7 = ColorShade(0x2a, 'blue')
        SHADE_8 = ColorShade(0x2b, 'blue')
        SHADE_9 = ColorShade(0x41, 'blue')
        SHADE_10 = ColorShade(0x42, 'blue')
        SHADE_11 = ColorShade(0x4e, 'blue')
        SHADE_12 = ColorShade(0x4f, 'blue')
        SHADE_13 = ColorShade(0x5a, 'blue')
        SHADE_14 = ColorShade(0x5b, 'blue')
        SHADE_15 = ColorShade(0x5c, 'blue')
        SHADE_16 = ColorShade(0x67, 'blue')
        SHADE_17 = ColorShade(0x68, 'blue')

    class Green:
        SHADE_1 = ColorShade(0x0d, 'green')
        SHADE_2 = ColorShade(0x0e, 'green')
        SHADE_3 = ColorShade(0x0f, 'green')
        SHADE_4 = ColorShade(0x10, 'green')
        SHADE_5 = ColorShade(0x11, 'green')
        SHADE_6 = ColorShade(0x12, 'green')
        SHADE_7 = ColorShade(0x13, 'green')
        SHADE_8 = ColorShade(0x14, 'green')
        SHADE_9 = ColorShade(0x15, 'green')
        SHADE_10 = ColorShade(0x16, 'green')
        SHADE_11 = ColorShade(0x17, 'green')
        SHADE_12 = ColorShade(0x18, 'green')
        SHADE_13 = ColorShade(0x19, 'green')
        SHADE_14 = ColorShade(0x1a, 'green')
        SHADE_15 = ColorShade(0x1b, 'green')
        SHADE_16 = ColorShade(0x1c, 'green')
        SHADE_17 = ColorShade(0x1d, 'green')
        SHADE_18 = ColorShade(0x1e, 'green')
        SHADE_19 = ColorShade(0x1f, 'green')
        SHADE_20 = ColorShade(0x20, 'green')
        SHADE_21 = ColorShade(0x21, 'green')
        SHADE_22 = ColorShade(0x22, 'green')
        SHADE_23 = ColorShade(0x23, 'green')
        SHADE_24 = ColorShade(0x3f, 'green')
        SHADE_25 = ColorShade(0x40, 'green')
        SHADE_26 = ColorShade(0x41, 'green')
        SHADE_27 = ColorShade(0x44, 'green')
        SHADE_28 = ColorShade(0x4b, 'green')
        SHADE_29 = ColorShade(0x4c, 'green')
        SHADE_30 = ColorShade(0x4d, 'green')
        SHADE_31 = ColorShade(0x55, 'green')
        SHADE_32 = ColorShade(0x56, 'green')
        SHADE_33 = ColorShade(0x57, 'green')
        SHADE_34 = ColorShade(0x58, 'green')
        SHADE_35 = ColorShade(0x59, 'green')
        SHADE_36 = ColorShade(0x62, 'green')
        SHADE_37 = ColorShade(0x65, 'green')
        SHADE_38 = ColorShade(0x66, 'green')
        SHADE_39 = ColorShade(0x6e, 'green')
        SHADE_40 = ColorShade(0x6f, 'green')
        SHADE_41 = ColorShade(0x72, 'green')
        SHADE_42 = ColorShade(0x7a, 'green')
        SHADE_43 = ColorShade(0x7b, 'green')

    class Violet:
        SHADE_1 = ColorShade(0x2c, 'violet')
        SHADE_2 = ColorShade(0x2d, 'violet')
        SHADE_3 = ColorShade(0x2e, 'violet')
        SHADE_4 = ColorShade(0x2f, 'violet')
        SHADE_5 = ColorShade(0x30, 'violet')
        SHADE_6 = ColorShade(0x31, 'violet')
        SHADE_7 = ColorShade(0x32, 'violet')
        SHADE_8 = ColorShade(0x33, 'violet')
        SHADE_9 = ColorShade(0x34, 'violet')
        SHADE_10 = ColorShade(0x35, 'violet')
        SHADE_11 = ColorShade(0x36, 'violet')
        SHADE_12 = ColorShade(0x37, 'violet')
        SHADE_13 = ColorShade(0x38, 'violet')
        SHADE_14 = ColorShade(0x39, 'violet')
        SHADE_15 = ColorShade(0x3a, 'violet')
        SHADE_16 = ColorShade(0x3b, 'violet')
        SHADE_17 = ColorShade(0x43, 'violet')
        SHADE_18 = ColorShade(0x45, 'violet')
        SHADE_19 = ColorShade(0x46, 'violet')
        SHADE_20 = ColorShade(0x47, 'violet')
        SHADE_21 = ColorShade(0x50, 'violet')
        SHADE_22 = ColorShade(0x51, 'violet')
        SHADE_23 = ColorShade(0x52, 'violet')
        SHADE_24 = ColorShade(0x5d, 'violet')
        SHADE_25 = ColorShade(0x5e, 'violet')
        SHADE_26 = ColorShade(0x5f, 'violet')
        SHADE_27 = ColorShade(0x70, 'violet')
        SHADE_28 = ColorShade(0x73, 'violet')
        SHADE_29 = ColorShade(0x74, 'violet')

    class White:
        SHADE_1 = ColorShade(0x01, 'white')
        SHADE_2 = ColorShade(0x02, 'white')
        SHADE_3 = ColorShade(0x03, 'white')
        SHADE_4 = ColorShade(0x75, 'white')
        SHADE_5 = ColorShade(0x76, 'white')
        SHADE_6 = ColorShade(0x77, 'white')


class ColorShadeStore:
    """
    Color shade store for the Launchpad.
    """
    COLOR_GROUPS = ['red', 'orange', 'yellow', 'green',
                    'blue', 'violet', 'white']
    COLOR_GROUP_SYMBOLS = list(map(lambda color: color[0],
                                   COLOR_GROUPS))

    def __iter__(self):
        for color_group in ColorShadeStore.COLOR_GROUPS:
            color_shades_in_group = ColorPalette.__dict__[color_group.capitalize()].__dict__  # noqa
            for _, color_shade in color_shades_in_group.items():
                if isinstance(color_shade, ColorShade):
                    yield color_shade

    def contains(self, value):
        """
        Searches for color shade `value` and returns `True` if
        the color shade exists, otherwise returns `False`.
        """
        color, _ = self._parse(value)
        return True if color else False

    def find(self, value):
        """
        Searches for color shade `value` and returns the
        `ColorShade` if found, otherwise returns `None`.
        """
        if isinstance(value, ColorShade):
            return value
        return self._find_shade(*self._parse(value))

    def _find_shade(self, color, color_shade_id=1):
        if not color:
            return None

        color_shade = None
        color_shades_in_group = ColorPalette.__dict__[color.capitalize()].__dict__  # noqa
        if color_shade_id:
            shade_clause = f'SHADE_{color_shade_id}'
            if shade_clause in color_shades_in_group:
                color_shade = color_shades_in_group[shade_clause]
        else:
            color_shade = color_shades_in_group['SHADE_1']

        return color_shade

    def _color_from_symbol(self, symbol):
        return ColorShadeStore.COLOR_GROUPS[ColorShadeStore.COLOR_GROUP_SYMBOLS.index(symbol)]  # noqa

    # Valid input: red, o, y2, green3
    def _parse(self, value):
        color = None
        color_shade_id = None

        if isinstance(value, str):
            has_digit_suffix = re.search('[0-9]+', value)
            if has_digit_suffix:
                match = re.match('([a-z]+)([0-9]+)', value.lower())
                if match and len(match.groups()) == 2:
                    color = (match.group(1)
                             if match.group(1) in ColorShadeStore.COLOR_GROUPS
                             else None)
                    color = (self._color_from_symbol(match.group(1))
                             if not color and match.group(1)
                             in ColorShadeStore.COLOR_GROUP_SYMBOLS
                             else color)
                    color_shade_id = int(match.group(2))
                else:
                    color = None
                    color_shade_id = None
            elif value.lower() in ColorShadeStore.COLOR_GROUPS:
                color = value.lower()
                color_shade_id = 1
            elif value.lower() in ColorShadeStore.COLOR_GROUP_SYMBOLS:
                color = self._color_from_symbol(value.lower())
                color_shade_id = 1

        return (color, color_shade_id)
