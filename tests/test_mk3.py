from rtmidi import MidiIn, MidiOut, API_RTMIDI_DUMMY
import unittest
from lpminimk3.__init__ import LaunchpadMiniMk3
from lpminimk3._utils import MidiEvent, MidiClient,\
        MidiPort, Interface, Mode, Layout
from lpminimk3.midi_messages import SysExMessages


CLIENT_NAME = 'Launchpad Mini MK3'
CLIENT_ID = 36

midi_out = MidiOut(API_RTMIDI_DUMMY, CLIENT_NAME)
midi_in = MidiIn(API_RTMIDI_DUMMY, CLIENT_NAME)

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


class TestMk3(unittest.TestCase):
    def _create_virtual_launchpad(self):
        midi_client = VirtualMidiClient(CLIENT_NAME, CLIENT_ID)
        self.daw_in_port = VirtualMidiPort(IN_PORTS['daw']['port_name'],
                                           IN_PORTS['daw']['port_number'],
                                           IN_PORTS['daw']['port_index'],
                                           IN_PORTS['daw']['system_port_name'],
                                           direction=VirtualMidiPort.IN,
                                           midi_in=midi_in)
        self.midi_in_port = VirtualMidiPort(IN_PORTS['midi']['port_name'],
                                            IN_PORTS['midi']['port_number'],
                                            IN_PORTS['midi']['port_index'],
                                            IN_PORTS['midi']['system_port_name'],  # noqa
                                            direction=VirtualMidiPort.IN,
                                            midi_in=midi_in)
        self.daw_out_port = VirtualMidiPort(OUT_PORTS['daw']['port_name'],
                                            OUT_PORTS['daw']['port_number'],
                                            OUT_PORTS['daw']['port_index'],
                                            OUT_PORTS['daw']['system_port_name'],  # noqa
                                            direction=VirtualMidiPort.OUT,
                                            midi_out=midi_out)
        self.midi_out_port = VirtualMidiPort(OUT_PORTS['midi']['port_name'],
                                             OUT_PORTS['midi']['port_number'],
                                             OUT_PORTS['midi']['port_index'],
                                             OUT_PORTS['midi']['system_port_name'],  # noqa
                                             direction=VirtualMidiPort.OUT,
                                             midi_out=midi_out)

        midi_client.append_out_port(self.daw_out_port)
        midi_client.append_out_port(self.midi_out_port)
        midi_client.append_in_port(self.daw_in_port)
        midi_client.append_in_port(self.midi_in_port)

        return VirtualLaunchpadMiniMk3(midi_client)

    def setUp(self):
        self.lp = self._create_virtual_launchpad()

    def tearDown(self):
        if self.lp.is_open():
            self.lp.close()

    def test_open_midi_interface(self):
        self.assertFalse(self.lp.is_open(), 'Launchpad ports already open.')
        self.lp.open(interface=Interface.MIDI)
        self.assertTrue(self.lp.is_open(), 'Failed to open launchpad ports.')

    def test_open_daw_interface(self):
        self.assertFalse(self.lp.is_open(), 'Launchpad ports already open.')
        self.lp.open(interface=Interface.DAW)
        self.assertTrue(self.lp.is_open(), 'Failed to open launchpad ports.')

    def test_close(self):
        self.assertFalse(self.lp.is_open(), 'Launchpad ports already open.')

        self.lp.open()
        self.assertTrue(self.lp.is_open(), 'Failed to open launchpad ports.')

        self.lp.close()
        self.assertFalse(self.lp.is_open(), 'Failed to close launchpad ports.')

    def test_send_message(self):
        self.lp.open()

        self.lp.send_message(DUMMY_MIDI_MESSAGE, interface=Interface.MIDI)
        self.assertEqual(self.lp.midi_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')

        self.lp.send_message(DUMMY_MIDI_MESSAGE,
                             interface=Interface.DAW)
        self.assertEqual(self.lp.daw_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE, 'MIDI message mismatch.')

        self.lp.send_message(DUMMY_MIDI_MESSAGE, interface='midi')
        self.assertEqual(self.lp.midi_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')

        self.lp.send_message(DUMMY_MIDI_MESSAGE, interface='daw')
        self.assertEqual(self.lp.daw_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')
        with self.assertRaises(RuntimeError):
            self.lp.send_message(DUMMY_MIDI_MESSAGE, interface=None)
        with self.assertRaises(RuntimeError):
            self.lp.send_message(DUMMY_MIDI_MESSAGE, interface='')

    def test_poll_for_event(self):
        self.lp.open()
        self.assertEqual(self.lp.poll_for_event(interface=Interface.MIDI),
                         DUMMY_MIDI_EVENT,
                         'MidiEvent mismatch.')
        self.assertEqual(self.lp.poll_for_event(interface=Interface.DAW),
                         DUMMY_MIDI_EVENT,
                         'MidiEvent mismatch.')
        with self.assertRaises(RuntimeError):
            self.lp.poll_for_event(interface=None)

    def test_id(self):
        self.lp.open()
        self.assertEqual(self.lp.id,
                         CLIENT_ID,
                         'Launchpad ID mismatch.')

    def test_daw_in_port(self):
        self.lp.open()
        self.assertEqual(self.lp.daw_in_port,
                         self.daw_in_port,
                         'DAW-in port mismatch.')

    def test_daw_out_port(self):
        self.lp.open()
        self.assertEqual(self.lp.daw_out_port,
                         self.daw_out_port,
                         'DAW-out port mismatch.')

    def test_midi_in_port(self):
        self.lp.open()
        self.assertEqual(self.lp.midi_in_port,
                         self.midi_in_port,
                         'MIDI-in port mismatch.')

    def test_midi_out_port(self):
        self.lp.open()
        self.assertEqual(self.lp.midi_out_port,
                         self.midi_out_port,
                         'MIDI-out port mismatch.')

    def test_interface(self):
        self.lp.open()

        self.lp.interface = Interface.DAW
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Interfaces.DAW,
                         'Interface mismatch.')

        self.lp.interface = Interface.MIDI
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Interfaces.MIDI,
                         'Interface mismatch.')

        self.lp.interface = 'daw'
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Interfaces.DAW,
                         'Interface mismatch.')

        self.lp.interface = 'midi'
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Interfaces.MIDI,
                         'Interface mismatch.')

        with self.assertRaises(ValueError):
            self.lp.interface = ''
        with self.assertRaises(ValueError):
            self.lp.interface = 'd'

    def test_mode(self):
        self.lp.open()

        self.lp.mode = Mode.LIVE
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Modes.LIVE,
                         'Mode mismatch.')

        self.lp.mode = Mode.PROG
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Modes.PROG,
                         'Mode mismatch.')

        self.lp.mode = 'live'
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Modes.LIVE,
                         'Mode mismatch.')

        self.lp.mode = 'prog'
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Modes.PROG,
                         'Mode mismatch.')

        with self.assertRaises(ValueError):
            self.lp.mode = ''
        with self.assertRaises(ValueError):
            self.lp.mode = 'l'

    def test_layout(self):
        self.lp.open()

        self.lp.layout = Layout.SESSION
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.SESSION,
                         'Layout mismatch.')

        self.lp.layout = Layout.CUSTOM_1
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.CUSTOM_1,
                         'Layout mismatch.')

        self.lp.layout = Layout.CUSTOM_2
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.CUSTOM_2,
                         'Layout mismatch.')

        self.lp.layout = Layout.CUSTOM_3
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.CUSTOM_3,
                         'Layout mismatch.')

        self.lp.layout = Layout.DAW_FADERS
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.DAW_FADERS,
                         'Layout mismatch.')

        self.lp.layout = Layout.PROG
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.PROG,
                         'Layout mismatch.')

        self.lp.layout = 'session'
        self.assertEqual(self.lp.interface.midi_event.message,
                         SysExMessages.Layouts.SESSION,
                         'Layout mismatch.')

        self.lp.layout = 'custom_1'
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.CUSTOM_1,
                         'Layout mismatch.')

        self.lp.layout = 'custom_2'
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.CUSTOM_2,
                         'Layout mismatch.')

        self.lp.layout = 'custom_3'
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.CUSTOM_3,
                         'Layout mismatch.')

        self.lp.layout = 'daw_faders'
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.DAW_FADERS,
                         'Layout mismatch.')

        self.lp.layout = 'prog'
        self.assertEqual(self.lp.layout.midi_event.message,
                         SysExMessages.Layouts.PROG,
                         'Layout mismatch.')

        with self.assertRaises(ValueError):
            self.lp.mode = ''
        with self.assertRaises(ValueError):
            self.lp.mode = 's'

    def test_device_inquiry(self):
        self.lp.open()
        self.assertEqual(self.lp.device_inquiry().message,
                         SysExMessages.Modes.PROG,
                         'Device inquiry mismatch.')


if __name__ == '__main__':
    unittest.main()
