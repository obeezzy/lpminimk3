"""MIDI messages for the Launchpad Mini MK3.
"""

from abc import ABC
from functools import reduce


class SysExMessages:
    """SysEx messages.
    """
    DEVICE_INQUIRY = [0xf0, 0x7e, 0xe7, 0xf0, 0x06, 0x01, 0xf7]

    class Interfaces:
        """SysEx Interface messages.
        """
        DAW = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x10, 0x00, 0xf7]
        MIDI = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x10, 0x01, 0xf7]
        READBACK = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x10, 0xf7]

    class Layouts:
        """SysEx Layout messages.
        """
        SESSION = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x00, 0xf7]
        CUSTOM_1 = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x04, 0xf7]
        CUSTOM_2 = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x05, 0xf7]
        CUSTOM_3 = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x06, 0xf7]
        DAW_FADERS = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x0d, 0xf7]
        PROG = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x7f, 0xf7]
        READBACK = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0xf7]

    class Modes:
        """SysEx Mode messages.
        """
        LIVE = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x0e, 0x00, 0xf7]
        PROG = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x0e, 0x01, 0xf7]
        READBACK = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x0e, 0xf7]


class MidiMessage(ABC):
    """MIDI message.
    """
    @property
    def data(self):
        """Data.
        """
        return []


class Constants:
    """Constants.
    """
    DEFAULT_COLOR_ID = 9
    MIDI_MIN_VALUE = 0
    MIDI_MAX_VALUE = 0x7f

    class LightingMode:
        OFF = 0x80
        STATIC = 0x90
        FLASH = 0x91

    class LightingType:
        STATIC = 0x00
        FLASH = 0x01
        PULSE = 0x02
        RGB = 0x03

    class MidiWord:
        NOTE_HEADER = 0x90
        CC_HEADER = 0xb0


class ColorspecFragment:
    """Colorspec fragment.
    """
    def __init__(self, lighting_type, led_index, *lighting_data):
        self._lighting_type = lighting_type
        self._led_index = led_index
        self._lighting_data = list(lighting_data)

    @property
    def data(self):
        """Data.
        """
        return ([self._lighting_type,
                self._led_index]
                + self._lighting_data)

    def append(self, lighting_data):
        """Append lighting data `lighting_data`.

        Parameters
        ----------
        lighting_data : list of int
            Lighting data.
        """
        self._lighting_data.extend(lighting_data)

    def __repr__(self):
        return ('ColorspecFragment('
                f'lighting_type={self._lighting_type}, '
                f'led_index={self._led_index}, '
                f'lighting_data={self._lighting_data})')

    def __str__(self):
        fragment_str = str([self._lighting_type, self._led_index]
                           + list(self._lighting_data))
        return fragment_str


class Colorspec(MidiMessage):
    """Colorspec MIDI message.
    """
    def __init__(self, *fragments):
        self._start_clause = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x03]
        self._fragments = list(fragments)
        self._end_clause = [0xf7]

    @MidiMessage.data.getter
    def data(self):
        """Data.
        """
        payload = list(reduce(lambda data, fragment: data + fragment.data,
                              self._fragments, []))  # noqa
        return (self._start_clause
                + payload
                + self._end_clause)

    def append(self, fragment):
        """Append fragment to colorspec.

        Parameters
        ----------
        fragment : ColorspecFragment
            Colorspec fragment.

        See Also
        --------
        ColorspecFragment
        """
        if not isinstance(fragment, ColorspecFragment):
            raise ValueError('Must be a ColorspecFragment.')
        self._fragments.append(fragment)

    def __repr__(self):
        return f'Colorspec({self.data})'


class Lighting(MidiMessage):
    """Lighting MIDI message.
    """
    def __init__(self, lighting_mode, midi_value, color_id):
        self._lighting_mode = lighting_mode
        self._midi_value = midi_value
        self._color_id = color_id

    def __repr__(self):
        return ('Lighting('
                f'lighting_mode={self._lighting_mode}, '
                f'midi_value={self._midi_value}, '
                f'color_id={self.color_id})')

    @MidiMessage.data.getter
    def data(self):
        """Data.
        """
        return [self._lighting_mode,
                self._midi_value,
                self._color_id]

    @property
    def lighting_mode(self):
        """Lighting mode.
        """
        return self._lighting_mode

    @property
    def midi_value(self):
        """MIDI value.
        """
        return self._midi_value

    @property
    def color_id(self):
        """Color ID.
        """
        return self._color_id
