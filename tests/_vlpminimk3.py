from tests._rtmidi_dummy import MidiIn, MidiOut, API_RTMIDI_DUMMY
from lpminimk3.__init__ import LaunchpadMiniMk3
from lpminimk3._utils import MidiEvent, MidiClient,\
                             MidiPort
from lpminimk3.midi_messages import SysExMessages

CLIENT_NAME = 'Launchpad Mini MK3'
CLIENT_ID = 36

DUMMY_MIDI_MESSAGE = [0x90, 0x90, 0x90]
DUMMY_MIDI_EVENT = MidiEvent(DUMMY_MIDI_MESSAGE, 0)

IN_PORTS = {
        'daw': {
            'port_name': 'Launchpad Mini MK3 MIDI 1',
            'system_port_name': 'lpminimk3 dawin',
            'port_number': 0,
            'port_index': 4
            },
        'midi': {
            'port_name': 'Launchpad Mini MK3 MIDI 2',
            'system_port_name': 'lpminimk3 midiin',
            'port_number': 1,
            'port_index': 5
            }
    }
OUT_PORTS = {
        'daw': {
             'port_name': 'Launchpad Mini MK3 MIDI 1',
             'system_port_name': 'lpminimk3 dawout',
             'port_number': 0,
             'port_index': 4
            },
        'midi': {
             'port_name': 'Launchpad Mini MK3 MIDI 2',
             'system_port_name': 'lpminimk3 midiout',
             'port_number': 1,
             'port_index': 5
            }
    }


class VirtualMidiPort(MidiPort):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_message(self, message, *args, **kwargs):
        self.sent_message = message

    def poll_for_event(self, *args, **kwargs):
        return DUMMY_MIDI_EVENT


class VirtualMidiClient(MidiClient):
    pass


class VirtualLaunchpadMiniMk3(LaunchpadMiniMk3):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sent_message = None
        self.returned_event = None

    def send_message(self, message, *args, **kwargs):  # noqa
        self.sent_message = message
        if self.sent_message == SysExMessages.Interfaces.MIDI:
            self.returned_event = MidiEvent(SysExMessages.Interfaces.MIDI, 0)
        elif self.sent_message == SysExMessages.Interfaces.DAW:
            self.returned_event = MidiEvent(SysExMessages.Interfaces.DAW, 0)
        elif self.sent_message == SysExMessages.Modes.LIVE:
            self.returned_event = MidiEvent(SysExMessages.Modes.LIVE, 0)
        elif self.sent_message == SysExMessages.Modes.PROG:
            self.returned_event = MidiEvent(SysExMessages.Modes.PROG, 0)
        elif self.sent_message == SysExMessages.Layouts.SESSION:
            self.returned_event = MidiEvent(SysExMessages.Layouts.SESSION, 0)
        elif self.sent_message == SysExMessages.Layouts.CUSTOM_1:
            self.returned_event = MidiEvent(SysExMessages.Layouts.CUSTOM_1, 0)
        elif self.sent_message == SysExMessages.Layouts.CUSTOM_2:
            self.returned_event = MidiEvent(SysExMessages.Layouts.CUSTOM_2, 0)
        elif self.sent_message == SysExMessages.Layouts.CUSTOM_3:
            self.returned_event = MidiEvent(SysExMessages.Layouts.CUSTOM_3, 0)
        elif self.sent_message == SysExMessages.Layouts.DAW_FADERS:
            self.returned_event = MidiEvent(SysExMessages.Layouts.DAW_FADERS, 0)  # noqa
        elif self.sent_message == SysExMessages.Layouts.PROG:
            self.returned_event = MidiEvent(SysExMessages.Layouts.PROG, 0)
        elif self.sent_message == SysExMessages.DEVICE_INQUIRY:
            self.returned_event = MidiEvent(SysExMessages.Modes.PROG, 0)
        else:
            super().send_message(message, *args, **kwargs)

    def poll_for_event(self, *args, **kwargs):
        if self.sent_message == SysExMessages.Interfaces.READBACK \
                or self.sent_message == SysExMessages.Modes.READBACK \
                or self.sent_message == SysExMessages.Layouts.READBACK \
                or self.sent_message == SysExMessages.DEVICE_INQUIRY:
            return self.returned_event
        return super().poll_for_event(*args, **kwargs)


def create_virtual_launchpad():
    midi_out = MidiOut(API_RTMIDI_DUMMY, CLIENT_NAME)
    midi_in = MidiIn(API_RTMIDI_DUMMY, CLIENT_NAME)
    midi_client = VirtualMidiClient(CLIENT_NAME, CLIENT_ID)

    daw_in_port = VirtualMidiPort(IN_PORTS['daw']['port_name'],
                                  IN_PORTS['daw']['port_number'],
                                  IN_PORTS['daw']['port_index'],
                                  IN_PORTS['daw']['system_port_name'],
                                  direction=VirtualMidiPort.IN,
                                  midi_in=midi_in)
    midi_in_port = VirtualMidiPort(IN_PORTS['midi']['port_name'],
                                   IN_PORTS['midi']['port_number'],
                                   IN_PORTS['midi']['port_index'],
                                   IN_PORTS['midi']['system_port_name'],  # noqa
                                   direction=VirtualMidiPort.IN,
                                   midi_in=midi_in)
    daw_out_port = VirtualMidiPort(OUT_PORTS['daw']['port_name'],
                                   OUT_PORTS['daw']['port_number'],
                                   OUT_PORTS['daw']['port_index'],
                                   OUT_PORTS['daw']['system_port_name'],  # noqa
                                   direction=VirtualMidiPort.OUT,
                                   midi_out=midi_out)
    midi_out_port = VirtualMidiPort(OUT_PORTS['midi']['port_name'],
                                    OUT_PORTS['midi']['port_number'],
                                    OUT_PORTS['midi']['port_index'],
                                    OUT_PORTS['midi']['system_port_name'],  # noqa
                                    direction=VirtualMidiPort.OUT,
                                    midi_out=midi_out)

    midi_client.append_out_port(daw_out_port)
    midi_client.append_out_port(midi_out_port)
    midi_client.append_in_port(daw_in_port)
    midi_client.append_in_port(midi_in_port)

    return VirtualLaunchpadMiniMk3(midi_client)
