"""Region of LEDs on a matrix.
"""

from abc import ABC


class Region(ABC):
    """A collection of LEDs on a matrix.
    """

    def __len__(self):
        return len(self.button_names)

    @property
    def button_names(self):
        """Button names for region.
        """
        pass


class Labeled(Region):
    """All labeled buttons on a panel.
    """

    @Region.button_names.getter
    def button_names(self):
        """Button names for labeled region.
        """
        return ['up',
                'down',
                'left',
                'right',
                'session',
                'drums',
                'keys',
                'user',
                'logo',
                'scene_launch_1',
                'scene_launch_2',
                'scene_launch_3',
                'scene_launch_4',
                'scene_launch_5',
                'scene_launch_6',
                'scene_launch_7',
                'stop_solo_mute']


class Custom(Region):
    """Custom region.
    """

    def __init__(self, button_names):
        """Constructs a region whose buttons
        can be specified through `button_names`.

        Parameters
        ----------
        button_names : list of str
            List of buttons to be included
            in region.
        """
        self._button_names = button_names

    @Region.button_names.getter
    def button_names(self):
        """Button names for custom region.
        """
        return self._button_names
