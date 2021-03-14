import enum
import time

_MIDI_MESSAGE_LENGTH = 9

class MidiEvent:
    def __init__(self, message, deltatime):
        self._message = message
        self._deltatime = deltatime

    @property
    def message(self):
        return self._message

    @property
    def deltatime(self):
        return self._deltatime

    def __repr__(self):
        return 'MidiEvent(message={}, deltatime={})'.format(self.message, self.deltatime)

class MidiPort:
    OUT = 'out'
    IN = 'in'
    DEFAULT_CLIENT_NAME = 'lpminimk3'

    def __init__(self, port_name, port_number, port_index, full_port_name, *, direction, midi_in=None, midi_out=None):
        self._port_name = port_name
        self._port_number = port_number
        self._port_index = port_index
        self._full_port_name = full_port_name
        self._midi_in = midi_in
        self._midi_out = midi_out
        self._direction = direction
        if midi_in:
            midi_in.ignore_types(sysex=False, timing=False, active_sense=True)

    def __eq__(self, other):
        return self.full_port_name == other.full_port_name

    def __repr__(self):
        return 'MidiPort(name={}, number={}, index={})'.format(self.port_name, self.port_number, self.port_index, self.full_port_name)

    def __exit__(self):
        self.close()

    @property
    def port_name(self):
        return self._port_name

    @property
    def port_number(self):
        return self._port_number

    @property
    def port_index(self):
        return self._port_index

    @property
    def full_port_name(self):
        return self._full_port_name

    @property
    def midi_in_handle(self):
        return self._midi_in

    @property
    def midi_out_handle(self):
        return self._midi_out

    def is_open(self):
        if self._midi_in and self._direction == MidiPort.IN:
            return self._midi_in.is_port_open()
        elif self._midi_out and self._direction == MidiPort.OUT:
            return self._midi_out.is_port_open()
        return False

    def open(self):
        if self._direction == MidiPort.OUT and not self._midi_out.is_port_open():
            self._midi_out.open_port(self.port_index, MidiPort.OUT)
            self._midi_out.set_client_name(MidiPort.DEFAULT_CLIENT_NAME)
        elif self._direction == MidiPort.IN and not self._midi_in.is_port_open():
            self._midi_in.open_port(self.port_index, MidiPort.IN)
            self._midi_in.set_client_name(MidiPort.DEFAULT_CLIENT_NAME)

    def close(self):
        if self.is_open():
            if self._midi_out and self._direction == MidiPort.OUT:
                self._midi_out.close_port()
            elif self._midi_in and self._direction == MidiPort.IN:
                self._midi_in.close_port()

    def send_message(self, message):
        if self._midi_in and self._direction == MidiPort.IN:
            self._midi_in.send_message(message)
        elif self._midi_out and self._direction == MidiPort.OUT:
            self._midi_out.send_message(message)
        else:
            raise RuntimeError('Failed to send message.')

    def poll_for_event(self, *, timeout=5, match=None):
        if not self._midi_in:
            return
        event = None
        polling = True
        elapsed = 0
        timeout = 0 if timeout < 0 else timeout
        while polling and timeout > elapsed:
            raw_message = self._midi_in.get_message()
            event = MidiEvent(*raw_message) if raw_message else None
            if event and not match:
                polling = False
            elif event and match == event.message:
                polling = False
            time.sleep(.1)
            elapsed += .1 if timeout > 0 else 0
        return event

    def clear_event_queue(self):
        while self._midi_in and self._midi_in.get_message():
            continue

class Interface:
    DAW = 'daw'
    MIDI = 'midi'
    READBACK_POSITION = 7

    class MidiWord(enum.IntEnum):
        DAW = 0x00
        MIDI = 0x01

    def __init__(self, midi_event):
        if len(midi_event.message) != _MIDI_MESSAGE_LENGTH:
            raise RuntimeError('Unexpected MIDI message length.')
        self._midi_event = midi_event
        midi_value = midi_event.message[Interface.READBACK_POSITION]
        self._interface = Interface.MIDI \
                if midi_value == Interface.MidiWord.MIDI \
                else Interface.DAW

    def __repr__(self):
        return 'Interface()' if self._interface is None else 'Interface(\'Interface.{}\')'.format(self._interface.upper())

class Mode:
    LIVE = 'live'
    PROG = 'prog'
    READBACK_POSITION = 7

    class MidiWord(enum.IntEnum):
        LIVE = 0x00
        PROG = 0x01

    def __init__(self, midi_event):
        if len(midi_event.message) != _MIDI_MESSAGE_LENGTH:
            raise RuntimeError('Unexpected MIDI message length.')
        self._midi_event = midi_event
        midi_value = midi_event.message[Mode.READBACK_POSITION]
        self._mode = Mode.LIVE \
                if midi_value == Mode.MidiWord.LIVE \
                else Mode.PROG

    def __repr__(self):
        return 'Mode()' if self._mode is None else 'Mode(\'Mode.{}\')'.format(self._mode.upper())

class Layout:
    SESSION = 'session'
    CUSTOM_1 = 'custom_1'
    CUSTOM_2 = 'custom_2'
    CUSTOM_3 = 'custom_3'
    DAW_FADERS = 'daw_faders'
    PROG = 'prog'
    READBACK_POSITION = 7

    class MidiWord(enum.IntEnum):
        SESSION = 0x00
        CUSTOM_1 = 0x04
        CUSTOM_2 = 0x05
        CUSTOM_3 = 0x06
        DAW_FADERS = 0x0d
        PROG = 0x7f

    def __init__(self, midi_event):
        if len(midi_event.message) != _MIDI_MESSAGE_LENGTH:
            raise RuntimeError('Unexpected MIDI message length.')
        self._midi_event = midi_event
        midi_value = midi_event.message[Layout.READBACK_POSITION]
        if midi_value == Layout.MidiWord.SESSION:
            self._layout = Layout.SESSION
        elif midi_value == Layout.MidiWord.CUSTOM_1:
            self._layout = Layout.CUSTOM_1
        elif midi_value == Layout.MidiWord.CUSTOM_2:
            self._layout = Layout.CUSTOM_2
        elif midi_value == Layout.MidiWord.CUSTOM_3:
            self._layout = Layout.CUSTOM_3
        elif midi_value == Layout.MidiWord.DAW_FADERS:
            self._layout = Layout.DAW_FADERS
        elif midi_value == Layout.MidiWord.PROG:
            self._layout = Layout.PROG

    def __repr__(self):
        return 'Layout()' if self._layout is None else 'Layout(\'Layout.{}\')'.format(self._layout.upper())

class MidiClient:
    def __init__(self, client_name, client_number):
        self._client_name = client_name
        self._client_number = client_number
        self._out_ports = []
        self._in_ports = []

    def __eq__(self, other):
        return self.client_name == other.client_name

    def __repr__(self):
        return 'MidiClient(name={}, number={})'.format(self.client_name, self.client_number)

    @property
    def daw_out_port(self):
        daw_ports = list(filter(lambda port: '1' in port.port_name, self._out_ports))
        return daw_ports[0] if len(daw_ports) > 0 else None

    @property
    def daw_in_port(self):
        daw_ports = list(filter(lambda port: '1' in port.port_name, self._in_ports))
        return daw_ports[0] if len(daw_ports) > 0 else None

    @property
    def midi_out_port(self):
        midi_ports = list(filter(lambda port: '2' in port.port_name, self._out_ports))
        return midi_ports[0] if len(midi_ports) > 0 else None

    @property
    def midi_in_port(self):
        midi_ports = list(filter(lambda port: '2' in port.port_name, self._in_ports))
        return midi_ports[0] if len(midi_ports) > 0 else None

    @property
    def ports(self):
        return self._out_ports + self._in_ports

    @property
    def out_ports(self):
        return self._out_ports

    @property
    def in_ports(self):
        return self._in_ports

    @property
    def client_name(self):
        return self._client_name

    @property
    def client_number(self):
        return self._client_number

    def is_open(self):
        return all(port.is_open() for port in self.ports)

    def open(self, interface=Interface.MIDI, *, mode='rw'):
        self.close()
        if interface == Interface.DAW:
            if 'r' in mode:
                self.daw_in_port.open()
            if 'w' in mode:
                self.daw_out_port.open()
        elif interface == Interface.MIDI:
            self.midi_in_port.open()
            if 'r' in mode.lower():
                self.midi_in_port.open()
            if 'w' in mode.lower():
                self.midi_out_port.open()
        else:
            raise ValueError('Must be a valid Interface.')

    def close(self):
        for port in self.ports:
            if port.is_open():
                port.close()

    def append_out_port(self, port):
        if not isinstance(port, MidiPort):
            raise TypeError('Must be of type "MidiPort".')
        if port not in self._out_ports:
            self._out_ports.append(port)

    def append_in_port(self, port):
        if not isinstance(port, MidiPort):
            raise TypeError('Must be of type "MidiPort".')
        if port not in self._in_ports:
            self._in_ports.append(port)

class SystemMidiPortParser:
    @staticmethod
    def extract_names(full_port_name):
        client_name = ''
        port_name = ''
        tokens = full_port_name.split(' ')[::-1]
        tokens.pop(0) # Remove port pair e.g. '36:0'
        name_pair = ' '.join(tokens[::-1])
        if len(name_pair.split(':')) == 2:
            client_name = name_pair.split(':')[0]
            port_name = name_pair.split(':')[1]
        return client_name, port_name

    @staticmethod
    def extract_numbers(full_port_name):
        client_number = int(full_port_name.split(' ')[::-1][0].split(':')[0])
        port_number = int(full_port_name.split(' ')[::-1][0].split(':')[1])
        return client_number, port_number
