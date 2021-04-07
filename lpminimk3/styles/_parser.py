import os
import json
import jsonschema
from ..midimessages import Constants


class GlyphDictionary:
    def __init__(self, json_filename, schema_filename):
        self._filename = os.path.abspath(json_filename)
        self._data = self._load(json_filename)
        schema = self._load(schema_filename)
        self._validate(self._data, schema)

    def __iter__(self):
        for glyph, bitmap_data in self._data.items():
            yield glyph, bitmap_data

    def __contains__(self, unicode):
        return unicode in self._data['glyphs']

    def __getitem__(self, unicode):
        return self._data['glyphs'][unicode]

    def __repr__(self):
        return 'GlyphDictionary(filename=\'{}\')'.format(self.filename)

    def __str__(self):
        return (str(self._data['glyphs'])
                if self._data
                else '')

    @property
    def filename(self):
        return self._filename

    def _load(self, filename):
        data = None
        with open(os.path.abspath(filename)) as f:
            data = json.load(f.read())
        return data

    def _validate(self, data, schema):
        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError:
            raise ValueError('Invalid JSON file format.')


class LightingConfig:
    def __init__(self, *, on_state=None, off_state=None):
        self._on_state = on_state
        self._off_state = off_state

    def __repr__(self):
        return 'LightingConfig(\'{}\')'.format(self._name)

    def __str__(self):
        return self._data

    @property
    def on_state(self):
        return (self._on_state
                if self._on_state
                else [Constants.DEFAULT_COLOR_ID])

    @property
    def off_state(self):
        return (self._off_state
                if self._off_state
                else [Constants.LightingMode.OFF])


class BitConfig:
    def __init__(self, name=None, config_data=None):
        self._name = name
        self._data = config_data

    def __repr__(self):
        return 'BitConfig(\'{}\')'.format(self._name)

    def __str__(self):
        return self._data

    @property
    def lighting_type(self):
        return (self._data['lighting_type']
                if self._data and 'lighting_type' in self._data
                else Constants.LightingType.STATIC)

    @property
    def name(self):
        return (self._name
                if self._name
                else 'default')

    @property
    def lighting_data(self):
        return (LightingConfig(self.lighting_type,
                               **self._data['lighting_data'])
                if self._data and 'lighting_data' in self._data
                else Constants.LightingType.STATIC)


class BitmapConfig:
    def __init__(self, config_data):
        self._data = config_data

    def __getitem__(self, name):
        if name in self._data:
            return self._data[name]
        return BitConfig()


class Character:
    def __init__(self, glyph, bitmap):
        self._glyph = glyph
        self._bitmap = bitmap

    @property
    def glyph(self):
        return self._glyph

    @property
    def bitmap(self):
        return self._bitmap

    def __repr__(self):
        return 'Character(\'{}\')'.format(self._glyph)

    def __str__(self):
        return self._glyph
