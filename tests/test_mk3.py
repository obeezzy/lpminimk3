import unittest
from lpminimk3.utils import Interface, Mode, Layout
from lpminimk3.midi_messages import SysExMessages
from tests._vlpminimk3 import (DUMMY_MIDI_MESSAGE,
                               DUMMY_MIDI_EVENT,
                               CLIENT_ID,
                               create_virtual_launchpad)


class TestMk3(unittest.TestCase):
    def setUp(self):
        self.lp = create_virtual_launchpad()

    def tearDown(self):
        self.lp.close()

    def test_open_midi_interface(self):
        self.assertFalse(self.lp.is_open(),
                         'Launchpad ports already open.')
        self.lp.open(interface=Interface.MIDI)
        self.assertTrue(self.lp.is_open(),
                        'Failed to open launchpad ports.')

    def test_open_daw_interface(self):
        self.assertFalse(self.lp.is_open(),
                         'Launchpad ports already open.')
        self.lp.open(interface=Interface.DAW)
        self.assertTrue(self.lp.is_open(),
                        'Failed to open launchpad ports.')

    def test_close(self):
        self.assertFalse(self.lp.is_open(),
                         'Launchpad ports already open.')

        self.lp.open()
        self.assertTrue(self.lp.is_open(),
                        'Failed to open launchpad ports.')

        self.lp.close()
        self.assertFalse(self.lp.is_open(),
                         'Failed to close launchpad ports.')

    def test_send_message(self):
        self.lp.open()

        self.lp.send_message(DUMMY_MIDI_MESSAGE, interface=Interface.MIDI)
        self.assertEqual(self.lp.midi_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')

        self.lp.send_message(DUMMY_MIDI_MESSAGE,
                             interface=Interface.DAW)
        self.assertEqual(self.lp.daw_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')

        self.lp.send_message(DUMMY_MIDI_MESSAGE, interface='midi')
        self.assertEqual(self.lp.midi_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')

        self.lp.send_message(DUMMY_MIDI_MESSAGE, interface='daw')
        self.assertEqual(self.lp.daw_out_port.sent_message,
                         DUMMY_MIDI_MESSAGE,
                         'MIDI message mismatch.')
        with self.assertRaises(ValueError):
            self.lp.send_message(DUMMY_MIDI_MESSAGE, interface=None)
        with self.assertRaises(ValueError):
            self.lp.send_message(DUMMY_MIDI_MESSAGE, interface='')

    def test_poll_for_event(self):
        self.lp.open()
        self.assertEqual(self.lp.poll_for_event(interface=Interface.MIDI),
                         DUMMY_MIDI_EVENT,
                         'MidiEvent mismatch.')
        self.assertEqual(self.lp.poll_for_event(interface=Interface.DAW),
                         DUMMY_MIDI_EVENT,
                         'MidiEvent mismatch.')
        with self.assertRaises(ValueError):
            self.lp.poll_for_event(interface=None)

    def test_id(self):
        self.lp.open()
        self.assertEqual(self.lp.id,
                         CLIENT_ID,
                         'Launchpad ID mismatch.')

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
            self.lp.layout = ''
        with self.assertRaises(ValueError):
            self.lp.layout = 's'

    def test_device_inquiry(self):
        self.lp.open()
        self.assertEqual(self.lp.device_inquiry().message,
                         SysExMessages.Modes.PROG,
                         'Device inquiry mismatch.')

    def test_eq(self):
        self.lp.open()

        another_lp = create_virtual_launchpad(client_id=99)
        another_lp.open()

        self.assertTrue(self.lp != another_lp,
                        'Launchpad mismatch.')
        self.assertTrue(self.lp.id != another_lp.id,
                        'Launchpad ID mismatch.')
        self.assertTrue(self.lp.interface != another_lp.interface,
                        'Launchpad interface mismatch.')
        self.assertTrue(self.lp.mode != another_lp.mode,
                        'Launchpad mode mismatch.')
        self.assertTrue(self.lp.layout != another_lp.layout,
                        'Launchpad layout mismatch.')
        self.assertTrue(self.lp.panel != another_lp.panel,
                        'Launchpad panel mismatch.')
        self.assertTrue(self.lp.grid != another_lp.grid,
                        'Launchpad grid mismatch.')


if __name__ == '__main__':
    unittest.main()
