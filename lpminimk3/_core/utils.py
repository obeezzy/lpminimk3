"""
Utility classes for Launchpad Mini MK3.
"""

import enum
import time
import re
import platform
from collections import namedtuple
from . import logging
from ..match import Match

logger = logging.getLogger(__name__)

MIDI_MESSAGE_LENGTH = 9


class MidiEvent:
    """
    A MIDI event.

    A MIDI event is received every time the Launchpad's MIDI port
    is read.
    """

    def __init__(self, message, deltatime=0):
        self._message = message
        self._deltatime = deltatime

    def __eq__(self, other):
        if not isinstance(other, (MidiEvent, list)):
            return False
        if isinstance(other, list):
            return self.message == other
        return self.message == other.message

    @property
    def message(self):
        return self._message

    @property
    def deltatime(self):
        return self._deltatime

    def __repr__(self):
        return ('MidiEvent('
                f'message={self.message}, '
                f'deltatime={self.deltatime})')


class ButtonEvent:
    """
    A button event.

    A button event is received every time a button on the Launchpad
    is pushed.
    """

    PRESS = 'press'
    RELEASE = 'release'
    PRESS_RELEASE = 'press_release'

    def __init__(self, midi_event, buttons):
        self._midi_event = midi_event
        self._button = self._determine_button(midi_event, buttons)

    def __eq__(self, other):
        if not isinstance(other, ButtonEvent):
            return False
        return self.midi_event == other.midi_event

    def __repr__(self):
        return ("ButtonEvent("
                f"button='{self.button.name}', "
                f"type='{self.type}', "
                f"deltatime={self.deltatime})")

    @property
    def message(self):
        return self._midi_event.message

    @property
    def deltatime(self):
        return self._midi_event.deltatime

    @property
    def button(self):
        return self._button

    @property
    def type(self):
        if not self._midi_event:
            return ''
        return (ButtonEvent.RELEASE
                if self._midi_event
                and len(self._midi_event.message) == 3
                and self._midi_event.message[2] == 0x0
                else ButtonEvent.PRESS)

    def _determine_button(self, midi_event, buttons):
        found_buttons = (list(filter(lambda b: b.midi_value == midi_event.message[1], buttons))  # noqa
                         if midi_event and midi_event.message and len(midi_event.message) == 3  # noqa
                         else None)
        return (found_buttons[0]
                if found_buttons and len(found_buttons)
                else None)


class MidiPort:
    """
    A MIDI port.
    """

    OUT = 'out'
    IN = 'in'
    DEFAULT_CLIENT_NAME = 'lpminimk3'

    def __init__(self, port_name, port_number, port_index,
                 system_port_name, *, direction,
                 midi_in=None, midi_out=None,
                 virtual=False):
        self._port_name = port_name
        self._port_number = port_number
        self._port_index = port_index
        self._system_port_name = system_port_name
        self._midi_in = midi_in
        self._midi_out = midi_out
        self._direction = direction
        self._virtual = virtual
        if midi_in:
            midi_in.ignore_types(sysex=False, timing=False)

    def __eq__(self, other):
        if not isinstance(other, MidiPort):
            return False
        return self.system_port_name == other.system_port_name

    def __repr__(self):
        return ("MidiPort("
                f"name='{self.port_name}', "
                f"number={self.port_number}, "
                f"index={self.port_index})")

    def __exit__(self, *args, **kwargs):
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
    def system_port_name(self):
        return self._system_port_name

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
        if (self._direction == MidiPort.OUT
                and not self._midi_out.is_port_open()):
            if self._virtual:
                self._midi_out.open_virtual_port(self._system_port_name)
            else:
                self._midi_out.open_port(self.port_index, MidiPort.OUT)

            if platform.system() != 'Windows' and platform.system() != 'Darwin':
                self._midi_out.set_client_name(MidiPort.DEFAULT_CLIENT_NAME)

        elif (self._direction == MidiPort.IN
                and not self._midi_in.is_port_open()):
            if self._virtual:
                self._midi_in.open_virtual_port(self._system_port_name)
            else:
                self._midi_in.open_port(self.port_index, MidiPort.IN)

            if platform.system() != 'Windows' and platform.system() != 'Darwin':
                self._midi_in.set_client_name(MidiPort.DEFAULT_CLIENT_NAME)

    def close(self):
        if self.is_open():
            if self._midi_out and self._direction == MidiPort.OUT:
                self._midi_out.close_port()
            elif self._midi_in and self._direction == MidiPort.IN:
                self._midi_in.close_port()

    def send_message(self, message):
        if (not message
                or (not isinstance(message, list)
                    and not hasattr(message, 'data'))):
            raise TypeError('Message must be of type list or MidiMessage.')
        message = (message.data
                   if hasattr(message, 'data')
                   else message)

        if self._midi_in and self._direction == MidiPort.IN:
            self._midi_in.send_message(message)
            logger.debug(f'MIDI message sent: {message}')
        elif self._midi_out and self._direction == MidiPort.OUT:
            self._midi_out.send_message(message)
            logger.debug(f'MIDI message sent: {message}')
        else:
            raise RuntimeError('Failed to send message.')

    def poll_for_event(self, *, timeout=5, match=None, read_delay=.001):
        assert self._midi_in
        event = None
        polling = True
        elapsed = 0 if timeout else -1
        timeout = 0 if not timeout else timeout
        timeout = 0 if timeout < 0 else timeout
        while polling and timeout > elapsed:
            try:
                raw_message = self._midi_in.get_message()
                event = MidiEvent(*raw_message) if raw_message else None
                logger.debug(f'MIDI event: {event}')
                if event and not match:
                    polling = False
                elif event and isinstance(match, list) and match == event.message:  # noqa
                    polling = False
                elif event and isinstance(match, Match) and match.contains(event.message):  # noqa
                    polling = False
                time.sleep(read_delay)
                elapsed += .1 if timeout and timeout > 0 else 0
            except KeyboardInterrupt:
                logger.debug('\nPolling terminated.')
                raise
        return event

    def clear_event_queue(self, *, read_delay=.001):
        while self._midi_in and self._midi_in.get_message():
            time.sleep(read_delay)


class Interface:
    """
    Interface of the launchpad.
    """

    DAW = 'daw'
    MIDI = 'midi'
    READBACK_POSITION = 7

    class MidiWord(enum.IntEnum):
        DAW = 0x00
        MIDI = 0x01

    def __init__(self, midi_event):
        if len(midi_event.message) != MIDI_MESSAGE_LENGTH:
            raise RuntimeError('Unexpected MIDI message length; '
                               f'expected {MIDI_MESSAGE_LENGTH}, '
                               f'got {len(midi_event.message)}.')
        self._midi_event = midi_event
        midi_value = midi_event.message[Interface.READBACK_POSITION]
        self._interface = (Interface.MIDI
                           if midi_value == Interface.MidiWord.MIDI
                           else Interface.DAW)

    def __eq__(self, other):
        if (not isinstance(other, str)
                or (other.lower() != Interface.MIDI
                    and other.lower() != Interface.DAW)):
            return False
        return self.midi_event == other.midi_event

    def __repr__(self):
        return ('Interface()'
                if not self._interface
                else f"Interface('Interface.{self._interface.upper()}')")

    @property
    def midi_event(self):
        return self._midi_event


class Mode:
    """
    A Launchpad mode.
    """

    LIVE = 'live'
    PROG = 'prog'
    READBACK_POSITION = 7

    class MidiWord(enum.IntEnum):
        LIVE = 0x00
        PROG = 0x01

    def __init__(self, midi_event):
        if len(midi_event.message) != MIDI_MESSAGE_LENGTH:
            raise RuntimeError('Unexpected MIDI message length; '
                               f'expected {MIDI_MESSAGE_LENGTH}, '
                               f'got {midi_event.message}.')
        self._midi_event = midi_event
        midi_value = midi_event.message[Mode.READBACK_POSITION]
        self._mode = (Mode.LIVE
                      if midi_value == Mode.MidiWord.LIVE
                      else Mode.PROG)

    def __eq__(self, other):
        if (not isinstance(other, str)
                or (other.lower() != Mode.LIVE
                    and other.lower() != Mode.PROG)):
            return False
        return self.midi_event == other.midi_event

    def __repr__(self):
        return ('Mode()'
                if not self._mode
                else f"Mode('Mode.{self._mode.upper()}')")

    @property
    def midi_event(self):
        return self._midi_event


class Layout:
    """
    A Launchpad layout.
    """

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
        if len(midi_event.message) != MIDI_MESSAGE_LENGTH:
            raise RuntimeError('Unexpected MIDI message length; '
                               f'expected {MIDI_MESSAGE_LENGTH}, '
                               f'got {len(midi_event.message)}.')
        self._midi_event = midi_event
        midi_value = midi_event.message[Layout.READBACK_POSITION]
        self._layout = self._determine_layout(midi_value)

    def __eq__(self, other):
        if (not isinstance(other, str)
                or (other.lower() != Layout.SESSION
                    and other.lower() != Layout.CUSTOM_1
                    and other.lower() != Layout.CUSTOM_2
                    and other.lower() != Layout.CUSTOM_3
                    and other.lower() != Layout.DAW_FADERS
                    and other.lower() != Layout.PROG)):
            return False
        return self.midi_event == other.midi_event

    def __repr__(self):
        return ('Layout()'
                if not self._layout
                else f"Layout('Layout.{self._layout.upper()}')")

    @property
    def midi_event(self):
        return self._midi_event

    def _determine_layout(self, midi_value):
        if midi_value == Layout.MidiWord.SESSION:
            layout = Layout.SESSION
        elif midi_value == Layout.MidiWord.CUSTOM_1:
            layout = Layout.CUSTOM_1
        elif midi_value == Layout.MidiWord.CUSTOM_2:
            layout = Layout.CUSTOM_2
        elif midi_value == Layout.MidiWord.CUSTOM_3:
            layout = Layout.CUSTOM_3
        elif midi_value == Layout.MidiWord.DAW_FADERS:
            layout = Layout.DAW_FADERS
        else:
            layout = Layout.PROG
        return layout


class MidiClient:
    """
    A MIDI client.
    """

    def __init__(self, client_name, client_number):
        self._client_name = client_name
        self._client_number = client_number
        self._out_ports = []
        self._in_ports = []

    def __eq__(self, other):
        if not isinstance(other, MidiClient):
            return False
        return (self.client_name == other.client_name
                and self.client_number == other.client_number)

    def __repr__(self):
        return ("MidiClient("
                f"name='{self.client_name}', "
                f"number={self.client_number})")

    @property
    def daw_out_port(self):
        daw_ports = list(filter(lambda port: re.search(r'1|DA',
                                port.port_name),
                                self._out_ports))
        return daw_ports[0] if len(daw_ports) > 0 else None

    @property
    def daw_in_port(self):
        daw_ports = list(filter(lambda port: re.search(r'1|DA',
                                port.port_name),
                                self._in_ports))
        return daw_ports[0] if len(daw_ports) > 0 else None

    @property
    def midi_out_port(self):
        midi_ports = list(filter(lambda port: re.search(r'2|MI',
                                 port.port_name),
                                 self._out_ports))
        return midi_ports[0] if len(midi_ports) > 0 else None

    @property
    def midi_in_port(self):
        midi_ports = list(filter(lambda port: re.search(r'2|MI',
                                 port.port_name),
                                 self._in_ports))
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

    def open(self, interface=Interface.MIDI):
        self.close()
        if interface == Interface.DAW:
            self.daw_in_port.open()
            self.daw_out_port.open()
        elif interface == Interface.MIDI:
            self.midi_in_port.open()
            self.midi_out_port.open()
        else:
            raise ValueError('Must be a valid Interface.')

    def close(self):
        for port in self.ports:
            if port.is_open():
                port.close()

    def append_out_port(self, port):
        if not isinstance(port, MidiPort):
            raise TypeError('Must be of type MidiPort.')
        if port not in self._out_ports:
            self._out_ports.append(port)

    def append_in_port(self, port):
        if not isinstance(port, MidiPort):
            raise TypeError('Must be of type MidiPort.')
        if port not in self._in_ports:
            self._in_ports.append(port)


class SystemMidiPortParser:
    """
    System-specific way of parsing MIDI port names.
    """

    def __init__(self, in_ports, out_ports):
        lp_in_ports = list(filter(lambda port: re.search(r'Mini\s*MK3',
                                                         port,
                                                         re.IGNORECASE),
                                  in_ports))
        lp_out_ports = list(filter(lambda port: re.search(r'Mini\s*MK3',
                                                          port,
                                                          re.IGNORECASE),
                                   out_ports))
        self._found_clients = []
        self._parse(lp_in_ports,
                    in_ports,
                    MidiPort.IN)
        self._parse(lp_out_ports,
                    out_ports,
                    MidiPort.OUT)

    def _parse(self, lp_ports, ports, direction):
        ClientData = namedtuple('ClientData',
                                ['client_name',
                                 'client_number',
                                 'ports'])
        PortData = namedtuple('PortData',
                              ['port_name',
                               'port_number',
                               'port_index',
                               'system_port_name',
                               'direction'])
        for index, system_port_name in enumerate(lp_ports):
            linux_match = re.match(r'(.+):(.+)\s(\d+):(\d+)$', system_port_name)  # noqa
            windows_match = re.match(r'^(.+)\s\d+$', system_port_name)
            windows_match2 = re.match(r'(.+)\s\((.+)\)\s\d+$', system_port_name)  # noqa
            mac_match = re.match(r'(.+\sMK3)\s(.+)$', system_port_name)

            client_name = ''
            port_name = ''
            client_number = int(index + 1)
            port_number = int(index + 1)

            if linux_match:
                client_name = linux_match.group(1)
                port_name = linux_match.group(2)
                client_number = int(linux_match.group(3))
                port_number = int(linux_match.group(4))
            elif windows_match and not windows_match2:
                client_name = windows_match.group(1)
                port_name = system_port_name
            elif windows_match2:
                client_name = windows_match2.group(2)
                port_name = system_port_name
            elif mac_match:
                client_name = mac_match.group(1)
                port_name = system_port_name

            port_index = ports.index(system_port_name)
            port_data = PortData(port_name,
                                 port_number,
                                 port_index,
                                 system_port_name,
                                 direction)
            existing_client_data = list(filter(lambda c: c.client_name == client_name,  # noqa
                                        self._found_clients))
            existing_client_data = (existing_client_data[0]
                                    if len(existing_client_data) > 0
                                    else None)
            if not existing_client_data:
                client_data = ClientData(client_name,
                                         client_number,
                                         [])
                client_data.ports.append(port_data)
                self._found_clients.append(client_data)
            else:
                existing_client_data.ports.append(port_data)

    @property
    def found_clients(self):
        return self._found_clients
