import unittest
from lpminimk3.utils import MidiPort
from lpminimk3.system_midi_port_parser import SystemMidiPortParser
import os


class TestSystemMidiPortParser(unittest.TestCase):
    def test_parse_midi_ports_linux(self):
        os.environ["SIMULATED_OS"] = "Linux"
        out_ports = ["Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",
                     "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1"]
        in_ports = ["Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",
                    "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1"]

        parser = SystemMidiPortParser(in_ports, out_ports)
        self.assertEqual(len(parser.found_clients),
                         1,
                         "Client count mismatch.")

        # DAW IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DA",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_number,
                         0,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MI",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DA",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_number,
                         0,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MI",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

    def test_parse_midi_ports_windows(self):
        os.environ["SIMULATED_OS"] = "Windows"
        out_ports = ["Microsoft GS Wavetable Synth 0",
                     "LPMiniMK3 MIDI 1",
                     "MIDIOUT2 (LPMiniMK3 MIDI) 2"]
        in_ports = ["LPMiniMK3 MIDI 0",
                    "MIDIIN2 (LPMiniMK3 MIDI) 1"]

        parser = SystemMidiPortParser(in_ports, out_ports)
        self.assertEqual(len(parser.found_clients),
                         1,
                         "Client count mismatch.")

        # DAW IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "LPMiniMK3 MIDI",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_name,
                         "LPMiniMK3 MIDI 0",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].system_port_name,
                         "LPMiniMK3 MIDI 0",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "LPMiniMK3 MIDI",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_name,
                         "MIDIIN2 (LPMiniMK3 MIDI) 1",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_number,
                         2,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].system_port_name,
                         "MIDIIN2 (LPMiniMK3 MIDI) 1",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "LPMiniMK3 MIDI",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_name,
                         "LPMiniMK3 MIDI 1",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].system_port_name,
                         "LPMiniMK3 MIDI 1",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "LPMiniMK3 MIDI",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_name,
                         "MIDIOUT2 (LPMiniMK3 MIDI) 2",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_number,
                         2,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_index,
                         2,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].system_port_name,
                         "MIDIOUT2 (LPMiniMK3 MIDI) 2",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

    def test_parse_midi_ports_mac(self):
        os.environ["SIMULATED_OS"] = "Darwin"
        out_ports = ["Launchpad Mini MK3 LPMiniMK3 DAW Out",
                     "Launchpad Mini MK3 LPMiniMK3 MIDI Out"]
        in_ports = ["Launchpad Mini MK3 LPMiniMK3 DAW In",
                    "Launchpad Mini MK3 LPMiniMK3 MIDI In"]

        parser = SystemMidiPortParser(in_ports, out_ports)
        self.assertEqual(len(parser.found_clients),
                         1,
                         "Client count mismatch.")

        # DAW IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW In",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW In",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_number,
                         2,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_number,
                         3,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_number,
                         4,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

    # NOTE: Unverified
    def test_parse_midi_ports_two_clients_linux(self):
        os.environ["SIMULATED_OS"] = "Linux"
        out_ports = ["Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",
                     "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1",
                     "reface CP:reface CP MIDI 1 24:0",
                     "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 38:0",
                     "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 38:1",
                     ]
        in_ports = ["Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",
                    "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1",
                    "reface CP:reface CP MIDI 1 24:0",
                    "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 38:0",
                    "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 38:1"]

        parser = SystemMidiPortParser(in_ports, out_ports)
        self.assertEqual(len(parser.found_clients),
                         2,
                         "Client count mismatch.")

        # DAW IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DA",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_number,
                         0,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI IN port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MI",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DA",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_number,
                         0,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 36:0",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI OUT port
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         36,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MI",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 36:1",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # DAW IN port, client 2
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         38,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DA",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].port_number,
                         0,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].port_index,
                         3,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 38:0",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI IN port
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         38,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MI",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].port_index,
                         4,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 38:1",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         38,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DA",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].port_number,
                         0,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].port_index,
                         3,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 DA 38:0",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI OUT port
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         38,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MI",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].port_index,
                         4,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].system_port_name,
                         "Launchpad Mini MK3:Launchpad Mini MK3 LPMiniMK3 MI 38:1",  # noqa
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

    def test_parse_midi_ports_two_clients_mac(self):
        os.environ["SIMULATED_OS"] = "Darwin"
        in_ports = ["Launchpad Mini MK3 LPMiniMK3 DAW In",
                    "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                    "reface CP",
                    "Launchpad Mini MK3 LPMiniMK3 DAW In",
                    "Launchpad Mini MK3 LPMiniMK3 MIDI In"]
        out_ports = ["Launchpad Mini MK3 LPMiniMK3 DAW Out",
                     "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                     "reface CP",
                     "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                     "Launchpad Mini MK3 LPMiniMK3 MIDI Out"]

        parser = SystemMidiPortParser(in_ports, out_ports)
        self.assertEqual(len(parser.found_clients),
                         2,
                         "Client count mismatch.")

        # DAW IN port, client 1
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW In",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW In",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port, client 1
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_number,
                         2,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].port_index,
                         0,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[1].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI IN port, client 1
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_number,
                         3,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[2].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI OUT port, client 1
        self.assertEqual(parser.found_clients[0].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[0].client_number,
                         1,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_number,
                         4,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].port_index,
                         1,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[0].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # DAW IN port, client 2
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         2,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW In",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].port_number,
                         1,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].port_index,
                         3,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW In",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[0].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # DAW OUT port, client 2
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         2,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].port_number,
                         2,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].port_index,
                         3,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 DAW Out",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[1].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")

        # MIDI IN port, client 2
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         2,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].port_number,
                         3,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].port_index,
                         4,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI In",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[2].direction,
                         MidiPort.IN,
                         "Direction mismatch.")

        # MIDI OUT port, client 2
        self.assertEqual(parser.found_clients[1].client_name,
                         "Launchpad Mini MK3",
                         "Client name mismatch.")
        self.assertEqual(parser.found_clients[1].client_number,
                         2,
                         "Client number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                         "Port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].port_number,
                         4,
                         "Port number mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].port_index,
                         4,
                         "Port index mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].system_port_name,
                         "Launchpad Mini MK3 LPMiniMK3 MIDI Out",
                         "System port name mismatch.")
        self.assertEqual(parser.found_clients[1].ports[3].direction,
                         MidiPort.OUT,
                         "Direction mismatch.")


if __name__ == '__main__':
    unittest.main()
