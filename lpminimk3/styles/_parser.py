import os
import json
import jsonschema
from ..midi_messages import Constants


class GlyphDictionary:
    def __init__(self, json_filename, schema_filename):
        self._filename = self._determine_abspath(json_filename)
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
            current_dir = os.path.abspath(os.path.dirname(__file__))
            return os.path.join(current_dir, filename)
        return filename


class LightingConfig:
    DEFAULT_ON_STATE = 1
    DEFAULT_OFF_STATE = 0

    def __init__(self, lighting_type, *, on_state=None, off_state=None):
        self._lighting_type = lighting_type
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
                else [LightingConfig.DEFAULT_ON_STATE])

    @property
    def off_state(self):
        return (self._off_state
                if self._off_state
                else [LightingConfig.DEFAULT_OFF_STATE])


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
        if self._data:
            return LightingConfig(self.lighting_type,
                                  **self._data.get('lighting_data'))
        return None


class BitmapConfig:
    def __init__(self, config_data):
        self._data = config_data

    def __getitem__(self, name):
        if self._data and name in self._data:
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
