"""Web color.

This module is an abstraction over web colors. The full list
of colors can be found on
`Wikipedia <https://en.wikipedia.org/wiki/Lists_of_colors>`_.

Example
-------
Set color of LED "0x0" to "amethyst":
>>> import lpminimk3
>>> lp = lpminimk3.find_launchpads()[0]
>>> lp.open()
>>> lp.mode = 'prog'
>>> lp.grid.led('0x0').color = lpminimk3.colors.WebColor("amethyst")
"""

import os
import json
import jsonschema


class WebColorDictionary:
    """Web color dictionary.
    """
    def __init__(self,
                 json_filename, *,
                 schema_filename='./web_colors.schema.json'):
        """Constructs a web color dictionary from JSON file
        `json_filename`.

        Parameters
        ----------
        json_filename : str
            Name of JSON file to parse.
        schema_filename : str, optional
            Name of schema JSON file.
        """
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
        """File name.
        """
        return self._filename

    @property
    def data(self):
        """Data.
        """
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
    """Web color.

    Example
    -------
    Set color of LED "0x0" to "amethyst":
    >>> import lpminimk3
    >>> from lpminimk3.colors import WebColor
    >>> lp = lpminimk3.find_launchpads()[0]
    >>> lp.open()
    >>> lp.mode = 'prog'
    >>> lp.grid.led('0x0').color = WebColor("amethyst")
    """

    """Web color dictionary.
    """
    COLOR_DICT = WebColorDictionary('./web_colors.json')

    def __init__(self, name):
        """Constructs a web color with name `name`.

        Parameters
        ----------
        name : str
            Name of web color.
        """
        self._name = name

    @property
    def name(self):
        """Name.
        """
        return self._name

    @property
    def rgb(self):
        """RGB value.
        Its possible values range from 0 to 255.
        """
        return WebColor.COLOR_DICT[self._name]['rgb']

    @property
    def rgb_normalized(self):
        """RGB value, normalized to work on a Launchpad.
        Its possible values range from 0 to 127.
        """
        r, g, b = self.COLOR_DICT[self._name]['rgb']
        return (r >> 1, g >> 1, b >> 1)

    @property
    def hex(self):
        """Hex color.
        """
        return self.WEB_COLOR_DICTIONARY[self._name]['hex']
