import os
import re
import platform
from collections import namedtuple
from .utils import MidiPort


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


class SystemMidiPortParser:
    """System-specific way of parsing MIDI port names.
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

        self._parser = None
        system = os.environ.get("SIMULATED_OS", platform.system())
        if system == 'Windows':
            self._parser = _SystemMidiPortParserWindows(lp_in_ports,
                                                        in_ports,
                                                        lp_out_ports,
                                                        out_ports)
        elif system == 'Darwin':
            self._parser = _SystemMidiPortParserMac(lp_in_ports,
                                                    in_ports,
                                                    lp_out_ports,
                                                    out_ports)
        else:
            self._parser = _SystemMidiPortParserLinux(lp_in_ports,
                                                      in_ports,
                                                      lp_out_ports,
                                                      out_ports)

    @property
    def found_clients(self):
        """Found clients.
        """
        return self._parser.found_clients


class _SystemMidiPortParserWindows:
    def __init__(self,
                 lp_in_ports,
                 in_ports,
                 lp_out_ports,
                 out_ports):
        self._found_clients = []
        self._parse(lp_in_ports, in_ports, MidiPort.IN)
        self._parse(lp_out_ports, out_ports, MidiPort.OUT)

    def _parse(self, lp_ports, ports, direction):
        for index, system_port_name in enumerate(lp_ports):
            match = re.match(r'^(.+)\s\d+$', system_port_name)
            match2 = re.match(r'(.+)\s\((.+)\)\s\d+$', system_port_name)  # noqa

            client_name = ''
            port_name = ''
            client_number = int(index + 1)
            port_number = int(index + 1)

            if match and not match2:
                client_name = match.group(1)
                port_name = system_port_name
            elif match2:
                client_name = match2.group(2)
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


class _SystemMidiPortParserMac:
    def __init__(self,
                 lp_in_ports,
                 in_ports,
                 lp_out_ports,
                 out_ports):
        self._found_clients = []
        self._mapped_in_ports = []
        self._mapped_out_ports = []

        self._map_ports(in_ports, out_ports)
        self._parse(lp_in_ports, lp_out_ports)

    def _map_ports(self, in_ports, out_ports):
        for index, system_port_name in enumerate(in_ports):
            match = re.match(r'(.+\sMK3)\s(.+)$', system_port_name)
            if match:
                self._mapped_in_ports.append(index)

        for index, system_port_name in enumerate(out_ports):
            match = re.match(r'(.+\sMK3)\s(.+)$', system_port_name)
            if match:
                self._mapped_out_ports.append(index)

    def _parse(self, in_lp_ports, out_lp_ports):
        assert len(in_lp_ports) == len(out_lp_ports), "Launchpad port count mismatch"
        assert len(self._mapped_in_ports) == len(self._mapped_out_ports), "Mapped port count mismatch"

        partial_client = None  # Client with only half its ports appended
        for index, (in_system_port_name, out_system_port_name) in enumerate(zip(in_lp_ports, out_lp_ports)):
            match = re.match(r'(.+\sMK3)\s(.+)$', in_system_port_name)

            client_number = len(self._found_clients) + 1
            client_name = (match.group(1)
                           if partial_client is None
                           else partial_client.client_name)

            in_port_data = PortData(in_system_port_name,
                                    1 if partial_client is None else 3,
                                    self._mapped_in_ports[index],
                                    in_system_port_name,
                                    MidiPort.IN)
            out_port_data = PortData(out_system_port_name,
                                     2 if partial_client is None else 4,
                                     self._mapped_out_ports[index],
                                     out_system_port_name,
                                     MidiPort.OUT)
            if partial_client is None:
                client_data = ClientData(client_name,
                                         client_number,
                                         [in_port_data, out_port_data])
                partial_client = client_data
            else:
                partial_client.ports.append(in_port_data)
                partial_client.ports.append(out_port_data)
                self._found_clients.append(partial_client)
                partial_client = None

    @property
    def found_clients(self):
        return self._found_clients


class _SystemMidiPortParserLinux:
    def __init__(self,
                 lp_in_ports,
                 in_ports,
                 lp_out_ports,
                 out_ports):
        self._found_clients = []
        self._parse(lp_in_ports, in_ports, MidiPort.IN)
        self._parse(lp_out_ports, out_ports, MidiPort.OUT)

    def _parse(self, lp_ports, ports, direction):
        for index, system_port_name in enumerate(lp_ports):
            match = re.match(r'(.+):(.+)\s(\d+):(\d+)$', system_port_name)  # noqa
            client_name = ''
            port_name = ''
            client_number = int(index + 1)
            port_number = int(index + 1)

            if match:
                client_name = match.group(1)
                port_name = match.group(2)
                client_number = int(match.group(3))
                port_number = int(match.group(4))

            port_index = ports.index(system_port_name)
            port_data = PortData(port_name,
                                 port_number,
                                 port_index,
                                 system_port_name,
                                 direction)
            existing_client_data = list(filter(lambda c: c.client_number == client_number,  # noqa
                                        self._found_clients))
            existing_client_data = (existing_client_data[0]
                                    if len(existing_client_data) > 0
                                    else None)
            if not existing_client_data:
                client_data = ClientData(client_name,
                                         client_number,
                                         [port_data])
                self._found_clients.append(client_data)
            else:
                existing_client_data.ports.append(port_data)

    @property
    def found_clients(self):
        return self._found_clients
