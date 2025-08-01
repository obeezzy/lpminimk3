"""Software model and discovery functions for Launchpad Mini MK3.
"""
from rtmidi import MidiOut, MidiIn
from .components import (Grid,
                         Panel)
from .utils import (Interface,
                    Layout,
                    MidiClient,
                    MidiPort,
                    Mode)
from .midi_messages import SysExMessages
from .system_midi_port_parser import SystemMidiPortParser  # noqa


class LaunchpadMiniMk3:
    """A Launchpad Mini MK3 device.
    """

    def __init__(self, midi_client):
        self._midi_client = midi_client

    def __eq__(self, other):
        if not isinstance(other, LaunchpadMiniMk3):
            return False
        return self.id == other.id

    def __repr__(self):
        return f'LaunchpadMiniMk3(id={self.id})'

    def is_open(self):
        """Returns `True` if the device is open, otherwise
        returns `False`. An open device is a device that can
        be read from and/or written to.

        Returns
        -------
        Boolean
            `True` if device is open, otherwise `False`.
        """
        return self._midi_client.is_open()

    def open(self, interface=Interface.MIDI):
        """Opens interface `interface` on this device for reading
        and writing.

        Parameters
        ----------
        interface : str, optional
            Interface to open.

        Raises
        ------
        ValueError
            If `interface` is invalid.

        See Also
        --------
        Interface
        """
        self._midi_client.open(interface)
        self.interface = interface

    def close(self):
        """Closes this device.
        """
        self._midi_client.close()

    def send_message(self, msg, *, interface=Interface.MIDI):
        """Sends a MIDI message `msg` to the `interface` of
        this device.

        Parameters
        ----------
        message : list
            MIDI message.
        interface : str, optional
            Interface to which to send message.

        Raises
        ------
        ValueError
            If `interface` is invalid.
        RuntimeError
            If device is closed.
        """
        if self.is_open():
            if interface == Interface.DAW:
                self.daw_out_port.send_message(msg)
            elif interface == Interface.MIDI:
                self.midi_out_port.send_message(msg)
            else:
                raise ValueError('Must be a valid Interface')
        else:
            raise RuntimeError('Port closed.')

    def poll_for_event(self, *, interface=Interface.MIDI,
                       timeout=5, match=None):
        """Polls for a MIDI event from interface `interface` either until
        `timeout` is reached or `match` is found.

        Parameters
        ----------
        interface : str, optional
            Interface to poll.
        timeout : float, optional
            Duration in seconds to wait for event before returning `None`.
        match : Match or None, optional
            Match criterion.

        Returns
        -------
        MidiEvent
            MIDI event received.

        Raises
        ------
        ValueError
            If `interface` is invalid.
        RuntimeError
            If this device is closed.

        See Also
        --------
        Interface
        MidiEvent
        """
        if self.is_open():
            if interface == Interface.DAW:
                return self.daw_in_port.poll_for_event(timeout=timeout,
                                                       match=match)
            elif interface == Interface.MIDI:
                return self.midi_in_port.poll_for_event(timeout=timeout,
                                                        match=match)
            else:
                raise ValueError('Must be a valid Interface.')
        else:
            raise RuntimeError('Port closed.')

    def clear_event_queue(self, *, interface=Interface.MIDI):
        """Clears MIDI event queue for interface `interface`.

        Parameters
        ----------
        interface : str
            Interface to clear.

        Raises
        ------
        ValueError
            If `interface` is invalid.
        RuntimeError
            If device is closed.

        See Also
        --------
        Interface
        """
        if self.is_open():
            if interface == Interface.DAW:
                return self.daw_in_port.clear_event_queue()
            elif interface == Interface.MIDI:
                return self.midi_in_port.clear_event_queue()
            else:
                raise ValueError('Must be a valid Interface.')
        else:
            raise RuntimeError('Port closed.')

    @property
    def id(self):
        """Unique ID of this device.
        """
        return self._midi_client.client_number

    @property
    def daw_in_port(self):
        """DAW interface MIDI-in port.

        Used for internal purposes.
        """
        return self._midi_client.daw_in_port

    @property
    def daw_out_port(self):
        """DAW interface MIDI-out port.

        Used for internal purposes.
        """
        return self._midi_client.daw_out_port

    @property
    def midi_in_port(self):
        """MIDI interface MIDI-in port.

        Used for internal purposes.
        """
        return self._midi_client.midi_in_port

    @property
    def midi_out_port(self):
        """MIDI interface MIDI-out port.

        Used for internal purposes.
        """
        return self._midi_client.midi_out_port

    @property
    def interface(self):
        """Interface of Launchpad.

        See Also
        --------
        Interface
        """
        self.send_message(SysExMessages.Interfaces.READBACK)
        return Interface(self.poll_for_event())

    @interface.setter
    def interface(self, value):
        if value.lower() == Interface.MIDI:
            self.send_message(SysExMessages.Interfaces.MIDI)
        elif value.lower() == Interface.DAW:
            self.send_message(SysExMessages.Interfaces.DAW)
        else:
            raise ValueError('Invalid interface set.')

    @property
    def panel(self):
        """Panel of Launchpad; represents the 9x9 array of buttons,
        with face buttons included.

        See Also
        --------
        Panel
        """
        return Panel(self)

    @property
    def grid(self):
        """Grid of Launchpad; represents the 8x8 array of white,
        faceless buttons.

        See Also
        --------
        Grid
        """
        return Grid(self)

    @property
    def mode(self):
        """
        Mode of Launchpad.

        See Also
        --------
        Mode
        """
        self.send_message(SysExMessages.Modes.READBACK)
        return Mode(self.poll_for_event())

    @mode.setter
    def mode(self, value):
        if value.lower() == Mode.LIVE:
            self.send_message(SysExMessages.Modes.LIVE)
        elif value.lower() == Mode.PROG:
            self.send_message(SysExMessages.Modes.PROG)
        else:
            raise ValueError('Invalid mode set.')

    @property
    def layout(self):
        """Layout of Launchpad.

        See Also
        --------
        Layout
        """
        self.send_message(SysExMessages.Layouts.READBACK)
        return Layout(self.poll_for_event())

    @layout.setter
    def layout(self, value):
        if value.lower() == Layout.SESSION:
            self.send_message(SysExMessages.Layouts.SESSION)
        elif value.lower() == Layout.CUSTOM_1:
            self.send_message(SysExMessages.Layouts.CUSTOM_1)
        elif value.lower() == Layout.CUSTOM_2:
            self.send_message(SysExMessages.Layouts.CUSTOM_2)
        elif value.lower() == Layout.CUSTOM_3:
            self.send_message(SysExMessages.Layouts.CUSTOM_3)
        elif value.lower() == Layout.DAW_FADERS:
            self.send_message(SysExMessages.Layouts.DAW_FADERS)
        elif value.lower() == Layout.PROG:
            self.send_message(SysExMessages.Layouts.PROG)
        else:
            raise ValueError('Invalid layout set.')

    def device_inquiry(self):
        """Sends a "device inquiry" message to this device.

        Returns
        -------
        MidiEvent
            MIDI event received.
        """
        self.mode = Mode.PROG
        self.send_message(SysExMessages.DEVICE_INQUIRY)
        return self.poll_for_event()


def find_launchpads():
    """Searches for connected Launchpad Mini MK3 devices.

    Returns
    -------
    list of LaunchpadMiniMk3
        List of found devices.
    """
    out_ports = MidiOut().get_ports()
    in_ports = MidiIn().get_ports()
    parser = SystemMidiPortParser(in_ports, out_ports)

    found_launchpads = []
    for client_data in parser.found_clients:
        midi_client = MidiClient(client_data.client_name,
                                 client_data.client_number)

        for port_data in client_data.ports:
            midi_out = MidiOut()
            midi_in = MidiIn()
            midi_port = MidiPort(port_data.port_name,
                                 port_data.port_number,
                                 port_data.port_index,
                                 port_data.system_port_name,
                                 direction=port_data.direction,
                                 midi_out=midi_out,
                                 midi_in=midi_in)
            if port_data.direction == MidiPort.OUT:
                midi_client.append_out_port(midi_port)
            elif port_data.direction == MidiPort.IN:
                midi_client.append_in_port(midi_port)

        found_launchpads.append(LaunchpadMiniMk3(midi_client))

    return found_launchpads
