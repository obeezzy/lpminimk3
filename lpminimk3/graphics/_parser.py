import os
import json
import jsonschema
from ..midi_messages import Constants


class GlyphDictionary:
    def __init__(self,
                 json_filename, *,
                 schema_filename='./schema/glyph.schema.json'):
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
        return f"GlyphDictionary(filename='{os.path.basename(self.filename)}')"

    def __str__(self):
        return (str(self._data['glyphs'])
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


class BitmapDocument:
    def __init__(self,
                 json_filename, *,
                 schema_filename='./schema/bitmap.schema.json'):
        assert json_filename
        self._filename = self._determine_abspath(json_filename)
        self._data = self._load(json_filename)
        schema = self._load(schema_filename)
        self._validate(self._data, schema)

    def __repr__(self):
        return f"BitmapDocument(filename='{self.filename}')"

    def __str__(self):
        return repr(self)

    @property
    def filename(self):
        return self._filename

    @property
    def bitmap_data(self):
        return self._data['bitmap']['data']

    @property
    def bitmap_config(self):
        return self._data['bitmap']['config']

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


class MovieDocument:
    def __init__(self,
                 json_filename, *,
                 schema_filename='./schema/movie.schema.json'):
        assert json_filename
        self._filename = self._determine_abspath(json_filename)
        self._data = self._load(json_filename)
        schema = self._load(schema_filename)
        self._validate(self._data, schema)

    def __repr__(self):
        return f"MovieDocument(filename='{self.filename}')"

    def __str__(self):
        return repr(self)

    @property
    def filename(self):
        return self._filename

    @property
    def framerate(self):
        return self._data['framerate']

    @property
    def frames(self):
        return self._data['frames']

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


class LightingType:
    FLASH = 'flash'
    PULSE = 'pulse'
    RGB = 'rgb'

    def __init__(self, type_str):
        self._type_str = type_str

    @property
    def midi_value(self):
        if self._type_str == LightingType.FLASH:
            return Constants.LightingType.FLASH
        elif self._type_str == LightingType.PULSE:
            return Constants.LightingType.PULSE
        elif self._type_str == LightingType.RGB:
            return Constants.LightingType.RGB
        return Constants.LightingType.STATIC


class LightingColor:
    def __init__(self, *, id=0, rgb=[0, 0, 0]):
        self._id = id
        self._rgb = rgb

    def __repr__(self):
        return ('LightingColor('
                f'id={self.id}, '
                f'rgb={self.rgb})')

    def __str__(self):
        return repr(self)

    @property
    def id(self):
        return self._id

    @property
    def rgb(self):
        return self._rgb


class LightingState:
    def __init__(self, state=None):
        self._color = (LightingColor(**state['color'])
                       if state
                       else LightingColor())

    def __repr__(self):
        return ('LightingState('
                f'color_id={self._color.id}, '
                f'rgb={self._color.rgb})')

    def __str__(self):
        return repr(self)

    @property
    def color(self):
        return self._color


class LightingData:
    def __init__(self,
                 lighting_type, *,
                 on_state=None,
                 off_state=None):
        self._lighting_type = lighting_type
        self._on_state = (LightingState(on_state)
                          if on_state
                          else None)
        self._off_state = (LightingState(off_state)
                           if off_state
                           else None)

    def __repr__(self):
        return ("LightingData("
                f"on_state={self.on_state}, "
                f"off_state={self.off_state})")

    def __str__(self):
        return repr(self)

    @property
    def on_state(self):
        return self._on_state

    @property
    def off_state(self):
        return self._off_state


class BitConfig:
    def __init__(self, name=None, config_data=None):
        self._name = name
        self._data = config_data

    def __repr__(self):
        return f"BitConfig(name='{self._name}')"

    def __str__(self):
        return repr(self)

    @property
    def lighting_type(self):
        return (LightingType(self._data['lighting_type']).midi_value
                if self._data and 'lighting_type' in self._data
                else Constants.LightingType.STATIC)

    @property
    def name(self):
        return self._name

    @property
    def lighting_data(self):
        if self._data:
            return LightingData(self.lighting_type,
                                **self._data.get('lighting_data'))
        return None


class BitmapConfig:
    def __init__(self, config_data):
        self._data = self._load(config_data)

    def __getitem__(self, name):
        if self._data and name in self._data:
            return self._data[name]
        return BitConfig()

    def _load(self, config_data):
        config_dict = {}
        if config_data:
            for button_name, data in config_data.items():
                config_dict[button_name] = BitConfig(button_name, data)
        return config_dict

    def __repr__(self):
        return f"BitmapConfig('{str(self._data)}')"

    def __str__(self):
        return repr(self)
