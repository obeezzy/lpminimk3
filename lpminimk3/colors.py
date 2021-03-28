"""
Colors for the Launchpad Mini MK3.
"""

import re


class RgbColor:
    """An RGB color."""
    _MIN_HEX_LENGTH = 4
    _MAX_HEX_LENGTH = 7
    _MIN_COLOR_VALUE = 0
    _MAX_COLOR_VALUE = 255

    def __init__(self, value):
        if (not isinstance(value, str)
            and not isinstance(value, tuple)
                and not isinstance(value, list)):
            raise RuntimeError('RGB color must be str or tuple or list.')
        if (isinstance(value, str)
            and len(value) != RgbColor._MIN_HEX_LENGTH
                and len(value) != RgbColor._MAX_HEX_LENGTH):
            raise RuntimeError('Only hex values in the '
                               '#rgb and #rrggbb formats are accepted.')
        self._parse(value)

    @staticmethod
    def is_valid(value):
        """
        Returns `True` if `value` is a valid (r,g,b) or hex value,
        otherwise returns `False`.
        """
        if isinstance(value, str):
            match = re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', value)
            return True if match else False
        elif isinstance(value, tuple) or isinstance(value, list):
            valid_values = []
            for rgb_value in value:
                if rgb_value >= RgbColor._MIN_COLOR_VALUE \
                        and rgb_value <= RgbColor._MAX_COLOR_VALUE:
                    valid_values.append(rgb_value)
            return len(valid_values) == len(value) and len(value) <= 3
        return False

    @property
    def value(self):
        """RGB value, as string."""
        return self._value

    @property
    def r(self):
        """Red value, in hexadecimal."""
        return self._r

    @property
    def g(self):
        """Green value, in hexadecimal."""
        return self._g

    @property
    def b(self):
        """Blue value, in hexadecimal."""
        return self._b

    def _parse(self, value):
        if isinstance(value, str) and len(value) == RgbColor._MIN_HEX_LENGTH:
            self._r = int(value[1], 16)
            self._g = int(value[2], 16)
            self._b = int(value[3], 16)
            self._value = value
        elif isinstance(value, str) and len(value) == RgbColor._MAX_HEX_LENGTH:
            self._r = int(value[1:3], 16)
            self._g = int(value[3:5], 16)
            self._b = int(value[5:7], 16)
            self._value = value

    def __repr__(self):
        return 'RgbColor(r={}, g={}, b={})'.format(self.r, self.g, self.b)


class ColorShade:
    """
    This class represents one of the colors in the color palette of the
    launchpad. There are 128 valid color shades, ranging from ID 0 to 127.
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

    @staticmethod
    def is_valid_id(value):
        """
        Returns `True` if `value` is a valid color ID,
        otherwise returns `False`.
        """
        return (True
                if value >= ColorShade.MIN_COLOR_ID
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

    def __repr__(self):
        return ('ColorShade(group={}, id={})'
                .format(self.color_group, self.color_id))


class ColorPalette:
    """
    Color palette of launchpad.
    """
    class Red:
        SHADE_1 = ColorShade(0x05, 'red')
        SHADE_2 = ColorShade(0x06, 'red')
        SHADE_3 = ColorShade(0x07, 'red')
        SHADE_4 = ColorShade(0x0b, 'red')
        SHADE_5 = ColorShade(0x48, 'red')
        SHADE_6 = ColorShade(0x53, 'red')
        SHADE_7 = ColorShade(0x6a, 'red')
        SHADE_8 = ColorShade(0x6b, 'red')
        SHADE_9 = ColorShade(0x78, 'red')
        SHADE_10 = ColorShade(0x79, 'red')
        SHADE_11 = ColorShade(0x7f, 'red')

    class Orange:
        SHADE_1 = ColorShade(0x0a, 'orange')
        SHADE_2 = ColorShade(0x09, 'orange')
        SHADE_3 = ColorShade(0x3c, 'orange')
        SHADE_4 = ColorShade(0x54, 'orange')
        SHADE_5 = ColorShade(0x60, 'orange')
        SHADE_6 = ColorShade(0x6c, 'orange')
        SHADE_7 = ColorShade(0x7e, 'orange')

    class Yellow:
        SHADE_1 = ColorShade(0x08, 'yellow')
        SHADE_2 = ColorShade(0x0c, 'yellow')
        SHADE_3 = ColorShade(0x0d, 'yellow')
        SHADE_4 = ColorShade(0x0e, 'yellow')
        SHADE_5 = ColorShade(0x0f, 'yellow')
        SHADE_6 = ColorShade(0x3d, 'yellow')
        SHADE_7 = ColorShade(0x3e, 'yellow')
        SHADE_8 = ColorShade(0x49, 'yellow')
        SHADE_9 = ColorShade(0x49, 'yellow')
        SHADE_10 = ColorShade(0x4a, 'yellow')
        SHADE_11 = ColorShade(0x55, 'yellow')
        SHADE_12 = ColorShade(0x61, 'yellow')
        SHADE_13 = ColorShade(0x62, 'yellow')
        SHADE_14 = ColorShade(0x63, 'yellow')
        SHADE_15 = ColorShade(0x64, 'yellow')
        SHADE_16 = ColorShade(0x69, 'yellow')
        SHADE_17 = ColorShade(0x6d, 'yellow')
        SHADE_18 = ColorShade(0x71, 'yellow')
        SHADE_19 = ColorShade(0x7c, 'yellow')
        SHADE_20 = ColorShade(0x7d, 'yellow')

    class Blue:
        SHADE_1 = ColorShade(0x1d, 'blue')
        SHADE_2 = ColorShade(0x20, 'blue')
        SHADE_3 = ColorShade(0x21, 'blue')
        SHADE_4 = ColorShade(0x22, 'blue')
        SHADE_5 = ColorShade(0x24, 'blue')
        SHADE_6 = ColorShade(0x25, 'blue')
        SHADE_7 = ColorShade(0x26, 'blue')
        SHADE_8 = ColorShade(0x27, 'blue')
        SHADE_9 = ColorShade(0x28, 'blue')
        SHADE_10 = ColorShade(0x29, 'blue')
        SHADE_11 = ColorShade(0x2a, 'blue')
        SHADE_12 = ColorShade(0x2b, 'blue')
        SHADE_13 = ColorShade(0x41, 'blue')
        SHADE_14 = ColorShade(0x4d, 'blue')
        SHADE_15 = ColorShade(0x4e, 'blue')
        SHADE_16 = ColorShade(0x4f, 'blue')
        SHADE_17 = ColorShade(0x5a, 'blue')
        SHADE_18 = ColorShade(0x5b, 'blue')
        SHADE_19 = ColorShade(0x68, 'blue')

    class Green:
        SHADE_1 = ColorShade(0x10, 'green')
        SHADE_2 = ColorShade(0x11, 'green')
        SHADE_3 = ColorShade(0x12, 'green')
        SHADE_4 = ColorShade(0x13, 'green')
        SHADE_5 = ColorShade(0x14, 'green')
        SHADE_6 = ColorShade(0x15, 'green')
        SHADE_7 = ColorShade(0x16, 'green')
        SHADE_8 = ColorShade(0x17, 'green')
        SHADE_9 = ColorShade(0x18, 'green')
        SHADE_10 = ColorShade(0x19, 'green')
        SHADE_11 = ColorShade(0x1a, 'green')
        SHADE_12 = ColorShade(0x1b, 'green')
        SHADE_13 = ColorShade(0x1c, 'green')
        SHADE_14 = ColorShade(0x1e, 'green')
        SHADE_15 = ColorShade(0x1f, 'green')
        SHADE_16 = ColorShade(0x23, 'green')
        SHADE_17 = ColorShade(0x3f, 'green')
        SHADE_18 = ColorShade(0x40, 'green')
        SHADE_19 = ColorShade(0x41, 'green')
        SHADE_20 = ColorShade(0x44, 'green')
        SHADE_21 = ColorShade(0x4c, 'green')
        SHADE_22 = ColorShade(0x56, 'green')
        SHADE_23 = ColorShade(0x57, 'green')
        SHADE_24 = ColorShade(0x58, 'green')
        SHADE_25 = ColorShade(0x59, 'green')
        SHADE_26 = ColorShade(0x65, 'green')
        SHADE_27 = ColorShade(0x66, 'green')
        SHADE_28 = ColorShade(0x6e, 'green')
        SHADE_29 = ColorShade(0x6f, 'green')
        SHADE_30 = ColorShade(0x72, 'green')
        SHADE_31 = ColorShade(0x7a, 'green')
        SHADE_32 = ColorShade(0x7b, 'green')

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
        SHADE_27 = ColorShade(0x67, 'violet')
        SHADE_28 = ColorShade(0x70, 'violet')
        SHADE_29 = ColorShade(0x73, 'violet')
        SHADE_30 = ColorShade(0x74, 'violet')

    class White:
        SHADE_1 = ColorShade(0x04, 'white')
        SHADE_2 = ColorShade(0x77, 'white')

    class Gray:
        SHADE_1 = ColorShade(0x01, 'gray')
        SHADE_2 = ColorShade(0x02, 'gray')
        SHADE_3 = ColorShade(0x03, 'gray')
        SHADE_4 = ColorShade(0x75, 'gray')
        SHADE_5 = ColorShade(0x76, 'gray')


class ColorShadeStore:
    """
    This class represents a collection of all color shades
    available to launchpad.
    """
    COLOR_GROUPS = ['red', 'orange', 'yellow', 'green',
                    'blue', 'violet', 'white', 'gray']
    COLOR_GROUP_SYMBOLS = ['r', 'o', 'y', 'g',
                           'b', 'v', 'w', 'z']

    def __init__(self):
        assert len(ColorShadeStore.COLOR_GROUPS) == \
                len(ColorShadeStore.COLOR_GROUP_SYMBOLS), \
                "len(COLOR_GROUPS) != len(COLOR_GROUP_SYMBOLS)"

    def find(self, value):
        """
        Searches for color shade `value` and returns the
        `ColorShade` if found, otherwise returns `None`.
        """
        return self._find_shade(*self._parse(value))

    def _find_shade(self, color, color_shade_id):
        if not color:
            raise RuntimeError('Expected color string, got "{}".'
                               .format(color))

        color_shade = None
        color_group = ColorPalette.__dict__[color.capitalize()]
        if color_shade_id:
            shade_clause = 'SHADE_{}'.format(color_shade_id)
            if shade_clause in color_group.__dict__:
                color_shade = color_group.__dict__[shade_clause]
        else:
            color_shade = color_group.__dict__.items()[-1]

        return color_shade

    def contains(self, value):
        """
        Searches for color shade `value` and returns `True` if
        the color shade exists, otherwise returns `False`.
        """
        color, _ = self._parse(value)
        return True if color else False

    def _color_from_symbol(self, symbol):
        return ColorShadeStore.COLOR_GROUPS[ColorShadeStore.COLOR_GROUP_SYMBOLS.index(symbol)]  # noqa

    # Valid input: red, o, y2, green3
    def _parse(self, value):
        color = None
        color_shade_id = None

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
