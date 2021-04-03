"""
Match MIDI messages with incoming MIDI events.
"""

from .midi_messages import SysExMessages


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

    def __init__(self, buttons, event_type):
        self._buttons = buttons
        self._event_type = event_type.lower().replace('|', '_')

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
            if self._event_type == 'press':
                messages.append(SysExMessages.lighting_message(header, button.midi_value, 0x7f))  # noqa
            elif self._event_type == 'release':
                messages.append(SysExMessages.lighting_message(header, button.midi_value, 0x0))  # noqa
            elif self._event_type == 'press_release':
                messages.append(SysExMessages.lighting_message(header, button.midi_value, 0x7f))  # noqa
                messages.append(SysExMessages.lighting_message(header, button.midi_value, 0x0))  # noqa
        return messages
