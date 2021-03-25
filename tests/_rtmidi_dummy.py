API_RTMIDI_DUMMY = 5


class MidiIn:
    def __init__(self, api=API_RTMIDI_DUMMY, client_name=None):
        self._api = api
        self._client_name = client_name
        self._port_number = -1
        self._port_name = ''
        self._port_open = False

    def ignore_types(self, *args, **kwargs):
        pass

    def is_port_open(self):
        return self._port_open

    def get_current_api(self):
        return self._api

    def open_port(self, port_number, port_name):
        self._port_number = port_number
        self._port_name = port_name
        self._port_open = True

    def open_virtual_port(self, port_number, port_name):
        self._port_number = port_number
        self._port_name = port_name
        self._port_open = True

    def close_port(self):
        self._client_name = ''
        self._port_number = -1
        self._port_name = ''
        self._port_open = False

    def set_client_name(self, client_name):
        self._client_name = client_name

    def set_port_name(self, port_name):
        self._port_name = port_name

    def get_client_name(self):
        return self._client_name

    def get_port_name(self):
        return self._port_name


class MidiOut:
    def __init__(self, api=API_RTMIDI_DUMMY, client_name=None):
        self._api = api
        self._client_name = client_name
        self._port_number = -1
        self._port_name = ''
        self._port_open = False

    def get_current_api(self):
        return self._api

    def is_port_open(self):
        return self._port_open

    def open_port(self, port_number, port_name):
        self._port_number = port_number
        self._port_name = port_name
        self._port_open = True

    def open_virtual_port(self, port_number, port_name):
        self._port_number = port_number
        self._port_name = port_name
        self._port_open = True

    def close_port(self):
        self._port_number = -1
        self._port_name = ''
        self._port_open = False

    def set_client_name(self, client_name):
        self._client_name = client_name

    def set_port_name(self, port_name):
        self._port_name = port_name

    def get_client_name(self):
        return self._client_name

    def get_port_name(self):
        return self._port_name

    def send_message(self, message):
        pass
