"""
MIDI messages for the Launchpad Mini MK3.
"""
from abc import ABC
from functools import reduce


class SysExMessages:
    DEVICE_INQUIRY = [0xf0, 0x7e, 0xe7, 0xf0, 0x06, 0x01, 0xf7]

    class Interfaces:
        DAW = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x10, 0x00, 0xf7]
        MIDI = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x10, 0x01, 0xf7]
        READBACK = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x10, 0xf7]

    class Layouts:
        SESSION = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x00, 0xf7]
        CUSTOM_1 = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x04, 0xf7]
        CUSTOM_2 = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x05, 0xf7]
        CUSTOM_3 = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x06, 0xf7]
        DAW_FADERS = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x0d, 0xf7]
        PROG = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0x7f, 0xf7]
        READBACK = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x00, 0xf7]

    class Modes:
        LIVE = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x0e, 0x00, 0xf7]
        PROG = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x0e, 0x01, 0xf7]
        READBACK = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x0e, 0xf7]


class MidiMessage(ABC):
    @property
    def data(self):
        return []


class Constants:
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
    def __init__(self, lighting_type, led_index, *lighting_data):
        self._lighting_type = lighting_type
        self._led_index = led_index
        self._lighting_data = list(lighting_data)

    @property
    def data(self):
        return ([self._lighting_type,
                self._led_index]
                + self._lighting_data)

    def append(self, lighting_data):
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
    def __init__(self, *fragments):
        self._start_clause = [0xf0, 0x00, 0x20, 0x29, 0x02, 0x0d, 0x03]
        self._fragments = list(fragments)
        self._end_clause = [0xf7]

    @MidiMessage.data.getter
    def data(self):
        payload = list(reduce(lambda data, fragment: data + fragment.data,
                              self._fragments, []))  # noqa
        return (self._start_clause
                + payload
                + self._end_clause)

    def append(self, fragment):
        if not isinstance(fragment, ColorspecFragment):
            raise ValueError('Must be a ColorspecFragment.')
        self._fragments.append(fragment)

    def __repr__(self):
        return f'Colorspec({self.data})'


class Lighting(MidiMessage):
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
        return [self._lighting_mode,
                self._midi_value,
                self._color_id]

    @property
    def lighting_mode(self):
        return self._lighting_mode

    @property
    def midi_value(self):
        return self._midi_value

    @property
    def color_id(self):
        return self._color_id
