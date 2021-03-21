from ._utils import Interface
from .colors import ColorShade, ColorShadeStore, RgbColor

class Animable:
    def animate(self, animation, *, timeout=0):
        pass

class ButtonFace:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    SESSION = 'session'
    DRUM = 'drum'
    KEYS = 'keys'
    USER = 'user'
    LOGO = 'logo'
    SCENE_LAUNCH_1 = 'scene_launch_1'
    SCENE_LAUNCH_2 = 'scene_launch_2'
    SCENE_LAUNCH_3 = 'scene_launch_3'
    SCENE_LAUNCH_4 = 'scene_launch_4'
    SCENE_LAUNCH_5 = 'scene_launch_5'
    SCENE_LAUNCH_6 = 'scene_launch_6'
    SCENE_LAUNCH_7 = 'scene_launch_7'
    STOP_SOLO_MUTE = 'stop_solo_mute'

class Led:
    OFF = 'off'
    STATIC = 'static'
    FLASH = 'flash'
    PULSE = 'pulse'

    _LIGHTING_MODE = {
            'off': 0x80,
            'static': 0x90,
            'flash': 0x91,
            'pulse': 0x92
    }
    _LIGHTING_TYPE = {
            'static': 0x00,
            'flash': 0x01,
            'pulse': 0x02,
            'rgb': 0x03
    }

    def __init__(self, *, launchpad, button_names, layout, x=-1, y=-1, name='', mode=STATIC):
        self._launchpad = launchpad
        self._button_names = button_names
        name = x if isinstance(x, str) and name == '' else name
        x = -1 if isinstance(x, str) else x
        self._x = x
        self._y = y
        self._mode = mode
        self._max_x = -1
        self._max_y = -1
        self._note_number = -1
        self._initialize(name, layout) # FIXME: Order of function calls matter

    def _initialize(self, name, layout): # FIXME: Order of function calls matter
        self._determine_bounds()
        if self._x < 0 and self._y < 0:
            self._determine_coordinates(name)
        self._determine_note_number(layout)

    def _determine_coordinates(self, name):
        found = False
        for row, button_row in enumerate(self._button_names):
            for column, button_name in enumerate(button_row):
                if button_name == name.lower():
                    self._x = row
                    self._y = column
                    found = True
                    break
                elif name.lower() in button_name \
                        and name.lower() in ButtonFace.STOP_SOLO_MUTE.split('_'):
                    self._x = row
                    self._y = column
                    found = True
                    break
            if found:
                break
        if self._x < 0 or self._y < 0:
            raise RuntimeError('Invalid name set.')

    def _determine_note_number(self, layout):
        if not self._is_within_range():
            raise RuntimeError('LED out of range.')
        self._note_number = layout[self._x][self._y]

    def _determine_bounds(self):
        if len(self._button_names) > 0:
            self._max_x = len(self._button_names[0])
            self._max_y = len(self._button_names)
        else:
            raise RuntimeError('No button names passed in.')

    @property
    def id(self):
        if not self._is_within_range():
            return -1
        return (self._y * (self._max_y + 1)) + self._x + 1

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def name(self):
        return self._button_names[self.x][self.y] \
                if self._is_within_range() \
                else ''

    @property
    def launchpad(self):
        return self._launchpad

    @property
    def color(self):
        return None

    @color.setter
    def color(self, value):
        if not value or value == '':
            self.reset()
        elif not isinstance(value, ColorShade) and not isinstance(value, str) \
                and not isinstance(value, int):
            raise TypeError('Must be of type ColorShade or str or int.')
        elif ((isinstance(value, str)
                and not ColorShadeStore().contains(value)
                and not RgbColor.is_valid(value))
                or ((isinstance(value, tuple) or isinstance(value, list))
                        and not RgbColor.is_valid(value))):
            raise RuntimeError('Invalid color.')
        elif RgbColor.is_valid(value):
            rgb_color = RgbColor(value)
            message = self._colorspec_message(self._LIGHTING_TYPES['rgb'], self._note_number, rgb_color.r, rgb_color.g, rgb_color.b)
            self.launchpad.send_message(message)
        else:
            color_id = ColorShadeStore().find(value).color_id \
                    if not isinstance(value, int) \
                    else value
            color_id = value if ColorShade.is_valid_id(value) else None
            if not color_id:
                raise RuntimeError('Color ID values must be between 0 and 127.')
            else:
                self.launchpad.send_message([self._LIGHTING_MODE[self._mode], self._note_number, color_id])

    def reset(self):
        self.launchpad.send_message([self._LIGHTING_MODE[Led.OFF], self._note_number, 0x0])

    def _colorspec_message(self, lighting_type, led_index, *lighting_data):
        return [0xf0, 0x00,0x20, 0x29, 0x02, 0x0d, 0x03, lighting_type, led_index] + list(lighting_data) + [0xf7]

    def _is_within_range(self):
        return self._x >= 0 \
                and self._y >= 0 \
                and self._x <= self._max_x \
                and self._y <= self._max_y

    def __repr__(self):
        return 'Led(x={}, y={})'.format(self.x, self.y)

class Panel(Animable):
    PROG = 'prog'
    CUSTOM = 'custom'
    _PROG_MODE_MIDI_LAYOUT = [
            [0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x61, 0x62, 0x63],
            [0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59],
            [0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f],
            [0x3d, 0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45],
            [0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b],
            [0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31],
            [0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27],
            [0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d],
            [0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13]
    ]
    _CUSTOM_MODE_MIDI_LAYOUT = [
            [0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x61, 0x62, 0x63],
            [0x40, 0x41, 0x42, 0x43, 0x60, 0x61, 0x62, 0x63, 0x59],
            [0x3c, 0x3d, 0x3e, 0x3f, 0x5c, 0x5d, 0x5e, 0x5f, 0x4f],
            [0x38, 0x39, 0x3a, 0x3b, 0x58, 0x59, 0x60, 0x5b, 0x45],
            [0x34, 0x35, 0x36, 0x37, 0x54, 0x55, 0x56, 0x57, 0x3b],
            [0x30, 0x31, 0x32, 0x33, 0x50, 0x51, 0x52, 0x53, 0x31],
            [0x2c, 0x2d, 0x2e, 0x2f, 0x4c, 0x4d, 0x4e, 0x4f, 0x27],
            [0x28, 0x29, 0x2a, 0x2b, 0x48, 0x49, 0x4a, 0x4b, 0x1d],
            [0x24, 0x25, 0x26, 0x27, 0x44, 0x45, 0x46, 0x47, 0x13]
    ]
    _BUTTON_NAMES = [
            ['up', 'down', 'left', 'right', 'session', 'drums', 'keys', 'user', 'logo'],
            ['0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7', 'scene_launch_1'],
            ['1x0', '1x1', '1x2', '1x3', '1x4', '1x5', '1x6', '1x7', 'scene_launch_2'],
            ['2x0', '2x1', '2x2', '2x3', '2x4', '2x5', '2x6', '2x7', 'scene_launch_3'],
            ['3x0', '3x1', '3x2', '3x3', '3x4', '3x5', '3x6', '3x7', 'scene_launch_4'],
            ['4x0', '4x1', '4x2', '4x3', '4x4', '4x5', '4x6', '4x7', 'scene_launch_5'],
            ['5x0', '5x1', '5x2', '5x3', '5x4', '5x5', '5x6', '5x7', 'scene_launch_6'],
            ['6x0', '6x1', '6x2', '6x3', '6x4', '6x5', '6x6', '6x7', 'scene_launch_7'],
            ['7x0', '7x1', '7x2', '7x3', '7x4', '7x5', '7x6', '7x7', 'stop_solo_mute']
    ]

    def __init__(self, launchpad):
        self._launchpad = launchpad

    @property
    def launchpad(self):
        return self._launchpad

    @property
    def max_x(self):
        return len(Panel._BUTTON_NAMES[0])

    @property
    def max_y(self):
        return len(Panel._BUTTON_NAMES)

    def led(self, x=-1, y=-1, *, name='', layout=PROG, mode=Led.STATIC):
        if layout == Panel.CUSTOM:
            return Led(launchpad=self._launchpad, button_names=Panel._BUTTON_NAMES, layout=Panel._CUSTOM_MODE_MIDI_LAYOUT, x=x, y=y, name=name, mode=mode)
        return Led(launchpad=self._launchpad, button_names=Panel._BUTTON_NAMES, layout=Panel._PROG_MODE_MIDI_LAYOUT, x=x, y=y, name=name, mode=mode)

    def __repr__(self):
        return 'Panel({}x{})'.format(self.max_x, self.max_y)

class Grid(Animable):
    PROG = 'prog'
    CUSTOM = 'custom'
    _PROG_MODE_MIDI_LAYOUT = [
            [0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58],
            [0x47, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e],
            [0x3d, 0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44],
            [0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a],
            [0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30],
            [0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26],
            [0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c],
            [0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12]
    ]
    _CUSTOM_MODE_MIDI_LAYOUT = [
            [0x40, 0x41, 0x42, 0x43, 0x60, 0x61, 0x62, 0x63],
            [0x3c, 0x3d, 0x3e, 0x3f, 0x5c, 0x5d, 0x5e, 0x5f],
            [0x38, 0x39, 0x3a, 0x3b, 0x58, 0x59, 0x60, 0x5b],
            [0x34, 0x35, 0x36, 0x37, 0x54, 0x55, 0x56, 0x57],
            [0x30, 0x31, 0x32, 0x33, 0x50, 0x51, 0x52, 0x53],
            [0x2c, 0x2d, 0x2e, 0x2f, 0x4c, 0x4d, 0x4e, 0x4f],
            [0x28, 0x29, 0x2a, 0x2b, 0x48, 0x49, 0x4a, 0x4b],
            [0x24, 0x25, 0x26, 0x27, 0x44, 0x45, 0x46, 0x47]
    ]
    _BUTTON_NAMES = [
            ['0x0', '0x1', '0x2', '0x3', '0x4', '0x5', '0x6', '0x7'],
            ['1x0', '1x1', '1x2', '1x3', '1x4', '1x5', '1x6', '1x7'],
            ['2x0', '2x1', '2x2', '2x3', '2x4', '2x5', '2x6', '2x7'],
            ['3x0', '3x1', '3x2', '3x3', '3x4', '3x5', '3x6', '3x7'],
            ['4x0', '4x1', '4x2', '4x3', '4x4', '4x5', '4x6', '4x7'],
            ['5x0', '5x1', '5x2', '5x3', '5x4', '5x5', '5x6', '5x7'],
            ['6x0', '6x1', '6x2', '6x3', '6x4', '6x5', '6x6', '6x7'],
            ['7x0', '7x1', '7x2', '7x3', '7x4', '7x5', '7x6', '7x7']
    ]

    def __init__(self, launchpad):
        self._launchpad = launchpad

    @property
    def launchpad(self):
        return self._launchpad

    @property
    def max_x(self):
        return len(Grid._BUTTON_NAMES[0])

    @property
    def max_y(self):
        return len(Grid._BUTTON_NAMES)

    def led(self, x=-1, y=-1, *, name='', layout=PROG, mode=Led.STATIC):
        if layout == Grid.CUSTOM:
            return Led(launchpad=self._launchpad, button_names=Grid._BUTTON_NAMES, layout=Grid._CUSTOM_MODE_MIDI_LAYOUT, x=x, y=y, name=name, mode=mode)
        return Led(launchpad=self._launchpad, button_names=Grid._BUTTON_NAMES, layout=Grid._PROG_MODE_MIDI_LAYOUT, x=x, y=y, name=name, mode=mode)

    def __repr__(self):
        return 'Grid({}x{})'.format(self.max_x, self.max_y)
