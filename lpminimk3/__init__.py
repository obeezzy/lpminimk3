from rtmidi import MidiOut as _MidiOut, MidiIn as _MidiIn
from ._components import Grid, Panel
from ._utils import SystemMidiPortParser as _SystemMidiPortParser,\
                    MidiPort as _MidiPort, MidiClient as _MidiClient, \
                    Interface, Mode, Layout
from .midi_messages import SysExMessages as _SysExMessages

_midi_out = _MidiOut()
_out_ports = _midi_out.get_ports()
_midi_in = _MidiIn()
_in_ports = _midi_in.get_ports()
_launchpad_port_prefixes = ['Launchpad Mini MK3 MIDI']


class LaunchpadMiniMk3:
    def __init__(self, midi_client):
        self._midi_client = midi_client

    def is_open(self):
        return self._midi_client.is_open()

    def open(self, interface=Interface.MIDI, *, mode='rw'):
        self._midi_client.open(interface, mode=mode)
        self.interface = interface

    def close(self):
        self._midi_client.close()

    def send_message(self, msg, *, interface=Interface.MIDI):
        if self.is_open():
            if interface == Interface.DAW:
                self.daw_out_port.send_message(msg)
            elif interface == Interface.MIDI:
                self.midi_out_port.send_message(msg)
            else:
                raise RuntimeError('No interface set.')
        else:
            raise RuntimeError('Port closed.')

    def poll_for_event(self, *, interface=Interface.MIDI,
                       timeout=5, match=None):
        if self.is_open():
            if interface == Interface.DAW:
                return self.daw_in_port.poll_for_event(timeout=timeout,
                                                       match=match)
            elif interface == Interface.MIDI:
                return self.midi_in_port.poll_for_event(timeout=timeout,
                                                        match=match)
            else:
                raise RuntimeError('No interface set.')
        else:
            raise RuntimeError('Port closed.')

    @property
    def id(self):
        return self._midi_client.client_number

    @property
    def daw_in_port(self):
        return self._midi_client.daw_in_port

    @property
    def daw_out_port(self):
        return self._midi_client.daw_out_port

    @property
    def midi_in_port(self):
        return self._midi_client.midi_in_port

    @property
    def midi_out_port(self):
        return self._midi_client.midi_out_port

    @property
    def interface(self):
        self.send_message(_SysExMessages.Interfaces.READBACK)
        return Interface(self.poll_for_event())

    @interface.setter
    def interface(self, value):
        if value.lower() == Interface.MIDI:
            self.send_message(_SysExMessages.Interfaces.MIDI)
        elif value.lower() == Interface.DAW:
            self.send_message(_SysExMessages.Interfaces.DAW)
        else:
            raise ValueError('Invalid interface set.')

    @property
    def panel(self):
        return Panel(self)

    @property
    def grid(self):
        return Grid(self)

    @property
    def mode(self):
        self.send_message(_SysExMessages.Modes.READBACK)
        return Mode(self.poll_for_event())

    @mode.setter
    def mode(self, value):
        if value.lower() == Mode.LIVE:
            self.send_message(_SysExMessages.Modes.LIVE)
        elif value.lower() == Mode.PROG:
            self.send_message(_SysExMessages.Modes.PROG)
        else:
            raise ValueError('Invalid mode set.')

    @property
    def layout(self):
        self.send_message(_SysExMessages.Layouts.READBACK)
        return Layout(self.poll_for_event())

    @layout.setter
    def layout(self, value):
        if value.lower() == Layout.SESSION:
            self.send_message(_SysExMessages.Layouts.SESSION)
        elif value.lower() == Layout.CUSTOM_1:
            self.send_message(_SysExMessages.Layouts.CUSTOM_1)
        elif value.lower() == Layout.CUSTOM_2:
            self.send_message(_SysExMessages.Layouts.CUSTOM_2)
        elif value.lower() == Layout.CUSTOM_3:
            self.send_message(_SysExMessages.Layouts.CUSTOM_3)
        elif value.lower() == Layout.DAW_FADERS:
            self.send_message(_SysExMessages.Layouts.DAW_FADERS)
        elif value.lower() == Layout.PROG:
            self.send_message(_SysExMessages.Layouts.PROG)
        else:
            raise ValueError('Invalid layout set.')

    def device_inquiry(self):
        self.mode = Mode.PROG
        self.send_message(_SysExMessages.DEVICE_INQUIRY)
        return self.poll_for_event()

    def __repr__(self):
        return 'LaunchpadMiniMk3(id={})'.format(self.id)


def find_launchpads():
    found_launchpad_out_ports = [port for port in _out_ports
                                 if any(launchpad in port
                                        for launchpad
                                        in _launchpad_port_prefixes)]
    found_launchpad_in_ports = [port for port in _in_ports
                                if any(launchpad in port
                                       for launchpad
                                       in _launchpad_port_prefixes)]
    found_midi_clients = {}
    for system_port_name in found_launchpad_out_ports:
        client_name, port_name = _SystemMidiPortParser\
                                    .extract_names(system_port_name)
        client_number, port_number = _SystemMidiPortParser\
            .extract_numbers(system_port_name)
        midi_client = _MidiClient(client_name, client_number)
        port_index = _out_ports.index(system_port_name)
        midi_port = _MidiPort(port_name, port_number,
                              port_index, system_port_name,
                              direction=_MidiPort.OUT,
                              midi_out=_midi_out)
        midi_client.append_out_port(midi_port)

        if midi_client.client_number not in found_midi_clients:
            found_midi_clients[midi_client.client_number] = midi_client
        else:
            existing_midi_client = found_midi_clients[midi_client.client_number]  # noqa
            existing_midi_client.append_out_port(midi_port)

    for system_port_name in found_launchpad_in_ports:
        client_name, port_name = _SystemMidiPortParser\
                                    .extract_names(system_port_name)
        client_number, port_number = _SystemMidiPortParser\
            .extract_numbers(system_port_name)
        port_index = _in_ports.index(system_port_name)
        midi_client = _MidiClient(client_name, client_number)
        midi_port = _MidiPort(port_name, port_number,
                              port_index, system_port_name,
                              midi_in=_midi_in,
                              direction=_MidiPort.IN)
        midi_client.append_in_port(midi_port)

        if midi_client.client_number not in found_midi_clients:
            found_midi_clients[midi_client.client_number] = midi_client
        else:
            existing_midi_client = found_midi_clients[midi_client.client_number]  # noqa
            existing_midi_client.append_in_port(midi_port)

    found_launchpads = []
    for client_number, found_client in found_midi_clients.items():
        found_launchpads.append(LaunchpadMiniMk3(found_client))

    return found_launchpads
