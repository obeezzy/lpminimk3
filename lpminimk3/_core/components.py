"""
Software representation of physical components for Launchpad Mini MK3.
"""

import math
import re
from abc import ABC
from ..colors._colors import ColorShade, ColorShadeStore, RgbColor
from ..midi_messages import Colorspec,\
                            ColorspecFragment,\
                            Constants,\
                            Lighting
from ..match import ButtonMatch
from .utils import ButtonEvent
from ..region import Region


class Matrix(ABC):
    """
    A matrix of pad buttons/LEDs on the surface of the Launchpad.
    """
    @property
    def launchpad(self):
        pass

    @property
    def width(self):
        return -1

    @property
    def height(self):
        return -1

    @property
    def max_x(self):
        return -1

    @property
    def max_y(self):
        return -1

    def led_range(self):
        pass

    def render(self, renderable):
        renderable.render(self)


class FlipAxis:
    X = 'x'
    Y = 'y'
    XY = 'xy'


class _MatrixTransform:
    def __init__(self, matrix, layout, led_mode):
        self._matrix = matrix
        self._layout = layout
        self._led_mode = led_mode

    def rotated_led_range(self, angle, *, flip_axis=''):
        assert angle, 'Angle cannot be zero.'
        angle = self._normalize_angle(angle)
        angle = self._flip_angle(angle)
        angle_rad = math.radians(angle)
        for led in self._matrix.led_range(layout=self._layout,
                                          mode=self._led_mode):
            rotated_x = round((led.y * math.sin(angle_rad)) + (led.x * math.cos(angle_rad)))  # noqa
            rotated_y = round((led.y * math.cos(angle_rad)) - (led.x * math.sin(angle_rad)))  # noqa
            if angle == 90:
                rotated_y = min(self._matrix.max_y + rotated_y, self._matrix.max_y)  # noqa
            elif angle == 180:
                rotated_y = min(self._matrix.max_y + rotated_y, self._matrix.max_y)  # noqa
                rotated_x = min(self._matrix.max_x + rotated_x, self._matrix.max_x)  # noqa
            elif angle == 270:
                rotated_x = min(self._matrix.max_x + rotated_x, self._matrix.max_x)  # noqa
            if flip_axis:
                flipped_x = (self._flip_axis(rotated_x)
                             if FlipAxis.X in flip_axis
                             else rotated_x)
                flipped_y = (self._flip_axis(rotated_y)
                             if FlipAxis.Y in flip_axis
                             else rotated_y)
                yield self._matrix.led(x=flipped_x,
                                       y=flipped_y,
                                       layout=self._layout,
                                       mode=self._led_mode)
            else:
                yield self._matrix.led(x=rotated_x,
                                       y=rotated_y,
                                       layout=self._layout,
                                       mode=self._led_mode)

    def flipped_led_range(self, axis):
        for led in self._matrix.led_range(layout=self._layout,
                                          mode=self._led_mode):
            flipped_x = (self._flip_axis(led.x)
                         if FlipAxis.X in axis
                         else led.x)
            flipped_y = (self._flip_axis(led.y)
                         if FlipAxis.Y in axis
                         else led.y)
            yield self._matrix.led(x=flipped_x,
                                   y=flipped_y,
                                   layout=self._layout,
                                   mode=self._led_mode)

    def _flip_axis(self, value):
        max_value = self._matrix.width - 1
        return max_value - value

    def _flip_angle(self, angle):
        if angle == -90 or angle == 270:
            return 90
        elif angle == -180:
            return 180
        elif angle == 90 or angle == -270:
            return 270
        return angle

    def _normalize_angle(self, angle):
        if angle and (angle % 90) == 0 and abs(angle) > 270:
            return angle % 360
        assert (round(abs(angle)) in (0, 90, 180, 270)), \
               'Angle must be a multiple of 90.'
        return angle


class _MatrixCoordinate:
    def __init__(self, launchpad, layout, button_names, *,
                 name='',
                 coordinate_id=-1,
                 x=-1, y=-1):
        x, y = (self._determine_coordinate_from_name(name,
                                                     button_names)
                if x < 0 and y < 0 and len(name) > 0
                else (x, y))
        matrix_width, matrix_height = self._determine_bounds(button_names)

        x, y = (self._determine_coordinate_from_id(coordinate_id,
                                                   bounds=(matrix_width, matrix_height))  # noqa
                if coordinate_id >= 0 and x < 0 and y < 0
                else (x, y))
        name = self._determine_name_from_coordinate(x, y,
                                                    button_names,
                                                    bounds=(matrix_width, matrix_height))  # noqa
        midi_value = self._determine_midi_value(x, y,
                                                layout,
                                                bounds=(matrix_width, matrix_height))  # noqa
        self._x = x
        self._y = y
        self._id = coordinate_id
        self._matrix_width = matrix_width
        self._matrix_height = matrix_height
        self._name = name
        self._midi_value = midi_value

    def __repr__(self):
        return ('LayoutCoordinate('
                f'name={self.name}, '
                f'x={self.x}, '
                f'y={self.y}, '
                f'id={self.id})')

    @property
    def id(self):
        within_range = (self._x >= 0
                        and self._y >= 0
                        and self._x < self._matrix_width
                        and self._y < self._matrix_height)
        if not within_range:
            return -1
        return (self._y * self._matrix_height) + self._x + 1

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def midi_value(self):
        return self._midi_value

    @property
    def matrix_width(self):
        return self._matrix_width

    @property
    def matrix_height(self):
        return self._matrix_height

    def _determine_coordinate_from_id(self, led_id, bounds):
        width, height = bounds
        x = int(led_id % width)
        y = int(led_id / height)
        return x, y

    def _determine_coordinate_from_name(self, name, button_names):
        found = False
        x = y = -1
        for column, button_column in enumerate(button_names):
            for row, button_name in enumerate(button_column):
                if button_name == name.lower():
                    x = row
                    y = column
                    found = True
                    break
                elif (name.lower() in button_name
                        and name.lower()
                        in ButtonFace.STOP_SOLO_MUTE.split('_')):
                    x = row
                    y = column
                    found = True
                    break
            if found:
                break
        if x < 0 or y < 0:
            raise ValueError('Invalid name set.')

        return x, y

    def _determine_midi_value(self, x, y, layout, bounds):
        width, height = bounds
        within_range = (x >= 0
                        and y >= 0
                        and x < width
                        and y < height)
        if not within_range:
            raise ValueError('Led(x,y) out of range: '
                             f'value({x},{y}), '
                             f'range((0,{width}),(0,{height}))')
        return layout[y][x]

    def _determine_name_from_coordinate(self, x, y, button_names, bounds):
        matrix_width, matrix_height = bounds
        within_range = (x >= 0
                        and y >= 0
                        and x < matrix_width
                        and y < matrix_height)
        if not within_range:
            raise ValueError('Led(x,y) out of range: '
                             f'value({x},{y}), '
                             f'range((0,{matrix_width}),(0,{matrix_height}))')
        return button_names[y][x]

    def _determine_bounds(self, button_names):
        assert len(button_names) > 0
        matrix_width = len(button_names[0])
        matrix_height = len(button_names)
        return matrix_width, matrix_height


class _LedColor:
    def __init__(self,
                 value=None, *,
                 lighting_mode,
                 midi_value,
                 lighting_type=Constants.LightingType.STATIC):
        self._value = value
        self._message = None
        self._lighting_mode = lighting_mode
        self._lighting_type = lighting_type
        self._midi_value = midi_value

        assert isinstance(lighting_mode, int)
        assert isinstance(lighting_type, int)

        if not value:
            self._message = self._create_reset_message(lighting_mode,
                                                       midi_value)
        elif (not isinstance(value, ColorShade)
                and not isinstance(value, str)
                and not isinstance(value, int)
                and not isinstance(value, (tuple, list))):
            raise TypeError('Must be of type ColorShade or str '
                            'or int or tuple or list.')
        elif ((isinstance(value, str)
                and not ColorShadeStore().contains(value)
                and not RgbColor.is_valid(value))
                or (isinstance(value, (tuple, list))
                    and not RgbColor.is_valid(value))):
            raise ValueError('Invalid color.')
        elif RgbColor.is_valid(value):
            colorspec = self._create_colorspec_message(value,
                                                       lighting_type,
                                                       midi_value)
            self._message = colorspec
        else:
            lighting = self._create_lighting_message(value,
                                                     lighting_mode,
                                                     midi_value)
            self._message = lighting

    @property
    def message(self):
        return self._message

    def _create_colorspec_message(self, value, lighting_type, midi_value):
        rgb_color = RgbColor(value)
        colorspec = Colorspec(ColorspecFragment(lighting_type,
                                                midi_value,
                                                rgb_color.r,
                                                rgb_color.g,
                                                rgb_color.b))
        return colorspec

    def _create_lighting_message(self, value, lighting_mode, midi_value):
        color_id = value if ColorShade.is_valid_id(value) else -1
        lighting = None
        if color_id < 0:
            color_shade = ColorShadeStore().find(value)
            color_id = (color_shade.color_id
                        if color_shade
                        else color_id)
        if color_id < 0:
            raise ValueError(f'Color ID values must be between '
                             f'{ColorShade.MIN_COLOR_ID} and '
                             f'{ColorShade.MAX_COLOR_ID}.')
        else:
            lighting = Lighting(lighting_mode,
                                midi_value,
                                color_id)
        return lighting

    def _create_reset_message(self, lighting_mode, midi_value):
        lighting = Lighting(lighting_mode,
                            midi_value,
                            0x0)
        return lighting


class ButtonFace:
    """
    A button face.

    A button face is the marking placed on the top of
    some Launchpad buttons.
    """
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    SESSION = 'session'
    DRUMS = 'drums'
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


class ButtonGroup:
    """
    A group of buttons.
    """

    def __init__(self, launchpad,
                 layout,
                 button_names,
                 args):
        self._launchpad = launchpad
        self._layout = layout
        self._button_names = button_names
        self._buttons = self._create_buttons(launchpad,
                                             layout,
                                             button_names,
                                             args)

    def __iter__(self):
        return iter(self._buttons)

    def __repr__(self):
        names = list(map(lambda name: f"'{name}'", self.names))
        return f'ButtonGroup({names})'

    @property
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @property
    def names(self):
        """
        Names of buttons in group.
        """
        return [button.name for button in self._buttons]

    def poll_for_event(self, *, interface='midi', timeout=None,
                       type=ButtonEvent.PRESS_RELEASE):
        """
        Polls for MIDI events of buttons specified
        in this group. If `timeout` is `None`, this function will
        wait indefinitely until a :class:`ButtonEvent` is
        received. If no event is received, `None` is returned.

        Keyword Args:
            interface (str): Interface to which to send message.
                (See :class:`Interface`.)
            timeout (float): Duration in seconds to wait for event to occur
            type (str): Event type.
                (Possible values: 'press', 'release', 'press|release')

        Returns:
            ButtonEvent: Button event (See :class:`ButtonEvent`).
        """
        if (not type
                or (type.lower().replace('|', '_') != ButtonEvent.PRESS_RELEASE  # noqa
                    and type.lower() != ButtonEvent.RELEASE
                    and type.lower() != ButtonEvent.PRESS)):
            raise ValueError('Not a valid event type.')

        midi_event = self._launchpad.poll_for_event(interface=interface,
                                                    timeout=timeout,
                                                    match=ButtonMatch(self._buttons,  # noqa
                                                                      type))  # noqa
        return (ButtonEvent(midi_event, self._buttons)
                if midi_event
                else None)

    def clear_event_queue(self, *, interface='midi'):
        """
        Clears event queue.

        Keyword Args:
            interface (str): Interface to clear.
                (See :class:`Interface`.)

        Raises:
            ValueError: If `interface` is invalid.
            RuntimeError: If device is closed.
        """
        self._launchpad.clear_event_queue()

    # FIXME: Too complex
    def _create_buttons(self, launchpad, layout, button_names, args):  # noqa
        buttons = []
        for arg in args:
            found = False
            for column, button_name_column in enumerate(button_names):
                if found:
                    break
                for row, button_name in enumerate(button_name_column):
                    if found:
                        break
                    elif arg and isinstance(arg, str):
                        if arg.lower() == button_name:
                            buttons.append(Button(launchpad,
                                                  layout,
                                                  button_names,
                                                  name=arg))
                            found = True
                    elif isinstance(arg, tuple):
                        if (len(arg) == 2
                                and arg[0] == row
                                and arg[1] == column):
                            buttons.append(Button(launchpad,
                                                  layout,
                                                  button_names,
                                                  x=row, y=column))
                            found = True
                    elif isinstance(arg, int):
                        buttons.append(Button(launchpad,
                                              layout,
                                              button_names,
                                              button_id=arg))
                        found = True
                    else:
                        raise ValueError(f'Invalid button "{str(arg)}".')
        return set(buttons)


class Led:
    """
    An LED on the Launchpad.
    """

    OFF = 'off'
    STATIC = 'static'
    FLASH = 'flash'
    PULSE = 'pulse'

    _LIGHTING_MODE = {
            'off': Constants.LightingMode.OFF,
            'static': Constants.LightingMode.STATIC,
            'flash': Constants.LightingMode.FLASH
    }
    _LIGHTING_TYPE = {
            'static': Constants.LightingType.STATIC,
            'flash': Constants.LightingType.FLASH,
            'pulse': Constants.LightingType.PULSE,
            'rgb': Constants.LightingType.RGB
    }

    def __init__(self, *, launchpad, button_names,
                 layout, x=-1, y=-1, name='', mode=STATIC):
        self._launchpad = launchpad
        self._button_names = button_names
        self._mode = mode
        self._x = self._y = -1

        name = (x if isinstance(x, str)
                and not name else name)
        if isinstance(x, str) and not name:
            raise ValueError('Invalid name.')
        x = -1 if isinstance(x, str) else x

        led_id = x if x >= 0 and y < 0 else -1
        x = -1 if isinstance(x, int) and led_id >= 0 else x

        coordinate = _MatrixCoordinate(launchpad=launchpad,
                                       layout=layout,
                                       button_names=button_names,
                                       name=name,
                                       coordinate_id=led_id,
                                       x=x, y=y)

        self._x = coordinate.x
        self._y = coordinate.y
        self._matrix_width = coordinate.matrix_width
        self._matrix_height = coordinate.matrix_height
        self._midi_value = coordinate.midi_value

    def __eq__(self, other):
        if not isinstance(other, Led):
            return False
        return (self.launchpad == other.launchpad
                and self.name == other.name)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return f"Led(x={self.x}, y={self.x}, name='{self.name}')"

    @property
    def id(self):
        """
        Unique ID of LED.
        """
        if not self._is_within_range():
            return -1
        return (self._y * self._matrix_height) + self._x + 1

    @property
    def x(self):
        """
        X position of LED.
        """
        return self._x

    @property
    def y(self):
        """
        Y position of LED.
        """
        return self._y

    @property
    def name(self):
        """
        Name of LED.
        """
        return (self._button_names[self.y][self.x]
                if self._is_within_range()
                else '')

    @property
    def midi_value(self):
        """
        Midi value of LED.
        """
        return self._midi_value

    @property
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @property
    def color(self):
        """
        Color. Retrieving the set color is not supported.
        """
        return None

    @color.setter
    def color(self, value):
        """
        Sets the color of the LED to `value`.

        Args:
            value (ColorShade or str or int): Color value.

        Raises:
            ValueError: When invalid value is used.
            TypeError: When invalid type is used.
        """
        message = _LedColor(value,
                            lighting_mode=self._LIGHTING_MODE[self._mode],
                            lighting_type=self._LIGHTING_TYPE['rgb'],
                            midi_value=self._midi_value).message
        self.launchpad.send_message(message)

    @color.deleter
    def color(self):
        """Turns LED off."""
        self.reset()

    def reset(self):
        """Turns LED off."""
        message = _LedColor(lighting_mode=self._LIGHTING_MODE[self._mode],
                            midi_value=self._midi_value).message
        self.launchpad.send_message(message)

    def _is_within_range(self):
        return (self._x >= 0
                and self._y >= 0
                and self._x < self._matrix_width
                and self._y < self._matrix_height)


class Button:
    """
    A button on the Launchpad.
    """

    def __init__(self, launchpad,
                 layout,
                 button_names, *,
                 x=-1, y=-1,
                 name='',
                 button_id=-1):
        coordinate = _MatrixCoordinate(launchpad=launchpad,
                                       layout=layout,
                                       button_names=button_names,
                                       name=name,
                                       coordinate_id=button_id,
                                       x=x, y=y)
        self._launchpad = launchpad
        self._layout = layout
        self._button_names = button_names
        self._name = coordinate.name
        self._x = coordinate.x
        self._y = coordinate.y
        self._button_id = coordinate.id
        self._midi_value = coordinate.midi_value

    def __eq__(self, other):
        if not isinstance(other, Button):
            return False
        return (self.launchpad == other.launchpad
                and self.name == other.name)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return ("Button("
                f"name='{self.name}', "
                f"x={self.x}, "
                f"y={self.y}, "
                f"id={self.id})")

    @property
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @property
    def x(self):
        """
        X position of button.
        """
        return self._x

    @property
    def y(self):
        """
        Y position of button.
        """
        return self._y

    @property
    def name(self):
        """
        Name of button.
        """
        return self._name

    @property
    def midi_value(self):
        """
        MIDI value of button.
        """
        return self._midi_value

    @property
    def id(self):
        """
        Unique ID of button.
        """
        return self._button_id

    @property
    def parent(self):
        """
        Parent of button, either 'grid' or 'panel'.
        """
        match = re.match('^\\d+x\\d+$', self._name)
        if match:
            return 'grid'
        return 'panel' if self._button_id else ''

    @property
    def led(self):
        """
        LED of button.
        """
        return Led(launchpad=self._launchpad,
                   layout=self._layout,
                   button_names=self._button_names,
                   x=self._x,
                   y=self._y)

    @property
    def layout(self):
        """
        Button layout.
        """
        return self._layout


class Panel(Matrix):
    """
    Panel of Launchpad.

    The panel represents the 9x9 matrix of pad buttons
    on the surface of the Launchpad.
    """
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
            [0x38, 0x39, 0x3a, 0x3b, 0x58, 0x59, 0x5a, 0x5b, 0x45],
            [0x34, 0x35, 0x36, 0x37, 0x54, 0x55, 0x56, 0x57, 0x3b],
            [0x30, 0x31, 0x32, 0x33, 0x50, 0x51, 0x52, 0x53, 0x31],
            [0x2c, 0x2d, 0x2e, 0x2f, 0x4c, 0x4d, 0x4e, 0x4f, 0x27],
            [0x28, 0x29, 0x2a, 0x2b, 0x48, 0x49, 0x4a, 0x4b, 0x1d],
            [0x24, 0x25, 0x26, 0x27, 0x44, 0x45, 0x46, 0x47, 0x13]
    ]

    _BUTTON_NAMES = [
            ['up', 'down', 'left', 'right', 'session', 'drums', 'keys', 'user', 'logo'],  # noqa
            ['0x0', '1x0', '2x0', '3x0', '4x0', '5x0', '6x0', '7x0', 'scene_launch_1'],  # noqa
            ['0x1', '1x1', '2x1', '3x1', '4x1', '5x1', '6x1', '7x1', 'scene_launch_2'],  # noqa
            ['0x2', '1x2', '2x2', '3x2', '4x2', '5x2', '6x2', '7x2', 'scene_launch_3'],  # noqa
            ['0x3', '1x3', '2x3', '3x3', '4x3', '5x3', '6x3', '7x3', 'scene_launch_4'],  # noqa
            ['0x4', '1x4', '2x4', '3x4', '4x4', '5x4', '6x4', '7x4', 'scene_launch_5'],  # noqa
            ['0x5', '1x5', '2x5', '3x5', '4x5', '5x5', '6x5', '7x5', 'scene_launch_6'],  # noqa
            ['0x6', '1x6', '2x6', '3x6', '4x6', '5x6', '6x6', '7x6', 'scene_launch_7'],  # noqa
            ['0x7', '1x7', '2x7', '3x7', '4x7', '5x7', '6x7', '7x7', 'stop_solo_mute']   # noqa
    ]

    def __init__(self, launchpad):
        self._launchpad = launchpad

    def __eq__(self, other):
        if not isinstance(other, Panel):
            return False
        return self.launchpad == other.launchpad

    def __repr__(self):
        return f'Panel({self.width}x{self.height})'

    @Matrix.launchpad.getter
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @Matrix.width.getter
    def width(self):
        """
        Max X.
        """
        return len(Panel._BUTTON_NAMES[0])

    @Matrix.height.getter
    def height(self):
        """
        Max Y.
        """
        return len(Panel._BUTTON_NAMES)

    @property
    def max_id(self):
        """
        Max ID.
        """
        return self.width * self.height

    @Matrix.max_x.getter
    def max_x(self):
        """
        Max X.
        """
        return (self.width - 1
                if self.width >= 0
                else -1)

    @Matrix.max_y.getter
    def max_y(self):
        """
        Max Y.
        """
        return (self.height - 1
                if self.height >= 0
                else -1)

    def led(self, x=-1, y=-1, *, name='', layout=PROG, mode=Led.STATIC):
        """
        Returns an LED.

        Args:
            x (int): X position of LED.
            y (int): Y position of LED.

        Keyword Args:
            name (str): Name of LED.
            layout (Layout): Layout of buttons.
            mode (str): Lighting mode.
        """
        return Led(launchpad=self._launchpad,
                   button_names=Panel._BUTTON_NAMES,
                   layout=(Panel._CUSTOM_MODE_MIDI_LAYOUT
                           if layout == Panel.CUSTOM
                           else Panel._PROG_MODE_MIDI_LAYOUT),
                   x=x, y=y,
                   name=name, mode=mode)

    # FIXME: Too complex
    def led_range(self, *,  # noqa
                  layout=PROG,
                  mode=Led.STATIC,
                  rotation=0,
                  flip_axis='',
                  region=None):
        """
        Returns an immutable sequence of LEDs.

        Keyword Args:
            layout (Layout): Layout of buttons.
            mode (str): Lighting mode.
            rotation (int): Rotation angle in degrees.
                (Possible values: 0, 90, 180, 270, -90)

        Yields:
            Led: Sequence of LEDs
        """
        if region and not isinstance(region, Region):
            raise TypeError("'region' must be of type 'Region'.")
        elif rotation and not isinstance(rotation, int):
            raise TypeError("'rotation' must be of type 'int'.")
        elif flip_axis and not isinstance(flip_axis, str):
            raise TypeError("'flip_axis' must be of type 'str'.")

        if region:
            for name in region.button_names:
                yield self.led(name=name, layout=layout, mode=mode)
        elif rotation:
            for led in _MatrixTransform(self, layout, mode).rotated_led_range(rotation,  # noqa
                                                                              flip_axis=flip_axis):  # noqa
                yield led
        elif not rotation and flip_axis:
            for led in _MatrixTransform(self, layout, mode).flipped_led_range(flip_axis):  # noqa
                yield led
        else:
            for led_id in range(self.max_id):
                yield self.led(led_id, layout=layout, mode=mode)

    def buttons(self, *args, layout=PROG):
        """
        Returns a :class:`ButtonGroup`.

        Args:
            args (list): Button names, button IDs
                or button XY-pairs

        Keyword Args:
            layout (Layout): Layout of buttons.
        """
        args = (args
                if len(args) > 0
                else [button_name
                      for button_row in Panel._BUTTON_NAMES
                      for button_name in button_row])
        return ButtonGroup(launchpad=self._launchpad,
                           layout=(Panel._CUSTOM_MODE_MIDI_LAYOUT
                                   if layout == Panel.CUSTOM
                                   else Panel._PROG_MODE_MIDI_LAYOUT),
                           button_names=Panel._BUTTON_NAMES,
                           args=list(args))


class Grid(Matrix):
    """
    Grid of Launchpad.

    The grid represents the 8x8 grid of white, faceless
    buttons of the Launchpad.
    """
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
            [0x38, 0x39, 0x3a, 0x3b, 0x58, 0x59, 0x5a, 0x5b],
            [0x34, 0x35, 0x36, 0x37, 0x54, 0x55, 0x56, 0x57],
            [0x30, 0x31, 0x32, 0x33, 0x50, 0x51, 0x52, 0x53],
            [0x2c, 0x2d, 0x2e, 0x2f, 0x4c, 0x4d, 0x4e, 0x4f],
            [0x28, 0x29, 0x2a, 0x2b, 0x48, 0x49, 0x4a, 0x4b],
            [0x24, 0x25, 0x26, 0x27, 0x44, 0x45, 0x46, 0x47]
    ]
    _BUTTON_NAMES = [
            ['0x0', '1x0', '2x0', '3x0', '4x0', '5x0', '6x0', '7x0'],
            ['0x1', '1x1', '2x1', '3x1', '4x1', '5x1', '6x1', '7x1'],
            ['0x2', '1x2', '2x2', '3x2', '4x2', '5x2', '6x2', '7x2'],
            ['0x3', '1x3', '2x3', '3x3', '4x3', '5x3', '6x3', '7x3'],
            ['0x4', '1x4', '2x4', '3x4', '4x4', '5x4', '6x4', '7x4'],
            ['0x5', '1x5', '2x5', '3x5', '4x5', '5x5', '6x5', '7x5'],
            ['0x6', '1x6', '2x6', '3x6', '4x6', '5x6', '6x6', '7x6'],
            ['0x7', '1x7', '2x7', '3x7', '4x7', '5x7', '6x7', '7x7']
    ]

    def __init__(self, launchpad):
        self._launchpad = launchpad

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return self.launchpad == other.launchpad

    def __repr__(self):
        return f'Grid({self.width}x{self.height})'

    @Matrix.launchpad.getter
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @Matrix.width.getter
    def width(self):
        """
        Max X.
        """
        return len(Grid._BUTTON_NAMES[0])

    @Matrix.height.getter
    def height(self):
        """
        Max Y.
        """
        return len(Grid._BUTTON_NAMES)

    @property
    def max_id(self):
        """
        Max ID.
        """
        return self.width * self.height

    @Matrix.max_x.getter
    def max_x(self):
        """
        Max X.
        """
        return (self.width - 1
                if self.width >= 0
                else -1)

    @Matrix.max_y.getter
    def max_y(self):
        """
        Max Y.
        """
        return (self.height - 1
                if self.height >= 0
                else -1)

    def led(self, x=-1, y=-1, *, name='', layout=PROG, mode=Led.STATIC):
        """
        Returns an LED.

        Args:
            x (int): X position of LED.
            y (int): Y position of LED.

        Keyword Args:
            name (str): Name of LED.
            layout (Layout): Layout of buttons.
            mode (str): Lighting mode.
        """
        return Led(launchpad=self._launchpad,
                   button_names=Grid._BUTTON_NAMES,
                   layout=(Grid._CUSTOM_MODE_MIDI_LAYOUT
                           if layout == Grid.CUSTOM
                           else Grid._PROG_MODE_MIDI_LAYOUT),
                   x=x, y=y,
                   name=name, mode=mode)

    # FIXME: Too complex
    def led_range(self, *,  # noqa
                  layout=PROG,
                  mode=Led.STATIC,
                  rotation=0,
                  flip_axis='',
                  region=None):
        """
        Returns an immutable sequence of LEDs.

        Keyword Args:
            layout (Layout): Layout of buttons.
            mode (str): Lighting mode.
            rotation (int): Rotation angle in degrees.
                (Possible values: 0, 90, 180, 270, -90)

        Yields:
            Led: Sequence of LEDs
        """
        if region and not isinstance(region, Region):
            raise TypeError("'region' must be of type 'Region'.")
        elif rotation and not isinstance(rotation, int):
            raise TypeError("'rotation' must be of type 'int'.")
        elif flip_axis and not isinstance(flip_axis, str):
            raise TypeError("'flip_axis' must be of type 'str'.")

        if region:
            for name in region.button_names:
                yield self.led(name=name, layout=layout, mode=mode)
        elif rotation:
            for led in _MatrixTransform(self, layout, mode).rotated_led_range(rotation,  # noqa
                                                                              flip_axis=flip_axis):  # noqa
                yield led
        elif not rotation and flip_axis:
            for led in _MatrixTransform(self, layout, mode).flipped_led_range(flip_axis):  # noqa
                yield led
        else:
            for led_id in range(self.max_id):
                yield self.led(led_id, layout=layout, mode=mode)

    def buttons(self, *args, layout=PROG):
        """
        Returns a :class:`ButtonGroup`.

        Args:
            args (list): Button names, button IDs
                or button XY-pairs

        Keyword Args:
            layout (Layout): Layout of buttons.
        """
        args = (args
                if len(args) > 0
                else [button_name
                      for button_row in Grid._BUTTON_NAMES
                      for button_name in button_row])
        return ButtonGroup(launchpad=self._launchpad,
                           layout=(Grid._CUSTOM_MODE_MIDI_LAYOUT
                                   if layout == Grid.CUSTOM
                                   else Grid._PROG_MODE_MIDI_LAYOUT),
                           button_names=Grid._BUTTON_NAMES,
                           args=list(args))
