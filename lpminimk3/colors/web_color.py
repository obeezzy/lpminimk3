import os
import json
import jsonschema


class WebColorDictionary:
    def __init__(self,
                 json_filename, *,
                 schema_filename='./web_colors.schema.json'):
        self._filename = self._determine_abspath(json_filename)
        self._data = self._load(json_filename)
        schema = self._load(schema_filename)
        self._validate(self._data, schema)

    def __contains__(self, color):
        return color in self._data

    def __getitem__(self, color):
        return self._data[color]

    def __repr__(self):
        return ("WebColorDictionary("
                f"filename='{os.path.basename(self.filename)}')")

    def __str__(self):
        return (str(self._data)
                if self._data
                else '')

    @property
    def filename(self):
        return self._filename

    @property
    def data(self):
        return self._data

    def _load(self, filename):
        data = None
        filename = self._determine_abspath(filename)
        with open(filename) as f:
            data = json.load(f)
        return data

    def _validate(self, data, schema):
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError:
            raise ValueError('Invalid JSON file format.')

    def _determine_abspath(self, filename):
        if not os.path.isabs(filename):
            current_dir = os.path.dirname(__file__)
            return os.path.join(current_dir, filename)
        return filename


class WebColor:
    def __init__(self, name):
        self._web_dictionary = WebColorDictionary('./web_colors.json')
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def rgb(self):
        return self._web_dictionary[self._name]['rgb']

    @property
    def rgb_normalized(self):
        r, g, b = self._web_dictionary[self._name]['rgb']
        return (r >> 1, g >> 1, b >> 1)

    @property
    def hex(self):
        return self._web_dictionary[self._name]['hex']
