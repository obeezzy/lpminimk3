"""
Match MIDI messages with incoming MIDI events.
"""

from .midi_messages import Lighting


class Match:
    """
    A set of rules for filtering MIDI events.
    """

    def contains(self, message):
        return False


class ButtonMatch(Match):
    """
    A set of rules for filtering button events.
    """
    NOTE_HEADER = 0x90
    CC_HEADER = 0xb0

    def __init__(self, buttons, type):
        self._buttons = buttons
        self._type = type.lower().replace('|', '_')

    def contains(self, message):
        """
        Returns `True` if message `message` is a valid button
        message, otherwise returns `False`.
        """
        button_messages = self._determine_messages()
        for button_message in button_messages:
            if message == button_message:
                return True
        return False

    def _determine_messages(self):
        messages = []
        for button in self._buttons:
            header = (ButtonMatch.NOTE_HEADER
                      if button.parent == 'grid'
                      else ButtonMatch.CC_HEADER)
            if self._type == 'press':
                messages.append(Lighting(header, button.midi_value, 0x7f).data)  # noqa
            elif self._type == 'release':
                messages.append(Lighting(header, button.midi_value, 0x0).data)  # noqa
            elif self._type == 'press_release':
                messages.append(Lighting(header, button.midi_value, 0x7f).data)  # noqa
                messages.append(Lighting(header, button.midi_value, 0x0).data)  # noqa
        return messages
