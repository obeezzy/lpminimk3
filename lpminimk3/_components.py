"""
Software representation of physical components for Launchpad Mini MK3.
"""

import re
from .colors import ColorShade, ColorShadeStore, RgbColor
from .midi_messages import SysExMessages
from .match import ButtonMatch
from ._utils import ButtonEvent


class Animable:
    @property
    def max_x(self):
        return -1

    @property
    def max_y(self):
        return -1

    def led_range(self):
        pass

    def animate(self, animation, *, timeout=None):
        pass


class _LayoutCoordinate:
    def __init__(self, launchpad, layout, button_names, *,
                 name='',
                 coordinate_id=-1,
                 x=-1, y=-1):
        x, y = (self._determine_coordinate_from_name(name,
                                                     button_names)
                if x < 0 and y < 0 and len(name) > 0
                else (x, y))
        max_x, max_y = self._determine_bounds(button_names)

        x, y = (self._determine_coordinate_from_id(coordinate_id,
                                                   bounds=(max_x, max_y))
                if coordinate_id >= 0 and x < 0 and y < 0
                else (x, y))
        name = self._determine_name_from_coordinate(x, y,
                                                    button_names,
                                                    bounds=(max_x, max_y))
        midi_value = self._determine_midi_value(x, y,
                                                layout,
                                                bounds=(max_x, max_y))
        self._x = x
        self._y = y
        self._id = coordinate_id
        self._max_x = max_x
        self._max_y = max_y
        self._name = name
        self._midi_value = midi_value

    @property
    def id(self):
        within_range = (self._x >= 0
                        and self._y >= 0
                        and self._x < self._max_x
                        and self._y < self._max_y)
        if not within_range:
            return -1
        return (self._y * self._max_y) + self._x + 1

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
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    def _determine_coordinate_from_id(self, led_id, bounds):
        max_x, max_y = bounds
        x = int(led_id % max_x)
        y = int(led_id / max_y)
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
        max_x, max_y = bounds
        within_range = (x >= 0
                        and y >= 0
                        and x < max_x
                        and y < max_y)
        if not within_range:
            raise ValueError('Led(x,y) out of range: '
                             'value({},{}), '
                             'range((0,{}),(0,{}))'
                             .format(x, y, max_x, max_y))
        return layout[y][x]

    def _determine_name_from_coordinate(self, x, y, button_names, bounds):
        max_x, max_y = bounds
        within_range = (x >= 0
                        and y >= 0
                        and x < max_x
                        and y < max_y)
        if not within_range:
            raise ValueError('Led(x,y) out of range: '
                             'value({},{}), '
                             'range((0,{}),(0,{}))'
                             .format(x, y, max_x, max_y))
        return button_names[y][x]

    def _determine_bounds(self, button_names):
        if len(button_names) > 0:
            max_x = len(button_names[0])
            max_y = len(button_names)
            return max_x, max_y
        else:
            raise RuntimeError('Empty button name list.')

    def __repr__(self):
        return ('LayoutCoordinate(name={}, x={}, y={}, id={})'
                .format(self.name, self.x, self.y, self.id))


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
        names = list(map(lambda name: "'{}'".format(name), self.names))
        return 'ButtonGroup({})'.format(', '.join(names))

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
                       event_type=ButtonEvent.PRESS_RELEASE):
        """
        Polls for MIDI events of buttons specified
        in this group. If `timeout` is `None`, this function will
        wait indefinitely until a :class:`ButtonEvent` is
        received. If no event is received, `None` is returned.

        Keyword Args:
            interface (str): Interface to which to send message.
                (See :class:`Interface`.)
            timeout (float): Duration in seconds to wait for event to occur
            event_type (str): Event type.
                (Possible values: 'press', 'release', 'press|release')

        Returns:
            ButtonEvent: Button event (See :class:`ButtonEvent`).
        """
        if (not event_type
                or (event_type.lower().replace('|', '_') != ButtonEvent.PRESS_RELEASE  # noqa
                    and event_type.lower() != ButtonEvent.RELEASE
                    and event_type.lower() != ButtonEvent.PRESS)):
            raise ValueError('Not a valid event type.')

        midi_event = self._launchpad.poll_for_event(interface=interface,
                                                    timeout=timeout,
                                                    match=ButtonMatch(self._buttons,  # noqa
                                                                      event_type))  # noqa
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
                        raise ValueError('Invalid button "{}".'
                                         .format(str(arg)))
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

    def __init__(self, *, launchpad, button_names,
                 layout, x=-1, y=-1, name='', mode=STATIC):
        self._launchpad = launchpad
        self._button_names = button_names
        self._mode = mode
        self._x = self._y = -1

        name = (x if isinstance(x, str)
                and name == '' else name)
        if isinstance(x, str) and name == '':
            raise ValueError('Invalid name')
        x = -1 if isinstance(x, str) else x

        led_id = x if x >= 0 and y < 0 else -1
        x = -1 if isinstance(x, int) and led_id >= 0 else x

        coordinate = _LayoutCoordinate(launchpad=launchpad,
                                       layout=layout,
                                       button_names=button_names,
                                       name=name,
                                       coordinate_id=led_id,
                                       x=x, y=y)

        self._x = coordinate.x
        self._y = coordinate.y
        self._max_x = coordinate.max_x
        self._max_y = coordinate.max_y
        self._midi_value = coordinate.midi_value

    def __eq__(self, other):
        if not isinstance(other, Led):
            return False
        return (self.launchpad == other.launchpad
                and self.name == other.name)

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return ('Led(x={}, y={}, name=\'{}\')'
                .format(self.x, self.y, self.name))

    @property
    def id(self):
        """
        Unique ID of LED.
        """
        if not self._is_within_range():
            return -1
        return (self._y * self._max_y) + self._x + 1

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
            raise ValueError('Invalid color.')
        elif RgbColor.is_valid(value):
            rgb_color = RgbColor(value)
            colorspec = SysExMessages.colorspec_message(self._LIGHTING_TYPE['rgb'],  # noqa
                                                        self._midi_value,
                                                        rgb_color.r,
                                                        rgb_color.g,
                                                        rgb_color.b)
            self.launchpad.send_message(colorspec)
        else:
            color_id = value if ColorShade.is_valid_id(value) else -1
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
                lighting = SysExMessages.lighting_message(self._LIGHTING_MODE[self._mode],  # noqa
                                                          self._midi_value, color_id)   # noqa
                self.launchpad.send_message(lighting)

    @color.deleter
    def color(self):
        """Turns LED off."""
        self.reset()

    def reset(self):
        """Turns LED off."""
        lighting = SysExMessages.lighting_message(self._LIGHTING_MODE[self._mode],  # noqa
                                                  self._midi_value, 0x0)   # noqa
        self.launchpad.send_message(lighting)

    def _is_within_range(self):
        return self._x >= 0 \
                and self._y >= 0 \
                and self._x < self._max_x \
                and self._y < self._max_y


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
        coordinate = _LayoutCoordinate(launchpad=launchpad,
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
        return ('Button(name=\'{}\', x={}, y={}, id={})'
                .format(self.name, self.x, self.y, self.id))

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


class Panel(Animable):
    """
    Panel of Launchpad.

    The panel represents the 9x9 grid of buttons of the Launchpad.
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
        return 'Panel({}x{})'.format(self.max_x, self.max_y)

    @property
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @property
    def max_id(self):
        """
        Max ID.
        """
        return self.max_x * self.max_y

    @Animable.max_x.getter
    def max_x(self):
        """
        Max X.
        """
        return len(Panel._BUTTON_NAMES[0])

    @Animable.max_y.getter
    def max_y(self):
        """
        Max Y.
        """
        return len(Panel._BUTTON_NAMES)

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
        if layout == Panel.CUSTOM:
            return Led(launchpad=self._launchpad,
                       button_names=Panel._BUTTON_NAMES,
                       layout=Panel._CUSTOM_MODE_MIDI_LAYOUT,
                       x=x, y=y,
                       name=name, mode=mode)
        return Led(launchpad=self._launchpad,
                   button_names=Panel._BUTTON_NAMES,
                   layout=Panel._PROG_MODE_MIDI_LAYOUT,
                   x=x, y=y,
                   name=name, mode=mode)

    def led_range(self, *, layout=PROG, mode=Led.STATIC):
        """
        Returns an immutable sequence of LEDs.

        Keyword Args:
            layout (Layout): Layout of buttons.
            mode (str): Lighting mode.

        Yields:
            Led: Sequence of LEDs
        """
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
        if layout == Panel.CUSTOM:
            return ButtonGroup(launchpad=self._launchpad,
                               layout=Panel._CUSTOM_MODE_MIDI_LAYOUT,
                               button_names=Panel._BUTTON_NAMES,
                               args=list(args))
        return ButtonGroup(launchpad=self._launchpad,
                           layout=Panel._PROG_MODE_MIDI_LAYOUT,
                           button_names=Panel._BUTTON_NAMES,
                           args=list(args))


class Grid(Animable):
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
        return 'Grid({}x{})'.format(self.max_x, self.max_y)

    @property
    def launchpad(self):
        """
        Launchpad reference.
        """
        return self._launchpad

    @property
    def max_id(self):
        """
        Max ID.
        """
        return self.max_x * self.max_y

    @Animable.max_x.getter
    def max_x(self):
        """
        Max X.
        """
        return len(Grid._BUTTON_NAMES[0])

    @Animable.max_y.getter
    def max_y(self):
        """
        Max Y.
        """
        return len(Grid._BUTTON_NAMES)

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
        if layout == Grid.CUSTOM:
            return Led(launchpad=self._launchpad,
                       button_names=Grid._BUTTON_NAMES,
                       layout=Grid._CUSTOM_MODE_MIDI_LAYOUT,
                       x=x, y=y,
                       name=name, mode=mode)
        return Led(launchpad=self._launchpad,
                   button_names=Grid._BUTTON_NAMES,
                   layout=Grid._PROG_MODE_MIDI_LAYOUT,
                   x=x, y=y, name=name, mode=mode)

    def led_range(self, *, layout=PROG, mode=Led.STATIC):
        """
        Returns an immutable sequence of LEDs.

        Keyword Args:
            layout (Layout): Layout of buttons.
            mode (str): Lighting mode.

        Yields:
            Led: Sequence of LEDs
        """
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
        if layout == Grid.CUSTOM:
            return ButtonGroup(launchpad=self._launchpad,
                               layout=Grid._CUSTOM_MODE_MIDI_LAYOUT,
                               button_names=Grid._BUTTON_NAMES,
                               args=list(args))
        return ButtonGroup(launchpad=self._launchpad,
                           layout=Grid._PROG_MODE_MIDI_LAYOUT,
                           button_names=Grid._BUTTON_NAMES,
                           args=list(args))
